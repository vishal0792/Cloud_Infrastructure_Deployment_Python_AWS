# Cloud-Infrastructure-Deployment-Python-AWS

The project is implemented using following steps:

Wrote a simple index.html webpage.  
Wrote a python script to perform the following actions.  
- Pushed the above created index.html file to git repository.
- Created an ec2 fleet with an auto-scaling group of a minimum of 2 instances and a maximum of 3 instances using boto3 python library
- Installed and configured an Apache webserver on each of these instances.
- Used Paramiko to fetch the index.html file from your git repository to instances. Moved it to a /var/www/html directory.
- Did not included any credentials/access keys in the code.

Testing Performed:
- Terminated one instance using CLI or console and tested if the auto-scaling group worked.
- You should be able to access the webpage using public IP or AWS provided public DNS.
