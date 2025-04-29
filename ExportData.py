import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from datetime import datetime, timedelta

INFLUX_URL = "http://148.153.56.50:8086/"  
INFLUX_TOKEN = "UkMjRH1KMD64tV-ZjLAfVguJl-B5pjdWA7Zt-z1nhVypELkTXm7LyS1Ytg9DqNXWRbIft76qAG90L2eeg3jO6g=="     
INFLUX_ORG = "CDS" 
INFLUX_BUCKET = "DAL00"


TIME_RANGE_START = "2024-03-01T00:00:00Z"
TIME_RANGE_STOP = "2024-03-01T06:00:00Z"
WINDOW_PERIOD = "30m"
MEASUREMENT = "measurement1"
BREAKER_TAG = "1/3"
RPP_TAG = "RPP-A-1-1"

OUTPUT_FILENAME = "influxdb_export.csv"
OUTPUT_DIRECTORY = "." 

flux_query = f'''
from(bucket: "{INFLUX_BUCKET}")
  |> range(start: {TIME_RANGE_START}, stop: {TIME_RANGE_STOP})
  |> filter(fn: (r) => r["_measurement"] == "{MEASUREMENT}")
  |> aggregateWindow(every: {WINDOW_PERIOD}, fn: mean, createEmpty: false)
  |> keep(columns: ["_time", "_value", "RPP", "Breaker"])
  |> group()
  |> sort(columns: ["RPP", "Breaker", "_time"])
  |> yield(name: "mean")
'''

def export_influxdb_query_to_csv(output_dir, output_filename):
    full_output_path = os.path.join(output_dir, output_filename)
    client = None

    #creare a influxdb client with the database
    client = influxdb_client.InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG,
        timeout=30_000
    )

    #get query api
    query_api = client.query_api()

    print("Running query on bucket" +INFLUX_BUCKET)
    print(flux_query)

    #runs the query and store the data 
    #takes in the query above
    csv_iterator = query_api.query_csv(query=flux_query, org=INFLUX_ORG)

    line_count = 0
    row_index = 0
    #create and write the csv file 
    #newline='', encoding='utf-8'
    with open(full_output_path, 'w') as csvfile:
        for row_list in csv_iterator:
            if row_index >= 4:
                row_list[3] = row_list[3].replace('T', ' ').replace('Z', '')
                time = row_list[3] = 'Data record time: ' + row_list[3]
                value = row_list[4] = 'Measured electricty: ' + row_list[4]
                breaker =row_list[5] = 'Breaker: ' + row_list[5]
                rpp = row_list[6] = 'RPP: ' + row_list[6]
                part = [time, value, rpp, breaker]
                line = ",".join(part)
                csvfile.write(line + '\n')
                line_count += 1
            row_index += 1

    with open(full_output_path) as csvfile:
        print(csvfile.read())

    if line_count > 0:
        print("\nSuccessfully queried data and saved to '" + full_output_path + "'")
        print("Total lines written: " + str(line_count))
    else:
        print("\nQuery executed, but no data was returned. Empty file '" + full_output_path + "' created.")



    client.close()

    

if __name__ == "__main__":
    export_influxdb_query_to_csv(OUTPUT_DIRECTORY, OUTPUT_FILENAME)

