import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set pwd to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load data
with open('ycsb2.json') as f:
    data = json.load(f)

# Flatten data for DataFrame
rows = []
for entry in data:
    row = {}
    row.update(entry['config'])
    row.update(entry['results'])
    rows.append(row)

df = pd.DataFrame(rows)

# Only keep rows with valid benchmark and cgroup_name
df = df[df['benchmark'].notnull() & df['cgroup_name'].notnull()]

# Group by benchmark and cgroup_name, then average
grouped = df.groupby(['benchmark', 'cgroup_name']).agg({
    'throughput_avg': 'mean',
    'read_latency_avg': 'mean'
}).reset_index()

benchmarks = grouped['benchmark'].unique()
cgroups = grouped['cgroup_name'].unique()
x = np.arange(len(benchmarks))
bar_width = 0.35

# Throughput plot
plt.figure(figsize=(10, 5))
for j, cgroup in enumerate(cgroups):
    values = []
    for bench in benchmarks:
        row = grouped[(grouped['benchmark'] == bench) & (grouped['cgroup_name'] == cgroup)]
        values.append(row['throughput_avg'].values[0] if not row.empty else 0)
    plt.bar(x + j * bar_width, values, width=bar_width, label=cgroup)
plt.title('Average Throughput (ops/sec) by Benchmark and Policy')
plt.xlabel('Benchmark')
plt.ylabel('Avg Throughput')
plt.xticks(x + bar_width * (len(cgroups)-1)/2, benchmarks)
plt.legend()
plt.grid(True, axis='y')
plt.yscale('log')  # <-- Add this line for log-scale
plt.tight_layout()
plt.savefig('ycsb_avg_throughput.png')
plt.close()

# Latency plot
plt.figure(figsize=(10, 5))
for j, cgroup in enumerate(cgroups):
    values = []
    for bench in benchmarks:
        row = grouped[(grouped['benchmark'] == bench) & (grouped['cgroup_name'] == cgroup)]
        values.append(row['read_latency_avg'].values[0] if not row.empty else 0)
    plt.bar(x + j * bar_width, values, width=bar_width, label=cgroup)
plt.title('Average Read Latency (ns) by Benchmark and Policy')
plt.xlabel('Benchmark')
plt.ylabel('Avg Read Latency')
plt.xticks(x + bar_width * (len(cgroups)-1)/2, benchmarks)
plt.legend()
plt.grid(True, axis='y')
plt.tight_layout()
plt.savefig('ycsb_avg_latency.png')
plt.close()

print("Saved ycsb_avg_throughput.png and ycsb_avg_latency.png")