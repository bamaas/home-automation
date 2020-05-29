from webdav3.client import Client
import subprocess
from datetime import datetime, date, timedelta
import os
import configparser
from pathlib import Path

def create_backup(to_backup, encryption_password):
    print("Creating backup...")
    today = datetime.today().strftime('%d-%m-%Y')
    backup = f'{today}-backup.7z'
    cmd = f"sudo docker run --rm --workdir /data -it -v {to_backup}:/data crazymax/7zip 7za a -tzip -p{encryption_password} -mem=AES256 {backup}"
    stdout = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].decode()
    # move file to backup folder
    cwd = os.getcwd()
    path = str(Path(cwd).parent) + f'/{backup}'
    os.rename(path, cwd + f'/{backup}')
    print(f"Created backup: {backup}")
    print("\n")
    return backup


def upload_to_stack(folder, backup, username, password):
    print("Uploading to Stack...")
    print(folder)
    options = {
     'webdav_hostname': f"https://{username}.stackstorage.com/remote.php/webdav/",
     'webdav_login': username,
     'webdav_password': password,
     'verbose': True
    }
    remote_path = folder + backup
    client = Client(options)
    client.verify = True
    client.upload_sync(remote_path=remote_path, local_path=backup)
    client.check(remote_path)
    print("Uploaded backup: {}{}".format(options['webdav_hostname'], remote_path))
    print("\n")

def remove_backup(backup):
    print(f"Removing local backup...")
    os.remove(backup)
    print("Removed: ", backup)
    print("\n")

# Parse config
config = configparser.ConfigParser()
config.read('config.ini')
to_backup = config['backup']['to_backup']
stack_username = config['stack']['username']
stack_password = config['stack']['password']
stack_folder = config['stack']['folder']
encryption_password = config['backup']['encryption']

# Script
backup = create_backup(to_backup, encryption_password)
upload_to_stack(stack_folder, backup, stack_username, stack_password)
remove_backup(backup)
print("Done!")

# config.ini example:
# [stack]
# username=
# password=
# folder=

# [encryption]
# password=