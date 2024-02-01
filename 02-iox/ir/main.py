from flask import Flask, render_template
import requests
import json

app = Flask(__name__)
rpi_address = "<address-of-your-raspberry-pi>"

def get_json(filename):
    with open(filename, 'r') as f: 
        return json.load(f)

def write_json(filename, data):
    with open(filename, 'w') as f: 
        json.dump(data, f)

def get_temperature():
    try:
        response = requests.get(f"http://{rpi_address}:5000/temperature", verify=False).text
        return int(response)
    except Exception as e:
        return 7

@app.route("/temperature")
def show_temperature():
    return str(get_temperature())

@app.route("/")
def hello_world():
    temp_data = get_json('temperatures.json')
    current_temp = get_temperature()
    new_temp_data = temp_data[1:] + [current_temp]
    write_json('temperatures.json', new_temp_data)
    return render_template('index.html', current_temperature=current_temp, temp_data=new_temp_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)