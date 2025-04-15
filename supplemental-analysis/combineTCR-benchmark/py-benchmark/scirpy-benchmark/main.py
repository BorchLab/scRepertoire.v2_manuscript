from scirpy.io import read_10x_vdj
import os
import pandas as pd
import logging

from benchmarker import benchmark

def main() -> int:
    
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting scirpy benchmark...")
    
    benchmark_results = pd.DataFrame()
    DATASET_DIR = "../../datasets/"
    DATASET_SUBDIRS = sorted([x for x in os.listdir(DATASET_DIR) if os.path.isdir(DATASET_DIR + x)], key=int)
    output_filename = "../../results/scirpy.csv"
    
    for dataset_subdir in DATASET_SUBDIRS:
        dataset_size = int(dataset_subdir)        
        current_dataset_fname = DATASET_DIR + dataset_subdir + "/filtered_contig_annotation.csv"
        
        logging.info(f"Processing dataset of size {dataset_size}...")
        benchmark_record = benchmark(read_10x_vdj, current_dataset_fname, iterations=10)
        benchmark_record.insert(0, "dataset_size", dataset_size)
        benchmark_results = pd.concat([benchmark_results, benchmark_record], ignore_index=True)
        benchmark_results.to_csv(output_filename, index=False)
        logging.info(f"Dataset of size {dataset_size} processed.")
    
    logging.info(f"scirpy Benchmark completed.")
    return 0

if __name__ == "__main__":
    main()
