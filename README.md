# Deploying Mezzanine with Ansible

A complete Ansible playbook for deploying [Mezzanine CMS](http://mezzanine.jupo.org/) to an Ubuntu server, based on Chapter 7 of "Ansible: Up and Running, 3rd Edition".

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

## 📄 License

This project is provided as educational material based on "Ansible: Up and Running".
