import pyftp as ftp_lib
import os, os.path
import time
# mine is 192.168.1.71
host_name = input('Enter ip: ')
username = input("Username: ")
password = input("Password: ")

# directory at ftp server will be saved as all the text after the '/'. "F:/projects".split("/")[-1] <-returns 'projects'
dirs_to_save = [
    "F:/Projects",
    "F:/Memes",
    "F:/Word & Excel",
    "F:/Adobe",
    "F:/Downloads Folder",
    "F:/Punge Downloads"
]

new_ftp = ftp_lib.PyFTP(host_name, username, password)
new_ftp.connect()

def ensure_valid_dir():
    for item in dirs_to_save:
        if os.path.exists(item) is False:
            print(f'{item} IS INVALID!!!')
        else:
            print(f'{item} IS VALID')




# dir_number is used to overwrite one of 10(by default) backup locations. A function outside of upload_dir will
# Detirmine what number to use. Which will check the write-time of each folder and will take the [-1](which will be a
# number) of the directory name, then pass that to upload_dir.
# Upload_dir will also be ran multiple times if
def upload_dir(dir_destination, dir_source):
    # stands for 'current_time'. used to time the function
    cur_time = time.time()
    # Formatted string for the remote path
    remote_path = f"./BACKUPS/{dir_destination}"
    # variable assignment not needed, but makes it look a bit nicer, easier to understand
    local_path = dir_source
    # Command to put recursively the local path to the remote path
    new_ftp.put_r(local_path, remote_path)
    # Tells us how long the function took. Rounded to two decimal places
    print(f'done in: {round(time.time() - cur_time, 2)}')

def upload_multiple_dir(dir_destination, dir_source_list):
    # To time the runtime.
    cur_time = time.time()
    # Iterate over each entry in directories to save
    for directory in dir_source_list:
        local_path = directory.split("/")[-1]
        # Formats like BACKUPS/Memes/memesubfolder, BACKUPS/Memes/scndfolder
        remote_path = f'./BACKUPS/{dir_destination}/{local_path}'
        new_ftp.mkdir(remote_path)
        print(f'directory: {directory}')
        new_ftp.put_r(directory, remote_path)
        print(f'completed: {directory}')
    print(f'done in: {round(time.time() - cur_time, 2)}')


# TODO turn the date, time -> datetime objects so they can be compared. Alternatively, find own way to compare them,
# TODO perhaps a 'line of succession'. So it goes from yr->mnth->day->hr->min->second organized top -> bottom
def print_folders():
    for entry in new_ftp.listdir("./BACKUPS"):
        date = entry[0:8]
        x = date.split('-')
        date = f"{x[2]}-{x[0]}-{x[1]}"
        time = entry[10:17]
        fake_name = entry[39:]
        direct = fake_name.split(' ')[0]
        print('-----------')
        print(f'date: {date}\ntime: {time}\ndir: {direct}\n')
        print(entry)


def time_change(ti):
    # 01:41PM
    if 'PM' in ti:
        core = int(ti[:2])
        core +=12
        return f'{core}:{ti[3:-2]}'
    else:
        return ti[:-2].replace(':', '')



def query_and_format():
    # Creating the dict to return !
    master = {}
    # Iterating over each folder in the backup server
    for entry in new_ftp.listdir("./BACKUPS"):
        # extracts the date and processes it
        old_date = entry[0:8]
        x = old_date.split('-')
        dte = x[2]+x[0]+x[1]
        date = dte.replace('-', '')
        # preps the time for being converted to a 24hr format, for proper evaluation
        old_time = time_change(entry[10:17])
        time_en = old_time.replace(":", '')
        name = entry[39:].split(' ')[0]
        # Adds and entry in the master dictionary for each backup folder
        master[name] = date+time_en
        # returns da dictionary, to use
    return master

def get_oldest_folder():
    mstr = query_and_format()
    # Gets one element in the dict, used for comparing for finding the first
    i = next(iter(mstr))
    # this is the variable that will be returned (string containing folder name)
    return_name = ''
    # Iterate over each dict entry
    for name, val in mstr.items():
        # evaluate the val.
        if val < i:
            # Sets i as the lowest date (so far!)
            i = val
            # sets return_name = to the key of the dict (the name of folder)
            return_name = name
    # Here lies the oldest folder !
    return return_name

upload_dir(get_oldest_folder(), dirs_to_save[1])
#upload_multiple_dir(get_oldest_folder(), dirs_to_save)
#print_folders()

new_ftp.close()

