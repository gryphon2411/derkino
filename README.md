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
   
   # The directory structure is created by the Ansible/Helm deployment system
   # No manual creation needed after cloning
   ```

3. **Set up Ansible Vault (Security Critical)**:

   Ansible Vault passwords should NEVER be committed to version control. Use one of these secure methods:

   ## Option 1: Environment Variable
   ```bash
   export ANSIBLE_VAULT_PASSWORD="your_secure_password"
   ```

   ## Option 2: External Password File
   ```bash
   # Create a secure vault password file (DO NOT COMMIT THIS FILE)
   echo "your_secure_local_password" > ~/.derkino-local-vault-password
   chmod 600 ~/.derkino-local-vault-password
   ```

   ## Option 3: Prompt for Password
   ```bash
   # Will prompt interactively for vault password
   ```

   ## Creating Secrets File
   
   Create your secrets file based on the template:
   ```bash
   # Copy the template
   cp deployment/secrets/secrets-template.yml deployment/secrets/local/secrets.yml
   
   # Edit with your actual passwords
   nano deployment/secrets/local/secrets.yml
   
   # Encrypt the file
   ansible-vault encrypt deployment/secrets/local/secrets.yml
   ```

4. **Deploy to local environment**:
   ```bash
   # Deploy using Ansible with local environment
   # Choose one of these secure vault password methods:
   
   # Option 1: Environment variable
   export ANSIBLE_VAULT_PASSWORD="your_secure_local_password"
   ansible-playbook deployment/ansible/deploy.yml -i deployment/ansible/inventory/local -e "environment=local"
   
   # Option 2: External password file
   ansible-playbook deployment/ansible/deploy.yml -i deployment/ansible/inventory/local -e "environment=local" --vault-password-file ~/.derkino-local-vault-password
   
   # Option 3: Prompt for password
   ansible-playbook deployment/ansible/deploy.yml -i deployment/ansible/inventory/local -e "environment=local" --ask-vault-pass
   
   # Use --check flag to test playbook execution without making changes
   # ansible-playbook deployment/ansible/deploy.yml -i deployment/ansible/inventory/local -e "environment=local" --vault-password-file ~/.derkino-local-vault-password --check
   ```

5. **Deploy to dev environment**:
   ```bash
   # Deploy using Ansible with dev environment
   # Choose one of these secure vault password methods:
   
   # Option 1: Environment variable
   export ANSIBLE_VAULT_PASSWORD="your_secure_dev_password"
   ansible-playbook deployment/ansible/deploy.yml -i deployment/ansible/inventory/dev -e "environment=dev"
   
   # Option 2: External password file
   ansible-playbook deployment/ansible/deploy.yml -i deployment/ansible/inventory/dev -e "environment=dev" --vault-password-file ~/.derkino-dev-vault-password
   
   # Option 3: Prompt for password
   ansible-playbook deployment/ansible/deploy.yml -i deployment/ansible/inventory/dev -e "environment=dev" --ask-vault-pass
   
   # Use --check flag to test playbook execution without making changes
   # ansible-playbook deployment/ansible/deploy.yml -i deployment/ansible/inventory/dev -e "environment=dev" --vault-password-file ~/.derkino-dev-vault-password --check
   ```

### How It Works

- **Helm Charts**: Kubernetes resources are templated using Helm charts in `deployment/helm-charts/`
  - `derkino-infrastructure/`: For databases, messaging, and monitoring
  - `derkino-services/`: For backend microservices
  - `derkino-ui/`: For the frontend application

- **Ansible Orchestration**: The `deployment/ansible/deploy.yml` playbook coordinates the deployment:
  - Loads environment-specific variables from `ansible/environments/`
  - Uses Ansible Vault for secure secret management (vault passwords must be stored locally and never committed)
  - Manages the deployment of Helm charts in the correct order

- **Environment Configuration**:
  - `deployment/ansible/environments/local.yml`: `api_host_url: "http://local.derkino.com"`, `kubernetes_context: "minikube"`
  - `deployment/ansible/environments/dev.yml`: `api_host_url: "http://dev.derkino.com"`, `kubernetes_context: "dev-cluster"`

### Accessing the Application

After deployment, access the application at:
- Local: http://local.derkino.com
- Dev: http://dev.derkino.com

### Security Notice

**Important**: Never commit Ansible Vault password files to version control. These files contain the decryption keys to all your secrets and putting them in the repository puts the entire system at risk of compromise. 

Per Ansible's own documentation:
> "Do not add password files to source control."

Store vault passwords in a secure secret manager (HashiCorp Vault, 1Password, Bitwarden) or share them with the team via encrypted channels (Signal, PGP).

Only encrypted secrets (e.g., `secrets/local/db-password.yml`) should be committed, and access to this repository should be restricted.

## Components
![Derkino Components Diagram](/architecture/components.drawio.svg)
