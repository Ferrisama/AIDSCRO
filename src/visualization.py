# src/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64


def plot_feature_importance(feature_importance):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(feature_importance.values()),
                y=list(feature_importance.keys()), orient='h')
    plt.title('Feature Importance')
    plt.xlabel('Importance')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()


def plot_energy_consumption_prediction(actual, predicted):
    plt.figure(figsize=(12, 6))
    plt.plot(actual, label='Actual')
    plt.plot(predicted, label='Predicted')
    plt.title('Actual vs Predicted Energy Consumption')
    plt.xlabel('Time')
    plt.ylabel('Energy Consumption')
    plt.legend()
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()


def create_html_report(feature_importance_plot, prediction_plot, optimization_strategies):
    strategies_html = "<h2>Optimization Strategies</h2><ul>"
    for strategy in optimization_strategies:
        strategies_html += f"<li>{strategy}</li>"
    strategies_html += "</ul>"

    html = f"""
    <html>
        <head>
            <title>AIDSCRO Visualization and Optimization Report</title>
        </head>
        <body>
            <h1>AIDSCRO Visualization and Optimization Report</h1>
            <h2>Feature Importance</h2>
            <img src="data:image/png;base64,{feature_importance_plot}" alt="Feature Importance Plot">
            <h2>Energy Consumption Prediction</h2>
            <img src="data:image/png;base64,{prediction_plot}" alt="Energy Consumption Prediction Plot">
            {strategies_html}
        </body>
    </html>
    """
    return html
