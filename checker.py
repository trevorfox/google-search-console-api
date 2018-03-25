import requests
import logging
logging.basicConfig(filename='fixed.log',level=logging.DEBUG)


# This function takes as arguments, script setup variables and record from the API query
# As it stands, it calls the URL to see what status code is returned and prints it with the status code that Googlebot saw most recently
# The commented block would then mark the URL as fixed if the URL returns a 200 response
def check(SITE_URL, ERROR_CATEGORY, record):
    verify = requests.get(SITE_URL + record['pageUrl'])
    print (verify.url)
    print (verify.status_code, record['responseCode'])

  # if (verify.status_code == 200):
  #     logging.debug(ERROR_CATEGORY + ', ' + check.url)
  #     pprint(record)
  #     fix = webmasters_service.urlcrawlerrorssamples().markAsFixed(siteUrl=SITE_URL, url=record['pageUrl'], category=ERROR_CATEGORY, platform='web').execute()
