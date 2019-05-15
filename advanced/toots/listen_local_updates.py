from mastodon import Mastodon, CallbackStreamListener
import mastodon
import redis
import requests
import datetime
import json
import random

def dt_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return(obj.isoformat())
    else:
      TypeError("Unknown serializer")

def local_update_handler(status):
    print(status)
    r.lpush('mastodon', json.dumps(status, default=dt_serializer))


r = redis.Redis(host='redis')

# r.delete('instances')
# instances = ["mastodon.xyz","awoo.space","social.tchncs.de","hostux.social","aleph.land","mastodon.gougere.fr","social.wxcafe.net","octodon.social","social.nasqueron.org","mastodon.club","anticapitalist.party","mastodon.cloud","mstdn.io","botsin.space","mastodon.top","toot.cafe","mastodon.technology","social.targaryen.house","toot.cat","niu.moe","mastodon.at","meow.social","infosec.exchange","mastodon.host","freeradical.zone","queer.party","soc.ialis.me","framapiaf.org","mstdn.maud.io","x0r.be","mastodon.juggler.jp","kirakiratter.com","g0v.social","chaos.social","tablegame.mstdn.cloud","pawoo.net","mstdn-workers.com","mstdn.kemono-friends.info","otoya.space","mastodon.art","imastodon.net","vocalodon.net","ika.queloud.net","kinky.business","mstdn.osaka","wandering.shop","mastodont.cat","eletusk.club","mastodon.etalab.gouv.fr","mstdn.guru","ro-mastodon.puyo.jp","mimumedon.com","photodn.net","linuxrocks.online","ffxiv-mastodon.com","mastodon.sdf.org","mathtod.online","mental.social","baraag.net","eigadon.net","matchdon.com","scholar.social","mathstodon.xyz","todon.nl","elekk.xyz","mstdn.tokyocameraclub.com","acg.mn","lou.lt","music.pawoo.net","rubber.social","anarchism.space","fosstodon.org","hearthtodon.com","ichiji.social","cmx.im","knzk.me","mastodon.gamedev.place","bsd.network","mastodonten.de","layer8.space","vis.social","artalley.porn","kinkyelephant.com","mastodon.bida.im","eldritch.cafe","id.cc","sunbeam.city","witchcraft.cafe","yiff.life","qoto.org","abdl.link","bitcoinhackers.org","liberdon.com","witches.live","ruby.social","quey.org","sander.social","mastodon.eus","snouts.online","snel.social","humblr.social","fandom.ink","mingxingsex.com","sinblr.com","berries.space","bear.community","inditoot.com","hotwife.social","displaced.social","qaf.men","social.theliturgists.com","best-friends.chat"]
instances = ["mastodon.xyz","awoo.space","social.tchncs.de","hostux.social","aleph.land","mastodon.gougere.fr","social.wxcafe.net","oc.todon.fr","octodon.social","mastodon.club","anticapitalist.party","mastodon.cloud","mstdn.io","botsin.space","mastodon.top","toot.cafe","mastodon.technology","social.targaryen.house","toot.cat","niu.moe","mastodon.at","meow.social","mamot.fr","mastodon.zaclys.com","infosec.exchange","mastodon.host","freeradical.zone","queer.party","soc.ialis.me","framapiaf.org","mstdn.maud.io","x0r.be","mstdn.jp","mastodon.juggler.jp","kirakiratter.com","g0v.social","chaos.social","tablegame.mstdn.cloud","pawoo.net","mstdn-workers.com","mstdn.kemono-friends.info","otoya.space","mastodon.art","imastodon.net","vocalodon.net","ika.queloud.net","kinky.business","mstdn.osaka","wandering.shop","mastodont.cat","otogamer.me","eletusk.club","mastodon.etalab.gouv.fr","mstdn.guru","ro-mastodon.puyo.jp","mimumedon.com","photodn.net","linuxrocks.online","ffxiv-mastodon.com","mastodon.sdf.org","mathtod.online","mental.social","baraag.net","eigadon.net","matchdon.com","scholar.social","mathstodon.xyz","mastodon.social","todon.nl","elekk.xyz","mstdn.tokyocameraclub.com","acg.mn","qiitadon.com","lou.lt","music.pawoo.net","rubber.social","anarchism.space","fosstodon.org","hearthtodon.com","ichiji.social","cmx.im","knzk.me","mastodon.gamedev.place","bsd.network","mastodonten.de","layer8.space","vis.social","artalley.porn","kinkyelephant.com","mastodon.bida.im","eldritch.cafe","id.cc","sunbeam.city","witchcraft.cafe","yiff.life","qoto.org","abdl.link","bitcoinhackers.org","liberdon.com","witches.live","ruby.social","quey.org","sander.social","mastodon.eus","snouts.online","snel.social","humblr.social","fandom.ink","mingxingsex.com","sinblr.com","berries.space","bear.community","inditoot.com","hotwife.social","displaced.social","ura-mstdn.com","qaf.men","social.theliturgists.com","best-friends.chat"]

# for instance in instances:
#     r.sadd('instances', instance)


# while True:RequestException
for i in range(5):
    # api_base_url = str(r.srandmember('instances'))
    api_base_url = random.choice(instances)
    print(f"trying: {api_base_url}")
    # api_base_url = 'mastodon.social'
    # api_base_url = 'mstdn.io'
    try:
        # with r.lock(api_base_url, blocking_timeout=5) as lock:
        print(f"Using {api_base_url}")
        m = Mastodon(api_base_url=f"https://{api_base_url}")
        listener = CallbackStreamListener(local_update_handler=local_update_handler)
        m.stream_local(listener)
    #
    # except redis.exceptions.LockError:
    #     # the lock wasn't acquired
    #     # let's try a different instance
    #     print(f"{api_base_url} alreay locked")
    #
    except mastodon.MastodonError as err:
        print(f"MastodonError: {err}")

    # except requests.exceptions.ReadTimeout as err:
    #     print(f"requests.exceptions.ReadTimeout: {err}")

    except requests.exceptions.RequestException as err:
        print(f"RequestException: {err}")


# # while True:
# for i in range(5):
#     # api_base_url = str(r.srandmember('instances'))
#     api_base_url = str(r.srandmember('instances'), 'utf-8')
#     print(f"trying: {api_base_url}")
#     # api_base_url = 'mastodon.social'
#     # api_base_url = 'mstdn.io'
#     try:
#         with r.lock(api_base_url, blocking_timeout=5) as lock:
#             print(f"Using {api_base_url}")
#             m = Mastodon(api_base_url=f"https://{api_base_url}")
#             listener = CallbackStreamListener(local_update_handler=local_update_handler)
#             m.stream_local(listener)
#     #
#     except redis.exceptions.LockError:
#         # the lock wasn't acquired
#         # let's try a different instance
#         print(f"{api_base_url} alreay locked")
#     #
#     except mastodon.MastodonError as err:
#         print(f"MastodonError: {err}")

#     # except mastodon.MastodonVersionError:
#     #     print("MastodonVersionError")
#     # except mastodon.MastodonNetworkError:
#     #     print("MastodonNetworkError")


# json.loads(r.rpop('mastodon'))
# json.loads(r.brpop('mastodon')[1])
