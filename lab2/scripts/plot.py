import os
import matplotlib.pyplot as plt
import pandas as pd

CSV_PATH = "benchmark_results.csv"
OUTPUT_DIR = "plots"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "speedup.png")


def main():
    if not os.path.exists(CSV_PATH):
        print(f"Файл {CSV_PATH} не найден!")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = pd.read_csv(CSV_PATH)

    plt.figure(figsize=(9, 5))

    for n in df["N"].unique():
        sub = df[df["N"] == n]
        plt.plot(sub["Threads"], sub["Speedup"], marker="o", label=f"N = {n}")

    plt.plot(
        df["Threads"].unique(),
        df["Threads"].unique(),
        "k--",
        alpha=0.5,
        label="Идеальное ускорение",
    )

    plt.title("Ускорение (Speedup) от количества потоков")
    plt.xlabel("Количество потоков (OpenMP)")
    plt.ylabel("Ускорение (S = T1 / Tp)")
    plt.xticks(df["Threads"].unique())
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(OUTPUT_FILE, dpi=300)
    print(f"График успешно сохранен в: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()