from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Tuple
from pathlib import Path
from datetime import datetime
import json


app = FastAPI(title="Arusha Smart City Data Link API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_data() -> Dict[str, Any]:
  root = Path(__file__).resolve().parents[1]
  data_path = root / "arusha_data.json"
  with data_path.open("r", encoding="utf-8") as f:
      return json.load(f)


ARUSHA_DATA = load_data()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    reasoning_steps: List[str]
    timestamp: datetime


def analyze_population_hotspots(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    hotspots: List[Dict[str, Any]] = []
    for p in data["population_stats"]:
        if p["density_per_km2"] >= 1000 or p["annual_growth_rate"] >= 0.035:
            hotspots.append(p)
    return hotspots


def reasoning_loop(question: str, data: Dict[str, Any]) -> Tuple[str, List[str]]:
    steps: List[str] = []
    q = question.lower()

    steps.append("Hatua 1: Kutafsiri swali na kubaini mada.")
    topic = "general"
    if "idadi ya watu" in q or "ongezeko" in q or "population" in q:
        topic = "population"
    elif "hali ya hewa" in q or "mvua" in q or "weather" in q:
        topic = "weather"
    elif "afya" in q or "hospital" in q or "vituo vya afya" in q:
        topic = "health"
    elif "shule" in q or "elimu" in q:
        topic = "education"

    steps.append(f"Hatua 2: Mada iliyotambuliwa ni: {topic}.")

    if topic == "population":
        steps.append("Hatua 3: Kufilisha kata zenye msongamano na ukuaji mkubwa.")
        hotspots = analyze_population_hotspots(data)
        if not hotspots:
            answer = (
                "Kwa sasa hakuna kata zinazovuka viwango vya juu vya msongamano "
                "kulingana na takwimu zilizopo."
            )
        else:
            lines: List[str] = []
            for p in hotspots:
                lines.append(
                    f"- {p['ward']} (wilaya {p['district_code']}): "
                    f"watu {p['population']}, msongamano {p['density_per_km2']} kwa km², "
                    f"ukuaji {p['annual_growth_rate'] * 100:.1f}% kwa mwaka. "
                    "Inapendekezwa kuongeza vituo vya afya na shule katika kata hii ili "
                    "kidhi mahitaji."
                )
            answer = "Kata zifuatazo zina ongezeko kubwa la watu:\n" + "\n".join(lines)
        steps.append("Hatua 4: Kutoa mapendekezo mahususi ya miundombinu.")
    else:
        answer = (
            "Mfumo huu unaweza kujibu maswali kuhusu idadi ya watu, afya, elimu "
            "na hali ya hewa katika Arusha. Jaribu kuuliza kuhusu 'ongezeko la watu' "
            "au 'hali ya hewa' kwenye kata fulani."
        )
        steps.append("Hatua 3: Kutoa muhtasari wa uwezo wa mfumo.")

    steps.append("Hatua 5: Kurekodi hoja kwa ajili ya uwajibikaji wa AI.")
    return answer, steps


@app.get("/api/overview")
def get_overview():
    total_pop = sum(p["population"] for p in ARUSHA_DATA["population_stats"])
    return {
        "region": ARUSHA_DATA["meta"]["region"],
        "total_population": total_pop,
        "districts": ARUSHA_DATA["districts"],
    }


@app.get("/api/data")
def get_full_data():
    return ARUSHA_DATA


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer, steps = reasoning_loop(req.question, ARUSHA_DATA)
    return ChatResponse(answer=answer, reasoning_steps=steps, timestamp=datetime.utcnow())

