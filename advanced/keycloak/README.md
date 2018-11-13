
https://medium.com/@mrbobbytables/kubernetes-day-2-operations-authn-authz-with-oidc-and-a-little-help-from-keycloak-de4ea1bdbbe


```bash

# delete old files and clean up `/etc/hosts`
rm ./pki/keycloak*
rm ./kubeconfigs/*
sudo vi /etc/hosts


# [ make sure minikube according to main README.md is running ]


# declare some keycloak variables
KEYCLOAK_ADDRESS="keycloak.local-two"
# KEYCLOAK_ADDRESS="keycloak.devlocal"
KEYCLOAK_AUTH_REALM="k8s"
KEYCLOAK_CLIENT_ID="oidckube"

# here?
minikube_ip=$(minikube ip)
echo "$minikube_ip $KEYCLOAK_ADDRESS" | sudo tee --append /etc/hosts


# test dns lookup
ping $KEYCLOAK_ADDRESS
minikube ssh ping $KEYCLOAK_ADDRESS

kubectl create -f https://k8s.io/examples/admin/dns/busybox.yaml
kubectl exec -ti busybox -- nslookup $KEYCLOAK_ADDRESS


# render `keycloak.json`
cat <<EOF > ./pki/keycloak.json
{
  "CN": "keycloak",
  "hosts": ["$KEYCLOAK_ADDRESS"],
  "key": {
    "algo": "ecdsa",
    "size": 256
  }
}
EOF

# generate all these pem files
cfssl gencert -initca "pki/ca-csr.json" | cfssljson -bare "pki/keycloak-ca" -
cfssl gencert \
  -ca="pki/keycloak-ca.pem" \
  -ca-key="pki/keycloak-ca-key.pem" \
  -config="pki/ca-config.json" \
  -profile=server \
  "pki/keycloak.json" | cfssljson -bare "pki/keycloak"


# place `keycloak-ca.pem` on the machine for the kube-apiserver
cat "./pki/keycloak-ca.pem" | ssh -t -q -o StrictHostKeyChecking=no \
  -i "$(minikube ssh-key)" "docker@$(minikube ip)" 'cat - | sudo tee /var/lib/minikube/certs/keycloak-ca.pem'

  # this does not work :-/
  # cat "./pki/keycloak-ca.pem" | minikube ssh 'cat - | sudo tee /var/lib/minikube/certs/keycloak-ca.pem'

# render oidc parameters
cat <<EOF
    - --oidc-issuer-url=https://$KEYCLOAK_ADDRESS/auth/realms/$KEYCLOAK_AUTH_REALM
    - --oidc-client-id=$KEYCLOAK_CLIENT_ID
    - --oidc-username-claim=email
    - "--oidc-username-prefix=oidc:"
    - --oidc-groups-claim=groups
    - "--oidc-groups-prefix=oidc:"
    - --oidc-ca-file=/var/lib/minikube/certs/keycloak-ca.pem
EOF


# enter minikube and add parameters to the kube-apiserver.yaml manifest
minikube ssh \
  sudo vi /etc/kubernetes/manifests/kube-apiserver.yaml

kubectl -n kube-system get pods kube-apiserver-minikube -o yaml

minikube ssh -- cat /var/lib/minikube/certs/ca.crt | openssl x509 -in - -noout -text
minikube ssh -- cat /var/lib/minikube/certs/keycloak-ca.pem | openssl x509 -in - -noout -text

kubectl -n kube-system logs -f kube-apiserver-minikube

# # ensure our ingress-controller is running
# kubectl apply -f ../ingress-nginx/ingress-nginx.yaml

# # add minikube ip to `/etc/hosts`
# minikube_ip=$(minikube ip)
# echo "$minikube_ip $KEYCLOAK_ADDRESS" | sudo tee --append /etc/hosts


# render ingress
cat <<EOF > ./manifests/ing-keycloak.yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: keycloak
  namespace: keycloak
  labels:
    app: keycloak
    component: keycloak
spec:
  rules:
  - host: $KEYCLOAK_ADDRESS
    http:
      paths:
      - backend:
          serviceName: keycloak
          servicePort: http
        path: /
  tls:
  - secretName: keycloak-cert
    hosts:
    - $KEYCLOAK_ADDRESS
EOF


kubectl -n keycloak create secret tls keycloak-cert --cert="pki/keycloak.pem" --key="pki/keycloak-key.pem" --dry-run -o yaml \
  > ./manifests/secret-keycloak-cert.yaml

# now start keycloak
kubectl apply -f ./manifests

kubectl get --all-namespaces pods --watch


# open keycloak admin and enter `keycloak`, `keycloak` and click some configuraion
xdg-open "https://$KEYCLOAK_ADDRESS/auth/admin/"

  # create realm
  #   https://$KEYCLOAK_ADDRESS/auth/admin/master/console/#/create/realm
  #     Import: k8s-realm-example.json
  #       [Create]
  #
  # https://$KEYCLOAK_ADDRESS/auth/admin/master/console/#/realms/k8s/clients
  #   Client ID:
  #     [oidckube]
  #       Credentials:
  #         [Regenerate Secret]
              KEYCLOAK_CLIENT_SECRET="put-secret-here"

  # create the users
  #   https://$KEYCLOAK_ADDRESS/auth/admin/master/console/#/realms/k8s/users
  #     [Add user]
  #       Details:
  #         Username: admin
  #         Email: admin@company.mine
  #           [Save]
  #       Credentials:
  #         New Password: keycloak
  #         Password Confirmation: keycloak
  #         Temporary: Off
  #           [Reset Password]
  #       Groups:
  #         Join: cluster-admins
  #
  #   repeat for "user" with "user@home.office" and group "cluster-users"
      
# FIXME copy ${KUBECONFIGS}pki/keycloak-ca.pem

mkdir -p ${KUBECONFIGS}pki/
cp ./pki/keycloak-ca.pem ${KUBECONFIGS}pki/keycloak-ca.pem


KEYCLOAK_CLIENT_SECRET="0408cc36-a7ac-4bcd-8e9a-e2da5560f2f3"

# KEYCLOAK_USERNAME="admin"
# KEYCLOAK_PASSWORD="keycloak"

KEYCLOAK_USERNAME="user"
KEYCLOAK_PASSWORD="keycloak"

TOKEN=$(curl -k -s "https://$KEYCLOAK_ADDRESS/auth/realms/$KEYCLOAK_AUTH_REALM/protocol/openid-connect/token" \
  -d grant_type=password \
  -d response_type=id_token \
  -d scope=openid \
  -d client_id="$KEYCLOAK_CLIENT_ID" \
  -d client_secret="$KEYCLOAK_CLIENT_SECRET" \
  -d username="$KEYCLOAK_USERNAME" \
  -d password="$KEYCLOAK_PASSWORD" \
  -d totp="$KEYCLOAK_TOTP")

echo "$TOKEN" | jq

id_token=$(echo "$TOKEN" | jq -r '.id_token')
refresh_token=$(echo "$TOKEN" | jq -r '.refresh_token')


# prepare separate kubeconfig for user
export KUBECONFIG="${KUBECONFIGS}minikube-oidc-$KEYCLOAK_USERNAME.conf"

cp ${KUBECONFIGS}minikube-cert-admin.conf "$KUBECONFIG"
kubectl config unset users


kubectl config set-credentials "minikube" \
  --auth-provider=oidc \
  --auth-provider-arg=idp-certificate-authority="${KUBECONFIGS}pki/keycloak-ca.pem" \
  --auth-provider-arg=idp-issuer-url="https://$KEYCLOAK_ADDRESS/auth/realms/$KEYCLOAK_AUTH_REALM" \
  --auth-provider-arg=client-id="$KEYCLOAK_CLIENT_ID" \
  --auth-provider-arg=client-secret="$KEYCLOAK_CLIENT_SECRET" \
  --auth-provider-arg=id-token="$id_token" \
  --auth-provider-arg=refresh-token="$refresh_token"


export KUBECONFIG=${KUBECONFIGS}minikube-cert-admin.conf 

export KUBECONFIG=${KUBECONFIGS}minikube-oidc-user.conf
kubectl delete pods busybox

export KUBECONFIG=${KUBECONFIGS}minikube-oidc-admin.conf

```


## alternative ?

```bash
# now bring up the machine!
minikube delete ; minikube start --kubernetes-version=v1.12.2 --memory=4096 --bootstrapper=kubeadm --vm-driver kvm2 \
  --extra-config=kubelet.authentication-token-webhook=true \
  --extra-config=kubelet.authorization-mode=Webhook \
  --extra-config=scheduler.address=0.0.0.0 \
  --extra-config=controller-manager.address=0.0.0.0 \
  --mount --mount-string ./pki/keycloak-ca.pem:/var/lib/minikube/certs/keycloak-ca.pem \
  --extra-config=apiserver.oidc-issuer-url=https://$KEYCLOAK_ADDRESS/auth/realms/$KEYCLOAK_AUTH_REALM \
  --extra-config=apiserver.oidc-client-id=$KEYCLOAK_CLIENT_ID \
  --extra-config=apiserver.oidc-username-claim=email \
  --extra-config=apiserver.oidc-username-prefix="oidc:" \
  --extra-config=apiserver.oidc-groups-claim=groups \
  --extra-config=apiserver.oidc-groups-prefix="oidc:" \
  --extra-config=apiserver.oidc-ca-file=/var/lib/minikube/certs/keycloak-ca.pem
```
