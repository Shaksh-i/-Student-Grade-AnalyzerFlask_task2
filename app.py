from flask import Flask, render_template, request
import pandas as pd
import json

app = Flask(__name__)

# In-memory storage for uploaded CSV
df_data = pd.DataFrame()

@app.route("/", methods=["GET", "POST"])
def summary():
    global df_data
    summary_data = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            try:
                df_data = pd.read_csv(file)
                summary_data = []
                for name, group in df_data.groupby("Name"):
                    summary_data.append({
                        "name": name,
                        "avg": round(group["Marks"].mean(), 2),
                        "highest": group["Marks"].max(),
                        "lowest": group["Marks"].min()
                    })
            except Exception as e:
                return f"Error reading CSV: {e}"
    return render_template("summary.html", summary=summary_data)

@app.route("/analytics")
def analytics():
    global df_data
    if df_data.empty:
        subjects = []
        averages = []
    else:
        subjects = list(df_data["Subject"].unique())
        averages = [round(df_data[df_data["Subject"] == s]["Marks"].mean(), 2) for s in subjects]

    # Convert Python lists to JSON for safe JS usage
    return render_template(
        "analytics.html",
        subjects=json.dumps(subjects),
        averages=json.dumps(averages)
    )

if __name__ == "__main__":
    app.run(debug=True)
