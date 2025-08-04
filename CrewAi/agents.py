from openai import OpenAI
from dotenv import load_dotenv
import os
from crewai import Agent,Task,Crew
from tools import describe_image,list_object


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
    tools=[describe_image,list_object],
    allow_delegation=False


)



crewAi_agent=Task(
    description=( "Take the image file at {image_path}, describe it using the vision model, "
        "then extract a bullet-point list of all the objects visible in the image."
   ),
    expected_output="A detailed bullet-point list of objects seen in the image.",
    agent=ImageExtractor,
    tools=[describe_image,list_object],
    async_execution=False,
    output_file="output.txt",
)

crew=Crew(
    agents=[ImageExtractor],
    tasks=[crewAi_agent],
    verbose=True
    
)


image_path = 'mahad.jpg' 

print("Crew AI in action...")
result = crew.kickoff(inputs={"image_path": image_path})
    