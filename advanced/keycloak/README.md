
https://medium.com/@mrbobbytables/kubernetes-day-2-operations-authn-authz-with-oidc-and-a-little-help-from-keycloak-de4ea1bdbbe


```bash
# delete old files and clean up `/etc/hosts`
rm ./server*
rm ./kubeconfig*
cat /etc/hosts

# [ make sure minikube according to main README.md is running ]


# declare some keycloak variables
KEYCLOAK_ADDRESS_INGRESS="keycloak.cluster.mini"
# KEYCLOAK_ADDRESS_SERVICE="keycloak.keycloak.svc"
KEYCLOAK_AUTH_REALM="training-advanced"
KEYCLOAK_CLIENT_ID="kube-apiserver"

# https://kubernetes.io/docs/tasks/tls/managing-tls-in-a-cluster/#download-and-install-cfssl


cat <<EOF | cfssl genkey - | cfssljson -bare server
{
  "hosts": ["$KEYCLOAK_ADDRESS_INGRESS"],
  "CN": "$KEYCLOAK_ADDRESS_INGRESS",
  "key": {
    "algo": "ecdsa",
    "size": 256
  }
}
EOF

cfssl certinfo -csr server.csr


cat <<EOF | kubectl create -f -
apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
  # name: my-svc.my-namespace
  name: keycloak
spec:
  groups:
  - system:authenticated
  request: $(cat server.csr | base64 | tr -d '\n')
  usages:
  - digital signature
  - key encipherment
  - server auth
  - client auth
EOF

kubectl get csr keycloak -o jsonpath='{.status.certificate}' \
  | base64 --decode > server.crt

cfssl certinfo -cert server.crt


kubectl -n keycloak create secret tls keycloak-tls --cert="server.crt" --key="server-key.pem" --dry-run -o yaml \
  > ./manifests/secret-keycloak-cert.yaml

kustomize build ./sources/overlay-training --output ./manifests/kustomized.yaml
# ignore this warning: "2019/03/10 21:09:56 nil value at `volumeClaimTemplates.metadata.labels` ignored in mutation attempt"

kubectl apply -f ./manifests/


curl --insecure --header 'Host: keycloak.cluster.mini' https://$(minikube ip)/
```


## Create and configure realm

