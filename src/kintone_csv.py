import csv
import datetime
import dateutil.parser as parser
import kintone_util

# TODO: Create docstring

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
  record_dir = record_dirs[0]
  header = []
  i = 0
  while i < len(record_dir):
    for code in record_dir:
      if i == record_dir[code]['index']:
        header.append(code)
        i += 1
  return header

def create_rows(header, record_dirs):
  rows = []
  for record_dir in record_dirs:
    row = []
    for code in header:
      row.append(record_dir[code]['value'])
    rows.append(row)
  return rows

def main():
  # TODO: Pass these variables from arguments
  # TODO: Pass a list of fields and convert it into array
  fields = ['$id', '時刻', '作成日時', '文字列__複数行_', 'チェックボックス', '添付ファイル']
  app = 283
  query = ''

  records = kintone_util.get_all_records(fields, app, query)
  record_dirs = create_record_dirs(records, fields)
  header = create_header(record_dirs)
  rows = create_rows(header, record_dirs)

  # TODO: Modify filename more appropriate one
  filename = 'test.csv'
  with open(filename, 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(rows)

if __name__ == '__main__':
  main()
