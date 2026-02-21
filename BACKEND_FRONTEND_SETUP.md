# 🔗 Backend-Frontend Connection Guide

## ✅ What Was Created

### Backend API (`api.py`)
- ✅ Flask REST API server
- ✅ Loads your trained model (`Best_Cattle_Breed.h5`)
- ✅ Three-tier confidence system
- ✅ Image upload & prediction endpoint
- ✅ CORS enabled for frontend

### Updated Frontend
- ✅ Real API integration (replaced mock data)
- ✅ Three-tier result display (Green/Orange/Red)
- ✅ Top 3 predictions
- ✅ Color-coded confidence bars

---

## 🚀 How to Run

### Step 1: Install Backend Dependencies

```powershell
cd Cattle-Breed-Classification
pip install -r requirements-api.txt
```

**What this installs:**
- Flask (web framework)
- Flask-CORS (enables frontend connection)
- TensorFlow, Pillow, NumPy (already installed)

---

### Step 2: Start Backend Server

```powershell
cd Cattle-Breed-Classification
python api.py
```

**You should see:**
```
🐄 Cattle Breed Classification API Server
============================================================
✅ Model: Best_Cattle_Breed.h5
✅ Classes: 41 cattle breeds
✅ High Confidence: ≥70%
✅ Low Confidence: <40%
============================================================
🚀 Server starting on http://localhost:5000
```

**Keep this terminal running!**

---

### Step 3: Start Frontend (New Terminal)

Open a **new terminal** (keep backend running):

```powershell
cd Cattles-Breed-Detection-Frontend/Frontend
npm install
npm run dev
```

**You should see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

### Step 4: Test the Connection

1. **Open browser**: Go to `http://localhost:5173`
2. **Upload cattle image**: Drag & drop or click to browse
3. **See results**: Three-tier color-coded detection!

---

## 🎨 Three-Tier Detection Display

### ✅ Green - Direct Match (≥70% confidence)
```
✅ Direct Match
Breed: Gir
Confidence: 87.34%
Status: High confidence detection
```

### ⚠️ Orange - Similar Breed (40-70% confidence)
```
⚠️ Similar Breed
Breed: Similar to Sahiwal
Confidence: 55.23%
Status: Possible match - may be related breed
```

### ❌ Red - Not Found (<40% confidence)
```
❌ Not Found
Breed: Breed Not Found
Confidence: 23.45%
Status: Breed not found - confidence too low
```

---

## 📡 API Endpoints

### POST `/predict`
Upload image for breed detection

**Request:**
```bash
curl -X POST -F "image=@cattle.jpg" http://localhost:5000/predict
```

**Response:**
```json
{
  "success": true,
  "status": "success",
  "breed": "Gir",
  "confidence": 87.34,
  "category": "direct",
  "color": "green",
  "message": "High confidence detection: Gir",
  "top_predictions": [
    {"breed": "Gir", "confidence": 87.34},
    {"breed": "Kankrej", "confidence": 8.12},
    {"breed": "Sahiwal", "confidence": 2.45}
  ]
}
```

### GET `/health`
Check if API is running

### GET `/breeds`
Get list of all 41 cattle breeds

### GET `/config`
Get confidence threshold configuration

---

## 🔧 Troubleshooting

### ❌ Frontend shows "Failed to connect"
**Problem:** Backend not running
**Solution:**
```powershell
cd Cattle-Breed-Classification
python api.py
```

### ❌ CORS Error
**Problem:** Frontend and backend on different ports
**Solution:** Already fixed with `flask-cors` - just make sure both servers are running

### ❌ Model not found
**Problem:** `Best_Cattle_Breed.h5` doesn't exist
**Solution:**
```powershell
cd Cattle-Breed-Classification
python train.py
```

### ❌ Port 5000 already in use
**Solution:** Change port in `api.py` line 246:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Change to 5001
```
And update frontend `API_URL` in `Index.tsx`:
```typescript
const API_URL = "http://localhost:5001";
```

---

## 🎯 Testing Tips

### Test with Dataset Images
```powershell
# Upload images from your dataset
Dataset/Indian_bovine_breeds/Gir/*.jpg
Dataset/Indian_bovine_breeds/Sahiwal/*.jpg
```

### Test API Directly (Without Frontend)
```powershell
# Windows PowerShell
curl -X POST -F "image=@Dataset/Indian_bovine_breeds/Gir/image.jpg" http://localhost:5000/predict
```

### Check API Health
```powershell
curl http://localhost:5000/health
```

---

## 📊 Expected Behavior

| Upload | Confidence | Display | Border | Icon |
|--------|-----------|---------|--------|------|
| Pure Gir cattle | 87% | ✅ Gir | Green | ✓ |
| Crossbreed Sahiwal | 55% | ⚠️ Similar to Sahiwal | Orange | ⚠ |
| Dog/Non-cattle | 23% | ❌ Not Found | Red | ✗ |

---

## 🎉 You're Connected!

**Both servers running?**
- ✅ Backend: `http://localhost:5000` ← API
- ✅ Frontend: `http://localhost:5173` ← Web UI

**Upload a cattle image and see the three-tier detection in action!** 🐄✨

---

## ⚙️ Customization

### Change Confidence Thresholds
Edit `api.py` lines 19-20:
```python
HIGH_CONFIDENCE_THRESHOLD = 70.0   # Change to 80 for stricter
LOW_CONFIDENCE_THRESHOLD = 40.0    # Change to 30 for more lenient
```

Restart backend server after changes.

---

## 🚀 Next Steps

1. **Test with real cattle images**
2. **Try different breeds**
3. **See three-tier system in action**
4. **Share with others!**

**Enjoy your fully connected cattle breed detection system!** 🎊
