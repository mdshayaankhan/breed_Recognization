"""
Standalone prediction script for cattle breed classification.
Usage: python predict.py <image_path>
"""
import os
import sys
import numpy as np
import cv2
import tensorflow as tf
import warnings
warnings.filterwarnings("ignore")

# ------------ CONSTANTS -----------------
MODEL_PATH = "Best_Cattle_Breed.h5"
DATA_DIR = "Dataset/Indian_bovine_breeds/"

# Three-tier confidence system:
HIGH_CONFIDENCE_THRESHOLD = 70.0   # Direct match: "Breed is X"
LOW_CONFIDENCE_THRESHOLD = 40.0    # Below this: "Breed not found"
# Between thresholds (40-70%): "Similar to X" - for breeds similar to dataset

# -------------------- LOAD MODEL --------------------------
def load_model_and_classes():
    """Load trained model and class names"""
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Error: Model file '{MODEL_PATH}' not found.")
        print(f"Please train the model first using: python train.py")
        sys.exit(1)
    
    model = tf.keras.models.load_model(MODEL_PATH)
    
    if not os.path.isdir(DATA_DIR):
        print(f"❌ Error: Dataset directory '{DATA_DIR}' not found.")
        sys.exit(1)
    
    class_names = sorted([d for d in os.listdir(DATA_DIR) 
                         if os.path.isdir(os.path.join(DATA_DIR, d))])
    
    print(f"✅ Model loaded successfully")
    print(f"✅ Detected {len(class_names)} cattle breeds from dataset")
    return model, class_names

# -------------------- IMAGE PREPROCESS --------------------
def preprocess_image(image_path):
    """Preprocess image for model prediction"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")
    
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Unable to read image from '{image_path}'.")
    
    # Convert BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = tf.keras.applications.efficientnet_v2.preprocess_input(img.astype(np.float32))
    img = np.expand_dims(img, axis=0)
    return img

# ---------------- PREDICTION FUNCTION ------------------------
def predict_breed(model, class_names, image_path):
    """Predict cattle breed from image"""
    try:
        print(f"\n🔍 Analyzing image: {image_path}")
        img = preprocess_image(image_path)
        
        # Get prediction
        preds = model.predict(img, verbose=0)
        class_id = np.argmax(preds[0])
        confidence = float(preds[0][class_id] * 100)
        
        # Get breed name
        breed_name = class_names[class_id] if class_id < len(class_names) else f"Unknown_Class_{class_id}"
        
        print(f"\n{'='*60}")
        
        # Three-tier confidence system
        if confidence >= HIGH_CONFIDENCE_THRESHOLD:
            # High confidence: Direct match
            print(f"✅ BREED DETECTED: {breed_name}")
            print(f"   Confidence: {confidence:.2f}%")
            print(f"   Status: DIRECT MATCH (High confidence)")
            
        elif confidence >= LOW_CONFIDENCE_THRESHOLD:
            # Medium confidence: Similar breed (possibly related)
            print(f"⚠️  SIMILAR BREED: {breed_name}")
            print(f"   Confidence: {confidence:.2f}%")
            print(f"   Status: POSSIBLE MATCH")
            print(f"   Note: This may be a related breed or variant similar to {breed_name}")
            print(f"         from your dataset, but not an exact match.")
            
        else:
            # Low confidence: Not recognized
            print(f"❌ BREED NOT FOUND")
            print(f"   Confidence: {confidence:.2f}% (below threshold {LOW_CONFIDENCE_THRESHOLD}%)")
            print(f"   This image does not appear to be a recognized cattle breed")
            print(f"   from the training dataset.")
            print(f"   Closest match would be: {breed_name}")
            print(f"{'='*60}\n")
            return None
        
        # Show top 3 predictions
        top_3_idx = np.argsort(preds[0])[-3:][::-1]
        print(f"\n   Top 3 predictions:")
        for i, idx in enumerate(top_3_idx, 1):
            if idx < len(class_names):
                print(f"   {i}. {class_names[idx]}: {preds[0][idx]*100:.2f}%")
        
        print(f"{'='*60}\n")
        return breed_name, confidence
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return None

# -------------------- MAIN --------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python predict.py <image_path>")
        print("Example: python predict.py test_image.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Load model and classes
    model, class_names = load_model_and_classes()
    
    # Make prediction
    predict_breed(model, class_names, image_path)

if __name__ == "__main__":
    main()
