import requests
import json
import config
import sftp

def get_uuid(username):
        response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        if response.status_code == 200:
                return response.json()['id']
        return None

def add_to_json(uuid, nickname):
    
        json_data = {
                "uuid": uuid,
                "name": nickname,
        }

        data = json.load(open("whitelist.json"))
        data.append(json_data)

        with open("whitelist.json", "w") as file:
                json.dump(data, file)

        print(f"UUID '{uuid}' и никнейм '{nickname}' успешно добавлены в JSON")

def whitelist_add(uuid, nickname):

        add_to_json(uuid, nickname)

        hostname = config.host
        port = config.port
        username = config.user
        password = config.password
        remote_filepath = 'whitelist.json'
        local_filepath = 'whitelist.json'

        sftp.upload_file_sftp(hostname, port, username, password, remote_filepath, local_filepath)