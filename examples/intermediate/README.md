# Intermediate Examples

This directory contains real-world Ansible playbooks for common infrastructure scenarios.

## Examples

### 1. Web Server Setup (Nginx)
**Directory**: `web-server/`

Complete Nginx web server deployment with SSL/TLS support.

**Includes**:
- `nginx-setup.yml` - Main playbook
- `nginx.conf.j2` - Nginx configuration template
- `vhost.conf.j2` - Virtual host template

**Features**:
- Nginx installation and configuration
- SSL/TLS certificate generation (self-signed)
- Virtual host setup
- Firewall configuration (UFW)
- Performance optimization
- Security headers

**Usage**:
```bash
cd web-server
ansible-playbook -i ../../inventories/example_hosts nginx-setup.yml \
  -e "server_name=mysite.com"
```

---

### 2. Database Setup (PostgreSQL)
**Directory**: `database/`

PostgreSQL database server installation and configuration.

**Includes**:
- `postgresql-setup.yml` - Complete PostgreSQL setup

**Features**:
- PostgreSQL installation
- Database and user creation
- Performance tuning
- Automated backup configuration
- Security hardening
- Cron job for daily backups

**Usage**:
```bash
cd database
ansible-playbook -i ../../inventories/example_hosts postgresql-setup.yml \
  -e "db_password=SecurePassword123"
```

---

### 3. Application Deployment (Flask)
**Directory**: `app-deployment/`

Python Flask web application deployment with production setup.

**Includes**:
- `flask-app-deployment.yml` - Main deployment playbook
- `flask-app.service.j2` - Systemd service template

**Features**:
- Python virtual environment setup
- Flask application deployment
- Gunicorn WSGI server configuration
- Nginx reverse proxy
- Systemd service creation
- Application health checks

**Usage**:
```bash
cd app-deployment
ansible-playbook -i ../../inventories/example_hosts flask-app-deployment.yml
```

---

## Use Cases

These intermediate examples are designed for:

- **DevOps Engineers**: Setting up development and staging environments
- **System Administrators**: Automating common infrastructure tasks
- **Developers**: Deploying applications to production
- **Students**: Learning production-ready deployment patterns

## Prerequisites

- Ansible 2.9 or later
- Target Ubuntu/Debian servers (20.04+ recommended)
- SSH access with sudo privileges
- Basic understanding of:
  - Web servers (Nginx/Apache)
  - Databases (PostgreSQL/MySQL)
  - Python applications
  - Systemd services

## Best Practices Demonstrated

1. **Template Usage**: Jinja2 templates for dynamic configuration
2. **Handlers**: Efficient service restarts only when needed
3. **Variables**: Proper variable organization and precedence
4. **Security**: 
   - Firewall configuration
   - SSL/TLS setup
   - Secure file permissions
   - Password management
5. **Idempotency**: All playbooks can be run multiple times safely
6. **Error Handling**: Proper task verification and validation

## Next Steps

After mastering these intermediate examples:
1. Explore the [Advanced Examples](../advanced/) for role-based organization
2. Learn about [Ansible Vault](../advanced/vault-encrypted/) for secrets management
3. Study [Dynamic Inventory](../advanced/dynamic-inventory/) for cloud deployments

## Common Issues

**Issue**: Firewall blocking connections
- **Solution**: Ensure UFW rules are properly configured and enabled

**Issue**: PostgreSQL authentication failure
- **Solution**: Check pg_hba.conf settings and user passwords

**Issue**: Nginx configuration test fails
- **Solution**: Verify template syntax and variable values

**Issue**: Application not starting
- **Solution**: Check systemd service logs with `journalctl -u service-name`
