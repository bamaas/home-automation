import yaml
import os

cwd = os.getcwd()

if not os.path.exists(cwd + '/home-assistant/secrets.yaml'):
    raise Exception("Please create './home-assistant/secrets.yaml' file.")

# Get mqtt_usernamd and mqtt_password from ./home-assistant/secrets.yaml
with open(cwd + '/home-assistant/secrets.yaml') as secrets:
    content = yaml.safe_load(secrets)
    mqtt_username = content['mqtt_username']
    mqtt_password = content['mqtt_password']

# Add username and password to mqtt passwd file
with open(cwd + '/mqtt/passwd', 'w') as passwd:
    passwd.write(mqtt_username + ':' + mqtt_password)

# Add username and password to zigbee2mqtt configuration file
with open(cwd + '/zigbee2mqtt/configuration.yaml') as secrets:
    content = yaml.safe_load(secrets)
    content['mqtt']['user'] = mqtt_username
    content['mqtt']['pasword'] = mqtt_password
with open(cwd + '/zigbee2mqtt/configuration.yaml', 'w') as secrets:
    secrets.write(yaml.dump(content, default_flow_style=False))

os.system(f"sudo bash setup.bash {mqtt_username} {mqtt_password}")