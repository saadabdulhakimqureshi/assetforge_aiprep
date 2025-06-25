from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from models.request_model import ProjectContext
from services.ai_agent import generate_recommendations
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme != "Bearer" or credentials.credentials != OPENAI_API_KEY:
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
        result = await generate_recommendations(context)
        return {"recomendations": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))