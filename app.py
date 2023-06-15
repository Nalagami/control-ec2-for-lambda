try:
    import unzip_requirements
except ImportError:
    pass

import json

# from aws-lambda import (APIGatewayProxyEventV2, APIGatewayProxyResultV2 )
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

PUBLIC_KEY = ""
verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))


def lambda_handler(event: dict, context: dict):
    try:
        headers: dict = {k.lower(): v for k, v in event["headers"].items()}
        rawBody: str = event["body"]
        signature = headers.get("x-signature-ed25519", "")
        timestamp = headers.get("x-signature-timestamp", "")
        # validate the interaction
        if not verify(signature, timestamp, rawBody):
            return {
                "cookies": [],
                "isBase64Encoded": False,
                "statusCode": 401,
                "headers": {},
                "body": "",
            }

        req: dict = json.loads(rawBody)
        if req["type"] == 1:  # InteractionType.Ping
            # registerCommands()
            return {"type": 1}  # InteractionResponseType.Pong
        elif req["type"] == 2:  # InteractionType.ApplicationCommand
            # command options list -> dict
            opts = (
                {v["name"]: v["value"] for v in req["data"]["options"]}
                if "options" in req["data"]
                else {}
            )

            text = "Hello!"
        if "user" in opts:
            text = f"Hello, <@{opts['user']}>!"

        return {
            "type": 4,  # InteractionResponseType.ChannelMessageWithSource
            "data": {"content": text},
        }

    except:
        raise


def verify(signature: str, timestamp: str, body: str) -> bool:
    try:
        verify_key.verify(
            f"{timestamp}{body}".encode(), bytes.fromhex(signature)
        )
    except Exception as e:
        print(f"failed to verify request: {e}")
        return False

    return True


def command_handler(body):
    command = body["data"]["name"]

    if command == "hello":
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "type": 4,
                    "data": {
                        "content": "Hello, World.",
                    },
                }
            ),
        }
    else:
        return {"statusCode": 400, "body": json.dumps("unhandled command")}
