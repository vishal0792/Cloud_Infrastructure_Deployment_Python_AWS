
#Creation of template with EC2 userdata
#Creation of autoscaling group and attach the launch template to it

import boto3
import base64
from botocore.exceptions import ClientError

with open("newuserdata.txt", "r") as file:
    USERDATA_FILE = file.read()
    message_bytes = USERDATA_FILE.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

class Assignment7_EC2(object):
    def __init__(self, ec2_client):
        self.ec2_client=ec2_client

    def Assignment7_vpc_subnet(self):
        vpc_sb_id = ""
        output1 = self.ec2_client.describe_vpcs()
        for vpc in output1["Vpcs"]:
            if vpc['IsDefault'] == True:
                vpc_sb_id = vpc["VpcId"]
                break

        output1 = self.ec2_client.describe_subnets(Filters=[{"Name":"vpc-id", "Values": [vpc_sb_id]}])
        sub_id = output1["Subnets"][0]["SubnetId"]
        AZ = output1["Subnets"][0]["AvailabilityZone"]
        return vpc_sb_id, sub_id, AZ

    def create_ec2_security_group(self):
        secg_name = "Assignment7_Security_Group_VishalGupta"
        print("Security Group: STARTED ")
        try:
            vpc_sb_id, sub_id, AZ = self.Assignment7_vpc_subnet()
            output2 = self.ec2_client.create_security_group(
                GroupName=secg_name,
                Description="This SG is created using Python for assignment7",
                VpcId=vpc_sb_id
            )
            secg_id = output2["GroupId"]
            sg_config = self.ec2_client.authorize_security_group_ingress(
                GroupId=secg_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort':22,
                        'IpRanges':[{'CidrIp':'0.0.0.0/0'}]
                    },
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 80,
                        'ToPort': 80,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    },
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 443,
                        'ToPort': 443,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )
            print("Security Group: COMPLETED")
            return secg_id, secg_name
        except Exception as e:
           if str(e).__contains__("already exists"):
                output2 = self.ec2_client.describe_security_groups(GroupNames=[secg_name])
                secg_id = output2["SecurityGroups"][0]["GroupId"]
                print("Security Group already exists")
                return secg_id, secg_name

    def Assignment7_launch_template(self):
        print("Launch Templates : STARTED ")
        temp_name = 'Assignment7_LaunchTemplate_VishalGupta'
        try:
            secg_id, secg_name = self.create_ec2_security_group()
            output3 = self.ec2_client.create_launch_template(
                LaunchTemplateName=temp_name,
                LaunchTemplateData={
                    'ImageId': 'ami-0dc2d3e4c0f9ebd18',
                    'InstanceType' : "t2.micro",
                    'KeyName' : "Testing",
                    'UserData': base64_message,
                    'SecurityGroupIds': [secg_id]
                }
            )
            temp_id = output3['LaunchTemplate']['LaunchTemplateId']
            print("Launch Templates: COMPLETED")
            return temp_id, temp_name
        except Exception as e:
            output3 = self.ec2_client.describe_launch_templates(
                LaunchTemplateNames=[
                    temp_name,
                ]
            )
            temp_id = output3['LaunchTemplates'][0]['LaunchTemplateId']
            return temp_id, temp_name

    def Assignment7_autoscaling(self):
        print ("Autoscaling using launch template: Started")
        temp_id, temp_name = self.Assignment7_launch_template()
        vpc_sb_id, sub_id, AZ = self.Assignment7_vpc_subnet()
        client = boto3.client('autoscaling')
        output4 = client.create_auto_scaling_group(
            AutoScalingGroupName='Assignment7_AUTOSCALE',
            LaunchTemplate={
                'LaunchTemplateId': temp_id,
            },
            MinSize=2,
            MaxSize=3,
            DesiredCapacity=2,
            AvailabilityZones=[
                AZ,
            ]
        )

        if str(output4["ResponseMetadata"]["HTTPStatusCode"]) == "200":
            print("Auto Scaling Group using Launch Templates: COMPLETED")
        else:
            print("Auto Scaling Group using Launch Templates : FAILED")
        return True

try:
    ec2_client = boto3.client('ec2')
    Object1 = Assignment7_EC2(ec2_client)
    Object1.Assignment7_autoscaling()
except ClientError as e:
    print(e)