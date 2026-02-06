# Dynamic Inventory Example
#
# Description:
#   Demonstrates using dynamic inventory to automatically discover
#   and manage infrastructure from external sources
#
# Supported Sources:
#   - AWS EC2
#   - Azure
#   - Google Cloud Platform
#   - Docker
#   - VMware
#   - Custom scripts
#
# Key Concepts:
#   - Dynamic inventory plugins
#   - Auto-discovery of infrastructure
#   - Inventory caching
#   - Grouping and filtering

## Using AWS EC2 Dynamic Inventory

1. Install boto3:
```bash
pip install boto3 botocore
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Create inventory configuration file (aws_ec2.yml):
See aws_ec2.yml in this directory

4. Test inventory:
```bash
ansible-inventory -i aws_ec2.yml --graph
ansible-inventory -i aws_ec2.yml --list
```

5. Use in playbook:
```bash
ansible-playbook -i aws_ec2.yml playbook.yml
```

## Using Azure Dynamic Inventory

1. Install Azure SDK:
```bash
pip install azure-mgmt-compute azure-mgmt-network azure-mgmt-resource
```

2. Configure Azure credentials:
```bash
az login
```

3. Create inventory configuration (azure_rm.yml)

4. Use in playbook:
```bash
ansible-playbook -i azure_rm.yml playbook.yml
```

## Using GCP Dynamic Inventory

1. Install GCP SDK:
```bash
pip install google-auth requests
```

2. Configure GCP credentials

3. Create inventory configuration (gcp_compute.yml)

4. Use in playbook:
```bash
ansible-playbook -i gcp_compute.yml playbook.yml
```

## Custom Dynamic Inventory Script

For custom sources, create a Python script that outputs JSON in the required format.
See custom_inventory.py for an example.

Make it executable:
```bash
chmod +x custom_inventory.py
```

Use it:
```bash
ansible-playbook -i custom_inventory.py playbook.yml
```

## Inventory Caching

Enable caching to improve performance:
```ini
# ansible.cfg
[inventory]
cache = yes
cache_plugin = jsonfile
cache_timeout = 3600
cache_connection = /tmp/ansible_inventory_cache
```
