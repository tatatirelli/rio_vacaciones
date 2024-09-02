import pandas as pd
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI

from src.model.model_predictor import RioVacationPredictor

app = FastAPI()
class Item(BaseModel):
    latitude: float
    longitude: float
    bathrooms: float
    price: float

class Items(BaseModel):
    items: List[Item]

predictor = RioVacationPredictor('artifacts/models/rio_vac_scale_n_predict.pkl')

@app.post("/predict/")
async def predict(items_object: Items):
    input_df = pd.DataFrame([item.model_dump() for item in items_object.items])
    output_df = predictor.predict(input_df)
    return output_df.to_dict(orient='records')
