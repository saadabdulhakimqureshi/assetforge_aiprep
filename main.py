from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from together import Together
from models.request_model import ProjectContext
# from open_ai_services.ai_agent import generate_recommendations
from together_ai_services.asset_recommendation_agent import AssetRecommendationAgent
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=TOGETHER_API_KEY)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != TOGETHER_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Bearer token",
        )

app = FastAPI(title="AssetForge AI Backend")

@app.get("/")
def read_root(credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    return {"message": "AssetForge OpenAI is live"}
    
@app.post("/recommend")
async def recommend_assets(
        context: ProjectContext,
        credentials: HTTPAuthorizationCredentials = Depends(verify_token)
    ):
    try:
        agent = AssetRecommendationAgent(client=client)
        result = await agent.run(context)
        return {"recomendations": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))