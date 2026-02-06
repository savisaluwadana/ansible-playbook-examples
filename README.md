# Ansible Playbook Examples

A comprehensive collection of Ansible playbooks, examples, and theory documentation to help you learn and master Ansible automation. From basic system administration to advanced deployment strategies.

## 📚 Table of Contents

1. [Quick Start](#-quick-start)
2. [Ansible Theory](#-ansible-theory)
3. [Examples by Difficulty](#-examples-by-difficulty)
   - [Basic Examples](#basic-examples)
   - [Intermediate Examples](#intermediate-examples)
   - [Advanced Examples](#advanced-examples)
4. [Mezzanine CMS Deployment](#-mezzanine-cms-deployment-example)
5. [Project Structure](#-project-structure)
6. [Contributing](#-contributing)
7. [Additional Resources](#-additional-resources)

---

## 🚀 Quick Start

### Prerequisites

**On Your Control Machine:**
- Ansible 2.9 or later
- Python 3.8+
- SSH access to target hosts

**On Target Hosts:**
- Ubuntu 20.04+ or equivalent Linux distribution
- Python 3
- SSH server running

### Installation

Install Ansible:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ansible

# macOS
brew install ansible

# pip
pip install ansible
```

### Your First Playbook

1. Clone this repository:
```bash
git clone https://github.com/savisaluwadana/ansible-playbook-examples.git
cd ansible-playbook-examples
```

2. Update inventory with your hosts:
```bash
cp inventories/example_hosts inventories/my_hosts
# Edit inventories/my_hosts with your server details
```

3. Run a basic example:
```bash
ansible-playbook -i inventories/my_hosts examples/basic/system-update-playbook.yml
```

---

## 📖 Ansible Theory

Before diving into examples, we recommend reading our comprehensive Ansible theory documentation:

**[📘 ANSIBLE_THEORY.md](ANSIBLE_THEORY.md)** - Complete guide covering:
- Ansible Architecture (Control nodes, managed nodes, inventory, modules, plugins)
- Core Concepts (Playbooks, tasks, handlers, roles, variables, facts)
- Conditionals and Loops
- Templates (Jinja2)
- Vault for Secrets Management
- Inventory Management (Static and Dynamic)
- Ansible Modules
- Best Practices (Idempotency, organization, security, testing)
- Ansible Galaxy

---

## 📁 Examples by Difficulty

### Basic Examples

Perfect for beginners learning Ansible fundamentals.

#### 🔧 [System Update and Package Management](examples/basic/system-update-playbook.yml)
- Updates all packages on Debian/Ubuntu and RedHat/CentOS
- Demonstrates OS family detection and conditional execution
- **Concepts**: `when` conditionals, `apt`/`yum` modules, fact gathering

#### 👥 [User and Group Management](examples/basic/user-management-playbook.yml)
- Creates users, groups, and configures SSH keys
- Manages sudo access
- **Concepts**: `user`, `group`, `authorized_key` modules, loops

#### 📂 [File and Directory Operations](examples/basic/file-operations-playbook.yml)
- Creates directories, copies files, manages permissions
- Sets up log rotation
- **Concepts**: `file`, `copy`, `template`, `lineinfile` modules

#### 🔄 [Service Management](examples/basic/service-management-playbook.yml)
- Installs and manages system services (nginx, ssh)
- Configures systemd services
- **Concepts**: `service` module, handlers, service verification

### Intermediate Examples

For users comfortable with Ansible basics, ready for real-world scenarios.

#### 🌐 [Web Server Setup (Nginx)](examples/intermediate/web-server/)
- Complete Nginx installation and configuration
- SSL/TLS certificate generation
- Virtual host configuration
- Firewall setup
- **Concepts**: Templates, SSL configuration, handlers, UFW firewall

#### 🗄️ [Database Setup (PostgreSQL)](examples/intermediate/database/)
- PostgreSQL installation and configuration
- Database and user creation
- Performance tuning
- Automated backup setup
- **Concepts**: PostgreSQL modules, cron jobs, security hardening

#### 🚀 [Application Deployment (Flask)](examples/intermediate/app-deployment/)
- Python Flask application deployment
- Virtual environment setup
- Gunicorn WSGI server configuration
- Nginx reverse proxy
- Systemd service creation
- **Concepts**: Python deployment, systemd, reverse proxy, application lifecycle

### Advanced Examples

Advanced patterns and best practices for production environments.

#### 🏗️ [Role-Based Playbooks](examples/advanced/role-based/)
- Complete role structure with common, webserver, and database roles
- Demonstrates proper role organization
- Reusable components
- **Directory Structure**:
  ```
  roles/
    ├── common/       # Base configuration for all servers
    ├── webserver/    # Web server role
    └── database/     # Database role
  ```
- **Concepts**: Role organization, dependencies, variable precedence

#### 🔐 [Vault-Encrypted Variables](examples/advanced/vault-encrypted/)
- Secure handling of sensitive data (passwords, API keys)
- Ansible Vault encryption and decryption
- Best practices for secrets management
- **Concepts**: `ansible-vault`, `no_log`, secure variable handling
- **Usage**:
  ```bash
  ansible-vault create secrets.yml
  ansible-playbook vault-playbook.yml --ask-vault-pass
  ```

#### 🔍 [Dynamic Inventory](examples/advanced/dynamic-inventory/)
- Auto-discovery of infrastructure
- AWS EC2, Azure, GCP inventory plugins
- Custom dynamic inventory scripts
- **Concepts**: Inventory plugins, cloud integration, auto-scaling
- **Includes**:
  - `aws_ec2.yml` - AWS EC2 dynamic inventory
  - `custom_inventory.py` - Custom inventory script example

---

## 🎯 Mezzanine CMS Deployment Example

A complete production-ready example deploying [Mezzanine CMS](http://mezzanine.jupo.org/) to an Ubuntu server.

## 📋 Prerequisites

### On Your Control Machine (where you run Ansible)

- **Ansible** 2.9 or later
- **Vagrant** 2.x (for local testing)
- **VirtualBox** 6.x or later
- **Git** (with SSH key configured for GitHub)
- **SSH Agent** running with your key loaded

### On Target Server

- Ubuntu 20.04 LTS (Focal Fossa)
- SSH access with sudo privileges

## 🗂️ Project Structure

```
ansible-mezzanine/
├── mezzanine.yml           # Main Ansible playbook
├── hosts                   # Inventory file
├── ansible.cfg             # Ansible configuration
├── Vagrantfile             # Vagrant configuration
├── requirements.txt        # Python packages for Mezzanine
├── secrets.yml.example     # Template for secrets (copy to secrets.yml)
├── .gitignore              # Git ignore patterns
├── README.md               # This documentation
├── templates/
│   ├── local_settings.py.j2    # Django settings template
│   ├── gunicorn.conf.py.j2     # Gunicorn config template
│   ├── supervisor.conf.j2      # Supervisor config template
│   └── nginx.conf.j2           # NGINX config template
└── scripts/
    ├── setsite.py              # Set Django site domain
    └── setadmin.py             # Set admin credentials
```

## 🚀 Quick Start with Vagrant

### 1. Clone and Configure

```bash
cd ansible-mezzanine

# Copy secrets template and customize
cp secrets.yml.example secrets.yml

# Edit secrets.yml with your own values
# IMPORTANT: Generate new random values for production!
```

### 2. Set Up SSH Agent (for GitHub)

```bash
# Start SSH agent
eval $(ssh-agent)

# Add your SSH key
ssh-add ~/.ssh/id_rsa

# Verify key is loaded
ssh-add -L
```

### 3. Deploy

```bash
# Create VM and run playbook
vagrant up
```

### 4. Access Mezzanine

Open your browser to:
- **HTTP**: http://192.168.33.10.nip.io
- **HTTPS**: https://192.168.33.10.nip.io (accept self-signed cert)
- **Admin**: https://192.168.33.10.nip.io/admin
  - Username: `admin`
  - Password: (value from `admin_pass` in secrets.yml)

## 📝 Configuration

### Variables (mezzanine.yml)

| Variable | Description | Default |
|----------|-------------|---------|
| `proj_app` | Django project name | `mezzanine_example` |
| `live_hostname` | Primary domain | `192.168.33.10.nip.io` |
| `domains` | List of allowed domains | `[192.168.33.10.nip.io, www.192.168.33.10.nip.io]` |
| `repo_url` | Git repository URL | `git@github.com:ansiblebook/mezzanine_example.git` |
| `tls_enabled` | Enable HTTPS | `true` |
| `locale` | System locale | `en_US.UTF-8` |

### Secrets (secrets.yml)

| Variable | Description |
|----------|-------------|
| `db_pass` | PostgreSQL database password |
| `admin_pass` | Mezzanine admin password |
| `secret_key` | Django SECRET_KEY |
| `nevercache_key` | Mezzanine NEVERCACHE_KEY |
| `twitter_*` | Twitter API credentials (optional) |

## 🔧 Playbook Tasks Overview

The playbook performs these tasks in order:

1. **Install apt packages** - Git, NGINX, PostgreSQL, Python, Supervisor, etc.
2. **Create directories** - Project path and logs directory
3. **Clone repository** - Checkout Mezzanine project from GitHub
4. **Setup virtualenv** - Create Python virtual environment
5. **Install Python packages** - pip install from requirements.txt
6. **Configure PostgreSQL** - Create database user and database
7. **Generate TLS certificates** - Self-signed certificates (if enabled)
8. **Configure NGINX** - Reverse proxy configuration
9. **Configure Supervisor** - Process manager for Gunicorn
10. **Configure Gunicorn** - WSGI application server
11. **Generate Django settings** - local_settings.py from template
12. **Run migrations** - Django database migrations
13. **Collect static files** - Django collectstatic
14. **Set site domain** - Configure Django Sites framework
15. **Set admin password** - Create/update admin user
16. **Install cron job** - Twitter polling (every 5 minutes)

## 📋 Useful Commands

### List Playbook Tasks

```bash
ansible-playbook --list-tasks mezzanine.yml
```

### Check Playbook Syntax

```bash
ansible-playbook --syntax-check mezzanine.yml
```

### Run Playbook Manually

```bash
ansible-playbook mezzanine.yml
```

### Run with Verbose Output

```bash
ansible-playbook -vvv mezzanine.yml
```

### Check Mode (Dry Run)

```bash
ansible-playbook --check mezzanine.yml
```

### Vagrant Commands

```bash
# Start/provision VM
vagrant up

# SSH into VM
vagrant ssh

# Re-run playbook
vagrant provision

# Destroy VM
vagrant destroy -f

# Recreate from scratch
vagrant destroy -f && vagrant up
```

## 🐛 Troubleshooting

### Cannot Clone Git Repository

**Error**: `fatal: Could not read from remote repository`

**Solutions**:
1. Remove old host key:
   ```bash
   ssh-keygen -R 192.168.33.10
   ```
2. Ensure SSH agent is running with your key
3. Verify GitHub SSH access:
   ```bash
   ssh -T git@github.com
   ```

### Cannot Reach nip.io Domain

**Problem**: DNS lookup fails for `192.168.33.10.nip.io`

**Solutions**:
1. Test DNS resolution:
   ```bash
   dig +short 192.168.33.10.nip.io
   ```
2. Add to `/etc/hosts` if DNS fails:
   ```
   192.168.33.10 192.168.33.10.nip.io www.192.168.33.10.nip.io
   ```

### Bad Request (400)

**Cause**: Accessing with hostname not in ALLOWED_HOSTS

**Solution**: Use one of the configured domains:
- `192.168.33.10.nip.io`
- `www.192.168.33.10.nip.io`

### PostgreSQL Connection Errors

**Solution**: SSH into VM and check PostgreSQL:
```bash
vagrant ssh
sudo systemctl status postgresql
sudo -u postgres psql -c "\l"
```

### Supervisor/Gunicorn Issues

**Solution**: Check supervisor status:
```bash
vagrant ssh
sudo supervisorctl status
sudo supervisorctl tail gunicorn_mezzanine
```

## 🔒 Security Considerations

1. **Never commit secrets.yml** - It's in .gitignore for safety
2. **Generate unique keys** - Don't use the example values in production
3. **Use ansible-vault** for production secrets encryption
4. **Replace self-signed certs** with real certificates (Let's Encrypt)
5. **Restrict SSH access** and use key-based authentication only

## 📚 Directory Structure on Target Server

After deployment, files are organized as:

```
/home/vagrant/
├── logs/                           # Application logs
├── mezzanine/
│   └── mezzanine_example/          # Django project
│       ├── manage.py
│       ├── gunicorn.conf.py
│       ├── gunicorn.sock           # Unix socket
│       ├── static/                 # Collected static files
│       └── mezzanine_example/
│           ├── settings.py
│           └── local_settings.py   # Generated config
└── .virtualenvs/
    └── mezzanine_example/          # Python virtualenv
```

## 📖 Further Reading

- [Ansible Documentation](https://docs.ansible.com/)
- [Mezzanine Documentation](https://mezzanine.readthedocs.io/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Ansible: Up and Running, 3rd Edition](https://www.ansiblebook.com/)

---

## 📂 Project Structure

```
ansible-playbook-examples/
├── README.md                          # This file
├── ANSIBLE_THEORY.md                  # Comprehensive Ansible theory documentation
├── example1.yml                       # Original simple nginx example
│
├── examples/                          # Organized playbook examples
│   ├── basic/                         # Basic examples for beginners
│   │   ├── system-update-playbook.yml
│   │   ├── user-management-playbook.yml
│   │   ├── file-operations-playbook.yml
│   │   └── service-management-playbook.yml
│   │
│   ├── intermediate/                  # Intermediate real-world examples
│   │   ├── web-server/
│   │   │   ├── nginx-setup.yml
│   │   │   ├── nginx.conf.j2
│   │   │   └── vhost.conf.j2
│   │   ├── database/
│   │   │   └── postgresql-setup.yml
│   │   └── app-deployment/
│   │       ├── flask-app-deployment.yml
│   │       └── flask-app.service.j2
│   │
│   └── advanced/                      # Advanced patterns and practices
│       ├── role-based/
│       │   ├── site.yml
│       │   └── roles/
│       │       ├── common/
│       │       ├── webserver/
│       │       └── database/
│       ├── vault-encrypted/
│       │   ├── README.md
│       │   ├── vault-playbook.yml
│       │   ├── app_secrets.j2
│       │   └── secrets.example.yml
│       └── dynamic-inventory/
│           ├── README.md
│           ├── aws_ec2.yml
│           └── custom_inventory.py
│
└── inventories/                       # Inventory file examples
    └── example_hosts                  # Example static inventory
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Adding New Examples

1. **Fork the repository**
2. **Create a new branch**: `git checkout -b feature/new-example`
3. **Follow the example structure**:
   - Add clear description at the top of the playbook
   - Include prerequisites
   - Document key concepts used
   - Provide usage instructions
   - Add expected output/results
   - Include use cases at the bottom
4. **Test your playbook** on a clean system
5. **Submit a pull request**

### Example Template

When creating new examples, use this template:

```yaml
---
# Example Name
#
# Description:
#   Brief description of what this playbook does
#
# Prerequisites:
#   - List prerequisites here
#
# Usage:
#   ansible-playbook -i inventory playbook.yml
#
# Expected Output:
#   - What should happen when run successfully
#
# Key Concepts:
#   - Concept 1
#   - Concept 2

- name: Playbook name
  hosts: target_hosts
  become: true
  
  tasks:
    - name: Task description
      module_name:
        parameter: value

# Use Cases:
#   - Use case 1
#   - Use case 2
```

### Reporting Issues

- Use GitHub Issues to report bugs or suggest improvements
- Include Ansible version, OS, and error messages
- Provide steps to reproduce the issue

### Documentation Improvements

- Fix typos or unclear explanations
- Add more examples to theory documentation
- Improve README organization
- Translate documentation (future)

---

## 📚 Additional Resources

### Official Documentation
- [Ansible Documentation](https://docs.ansible.com/) - Official comprehensive docs
- [Ansible Galaxy](https://galaxy.ansible.com/) - Repository of community roles
- [Ansible GitHub](https://github.com/ansible/ansible) - Source code and issues

### Books
- **"Ansible: Up and Running"** by Lorin Hochstein and René Moser
- **"Ansible for DevOps"** by Jeff Geerling
- **"Mastering Ansible"** by James Freeman and Jesse Keating

### Online Learning
- [Ansible 101 by Jeff Geerling](https://www.youtube.com/playlist?list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN) - YouTube series
- [Red Hat Ansible Training](https://www.redhat.com/en/services/training/ansible-training) - Official training
- [Ansible Tutorial for Beginners](https://www.youtube.com/playlist?list=PLT98CRl2KxKEUHie1m24-wkyHpEsa4Y70) - Video tutorials

### Community
- [Ansible Mailing List](https://groups.google.com/forum/#!forum/ansible-project)
- [Ansible Reddit](https://www.reddit.com/r/ansible/)
- [Ansible IRC](https://docs.ansible.com/ansible/latest/community/communication.html)
- [Ansible Forum](https://forum.ansible.com/)

### Related Projects
- [Ansible Lint](https://github.com/ansible/ansible-lint) - Best practice checker
- [Molecule](https://molecule.readthedocs.io/) - Testing framework for Ansible roles
- [AWX](https://github.com/ansible/awx) - Web-based UI for Ansible (upstream of Ansible Tower)

---

## 📄 License

This project is provided as educational material. Individual examples and documentation are available for free use in learning and personal projects.

Based on concepts from "Ansible: Up and Running" and community best practices.

---

## ⭐ Star This Repository

If you find this repository helpful, please consider giving it a star! It helps others discover these resources.

**Questions? Issues? Suggestions?** 
Open an [issue](https://github.com/savisaluwadana/ansible-playbook-examples/issues) or submit a pull request!
