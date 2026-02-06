# Basic Examples

This directory contains fundamental Ansible playbooks perfect for beginners learning Ansible basics.

## Examples

### 1. System Update and Package Management
**File**: `system-update-playbook.yml`

Updates all system packages and demonstrates conditional execution based on OS family.

**Key Concepts**:
- Conditional execution with `when`
- OS family detection using Ansible facts
- Package management with `apt` and `yum`
- Privilege escalation with `become`

**Usage**:
```bash
ansible-playbook -i ../../inventories/example_hosts system-update-playbook.yml
```

---

### 2. User and Group Management
**File**: `user-management-playbook.yml`

Creates and manages user accounts, groups, and SSH keys.

**Key Concepts**:
- User module for account management
- Group module for group creation
- Password hashing for security
- SSH key management with `authorized_key`
- Loops for processing multiple items

**Usage**:
```bash
ansible-playbook -i ../../inventories/example_hosts user-management-playbook.yml
```

---

### 3. File and Directory Operations
**File**: `file-operations-playbook.yml`

Demonstrates various file and directory manipulation operations.

**Key Concepts**:
- File module for file/directory operations
- Copy module for static files
- Template module for dynamic content generation
- Lineinfile for targeted file edits
- Blockinfile for multi-line insertions

**Usage**:
```bash
ansible-playbook -i ../../inventories/example_hosts file-operations-playbook.yml
```

---

### 4. Service Management
**File**: `service-management-playbook.yml`

Manages system services including installation, configuration, and monitoring.

**Key Concepts**:
- Service module for service management
- Handlers for service restarts
- Service verification and health checks
- Systemd service configuration
- Firewall configuration with UFW

**Usage**:
```bash
ansible-playbook -i ../../inventories/example_hosts service-management-playbook.yml
```

---

## Learning Path

1. **Start with**: `system-update-playbook.yml` to learn basic playbook structure
2. **Then try**: `user-management-playbook.yml` to understand loops and user management
3. **Next**: `file-operations-playbook.yml` to learn file manipulation
4. **Finally**: `service-management-playbook.yml` to understand service management and handlers

## Prerequisites

- Ansible 2.9 or later installed on control machine
- Target hosts running Ubuntu/Debian or RedHat/CentOS
- SSH access to target hosts with sudo privileges
- Python 3 installed on target hosts

## Tips

- Run playbooks with `-C` flag for check mode (dry run): `ansible-playbook -C playbook.yml`
- Use `--check --diff` to see what changes would be made
- Add `-v`, `-vv`, or `-vvv` for increased verbosity during debugging
- Use tags to run specific tasks: `ansible-playbook playbook.yml --tags install`
