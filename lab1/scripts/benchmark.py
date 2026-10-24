import csv
import os
import subprocess
import matplotlib.pyplot as plt

EXE_PATH = os.path.join("build", "windows-debug", "src", "src.exe")
SIZES = [200, 400, 800, 1200, 1600, 2000]
OUTPUT_CSV = "benchmark_results.csv"
OUTPUT_PLOT_DIR = "plots"
OUTPUT_PLOT_FILE = os.path.join(OUTPUT_PLOT_DIR, "performance.png")


def run_benchmark(n):
    cmd = [EXE_PATH, str(n)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


def main():
    os.makedirs(OUTPUT_PLOT_DIR, exist_ok=True)

    print(f"{'Size (N)':<10} | {'Time (s)':<12} | {'Time (ms)':<14} | {'GFLOPS':<10}")
    print("-" * 55)

    results = []
    times_sec = []
    gflops_list = []

    for n in SIZES:
        time_ms = run_benchmark(n)
        time_sec = time_ms / 1000.0
        operations = 2.0 * (n**3)
        gflops = (operations / time_sec) / 1e9 if time_sec > 0 else 0.0

        times_sec.append(time_sec)
        gflops_list.append(gflops)

        print(f"{n:<10} | {time_sec:<12.3f} | {time_ms:<14.2f} | {gflops:<10.2f}")

        results.append(
            {
                "N": n,
                "Time_sec": round(time_sec, 4),
                "Time_ms": round(time_ms, 2),
                "GFLOPS": round(gflops, 2),
            }
        )

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["N", "Time_sec", "Time_ms", "GFLOPS"])
        writer.writeheader()
        writer.writerows(results)

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(SIZES, times_sec, marker="o", color="blue", linewidth=2)
    plt.title("Время выполнения от размера матрицы")
    plt.xlabel("Размер матрицы (N)")
    plt.ylabel("Время (секунды)")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(SIZES, gflops_list, marker="s", color="green", linewidth=2)
    plt.title("Производительность от размера матрицы")
    plt.xlabel("Размер матрицы (N)")
    plt.ylabel("Производительность (GFLOPS)")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT_FILE, dpi=300)

    print("-" * 55)
    print(f"Эксперименты завершены. Результаты сохранены в: {OUTPUT_CSV}")
    print(f"График сохранен в: {OUTPUT_PLOT_FILE}")


if __name__ == "__main__":
    main()