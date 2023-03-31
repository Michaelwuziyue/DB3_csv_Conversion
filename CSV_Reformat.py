import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import glob
import os


def open_file_dialog():
    
    # ask the user to select a CSV file using a file dialog box
    file_path = filedialog.askopenfilename(title="Select a CSV file")

    # read the selected CSV file
    df = pd.read_csv(file_path)


    # create new column with calculated values
    df['pk_TimeStamp_Temp'] = (df['pk_TimeStamp'] / 60 / 60 / 24 / 10000000) - 109205

    # create new columns for integer and decimal parts of the calculated values
    df['pk_TimeStamp_Temp_BeforeDecimal'] = df['pk_TimeStamp_Temp'].astype(int)
    df['pk_TimeStamp_Temp_AfterDecimal'] = df['pk_TimeStamp_Temp'] - df['pk_TimeStamp_Temp_BeforeDecimal']
    df['pk_TimeStamp_Temp_AfterDecimal'] = df['pk_TimeStamp_Temp_AfterDecimal'].round(17)

    # convert integer column to datetime format
    df['pk_TimeStamp_Date'] = pd.to_datetime(df['pk_TimeStamp_Temp_BeforeDecimal'], unit='D', origin='1899-12-30')

    # convert decimal column to timedelta format
    df['pk_TimeStamp_Time'] = pd.to_timedelta(df['pk_TimeStamp_Temp_AfterDecimal'], unit='D')

    # save modified dataframe back to the same file
    df.to_csv(file_path, index=False)

    # Load the CSV data into a Pandas DataFrame
    data = pd.read_csv(file_path)
    # extract the directory path from the file path
    dir_path = os.path.dirname(file_path)
    # define a new file name
    new_file_name = "updated_" + os.path.basename(file_path)

    # construct the full path to the new file
    new_file_path = os.path.join(dir_path, new_file_name)

    # Pivot the data to create a tabular format
    pivoted_data = data.pivot(index=["pk_TimeStamp_Date", "pk_TimeStamp_Time"], columns="pk_fk_Id", values="Value")
    
    files_present = glob.glob(new_file_path)
    if not files_present:
        # Save the pivoted data to a new CSV file
        pivoted_data.to_csv(new_file_path)
        # display a pop-up message to confirm the save operation
        messagebox.showinfo("File Saved", f"The updated CSV file has been saved!")
    else:
        messagebox.showinfo("WARNING", f"This file already exists!")

# create a tkinter window
root = tk.Tk()

w = 800 # width for the Tk root
h = 650 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

# set the title of the window
root.title("CSV Reader")


# set the size of the window
root.geometry("400x200")

# set the style of the window
root.configure(bg="lightblue2")

# hide the tkinter window
root.withdraw()

# create a styled button widget using ttk
button = ttk.Button(root, text="Select CSV File", command=open_file_dialog)

# set the position and size of the button using the place() method
button.place(x=150, y=75, width=100, height=30)
"""
# pack the button widget
button.pack()
"""
# show the tkinter window
root.deiconify()

# run the tkinter event loop
root.mainloop()



