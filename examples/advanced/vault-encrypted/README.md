# Ansible Vault Example
#
# Description:
#   Demonstrates how to use Ansible Vault to encrypt sensitive data
#   such as passwords, API keys, and other secrets
#
# Setup:
#   1. Create encrypted variables file:
#      ansible-vault create secrets.yml
#   
#   2. Add sensitive data to secrets.yml:
#      db_password: "SuperSecretPassword123!"
#      api_key: "abc123xyz789"
#      ssh_private_key: |
#        -----BEGIN RSA PRIVATE KEY-----
#        ...
#        -----END RSA PRIVATE KEY-----
#
#   3. Run playbook with vault password:
#      ansible-playbook -i inventory vault-playbook.yml --ask-vault-pass
#
# Key Concepts:
#   - Encrypting sensitive data
#   - Using encrypted variables in playbooks
#   - Vault password management
#   - Best practices for secrets management

## Creating Encrypted Files

# Create new encrypted file
```bash
ansible-vault create secrets.yml
```

# Encrypt existing file
```bash
ansible-vault encrypt vars.yml
```

# Edit encrypted file
```bash
ansible-vault edit secrets.yml
```

# View encrypted file
```bash
ansible-vault view secrets.yml
```

# Decrypt file
```bash
ansible-vault decrypt secrets.yml
```

# Rekey (change password)
```bash
ansible-vault rekey secrets.yml
```

## Example Playbook Using Vault

See vault-playbook.yml for complete example.

## Example secrets.yml (before encryption)

```yaml
---
# Database credentials
db_password: "SuperSecretPassword123!"
db_root_password: "RootPassword456!"

# API keys
aws_access_key: "AKIAIOSFODNN7EXAMPLE"
aws_secret_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Application secrets
app_secret_key: "django-insecure-random-string-here"
jwt_secret: "jwt-secret-key-here"

# SMTP credentials
smtp_username: "user@example.com"
smtp_password: "EmailPassword123!"
```

## Using Vault Password File

Create a password file:
```bash
echo "MyVaultPassword" > ~/.vault_pass
chmod 600 ~/.vault_pass
```

Use in ansible.cfg:
```ini
[defaults]
vault_password_file = ~/.vault_pass
```

Or use in command line:
```bash
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass
```

## Using Multiple Vault IDs

```bash
# Create files with different vault IDs
ansible-vault create --vault-id dev@prompt secrets_dev.yml
ansible-vault create --vault-id prod@prompt secrets_prod.yml

# Run playbook with multiple vault IDs
ansible-playbook playbook.yml --vault-id dev@prompt --vault-id prod@prompt
```

## Encrypting Specific Variables (Inline)

```bash
# Encrypt a single string
ansible-vault encrypt_string 'mypassword' --name 'db_password'
```

Output to include in playbook:
```yaml
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66386439653765356339313566396163323166613933633933326463393931363863386565653838
          ...
```

## Best Practices

1. **Never commit unencrypted secrets to version control**
2. **Use different vault passwords for different environments**
3. **Store vault password files securely, outside the repository**
4. **Use ansible-vault rekey to rotate vault passwords regularly**
5. **Use --vault-id to manage multiple environments**
6. **Consider using external secret management tools (HashiCorp Vault, AWS Secrets Manager) for production**
