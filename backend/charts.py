import matplotlib.pyplot as plt
import os

CHART_FOLDER = "charts"
os.makedirs(CHART_FOLDER, exist_ok=True)

def bar_chart(df, x, y):

    plt.figure(figsize=(8,5))

    df.groupby(x)[y].sum().plot(kind="bar")

    path = os.path.join(CHART_FOLDER, "bar_chart.png")

    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return path