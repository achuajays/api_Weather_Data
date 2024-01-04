from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

model = pickle.load(open('p.pkl', 'rb'))

class I(BaseModel):
    n_1: float
    n_2: float
    n_3: float
    n_4: float
    n_5: float
    n_6: float

app = FastAPI()

# Use Path(__file__).parent to get the directory of the current script
csv_file_path = Path(__file__).parent / 'WeatherData.csv'
n = pd.read_csv(csv_file_path)

origins = [
    "http://localhost",  # Add the origin of your frontend application
    "http://localhost:8000",  # Add the URL where your HTML pages are served
    "file:///C:/Users/achu/Desktop/fastapi_python/api_Weather_Data/Weather_Data.html",
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/p')
async def p(i: I):
    p = pd.DataFrame([[i.n_1, i.n_2, i.n_3, i.n_4, i.n_5, i.n_6]],
                     columns=['Temp_C', 'Dew', 'Rel', 'Wind', 'Visibility_km', 'Press_kPa'])
    prediction = model.predict(p)
    l = n['Weather'].unique()
    print(prediction[0], '-', l[prediction[0]])
    return {'Weather': "{}".format(l[prediction[0]])}
