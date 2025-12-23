import json
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# Set pwd to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load data
with open("get-scan.json") as f:
    data = json.load(f)

# Group results by fadvise
grouped = defaultdict(list)
for entry in data:
    fadvise = entry["config"].get("fadvise", "")
    if not fadvise:
        fadvise = "NONE"
    grouped[fadvise].append(entry["results"])

# Prepare data for plotting
labels = []
read_means = []
read_errs = []
scan_means = []
scan_errs = []

for fadvise, results in grouped.items():
    read_vals = [r["read_throughput_avg"] for r in results]
    scan_vals = [r["scan_throughput_avg"] for r in results]
    labels.append(fadvise)
    read_means.append(sum(read_vals) / len(read_vals))
    scan_means.append(sum(scan_vals) / len(scan_vals))
    # Use min/max as error bars
    read_errs.append([
        read_means[-1] - min(read_vals),
        max(read_vals) - read_means[-1]
    ])
    scan_errs.append([
        scan_means[-1] - min(scan_vals),
        max(scan_vals) - scan_means[-1]
    ])

# Transpose error bars for matplotlib
read_errs = list(zip(*read_errs))
scan_errs = list(zip(*scan_errs))

x = range(len(labels))
width = 0.35

fig, ax = plt.subplots()
ax.bar([i - width/2 for i in x], read_means, width, yerr=read_errs, label='Read Throughput', capsize=5)
ax.bar([i + width/2 for i in x], scan_means, width, yerr=scan_errs, label='Scan Throughput', capsize=5)

ax.set_ylabel('Throughput (ops/sec)')
ax.set_title('Read and Scan Throughput by fadvise')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
plt.tight_layout()
plt.savefig("throughput_comparison.png")