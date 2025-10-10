![Derkino Shadowed Scaled Logo](/graphic-designs/logo-shadow-scaled.png)

# Derkino

Derkino ("The cinema"), derived from Yiddish (דער קינאָ), represents a personal educational initiative focused on exploring various technologies within the context of a cinema.

## Provision (Legacy)
```bash
$ basename "$(pwd)"
derkino
$ source ./orchestrators/k8s/provision.sh
```

> **Note**: The legacy provision.sh script is deprecated. Use the new Ansible/Helm deployment system below.

## Deployment System

The Derkino deployment system has been refactored to use a declarative Ansible/Helm workflow for consistent, repeatable deployments across environments.

### Setup Instructions

1. **Install dependencies** (one-time setup):
   - Ansible 2.9+
   - Helm 3+
   - kubectl
   - minikube

2. **Initialize the deployment system**:
   ```bash
   # Clone the repository (if not already done)
   git clone https://github.com/gryphon2411/derkino.git
   cd derkino
   
   # The directory structure is automatically created with the repository
   # No manual creation needed
   ```

3. **Deploy to local environment**:
   ```bash
   # Deploy using Ansible with local environment
   ansible-playbook deployment/ansible/deploy.yml -i deployment/ansible/inventory/local -e "environment=local" --vault-id @deployment/secrets/local/ansible-vault-password
   
   # Use --check flag to test playbook execution without making changes
   # ansible-playbook ansible/deploy.yml -i deployment/ansible/inventory/local -e "environment=local" --check
   ```

4. **Deploy to dev environment**:
   ```bash
   # Deploy using Ansible with dev environment
   ansible-playbook deployment/ansible/deploy.yml -i deployment/ansible/inventory/dev -e "environment=dev" --vault-id @deployment/secrets/dev/ansible-vault-password
   
   # Use --check flag to test playbook execution without making changes
   # ansible-playbook ansible/deploy.yml -i ansible/inventory/dev -e "environment=dev" --check
   ```

### How It Works

- **Helm Charts**: Kubernetes resources are templated using Helm charts in `deployment/helm-charts/`
  - `derkino-infrastructure/`: For databases, messaging, and monitoring
  - `derkino-services/`: For backend microservices
  - `derkino-ui/`: For the frontend application

- **Ansible Orchestration**: The `deployment/ansible/deploy.yml` playbook coordinates the deployment:
  - Loads environment-specific variables from `ansible/environments/`
  - Uses Ansible Vault (`secrets/local/`, `secrets/dev/`) for secure secret management
  - Manages the deployment of Helm charts in the correct order

- **Environment Configuration**:
  - `deployment/ansible/environments/local.yml`: `api_host_url: "http://local.derkino.com"`, `kubernetes_context: "minikube"`
  - `deployment/ansible/environments/dev.yml`: `api_host_url: "http://dev.derkino.com"`, `kubernetes_context: "dev-cluster"`

### Accessing the Application

After deployment, access the application at:
- Local: http://local.derkino.com
- Dev: http://dev.derkino.com

## Components
![Derkino Components Diagram](/architecture/components.drawio.svg)
