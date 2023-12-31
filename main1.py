from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import os
import psutil


def get_partitions():
    """
    Function to get all partitions on the system.

    Returns:
        list: A list of tuples containing partition information.
              Each tuple consists of (device, mountpoint, fstype).
    """
    partitions = psutil.disk_partitions(all=True)
    # Get the list of disk partitions on the system using psutil.disk_partitions().

    partition_info = []  # List to store the partition information as tuples.
    for partition in partitions:
        device = partition.device  # Get the partition device (e.g., '/dev/sda1', 'C:')
        partition_info.append(device)
        # Append the tuple containing partition information to the list.

    return partition_info
    # Return the list containing tuples of partition information (device, mountpoint, fstype).


def scan_files(starting_directory):
    # Function to scan the filesystem and retrieve file and directory information.
    file_list = []  # List to store file and directory details.

    for root, dirs, files in os.walk(starting_directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_list.append((file_name, file_path, "file"))  # Append file details to the list.
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            file_list.append((dir_name, dir_path, "directory"))  # Append directory details to the list.

    return file_list  # Return the list containing file and directory information.


def save_to_csv(file_list, csv_file):
    # Function to save the scanned files into a CSV file.
    df = pd.DataFrame(file_list, columns=['Name', 'Address', 'Type'])  # Create a DataFrame from the file_list.

    # Convert the 'Name' column to strings to avoid AttributeError in search.
    df['Name'] = df['Name'].astype(str)

    df.sort_values("Type", axis=0, ascending=True, inplace=True, na_position='first')  # Sort the DataFrame by 'Type'.
    df.to_csv(csv_file, index=False)  # Save the DataFrame to the CSV file without index.


def search(event):  # event is for hit the Enter key
    # Function to search for matching results in the CSV file.
    matching_results = []
    global partitions
    try:
        df = pd.read_csv('list_of_files.csv')  # Read the CSV file into a DataFrame for search.
    except FileNotFoundError:
        file_list = scan_files(partitions)  # Scan files if the CSV file is not found.
        save_to_csv(file_list, 'list_of_files.csv')
        df = pd.read_csv('list_of_files.csv')  # Read the CSV file into a DataFrame after saving.

    user_input = searchbox_entry.get()  # Get the user input for search.
    for index, row in df.iterrows():
        try:
            name = row['Name'].lower()  # Convert the 'Name' value to lowercase.
            if user_input in name:
                matching_results.append((row['Name'], row['Address'], row['Type']))  # Append matching results to list.
        except AttributeError:
            continue  # Ignore the row and continue with the next one.
    result_list.delete(*result_list.get_children())
    if matching_results:
        for index, row in enumerate(matching_results, 1):
            result_list.insert("", "end",
                               values=(index, row[0], row[1], row[2]))  # Insert matching results into the Treeview.
    else:
        messagebox.showerror(title="Oops!",
                             message="No matching results found.")  # Print a message if no matching results are found.


partitions = get_partitions()
all_files = []
for partition in partitions:
    files = scan_files(partition)  # Scan files from the starting directory.
    all_files.extend(files)

csv_file = 'list_of_files.csv'  # CSV file to store the scanned file list.
save_to_csv(all_files, csv_file)  # Save the scanned files to the CSV file.

# ------------------ UI&UX -------------------- #
BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title('FileHunt🏹')
window.config(padx=20, pady=20, background=BACKGROUND_COLOR, width=500, height=500)
window.bind('<Return>', search)

canvas = Canvas(width=100, height=100)
logo_img = PhotoImage(file='logo.png')  # Load the logo image.
canvas.create_image(50, 50, image=logo_img)

canvas.grid(row=0, column=0)

logo_label = Label(text='FileHunt!🏹', font=('Arial', 40, 'italic'))  # Create a label for the title.
logo_label.grid(row=0, column=1)

searchbox_entry = Entry(width=70)  # Create an entry widget for user input.
searchbox_entry.grid(row=1, column=0, columnspan=2)
searchbox_entry.focus()

search_btn = Button(text='Search', command=search)  # Create a button for search.
search_btn.grid(row=1, column=2, padx=5, pady=5)

result_list = ttk.Treeview(window,
                           columns=("Index", "Name", "Address", "Type"))  # Create a Treeview for displaying results.
result_list.heading("Index", text="Index")  # Set headings for columns.
result_list.heading("Name", text="Name")
result_list.heading("Address", text="Address")
result_list.heading("Type", text="Type")
result_list["show"] = "headings"
result_list.column("Index", width=50)  # Adjust the width of the "Index" column
result_list.grid(row=2, column=0, columnspan=3, padx=5)

window.mainloop()  # Start the main event loop for the GUI.
