from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

llm = AzureChatOpenAI(model="gpt-4o-mini", 
                      temperature=0)

def read_files_from_folder(folder_path):
    try:
        for root, _, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file:
                        yield file.read()
    except Exception as e:
        print(f"An error occurred: {e}")
        

def main():
    folder_path =r""
    files = [file_content for file_content in read_files_from_folder(folder_path)]
    top_files = files[:5]
    print(len(top_files))
    print(top_files[0])
    
    PROMPT = """
    Analyze the following code and provide a summary of its functionality.
    Generate the output in the following format provided in the output section:
    
    Code:
    {code}
    
    Output:
    Purpose: A brief description of the code's purpose.
    Summary: Summary of its functionality.
    """
    prompt = PromptTemplate(template=PROMPT)
    chain = prompt | llm
    response = chain.invoke({"code": top_files[0]})
    print(response.content)
    #for file in top_files:
    #    print(file)
    
if __name__ == "__main__":
    main()
