import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import json
from werkzeug.utils import secure_filename
from pathlib import Path
from utils.preprocessing import preprocess_image, allowed_file


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

print("Loading InceptionV3 model...")
model = tf.keras.models.load_model('models/inceptionv3.keras')
print("Model loaded successfully!")


with open('recommendations.json', 'r') as f:
    RECOMMENDATIONS = json.load(f)

CLASS_NAMES = ['No DR', 'Mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR']
TARGET_SIZE = (299, 299)  # inceptionV3 input size


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze')
def analyze():
    return render_template('analyze.html')


if __name__ == '__main__':
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    app.run(debug=True)