# Cloud Infrastructure Deployment Python AWS

Write a simple index.html webpage.  
Write a python script to perform the following actions.  
- Push the above created index.html file to your git repository.
- Create an ec2 fleet with an auto-scaling group of a minimum of 2 instances and a maximum of 3 instances using boto3.
- Install and configure an Apache webserver on each of these instances.
- Use Paramiko to fetch the index.html file from your git repository to instances. Move it to a /var/www/html directory.
- Do not include any credentials/access keys in your code.

Testing:
- Terminate one instance using CLI or console and test if the auto-scaling group is working.
- You should be able to access the webpage using public IP or AWS provided public DNS.
