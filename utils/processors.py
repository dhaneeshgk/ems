''' processing utils '''
import csv

## convert csv to json
def csv_to_json(file_path=None):
    with open(file_path, newline='') as csvfile:
        key_value_records = []
        for index, records in enumerate(csv.reader(csvfile)):
            if index==0:
                keys = records
            else:
                key_value_records.append({key:value for key, value in zip(keys,records)})
    return key_value_records
