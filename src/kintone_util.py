import base64
import json
import os
import urllib.request

DOMAIN = os.environ['KINTONE_DOMAIN']
USERNAME = os.environ['KINTONE_USERNAME']
PASSWORD = os.environ['KINTONE_PASSWORD']
BASE64ENCODED = base64.b64encode('{}:{}'.format(USERNAME, PASSWORD).encode('utf-8')).decode('utf-8')
PATH = '/k/v1/records.json'
URL = 'https://{}{}'.format(DOMAIN, PATH)

def get_all_records(fields, app, query):
  headers = {
    'Content-Type': 'application/json',
    'X-Cybozu-Authorization': BASE64ENCODED
  }
  data = {
    'app': app,
    'fields': fields,
    'query': query
  }
  req = urllib.request.Request(
    url = URL,
    data = json.dumps(data).encode(),
    headers = headers,
    method = 'GET'
  )

  # TODO: fetch records more than 500
  try:
    res = urllib.request.urlopen(req)
  except urllib.error.HTTPError as err:
    print(err)
  except urllib.error.URLError as err:
    print(err)

  body = json.loads(res.read())
  return body['records']
