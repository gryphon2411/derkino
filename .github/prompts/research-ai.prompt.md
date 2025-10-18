---
mode: ask
description: Generate effective research prompts for technical challenges (manually copiable to be used with research AIs)
---

## Research AI Prompt Template

**Usage:** Copy this template, fill in the placeholders with specific details, so the generated prompt will be manually copiable to be used with research AIs.

**Key Success Factor:** **Include concrete file content** - Research AIs cannot access your files, so you must provide explicit code snippets and error details.

Use this template to generate effective research prompts for technical challenges across various domains.

**Technology Stack:** ${input:techStack:technology/framework}
**Specific Challenge:** ${input:challenge:specific functionality}
**Error/Issue:** ${input:issue:specific error or issue}

### **Context:**
[Brief description of the technical challenge or problem domain]

### **Current Situation:**
[Specific details about what's currently not working or needs clarification]

### **Core Question:**
[Clear, focused question that gets to the heart of the issue]

### **Specific Technical Questions:**
1. [First specific technical aspect to research]
2. [Second specific technical aspect to research]
3. [Third specific technical aspect to research]
4. [Best practices or established patterns relevant to the issue]

### **Relevant File Context:**
**IMPORTANT: External AIs cannot access your files. Describe file contents explicitly.**

**File 1 - ${input:file1Name:primary configuration file}:**
```
${input:file1Content:full relevant code section or configuration}
```

**File 2 - ${input:file2Name:supporting file}:**
```
${input:file2Content:key code sections or configuration}
```

**File 3 - ${input:file3Name:error-related file}:**
```
${input:file3Content:specific code causing issues}
```

**Error Details:**
```
${input:errorDetails:specific error message or log output}
```

**GitHub Actions Context (if applicable):**
- Workflow: ${input:workflowName:workflow file name}
- Step: ${input:failingStep:specific step that fails}
- Error Code: ${input:errorCode:numeric error code if available}
- Workspace: ${workspaceFolderBasename}

### **Desired Outcome:**
[A clear, actionable recommendation or definitive answer]

### **Example Usage - General Template:**

**Context:** I'm working on a ${input:techStack} project that involves ${input:challenge}.

**Current Situation:** [Component/feature] is failing with ${input:issue} because [reason].

**Core Question:** What is the proper approach for [specific technical challenge]?

**Specific Technical Questions:**
1. Architecture: How should [component] be structured?
2. Configuration: What is the correct way to configure [specific settings]?
3. Integration: How to properly integrate [component A] with [component B]?
4. Best Practices: Are there established patterns for this type of implementation?

**Relevant File Context:**
**IMPORTANT: External AIs cannot access files. Describe contents explicitly.**

- **[File 1]**: [Brief description of file's role] - [Include relevant code snippets or describe key configurations]
- **[File 2]**: [Brief description of file's role] - [Include relevant code snippets or describe key configurations]
- **[File 3]**: [Brief description of file's role] - [Include relevant code snippets or describe key configurations]

**Desired Outcome:** A clear, industry-standard approach for [specific technical challenge].

### **Example Usage - Specific (CI/CD Pipeline):**

**Context:** I'm working on a ${input:techStack} CI/CD pipeline that validates ${input:challenge}.

**Current Situation:** The pipeline is failing due to ${input:issue} despite fixing the original configuration issue.

**Core Question:** What is the proper approach for handling ${input:specificIssue:dependency/configuration} issues in CI/CD workflows?

**Specific Technical Questions:**
1. Dependency Resolution: When should external dependencies be installed relative to validation steps?
2. Tool Configuration: How does the validation tool discover and use external dependencies?
3. Error Handling: Are there configuration settings that can ignore specific validation errors?
4. Best Practices: What is the recommended approach for projects with external dependencies?

**Relevant File Context:**
**IMPORTANT: External AIs cannot access files. Describe contents explicitly.**

**File 1 - CI/CD Workflow (${input:workflowFile:path/to/workflow}):**
```yaml
${input:workflowContent:relevant workflow configuration}
```

**File 2 - Configuration File (${input:configFile:path/to/config}):**
```yaml
${input:configContent:relevant configuration sections}
```

**File 3 - Source Code (${input:sourceFile:path/to/source}):**
```${input:language:programming language}
${input:sourceContent:code causing issues}
```

**Error Details:**
```
${input:errorDetails:specific error message or log output}
```

**CI/CD Context:**
- Platform: ${input:platform:GitHub Actions/Jenkins/etc}
- Step: ${input:failingStep:specific step that fails}
- Error Code: ${input:errorCode:numeric error code if available}

**Desired Outcome:** A clear, industry-standard approach for handling ${input:specificIssue:dependency/configuration} issues in CI/CD workflows.

**Example Usage - Specific (Infrastructure as Code):**

**Context:** I'm working on an ${input:techStack} infrastructure project using ${input:tool:configuration management tool}.

**Current Situation:** The ${input:component:chart/module/template} was automatically generated but failing validation due to ${input:issue:missing references/configuration}.

**Core Question:** What is the proper structure for ${input:component:umbrella chart/module} that orchestrates multiple ${input:subcomponents:subcharts/modules}?

**Specific Technical Questions:**
1. Template/Module Structure: What components should remain in the main structure?
2. Configuration Organization: How should configuration files be structured?
3. Validation Strategy: How to make the component pass validation/linting?
4. Best Practices: Are there established patterns for this type of infrastructure component?

**Relevant File Context:**
**IMPORTANT: External AIs cannot access files. Describe contents explicitly.**

**File 1 - Main Configuration (${input:mainConfig:path/to/main/config}):**
```${input:configType:yaml/json}
${input:mainConfigContent:relevant configuration sections}
```

**File 2 - Values/Parameters (${input:valuesFile:path/to/values}):**
```${input:configType:yaml/json}
${input:valuesContent:configuration values}
```

**File 3 - Template/Module (${input:templateFile:path/to/template}):**
```${input:templateLanguage:template language}
${input:templateContent:template causing issues}
```

**Error Details:**
```
${input:errorDetails:specific validation error}
```

**Tool Context:**
- Tool: ${input:tool:Helm/Terraform/Ansible}
- Validation Step: ${input:validationStep:specific validation command}
- Error Type: ${input:errorType:validation/syntax error}

**Desired Outcome:** A clear, industry-standard approach for structuring ${input:component:infrastructure components}.

### **Critical: Include Concrete File Content**
**Research AIs CANNOT access your files. You MUST provide explicit content.**

**File Content Requirements:**
- **Full code snippets**: Include the actual YAML/JSON/configuration that's relevant
- **Error details**: Copy-paste the exact error messages from logs
- **Line numbers**: Include line numbers or specific error locations
- **Code blocks**: Use triple backticks with language identifiers for readability

**Why this matters:**
- Without concrete file content, the AI cannot analyze your specific configuration
- Generic descriptions lead to generic, unhelpful answers
- Specific error messages allow the AI to diagnose exact issues
- File content enables the AI to suggest precise fixes

**Bad Example (vague):** "My workflow fails with collection errors"
**Good Example (specific):** 
```
WARNING: Error loading plugin 'kubernetes.core.k8s': No module named 'ansible_collections.kubernetes'
parser-error: couldn't resolve module/action 'kubernetes.core.k8s'.
roles/secrets/tasks/kafka.yml:3:3
```

**Bad Example (no file content):** "My values.yaml has configuration issues"
**Good Example (with content):**
```yaml
mongodb:
  service:
    port: 27017
postgresql:
  service:
    port: 5432
```

### **Tips for Effective Research Prompts:**
- Be specific about the technology stack and version
- Include error messages or specific symptoms
- Mention what you've already tried
- Specify whether you're looking for best practices, troubleshooting, or architectural guidance
- Include relevant code snippets or configuration examples when possible
- **Always assume the AI cannot access your files** - describe file contents explicitly
- **Generated prompt will be manually copied** - and will be manually pasted into a research AI tool