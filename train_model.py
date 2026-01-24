import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

cargo={
    0:"ice cream",
    1:"milk",
    2:"vaccines",
    3:"electronics"
}

data=[]

for _ in range(500):

    #For Ice Cream

    if np.random.random()>0.2:
        ic_temp=np.random.uniform(-25,-18)
    else:
        ic_temp=np.random.uniform(-10,-5)

    data.append({
        "cargo_type": 0, 
        "temperature": ic_temp,
        "humidity": np.random.uniform(20, 40), 
        "time_hours": np.random.uniform(1, 10),
        "is_spoiled": 1 if ic_temp > -18 else 0
    })

    #For Milk

    if np.random.random()>0.2:
        milk_temp=np.random.uniform(0,4)
    else:
        milk_temp=np.random.uniform(5,12)

    data.append({
        "cargo_type": 1, 
        "temperature": milk_temp,
        "humidity": np.random.uniform(40, 80), 
        "time_hours": np.random.uniform(1,5),
        "is_spoiled": 1 if milk_temp > 4 else 0 
    })

    #For Vaccines

    if np.random.random()>0.2:
        vac_temp=np.random.uniform(2,8)
    else:
        vac_temp=np.random.uniform(9,15)

    data.append({
        "cargo_type": 2, 
        "temperature": vac_temp,
        "humidity": np.random.uniform(30,50), 
        "time_hours": np.random.uniform(1,24),
        "is_spoiled": 1 if vac_temp < 2 or vac_temp > 8 else 0 
    })

    #for electronics

    if np.random.random() > 0.2:
        elec_temp = np.random.uniform(-10, 40)
    else:
        if np.random.random() > 0.3:
            elec_temp = np.random.uniform(41, 65)  #overheating
        else:
            elec_temp = np.random.uniform(-30, -11) #Extreme cold

    data.append({
        "cargo_type": 3, 
        "temperature": elec_temp,
        "humidity": np.random.uniform(20, 60), 
        "time_hours": np.random.uniform(5, 72),
        "is_spoiled": 1 if (elec_temp < -10 or elec_temp > 40) else 0
    })

df=pd.DataFrame(data)

x=df[['cargo_type','temperature','humidity','time_hours']]
y=df['is_spoiled']

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)

model=RandomForestClassifier(n_estimators=50)
model.fit(x_train,y_train)

print(f"model accuracy: {model.score(x_test,y_test)*100 }%")


with open('risk_model.pkl', 'wb') as f:
    pickle.dump(model, f)




    