import base64
import csv
import datetime
import dateutil.parser as parser
import http
import json
import os
import urllib.request

# TODO: Generate CSV file
# TODO: Create docstring
# TODO: Make fetch_kintone_records as module
# TODO: Write test code

# TODO: Modify the codes to allow user to pass these variables from arguments or envitonmental variables
DOMAIN = os.environ['KINTONE_DOMAIN']
USERNAME = os.environ['KINTONE_USERNAME']
PASSWORD = os.environ['KINTONE_PASSWORD']
BASE64ENCODED = base64.b64encode('{}:{}'.format(USERNAME, PASSWORD).encode('utf-8')).decode('utf-8')
PATH = '/k/v1/records.json'
URL = 'https://{}{}'.format(DOMAIN, PATH)

def fetch_kintone_records(fields, app, query):
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

def create_record_dirs(records, fields):
  record_dirs = []
  for record in records:
    record_dir = {}
    for code, value in record.items():
      record_dir[code] = {
        'index': fields.index(code)
      }
      field_type = value['type']
      field_value = value['value']
      if field_value:
        # Datetime
        if field_type in {'CREATED_TIME', 'DATETIME', 'UPDATED_TIME'}:
          field_value_trimmed = field_value[:-1] # 末尾の Z を削除
          formatted = parser.parse(field_value_trimmed).strftime('%Y-%m-%d %H:%M:%S')
        # Time
        elif field_type in {'TIME'}:
          formatted = parser.parse(field_value).strftime('%H:%M:%S')
        # Fields that may have line break
        elif field_type in {'MULTI_LINE_TEXT'}:
          formatted = field_value.replace('\n', '')
        # Fields that may have multiple values
        elif field_type in {'CATEGORY', 'CHECK_BOX', 'USER_SELECT', 'GROUP_SELECT', 'MULTI_SELECT', 'ORGANIZATION_SELECT'}:
          formatted = ' '.join(field_value)
        # Exclude some fields
        elif field_type in {'FILE', 'SUBTABLE'}:
          formatted = 'None'
        else:
          formatted = field_value
      else:
        if field_type in {'FILE', 'SUBTABLE'}:
          formatted = 'None'
        else:
          formatted = 'null'
      record_dir[code]['value'] = formatted
    record_dirs.append(record_dir)
  return record_dirs

def create_header(record_dirs):
  return

def create_rows(record_dirs):
  return

def main():
  # TODO: Pass these variables from arguments
  # TODO: Pass a list of fields and convert it into array
  fields = ['$id', '時刻', '作成日時', '文字列__複数行_', 'チェックボックス', '添付ファイル']
  app = 43185
  query = ''
  filename = 'test.csv'

  records = fetch_kintone_records(fields, app, query)
  record_dirs = create_record_dirs(records, fields)
  print(record_dirs)
  # header = create_header(record_dirs)
  # rows = create_rows(record_dirs)

  # with open(filename, 'w') as f:
  #   writer = csv.writer(f, lineterminator='\n')
  #   writer.writerow(header)
  #   writer.writerows(rows)

if __name__ == '__main__':
  main()
