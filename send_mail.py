from datetime import datetime, timedelta
import json
import time
import os 
json_file_path = 'time_dict_new.json'
json_file_path_new = 'time_dict.json'

# Initialize the last modification timestamp
last_modified_timestamp = datetime.now()

def on_json_file_change(data):
    # Replace this with the code you want to run when the JSON file changes
    print("JSON file has changed. Data:", data)

while True:
    try:
        # Get the current modification timestamp of the JSON file
        current_timestamp = os.path.getmtime(json_file_path_new)
        
        # Check if the file has been modified since the last check
        if current_timestamp != last_modified_timestamp:
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            
            last_modified_timestamp = current_timestamp
            
            with open(json_file_path_new, 'r') as json_file:
                data_new = json.load(json_file)
            on_json_file_change(data)
            # print("data",data)
            # print("data_new",data_new)
        d_data={}
        for key in data:
            d_data[key] = datetime.strptime(data[key], '%H:%M:%S')
        d_data_new={}
        for key in data_new:
            d_data_new[key] = datetime.strptime(data_new[key], '%H:%M:%S')

        # Calculate the time difference for each key
        time_differences = {}
        new_dict={}
        for key in data:
            time_diff = d_data_new[key] - d_data[key]
            time_differences[key] = time_diff
            # if time_diff >= timedelta(seconds=9):
            #     print("Time difference", time_diff)
            # if time_diff <= timedelta(seconds=9):
            #     new_dict['topic']=d_data[key]
            #     new_dict['data_not_come']=datetime.now().strftime("%H:%M:%S")
            #     json_file_store_path='history.json'
                # if new_dict is not None:
                #     with open(json_file_store_path,'w') as json_file_new:
                #         json.dump(new_dict, json_file_store_path)

                # if datetime.strftime(new_dict['data_not_come'])-datetime.strptime(data[key], '%H:%M:%S')>=timedelta(seconds=9):
                #     print("data_not_come")

        # print("new_dict",new_dict)



        # print(time_differences)
        new_dict={}
        json_file_store_path='history.json'
        # Print the time differences
        for key, value in time_differences.items():
            print(f"{key}: {value}")
            new_dict['topic']=key

            if value >= timedelta(seconds=9):
                new_dict['not_come_mail_time']=datetime.now().strftime("%H:%M:%S")
                
            print(new_dict)
        with open(json_file_store_path,'w') as json_file_store_path:
                json.dump(new_dict, json_file_store_path)






        
        # Sleep for a specified interval before checking again
        time.sleep(1)  # Adjust the interval as needed
    except KeyboardInterrupt:
        break