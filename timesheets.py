import requests
import csv
import time

def load_data_from_existing_csv(input_file): 
    task_ids = [] 
    rows = [] 
    try:
        with open(input_file, 'r') as file:
            reader = csv.DictReader(file)
            columns = reader.fieldnames  
            for row in reader:
                task_ids.append(row["Task ID"])
                rows.append(row)  
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    return task_ids, rows, columns

def fetch_task_by_id(task_id):

    url = f"https://api.clickup.com/api/v2/task/{task_id}" 
    headers = {
        "accept": "application/json",
        "Authorization": "authorization_token"
    }
    
    while True:
        response = requests.get(url, headers=headers)
         
        if response.status_code == 429:  
            reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
            wait_time = reset_time - time.time() + 1  
            print(f"Rate limit hit. Waiting for {wait_time} seconds...")
            time.sleep(wait_time)
            continue  
              
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching task {task_id}: {response.status_code} - {response.text}")
            return None

def parse_task(task, existing_row, columns): 
    parsed_entry = existing_row.copy()  
    parsed_entry["Task ID"] = task.get("id", "")
    
    for field in task.get("custom_fields", []):
        field_name = field.get("name")
        field_value = field.get("value", None)
        type_config_options = field.get("type_config", {}).get("options", [])

        if field_name in ["Billable/Non-Billable", "*ContactName", "*Description"]:
            selected_option = next(
                (option for option in type_config_options if option.get("id") in (field_value or [])), {}
            )
            parsed_entry[field_name] = selected_option.get("label", "")
    
    return parsed_entry

def fetch_and_parse_tasks(task_ids, existing_rows, columns):
    parsed_tasks = []
    for task_id, existing_row in zip(task_ids, existing_rows):
        task_data = fetch_task_by_id(task_id)
        if task_data:
            parsed_entry = parse_task(task_data, existing_row, columns)
            parsed_tasks.append(parsed_entry)
          
    return parsed_tasks

def export_filtered_tasks(filtered_data, output_file, columns):

    sorted_data = sorted(filtered_data, key=lambda x: x.get("User ID", ""))

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(sorted_data)
    print(f"Filtered data exported successfully to {output_file}")

if __name__ == "__main__":
   
    input_task_file = "Time Tracked Data.csv"
    task_ids, original_rows, existing_columns = load_data_from_existing_csv(input_task_file)

    if task_ids:
        parsed_data = fetch_and_parse_tasks(task_ids, original_rows, existing_columns)
        columns = existing_columns + ["Billable/Non-Billable", "*ContactName", "*Description"]

        output_file = "Timesheets.csv"
        export_filtered_tasks(parsed_data, output_file, columns)