```bash
# sudo docker run -ti --entrypoint bash jboss/keycloak:4.8.3.Final

sudo docker run --network=host $PWD/server.crt:/opt/jboss/server.crt -ti --entrypoint bash jboss/keycloak:4.8.3.Final

# client config

  export PATH=$PATH:/opt/jboss/keycloak/bin

  keycloak_base="https://keycloak.cluster.mini"
  realm="training-advanced"

  keytool -import -noprompt -storepass temp56 -keystore truststore.jks -file server.crt
  kcadm.sh config truststore --trustpass temp56 truststore.jks

  kcadm.sh config credentials \
    --server "$keycloak_base/auth" \
    --realm master \
    --user keycloak


# realms
  # kcadm.sh create realms -f demorealm.json

  kcadm.sh create realms -b '{
    "realm": "'"$realm"'",
    "enabled": true,
    "sslRequired": "external",
    "displayName": "Devops Gathering"
  }'

  # kcadm.sh get "realms/$realm"

# users

  # for user_email in $user_emails; do

  #   kcadm.sh create users -r "$realm" -b '{
  #     "username": "'"$user_email"'",
  #     "enabled": true,
  #     "email" : "'"$user_email"'"
  #   }'
  # done

  # kcadm.sh get users -r "$realm"

# groups

  kcadm.sh create groups -r "$realm" -b '{
    "name": "cluster-users",
    "path": "/cluster-users"
  }'

  kcadm.sh create groups -r "$realm" -b '{
    "name": "cluster-admins",
    "path": "/cluster-admins"
  }'


# clients / kube-apiserver

  kcadm.sh create clients -r "$realm" -b '{
    "clientId": "kube-apiserver",
    "enabled": true,
    "redirectUris": ["'"$keycloak_base"'/*", "https://gangway.cluster.mini/*"]
  }'

  kcadm.sh get -r "$realm" clients

  client_uuid=$(kcadm.sh get -r "$realm" clients | jq -r '.[] | select(.clientId == "kube-apiserver") | .id')
  kcadm.sh get -r "$realm" "clients/$client_uuid"

# clients / kube-apiserver / protocol-mappers

  kcadm.sh create "clients/$client_uuid/protocol-mappers/models" -r "$realm" -b '{
    "name" : "username",
    "protocol" : "openid-connect",
    "protocolMapper" : "oidc-usermodel-property-mapper",
    "config" : {
      "user.attribute" : "username",
      "claim.name" : "preferred_username",
      "jsonType.label" : "String",
      "id.token.claim" : "true",
      "access.token.claim" : "true",
      "userinfo.token.claim" : "true"
    }
  }'

  kcadm.sh create "clients/$client_uuid/protocol-mappers/models" -r "$realm" -b '{
    "name" : "email",
    "protocol" : "openid-connect",
    "protocolMapper" : "oidc-usermodel-property-mapper",
    "config" : {
      "user.attribute" : "email",
      "claim.name" : "email",
      "jsonType.label" : "String",
      "userinfo.token.claim" : "true",
      "id.token.claim" : "true",
      "access.token.claim" : "true"
    }
  }'

  kcadm.sh create "clients/$client_uuid/protocol-mappers/models" -r "$realm" -b '{
    "name" : "given name",
    "protocol" : "openid-connect",
    "protocolMapper" : "oidc-usermodel-property-mapper",
    "config" : {
      "user.attribute" : "firstName",
      "claim.name" : "given_name",
      "jsonType.label" : "String",
      "userinfo.token.claim" : "true",
      "id.token.claim" : "true",
      "access.token.claim" : "true"
    }
  }'

  kcadm.sh create "clients/$client_uuid/protocol-mappers/models" -r "$realm" -b '{
    "name" : "family name",
    "protocol" : "openid-connect",
    "protocolMapper" : "oidc-usermodel-property-mapper",
    "config" : {
      "user.attribute" : "lastName",
      "claim.name" : "family_name",
      "jsonType.label" : "String",
      "userinfo.token.claim" : "true",
      "id.token.claim" : "true",
      "access.token.claim" : "true"
    }
  }'

  kcadm.sh create "clients/$client_uuid/protocol-mappers/models" -r "$realm" -b '{
    "name" : "full name",
    "protocol" : "openid-connect",
    "protocolMapper" : "oidc-full-name-mapper",
    "config" : {
      "userinfo.token.claim" : "true",
      "id.token.claim" : "true",
      "access.token.claim" : "true"
    }
  }'

  kcadm.sh create "clients/$client_uuid/protocol-mappers/models" -r "$realm" -b '{
    "name" : "groups",
    "protocol" : "openid-connect",
    "protocolMapper" : "oidc-group-membership-mapper",
    "config" : {
      "claim.name" : "groups",
      "full.path" : "true",
      "id.token.claim" : "true",
      "access.token.claim" : "true",
      "userinfo.token.claim" : "true"
    }
  }'


# identity provider gitthub

  # kcadm.sh create identity-provider/instances \
  #   -r demorealm \
  #   -s alias=github \
  #   -s providerId=github \
  #   -s enabled=true \
  #   -s 'config.useJwksUrl="true"' \
  #   -s config.clientId=GITHUB_CLIENT_ID \
  #   -s config.clientSecret=GITHUB_CLIENT_SECRET


# client-secret

  kcadm.sh get -r "$realm" "clients/$client_uuid/client-secret"

```


## Add OIDC parameters to kube-apiserver

```bash
# render oidc parameters
cat <<EOF
    - --oidc-issuer-url=https://$KEYCLOAK_ADDRESS_INGRESS/auth/realms/$KEYCLOAK_AUTH_REALM
    - --oidc-client-id=$KEYCLOAK_CLIENT_ID
    - --oidc-username-claim=email
    - "--oidc-username-prefix=oidc:"
    - --oidc-groups-claim=groups
    - "--oidc-groups-prefix=oidc:"
    - --oidc-ca-file=/var/lib/minikube/certs/ca.crt
EOF

minikube ssh
sudo vi /etc/kubernetes/manifests/kube-apiserver.yaml
```




## Gangway

```bash
echo "$(minikube ip) gangway.cluster.mini" | sudo tee --append /etc/hosts

kubectl apply -f ../gangway/gangway.yaml

# secret session-security-key
kubectl -n gangway create secret generic session-security-key \
  --from-literal=session-security-key=$(openssl rand -base64 32)

# secret client-secret
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: client-secret
  namespace: gangway
type: Opaque
data:
  client-secret: "$(echo -n 8a743f72-d7f9-4403-972c-c62bff43bd65 | base64)"
EOF

