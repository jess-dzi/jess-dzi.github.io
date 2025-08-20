import os
import yfinance as yf
import matplotlib.pyplot as plt
import json

class ChartGenerator:
    def __init__(self, output_dir="../Personal Project/charts"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_chart(self, symbol, name):
        """Download last month of data and save a line chart."""
        df = yf.download(symbol, period="1mo", interval="1d")
        plt.figure(figsize=(8, 4))
        plt.plot(df.index, df["Close"], label=name, linewidth=2)
        plt.title(f"{name} - Last Month")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Save chart
        filename = f"{name.replace(' ', '_')}_chart.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, bbox_inches="tight")
        plt.close()
        return filename  # Return just filename for website relative path

    def generate_all(self, index_predictions):
        """
        Generate charts and dashboard JSON for a set of index predictions.
        index_predictions should be a dict: {name: (symbol, prediction)}
        """
        print("generate_all called with:", index_predictions)
        dashboard_data = []

        for name, (symbol, pred) in index_predictions.items():
            print(f"Generating chart for {name}...")
            filename = self.generate_chart(symbol, name)
            dashboard_data.append({
                "name": name,
                "symbol": symbol,
                "prediction": "up" if pred == 1 else "down",
                "chart": filename  # relative path for website
            })

        # Write JSON for website
        json_path = os.path.join(self.output_dir, "dashboard.json")
        print("Writing dashboard JSON to:", json_path)
        with open(json_path, "w") as f:
            json.dump(dashboard_data, f, indent=2)

        print("Charts and JSON ready!")
        return dashboard_data



