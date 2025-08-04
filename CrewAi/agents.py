from openai import OpenAI
from dotenv import load_dotenv
import os
from crewai import Agent


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



##agent to extracts description from image and make it lists

ImageExtractor=Agent(
    role="Describe images and make a list of them",
    goal="Vision to describe images using gpt and then extracts object lists from descriptions",
    verbose=True,
    memory=True,
    backstory=(
        "This agents is expert in describing images with precision and detail useing tools like gpt and then extracts the object list from the description"
    ),
    tools=[],
    allow_delegation=False


)