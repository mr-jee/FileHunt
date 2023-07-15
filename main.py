from tkinter import *
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import os

starting_directory = "D:\\"


def scan_files(directory):
    file_list = []

    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_list.append((file_name, file_path, "file"))
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                file_list.append((dir_name, dir_path, "directory"))
    return file_list


def save_to_csv(file_list, csv_file):
    df = pd.DataFrame(file_list, columns=['Name', 'Address', 'Type'])
    df.sort_values("Type", axis=0, ascending=True, inplace=True, na_position='first')
    df.to_csv(csv_file, index=False)


files = scan_files(starting_directory)

csv_file = 'list_of_files.csv'
save_to_csv(files, csv_file)

# ------------------ UI&UX-------------------- #
BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title('FileHunt🏹')
window.config(padx=20, pady=20, background=BACKGROUND_COLOR, width=500, height=500)

canvas = Canvas(width=100, height=100)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(50, 50, image=logo_img)

canvas.grid(row=0, column=0)

logo_label = Label(text='FileHunt!🏹', font=('Arial', 40, 'italic'))
logo_label.grid(row=0, column=1)

searchbox_entry = Entry(width=70)
searchbox_entry.grid(row=1, column=0, columnspan=2)
searchbox_entry.focus()

search_btn = Button(text='Search')
search_btn.grid(row=1, column=2, padx=5, pady=5)

result_list = Listbox(width=90, height=10)
result_list.grid(row=2, column=0, columnspan=3, padx=5)

window.mainloop()
