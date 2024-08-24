import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64


def plot_feature_importance(feature_importance):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(feature_importance.values()),
                y=list(feature_importance.keys()), orient='h')
    plt.title('Feature Importance for Traffic Prediction')
    plt.xlabel('Importance')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()


def plot_traffic_prediction(actual, predicted):
    plt.figure(figsize=(12, 6))
    plt.scatter(actual, predicted, alpha=0.5)
    plt.plot([actual.min(), actual.max()], [
             actual.min(), actual.max()], 'r--', lw=2)
    plt.xlabel('Actual Average Speed')
    plt.ylabel('Predicted Average Speed')
    plt.title('Actual vs Predicted Average Speed')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()


def create_html_report(feature_importance_plot, prediction_plot, optimization_strategies):
    strategies_html = "<h2>Route Optimization Strategies</h2><ul>"
    # Limit to first 10 strategies
    for strategy in optimization_strategies[:10]:
        strategies_html += f"<li>{strategy}</li>"
    strategies_html += "</ul>"

    html = f"""
    <html>
        <head>
            <title>AIDSCRO - Traffic Optimization Report</title>
        </head>
        <body>
            <h1>AIDSCRO - Traffic Optimization Report</h1>
            <h2>Feature Importance</h2>
            <img src="data:image/png;base64,{feature_importance_plot}" alt="Feature Importance Plot">
            <h2>Traffic Prediction</h2>
            <img src="data:image/png;base64,{prediction_plot}" alt="Traffic Prediction Plot">
            {strategies_html}
        </body>
    </html>
    """
    return html
