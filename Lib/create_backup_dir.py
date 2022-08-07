import pyftp as ftp_lib
import main_auto as mn
import os

bk = "./BACKUPS"

new_ftp = ftp_lib.PyFTP(mn.host_name, mn.username, mn.password, port=21)
new_ftp.connect()

def create():
    if not os.path.exists(bk):
        new_ftp.mkdir(bk)
    for x in range(1, 11):
        if new_ftp.isdir(f'{bk}/BACKUP{x}') is False:
            new_ftp.mkdir(f'{bk}/BACKUP{x}')
            print(f'folder made! : /BACKUP{x}')


create()





