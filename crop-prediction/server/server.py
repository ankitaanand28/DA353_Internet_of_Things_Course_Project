from __future__ import print_function
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn import tree
import pickle
import requests
import warnings

warnings.filterwarnings("ignore")
# from __future__ import print_function # In python 2.7
import sys
from json import *
from flask_cors import CORS, cross_origin
import random

app = Flask(__name__)
CORS(app)

crop_recommendation_model_path = "./XGBoost_2.pkl"  # "./XGBoost.pkl"
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, "rb"))

fertilizer_recommendation_model_path = (
    "./SVMClassifier_Fertilizer.pkl"  # "./xgb_pipeline.pkl"
)
fertilizer_recommendation_model = pickle.load(
    open(fertilizer_recommendation_model_path, "rb")
)


def generate_random_values():
    data_ranges = {"N": (0, 140), "P": (5, 145), "K": (5, 205), "fert": (0, 6)}

    random_values = []
    for key, (min_val, max_val) in data_ranges.items():
        random_values.append(int(random.uniform(min_val, max_val)))

    return random_values


@app.route("/crop", methods=["POST"])
def members1():

    try:
        N = int(request.json["N"])
        P = int(request.json["P"])
        K = int(request.json["K"])
        ph = float(request.json["Ph"])
        state = request.json["state"]
        district = request.json["district"]
        start_month = int(request.json["start_month"])
        end_month = int(request.json["end_month"])
    except:
        return jsonify({"crop": "failed to get info", "data": request.json})
    # return jsonify({"crop": 'printing request', "data": request.json})

    temprature = 20
    humidity = 30
    rainfall = 100

    x = requests.get(
        "https://api.mapbox.com/geocoding/v5/mapbox.places/"
        + district
        + " "
        + state
        + ".json?access_token=pk.eyJ1Ijoic2FpZ29ydGk4MSIsImEiOiJja3ZqY2M5cmYydXd2MnZwZ2VoZzl1ejNkIn0.CupGYvpb_LNtDgp7b-rZJg"
    )

    coordinates = x.json()["features"][0]["center"]

    y = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?lat="
        + str(coordinates[1])
        + "&lon="
        + str(coordinates[0])
        + "&appid=8d51fbf3b5ad7f3cc65ba0ea07220782"
    )

    humidity = y.json()["main"]["humidity"]
    temprature = y.json()["main"]["temp"]

    df = pd.read_csv("./data2.csv")
    # q = df.query('STATE_UT_NAME=="ANDAMAN And NICOBAR ISLANDS" and DISTRICT == "NICOBAR"', inplace = False)
    q = df.query(
        'STATE_UT_NAME == "{}" and DISTRICT == "{}"'.format(state, district),
        inplace=False,
    )

    total = 0
    # l=12

    if start_month <= end_month:
        l = (end_month - start_month) + 1

        for i in range(start_month, end_month + 1):
            try:
                total += int(q[i : i + 1].value)
            except:
                total -= 1

    elif start_month > end_month:
        l = (end_month + 12) - start_month + 1

        for i in range(start_month, 13):
            try:
                total += int(q[i : i + 1].value)
            except:
                total -= 1

        for i in range(1, end_month + 1):
            try:
                total += int(q[i : i + 1].value)
            except:
                total -= 1

    # for i in range(x, y+1):
    #     k = i
    #     if k>12:
    #         k=k-12
    #     total+=int(q[k:k+1].value)
    # for i in range(len(q)):
    #     total+=int(q[i:i+1].value)

    # l=12
    avg_rainfall = total / l
    random_sample = generate_random_values()
    data = np.array(
        [
            [
                N + random_sample[0],
                P + random_sample[1],
                K + random_sample[2],
                temprature,
                humidity,
                ph,
                avg_rainfall,
            ]
        ]
    )
    my_prediction = crop_recommendation_model.predict(data)
    # print(my_prediction)
    final_prediction = int(my_prediction[-1])
    crop_name_dict = {
        20: "rice",
        16: "maize",
        4: "chickpea",
        11: "kidneybeans",
        17: "pigeonpeas",
        12: "mothbeans",
        13: "mungbean",
        3: "blackgram",
        9: "lentil",
        18: "pomegranate",
        2: "banana",
        8: "mango",
        7: "grapes",
        21: "watermelon",
        15: "muskmelon",
        1: "apple",
        19: "orange",
        14: "papaya",
        5: "coconut",
        6: "cotton",
        10: "jute",
        0: "coffee",
    }
    pred_crop_name = crop_name_dict[final_prediction]
    return jsonify({"crop": pred_crop_name, "data": y.json()["main"], "l": l})


