from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def generate_terraform(requirement):
    prompt = f"Create Terraform code for: {requirement}"
    return llm.invoke(prompt).content

def validate_terraform(code):
    prompt = f"Validate this Terraform code and suggest fixes:\n{code}"
    return llm.invoke(prompt).content

def main():
    user_input = input("Enter requirement: ")

    code = generate_terraform(user_input)
    print("\nGenerated Code:\n", code)

    validation = validate_terraform(code)
    print("\nValidation:\n", validation)

if __name__ == "__main__":
    main()