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
- Auto-categorization  
- Handles real-world noisy data  

### 📈 Data Analysis
- Total spending calculation  
- Category-wise breakdown  
- Monthly summaries  

### 📉 Visualization
- 📊 Bar charts  
- 📈 Monthly trends  

### 💰 Budget Tracking
- Monthly budget  
- Remaining balance  
- Alerts  

### 🧠 Smart Insights
- Income vs expense detection  
- Savings calculation  
- Overspending alerts  

### 🤖 Prediction
- Median-based prediction  
- Category-wise forecasting  

---

## 🛠 Tech Stack
Flask • Pandas • Matplotlib • pdfplumber • Render  

---

## 📂 Project Structure
```
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
```

---

## ⚙️ Local Setup
```bash
git clone https://github.com/adityasing9/expense-tracker.git
cd expense-tracker
pip install -r requirements.txt
python app.py
```

Open: http://127.0.0.1:5000/

---

## 🚀 Deployment
```bash
pip install -r requirements.txt
gunicorn app:app
```

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

# 🚀 Detailed Project Breakdown

## 🔐 Authentication System
- Password hashing (`generate_password_hash`)
- Secure login validation (`check_password_hash`)
- Session-based authentication
- Logout functionality
- Route protection

---

## 📊 Expense Management System
- Add & delete expenses
- CSV storage (`data/{username}.csv`)
- Automatic file creation
- Data cleaning using Pandas
- Numeric conversion with error handling

---

## 📂 PDF Bank Statement Analyzer

### 📥 Upload System
- File upload using Flask (`request.files`)
- Supports PDF bank statements

### 📄 Text Extraction
- Extracts text using `pdfplumber`
- Handles multi-page PDFs

### 🔍 Data Parsing
- Line-by-line processing
- Removes noise (Opening Balance, Total, etc.)
- Regex-based extraction (amounts & dates)
- Handles inconsistent formats

### 🧹 Data Cleaning
- Removes invalid entries
- Removes duplicates
- Converts to structured dataset

---

## 🤖 Smart Data Processing Engine

### 🏷 Auto Categorization
- Food → Swiggy, Zomato  
- Travel → Uber, Ola  
- Shopping → Amazon, Flipkart  
- Bills → Electricity, Recharge  

### 💸 Debit vs Credit Detection
- Debit → Negative values  
- Credit → Positive values  

### 🧠 Structuring
- amount, category, type, date  

---

## 📈 Data Analysis Engine
- Total income & expense calculation
- Category grouping (`groupby`)
- Monthly filtering
- Highest spending category
- Average daily spending
- Median-based analysis

---

## 📉 Data Visualization System
- Bar chart (category spending)
- Line chart (monthly trend)
- Uses `matplotlib.use('Agg')`
- Saves graphs in `/static`

---

## 💰 Budget Management
- Monthly budget setting
- Remaining balance calculation
- Alerts:
  - 🚨 Exceeded  
  - ⚠️ Near limit  
  - ✅ Safe  

---

## 🧠 Smart Financial Insights
- Income vs expense separation
- Savings calculation
- Overspending detection
- Financial health feedback

---

## 🤖 Prediction System
- Median-based prediction
- Category-wise forecasting
- Outlier-resistant logic

---

## 🌐 Full-Stack Integration
- Flask backend routes (`/add`, `/delete`, `/view`, `/upload_pdf`)
- HTML + CSS frontend
- Jinja2 templating

---

## 🎨 UI/UX Design
- Glassmorphism UI
- Gradients & animations
- Responsive layout
- Interactive elements

---

## 📁 File Handling System
- Auto directory creation
- CSV storage
- Graph image generation
- Safe file handling using `os`

---

## 🚀 Deployment (Render)
- `requirements.txt`
- `Procfile` (Gunicorn)
- Cloud-compatible setup

---

## ⚠️ Real-World Challenges Solved
- Messy PDF parsing
- Noise removal
- Duplicate handling
- Data inconsistencies
- Temporary cloud storage handling

---

## 🧠 Core Concepts Demonstrated
- Data preprocessing
- Regex parsing
- File handling
- Session management
- Full-stack development
- Data visualization
- Financial logic
- Deployment pipeline

---

## 👨‍💻 Author
**Aditya Singh**  
https://github.com/adityasing9  

---

<p align="center">
  ⭐ If you like this project, give it a star!
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:6C63FF,100:00C6FF&height=120&section=footer"/>
</p>