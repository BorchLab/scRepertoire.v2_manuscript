import timeit
from collections.abc import Callable, Iterable
import pandas as pd
import numpy as np
from scipy.stats import t
import os
import logging
import gc, tracemalloc


def benchmark_vdj_loader(
    vdj_func: Callable,
    output_filename: str,
    iterations: int=10,
    dataset_dir: str = "../../datasets/"
) -> pd.DataFrame:
    """Benchmark a vdj data loader

    Args:
        vdj_func (Callable): must be a single argument function that takes in the directory
        of the vdj dataset to load.
        output_filename (str): the output csv filename to save results
        iterations (int, optional): Number of runtime benchmark runs. If this value is 0, then only memory is benchmarked. Defaults to 10.
        dataset_dir (str, optional): The top directory of all datasets. Defaults to "../../datasets/".

    Returns:
        pd.DataFrame: benchmark result dataframe with dataset size column
    """
    
    benchmark_results = pd.DataFrame()
    DATASET_SUBDIRS = sorted([x for x in os.listdir(dataset_dir) if os.path.isdir(dataset_dir + x)], key=int)
    
    for dataset_subdir in DATASET_SUBDIRS:
        
        dataset_size = int(dataset_subdir)
        full_dataset_subdir = os.path.join(dataset_dir, dataset_subdir)
        
        logging.info(f"Processing dataset of size {dataset_size}...")
        benchmark_record = benchmark(lambda: vdj_func(full_dataset_subdir), iterations=iterations)
        benchmark_record.insert(0, "dataset_size", dataset_size)
        benchmark_results = pd.concat([benchmark_results, benchmark_record], ignore_index=True)
        benchmark_results.to_csv(output_filename, index=False)
        logging.info(f"Dataset of size {dataset_size} processed.")
    
    return benchmark_results


def benchmark(func: Callable, iterations: int=10) -> pd.DataFrame:
    """Benchmark a no-argument function

    Args:
        func (Callable): A pure 0 argument function
        iterations (int, optional): Number of runtime benchmarking iterations. Defaults to 10.

    Returns:
        pd.DataFrame: 1 row benchmark result dataframe
    """
    if not iterations:
        return benchmark_memory(func)
    return pd.concat([
        benchmark_runtime(func, iterations=iterations),
        benchmark_memory(func)
    ], axis=1)

def benchmark_runtime(func: Callable, iterations: int=10) -> pd.DataFrame:

    times = np.array(timeit.repeat(func, number=1, repeat=iterations))

    benchmark_record = pd.DataFrame([{
        "min": as_bench_time(times.min()),
        "median": as_bench_time(np.median(times)),
        "mean": as_bench_time(times.mean()),
        "max": as_bench_time(times.max()),
        "sd": as_bench_time(times.std()),
        "ci95": as_bench_time(confidence_interval(times.std(), iterations))
    }])
    return benchmark_record


def as_bench_time(seconds: float) -> str:
    units = [
        (1e-9, "ns"),
        (1e-6, "µs"),
        (1e-3, "ms"),
        (1, "s"),
        (60, "m"),
        (3600, "h"),
        (86400, "d"),
        (604800, "w")
    ]
    selected_unit = units[0]
    for unit in units:
        if seconds >= unit[0]:
            selected_unit = unit
        else:
            break
    value = seconds / selected_unit[0]
    formatted = f"{value:.3g}"
    return f"{formatted}{selected_unit[1]}"


def confidence_interval(sd: float, n: int, alpha: float = 0.05) -> float:
    return t.ppf(1 - (alpha / 2), n - 1) * (sd / np.sqrt(n)) if n > 1 else 0.0


def benchmark_memory(func: Callable) -> pd.DataFrame:
    """Benchmark a 0-argument pure function for memory usage"""

    gc.collect()
    tracemalloc.start()
    snapshot_start = tracemalloc.take_snapshot()
    result = func()
    snapshot_end = tracemalloc.take_snapshot()
    tracemalloc.stop()
    
    global _anchor
    _anchor = result
    
    stats = snapshot_end.compare_to(snapshot_start, 'lineno')
    allocation_bytes = [stat.size_diff for stat in stats if stat.size_diff > 0]
    
    del _anchor
    
    return pd.DataFrame([{
        "mem_alloc": as_bench_bytes(sum(allocation_bytes)),
        "peak_mem_alloc": as_bench_bytes(max(allocation_bytes, default=0))
    }])


def as_bench_bytes(bytes_value: Iterable[float]) -> str:

    if bytes_value < 1024:
        return f"{bytes_value}B"
    
    units = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']
    for unit in units:
        bytes_value /= 1024
        if bytes_value < 1024:
            formatted = f"{bytes_value:.3g}"
            return f"{formatted}{unit}"
    return f"{bytes_value:.3g}{units[-1]}"
