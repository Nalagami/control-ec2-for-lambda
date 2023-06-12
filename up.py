import json
import os
import time

import boto3


def lambda_handler(event, context):
    print("[START] Starting Script")

    instance_id = os.environ["INSTANCE_ID"]

    start_ec2(instance_id)

    print("[FINISH] Finished runnning script")

    return


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
                print(status_response)
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


# def custom_print(msg):
#     if isinstance(msg, str):
#         msg = msg
#         print(msg)
#     else:
#         magjson = json.dump(msg, sort_keys=True, default=str)
#         msg = '[RESPONSE]\n' + magjson
#         print('[RESPONSE]' + magjson)

#         # Time since EPOCH
#     time_stamp_milli = int(round(time.time() * 1000))

#     # Initialize
#     log_group_name = os.environ['CUSTOM_LOG_GROUP']
#     log_stream_name = os.environ['CUSTOM_LOG_STREAM']
#     region = os.environ['AWS_REGION']
#     log_client = boto3.client('logs', region_name=region)

#     # Obtain the response and check if token exists

#     print(log_client.describe_log_streams(
#         logGroupName=log_group_name,
#         logStreamNamePrefix=log_stream_name)['logStreams'])

#     log_response = log_client.describe_log_streams(
#         logGroupName=log_group_name,
#         logStreamNamePrefix=log_stream_name)['logStreams']
#     found = 0
#     for key in log_response.keys():
#         if key == 'uploadSequenceToken':
#             found = 1

#     # If token does exists, the log already has entry; append to the log with token
#     if found:
#         upload_token = log_client.describe_log_streams(
#             logGroupName=log_group_name,
#             logStreamNamePrefix=log_stream_name)['logStreams'][0]['uploadSequenceToken']
#         response = log_client.put_log_events(
#             logGroupName=log_group_name,
#             logStreamName=log_stream_name,
#             logEvents=[
#                 {
#                     'timestamp': time_stamp_milli,
#                     'message': msg
#                 }
#             ],
#             sequenceToken=upload_token
#         )
#     # This log entry is absolutely new, therefore no need of token
#     else:
#         response = log_client.put_log_events(
#             logGroupName=log_group_name,
#             logStreamName=log_stream_name,
#             logEvents=[
#                 {
#                     'timestamp': time_stamp_milli,
#                     'message': msg
#                 }
#             ]
#         )
