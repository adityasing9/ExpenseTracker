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
    if not os.path.exists("expenses.csv"):
        df = pd.DataFrame(columns=["amount", "category"])
        df.to_csv("expenses.csv", index=False)

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

    import os
    import pandas as pd
    import matplotlib.pyplot as plt

    # Ensure CSV exists
    if not os.path.exists("expenses.csv"):
        df = pd.DataFrame(columns=["amount", "category"])
        df.to_csv("expenses.csv", index=False)

    df = pd.read_csv("expenses.csv")

    # Handle empty data
    if df.empty:
        return "No data available. Please add expenses."

    # Ensure correct columns
    if "amount" not in df.columns or "category" not in df.columns:
        return "CSV format error"

    # Convert amount safely
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna()

    total = df["amount"].sum()
    category_sum = df.groupby("category")["amount"].sum()

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

    # Graphs
    plt.figure()
    category_sum.plot(kind="bar")
    plt.savefig("static/bar.png")
    plt.close()

    plt.figure()
    category_sum.plot(kind="pie", autopct='%1.1f%%')
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