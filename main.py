from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import requests
import os,dotenv
import pickle


class Deliveryrequest(BaseModel):
    start_lon:float
    start_lat:float
    end_lon:float
    end_lat:float
    cargo_type:str

app=FastAPI()
dotenv.load_dotenv()

try:
    with open("risk_model.pkl","rb") as f:
        risk=pickle.load(f)
        print("model loaded successfully!")
except:
    print("model not found...")
    risk=None

cargo={"ice cream":0,"milk":1,"vaccines":2,"electronics":3}

@app.get('/get-route')

def get_route(start_long :float,start_lat:float,end_long:float,end_lat:float):
    ors_api_key=os.getenv("ORS_API_KEY") 
    url="https://api.openrouteservice.org/v2/directions/driving-car"
    headers={"Authorization":ors_api_key}
    params={"start":f"{start_long},{start_lat}","end":f"{end_long},{end_lat}"}
    response=requests.get(url,headers=headers,params=params)
    route_data=response.json()
    return route_data 


@app.get('/get-weather')
def get_weather(lat:float,lon:float):
    weather_api=os.getenv("OWM_API_KEY")
    weather_url="https://api.openweathermap.org/data/2.5/weather"
    params={
        "lat":lat,
        "lon":lon,
        "appid":weather_api,
        "units":"metric"
        }
    response=requests.get(weather_url,params=params) 
    dat=response.json() 
    return dat 


@app.post("/analyse-route")
def analyse_route(order:Deliveryrequest):
    start_lat=order.start_lat
    start_lon=order.start_lon
    end_lat=order.end_lat
    end_lon=order.end_lon
    cargo_type=order.cargo_type
    
    ors_api_key=os.getenv("ORS_API_KEY")
    owm_api_key=os.getenv("OWM_API_KEY")
    url="https://api.openrouteservice.org/v2/directions/driving-car"
    headers={"Authorization":ors_api_key}
    params={"start":f"{start_lon},{start_lat}","end":f"{end_lon},{end_lat}"}
    response=requests.get(url,headers=headers,params=params) 
    route_data=response.json()

    path_point=route_data['features'][0]['geometry']['coordinates']
    

    checkpoint=[
        path_point[0],
        path_point[len(path_point)//2],
        path_point[-1]
    ]

    weather_rep=[]
    for point in checkpoint:
        lon,lat=point

        params={
        "lat":lat,
        "lon":lon,
        "appid":owm_api_key,
        "units":"metric"
        }

        response=requests.get("https://api.openweathermap.org/data/2.5/weather",params=params) 
        weather_dat=response.json()

        temp=weather_dat['main']['temp']
        humidity=weather_dat['main']['humidity']

        cargo_id=cargo.get(cargo_type,-1)

        risk_stat='UNKNOWN'
        warn='cargo not supported'

        if risk and cargo_id!=-1:
            input_data = pd.DataFrame([{
                'cargo_type': cargo_id,
                'temperature': temp,
                'humidity': humidity,
                'time_hours': 2.0  # We assume 2 hours travel between points
            }])
            
            prediction = risk.predict(input_data)[0]
            
            if prediction==1:
                risk_stat = "DANGER"
                warn=f"High spoilage risk detected at {temp}°C, {humidity}% Humidity"
            else:
                risk_stat="SAFE"
                warn="Conditions are optimal."

        report={
            "lat":lat,
            "lon":lon,
            "temp":temp,
            "risk status":risk_stat,
            "warning":warn
        }
        weather_rep.append(report)
    
    return {
        "route_summary": route_data['features'][0]['properties']['summary'],
        "weather_checkpoints": weather_rep
    }

