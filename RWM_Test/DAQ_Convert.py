import csv
from datetime import datetime, timedelta

# Process Mapping.csv
with open('Mapping.csv', 'r') as mapping_file, open('Mapping_Temp.csv', 'w', newline='') as mapping_output_file:
    mapping_reader = csv.DictReader(mapping_file)

    # Define the columns we want to keep
    mapping_columns_to_keep = ['pk_Key', 'Name']

    # Write the header row to the output file
    mapping_writer = csv.DictWriter(mapping_output_file, fieldnames=mapping_columns_to_keep)
    mapping_writer.writeheader()

    # Loop over each row in the input file and write the desired columns to the output file
    for row in mapping_reader:
        new_row_mapping = {column: row[column] for column in mapping_columns_to_keep}
        mapping_writer.writerow(new_row_mapping)

# Process DAQ.csv
with open('DAQ.csv', 'r') as daq_file, open('DAQ_Temp.csv', 'w', newline='') as daq_output_file:
    daq_reader = csv.DictReader(daq_file)

    # Define the columns we want to keep
    daq_columns_to_keep = ['pk_TimeStamp', 'pk_fk_Id', 'Value']

    # Write the header row to the output file
    daq_writer = csv.DictWriter(daq_output_file, fieldnames=daq_columns_to_keep + ['Whole_Number','Decimal_Number'])
    daq_writer.writeheader()

    # Loop over each row in the input file and write the desired columns to the output file
    for row in daq_reader:
        #new_row_DAQ = {column: row[column] for column in daq_columns_to_keep}
        # Manipulate the pk_TimeStamp column
        pk_timestamp = int(row['pk_TimeStamp'])
        new_pk_timestamp = ((pk_timestamp / 60 / 60 / 24 / 10000000) - 109205)
        
        # Get the whole number and decimal part of the manipulated pk_TimeStamp
        whole_number = int(new_pk_timestamp)
        decimal_number = new_pk_timestamp - whole_number
        
        # Convert the whole_number to a date object and format it as a string
        date_str = (datetime(1900, 1, 1) + timedelta(days=whole_number)).strftime('%Y-%m-%d')

        # Convert the decimal_number to a time object and format it as a string
        time_str = (datetime.min + timedelta(seconds=decimal_number * 86400)).strftime(' %H:%M:%S')


        # Create a new row with the manipulated pk_TimeStamp column
        new_row_DAQ = {
            'Whole_Number': date_str,
            'Decimal_Number': time_str,
            'pk_fk_Id': row['pk_fk_Id'],
            'Value': row['Value'],
            'pk_TimeStamp': new_pk_timestamp
            #'Decimal_Number': '0' + str(decimal_number)[1:]
        }
        daq_writer.writerow(new_row_DAQ)

# Open Mapping_Temp.csv to create a dictionary of pk_Key to Name mappings
with open('Mapping_Temp.csv', 'r', newline='') as mapping_file:
    mapping_reader = csv.DictReader(mapping_file)
    mapping_dict = {row['pk_Key']: row['Name'] for row in mapping_reader}

# Open DAQ_Temp.csv and create a new file for writing
with open('DAQ_Temp.csv', 'r', newline='') as daq_temp_file, \
        open('DAQ_Final.csv', 'w', newline='') as daq_final_file:

    # Create a reader and writer object for DAQ_Temp.csv and DAQ_Final.csv
    daq_reader = csv.reader(daq_temp_file)
    daq_writer = csv.writer(daq_final_file)

    # Write the header row to the output file
    header = next(daq_reader)
    header[1] = 'Name'  # Rename the pf_fk_Id column to Name
    daq_writer.writerow(header)

    # Process each row in the input file
    for row in daq_reader:
        # Get the ID from the current row
        id = row[1]

        # Look up the corresponding Name in the mapping dictionary
        name = mapping_dict.get(id, '')

        # Replace the ID with the Name in the row
        row[1] = name

        # Write the modified row to the output file
        daq_writer.writerow(row)