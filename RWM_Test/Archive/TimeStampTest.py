import csv
import datetime


# Open the csv file
with open('Test.csv', 'r') as csvfile:
    # Create a csv reader object
    reader = csv.DictReader(csvfile)

    # Create a list to store the updated data
    updated_data = []

    # Loop through each row in the csv file
    for row in reader:
        # Get the value of the 'pk_TimeStamp' column
        timestamp = float(row['pk_TimeStamp'])

        # Convert the timestamp to seconds and subtract 109205
        seconds = (timestamp / float('60') / float('60') / float('24') / float('10000000')) - float('109205')

        # Split the seconds value into integer and fractional parts
        seconds_int = int(seconds)
        seconds_frac = seconds - seconds_int
        
        print(seconds_int)
        print(seconds_frac)
        
        # Format the integer and fractional parts
        date_format = datetime.datetime.fromtimestamp(seconds_int).strftime('%m/%d/%Y')
        seconds_frac_in_seconds = int(seconds_frac * 86400)
        time_format = datetime.datetime.utcfromtimestamp(seconds_frac_in_seconds).strftime('%H:%M:%S.%f')

        # Create a new row with the updated values
        updated_row = {
            'pk_TimeStamp': row['pk_TimeStamp'],
            'pk_TimeStamp_int': date_format,
            'pk_TimeStamp_frac': time_format,
            'pk_fk_Id': row['pk_fk_Id'],
            'Value': row['Value']
        }

        # Add the updated row to the list
        updated_data.append(updated_row)

# Open a new csv file in write mode
with open('updated_data.csv', 'w', newline='') as csvfile:
    # Define the fieldnames for the csv file
    fieldnames = ['pk_TimeStamp', 'pk_TimeStamp_int', 'pk_TimeStamp_frac', 'pk_fk_Id','Value']

    # Create a csv writer object
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the fieldnames to the csv file
    writer.writeheader()

    # Write the updated data to the csv file
    writer.writerows(updated_data)
