
from flask import Flask, make_response, request
import dbhelpers as dh
import apihelper as a
import json
import dbcreds as d

app = Flask(__name__)

@app.post('/api/pokemon')
def add_pokemon():
    name = request.json.get('name')
    description = request.json.get('description')
    img_url = request.json.get('img_url')

    valid_check = a.check_endpoint_info(request.json, ['name', 'description', 'img_url'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)
    result = dh.run_statement('CALL add_pokemon(?,?,?)', [name, description, img_url])
    if (type(result) ==list):
        return make_response(json.dumps(result, default=str), 200)
      
    else:
        return make_response(json.dumps(result, default=str), 400)

@app.get('/api/pokemon')
def show_all_pokemon():
    result = dh.run_statement('CALL show_all_pokemon()')
    if (type(result) ==list):
        return make_response(json.dumps(result, default=str), 200)
      
    else:
        return make_response(json.dumps(result, default=str), 400)





if(d.production_mode == True):
    print("Running in Production Mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)

    #testing