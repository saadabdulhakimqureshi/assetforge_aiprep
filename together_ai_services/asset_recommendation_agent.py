from together import Together
from models.categories import categories
from models.request_model import ProjectContext
import json

class AssetRecommendationAgent:
    def __init__(self, client):
        self.client = client

    async def fetch_assets(self, context: ProjectContext):
        response = self.client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Given a project with the following context:
                    - Description: {context.description}
                    - Genres: {', '.join(context.genres)}
                    - Setting: {context.setting or 'Not specified'}

                    Recommend a list of high-quality Fab assets (props, environments, characters) that would be most useful for this type of project.

                    Only return the list in this exact format:
                    [
                        {{
                            "title": "string",
                            "description": "string",
                            "storeLink": "string"
                        }},
                        ...
                    ]
                    """
                                    }
                                ]
                            )
        
        return response.choices[0].message.content
    
    async def categorize_assets(self, assets_json_str: str):
        response = self.client.chat.completions.create(
                        model="deepseek-ai/DeepSeek-V3",
                        messages=[
                            {
                                "role": "user",
                                "content": f"""
            You are given a list of game development assets:

            {assets_json_str}

            For each asset, assign one or more categories from the following list:
            {categories}

            Respond in this format:
            [
                {{
                    "title": "string",
                    "description": "string",
                    "storeLink": "string",
                    "categories": ["category1", "category2"]
                }},
                ...
            ]
            """
                            }
                        ]
                    )
        
        return response.choices[0].message.content
    
    async def run(self, context: ProjectContext):
        # Step 1: Fetch assets
        raw_assets = await self.fetch_assets(context)

        # Step 2: Categorize assets
        categorized_assets = await self.categorize_assets(raw_assets)

        # Optional: parse JSON if you want to return as Python data
        return categorized_assets