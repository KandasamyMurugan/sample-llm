import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# Generate MULTI-FILE Terraform project
def generate_terraform_project(requirement):
    prompt = f"""
Act as a DevOps engineer.

Task:
Generate a production-grade Terraform project for:
{requirement}

Constraints:
- Use AWS region us-east-1
- Use latest Terraform version and feature
- Use AWS provider version ~> 6.0
- Define provider version only in required_providers block
- Do NOT define version inside provider block
- Use ONLY non-deprecated resources
- DO NOT use server_side_encryption_configuration inside aws_s3_bucket
- Use aws_s3_bucket_server_side_encryption_configuration resource
- Follow AWS provider v5 syntax strictly
- Avoid deprecated arguments completely
- Use correct lifecycle syntax:
  noncurrent_version_expiration must use noncurrent_days
- Ignore deprecated options
- Follow best practices
CRITICAL:
- required_version MUST be inside terraform block ONLY
- NEVER place required_version inside provider block
- Use multiple files:
  - provider.tf
  - main.tf
  - variables.tf
  - outputs.tf
  - terraform.tfvars
  - Create .gitingore file to add the terraform.tfstate and terraform.tfstate.backup and other required files
- Include AWS provider with region us-east-1
- MUST include:
  - random_id resource
  - aws_s3_bucket (main)
  - aws_s3_bucket (logging)
  - aws_s3_bucket_public_access_block (for BOTH buckets)
  - aws_s3_bucket_lifecycle_configuration (main)
  - aws_s3_bucket_logging (main)
- Bucket names MUST use random_id suffix for global uniqueness
- Do NOT use ACL anywhere
- Enable versioning on both buckets
- Enable server-side encryption (AES256) on both buckets
- Block all public access on both buckets
- Enable server access logging (main → logging)
- Add depends_on for logging bucket
- Lifecycle must include:
  - transition to STANDARD_IA after 30 days
  - expiration MUST be greater than transition (e.g., 60 days)
- Tags:
  - Main → Name, Environment, Owner, Project
  - Logging → Name, Environment, Owner, Project, Purpose=Logging
- Add # infront of all the descriptions in the terraform files
- Do NOT include any explanations
- Do NOT include any plain English sentences
- Do NOT include backticks or markdown
- terraform.tfvars MUST contain ONLY key=value pairs
- terraform.tfvars values MUST be valid HCL
- All string values MUST be in double quotes
- Do NOT use versioning block inside aws_s3_bucket
- Use aws_s3_bucket_versioning resource
- Add below content in .gitignore folder.
# Terraform
.terraform/
*.tfstate
*.tfstate.*
.terraform.lock.hcl

# Variables
*.tfvars
*.tfvars.json

# Crash logs
crash.log

# OS / IDE
.DS_Store
Thumbs.db
.vscode/
.idea/
*.terraform_project/.terraform/providers/.../terraform-provider-aws_v6.41.0_x5.exe

### terraform.tfvars
<only valid tfvars content>


Output format STRICT:
### provider.tf
<code>

### main.tf
<code>

### variables.tf
<code>

### outputs.tf
<code>

### terraform.tfvars
<code>
"""
    return llm.invoke(prompt).content


# Save files automatically
def clean_code(content):
    # Remove markdown fences
    content = content.replace("```hcl", "")
    content = content.replace("```", "")
    return content.strip()

if os.path.exists("terraform_project/.terraform"):
    os.system("rm -rf terraform_project/.terraform")


def save_terraform_files(output):
    project_dir = "terraform_project"
    os.makedirs(project_dir, exist_ok=True)

    parts = output.split("###")

    for part in parts:
        if ".tf" in part:
            try:
                filename, content = part.split("\n", 1)

                filepath = os.path.join(project_dir, filename.strip())

                # CLEAN HERE
                cleaned_content = clean_code(content)

                with open(filepath, "w") as f:
                    f.write(cleaned_content)

                print(f"Created: {filepath}")

            except Exception as e:
                print("Error saving file:", e)


# Optional: Run Terraform
def run_terraform():
    os.chdir("terraform_project")

    print("\nRunning terraform init...")
    os.system("terraform init")

    print("\nRunning terraform plan...")
    os.system("terraform plan")

    apply = input("\nApply changes? (yes/no): ")
    if apply.lower() == "yes":
        os.system("terraform apply -auto-approve")

        destroy = input("\nDestroy resources after apply? (yes/no): ")
        if destroy.lower() == "yes":
            print("\nDestroying infrastructure...")
            os.system("terraform destroy -auto-approve")
        else:
            print("Resources kept running")
    else:
        print("Skipped apply")


# MAIN
def main():
    user_input = input("Enter requirement: ")

    output = generate_terraform_project(user_input)

    print("\nGenerated Terraform Project:\n")
    print(output)

    save_terraform_files(output)

    run = input("\nRun Terraform now? (yes/no): ")
    if run.lower() == "yes":
        run_terraform()


if __name__ == "__main__":
    main()