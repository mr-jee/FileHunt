import psutil
import pandas as pd
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def fetch_partitions():
    """ returns the list of partitions"""
    partitions = psutil.disk_partitions(all=False)
    partition_list = []
    for partition in partitions:
        partition_list.append(partition.device)
    print(partition_list)
    return partition_list


def scan_filesystem(starting_directory):
    """Takes the starting directory and start scanning"""
    file_list = []
    for (root, dir_names, file_names) in os.walk(starting_directory):
        #       new_list = [new_item                                         for item     in list]
        file_list.extend((file_name, os.path.join(root, file_name), "file") for file_name in file_names)
        # It will only fetch the name of directory which is in index -1 when we split path by \ or /
        file_list.extend((root.split(os.sep)[-1], os.path.join(root, dir_name), "directory") for dir_name in dir_names)
    return file_list


def update_database():
    """Update the indexed files and directories"""
    if os.path.exists('./list_of_files.csv'):
        # rename it with the current date, so we can understand when file updated
        current_time = datetime.now().strftime("%Y_%m_%d")
        os.rename('list_of_files.csv', f"{current_time}.csv")
    list_of_scanned_files = []
    for partition in fetch_partitions():
        list_of_scanned_files.extend(scan_filesystem(partition))
    # convert the lis_of_scanned_file to DataFrame
    df = pd.DataFrame(list_of_scanned_files, columns=['Name', 'Address', 'Type'])
    # Convert Name column if name of a directory would be a number
    df['Name'] = df['Name'].astype(str)
    df.sort_values("Type", axis=0, ascending=True, inplace=True, na_position='last')  # Sort the DataFrame by 'Type'.
    df.to_csv("list_of_files.csv", index=False)


update_database()
