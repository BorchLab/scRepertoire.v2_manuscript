box::use(data.table[fread])

#' @export
get_datasets <- function() {
    datasets <- lapply(list.files("datasets/", full.names = TRUE), \(file) {
        fread(file, data.table = FALSE)
    })
    names(datasets) <- sapply(datasets, nrow)
    datasets[order(as.integer(names(datasets)))]
}

#' assuming b is a benchmark result for a single expression,
#' return a 1 row data.frame of the results
#' @export
get_bench_record <- function(b) {
    data.frame(
        min = as.character(b$min),
        median = as.character(b$median),
        num_iter = b$n_itr,
        mem_alloc = as.character(b$mem_alloc),
        num_gc = b$n_gc,
        gc0_mean = mean(b$gc[[1]]$level0),
        gc0_median = median(b$gc[[1]]$level0),
        gc0_min = min(b$gc[[1]]$level0),
        gc0_max = max(b$gc[[1]]$level0),
        gc1_mean = mean(b$gc[[1]]$level1),
        gc1_median = median(b$gc[[1]]$level1),
        gc1_min = min(b$gc[[1]]$level1),
        gc1_max = max(b$gc[[1]]$level1),
        gc2_mean = mean(b$gc[[1]]$level2),
        gc2_median = median(b$gc[[1]]$level2),
        gc2_min = min(b$gc[[1]]$level2),
        gc2_max = max(b$gc[[1]]$level2)
    )
}

# TODO make get_bench_record_df