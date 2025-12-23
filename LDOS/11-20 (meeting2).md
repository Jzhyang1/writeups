
### Notes after chatting with Saurabh
* Page prefetching potentially
* Get eviction working on cloudlab

Download & boot
```bash
git clone https://github.com/cache-ext/cache_ext.git
cd cache_ext
git submodule update --init --recursive

sudo rm /usr/lib/python3.12/EXTERNALLY-MANAGED # Gets rid of python warning
sudo ./install_kernel.sh

sudo grub-reboot 'Advanced options for Ubuntu>Ubuntu, with Linux 6.6.8-cache-ext+'
sudo reboot now
```
Check system 
```bash
# Make sure it isn't generic
uname -r
```
Extra storage
```bash
sudo mkdir /data  
sudo /usr/local/etc/emulab/mkextrafs.pl -f /data  
# It may give some warnings, just say yes

sudo cp cache_ext /data -r
cd /data/cache_ext
```
Install benchmarks
```bash
# Required
./install_misc.sh
sudo ./setup_isolation.sh
sudo ./build_policies.sh
```
choose whichever ones are needed
```bash
# Benchmarks

sudo apt install clang-14  # needed for filesearch
sudo ./install_filesearch.sh

sudo apt install cmake     # needed for ycsb
sudo ./install_ycsb.sh     # NoSQL

sudo ./install_leveldb.sh  # KV store
```
Run benchmarks
```bash
cd /data/cache_ext/eval/<benchmark name>
sudo ./run.sh
```
View results
```bash
cat /data/cache_ext/results/<benchmark name>.json
```

---
Successfully run existing benchmark

Example results for file search
```json
[
    {
        "config": {
            "name": "filesearch_benchmark",
            "cpus": 8,
            "passes": 10,
            "cgroup_size": 1073741824,
            "cgroup_name": "baseline_test",
            "benchmark": "filesearch",
            "iteration": 1
        },
        "results": {
            "runtime_sec": 763.6647765636444
        }
    },
    {
        "config": {
            "name": "filesearch_benchmark",
            "cpus": 8,
            "passes": 10,
            "cgroup_size": 1073741824,
            "cgroup_name": "baseline_test",
            "benchmark": "filesearch",
            "iteration": 2
        },
        "results": {
            "runtime_sec": 750.0166215896606
        }
    },
    {
        "config": {
            "name": "filesearch_benchmark",
            "cpus": 8,
            "passes": 10,
            "cgroup_size": 1073741824,
            "cgroup_name": "baseline_test",
            "benchmark": "filesearch",
            "iteration": 3
        },
        "results": {
            "runtime_sec": 694.1990044116974
        }
    },
    {
        "config": {
            "name": "filesearch_benchmark",
            "cpus": 8,
            "passes": 10,
            "cgroup_size": 1073741824,
            "cgroup_name": "cache_ext_test",
            "benchmark": "filesearch",
            "iteration": 1
        },
        "results": {
            "runtime_sec": 419.0598957538605
        }
    },
    {
        "config": {
            "name": "filesearch_benchmark",
            "cpus": 8,
            "passes": 10,
            "cgroup_size": 1073741824,
            "cgroup_name": "cache_ext_test",
            "benchmark": "filesearch",
            "iteration": 2
        },
        "results": {
            "runtime_sec": 341.96610474586487
        }
    },
    {
        "config": {
            "name": "filesearch_benchmark",
            "cpus": 8,
            "passes": 10,
            "cgroup_size": 1073741824,
            "cgroup_name": "cache_ext_test",
            "benchmark": "filesearch",
            "iteration": 3
        },
        "results": {
            "runtime_sec": 336.6379985809326
        }
    }
]
```
---
Trying to run custom policy

It looks like all that needs to be done is to make a `cache_ext_<policyname>.{bpf.c,.c}` file and call `make` to get the `.out` file. Then run 

```bash
python3 "$BENCH_PATH/bench_<workload>.py" \
	--cpu 8 \
	--policy-loader "$POLICY_PATH/cache_ext_<policyname>.out" \
	--results-file "$RESULTS_PATH/<workload>_results.json" \
	--data-dir "$FILES_PATH" \
	--iterations "$ITERATIONS"
```

Where is this defined? `struct cache_ext_eviction_ctx`
Let's use this (random eviction): https://github.com/Jzhyang1/cache_ext.git