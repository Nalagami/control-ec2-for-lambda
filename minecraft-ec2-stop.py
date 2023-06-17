try:
    import unzip_requirements
except ImportError:
    pass

import os
import boto3


def lambda_handler(event, context):
    print("[START] Starting Script")

    instance_id = os.environ["INSTANCE_ID"]

    stop_ec2_instances(instance_id)

    print("[FINISH] Finished stopping script")

    return


def stop_ec2_instances(instance_id: str) -> None:
    """
    Stop all instances and wait until they are stopped.
    NOTE: the wait method can only wait for one instance at a time
    This script is not expected to stop multiple instances at once
    therefore will not loop all instances to wait.
    """
    try:
        region = os.environ["AWS_REGION"]
        print("[INFO] Stopping Instance: " + str(instance_id))
        ec2_client = boto3.client("ec2", region_name=region)
        ec2_resource = boto3.resource("ec2").Instance(instance_id)
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        print(response)
        ec2_resource.wait_until_stopped()
        print(
            "[INFO] Successfully Called to Stop Instance: " + str(instance_id)
        )

    except Exception as error:
        print("[ERROR] " + str(error))
        # call_sns(str(error))
        return error
