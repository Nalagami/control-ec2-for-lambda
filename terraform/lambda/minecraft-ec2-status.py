try:
    import unzip_requirements
except ImportError:
    pass

import json
import os
import requests

import boto3


def lambda_handler(event, context):
    print("[START] Starting Script")

    instance_id = os.environ["INSTANCE_ID"]

    result = status_ec2(instance_id)

    application_id = event["DISCORD_APP_ID"]
    interaction_token = event["token"]
    message = {}
    if result == 1:
        message = {"content": ":yellow_circle: ec2 stopping!"}
    elif result == 0:
        message = {"content": ":green_circle: ec2 starting!"}
    else:
        message = {"content": ":red_circle: error!"}
    payload = json.dumps(message)
    r = requests.post(
        url=f"https://discord.com/api/v10/webhooks/{application_id}/{interaction_token}",
        data=payload,
        headers={
            "Content-Type": "application/json",
        },
    )

    print("[FINISH] Finished runnning script")

    return


# TODO: statusにスタンプ(green, redなど)をつけてメッセージを送信する
# TODO: 起動時はIPアドレスを返す
def status_ec2(instance_id: str) -> None:
    try:
        region = os.environ["AWS_REGION"]
        ec2_client = boto3.client("ec2", region_name=region)
        ec2_resource = boto3.resource("ec2").Instance(instance_id)

        status_response = ec2_client.describe_instances(
            InstanceIds=[instance_id]
        )

        if (
            status_response["Reservations"][0]["Instances"][0]["State"]["Name"]
            == "running"
        ):
            print("[INFO] Instance is running: " + str(instance_id))
            return 0
        elif (
            status_response["Reservations"][0]["Instances"][0]["State"]["Name"]
            == "stopping"
            or status_response["Reservations"][0]["Instances"][0]["State"][
                "Name"
            ]
            == "stopped"
        ):
            print("[INFO] Instance is stoppping: " + str(instance_id))
            return 1
        else:
            print("[ERROR]Instance status unexpected")

    except Exception as error:
        print("[ERROR]" + str(error))
        return error
