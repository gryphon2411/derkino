# Derkino Infrastructure Deployment

This directory contains the Ansible and Helm-based deployment system for Derkino infrastructure.

## New Standard CI Validation Pipeline

### Prerequisites
- Helm 3.14+

### Pipeline Sequence

#### 1. Checkout Repository
```bash
git clone https://github.com/gryphon2411/derkino.git
cd derkino
```

#### 2. Build Dependencies from Lock File
```bash
cd infrastructure/helm-charts/derkino-infrastructure
helm dependency build .
```

#### 3. Validate the Chart
```bash
helm lint --with-subcharts .
```

#### 4. Template Validation (Most Powerful Check)
```bash
helm template --debug .
```

### Local Development Workflow

#### For Infrastructure Changes
1. Make changes to Helm charts or Ansible playbooks
2. Test locally:
   ```bash
   cd infrastructure/helm-charts/derkino-infrastructure
   helm dependency update .
   helm lint --with-subcharts .
   ```
3. Commit changes including updated `Chart.lock` file
4. Push to trigger CI/CD pipeline

#### For Dependency Updates
1. Update dependency versions in `Chart.yaml` files
2. Run:
   ```bash
   helm dependency update .
   ```
3. Commit updated `Chart.lock` file
4. The CI/CD pipeline will use `helm dependency build` for reproducible builds

### File Structure

```
### File Structure

infrastructure/
├── ansible/                    # Ansible playbooks and roles
│   ├── deploy.yml             # Main deployment playbook
│   ├── roles/
│   │   ├── helm/              # Helm deployment tasks
│   │   ├── secrets/           # Secret management
│   │   └── migration/         # Zero-downtime migration
│   └── inventory/             # Environment-specific configurations
├── helm-charts/               # Helm charts
│   └── derkino-infrastructure/
│       ├── Chart.yaml         # Parent chart definition
│       ├── Chart.lock         # Dependency lock file
│       ├── values.yaml        # Default values
│       ├── .gitignore         # Exclude downloaded dependencies
│   └── charts/            # Subcharts
│       ├── mongodb/
│       ├── postgresql/
│       ├── redis-stack/
│       └── kafka/
└── secrets/                   # Encrypted secrets (not in repo)
```

### Environment Configuration

#### Local Development
```bash
cd infrastructure/ansible
ansible-playbook deploy.yml -e env=local
```

#### Dev Environment
```bash
ansible-playbook deploy.yml -e env=dev
```

### Validation Commands

#### Helm Validation
```bash
# Lint all charts
helm lint --with-subcharts .

# Dry-run installation
helm install test-install . --dry-run
```

#### Ansible Validation
```bash
# Syntax check
ansible-playbook --syntax-check deploy.yml

# Dry-run deployment
ansible-playbook --check deploy.yml

# Lint validation
ansible-lint deploy.yml
```

### Security

- **Secure secret handling**: Secrets managed via Ansible Vault with `no_log: true` to prevent logging
- **Non-root containers**: All infrastructure components run with `runAsNonRoot: true`
- **StatefulSet for databases**: MongoDB and PostgreSQL use StatefulSet for stable storage and network identity
- **Secret scanning**: CI pipeline includes TruffleHog to detect accidental secret commits
- **Downloaded Helm dependencies excluded** via `.gitignore`
- **All configurations version-controlled**
- **Dependencies pinned** via `Chart.lock` for reproducible builds

### Troubleshooting

#### Dependency Issues
If you encounter dependency warnings:
```bash
cd infrastructure/helm-charts/derkino-infrastructure
helm dependency update .
helm dependency build .
```

#### Validation Failures
Check the specific component:
```bash
# Check individual chart
helm lint charts/mongodb/

# Check Ansible syntax
ansible-playbook --syntax-check deploy.yml
```

This workflow ensures reliable, reproducible infrastructure deployments following Helm and Ansible best practices.