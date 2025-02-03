import requests
import csv
from datetime import datetime

def covert_date_to_milliseconds(date_string):
    dt = datetime.strptime(date_string, "%Y-%m-%d")
    unix_milliseconds = int(dt.timestamp() * 1000)
    return unix_milliseconds

def fetch_task_ids(start_date, end_date):
    url=f"https://api.clickup.com/api/v2/team/team_id/time_entries?start_date={start_date}&end_date={end_date}&assignee=assignee_id%assignee_id%assignee_id%assignee_id%assignee_id&include_task_tags=true&include_location_names=true&custom_task_ids=true"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "authorization_token"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:print(f"Error:{response.status_code}-{response.text}")
    return None

def parse_data(raw_data):
    parsed_data = []

    for entry in raw_data.get("data", []):
        parsed_entry = {
            "User ID": entry.get('user', {}).get('id', ""),
            "Username": entry.get('user', {}).get('username', ""),
            "Time Tracked": entry.get('duration', ""),
            "Task ID": entry.get('task', {}).get('id', ""),
            "Space Name": entry.get('task_location', {}).get('space_name', ""),
        }
        parsed_data.append(parsed_entry)

    return parsed_data

def export_tasks(parsed_data,output_file,columns):

    with open(output_file,'w') as file:
        writer = csv.DictWriter(file,fieldnames = columns)
        writer.writeheader()
        writer.writerows(parsed_data)
    print(f"Data exported successfully to {output_file}")

if __name__ == "__main__":
    input_start_date = input("Enter the start date (YYYY-MM-DD): ")
    input_end_date = input("Enter the end date (YYYY-MM-DD): ")

    unix_start_date = covert_date_to_milliseconds(input_start_date)
    unix_end_date = covert_date_to_milliseconds(input_end_date)

    raw_data = fetch_task_ids(unix_start_date,unix_end_date)
    if raw_data:
        parsed_data = parse_data(raw_data)
        output_file = "Time Tracked Data.csv"
        columns = ["User ID", "Username", "Time Tracked", 
            "Task ID", "Space Name"]
        export_tasks(parsed_data,output_file,columns)


