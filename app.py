from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
import requests
from pydantic import BaseModel

import xml.etree.ElementTree as ET

# Swagger 설정
app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    title="fastapi를 활용한 api 모음",
    description="설명적기",
    version="0.1.0",
    openapi_url="/openapi.json"
)

# 리액트 cors 설정
origins = {
    "*"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"hello": "world"}

class TrendResult(BaseModel):
    trends: list[str] = []

@app.get("/api/trends", response_model=TrendResult)
async def google_trends(region: str = Query("US", max_length=2)):
    url = f"https://trends.google.com/trends/trendingsearches/daily/rss?geo={region}"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    trends = []
    for item in root.iter("item"):
        title = item.find("title").text
        trends.append(title)
    return {"trends": trends}