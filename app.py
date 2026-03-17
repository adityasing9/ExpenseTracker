import matplotlib
matplotlib.use('Agg')  # No GUI (important for deployment)

import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# 🟢 Home Page
@app.route("/")
def home():
    return render_template("index.html")


# 🟡 Add Expense
@app.route("/add", methods=["POST"])
def add():
    amount = request.form["amount"]
    category = request.form["category"]

    # Read CSV
    df = pd.read_csv("expenses.csv")

    # Add new data
    new_data = {"amount": int(amount), "category": category}
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    # Save back
    df.to_csv("expenses.csv", index=False)

    return "Expense Added!"


# 🔵 View Dashboard
@app.route("/view")
def view():

    df = pd.read_csv("expenses.csv")

    # Basic analysis
    total = df["amount"].sum()
    category_sum = df.groupby("category")["amount"].sum()

    # 🔥 Prediction (robust)
    prediction = int(df["amount"].median())

    if df["amount"].max() > 2000:
        note = "⚠️ High-value expenses detected, prediction adjusted"
    else:
        note = "Spending pattern looks normal"

    # 📊 Category-wise prediction
    category_prediction = df.groupby("category")["amount"].median().to_dict()

    # 📊 Insights
    highest_amount = category_sum.max()
    highest_categories = category_sum[category_sum == highest_amount].index.tolist()

    # 📈 Graphs
    plt.figure()
    category_sum.plot(kind="bar")
    plt.title("Expenses by Category")
    plt.savefig("static/bar.png")
    plt.close()

    plt.figure()
    category_sum.plot(kind="pie", autopct='%1.1f%%')
    plt.title("Category Distribution")
    plt.savefig("static/pie.png")
    plt.close()

    return render_template(
        "view.html",
        total=total,
        category_sum=category_sum.to_dict(),
        highest_categories=highest_categories,
        highest_amount=highest_amount,
        prediction=prediction,
        note=note,
        category_prediction=category_prediction
    )


# 🔴 Run App (for deployment)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))