@app.route("/fertilizer", methods=["POST"])
def members2():

    try:
        N = int(request.json["N"])
        P = int(request.json["P"])
        K = int(request.json["K"])
        # ph = float(request.json['Ph'])
        state = request.json["state"]
        district = request.json["district"]
        moisture = float(request.json["moisture"])
        soil_type = request.json["soil_type"]
        crop_type = request.json["crop_type"]
        start_month = int(request.json["start_month"])
        end_month = int(request.json["end_month"])
    except:
        return jsonify({"crop": "failed to get info2", "data": request.json})

    temprature = 20
    humidity = 30
    rainfall = 100

    x = requests.get(
        "https://api.mapbox.com/geocoding/v5/mapbox.places/"
        + district
        + " "
        + state
        + ".json?access_token=pk.eyJ1Ijoic2FpZ29ydGk4MSIsImEiOiJja3ZqY2M5cmYydXd2MnZwZ2VoZzl1ejNkIn0.CupGYvpb_LNtDgp7b-rZJg"
    )

    coordinates = x.json()["features"][0]["center"]

    y = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?lat="
        + str(coordinates[1])
        + "&lon="
        + str(coordinates[0])
        + "&appid=8d51fbf3b5ad7f3cc65ba0ea07220782"
    )

    humidity = y.json()["main"]["humidity"]
    temprature = y.json()["main"]["temp"]

    df = pd.read_csv("./data2.csv")
    q = df.query(
        'STATE_UT_NAME=="ANDAMAN And NICOBAR ISLANDS" and DISTRICT == "NICOBAR"',
        inplace=False,
    )
    # q = df.query('STATE_UT_NAME == "{}" and DISTRICT == "{}"'.format(state, district), inplace = False)

    # total=0
    # for i in range(len(q)):
    #     total+=int(q[i:i+1].value)
    # avg_rainfall = total/len(q)

    total = 0
    # l=12

    if start_month <= end_month:
        l = (end_month - start_month) + 1

        for i in range(start_month, end_month + 1):
            try:
                total += int(q[i : i + 1].value)
            except:
                total -= 1

    elif start_month > end_month:
        l = (end_month + 12) - start_month + 1

        for i in range(start_month, 13):
            try:
                total += int(q[i : i + 1].value)
            except:
                total -= 1

        for i in range(1, end_month + 1):
            try:
                total += int(q[i : i + 1].value)
            except:
                total -= 1

    # for i in range(x, y+1):
    #     k = i
    #     if k>12:
    #         k=k-12
    #     total+=int(q[k:k+1].value)
    # for i in range(len(q)):
    #     total+=int(q[i:i+1].value)

    # l=12
    avg_rainfall = total / l
    crop2_dict = {
        "Maize": 3,
        "Sugarcane": 8,
        "Cotton": 1,
        "Tobacco": 9,
        "Paddy": 6,
        "Barley": 0,
        "Wheat": 10,
        "Millets": 4,
        "Oil seeds": 5,
        "Pulses": 7,
        "Ground Nuts": 2,
    }
    soil_type_dict = {"Sandy": 4, "Loamy": 2, "Black": 0, "Red": 3, "Clayey": 1}

    data = np.array([[avg_rainfall, humidity, moisture, soil_type, crop_type, N, K, P]])

    # data = np.array([[26, 52, 38, 4, 3,	37,	0, 0 ]])

    my_prediction = fertilizer_recommendation_model.predict(data)
    random_sample = generate_random_values()
    final_prediction = max(my_prediction[-1] - random_sample[3], 0)
    # final_prediction = 'dummie'

    fertname = {
        "0": "Diammonium Phosphate",
        "1": "Muriate of Potash (MOP)",
        "2": "Single Superphosphate (SSP) ",
        "3": "NPK",
        "4": "Zinc Sulphate",
        "5": "DAP",
        "6": "Urea",
    }

    # return jsonify({"crop": fertname[final_prediction], "data": data.tolist()})
    return jsonify({"crop": str(fertname[str(final_prediction)]), "data": fertname})


if __name__ == "__main__":
    app.run(debug=True)
