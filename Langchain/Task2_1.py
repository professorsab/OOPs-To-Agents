from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

llm=ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="AIzaSyBcc3o-tG6-okAkM1JAbZnswGMMK60UCgg"
)

Task2_1=PromptTemplate(
    input_variables=["product"],
    template="Generate a creative name for a company that makes {product} Please only give me one name"
)


# name_chain = Task2_1 | llm  
# result = name_chain.invoke({"product": "eco friendly water bottles"})
# print(result.content)  # Access content properly


Task2_1b=PromptTemplate(
    input_variables=["company_name"],
    template="Create a catchy slogan for this company: {company_name}"
    
) 


name_chain = LLMChain(
    llm=llm,
    prompt=Task2_1,
    output_key="company_name" 
)

slogan_chain = LLMChain(
    llm=llm,
    prompt=Task2_1b,
    output_key="slogan"  
)

main_chain = SequentialChain(
    chains=[name_chain, slogan_chain],
    input_variables=["product"],    
    output_variables=["slogan"], 
    verbose=False                  
)

result = main_chain({"product": "eco friendly water bottles"})
print(result["slogan"])  