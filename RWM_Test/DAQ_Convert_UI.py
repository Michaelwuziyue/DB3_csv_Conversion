import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import sys

def show_description():
    # create a new window
    description_window = tk.Toplevel(window)
    description_window.title("Program Description")
    description_window.iconbitmap('Saltworks-logomark.ico')
    description_window_width = 400
    description_window_height = 200
    
    # calculate the center position of the screen
    x = window.winfo_screenwidth() // 2 - description_window_width // 2
    y = window.winfo_screenheight() // 2 - description_window_height // 2
    description_window.geometry(f"{description_window_width}x{description_window_height}+{x}+{y}")
    # create a label with the program description
    description_label_text = "This program does: \n1. Read the mapping.csv file and extract the \nID vs Instrument Name columns,save as Mapping_Temp.csv. \n2. Read the input DAQ.csv extract the TimeStamp, ID, Value columns \nand save to DAQ_Temp.csv. \n3. In DAQ_Temp.csv, convert the timestamp into date and time. \n4. Swap the ID column inside DAQ_Temp with Name column in \nMapping_Temp.csv and export. \n- 2023-03-27 Michael Wu"
    description_label = tk.Label(description_window, text=description_label_text)
    description_label.pack(pady=20)
    
    # create a button to close the window
    close_button = tk.Button(description_window, text="Close", command=description_window.destroy)
    close_button.place(relx=0.5, rely=0.9, anchor="center")
    #close_button.pack()
""" 
def show_successful():
    successful_window = tk.Toplevel(window)
    successful_window.title("Message")
    successful_window.iconbitmap('Saltworks-logomark.ico')
    # calculate the center position of the screen
    x = window.winfo_screenwidth() // 2 - successful_window_width // 2
    y = window.winfo_screenheight() // 2 - successful_window_height // 2
    successful_window.geometry(f"{successful_window_width}x{successful_window_height}+{x}+{y}")
    successful_label = tk.Label(successful_window, text="Write Successfully!")
    successful_label.pack(pady=20)

def show_fail():
    fail_window = tk.Toplevel(window)
    fail_window.title("Message")
    fail_window.iconbitmap('Saltworks-logomark.ico')
    fail_label = tk.Label(fail_window, text="Write Failed!")
    fail_label.pack(pady=20)
"""
# Define a function to handle button click event
def process_csv():

        # Prompt the user to select the input file
    input_mapping_file = filedialog.askopenfilename(title="Select mapping file", filetypes=[("CSV files", "*.csv")])

    # Prompt the user to select the input file
    input_file = filedialog.askopenfilename(title="Select input file", filetypes=[("CSV files", "*.csv")])

    # Prompt the user to enter the output file name
    output_file = filedialog.asksaveasfilename(title="Save output file as", filetypes=[("CSV files", "*.csv")], defaultextension=".csv")

    # Process Mapping.csv
    with open(input_mapping_file, 'r') as mapping_file, open('Mapping_Temp.csv', 'w', newline='') as mapping_output_file:
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
    with open(input_file, 'r') as daq_file, open('DAQ_Temp.csv', 'w', newline='') as daq_output_file:
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
            new_pk_timestamp = ((pk_timestamp / 60 / 60 / 24 / 10000000) - 109207)
            
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
            # Write the modified row to the output file
            daq_writer.writerow(new_row_DAQ)


     # Open Mapping_Temp.csv to create a dictionary of pk_Key to Name mappings
    with open('Mapping_Temp.csv', 'r', newline='') as mapping_file:
        mapping_reader = csv.DictReader(mapping_file)
        mapping_dict = {row['pk_Key']: row['Name'] for row in mapping_reader}

    # Open DAQ_Temp.csv and create a new file for writing
    with open('DAQ_Temp.csv', 'r', newline='') as daq_temp_file, \
            open(output_file, 'w', newline='') as daq_final_file:

        # Create a reader and writer object for DAQ_Temp.csv and DAQ_Final.csv
        daq_reader = csv.reader(daq_temp_file)
        daq_writer = csv.writer(daq_final_file)

        # Write the header row to the output file
        header = next(daq_reader)
        header[1] = 'Name'  # Rename the pf_fk_Id column to Name
        daq_writer.writerow(header)
        
        
        for row in daq_reader:
            # Get the ID from the current row
            id = row[1]

            # Look up the corresponding Name in the mapping dictionary
            name = mapping_dict.get(id, '')

            # Replace the ID with the Name in the row
            row[1] = name

            # Write the modified row to the output file
            daq_writer.writerow(row)  
        
        
        
        
        
"""
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

 """       

# Create a GUI window
window = tk.Tk()# create a Tkinter window

def on_closing():
    # Ask the user if they want to exit
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # Close the GUI window
        window.destroy()
        # Terminate the application
        sys.exit()
    
window.protocol("WM_DELETE_WINDOW", on_closing)
# set the window title and logo
window.title("Saltworks Technologies - DAQ Convert v1.0")
window.iconbitmap('Saltworks-logomark.ico')
# Set the size of the main window
window.geometry('500x200')

# Get the width and height of the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the x and y position of the main window
x = (screen_width - window.winfo_reqwidth()) / 2
y = (screen_height - window.winfo_reqheight()) / 2

# Set the position of the main window
window.geometry('+%d+%d' % (x, y))

# Create a label widget
label_text = "1. ***You need DB Browser and Mapping file ready. \n2. Make sure the Mapping .csv file that's exported from DB browser in .csv format. \n3. Choose the DAQ .csv file that's exported from DB browser in .csv format. \n4. Choose the output .csv file. \n"
label = tk.Label(window, text=label_text)
label.place(relx=0.5, rely=0.3, anchor = 'center')

# Create a button widget
button = tk.Button(window, text="Select File", command=process_csv)
button.place(relx=0.5, rely=0.6, anchor = 'center')

# create another button
button2 = tk.Button(window, text="Program Description", command=show_description)

# position the button on the window
button2.place(relx=0.5, rely=0.8, anchor="center")




#button.pack()
# Display the window
window.mainloop()        
"""        
if __name__ == '__main__':
    process_csv()
""" 
