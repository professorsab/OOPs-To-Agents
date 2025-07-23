from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=google_api_key
)

_1st_Prompt=PromptTemplate(
    input_variables=["job_description"],
    template="Extract the key responsibilities from this job description. Return only a bullet-point list:\n\n{job_description}"
)

_2nd_Prompt=PromptTemplate(
    input_variables=["responsibilities"],
    template="Analyze these job responsibilities and identify the top 3 hard skills required:\n\n{responsibilities}\n\n:" 
)

_3rd_Prompt=PromptTemplate(
    input_variables=["skills"],
    template="Write a 3-sentence professional summary for Alex, who is applying for this job. Highlight their alignment with these skills:\n{skills}\n\nSummary:"
)

_1st_chain=LLMChain(
    llm=llm,
    prompt=_1st_Prompt,
    output_key="responsibilities"
)

_2nd_chain=LLMChain(
    llm=llm,
    prompt=_2nd_Prompt,
    output_key="skills"
)

_3rd_chain=LLMChain(
    llm=llm,
    prompt=_3rd_Prompt,
    output_key="summary"
)

main_chain=SequentialChain(
    chains=[_1st_chain,_2nd_chain,_3rd_chain],
    input_variables=["job_description"],
    output_variables=["responsibilities", "skills", "summary"]
    
)

job_desc = """We are hiring a Data Scientist to join our team. Responsibilities include:
- Cleaning and preprocessing large datasets using Python and SQL
- Building predictive models with TensorFlow and scikit-learn
- Communicating insights to stakeholders through visualizations (Tableau/PowerBI)
- Collaborating with engineering teams to deploy ML models

Requirements:
- 3+ years of experience in machine learning
- Strong statistical analysis skills
- Proficiency in Python and cloud platforms (AWS/GCP)"""

result = main_chain({"job_description": job_desc})

# Print all results
print("RESPONSIBILITIES:")
print(result["responsibilities"])
print("\nTOP SKILLS:")
print(result["skills"])
print("\nSUMMARY FOR ALEX:")
print(result["summary"])