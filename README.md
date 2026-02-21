# 🐄🔍 Cattle Breed Classification System 🚀 | Computer Vision + Deep Learning Project

🚀 I built a Cattle Breed Classifier using Python, TensorFlow & Deep Learning. Identify breeds like Alambadi, Amritmahal, Ayrshire, Banni, and more directly from cattle images with AI + GUI. 🐄🤖

💡 Ever wondered if Artificial Intelligence can help farmers, researchers, and veterinarians identify cattle breeds faster?
I’ll show you how I built a Cattle Breed Classifier using Python, TensorFlow, and Deep Learning — a complete end-to-end AI project for agriculture & livestock management. 🐮📊

We’ll go step by step:
✅ Loading and preprocessing cattle images
✅ Training a Deep Learning model with EfficientNetV2B0
✅ Building a classifier for multiple cattle breeds 🐄
✅ Creating a GUI with Tkinter for easy image upload & prediction
✅ Displaying results with breed name & confidence percentage 🎯

This is a full End-to-End Machine Learning Project — perfect for farmers. 🌱

This Project contains steps like:
• Prepare and organize a cattle image dataset
• Train & test a Deep Learning breed classifier
• Build a user-friendly GUI for predictions
• Apply AI in agriculture & livestock research
• Implement confidence thresholds to reject non-cattle or unknown breeds

## 🌐 Live Demo

- Frontend (Render): https://cattle-breed-prediction-model-frontend.onrender.com

## 🚀 Features

✅ **41 Indian Cattle Breeds** - Trained on diverse cattle breeds including Gir, Sahiwal, Red Sindhi, and more  
✅ **Transfer Learning** - Uses EfficientNetV2B0 pretrained on ImageNet for better accuracy  
✅ **Three-Tier Detection System**:
   - **Direct Match (≥70%)**: Exact breed from dataset
   - **Similar Breed (40-70%)**: Related/similar breeds not in exact dataset
   - **Not Found (<40%)**: Rejects non-cattle or unrelated images  
✅ **GUI Interface** - Easy-to-use Tkinter GUI with color-coded results  
✅ **CLI Tool** - Command-line prediction script for batch processing  
✅ **Comprehensive Metrics** - Classification report, confusion matrix, and accuracy metrics  

## 📋 Requirements

```bash

## 🎯 Quick Start

### Prerequisites
- **Python 3.11** (recommended for TensorFlow 2.20.0 compatibility)
- **Node.js v22+** and npm
- Trained model file `Best_Cattle_Breed.h5` (generated from `train.py`)

### 🚀 Run Locally (Easy Method)

**Option 1: One-Click Startup (Recommended)**
```powershell
.\start_all.ps1
```
This automated script will:
- Start the backend API server (Flask on http://127.0.0.1:5000)
- Wait for backend health check
- Start the frontend dev server (Vite on http://localhost:8080)
- Open both in separate PowerShell windows

**Option 2: Manual Setup**

1️⃣ **Create Python Virtual Environment:**
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

2️⃣ **Install Backend Dependencies:**
```powershell
pip install -r requirements.txt
```

3️⃣ **Start Backend API:**
```powershell
.\start_backend.ps1
# Or manually: python api.py
```
Backend will be available at: http://127.0.0.1:5000

4️⃣ **Start Frontend (New Terminal):**
```powershell
.\start_frontend.ps1
# Or manually: 
# cd Cattles-Breed-Detection-Frontend\Frontend
# npm install
# npm run dev
```
Frontend will be available at: http://localhost:8080

### 🧪 Test the System

**Health Check:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/health"
```

**Get Supported Breeds:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/breeds"
```

**Predict from Image:**
```powershell
$response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/predict" `
  -Method POST -Form @{ image = Get-Item "path\to\cattle.jpg" }
$response.Content | ConvertFrom-Json
```

### 🎨 Desktop GUI (Alternative)
```bash
python chatbot.py
- See results with color coding:
  - **Green** (≥70%): Direct breed match ✅
  - **Orange** (40-70%): Similar/related breed ⚠️
  - **Red** (<40%): Breed not found ❌

### 🔧 CLI Prediction
```bash
python predict.py path/to/cattle_image.jpg
```

### 📝 Training Your Own Model
```bash
python train.py
```
This will train the model for 10 epochs and save the best model as `Best_Cattle_Breed.h5`.

---

## ⚙️ Helper Scripts

The repository includes PowerShell automation scripts for Windows:

