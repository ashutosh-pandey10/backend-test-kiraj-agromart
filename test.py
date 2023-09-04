'''
    Creating a custom payload using the given .csv file in order to check if the 
    appplication is working or not
'''
import csv
import requests

url = 'http://localhost:8000/api/v1/upload_csv_file/' 

timeframe = 5  # Replace with your desired timeframe

# Read data from the text file and convert it to CSV format
input_file_path = 'NIFTY_F1_Xm8mAtb.txt'  # Replace with the path to your input text file
output_file_path = 'output.csv'  # Replace with the desired path for the output CSV file

with open(input_file_path, 'r') as txt_file, open(output_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    for line in txt_file:
        # Split each line by comma and strip whitespace
        fields = [field.strip() for field in line.strip().split(',')]
        csv_writer.writerow(fields)

try:
    # Prepare the data to send in the request
    data = {
        'timeframe': timeframe,
    }
    
    # Open and attach the CSV file to the request
    with open(output_file_path, 'rb') as file:
        files = {'file': (output_file_path, file)}

        # Send the POST request with the file
        response = requests.post(url, data=data, files=files)

        # Print the response
        if response.status_code == 200:
            result = response.json()
            print('Success:')
            print(result)
        else:
            print('Error:')
            print(response.status_code, response.text)
except Exception as e:
    print('Exception:', str(e))
