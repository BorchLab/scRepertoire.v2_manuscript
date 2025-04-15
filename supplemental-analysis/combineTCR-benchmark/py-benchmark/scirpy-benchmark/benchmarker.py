import timeit
from collections.abc import Callable, Iterable
import pandas as pd
import numpy as np
from scipy.stats import t
# import gc, tracemalloc

def benchmark(func: Callable, *args, iterations: int=10, **kwargs) -> pd.DataFrame:
    # Runtime timing
    times = np.array(timeit.repeat(lambda: func(*args, **kwargs), number=1, repeat=iterations))
    
    # # single memory profiling run
    # gc.collect()
    # tracemalloc.start()
    # func(*args, **kwargs)
    # snapshot = tracemalloc.take_snapshot()
    # tracemalloc.stop()
    # stats = snapshot.statistics('lineno')
    # func_stats = [stat for stat in stats if stat.traceback and func.__code__.co_filename in str(stat.traceback)]

    benchmark_record = pd.DataFrame([{
        "min": as_bench_time(times.min()),
        "median": as_bench_time(np.median(times)),
        "mean": as_bench_time(times.mean()),
        "max": as_bench_time(times.max()),
        "sd": as_bench_time(times.std()),
        "ci95": as_bench_time(t.ppf(0.975, iterations - 1) * (times.std() / np.sqrt(iterations)) if iterations > 1 else 0.0)#,
        # "mem_alloc": as_bench_bytes(sum(stat.size for stat in func_stats)),
        # "peak_mem_alloc": as_bench_bytes(max((stat.size for stat in func_stats), default=0))
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
