"""
Flask API Backend for Cattle Breed Classification
Connects the trained model to the React frontend
"""
import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import warnings
warnings.filterwarnings("ignore")

try:
    from waitress import serve
    USE_WAITRESS = True
except ImportError:
    USE_WAITRESS = False

# ==================== CONFIGURATION ====================
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

# Constants
MODEL_PATH = "Best_Cattle_Breed.h5"
DATA_DIR = "Dataset/Indian_bovine_breeds/"
IMAGE_SIZE = (224, 224)

# Three-tier confidence thresholds (kept for reference but not used)
HIGH_CONFIDENCE_THRESHOLD = 70.0
LOW_CONFIDENCE_THRESHOLD = 40.0

# ==================== LOAD MODEL & CLASSES ====================
print("🔄 Loading model and class names...")

# Load trained model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model file '{MODEL_PATH}' not found. Please train the model first.")

model = tf.keras.models.load_model(MODEL_PATH)
print(f"✅ Model loaded successfully from {MODEL_PATH}")

# Load class names
if os.path.isdir(DATA_DIR):
    # Preferred: derive class names from dataset folders when available
    CLASS_NAMES = sorted([
        d for d in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, d))
    ])
    print(f"✅ Loaded {len(CLASS_NAMES)} cattle breeds from dataset directory")
else:
    # Fallback for deployments where the full Dataset folder is not present
    CLASS_NAMES = [
        "Alambadi",
        "Amritmahal",
        "Ayrshire",
        "Banni",
        "Bargur",
        "Bhadawari",
        "Brown_Swiss",
        "Dangi",
        "Deoni",
        "Gir",
        "Guernsey",
        "Hallikar",
        "Hariana",
        "Holstein_Friesian",
        "Jaffrabadi",
        "Jersey",
        "Kangayam",
        "Kankrej",
        "Kasargod",
        "Kenkatha",
        "Kherigarh",
        "Khillari",
        "Krishna_Valley",
        "Malnad_gidda",
        "Mehsana",
        "Murrah",
        "Nagori",
        "Nagpuri",
        "Nili_Ravi",
        "Nimari",
        "Ongole",
        "Pulikulam",
        "Rathi",
        "Red_Dane",
        "Red_Sindhi",
        "Sahiwal",
        "Surti",
        "Tharparkar",
        "Toda",
        "Umblachery",
        "Vechur",
    ]
    print(f"❌ Dataset directory '{DATA_DIR}' not found; using built-in list of {len(CLASS_NAMES)} cattle breeds")

# ==================== HELPER FUNCTIONS ====================

def preprocess_image(image_bytes):
    """
    Preprocess uploaded image for model prediction
    """
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to model input size
        img = img.resize(IMAGE_SIZE)
        
        # Convert to numpy array
        img_array = np.array(img, dtype=np.float32)
        
        # Preprocess for EfficientNetV2
        img_array = tf.keras.applications.efficientnet_v2.preprocess_input(img_array)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        raise ValueError(f"Error preprocessing image: {str(e)}")

# ==================== API ENDPOINTS ====================

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "num_classes": len(CLASS_NAMES),
        "model_path": MODEL_PATH
    })

@app.route('/breeds', methods=['GET'])
def get_breeds():
    """
    Get list of all supported cattle breeds
    """
    return jsonify({
        "breeds": CLASS_NAMES,
        "total": len(CLASS_NAMES)
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint
    Accepts image upload and returns breed prediction with three-tier confidence
    """
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({
                "error": "No image file provided",
                "message": "Please upload an image file"
            }), 400
        
        file = request.files['image']
        
        # Check if file is valid
        if file.filename == '':
            return jsonify({
                "error": "Empty filename",
                "message": "Please select a valid image"
            }), 400
        
        # Read image bytes
        image_bytes = file.read()
        
        # Preprocess image
        try:
            processed_image = preprocess_image(image_bytes)
        except ValueError as e:
            return jsonify({
                "error": "Invalid image",
                "message": str(e)
            }), 400
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        
        # Get top prediction
        class_id = np.argmax(predictions[0])
        confidence = float(predictions[0][class_id] * 100)
        
        # Get breed name
        breed_name = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else f"Unknown_Class_{class_id}"
        
        # Build simple response - just breed and confidence
        response = {
            "success": True,
            "breed": breed_name,
            "confidence": round(confidence, 2)
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "message": str(e)
        }), 500

@app.route('/config', methods=['GET'])
def get_config():
    """
    Get current confidence threshold configuration
    """
    return jsonify({
        "high_confidence_threshold": HIGH_CONFIDENCE_THRESHOLD,
        "low_confidence_threshold": LOW_CONFIDENCE_THRESHOLD,
        "image_size": IMAGE_SIZE,
        "model_path": MODEL_PATH
    })

# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🐄 Cattle Breed Classification API Server")
    print("="*60)
    print(f"✅ Model: {MODEL_PATH}")
    print(f"✅ Classes: {len(CLASS_NAMES)} cattle breeds")
    print(f"✅ High Confidence: ≥{HIGH_CONFIDENCE_THRESHOLD}%")
    print(f"✅ Low Confidence: <{LOW_CONFIDENCE_THRESHOLD}%")
    print("="*60)
    print("🚀 Server starting on http://localhost:5000")
    print("📡 Endpoints:")
    print("   - POST /predict    (Upload image for prediction)")
    print("   - GET  /health     (Health check)")
    print("   - GET  /breeds     (List all breeds)")
    print("   - GET  /config     (Get configuration)")
    print("="*60)
    print("\n💡 Frontend should connect to: http://localhost:5000")
    print("💡 Test with: curl -X POST -F 'image=@test.jpg' http://localhost:5000/predict")
    print("\n🔄 Starting Flask server...\n")
    
    # Determine port from environment (useful for platforms like Render)
    port = int(os.environ.get("PORT", "5000"))

    # Use waitress for more stable production serving
    if USE_WAITRESS:
        print("✅ Using Waitress WSGI server for stable hosting")
        serve(app, host='0.0.0.0', port=port, threads=4)
    else:
        print("⚠️ Using Flask development server")
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
