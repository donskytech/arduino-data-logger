from . import api_bp
from flask import  jsonify, request
import datetime
from app.extensions import mongo
from flask import current_app

@api_bp.post('/sensors')
def add_sensor_reads():
    sensor_readings = request.get_json()

    sensor_id = sensor_readings['sensor_id']
    temperature_in_c = sensor_readings['temperature_in_c']
    temperature_in_f = sensor_readings['temperature_in_f']
    humidity = sensor_readings['humidity']
    heat_index_in_c = sensor_readings['heat_index_in_c']
    heat_index_in_f = sensor_readings['heat_index_in_f']
    
    current_app.logger.info(f"sensor_readings : {sensor_readings}")
    
    sensor_readings = {"timestamp": datetime.datetime.now(), "metadata": {"sensor_id": sensor_id},\
        "temperature_in_c": temperature_in_c, "temperature_in_f": temperature_in_f,  "humidity": humidity,\
        "heat_index_in_c": heat_index_in_c, "heat_index_in_f": heat_index_in_f}
    
    mongo.db.sensor_readings.insert_one(sensor_readings)
    
    return jsonify({"Status": "OK", "Message": "Successfully saved sensor records!"})
