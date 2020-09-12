from webdav3.client import Client
import subprocess
from datetime import datetime, date, timedelta
import os
import configparser
from pathlib import Path
import requests

def create_backup(to_backup, encryption_password):
    print("Creating backup...")
    today = datetime.today().strftime('%d-%m-%Y')
    backup = f'{today}-backup.7z'
    cmd = f"docker run --rm --workdir /data -it -v {to_backup}:/data crazymax/7zip 7za a -tzip -p{encryption_password} -mem=AES256 {backup}"
    stdout = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].decode()
    # move file to backup folder
    cwd = os.getcwd()
    path = str(Path(cwd).parent) + f'/{backup}'
    #os.rename(path, cwd + '/home-automation/backup/' + f'/{backup}')
    backup_path = f'/home/bas/home-automation/backup/{backup}'
    os.rename(f'/home/bas/{backup}', backup_path)
    print(f"Created backup: {backup_path}")
    print("\n")
    return backup_path


def upload_to_stack(local_path, remote_path, username, password):
    print("Uploading to Stack...")
    options = {
     'webdav_hostname': f"https://{username}.stackstorage.com/remote.php/webdav/",
     'webdav_login': username,
     'webdav_password': password,
     'verbose': True
    }
    client = Client(options)
    client.verify = True
    client.upload_sync(remote_path=remote_path, local_path=local_path)
    client.check(remote_path)
    print("Uploaded backup: {}{}".format(options['webdav_hostname'], remote_path))
    print("\n")

try:
	# Parse config
	config = configparser.ConfigParser()
	config.read('config.ini')
	to_backup = config['backup']['to_backup']
	stack_username = config['stack']['username']
	stack_password = config['stack']['password']
	stack_folder = config['stack']['folder']
	encryption_password = config['backup']['encryption']

	# Script
	local_path = create_backup(to_backup, encryption_password)
	file_name = local_path.split('/')[-1]
	remote_path = stack_folder + file_name
	upload_to_stack(local_path, remote_path, stack_username, stack_password)
	print(f"Removing local backup...")
	os.remove(local_path)
	print("Removed: ", local_path)
	print("\n")
	print("Done!")
except Exception as e:
	requests.get('https://api.telegram.org/bot782498847:AAExEREvD785Y40UF0uoRXuFaovveftDyus/sendMessage?chat_id=428621077&text=Home Automation backup failed! - {}'.format(e))

# config.ini example:
# [stack]
# username=
# password=
# folder=

# [encryption]
# password=
