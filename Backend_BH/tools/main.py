# app.py
from flask import Flask, render_template, request, jsonify
from .agent5 import get_recommendations
from services.analyse import resume_recommandations
from flask_cors import CORS

import json

app = Flask(__name__)

CORS(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def handle_recommendation(ref_client=None):
    ref_client = request.form.get('ref_client')
    if not ref_client:
        return jsonify({"status": "error", "message": "Reference client manquante"})
    
    result = get_recommendations(ref_client)
    return jsonify(result)
#dashboard api
@app.route('/resume_recommendations', methods=['GET'])
def get_resume_recommendations():
    summary = resume_recommandations()
    return jsonify(summary)
#api client dashboard
@app.route('/resume_recommendations_client/<client_id>', methods=['GET'])

def get_resume_recommendations_client(client_id):
    from services.analyse import resume_recommandations_client
    client_id = str(client_id).strip() 
    summary = resume_recommandations_client(client_id)
    return jsonify(summary)

#new list recommendations
@app.route('/recommendations_list/<client_ref>', methods=['GET'])
def get_recommendations_list_route(client_ref):
    from tools.list_recommendation import get_recommendations_list

    try:
        recommendations = get_recommendations_list(client_ref)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})    

if __name__ == '__main__':
    app.run(debug=True)