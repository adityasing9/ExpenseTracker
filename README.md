<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:6C63FF,100:00C6FF&height=200&section=header&text=Expense%20Tracker%20AI&fontSize=40&fontColor=ffffff&animation=fadeIn&fontAlignY=35" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Backend-Flask-blue?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/Data-Pandas-orange?style=for-the-badge&logo=pandas" />
  <img src="https://img.shields.io/badge/Visualization-Matplotlib-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI-Insights-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Deploy-Render-purple?style=for-the-badge&logo=render" />
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,flask,html,css,git,github" />
</p>

---

# 💰 Expense Tracker AI

A **smart full-stack finance application** built using Flask that helps users track expenses, analyze spending patterns, upload bank statements (PDF), and generate intelligent financial insights.

---

## 🌐 Live Demo

👉 https://expensetracker-sot6.onrender.com/

---

## ✨ Features

### 📊 Expense Management
- Add & delete expenses  
- Category-based tracking  
- User-wise data storage  

### 📂 PDF Bank Statement Upload
- Upload bank PDF  
- Auto-extract transactions  
- Auto-categorization (Food, Travel, Shopping, etc.)  
- Handles real-world noisy data  

### 📈 Data Analysis
- Total spending calculation  
- Category-wise breakdown  
- Monthly summaries  

### 📉 Visualization
- 📊 Bar chart (category spending)  
- 📈 Monthly trend graph  

### 💰 Budget Tracking
- Set monthly budget  
- Remaining balance calculation  
- Budget alerts  

### 🧠 Smart Insights
- Income vs Expense detection  
- Savings calculation  
- Overspending alerts  

### 🤖 Prediction
- Median-based prediction  
- Category-wise prediction  

---

## 🛠 Tech Stack

- Backend: Flask (Python)  
- Data Processing: Pandas  
- Visualization: Matplotlib  
- PDF Parsing: pdfplumber  
- Deployment: Render  

---

## 📂 Project Structure

expense-tracker/  
├── app.py  
├── requirements.txt  
├── Procfile  
├── data/  
├── templates/  
│   ├── login.html  
│   ├── register.html  
│   └── view.html  
└── static/  

---

## ⚙️ Local Setup

Clone repo:  
git clone https://github.com/adityasing9/expense-tracker.git  

cd expense-tracker  

Install:  
pip install -r requirements.txt  

Run:  
python app.py  

Open:  
http://127.0.0.1:5000/  

---

## 🚀 Deployment (Render)

Build Command:  
pip install -r requirements.txt  

Start Command:  
gunicorn app:app  

---

## ⚠️ Limitations

- Uses CSV instead of database  
- Render free tier → temporary storage  
- PDF parsing depends on bank format  

---

## 🚀 Future Improvements

- Add database (SQLite/PostgreSQL)  
- AI-based categorization  
- Mobile responsive UI  
- Export reports (PDF/Excel)  

---

## 🧠 Key Learnings

- Full-stack Flask development  
- Data cleaning & PDF parsing  
- Visualization using Matplotlib  
- Deployment on Render  

---

## 👨‍💻 Author

Aditya Singh  
https://github.com/adityasing9  

---

<p align="center">
  ⭐ If you like this project, give it a star!
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:6C63FF,100:00C6FF&height=120&section=footer"/>
</p>