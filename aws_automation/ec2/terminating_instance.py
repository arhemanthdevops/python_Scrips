import boto3
from tabulate import tabulate
from datetime import datetime, timedelta

def get_instance_name(instance):
    for tag in instance.get('Tags', []):
        if tag['Key'] == 'Name':
            return tag['Value']
    return 'N/A'

def get_running_time(instance_launch_time):
    current_time = datetime.utcnow()
    launch_time = datetime.strptime(instance_launch_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    running_time = current_time - launch_time
    return str(running_time)

def list_ec2_instances(region):
    session = boto3.Session(region_name=region)
    ec2 = session.client('ec2')

    response = ec2.describe_instances()
    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            public_ip = instance.get('PublicIpAddress', 'N/A')
            
            # Handle instances without a private IP address
            private_ip = instance.get('PrivateIpAddress', 'N/A')
            
            instance_name = get_instance_name(instance)
            launch_time = instance['LaunchTime'].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            running_time = get_running_time(launch_time)

            instances.append([instance_id, instance_name, state, public_ip, private_ip, running_time])

    headers = ["Instance ID", "Instance Name", "State", "Public IP", "Private IP", "Running Time"]
    print(tabulate(instances, headers, tablefmt="grid"))

def terminate_single_instance(region):
    instance_id = input("Enter the ID of the instance to terminate: ")
    confirm = input(f"Are you sure you want to terminate instance {instance_id}? (yes/no): ").lower()

    if confirm == 'yes':
        ec2 = boto3.client('ec2', region_name=region)
        ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"Instance {instance_id} termination initiated.")
    else:
        print("Termination canceled.")

def terminate_multiple_instances(region):
    instances_to_terminate = input("Enter the IDs of instances to terminate (comma-separated): ").split(',')
    confirm = input(f"Are you sure you want to terminate these instances? (yes/no): ").lower()

    if confirm == 'yes':
        ec2 = boto3.client('ec2', region_name=region)
        ec2.terminate_instances(InstanceIds=instances_to_terminate)
        print("Termination initiated for the specified instances.")
    else:
        print("Termination canceled.")

def terminate_all_instances(region):
    confirm = input("Are you sure you want to terminate all instances in this region? (yes/no): ").lower()

    if confirm == 'yes':
        ec2 = boto3.client('ec2', region_name=region)
        instances = ec2.describe_instances()
        instance_ids = [instance['InstanceId'] for reservation in instances['Reservations'] for instance in reservation['Instances']]

        if instance_ids:
            ec2.terminate_instances(InstanceIds=instance_ids)
            print("Termination initiated for all instances.")
        else:
            print("No instances to terminate.")
    else:
        print("Termination canceled.")

if __name__ == "__main__":
    region = input("Enter your AWS region: ")

    list_ec2_instances(region)

    choice = input("Choose an option:\n1. Terminate a single instance\n2. Terminate multiple instances\n3. Terminate all instances\n")
    
    if choice == '1':
        terminate_single_instance(region)
    elif choice == '2':
        terminate_multiple_instances(region)
    elif choice == '3':
        terminate_all_instances(region)
    else:
        print("Invalid choice. Exiting.")

