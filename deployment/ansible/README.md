# Ansible Development Environment

This directory contains Ansible playbooks and roles for deploying the Derkino application infrastructure.

## Virtual Environment Setup

A Python virtual environment is configured for Ansible development to avoid system Python conflicts.

### Activating the Virtual Environment

```bash
# Navigate to this directory
cd /home/eido/code/derkino/deployment/ansible

# Activate the virtual environment
source .venv/bin/activate

# Verify Ansible is available
ansible --version
ansible-lint --version
```

### Installing Dependencies

Dependencies are already installed in the virtual environment:
- `ansible` - Core automation tool
- `ansible-lint` - Linting and validation

To install additional packages:
```bash
source .venv/bin/activate
pip install <package-name>
```

### Running Ansible Playbooks

```bash
source .venv/bin/activate

# Run playbook with local inventory
ansible-playbook -i inventory/local deploy.yml

# Run with migration enabled
ansible-playbook -i inventory/local deploy.yml -e "migration_enabled=true"
```

## Directory Structure

```
deployment/ansible/
├── deploy.yml              # Main deployment playbook
├── environments/           # Environment-specific variables
├── group_vars/            # Global variables
├── inventory/             # Inventory files
├── roles/                 # Ansible roles
│   ├── common/           # Common tasks
│   ├── helm/             # Helm chart deployment
│   ├── kubernetes/       # Kubernetes resource management
│   ├── migration/        # Zero-downtime migration
│   ├── secrets/          # Secret management with Vault
│   └── ingress/          # Ingress configuration
├── .venv/                # Python virtual environment (gitignored)
└── .gitignore            # Git ignore rules
```

## Development Workflow

1. **Activate virtual environment**: `source .venv/bin/activate`
2. **Edit playbooks/roles**: Make changes to YAML files
3. **Validate with ansible-lint**: `ansible-lint deploy.yml`
4. **Test locally**: `ansible-playbook -i inventory/local deploy.yml`
5. **Commit changes**: Git will ignore virtual environment files

## Git Ignore Rules

The `.gitignore` file prevents committing:
- Virtual environment directories (`.venv/`, `venv/`, `env/`)
- Ansible Vault password files
- Temporary files and cache directories
- IDE configuration files
- Local configuration files