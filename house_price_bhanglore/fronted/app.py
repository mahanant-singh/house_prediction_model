from flask import Flask, request, render_template
import pandas as pd
import pickle

app = Flask(__name__)


data = pd.read_csv("clean_data.csv")

locations = data["location"].unique()


model = pickle.load(open("hose_pred.pkl", "rb"))


@app.route("/")
def index():
    locations = data["location"].unique()

    return render_template(
        "index.html",
        locations=locations
    )


@app.route("/predict", methods=["POST"])
def makePrediction():

    location = request.form.get("location")
    sqft = float(request.form.get("sqft"))
    bathrooms = int(request.form.get("bath"))
    bhk = int(request.form.get("bhk"))

   
    input_data = pd.DataFrame(
        [[location, sqft, bathrooms, bhk]],
        columns=["location", "total_sqft", "bath", "bhk"]
    )

    print(input_data)

    # Prediction
    result = model.predict(input_data)
    finalresult=str(round(result[0],2))

    return str("predicte price of aboue"+finalresult)


if __name__ == "__main__":
    app.run(debug=True)