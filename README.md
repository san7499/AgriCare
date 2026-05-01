# 🌿 AgriCare - Plant Disease Detection System

AgriCare is an AI-powered web application that helps farmers and users detect plant diseases using image processing and machine learning. Users can upload an image of a plant leaf, and the system predicts the disease along with basic recommendations.

---

## 🚀 Features

* 🌱 Upload plant leaf images
* 🤖 AI-based disease prediction using TensorFlow/Keras
* 📊 Fast and accurate results
* 🌐 Web-based interface using Flask
* 🖼️ Image processing using OpenCV
* 📈 Visualization using Matplotlib

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Flask (Python)
* **Machine Learning:** TensorFlow, Keras
* **Libraries:** NumPy, OpenCV, Pillow, Matplotlib
* **Deployment:** Render / Railway
* **Database (Optional):** MongoDB Atlas

---

## 📂 Project Structure

```
AgriCare/
│── static/
│── templates/
│── model/
│   └── model.h5
│── app.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation (Local Setup)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/san7499/AgriCare.git
cd AgriCare
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # For Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python app.py
```

App will run on:

```
http://127.0.0.1:5000
```

---

## 🌐 Deployment Guide

### 🚀 Deploy on Render

1. Go to Render Dashboard
2. Click **New Web Service**
3. Connect your GitHub repository
4. Use the following settings:

**Build Command:**

```
pip install -r requirements.txt
```

**Start Command:**

```
gunicorn app:app
```

---

## 📦 Requirements

```
flask==3.0.3
gunicorn==22.0.0
tensorflow-cpu==2.15.0
numpy==1.26.4
pillow==10.3.0
opencv-python-headless==4.9.0.80
matplotlib==3.8.4
pymongo==4.7.2
python-dotenv==1.0.1
```

---

## ⚠️ Important Notes

* Use `opencv-python-headless` instead of `opencv-python` for deployment
* Ensure `model.h5` file is included in the project
* Disable debug mode in production:

```python
app.run(debug=False)
```

---

## 🧠 Future Improvements

* 🌍 Multilingual support
* 📱 Mobile app integration
* ☁️ Cloud model optimization
* 📊 Advanced analytics dashboard

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## 👨‍💻 Author

**Sanket Khapake**
Aspiring Data Scientist & Full Stack Developer

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

---
