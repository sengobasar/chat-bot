import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

# Allow CORS so frontends served from other local ports (e.g., 5500) can call the API.
# For development you can allow all origins. In production, restrict this to your frontend origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Chat(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: Chat):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # <- update this to a supported model from your Groq console
            messages=[{"role": "user", "content": req.message}],
            max_tokens=300,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        return {"reply": reply}
    except Exception as e:
        # return helpful debugging info (do not leak keys in production)
        return {"error": str(e)}
