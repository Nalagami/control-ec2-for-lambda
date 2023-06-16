import requests
import os
import json

commands = {
    "name": "hello",
    "description": "Lambda discord sample",
    "options": [
        {
            "name": "action",
            "description": "start/stop/status",
            "type": 3,
            "required": True,
            "choices": [
                {"name": "start", "value": "start"},
                {"name": "stop", "value": "stop"},
                {"name": "status", "value": "status"},
            ],
        },
    ],
}


def main():
    url = f"https://discord.com/api/v10/applications/{os.environ['APPLICATION_ID']}/commands"
    headers = {
        "Authorization": f'Bot {os.environ["BOT_ACCESS_TOKEN"]}',
        "Content-Type": "application/json",
    }
    res = requests.post(url, headers=headers, data=json.dumps(commands))
    print(res.content)


if __name__ == "__main__":
    main()
