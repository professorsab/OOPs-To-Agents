from crewai.tools import tool
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()
client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



@tool("Describe an Image using GPT-4o mini versions model")
def describe_image(image_path:str)->str:
    """
    Describes an image using GPT-4o mini vision model.
    
    Args:
        image_path (str): Path to the image file to be described
        
    Returns:
        str: Detailed description of the image content
    """
    try:

        with open(image_path,"rb") as image_file:
            base64_image =base64.b64encode(image_file.read()).decode("utf-8")
        
        response =client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{
                "role":"user",
                "content":[
                    {
                        "type":"text","text":"please describe this image in detail."
                    },
                    {"type":"image_url","image_url":{
                        "url":f"data:image/jpeg;base64,{base64_image}"
                    },},
                ],

            },
            ],
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"error describing image: {e}"
    




@tool("extract object list from image description ")
def list_object(description:str)->str:
    """
    Extracts a list of objects from an image description.
    
    Args:
        description (str): Text description of an image
        
    Returns:
        str: Bullet-point list of objects found in the description
    """
    try:
        response=client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role":"system","content":"You are a helpful assistant that extracts objects from descriptions."},
                {"role":"user","content":f"From the following description, extract the list of objects in bullet points:\n\n{description}"}
            ]
            
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error {e}"


    
