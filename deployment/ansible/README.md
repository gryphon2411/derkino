# Ansible Development Environment

This directory contains Ansible playbooks and roles for deploying the Derkino 
application infrastructure.

## Virtual Environment Setup

A Python virtual environment is configured for Ansible development to avoid 
system Python conflicts.

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

# Run playbook with local inventory (using secure vault password)
# Option 1: Environment variable
export ANSIBLE_VAULT_PASSWORD="your_secure_password"
ansible-playbook -i inventory/local deploy.yml

# Option 2: External password file
ansible-playbook -i inventory/local deploy.yml --vault-password-file ~/.derkino-vault-password

# Option 3: Prompt for password
ansible-playbook -i inventory/local deploy.yml --ask-vault-pass

# Run with migration enabled
ansible-playbook -i inventory/local deploy.yml -e "migration_enabled=true" --vault-password-file ~/.derkino-vault-password
```

## Environment Configuration

### Environment Variables

Environment-specific configuration is managed through:

- `environments/local.yml` - Local development settings
- `environments/dev.yml` - Development environment settings
- `group_vars/all/vars.yml` - Global variables across all environments

**Key Configuration Variables:**

| Variable | Purpose | Default |
|----------|---------|---------|
| `deployment_environment` | Target environment (local, dev, prod) | local |
| `migration_enabled` | Enable/disable migration mode | false |
| `helm_infrastructure_namespace` | Kubernetes namespace | infrastructure |
| `secrets_namespace` | Secrets namespace | infrastructure |

### Inventory Files

Inventory files define target hosts for deployment:

- `inventory/local` - Local Minikube/Kubernetes cluster
- `inventory/dev` - Development cluster

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

## Deployment Workflow

### Standard Deployment (Helm Charts Only)

This is the primary deployment method for new installations or when migrating 
from kubectl manifests is not required.

```bash
# Activate virtual environment
source .venv/bin/activate

# Deploy infrastructure using Helm charts
ansible-playbook -i inventory/local deploy.yml -e "deployment_environment=local"
```

### Migration Deployment (Zero-Downtime)

Use this method when migrating from existing kubectl manifests to Helm charts 
without downtime.

```bash
# Activate virtual environment
source .venv/bin/activate

# Enable migration mode
ansible-playbook -i inventory/local deploy.yml -e "deployment_environment=local 
migration_enabled=true"
```

### Infrastructure Components

The playbook deploys these core infrastructure components:

| Component | Helm Chart | Purpose |
|-----------|------------|---------|
| **MongoDB** | `derkino-infrastructure/mongodb` | Document database for titles 
and metadata |
| **PostgreSQL** | `derkino-infrastructure/postgresql` | Relational database 
for auth and transactions |
| **Redis-Stack** | `derkino-infrastructure/redis-stack` | Caching and session 
management |
| **Kafka** | `derkino-infrastructure/kafka` | Event streaming and message 
broker |

## Development Workflow

1. **Activate virtual environment**: `source .venv/bin/activate`
2. **Edit playbooks/roles**: Make changes to YAML files
3. **Validate with ansible-lint**: `ansible-lint deploy.yml`
4. **Test locally**: `ansible-playbook -i inventory/local deploy.yml -e 
"deployment_environment=local"`
5. **Commit changes**: Git will ignore virtual environment files

## Role Documentation

### Helm Role
Deploys infrastructure components using Helm charts with comprehensive health 
checks and rollback procedures.

**Key Features:**
- Zero-downtime upgrades using `helm upgrade --install`
- Service connectivity testing after deployment
- Automatic rollback on failure using block/rescue patterns
- Namespace management with `--create-namespace`

**Configuration:**
- `helm_infrastructure_namespace`: Target namespace (default: "infrastructure")
- `helm_charts_path`: Path to Helm charts directory

### Migration Role
Implements zero-downtime migration from kubectl manifests to Helm charts.

**Migration Process:**
1. Deploy parallel infrastructure in `infrastructure-parallel` namespace
2. Wait for parallel services to be ready
3. Test connectivity to parallel services
4. Switch traffic using service selector patches
5. Remove original kubectl infrastructure

**Safety Features:**
- Conditional execution based on existing infrastructure
- Rollback procedures for failed traffic switching
- Comprehensive health checks throughout migration

### Secrets Role
Manages Kubernetes secrets using Ansible Vault for secure secret storage.

**Workflow:**
1. Ensure vault password file exists
2. Decrypt secrets file if encrypted
3. Apply secrets to Kubernetes
4. Re-encrypt secrets file

**Security:**
- Vault password stored in environment variable or group_vars
- Secrets file encrypted at rest
- Proper file permissions (0600) for vault password

## Troubleshooting

### Common Issues

**Helm Repository Issues:**
```bash
# Add repository manually if needed
helm repo add derkino-infrastructure 
deployment/helm-charts/derkino-infrastructure
helm repo update derkino-infrastructure
```

**Kubernetes Connectivity:**
```bash
# Verify kubectl can connect to cluster
kubectl cluster-info
kubectl get nodes
```

**Ansible Vault Issues:**
```bash
# Set vault password environment variable
export ANSIBLE_VAULT_PASSWORD="your_password"
```

**Rollback Procedures:**
If a deployment fails, the playbook automatically rolls back using Helm 
uninstall commands. Manual intervention may be required for complex failures.

## Quality Assurance

### Code Quality

The Ansible codebase follows strict quality standards:

- **ansible-lint compliance**: All code passes default ansible-lint rules
- **FQCN usage**: Uses `ansible.builtin.*` for built-in modules
- **Idempotency**: Commands include `changed_when: false` where appropriate
- **YAML formatting**: Proper indentation, line lengths, and no trailing spaces

### Testing Strategies

**Syntax Validation:**
```bash
ansible-playbook --syntax-check deploy.yml -e "deployment_environment=local"
```

**Dry-Run Testing:**
```bash
ansible-playbook --check deploy.yml -e "deployment_environment=local"
```

**Linting:**
```bash
ansible-lint deploy.yml
```

**Service Connectivity Testing:**
- MongoDB: `mongosh --eval "db.adminCommand({ping: 1})"`
- PostgreSQL: `psql -U postgres -c "SELECT 1;"`
- Redis: `redis-cli ping`
- Kafka: `kafka-topics.sh --bootstrap-server localhost:9092 --list`

## Milestone 2: Infrastructure Migration

This Ansible implementation completes **Milestone 2: Infrastructure Migration** 
which replaces kubectl manifests with version-controlled Helm charts driven by 
Ansible.

### Key Achievements

✅ **Helm Charts**: 4 core infrastructure components (MongoDB, PostgreSQL, 
Redis-Stack, Kafka)
✅ **Ansible Roles**: Helm deployment, zero-downtime migration, secrets 
management
✅ **Quality Standards**: Full ansible-lint compliance with default rules
✅ **Service Connectivity**: Comprehensive health checks and connectivity 
testing
✅ **Rollback Procedures**: Automatic recovery from failed deployments
✅ **Documentation**: Complete deployment workflow and troubleshooting guide

### Success Metrics

- **Deployment time**: ≤ 15 minutes from clean cluster to running services
- **Lint compliance**: `ansible-lint` returns 0 failures, 0 warnings
- **Migration safety**: Zero-downtime switch from kubectl to Helm
- **Team adoption**: Clear documentation for ≤ 30 minute deployment

## Git Ignore Rules

The `.gitignore` file prevents committing:
- Virtual environment directories (`.venv/`, `venv/`, `env/`)
- Ansible Vault password files
- Temporary files and cache directories
- IDE configuration files
- Local configuration files