| Script | Purpose |
|--------|---------|
| `start_all.ps1` | **One-click launcher** - Starts both backend and frontend with health check |
| `start_backend.ps1` | Activates venv and starts Flask API server |
| `start_frontend.ps1` | Installs dependencies and starts Vite dev server |

### Troubleshooting Tips

🔸 **TensorFlow Installation Issues:**
- Use Python 3.11 or 3.10 (TensorFlow 2.20.0 compatibility)
- Recreate the virtual environment if pip fails on TensorFlow wheels

🔸 **Backend Not Starting:**
- Ensure `Best_Cattle_Breed.h5` model file exists in the root directory
- Check if port 5000 is already in use: `netstat -ano | findstr :5000`
- Verify virtual environment is activated: `.\.venv\Scripts\Activate.ps1`

🔸 **Frontend Connection Issues:**
- Backend must be running before starting frontend
- Check CORS is enabled in `api.py` (already configured)
- Verify backend URL in frontend code points to `http://127.0.0.1:5000`

🔸 **Production Deployment:**
- Use WSGI server (Gunicorn/Waitress) instead of Flask dev server
- Set proper environment variables for production
- Serve frontend with nginx or similar web server

---

## 📊 Model Performance

- **Architecture**: EfficientNetV2B0 (Transfer Learning)
- **Input Size**: 224x224 RGB
- **Training**: 10 epochs with early stopping
- **Validation Split**: 80/20
- **Data Augmentation**: Random flip, rotation, zoom
- **Confidence Threshold**: 50% (adjustable)

## 🎨 Dataset Structure

```
Dataset/Indian_bovine_breeds/
├── Alambadi/
├── Amritmahal/
├── Gir/
├── Sahiwal/
└── ... (41 breeds total)
```

## 🔧 Adjusting Confidence Thresholds

The system uses two thresholds to categorize predictions:

**Edit in `chatbot.py` or `predict.py`:**

```python
HIGH_CONFIDENCE_THRESHOLD = 70.0   # Direct match (exact breed)
LOW_CONFIDENCE_THRESHOLD = 40.0    # Below this = not found
# Between 40-70% = Similar/related breed
```

**Examples:**
- **Strict Mode** (80% / 60%): Only very confident predictions, narrow similarity range
- **Balanced Mode** (70% / 40%): Default - good for detecting related breeds ✅
- **Lenient Mode** (60% / 30%): Accepts more similar breeds, wider detection range

---

## � Technologies Used

### Backend Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **TensorFlow** | 2.20.0 | Deep learning framework |
| **Keras** | (included in TF) | High-level neural networks API |
| **Flask** | 3.0.0 | Web framework for REST API |
| **Flask-CORS** | 4.0.0 | Cross-origin resource sharing |
| **NumPy** | 2.2.6 | Numerical computing |
| **OpenCV** | 4.12.0.88 | Computer vision & image processing |
| **Pillow** | 12.0.0 | Image manipulation |
| **Scikit-learn** | 1.7.2 | Machine learning utilities |
| **Matplotlib** | 3.10.7 | Data visualization & plotting |
| **h5py** | 3.15.1 | HDF5 model file format |
| **Tkinter** | (built-in) | Desktop GUI application |
| **Gunicorn/Waitress** | 21.2.0 | Production WSGI server |

### Frontend Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.3.1 | JavaScript library for UI |
| **TypeScript** | 5.8.3 | Type-safe JavaScript |
| **Vite** | 5.4.19 | Fast build tool & dev server |
| **Tailwind CSS** | 3.4.17 | Utility-first CSS framework |
| **Radix UI** | Latest | Accessible UI primitives |
| **shadcn/ui** | Latest | Re-usable component system |
| **TanStack Query** | 5.83.0 | Data fetching & caching |
| **React Hook Form** | 7.61.1 | Form state management |
| **Zod** | 3.25.76 | Schema validation |
| **Lucide React** | 0.462.0 | Icon library |
| **Recharts** | 2.15.4 | Charting library |
| **React Router DOM** | 6.30.1 | Client-side routing |

### Machine Learning
- **CNN Architecture**: Convolutional Neural Networks
- **Transfer Learning**: MobileNetV2 / EfficientNetV2B0
- **Pre-trained on**: ImageNet dataset
- **Image Processing**: 224×224 RGB normalization
- **Data Augmentation**: Flip, rotation, zoom, brightness

### Development Tools
- **Node.js & npm**: Frontend package management
- **Git**: Version control
- **PowerShell**: Automation scripts
- **ESLint**: Code linting
- **PostCSS**: CSS processing


#   B r e e d _ R e c o g n i z a t i o n  
 