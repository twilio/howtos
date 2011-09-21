# Twilio Intercom

Does your company use Google Apps for email and documents? If so, you can deploy a web-based intercom system, based on Twilio Client, in just minutes. The most difficult part is getting authentication keys from Google.

## Getting Your Users

For Twilio Intercom to work, it needs two pieces of information to work: the current user and the list of all memebers in your company. The latter is handled by `organization.py`.

## Google Apps

The default implementation of `organization.py` uses the [Google Apps Data API](http://code.google.com/googleapps/domain/gdata_provisioning_api_v2.0_developers_protocol.html) to get the necessary information. To access this API, you'll need to jump through some hoops on Google's end of things to allow Intercom access to your organization's members.

### Google Apps and OAuth

The `gdata` libraries use OAuth to authenticate client API calls. First, you'll need to log into your Google Apps dashboard. 

Navigate to **Advanced Options > Manage OAuth domain key third party** 

Check both boxes on the page: one next to **Enable this consumer key** and the other next to **Allow access to all APIs**.

Navigate to **Advanced Options > Manage third party OAuth Client access** 

Under Client Name, add `your-domain.com` and under One or More API Scopes, add the two feeds like this: `https://apps-apis.google.com/a/feeds/group/#readonly,https://apps-apis.google.com/a/feeds/user/#readonly`

Finally, fill in **OAuth consumer secret** and **OAuth consumer key** values in `organization.py` to finish up
