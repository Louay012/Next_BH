# app.py
from flask import Flask, render_template, request, jsonify
from .agent5 import get_recommendations

import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def handle_recommendation():
    ref_client = request.form.get('ref_client')
    if not ref_client:
        return jsonify({"status": "error", "message": "Reference client manquante"})
    
    result = get_recommendations()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)