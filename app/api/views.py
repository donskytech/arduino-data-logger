from . import api_bp
from flask import  jsonify, request
import datetime
from app.extensions import mongo

@api_bp.post('/sensors')
def add_sensor_reads():
    sensor_readings = request.get_json()

    sensor_id = sensor_readings['sensor_id']
    temperature = sensor_readings['temperature']
    humidity = sensor_readings['humidity']
    
    mongo.db.sensor_readings.insert_one({"timestamp": datetime.datetime.now(), "metadata": {"sensor_id": sensor_id},\
        "temperature": temperature, "pressure": humidity, })
    
    return jsonify({"Status": "OK", "Message": "Successfully saved sensor records!"})
