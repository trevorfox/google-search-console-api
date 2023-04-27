#!/usr/bin/python

import pickle
from checker import check
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Script setup
# Enter the URL for the site that you want to query as it is shown in Google Search Console
# For this example, the ERROR_CATEGORY is used to query specific types of crawl errors
SITE_URL = 'https://example.com/'
ERROR_CATEGORY = 'notFound'

# There are only two OAuth Scopes for the Google Search Console API
# For the most part, all you will need is `.readonly` but if you want to modify data in Google Search Console,
# you will need the second scope listed below
# Read more: https://developers.google.com/webmaster-tools/search-console-api-original/v3/
OAUTH_SCOPE = ('https://www.googleapis.com/auth/webmasters.readonly', 'https://www.googleapis.com/auth/webmasters')

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# This is auth flow walks you through the Web auth flow the first time you run the script and stores the credentials in a file
# Every subsequent time you run the script, the script will use the "pickled" credentials stored in config/credentials.pickle
try:
    credentials = pickle.load(open("config/credentials.pickle", "rb"))
except (OSError, IOError) as e:
    flow = InstalledAppFlow.from_client_secrets_file('config/client_secret.json', scopes=OAUTH_SCOPE)
    credentials = flow.run_local_server()
    pickle.dump(credentials, open("config/credentials.pickle", "wb"))

webmasters_service = build('webmasters', 'v3', credentials=credentials)

# Query your Google Search Console data
gsc_data = webmasters_service.urlcrawlerrorssamples().list(siteUrl=SITE_URL, category=ERROR_CATEGORY, platform='web').execute()
records = gsc_data['urlCrawlErrorSample']

# Iterate through all your URL records
# Each record is in the form:
"""
{
    'last_crawled': '2018-02-28T04:26:55.000Z',
    'pageUrl': 'plan-check-kitchen-bar-los-angeles',
    'urlDetails': {
        'linkedFromUrls': [
            'https://postmates.com/la/plan-check-kitchen-bar-los-angeles'
        ]
    }
}
"""

for record in records:
    check(SITE_URL, ERROR_CATEGORY, record)
