import ruamel.yaml
from os import path
from subprocess import Popen

compose_file = 'docker-compose-filebrowser.yaml'

def set_mount(host_dir):
    if not path.exists(host_dir):
           raise Exception(f'path {host_dir} does not exist on the host.')
    if host_dir.endswith('/'):
        host_dir = host_dir[:-1]
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    yaml.indent(sequence=3, offset=1)
    with open(compose_file, 'r') as ymlfile:
        data = yaml.load(ymlfile)
        volume = host_dir + ':/srv'
        data['services']['filebrowser']['volumes'] = [volume]
    with open(compose_file, 'w') as ymlfile:
        yaml.dump(data, ymlfile)

def set_user(username, password):
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    yaml.indent(sequence=3, offset=1)
    with open(compose_file, 'r') as ymlfile:
        data = yaml.load(ymlfile)
        volume = host_dir + ':/srv'
        data['services']['filebrowser']['build']['args']['USERNAME'] = username
        data['services']['filebrowser']['build']['args']['USERNAME'] = password
    with open(compose_file, 'w') as ymlfile:
        yaml.dump(data, ymlfile)

if __name__ == "__main__":
    host_dir = input('Path to folder to serve through Filebrowser: ')
    set_mount(host_dir)
    username = input('Please give a username: ')
    password = input('Please set a password: ')
    set_user(username, password)
    Popen(f'docker-compose -f {compose_file} build', shell=True).wait()
    Popen(f'docker-compose -f {compose_file} up -d', shell=True).wait()
    