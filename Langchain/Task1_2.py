import os
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
import google.generativeai as genai

model = genai.GenerativeModel(model_name="gemini-2.5-flash")
examples=[{"Text":"I got a promotion today!","Label":"Happy",}, {"Text":"My Dog  passed away.","Label":"Sad",},]

Example_prompt=PromptTemplate(
    input_variables=["Text","Label"],template="{Text}\n{Label}"
)


prompt=FewShotPromptTemplate(
    examples=examples,
    example_prompt=Example_prompt,
    prefix="Classify the Sentiment of these texts as either Happy or Sad",
    suffix="Text: {Text}\nLabel:",
    input_variables=["Text"]
    
)

my_prompt=prompt.format(
    Text="i have been selected for stanford university"
)

response =model.generate_content(my_prompt)

print (response.text)