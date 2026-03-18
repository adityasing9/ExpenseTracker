from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, session

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.colors as mcolors

import pdfplumber
import re

from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

os.makedirs("data", exist_ok=True)
os.makedirs("static", exist_ok=True)

# ===== AUTO CATEGORY FUNCTION =====
def auto_category(text):
    text = str(text).lower()

    if "swiggy" in text or "zomato" in text or "food" in text:
        return "Food"
    elif "uber" in text or "ola" in text or "travel" in text:
        return "Travel"
    elif "amazon" in text or "flipkart" in text:
        return "Shopping"
    elif "electricity" in text or "bill" in text:
        return "Bills"
    else:
        return "Other"

# ================= AUTH =================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not os.path.exists("users.csv"):
            pd.DataFrame(columns=["username", "password"]).to_csv("users.csv", index=False)

        df = pd.read_csv("users.csv")

        if username in df["username"].values:
            return "User already exists"

        df = pd.concat([df, pd.DataFrame([{
            "username": username,
            "password": generate_password_hash(password)
        }])], ignore_index=True)

        df.to_csv("users.csv", index=False)
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not os.path.exists("users.csv"):
            return "No users found"

        df = pd.read_csv("users.csv")
        user = df[df["username"] == username]

        if not user.empty:
            if check_password_hash(user.iloc[0]["password"], password):
                session["user"] = username
                return redirect("/view")

        return "Invalid credentials"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ================= HOME =================

@app.route("/")
def home():
    return redirect("/view") if "user" in session else redirect("/login")


# ================= ADD =================

