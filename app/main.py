from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import joblib
import json

with open("data/mappings.json", "r") as f:
    feature_map = json.load(f)

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  # Live Server or browser local preview
    "http://localhost:5500",  # Just in case
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    age: int
    gender: str
    cgpa: float
    work_satisfaction: int
    work_pressure: int
    work_hours: float
    financial_stress: int
    diet: str
    suicidal_thoughts: str
    sleep: str
    mental_illness_family: str

def get_prediction(confidence):
    if confidence >= 0.9:
        return "You are most likely experiencing signs of depression. It's highly recommended to talk to a mental health professional."
    elif confidence >= 0.7:
        return "There’s a strong indication of depressive symptoms. Consider reaching out to someone you trust or a counselor."
    elif confidence >= 0.5:
        return "Some signs of depression are present. It might be good to reflect on your mental health and monitor your feelings."
    elif confidence >= 0.3:
        return "Mild signs detected. You're likely okay, but it's still important to prioritize your well-being."
    else:
        return "You seem to be doing well mentally. Keep maintaining healthy habits and stay connected with loved ones."

@app.post("/predict")
def predict(data: UserInput):

    gender = feature_map["gender"][data.gender]
    diet = feature_map["diet"][data.diet]
    suicidal = feature_map["suicidal_thoughts"][data.suicidal_thoughts]
    mental_history = feature_map["mental_illness_family"][data.mental_illness_family]
    sleep_encoded = feature_map["sleep"][data.sleep]  

    features = [
        data.age,
        data.work_pressure,
        data.cgpa,
        data.work_satisfaction,
        diet,
        suicidal,
        data.work_hours,
        data.financial_stress,
        mental_history,
    ] + sleep_encoded + [gender]

    X = np.array([features])


    model = joblib.load("models/model.pkl")
    confidence = model.predict_proba(X)[0][1]
    result = get_prediction(confidence)

    return {"prediction": result}
