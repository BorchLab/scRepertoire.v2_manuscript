import dandelion as ddl
from dandelion import read_10x_vdj
import sys, os
import logging
logger = logging.getLogger(__name__)

sys.path.append("../")
from benchmarker import benchmark_vdj_loader


def dandelion_loader(dataset_subdir: str) -> ddl.Dandelion:
    return read_10x_vdj(dataset_subdir, filename_prefix='filtered')


def main() -> int:
    
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)
    logging.info("Starting sc-dandelion benchmark...")
    
    benchmark_vdj_loader(
        dandelion_loader,
        output_filename="../../results/dandelion.csv",
        iterations=10,
        dataset_dir="../../datasets/",
    )
    
    logging.info(f"sc-dandelion Benchmark completed.")
    return 0


if __name__ == "__main__":
    main()
