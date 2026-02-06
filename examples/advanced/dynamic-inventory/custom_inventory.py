#!/usr/bin/env python3
"""
Custom Dynamic Inventory Script Example

This script demonstrates how to create a custom dynamic inventory
for Ansible. It can be adapted to fetch inventory from any source
(API, database, CMDB, etc.)

Requirements:
- Python 3
- Output valid JSON in Ansible's expected format

Usage:
  ./custom_inventory.py --list
  ./custom_inventory.py --host <hostname>
"""

import json
import argparse


def get_inventory():
    """
    Build and return the complete inventory.
    
    In a real implementation, this would fetch data from your
    infrastructure source (API, database, etc.)
    """
    inventory = {
        # All hosts must be in at least one group
        'all': {
            'hosts': ['web1.example.com', 'web2.example.com', 'db1.example.com'],
            'vars': {
                'ansible_user': 'ubuntu',
                'ansible_python_interpreter': '/usr/bin/python3'
            }
        },
        
        # Define groups
        'webservers': {
            'hosts': ['web1.example.com', 'web2.example.com'],
            'vars': {
                'http_port': 80,
                'https_port': 443
            }
        },
        
        'databases': {
            'hosts': ['db1.example.com'],
            'vars': {
                'db_port': 5432
            }
        },
        
        # Group of groups
        'production': {
            'children': ['webservers', 'databases'],
            'vars': {
                'environment': 'production'
            }
        },
        
        # Host-specific variables
        '_meta': {
            'hostvars': {
                'web1.example.com': {
                    'ansible_host': '192.168.1.10',
                    'server_id': 1
                },
                'web2.example.com': {
                    'ansible_host': '192.168.1.11',
                    'server_id': 2
                },
                'db1.example.com': {
                    'ansible_host': '192.168.1.20',
                    'server_id': 10,
                    'db_master': True
                }
            }
        }
    }
    
    return inventory


def get_host_vars(hostname):
    """
    Return variables for a specific host.
    
    This is called with --host parameter.
    You can return empty dict {} as _meta includes all hostvars.
    """
    inventory = get_inventory()
    return inventory['_meta']['hostvars'].get(hostname, {})


def main():
    parser = argparse.ArgumentParser(description='Custom Ansible Dynamic Inventory')
    parser.add_argument('--list', action='store_true',
                       help='List all hosts')
    parser.add_argument('--host', action='store',
                       help='Get variables for a specific host')
    
    args = parser.parse_args()
    
    if args.list:
        # Return full inventory
        inventory = get_inventory()
        print(json.dumps(inventory, indent=2))
    elif args.host:
        # Return host-specific variables
        hostvars = get_host_vars(args.host)
        print(json.dumps(hostvars, indent=2))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
