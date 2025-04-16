from anndata import AnnData
from scirpy.io import read_10x_vdj
import logging
logger = logging.getLogger(__name__)

from benchmarker import benchmark_vdj_loader


def scirpy_loader(dataset_subdir: str) -> AnnData:
    return read_10x_vdj(dataset_subdir + '/filtered_contig_annotation.csv')


def main() -> int:
    
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)
    logger.info("Starting scirpy benchmark...")
    
    benchmark_vdj_loader(
        scirpy_loader,
        output_filename="../../results/scirpy.csv",
        iterations=10,
        dataset_dir="../../datasets/",
    )
    
    logging.info(f"scirpy Benchmark completed.")
    return 0


if __name__ == "__main__":
    main()
