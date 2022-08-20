from urllib import response
from flask import Flask,jsonify
import json

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

def get_json():
    with open('./output_files/data.json') as f:
        data = json.load(f)
        return data

def get_key(value,dic):

    for key in dic.keys():
        if(value in key):
            return key

    raise KeyError
  
@app.route('/')
def all():
    response = get_json()
    return jsonify(response)

@app.route('/<string:day>/')
def get_day(day):
    days = ('seg','ter','qua','qui','sex','sab','dom')
    response = get_json()
    
    if(day in days):
        return response[get_key(day,response)]
    else:
        return jsonify({'erro':'nao encontrado'})

app.run(debug=True)