@app.route("/add", methods=["POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    username = session["user"]
    file_path = f"data/{username}.csv"

    if not os.path.exists(file_path):
        pd.DataFrame(columns=["amount", "category", "date"]).to_csv(file_path, index=False)

    df = pd.read_csv(file_path)

    df = pd.concat([df, pd.DataFrame([{
        "amount": int(request.form["amount"]),
        "category": request.form["category"],
        "date": datetime.now().strftime("%Y-%m-%d")
    }])], ignore_index=True)

    df.to_csv(file_path, index=False)
    return redirect("/view")


# ================= DELETE =================

@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    if "user" not in session:
        return redirect("/login")

    file_path = f"data/{session['user']}.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if 0 <= index < len(df):
            df = df.drop(index).reset_index(drop=True)
            df.to_csv(file_path, index=False)

    return redirect("/view")


# ================= SET BUDGET =================

@app.route("/set_budget", methods=["POST"])
def set_budget():
    session["budget"] = float(request.form["budget"])
    return redirect("/view")


# ================= VIEW =================

@app.route("/view")
def view():
    if "user" not in session:
        return redirect("/login")

    username = session["user"]
    file_path = f"data/{username}.csv"

    if not os.path.exists(file_path):
        pd.DataFrame(columns=["amount", "category", "date"]).to_csv(file_path, index=False)

    df = pd.read_csv(file_path)

    # Fix missing date column
    if "date" not in df.columns:
        df["date"] = datetime.now().strftime("%Y-%m-%d")
        df.to_csv(file_path, index=False)

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna()

    # ===== EMPTY CASE =====
    budget = session.get("budget", 0)

    if df.empty:
        return render_template(
            "view.html",
            total=0, category_sum={}, highest_categories=[], highest_amount=0,
            prediction=0, note="No data yet. Start adding expenses!",
            category_prediction={}, data=[], bar_chart=None,
            budget=budget, remaining=budget,
            monthly_total=0, top_category="N/A", avg_daily=0,
            monthly_note="No data yet", line_chart=None
        )

    # ===== BASIC =====
    total = abs(df["amount"].sum())
    category_sum = df.groupby("category")["amount"].apply(lambda x: abs(x.sum()))
    data = df.to_dict(orient="records")
    # ✅ NEW: income vs expense
    spending = df[df["amount"] < 0]["amount"].abs()
    income = df[df["amount"] > 0]["amount"]

    total_spent = spending.sum()
    total_income = income.sum()

    if total_income > 0:
        savings = total_income - total_spent
    else:
        savings = -total_spent

    if savings < 0:
        insight = "🚨 You are overspending more than your income"
    elif savings < total_income * 0.2:
        insight = "⚠️ Your savings are very low"
    else:
        insight = "✅ Good financial health"

    # ===== MONTH =====
    df["month"] = df["date"].dt.to_period("M").astype(str)
    current_month = str(pd.Timestamp.today().to_period("M"))

    monthly_df = df[df["month"] == current_month]

    if not monthly_df.empty:
        monthly_total = monthly_df["amount"].sum()
        top_category = monthly_df.groupby("category")["amount"].sum().idxmax()
        days = monthly_df["date"].nunique()
        avg_daily = int(monthly_total / days) if days else 0
    else:
        monthly_total, top_category, avg_daily = 0, "N/A", 0

    # ===== MONTHLY NOTE (FIXED) =====
    if budget > 0:
        if monthly_total > budget:
            monthly_note = "🚨 Monthly budget exceeded"
        elif monthly_total > budget * 0.8:
            monthly_note = "⚠️ Close to monthly budget"
        else:
            monthly_note = "✅ Good spending this month"
    else:
        monthly_note = "Set budget to get insights"

    # ===== TREND =====
    monthly_trend = df.groupby("month")["amount"].sum()

    # ===== PREDICTION =====
    prediction = int(df["amount"].median())

    if budget > 0:
        remaining = budget - total
        if total > budget:
            note = "🚨 Budget exceeded!"
        elif total > budget * 0.8:
            note = "⚠️ Close to limit"
        else:
            note = "✅ Within budget"
    else:
        remaining = 0
        note = "Spending pattern looks normal"

    category_prediction = df.groupby("category")["amount"].median().to_dict()
    highest_amount = category_sum.max()
    highest_categories = category_sum[category_sum == highest_amount].index.tolist()

    if not os.path.exists("static"):
        os.makedirs("static")

    # ===== BAR =====
    colors = [mcolors.hsv_to_rgb((i / len(category_sum), 0.7, 0.7)) for i in range(len(category_sum))]
    plt.figure(figsize=(20, 10))
    category_sum.abs().plot(kind="bar", color=colors)
    bar_file = f"bar_{username}.png"
    plt.savefig(f"static/{bar_file}")
    plt.close()

    # ===== LINE =====
    plt.figure(figsize=(10, 5))
    monthly_trend.plot(marker='o')
    line_file = f"line_{username}.png"
    plt.savefig(f"static/{line_file}")
    plt.close()
    print(df.head())

    return render_template(
        "view.html",
        total=total,
        category_sum=category_sum.to_dict(),
        highest_categories=highest_categories,
        highest_amount=highest_amount,
        prediction=prediction,
        note=note,
        category_prediction=category_prediction,
        data=data,
        bar_chart=bar_file,
        line_chart=line_file,
        budget=budget,
        remaining=remaining,
        monthly_total=monthly_total,
        top_category=top_category,
        avg_daily=avg_daily,
        total_income=total_income,
        total_spent=total_spent,
        savings=savings,
        insight=insight,
        monthly_note=monthly_note
    )

@app.route("/upload", methods=["POST"])
def upload():
    if "user" not in session:
        return redirect("/login")

    file = request.files["file"]

    if file.filename == "":
        return redirect("/view")

    df_new = pd.read_csv(file)

    # Auto categorize if category missing
    if "category" not in df_new.columns:
        df_new["category"] = df_new.iloc[:, 0].apply(auto_category)

    # Expected columns: amount, category (you can adjust)
    if "amount" not in df_new.columns:
        return "CSV must contain 'amount' column"

    # Add missing columns
    if "category" not in df_new.columns:
        df_new["category"] = "Other"

    if "date" not in df_new.columns:
        df_new["date"] = datetime.now().strftime("%Y-%m-%d")

    username = session["user"]
    file_path = f"data/{username}.csv"

    if not os.path.exists(file_path):
        df_new.to_csv(file_path, index=False)
    else:
        df_old = pd.read_csv(file_path)
        df = pd.concat([df_old, df_new], ignore_index=True)
        df.to_csv(file_path, index=False)

    return redirect("/view")



@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if "user" not in session:
        return redirect("/login")

    file = request.files["file"]
    if file.filename == "":
        return redirect("/view")

    transactions = []

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if not text:
                    continue

                lines = text.split("\n")

                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    lower = line.lower()

                    # ✅ Skip unwanted lines
                    if any(x in lower for x in [
                        "opening balance", "ending balance",
                        "total", "account", "currency"
                    ]):
                        continue

                    # ✅ Must contain INR
                    if "inr" not in lower:
                        continue

                    # ✅ RELAXED DATE CHECK (FIXED)
                    if not re.search(r"\d{2}.*\d{4}", line):
                        continue

                    # ✅ FLEXIBLE AMOUNT EXTRACTION (FIXED)
                    matches = re.findall(r"([\d,]+\.\d{2})", line)

                    if len(matches) < 2:
                        continue

                    try:
                        values = [float(x.replace(",", "")) for x in matches]

                        # transaction = second last value
                        amount = values[-2]

                        # ✅ Detect debit/credit (FIXED)
                        is_debit = "-" in line

                        if is_debit:
                            amount = -amount

                        # ❌ Remove garbage
                        if abs(amount) > 100000 or amount == 0:
                            continue

                    except:
                        continue

                    category = auto_category(line)

                    transactions.append({
                        "amount": amount,
                        "category": category,
                        "type": "debit" if amount < 0 else "credit",
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })

    except Exception as e:
        return f"Error reading PDF: {str(e)}"

    if not transactions:
        return "No valid transactions found"

    # ===== SAVE CLEAN DATA =====
    username = session["user"]
    file_path = f"data/{username}.csv"

    df_new = pd.DataFrame(transactions)

    # ✅ REMOVE DUPLICATES
    df_new = df_new.drop_duplicates()

    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path)

        # ✅ Ensure same columns
        df_old = df_old.reindex(columns=["amount", "category", "type", "date"])

        df = pd.concat([df_old, df_new], ignore_index=True)
        df = df.drop_duplicates()
    else:
        df = df_new

    df.to_csv(file_path, index=False)

    return redirect("/view")
# ================= RUN =================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)