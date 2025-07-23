# import google.generativeai as genai
# from langchain_core.prompts import PromptTemplate
# import os
# from langchain.chains import LLMChain

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Load the Gemini Flash model
# model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# # Generate a simple response
# Task1_1=PromptTemplate(
#     input_variable=["text"],
#     template="You are a professional summarization assistant who specializes in distilling complex information into concise and meaningful summaries. Your task is to summarize a given text into a single sentence that captures its essential points.Here is the text to summarize:  {text} The summary should be clear, straightforward, and include the most critical details from the text. Aim for a balance between brevity and comprehensiveness."
# )

# formatted_prompt = Task1_1.format(text="The Apollo 11 mission, launched by NASA on July 16, 1969, was the first manned spacecraft to land on the Moon. Astronauts Neil Armstrong and Buzz Aldrin became the first humans to walk on the lunar surface, while Michael Collins orbited above in the command module. Armstrong famously declared, 'That’s one small step for man, one giant leap for mankind.' The mission marked a pivotal achievement in the Space Race and demonstrated the United States' technological prowess during the Cold War.")


# response = model.generate_content(formatted_prompt)
# chain =LLMChain(llm=model,prompt=Task1_1)
# chain.run("The rapid advancement of artificial intelligence (AI) in recent years has revolutionized numerous industries, from healthcare to finance. In healthcare, AI-powered diagnostic tools can analyze medical images with remarkable accuracy, often detecting anomalies that human eyes might miss. Financial institutions leverage AI algorithms for fraud detection, risk assessment, and algorithmic trading, enabling faster and more secure transactions. Meanwhile, the education sector benefits from personalized learning platforms that adapt to individual students' needs. However, these advancements also raise significant ethical concerns, including job displacement due to automation, data privacy issues, and the potential for biased decision-making when AI systems are trained on flawed datasets. Governments and organizations worldwide are now grappling with the challenge of establishing regulatory frameworks that encourage innovation while mitigating risks. As AI continues to evolve at an unprecedented pace, society must find a balance between harnessing its transformative potential and addressing its complex societal implications.")
# print(response.text)
# print()



import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# # Initialize LangChain-compatible Gemini
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))


# Initialize with explicit API key
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Define prompt
prompt = PromptTemplate(
    input_variables=["text"],  # Fixed: Use input_variables (not input_variable)
    template="You are a professional summarization assistant who specializes in distilling complex information into concise and meaningful summaries. Your task is to summarize a given text into a single sentence that captures its essential points.Here is the text to summarize:  {text} The summary should be clear, straightforward, and include the most critical details from the text. Aim for a balance between brevity and comprehensiveness."
)

# Create and run chain
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(text="The Apollo 11 mission, launched by NASA on July 16, 1969, was the first manned spacecraft to land on the Moon. Astronauts Neil Armstrong and Buzz Aldrin became the first humans to walk on the lunar surface, while Michael Collins orbited above in the command module. Armstrong famously declared, 'That’s one small step for man, one giant leap for mankind.' The mission marked a pivotal achievement in the Space Race and demonstrated the United States' technological prowess during the Cold War.")  # Pass input as keyword argument
print(result)
