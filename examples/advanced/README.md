# Advanced Examples

This directory contains advanced Ansible patterns and best practices for production environments.

## Examples

### 1. Role-Based Playbooks
**Directory**: `role-based/`

Demonstrates best practices for organizing playbooks using roles.

**Structure**:
```
role-based/
├── site.yml              # Main orchestration playbook
└── roles/
    ├── common/          # Base configuration for all servers
    │   ├── tasks/
    │   ├── handlers/
    │   └── defaults/
    ├── webserver/       # Web server role
    │   ├── tasks/
    │   ├── templates/
    │   ├── handlers/
    │   └── defaults/
    └── database/        # Database role
        ├── tasks/
        ├── handlers/
        └── defaults/
```

**Key Concepts**:
- Role organization and structure
- Separation of concerns
- Reusable components
- Variable precedence
- Role dependencies

**Usage**:
```bash
cd role-based
ansible-playbook -i ../../inventories/example_hosts site.yml
```

**Benefits**:
- Easy to maintain and scale
- Reusable across projects
- Clear separation of responsibilities
- Simplified testing

---

### 2. Vault-Encrypted Variables
**Directory**: `vault-encrypted/`

Secure handling of sensitive data using Ansible Vault.

**Includes**:
- `README.md` - Comprehensive vault usage guide
- `vault-playbook.yml` - Example playbook using encrypted variables
- `app_secrets.j2` - Template using encrypted variables
- `secrets.example.yml` - Example secrets file (unencrypted template)

**Features**:
- Creating and managing encrypted files
- Using encrypted variables in playbooks
- Multiple vault IDs for different environments
- Inline variable encryption
- Best practices for secrets management

**Usage**:
```bash
cd vault-encrypted

# Create encrypted secrets file
ansible-vault create secrets.yml

# Run playbook with vault password
ansible-playbook -i ../../inventories/example_hosts vault-playbook.yml --ask-vault-pass
```

**Important**:
- Never commit unencrypted secrets to version control
- Use different vault passwords for different environments
- Store vault password files securely
- Use `no_log: true` when handling sensitive data

---

### 3. Dynamic Inventory
**Directory**: `dynamic-inventory/`

Auto-discovery and management of infrastructure from external sources.

**Includes**:
- `README.md` - Dynamic inventory usage guide
- `aws_ec2.yml` - AWS EC2 inventory plugin configuration
- `custom_inventory.py` - Custom inventory script example

**Supported Sources**:
- AWS EC2
- Azure
- Google Cloud Platform
- Docker
- VMware
- Custom APIs/databases

**Features**:
- Automatic infrastructure discovery
- Cloud provider integration
- Custom inventory scripts
- Inventory caching for performance
- Dynamic grouping and filtering

**Usage**:
```bash
cd dynamic-inventory

# Test AWS EC2 inventory
ansible-inventory -i aws_ec2.yml --graph

# Use with playbook
ansible-playbook -i aws_ec2.yml playbook.yml

# Custom inventory script
ansible-playbook -i custom_inventory.py playbook.yml
```

**Prerequisites**:
- Cloud provider SDK installed (boto3 for AWS, etc.)
- Proper authentication configured
- Network access to cloud APIs

---

## When to Use Advanced Patterns

### Use Role-Based Organization When:
- Managing multiple similar servers
- Building reusable infrastructure components
- Working in a team environment
- Need to share code across projects
- Complexity grows beyond a few playbooks

### Use Ansible Vault When:
- Managing passwords and API keys
- Handling SSL certificates and private keys
- Storing cloud credentials
- Managing environment-specific secrets
- Compliance requires encryption at rest

### Use Dynamic Inventory When:
- Infrastructure changes frequently
- Using auto-scaling groups
- Managing cloud resources
- Servers are ephemeral
- Need real-time infrastructure state

## Production Considerations

1. **Role-Based Playbooks**:
   - Use Ansible Galaxy to share roles
   - Version roles independently
   - Document role dependencies
   - Test roles with Molecule

2. **Vault-Encrypted Variables**:
   - Integrate with CI/CD pipelines
   - Consider HashiCorp Vault for large deployments
   - Rotate secrets regularly
   - Use different vault IDs per environment

3. **Dynamic Inventory**:
   - Enable caching in production
   - Use inventory filters to reduce scope
   - Test inventory scripts thoroughly
   - Monitor API rate limits
   - Have fallback static inventory

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: Run Ansible Playbook
  uses: dawidd6/action-ansible-playbook@v2
  with:
    playbook: site.yml
    directory: ./role-based
    key: ${{ secrets.SSH_PRIVATE_KEY }}
    vault_password: ${{ secrets.VAULT_PASSWORD }}
    inventory: |
      [webservers]
      web1.example.com
```

### GitLab CI Example
```yaml
deploy:
  image: cytopia/ansible:latest
  script:
    - echo "$VAULT_PASSWORD" > .vault_pass
    - ansible-playbook -i inventory site.yml --vault-password-file .vault_pass
  after_script:
    - rm .vault_pass
```

## Security Best Practices

1. **Never commit sensitive data unencrypted**
2. **Use SSH keys, not passwords**
3. **Limit playbook permissions with `become_user`**
4. **Enable Ansible logging for audit trails**
5. **Use `no_log: true` for sensitive tasks**
6. **Validate external inputs**
7. **Keep Ansible and modules updated**
8. **Use vault for all secrets**

## Troubleshooting

**Issue**: Role not found
- **Solution**: Check `roles_path` in ansible.cfg or use full path

**Issue**: Vault decryption fails
- **Solution**: Verify vault password, check vault ID if using multiple

**Issue**: Dynamic inventory returns no hosts
- **Solution**: Verify cloud credentials and network connectivity

**Issue**: Template rendering fails
- **Solution**: Check variable definitions and template syntax

## Further Learning

- [Ansible Galaxy](https://galaxy.ansible.com/) - Browse community roles
- [Molecule](https://molecule.readthedocs.io/) - Role testing framework
- [Ansible Tower/AWX](https://github.com/ansible/awx) - Enterprise automation platform
- [Ansible Lint](https://github.com/ansible/ansible-lint) - Best practice checker
