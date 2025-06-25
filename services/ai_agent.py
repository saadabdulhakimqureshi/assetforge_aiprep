from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_recommendations(context):
    prompt = f"""
    Given a project with the following context:
    - Description: {context.description}
    - Genres: {', '.join(context.genres)}
    - Setting: {context.setting or 'Not specified'}

    Recommend a list of high-quality Fab assets (props, environments, characters) that would be most useful for this type of project.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response
