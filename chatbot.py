import os
import sys
import numpy as np
import cv2
import tensorflow as tf
import warnings
from tkinter import Tk, Label, Button, filedialog, messagebox
from PIL import Image, ImageTk
warnings.filterwarnings("ignore")

# ------------ CONSTANTS -----------------
MODEL_PATH = "Best_Cattle_Breed.h5"   # your trained cattle breed model (saved by train.py)
# Use the actual dataset path present in the repository so class ordering matches training
DATA_DIR = "Dataset/Indian_bovine_breeds/"

# Three-tier confidence system:
HIGH_CONFIDENCE_THRESHOLD = 70.0   # Direct match: "Breed is X"
LOW_CONFIDENCE_THRESHOLD = 40.0    # Below this: "Breed not found"
# Between thresholds (40-70%): "Similar to X" - for breeds similar to dataset

# -------------------- LOAD MODEL --------------------------
model = None
try:
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
    else:
        raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found.")
except Exception as e:
    # don't crash — show helpful info and allow GUI to start for debugging
    print(f"Warning: could not load model: {e}")

if os.path.isdir(DATA_DIR):
    CLASS_NAMES = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
else:
    CLASS_NAMES = []

print(f"Detected {len(CLASS_NAMES)} classes: {CLASS_NAMES}")

# -------------------- IMAGE PREPROCESS --------------------
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or invalid path.")
    # OpenCV reads images in BGR order — convert to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = tf.keras.applications.efficientnet_v2.preprocess_input(img.astype(np.float32))
    # model.predict expects a batch dimension
    img = np.expand_dims(img, axis=0)
    return img

# ---------------- PREDICTION FUNCTION ------------------------
def predict_image(image_path):
    try:
        if model is None:
            messagebox.showerror("Error", f"Model not loaded. Place '{MODEL_PATH}' in project root or train the model first.")
            return None, None, None  # Return 3 values now
        img = preprocess_image(image_path)
        preds = model.predict(img)
        class_id = np.argmax(preds[0])
        confidence = float(preds[0][class_id] * 100)
        
        # Get breed name
        if class_id < len(CLASS_NAMES):
            breed_name = CLASS_NAMES[class_id]
        else:
            breed_name = f"class_{class_id}"
        
        # Three-tier confidence system
        if confidence >= HIGH_CONFIDENCE_THRESHOLD:
            # High confidence: Direct match
            return breed_name, confidence, "direct"
        elif confidence >= LOW_CONFIDENCE_THRESHOLD:
            # Medium confidence: Similar breed (not exact match but related)
            return breed_name, confidence, "similar"
        else:
            # Low confidence: Not a recognized breed
            return "❌ Breed Not Found", confidence, "not_found"
            
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None, None, None
    
# ------------------ GUI CALLBACKS ----------------------------
def browse_image():
    file_path = filedialog.askopenfilename(
        title=" Select Cattle Image",
        filetypes=[(" Image files", "*.jpg *.jpeg *.png")]
    ) 
    if file_path:
        image = Image.open(file_path)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo

        predicted_class, confidence, match_type = predict_image(file_path)
        if predicted_class:
            if match_type == "direct":
                # High confidence: Direct match
                result_label.config(
                    text=f"✅ Prediction: {predicted_class}\nConfidence: {confidence:.2f}%\n(Direct match)",
                    fg="green"
                )
            elif match_type == "similar":
                # Medium confidence: Similar breed
                result_label.config(
                    text=f"⚠️ Similar to: {predicted_class}\nConfidence: {confidence:.2f}%\n(Possible related breed - not exact match)",
                    fg="orange"
                )
            else:  # not_found
                # Low confidence: Not recognized
                result_label.config(
                    text=f"❌ Breed Not Found\nConfidence: {confidence:.2f}%\n(Not a recognized cattle breed)",
                    fg="red"
                )


# --------------------- GUI SETUP -----------------------
root = Tk()
root.title("Cattle Breed Classifier")
root.geometry("400x500")

Label(root, text="Indian Cattle Breed Classifier", font=("Arial", 16)).pack(pady=10)

image_label = Label(root)
image_label.pack(pady=10)

browse_btn = Button(root, text= "Select Cattle Image", command=browse_image)
browse_btn.pack(pady=20)

result_label = Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

root.mainloop()
