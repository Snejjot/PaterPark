from datetime import datetime

from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from Levenshtein import distance
import pandas as pd

from validators import normalize, PlateValidator

app = Flask(__name__)
app.debug = False
app.secret_key = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///peterpark.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
# not to move to import head
from models import Plate
db.init_app(app)
db.create_all()


@app.route('/plate', methods=['GET', 'POST'])
def plate():

    if request.method == 'GET':
        return jsonify([result.serialized for result in Plate.query.all()])

    if request.method == 'POST':
        # just for the case if form data will be received instead of json
        data = normalize(request)
        if not data:
            return Response("Request body is not JSON serializable", status=400)

        validator = PlateValidator(response=data)
        errors = validator.fields_check()
        if errors:
            return {"status": "error", "message": errors}, 400
        errors = validator.format_check()
        if errors:
            return {"status": "error", "message": errors}, 422

        plate_num = data.get("plate")
        _plate = Plate(plate_num)
        db.session.add(_plate)
        _plate.timestamp = datetime.utcnow()
        db.session.commit()
        return jsonify(data)


@app.route('/search-plate', methods=['GET'])
def search_plate():
    """by default empty filter will return all values"""
    if request.method == 'GET':
        df = pd.DataFrame([result.serialized for result in Plate.query.all()])
        if df.empty:
            return Response(status=200)
        df.plate = df.plate.str.replace("-", "")
        filter_value = request.args.get("key", False)
        levenshtein = request.args.get("levenshtein", False)
        if not levenshtein:
            levenshtein = 0
        if filter_value:
            filter = filter_value.replace("-", "")
            df["lev_distance"] = df.apply(lambda row: distance(row["plate"], filter), axis=1)
            df = df[df["lev_distance"] <= int(levenshtein)]
            df.drop(columns=["lev_distance"], inplace=True)

        return jsonify(df.to_dict(orient="records"))


if __name__ == '__main__':
    app.run()
