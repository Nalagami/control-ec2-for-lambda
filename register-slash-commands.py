import requests
import os

commands = [
    {
        "name": "hello",
        "type": 1,
        "description": "Lambda discord sample",
    }
]


def main():
    url = f"https://discord.com/api/v10/applications/{os.environ['APPLICATION_ID']}/commands"
    headers = {
        "Authorization": f'Bot {os.environ["BOT_ACCESS_TOKEN"]}',
    }
    payload = commands
    res = requests.post(url, headers=headers, json=payload)
    print(res.content)


if __name__ == "__main__":
    main()
