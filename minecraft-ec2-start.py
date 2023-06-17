import os
import time
import boto3


def lambda_handler(event, context):
    print("[START] Starting script")

    instance_id = os.environ["INSTANCE_ID"]

    start_ec2(instance_id)

    print("[FINISH] Finished runnning script")

    return


# TODO: 起動後、メッセージ書き換えとIPアドレスを表示するように変更
def start_ec2(instance_id: str) -> None:
    try:
        print("[INFO] Starting Instance: " + str(instance_id))
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
            print("[INFO] Instance is already running: " + str(instance_id))
        else:
            print(
                "[INFO] Instance was not running so called to start: "
                + str(instance_id)
            )
            response = ec2_client.start_instances(InstanceIds=[instance_id])
            print(response)
            ec2_resource.wait_until_running()
            print(
                "[INFO] Waiting for Instance to be ready: " + str(instance_id)
            )
            cont = True
            total = 0

            while cont:
                status_response = ec2_client.describe_instance_status(
                    InstanceIds=[instance_id]
                )
                if (
                    status_response["InstanceStatuses"][0]["InstanceStatus"][
                        "Status"
                    ]
                    == "ok"
                    and status_response["InstanceStatuses"][0]["SystemStatus"][
                        "Status"
                    ]
                    == "ok"
                ):
                    cont = False
                else:
                    time.sleep(10)
                    total += 10

    except Exception as error:
        print("[ERROR]" + str(error))
        return error
