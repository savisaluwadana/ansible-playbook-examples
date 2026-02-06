# Ansible Theory & Concepts

A comprehensive guide to understanding Ansible architecture, core concepts, and best practices.

## Table of Contents

1. [Ansible Architecture](#ansible-architecture)
2. [Core Concepts](#core-concepts)
3. [Inventory Management](#inventory-management)
4. [Ansible Modules](#ansible-modules)
5. [Best Practices](#best-practices)
6. [Ansible Galaxy](#ansible-galaxy)

---

## Ansible Architecture

Ansible is an agentless automation tool that uses SSH to configure and manage systems. Understanding its architecture is crucial for effective use.

### Control Node

The **control node** is the machine where Ansible is installed and from which you run commands and playbooks.

**Requirements:**
- Python 3.8 or later
- Cannot be a Windows system
- Can manage hundreds or thousands of nodes

**Key characteristics:**
- Executes playbooks and ad-hoc commands
- Stores inventory files and configuration
- No daemons or background processes required

### Managed Nodes

**Managed nodes** (also called "hosts") are the target systems that Ansible configures and manages.

**Requirements:**
- SSH access (Linux/Unix)
- Python 2.7 or Python 3.5+ installed
- For Windows: PowerShell remoting and WinRM

**Key characteristics:**
- No Ansible-specific agent software required
- Accessed via SSH (or WinRM for Windows)
- Can be physical servers, VMs, containers, or cloud instances

### Inventory

The **inventory** is a list of managed nodes organized into groups.

**Format options:**
- INI format (default)
- YAML format
- Dynamic inventory scripts/plugins

**Example:**
```ini
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
db2.example.com

[production:children]
webservers
databases
```

### Modules

**Modules** are discrete units of code that Ansible executes on managed nodes.

**Characteristics:**
- Each module performs a specific task (install package, copy file, etc.)
- Idempotent by design (safe to run multiple times)
- Can be written in any language that returns JSON
- Python modules are most common

**Common modules:**
- `yum`, `apt` - Package management
- `copy`, `template` - File operations
- `service` - Service management
- `user`, `group` - User management

### Plugins

**Plugins** extend Ansible's core functionality on the control node.

**Types of plugins:**
- **Connection plugins**: Define how to connect to managed nodes (SSH, WinRM, Docker)
- **Inventory plugins**: Parse inventory sources
- **Lookup plugins**: Retrieve data from external sources
- **Filter plugins**: Transform data within templates
- **Callback plugins**: Control output and logging

---

## Core Concepts

### Playbooks

**Playbooks** are YAML files that define automation tasks in a structured, repeatable way.

**Structure:**
```yaml
---
- name: Playbook name
  hosts: target_hosts
  become: true  # Run as sudo
  vars:
    variable_name: value
  
  tasks:
    - name: Task description
      module_name:
        parameter: value
```

**Key features:**
- Human-readable automation blueprint
- Declarative (describe desired state, not steps)
- Can include multiple plays
- Support includes and imports for modularity

**Example:**
```yaml
---
- name: Configure web servers
  hosts: webservers
  become: true
  
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Start nginx service
      service:
        name: nginx
        state: started
        enabled: yes
```

### Tasks

**Tasks** are individual units of work within a playbook.

**Characteristics:**
- Execute modules with specific parameters
- Run sequentially by default
- Can be conditional
- Return status (ok, changed, failed, skipped)

**Anatomy of a task:**
```yaml
- name: Descriptive name of what task does
  module_name:
    parameter1: value1
    parameter2: value2
  when: condition  # Optional
  register: result_variable  # Optional
  tags:
    - tag1
    - tag2
```

### Handlers

**Handlers** are special tasks that only run when notified by other tasks.

**Use cases:**
- Restart services after configuration changes
- Reload applications
- Clear caches

**Example:**
```yaml
tasks:
  - name: Copy nginx config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: Restart nginx

handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

**Key behaviors:**
- Only run if notified
- Run once at the end of a play (even if notified multiple times)
- Run in order they're defined, not notified
- Can notify other handlers

### Roles

**Roles** provide a way to organize playbooks into reusable components.

**Directory structure:**
```
roles/
  webserver/
    tasks/
      main.yml
    handlers/
      main.yml
    templates/
      nginx.conf.j2
    files/
      index.html
    vars/
      main.yml
    defaults/
      main.yml
    meta/
      main.yml
```

**Benefits:**
- Reusability across projects
- Clear organization
- Easy sharing via Ansible Galaxy
- Simplified dependency management

**Using roles in playbooks:**
```yaml
---
- name: Configure servers
  hosts: webservers
  roles:
    - common
    - webserver
    - monitoring
```

### Variables and Facts

#### Variables

**Variables** store values that can be reused throughout playbooks.

**Variable precedence (lowest to highest):**
1. Role defaults
2. Inventory file or script group vars
3. Inventory group_vars/all
4. Playbook group_vars/all
5. Inventory group_vars/*
6. Playbook group_vars/*
7. Inventory file or script host vars
8. Inventory host_vars/*
9. Playbook host_vars/*
10. Host facts / cached set_facts
11. Play vars
12. Play vars_prompt
13. Play vars_files
14. Role vars
15. Block vars
16. Task vars
17. Include vars
18. Set_facts / registered vars
19. Role (and include_role) params
20. Include params
21. Extra vars (always win precedence)

**Defining variables:**
```yaml
# In playbook
vars:
  http_port: 80
  app_name: myapp

# In inventory
[webservers]
web1.example.com http_port=8080

# In group_vars/webservers.yml
http_port: 80
app_name: myapp

# Command line
ansible-playbook playbook.yml -e "http_port=8080"
```

**Using variables:**
```yaml
- name: Install {{ app_name }}
  apt:
    name: "{{ app_name }}"
    state: present

- debug:
    msg: "Application will run on port {{ http_port }}"
```

#### Facts

**Facts** are system information automatically gathered by Ansible.

**Gathering facts:**
```yaml
- name: Show system facts
  hosts: all
  tasks:
    - name: Display OS family
      debug:
        msg: "OS is {{ ansible_os_family }}"
    
    - name: Display IP address
      debug:
        msg: "IP is {{ ansible_default_ipv4.address }}"
```

**Common facts:**
- `ansible_os_family` - OS family (Debian, RedHat, etc.)
- `ansible_distribution` - Specific distribution (Ubuntu, CentOS)
- `ansible_hostname` - System hostname
- `ansible_default_ipv4.address` - Primary IP address
- `ansible_memtotal_mb` - Total memory in MB
- `ansible_processor_cores` - Number of CPU cores

**Disabling fact gathering:**
```yaml
---
- name: Playbook without facts
  hosts: all
  gather_facts: no
  tasks:
    - name: Some task
      ...
```

**Custom facts:**
```bash
# Create /etc/ansible/facts.d/custom.fact
[general]
environment=production
app_version=1.2.3
```

Access with: `{{ ansible_local.custom.general.environment }}`

### Conditionals and Loops

#### Conditionals

**When statements** control task execution based on conditions.

**Basic conditionals:**
```yaml
- name: Install Apache on RedHat
  yum:
    name: httpd
    state: present
  when: ansible_os_family == "RedHat"

- name: Install Apache on Debian
  apt:
    name: apache2
    state: present
  when: ansible_os_family == "Debian"
```

**Complex conditionals:**
```yaml
- name: Conditional with AND
  debug:
    msg: "This is a production web server"
  when:
    - inventory_hostname in groups['webservers']
    - environment == "production"

- name: Conditional with OR
  debug:
    msg: "Running on Ubuntu or Debian"
  when: ansible_distribution == "Ubuntu" or ansible_distribution == "Debian"
```

**Checking variables:**
```yaml
- name: Check if variable is defined
  debug:
    msg: "Variable is set"
  when: my_variable is defined

- name: Check if file exists
  stat:
    path: /etc/my_config
  register: config_file

- name: Use result of previous task
  debug:
    msg: "Config exists"
  when: config_file.stat.exists
```

#### Loops

**Loops** allow repeating tasks with different values.

**Simple loops:**
```yaml
- name: Install multiple packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - git
    - vim
```

**Loop over dictionaries:**
```yaml
- name: Create multiple users
  user:
    name: "{{ item.name }}"
    state: present
    groups: "{{ item.groups }}"
  loop:
    - { name: 'alice', groups: 'admin' }
    - { name: 'bob', groups: 'developers' }
    - { name: 'charlie', groups: 'developers' }
```

**Loop with index:**
```yaml
- name: Create files with index
  file:
    path: "/tmp/file_{{ item.0 }}.txt"
    state: touch
  loop: "{{ my_list | enumerate }}"
```

**Loop control:**
```yaml
- name: Loop with label
  debug:
    msg: "Installing {{ item.name }}"
  loop:
    - { name: 'nginx', version: '1.18' }
    - { name: 'redis', version: '6.0' }
  loop_control:
    label: "{{ item.name }}"
    pause: 2  # Pause 2 seconds between iterations
```

### Templates (Jinja2)

**Templates** use Jinja2 syntax to generate dynamic configuration files.

**Basic template syntax:**
```jinja2
{# This is a comment #}

{# Variables #}
Server name: {{ ansible_hostname }}
Port: {{ http_port }}

{# Conditionals #}
{% if ssl_enabled %}
SSL is enabled
{% else %}
SSL is disabled
{% endif %}

{# Loops #}
{% for server in web_servers %}
server {{ server }};
{% endfor %}

{# Filters #}
Uppercase: {{ app_name | upper }}
Default value: {{ undefined_var | default('fallback') }}
```

**Using templates in playbooks:**
```yaml
- name: Generate nginx config
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
  notify: Reload nginx
```

**Example template (nginx.conf.j2):**
```jinja2
user www-data;
worker_processes {{ ansible_processor_cores }};

events {
    worker_connections 1024;
}

http {
    server {
        listen {{ http_port }};
        server_name {{ server_name }};
        
        {% if ssl_enabled %}
        listen 443 ssl;
        ssl_certificate {{ ssl_cert_path }};
        ssl_certificate_key {{ ssl_key_path }};
        {% endif %}
        
        location / {
            proxy_pass http://{{ backend_server }};
        }
    }
}
```

**Common Jinja2 filters:**
- `{{ var | default('value') }}` - Default value if undefined
- `{{ list | join(', ') }}` - Join list items
- `{{ string | upper }}` - Convert to uppercase
- `{{ string | lower }}` - Convert to lowercase
- `{{ list | length }}` - Get list length
- `{{ dict | to_json }}` - Convert to JSON
- `{{ dict | to_yaml }}` - Convert to YAML

### Vault for Secrets Management

**Ansible Vault** encrypts sensitive data like passwords and keys.

**Creating encrypted files:**
```bash
# Create new encrypted file
ansible-vault create secrets.yml

# Encrypt existing file
ansible-vault encrypt vars.yml

# Edit encrypted file
ansible-vault edit secrets.yml

# View encrypted file
ansible-vault view secrets.yml

# Decrypt file
ansible-vault decrypt secrets.yml
```

**Using vault in playbooks:**
```yaml
---
- name: Playbook with encrypted vars
  hosts: all
  vars_files:
    - secrets.yml
  tasks:
    - name: Use encrypted variable
      debug:
        msg: "Password is {{ db_password }}"
```

**Running playbooks with vault:**
```bash
# Prompt for password
ansible-playbook playbook.yml --ask-vault-pass

# Use password file
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass

# Use multiple vault IDs
ansible-vault create --vault-id dev@prompt secrets_dev.yml
ansible-vault create --vault-id prod@prompt secrets_prod.yml
ansible-playbook playbook.yml --vault-id dev@prompt --vault-id prod@prompt
```

**Encrypting specific variables (inline):**
```bash
# Encrypt a string
ansible-vault encrypt_string 'mypassword' --name 'db_password'
```

**Output:**
```yaml
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653765356339313566396163323166613933633933326463393931363863386565653838
          ...
```

**Best practices:**
- Never commit vault passwords to version control
- Use different vault passwords for different environments
- Store vault password files securely
- Regularly rotate encrypted secrets

---

## Inventory Management

### Static Inventory

**Static inventory** is defined in a fixed file (INI or YAML format).

**INI format:**
```ini
# Simple host list
web1.example.com
web2.example.com

# Hosts with variables
web1.example.com http_port=8080
web2.example.com http_port=8081

# Groups
[webservers]
web1.example.com
web2.example.com

[databases]
db1.example.com
db2.example.com

# Group variables
[webservers:vars]
http_port=80
app_env=production

# Groups of groups
[production:children]
webservers
databases

# Host with custom connection
jumpbox.example.com ansible_connection=local
```

**YAML format:**
```yaml
all:
  hosts:
    web1.example.com:
      http_port: 8080
    web2.example.com:
      http_port: 8081
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
      vars:
        app_env: production
    databases:
      hosts:
        db1.example.com:
        db2.example.com:
    production:
      children:
        webservers:
        databases:
```

### Dynamic Inventory

**Dynamic inventory** generates inventory from external sources at runtime.

**Use cases:**
- Cloud environments (AWS, Azure, GCP)
- Container orchestration (Docker, Kubernetes)
- CMDBs and asset management systems
- Virtual infrastructure (VMware, OpenStack)

**Built-in inventory plugins:**
```bash
# AWS EC2
ansible-inventory -i aws_ec2.yml --graph

# Azure
ansible-inventory -i azure_rm.yml --graph

# GCP
ansible-inventory -i gcp_compute.yml --graph
```

**Example AWS EC2 inventory (aws_ec2.yml):**
```yaml
plugin: aws_ec2
regions:
  - us-east-1
  - us-west-2
filters:
  tag:Environment: production
keyed_groups:
  - key: tags.Application
    prefix: app
  - key: tags.Environment
    prefix: env
hostnames:
  - tag:Name
```

**Custom dynamic inventory script:**
```python
#!/usr/bin/env python3
import json

inventory = {
    "webservers": {
        "hosts": ["web1.example.com", "web2.example.com"],
        "vars": {"http_port": 80}
    },
    "_meta": {
        "hostvars": {
            "web1.example.com": {"ansible_host": "192.168.1.10"},
            "web2.example.com": {"ansible_host": "192.168.1.11"}
        }
    }
}

print(json.dumps(inventory))
```

### Inventory Variables

**Host variables** apply to specific hosts.
**Group variables** apply to all hosts in a group.

**Variable locations:**
```
inventory/
  hosts                    # Main inventory file
  group_vars/
    all.yml               # Variables for all hosts
    webservers.yml        # Variables for webservers group
    production.yml        # Variables for production group
  host_vars/
    web1.example.com.yml  # Variables specific to web1
    web2.example.com.yml  # Variables specific to web2
```

**Example group_vars/webservers.yml:**
```yaml
---
http_port: 80
app_name: myapp
log_level: info
```

**Example host_vars/web1.example.com.yml:**
```yaml
---
ansible_host: 192.168.1.10
http_port: 8080  # Override group variable
```

### Inventory Patterns

**Patterns** select specific hosts or groups for playbook execution.

**Examples:**
```bash
# All hosts
ansible all -m ping

# Specific host
ansible web1.example.com -m ping

# Specific group
ansible webservers -m ping

# Multiple groups (OR)
ansible webservers:databases -m ping

# Intersection of groups (AND)
ansible webservers:&production -m ping

# Exclusion (NOT)
ansible webservers:!production -m ping

# Wildcards
ansible web*.example.com -m ping

# Ranges
ansible web[1:5].example.com -m ping

# Complex patterns
ansible 'webservers:&production:!web1.example.com' -m ping
```

---

## Ansible Modules

### Core Module Categories

#### System Modules

**Package Management:**
- `apt` - Debian/Ubuntu package management
- `yum` - RedHat/CentOS package management
- `dnf` - Fedora package management
- `package` - Generic package manager (auto-detects)
- `pip` - Python package management
- `npm` - Node.js package management

**Service Management:**
- `service` - Manage services (generic)
- `systemd` - Manage systemd services

**User Management:**
- `user` - Manage user accounts
- `group` - Manage groups
- `authorized_key` - Manage SSH keys

#### Files Modules

**File Operations:**
- `copy` - Copy files from control to managed nodes
- `fetch` - Fetch files from managed nodes to control
- `file` - Manage file/directory properties
- `template` - Process Jinja2 templates
- `lineinfile` - Ensure a line is present/absent in a file
- `blockinfile` - Insert/update/remove text blocks
- `replace` - Replace text in files using regex

**Archive Operations:**
- `archive` - Create archives
- `unarchive` - Extract archives

#### Commands Modules

**Running Commands:**
- `command` - Execute commands (no shell processing)
- `shell` - Execute commands through shell
- `raw` - Execute raw commands (no Python required)
- `script` - Execute script on remote nodes

**When to use:**
- `command` - Simple commands without shell features
- `shell` - When you need pipes, redirects, or environment variables
- `raw` - For systems without Python installed

#### Network Modules

**Network Configuration:**
- `uri` - HTTP/HTTPS requests
- `get_url` - Download files from HTTP/HTTPS/FTP
- `slurp` - Read file from remote host (base64)

#### Cloud Modules

**AWS:**
- `ec2` - Manage EC2 instances
- `ec2_vpc_net` - Manage VPCs
- `s3_bucket` - Manage S3 buckets
- `rds` - Manage RDS instances

**Azure:**
- `azure_rm_virtualmachine` - Manage VMs
- `azure_rm_storageaccount` - Manage storage accounts

**GCP:**
- `gcp_compute_instance` - Manage compute instances
- `gcp_storage_bucket` - Manage storage buckets

### Module Examples

#### Package Module
```yaml
- name: Install nginx
  apt:
    name: nginx
    state: present        # present, absent, latest
    update_cache: yes
    cache_valid_time: 3600

- name: Install multiple packages
  apt:
    name:
      - nginx
      - git
      - vim
    state: present
```

#### Service Module
```yaml
- name: Ensure nginx is running
  service:
    name: nginx
    state: started        # started, stopped, restarted, reloaded
    enabled: yes          # Start on boot
```

#### User Module
```yaml
- name: Create user
  user:
    name: johndoe
    state: present
    groups: sudo,docker
    shell: /bin/bash
    create_home: yes
    password: "{{ 'mypassword' | password_hash('sha512') }}"
```

#### File Module
```yaml
- name: Create directory
  file:
    path: /opt/myapp
    state: directory
    owner: www-data
    group: www-data
    mode: '0755'

- name: Create symbolic link
  file:
    src: /opt/myapp/current
    dest: /opt/myapp/live
    state: link
```

#### Copy Module
```yaml
- name: Copy file
  copy:
    src: files/myconfig.conf
    dest: /etc/myapp/config.conf
    owner: root
    group: root
    mode: '0644'
    backup: yes
```

#### Template Module
```yaml
- name: Generate config from template
  template:
    src: templates/app.conf.j2
    dest: /etc/myapp/app.conf
    owner: root
    group: root
    mode: '0644'
    validate: 'myapp --test-config %s'
```

#### Command Module
```yaml
- name: Run command
  command: /usr/bin/myapp --version
  register: app_version
  changed_when: false  # This command doesn't change state

- name: Display version
  debug:
    var: app_version.stdout
```

#### Shell Module
```yaml
- name: Run shell command with pipe
  shell: cat /etc/os-release | grep VERSION_ID
  register: os_version
  changed_when: false
```

#### Git Module
```yaml
- name: Clone git repository
  git:
    repo: https://github.com/user/repo.git
    dest: /opt/myapp
    version: main
    force: yes
```

---

## Best Practices

### Idempotency

**Idempotency** means running a playbook multiple times produces the same result.

**Why it matters:**
- Safe to run playbooks repeatedly
- Predictable and reliable automation
- Easy to recover from partial failures

**Ensuring idempotency:**
```yaml
# Good - Idempotent
- name: Ensure nginx is installed
  apt:
    name: nginx
    state: present

# Bad - Not idempotent (runs every time)
- name: Download file
  shell: wget http://example.com/file.tar.gz

# Better - Idempotent
- name: Download file
  get_url:
    url: http://example.com/file.tar.gz
    dest: /tmp/file.tar.gz
    checksum: sha256:abc123...
```

**Making commands idempotent:**
```yaml
- name: Check if file exists
  stat:
    path: /opt/myapp/installed
  register: install_check

- name: Run installation
  command: /opt/myapp/install.sh
  when: not install_check.stat.exists

- name: Mark as installed
  file:
    path: /opt/myapp/installed
    state: touch
  when: not install_check.stat.exists
```

### Organization

**Directory structure best practices:**
```
ansible-project/
├── ansible.cfg              # Ansible configuration
├── inventories/
│   ├── production/
│   │   ├── hosts
│   │   └── group_vars/
│   └── staging/
│       ├── hosts
│       └── group_vars/
├── roles/
│   ├── common/
│   ├── webserver/
│   └── database/
├── playbooks/
│   ├── site.yml             # Master playbook
│   ├── webservers.yml
│   └── databases.yml
├── files/                   # Static files
├── templates/               # Jinja2 templates
└── group_vars/
    └── all.yml              # Global variables
```

**Naming conventions:**
- Use descriptive names for playbooks, roles, and tasks
- Use lowercase with underscores for file names
- Name tasks clearly to explain what they do

**Playbook organization:**
```yaml
---
# Good structure
- name: Configure web servers
  hosts: webservers
  become: true
  
  vars:
    http_port: 80
  
  pre_tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
      when: ansible_os_family == "Debian"
  
  roles:
    - common
    - webserver
  
  tasks:
    - name: Custom configuration
      template:
        src: custom.conf.j2
        dest: /etc/custom.conf
  
  post_tasks:
    - name: Send notification
      debug:
        msg: "Configuration complete"
```

### Security

**Security best practices:**

1. **Use Ansible Vault for secrets:**
```yaml
# Never do this
vars:
  db_password: "plaintext_password"

# Do this
vars_files:
  - vault_secrets.yml  # Encrypted with ansible-vault
```

2. **Limit privilege escalation:**
```yaml
# Only escalate when needed
- name: Non-privileged task
  debug:
    msg: "No sudo needed"
  
- name: Privileged task
  apt:
    name: nginx
    state: present
  become: true  # Only this task needs sudo
```

3. **Use SSH keys, not passwords:**
```bash
# In ansible.cfg or playbook
[defaults]
host_key_checking = True
```

4. **Validate external inputs:**
```yaml
- name: Validate variable
  assert:
    that:
      - app_env in ['dev', 'staging', 'production']
      - http_port | int > 1024
      - http_port | int < 65536
```

5. **Use no_log for sensitive data:**
```yaml
- name: Set database password
  mysql_user:
    name: myapp
    password: "{{ db_password }}"
    state: present
  no_log: true  # Don't log password
```

### Testing

**Testing strategies:**

1. **Syntax checking:**
```bash
ansible-playbook --syntax-check playbook.yml
```

2. **Dry run (check mode):**
```bash
ansible-playbook --check playbook.yml
```

3. **Diff mode:**
```bash
ansible-playbook --check --diff playbook.yml
```

4. **Limit to specific hosts:**
```bash
ansible-playbook playbook.yml --limit web1.example.com
```

5. **Use Molecule for role testing:**
```bash
# Install Molecule
pip install molecule molecule-docker

# Initialize Molecule in a role
cd roles/myrole
molecule init scenario

# Run tests
molecule test
```

6. **Validate with assert:**
```yaml
- name: Verify service is running
  service:
    name: nginx
  register: nginx_status

- name: Assert nginx is running
  assert:
    that:
      - nginx_status.status.ActiveState == "active"
    fail_msg: "Nginx is not running"
    success_msg: "Nginx is running"
```

### Performance

**Performance optimization:**

1. **Disable fact gathering when not needed:**
```yaml
---
- name: Quick playbook
  hosts: all
  gather_facts: no
  tasks:
    - name: Simple task
      ...
```

2. **Use pipelining:**
```ini
# ansible.cfg
[ssh_connection]
pipelining = True
```

3. **Increase parallelism:**
```ini
# ansible.cfg
[defaults]
forks = 20
```

4. **Use async for long-running tasks:**
```yaml
- name: Long running task
  command: /usr/bin/long_task
  async: 300       # Maximum runtime
  poll: 0          # Fire and forget

- name: Check on task later
  async_status:
    jid: "{{ long_task.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 30
```

---

## Ansible Galaxy

**Ansible Galaxy** is a repository for finding, sharing, and reusing Ansible roles.

### Using Galaxy Roles

**Search for roles:**
```bash
# Search on command line
ansible-galaxy search nginx

# Browse web interface
# https://galaxy.ansible.com/
```

**Install roles:**
```bash
# Install from Galaxy
ansible-galaxy install geerlingguy.nginx

# Install specific version
ansible-galaxy install geerlingguy.nginx,2.8.0

# Install from requirements file
ansible-galaxy install -r requirements.yml
```

**Requirements file (requirements.yml):**
```yaml
---
# From Galaxy
- name: geerlingguy.nginx
  version: 2.8.0

# From GitHub
- src: https://github.com/user/ansible-role-myapp
  name: myapp
  version: main

# From local path
- src: /path/to/local/role
  name: local_role
```

**Using installed roles:**
```yaml
---
- name: Configure web servers
  hosts: webservers
  roles:
    - geerlingguy.nginx
```

**Role installation location:**
- Default: `~/.ansible/roles/`
- Configure in `ansible.cfg`:
```ini
[defaults]
roles_path = ./roles:~/.ansible/roles:/usr/share/ansible/roles
```

### Creating Galaxy Roles

**Initialize new role:**
```bash
# Create role skeleton
ansible-galaxy init myrole

# Creates structure:
# myrole/
#   README.md
#   defaults/
#   files/
#   handlers/
#   meta/
#   tasks/
#   templates/
#   tests/
#   vars/
```

**Role metadata (meta/main.yml):**
```yaml
---
galaxy_info:
  author: Your Name
  description: Description of the role
  license: MIT
  min_ansible_version: 2.9
  
  platforms:
    - name: Ubuntu
      versions:
        - focal
        - jammy
    - name: EL
      versions:
        - 8
        - 9
  
  galaxy_tags:
    - web
    - nginx
    - server

dependencies: []
```

**Publishing to Galaxy:**
```bash
# Log in to Galaxy
ansible-galaxy login

# Import role from GitHub
# (Must have galaxy_info in meta/main.yml)
ansible-galaxy import <github_user> <github_repo>
```

### Galaxy Collections

**Collections** bundle roles, modules, and plugins together.

**Install collections:**
```bash
# Install from Galaxy
ansible-galaxy collection install community.general

# Install from requirements
ansible-galaxy collection install -r requirements.yml
```

**Collections requirements file:**
```yaml
---
collections:
  - name: community.general
    version: 5.0.0
  - name: ansible.posix
    version: 1.4.0
```

**Using collection modules:**
```yaml
---
- name: Use collection module
  hosts: all
  tasks:
    - name: Manage Docker container
      community.docker.docker_container:
        name: myapp
        image: nginx:latest
        state: started
```

---

## Additional Resources

### Official Documentation
- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Ansible GitHub](https://github.com/ansible/ansible)

### Books
- "Ansible: Up and Running" by Lorin Hochstein
- "Ansible for DevOps" by Jeff Geerling
- "Mastering Ansible" by James Freeman

### Community
- [Ansible Mailing List](https://groups.google.com/forum/#!forum/ansible-project)
- [Ansible Reddit](https://www.reddit.com/r/ansible/)
- [Ansible IRC](https://docs.ansible.com/ansible/latest/community/communication.html)

### Online Learning
- [Red Hat Ansible Training](https://www.redhat.com/en/services/training/ansible-training)
- [Ansible 101 by Jeff Geerling](https://www.youtube.com/playlist?list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN)
- [Ansible Tutorial for Beginners](https://www.youtube.com/playlist?list=PLT98CRl2KxKEUHie1m24-wkyHpEsa4Y70)

---

*Last updated: 2026*
