from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def generate_terraform(requirement):
    prompt = f"""
Act as a DevOps engineer.

Task:
Generate production-grade, policy-compliant infrastructure for:
{requirement}

Constraints:
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
  - expiration (30 days)
  - noncurrent_version_expiration (30 days)
  - transition to STANDARD_IA after 30 days
- Tags:
  - Main → Name, Environment, Owner, Project
  - Logging → Name, Environment, Owner, Project, Purpose=Logging

Output:
- Only Terraform code
- No explanation
- No markdown
- No backticks
"""
    return llm.invoke(prompt).content


def validate_terraform(code):
    prompt = f"""
Act as a Senior DevOps reviewer.

Task:
Carefully validate this Terraform code:

{code}

Context:
- Bucket names use random_id for uniqueness
- Lifecycle already includes expiration and transition
- Public access is already blocked
- Encryption is already enabled

Rules:
- Do NOT flag anything already implemented correctly
- Only report REAL missing or incorrect configurations
- Ignore best practices that are already satisfied

Output:
- Max 3 issues only
- Each issue = one short sentence
- Suggest improvement in one short line
- If no issues, say: "No critical issues found"
- Do NOT include code
"""
    return llm.invoke(prompt).content

def main():
    user_input = input("Enter requirement: ")

    code = generate_terraform(user_input)

    print("\nGenerated Code:\n", code)

    validation = validate_terraform(code)
    print("\nValidation:\n", validation)

if __name__ == "__main__":
    main()