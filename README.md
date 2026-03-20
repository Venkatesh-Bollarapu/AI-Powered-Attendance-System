# AI-Powered-Attendance-System
An intelligent **real-time attendance system** that uses **Face Recognition + Computer Vision + Backend API** to automatically detect, track, and store attendance data.

---

## 🚀 Features

* 🎥 Real-time face detection using MediaPipe
* 🧠 Face recognition using `face_recognition`
* ⏱️ Tracks how long each person is present
* ✅ Automatically marks **Present / Absent**
* 📡 Sends data to backend API (Node.js)
* 🗄️ Stores attendance in MongoDB
* 📊 Displays attendance summary

---

## 🧠 System Architecture

```
[ Webcam ]
     ↓
[ Python AI Engine ]
     ↓ (JSON API)
[ Node.js Backend ]
     ↓
[ MongoDB Database ]
```

---

## 🛠️ Tech Stack

### 👁️ AI / Computer Vision

* Python
* OpenCV
* MediaPipe
* face_recognition
* NumPy

### 🌐 Backend

* Node.js
* Express.js
* MongoDB (Mongoose)

---

## 📂 Project Structure

```
AI-Attendance-Tracking-System/
│
├── backend/
│   ├── index.js
│   ├── package.json
│
├── ai_engine/
│   ├── main.py
│   ├── encodings.pickle
│   ├── requirements.txt
│
├── README.md
├── LICENSE
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/AI-Attendance-Tracking-System.git
cd AI-Attendance-Tracking-System
```

---

### 2️⃣ Setup Backend

```bash
cd backend
npm install
node index.js
```

✔ Server runs on: `http://localhost:5000`

---

### 3️⃣ Setup AI Engine

```bash
cd ai_engine
pip install -r requirements.txt
python main.py
```

---

## ▶️ How It Works

1. Webcam captures live video
2. Faces are detected using MediaPipe
3. Encodings are compared with known faces
4. Recognized individuals are tracked
5. Time spent is calculated
6. After 30 seconds:

   * > 20 sec → **Present**
   * else → **Absent**
7. Data is sent to backend API
8. Stored in MongoDB

---

## 📡 API Endpoint

```
POST /attendance
```

### Example Request

```json
[
  {
    "name": "John",
    "attended_time": 25.3,
    "status": "Present"
  }
]
```

---

## 💡 Real-World Use Cases

* 🏫 Schools & Colleges
* 🏢 Office attendance systems
* 🏭 Workforce monitoring
* 🧪 Labs & restricted areas

---

## 🚧 Future Improvements

* Web dashboard (React)
* Multi-camera support
* Cloud deployment
* Authentication system
* Improved accuracy with deep learning

---

## 👨‍💻 Author

**Venkatesh Bollarapu**

---

## ⭐ Support
If you like this project, give it a ⭐ on GitHub!.
