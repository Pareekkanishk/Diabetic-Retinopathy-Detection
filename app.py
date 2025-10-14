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


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            processed_img = preprocess_image(filepath, TARGET_SIZE)
            predictions = model.predict(processed_img, verbose=0)
            predicted_class = int(np.argmax(predictions[0]))
            confidence = float(predictions[0][predicted_class]) * 100
            
            all_predictions = {
                CLASS_NAMES[i]: float(predictions[0][i]) * 100 
                for i in range(len(CLASS_NAMES))
            }
            
            class_recommendations = RECOMMENDATIONS[str(predicted_class)]
            
            return jsonify({
                'success': True,
                'prediction': CLASS_NAMES[predicted_class],
                'confidence': round(confidence, 2),
                'all_predictions': all_predictions,
                'recommendations': class_recommendations['recommendations'],
                'severity': class_recommendations['severity'],
                'image_path': f'/static/uploads/{filename}'
            })
        
        except Exception as e:
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file format'}), 400



if __name__ == '__main__':
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    app.run(debug=True)