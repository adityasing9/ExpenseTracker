import matplotlib
matplotlib.use('Agg')  # 👈 FIX (no GUI mode)

import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    amount = request.form["amount"]
    category = request.form["category"]

    df = pd.read_csv("expenses.csv")

    new_data = {"amount": int(amount), "category": category}
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    df.to_csv("expenses.csv", index=False)

    return "Expense Added!"

@app.route("/view")
def view():
    import matplotlib.pyplot as plt

    df = pd.read_csv("expenses.csv")

    total = df["amount"].sum()
    category_sum = df.groupby("category")["amount"].sum()

    from sklearn.linear_model import LinearRegression
    import numpy as np

    # Prepare data
    amounts = df["amount"].values

    # X = index (0,1,2...)
    X = np.arange(len(amounts)).reshape(-1, 1)
    y = amounts

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next expense
    next_index = [[len(amounts)]]
    prediction = int(df["amount"].median())
    if df["amount"].max() > 2000:
        note = "⚠️ High-value expenses detected, prediction adjusted"
    else:
        note = "Spending pattern looks normal"

    category_prediction = df.groupby("category")["amount"].median().to_dict()

    # 🔥 INSIGHTS
    highest_amount = category_sum.max()
    highest_categories = category_sum[category_sum == highest_amount].index.tolist()

    # Create graphs
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

if __name__ == "__main__":
    app.run(debug=True)