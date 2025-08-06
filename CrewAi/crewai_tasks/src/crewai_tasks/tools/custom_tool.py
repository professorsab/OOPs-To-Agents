from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class DescribeImageInput(BaseModel):
    """Input schema for DescribeImageTool."""
    image_path: str = Field(..., description="Path to the image file to be described")


class DescribeImageTool(BaseTool):
    name: str = "Describe Image"
    description: str = (
        "Describes an image using GPT-4o mini vision model. "
        "Useful for getting detailed descriptions of image content including objects, scenes, and visual elements."
    )
    args_schema: Type[BaseModel] = DescribeImageInput

    def _run(self, image_path: str) -> str:
        """
        Describes an image using GPT-4o mini vision model.
        
        Args:
            image_path (str): Path to the image file to be described
            
        Returns:
            str: Detailed description of the image content
        """
        try:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            
            response = client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "please describe this image in detail."
                        },
                        {
                            "type": "image_url", 
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                    ],
                }],
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"error describing image: {e}"


class ListObjectInput(BaseModel):
    """Input schema for ListObjectTool."""
    description: str = Field(..., description="Text description of an image to extract objects from")


class ListObjectTool(BaseTool):
    name: str = "Extract Objects"
    description: str = (
        "Extracts a list of objects from an image description. "
        "Useful for creating bullet-point lists of all objects, items, and entities mentioned in a description."
    )
    args_schema: Type[BaseModel] = ListObjectInput

    def _run(self, description: str) -> str:
        """
        Extracts a list of objects from an image description.
        
        Args:
            description (str): Text description of an image
            
        Returns:
            str: Bullet-point list of objects found in the description
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant that extracts objects from descriptions."
                    },
                    {
                        "role": "user", 
                        "content": f"From the following description, extract the list of objects in bullet points:\n\n{description}"
                    }
                ]
            )
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error {e}"


# Create instances of the tools for easy import
describe_image_tool = DescribeImageTool()
list_object_tool = ListObjectTool()
