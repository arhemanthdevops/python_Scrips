import boto3
from datetime import datetime
from prettytable import PrettyTable

def get_running_instances():
    ec2_client = boto3.client('ec2')
    # Fetches all AWS regions
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    running_instances = []

    for region in regions:
        # Creates an EC2 client for each region
        regional_ec2_client = boto3.client('ec2', region_name=region)
        instances = regional_ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                launch_time = instance['LaunchTime']
                name_tag = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), "")
                running_instances.append({'Region': region, 'Instance ID': instance_id, 'Name': name_tag, 'Launch Time': launch_time})

    return running_instances

def display_instances(running_instances):
    table = PrettyTable(['Number', 'Region', 'Instance ID', 'Name', 'Launch Time'])
    for idx, instance in enumerate(running_instances, start=1):
        table.add_row([idx, instance['Region'], instance['Instance ID'], instance['Name'], instance['Launch Time']])
    print(table)

def stop_instances(region, instance_ids):
    regional_ec2_client = boto3.client('ec2', region_name=region)
    regional_ec2_client.stop_instances(InstanceIds=instance_ids)
    print(f"Stopping Instance {instance_ids} in {region}")

def main():
    running_instances = get_running_instances()
    if not running_instances:
        print("No running instances found.")
        return

    display_instances(running_instances)

    choice = input("Choose an option:\n1. Stop all instances\n2. Stop specific instances\nEnter your choice (1 or 2): ")

    if choice == '1':
        for instance in running_instances:
            stop_instances(instance['Region'], [instance['Instance ID']])
    elif choice == '2':
        selected_indices = input("Enter the numbers of the instances to stop (e.g., 1, 3): ")
        selected_indices = [int(idx.strip()) - 1 for idx in selected_indices.split(',')]

        for index in selected_indices:
            if 0 <= index < len(running_instances):
                instance = running_instances[index]
                stop_instances(instance['Region'], [instance['Instance ID']])
            else:
                print(f"No instance found for number: {index + 1}")
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()

