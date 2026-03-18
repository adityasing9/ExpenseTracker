import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect
import pandas as pd
import os
import matplotlib.colors as mcolors

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

    if not os.path.exists("expenses.csv"):
        df = pd.DataFrame(columns=["amount", "category"])
        df.to_csv("expenses.csv", index=False)

    df = pd.read_csv("expenses.csv")

    new_data = {"amount": int(amount), "category": category}
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    df.to_csv("expenses.csv", index=False)

    return redirect("/view")   # 🔥 better UX


# 🗑 Delete Expense
@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    if not os.path.exists("expenses.csv"):
        return redirect("/view")

    df = pd.read_csv("expenses.csv")

    if 0 <= index < len(df):
        df = df.drop(index).reset_index(drop=True)
        df.to_csv("expenses.csv", index=False)

    return redirect("/view")   # 🔥 redirect instead of text


# 🔵 View Dashboard
@app.route("/view")
def view():

    # Ensure CSV exists
    if not os.path.exists("expenses.csv"):
        df = pd.DataFrame(columns=["amount", "category"])
        df.to_csv("expenses.csv", index=False)

    df = pd.read_csv("expenses.csv")

    # Handle empty
    if df.empty:
        return "No data available. Please add expenses."

    # Clean data
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna()

    total = df["amount"].sum()
    category_sum = df.groupby("category")["amount"].sum()

    # 🔥 Send full data for delete feature
    data = df.to_dict(orient="records")

    # 🔥 Dynamic Colors
    categories = category_sum.index.tolist()
    colors = [
        mcolors.hsv_to_rgb((i / len(categories), 0.7, 0.7))
        for i in range(len(categories))
    ]

    # Prediction
    prediction = int(df["amount"].median())

    if df["amount"].max() > 2000:
        note = "⚠️ High-value expenses detected"
    else:
        note = "Spending pattern looks normal"

    category_prediction = df.groupby("category")["amount"].median().to_dict()

    highest_amount = category_sum.max()
    highest_categories = category_sum[category_sum == highest_amount].index.tolist()

    # Ensure static folder
    if not os.path.exists("static"):
        os.makedirs("static")

    # 📊 Graph
    plt.figure(figsize=(20, 10))

    category_sum.plot(
        kind="bar",
        color=colors,
        width=0.6
    )

    plt.title("Expenses by Category", fontsize=22)
    plt.xlabel("Category", fontsize=16)
    plt.ylabel("Amount", fontsize=16)

    plt.xticks(fontsize=14, rotation=0)
    plt.yticks(fontsize=14)

    for i, v in enumerate(category_sum):
        plt.text(i, v + 50, str(int(v)), ha='center', fontsize=12)

    plt.tight_layout()
    plt.savefig("static/bar.png")
    plt.close()

    return render_template(
        "view.html",
        total=total,
        category_sum=category_sum.to_dict(),
        highest_categories=highest_categories,
        highest_amount=highest_amount,
        prediction=prediction,
        note=note,
        category_prediction=category_prediction,
        data=data   # 🔥 IMPORTANT
    )


# 🔴 Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))