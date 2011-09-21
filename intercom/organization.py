import gdata
import settings
from gdata.alt.appengine import run_on_appengine
from gdata.apps.service import AppsService
from google.appengine.api import memcache


SIG_METHOD = gdata.auth.OAuthSignatureMethod.HMAC_SHA1


def users():
    results = memcache.get("roster")

    if results is not None:
        return results

    apps = AppsService(domain=settings.CONSUMER_KEY, source="intercom")
    apps.SetOAuthInputParameters(
        SIG_METHOD, settings.CONSUMER_KEY,
        consumer_secret=settings.CONSUMER_SECRET,
        two_legged_oauth=True, requestor_id=settings.REQUESTOR)
    feed = apps.GetGeneratorForAllUsers()

    results = []

    def get_person(person):
        return {
            "name": "%s %s" % (person.name.given_name,
                person.name.family_name),
            "id": person.login.user_name,
            }

    for entry in feed:
        for person in entry.entry:
            results.append(get_person(person))

    memcache.add("roster", results, 14400)
    return results
