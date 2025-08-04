from crewai_tools import tool
from openai import OpenAI
client =OpenAI()
import base64

load_dotenv()
client=OpenAI(api_key=os.getenv("OPEN_API_KEY"))



@tool("Describe an Image using GPT-4o mini versions model")
def describe_image(image_path:str)->str:
    try:

        with open(image_path,"rb") as image_file:
            base64_image =base64.b64encode(image_file.read()).decode("utf-8")
        
        response =client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18"
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
    
