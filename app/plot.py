import matplotlib.pyplot as plt
import os

def plot_result(result, filename="plot.png"):
    if not result:
        raise ValueError("No data to plot.")

    keys = list(result[0].keys())
    x = [str(row[keys[0]]) for row in result]
    y = [row[keys[1]] for row in result]

    plt.figure(figsize=(10, 5))
    plt.bar(x, y, color="skyblue")
    plt.xlabel(keys[0])
    plt.ylabel(keys[1])
    plt.title(f"{keys[1]} by {keys[0]}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    out_path = os.path.join("app", "plots", filename)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    plt.close()

    return out_path
