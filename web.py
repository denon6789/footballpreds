import os
from flask import Flask, render_template_string
import pandas as pd
from predict_first_scheduled import main as scheduled_predictions

def get_latest_prediction_file():
    files = [f for f in os.listdir('.') if f.startswith('predictions_') and f.endswith('.html')]
    if not files:
        return None
    # Sort by date in filename
    files.sort(reverse=True)
    return files[0]

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Football Score Predictions</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<div class="container py-4">
    <h1 class="mb-4">Football Score Predictions</h1>
    {% if table %}
        {{ table|safe }}
    {% else %}
        <div class="alert alert-warning">No predictions available for upcoming games.</div>
    {% endif %}
</div>
</body>
</html>
'''

@app.route("/")
def index():
    # Always refresh predictions for the first scheduled date
    scheduled_predictions()
    pred_file = get_latest_prediction_file()
    if not pred_file or not os.path.exists(pred_file):
        return render_template_string(HTML_TEMPLATE, table=None)
    df = pd.read_html(pred_file)[0]
    table = df.to_html(classes="table table-striped", index=False)
    return render_template_string(HTML_TEMPLATE, table=table)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10001)), debug=True)
