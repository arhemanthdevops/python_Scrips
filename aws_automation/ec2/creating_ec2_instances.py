import boto3
from tabulate import tabulate

def create_ec2_instance():
    try:
        # Get user input for AWS resources
        region = input("Enter your AWS region: ")
        key_name = input("Enter the name of the key pair to use: ")
        security_group = input("Enter the name of the security group to use: ")
        ami_id = input("Enter the AMI ID to use: ")
        instance_type = input("Enter the instance type (e.g., t2.micro): ")

        # Prompt for the number of instances
        instance_count = int(input("How many EC2 instances do you want to create? "))

        # Initialize a boto3 session
        session = boto3.Session(region_name=region)
        ec2 = session.client('ec2')

        # Launch EC2 instances
        response = ec2.run_instances(
            ImageId=ami_id,
            MinCount=instance_count,
            MaxCount=instance_count,
            KeyName=key_name,
            InstanceType=instance_type,
            SecurityGroups=[security_group]
        )

        # Prepare data for tabulate
        table_data = []
        for instance in response['Instances']:
            instance_id = instance['InstanceId']
            public_ip = instance.get('PublicIpAddress', 'N/A')
            private_ip = instance['PrivateIpAddress']

            table_data.append([instance_id, public_ip, private_ip])

        # Display information about created instances in a table
        headers = ["Instance ID", "Public IP", "Private IP"]
        print("EC2 Instances Created:")
        print(tabulate(table_data, headers, tablefmt="grid"))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_ec2_instance()

