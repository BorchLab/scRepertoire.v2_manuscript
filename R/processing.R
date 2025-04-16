
# Helper functions
calculate_qc_metrics <- function(seurat_obj) {
  seurat_obj$nCount_RNA <- colSums(seurat_obj@assays$RNA@layers$counts)
  seurat_obj$nFeature_RNA <- colSums(seurat_obj@assays$RNA@layers$counts != 0)
  seurat_obj[["mito.genes"]] <- PercentageFeatureSet(seurat_obj, 
                                                     pattern = "^MT-")
  seurat_obj[["ribo.genes"]] <- PercentageFeatureSet(seurat_obj, 
                                                     pattern = "^RPS|RPL-")
  return(seurat_obj)
}

plot_qc_metrics <- function(seurat_obj, file_name) {
  p <- VlnPlot(
    object = seurat_obj,
    features = c("nCount_RNA", "nFeature_RNA", "mito.genes", "ribo.genes"),
    pt.size = 0,
    cols = "grey"
  ) +
    theme(legend.position = "none") +
    plot_layout(ncol = 2)
  ggsave(paste0("./qc/", file_name, "_metrics.pdf"), 
         plot = p, 
         height = 8, 
         width = 8)
}

filter_cells <- function(seurat_obj, file_name) {
  standev <- sd(log(seurat_obj$nFeature_RNA)) * 2
  mean_val <- mean(log(seurat_obj$nFeature_RNA))
  cut <- round(exp(standev + mean_val))
  
  p <- FeatureScatter(seurat_obj, 
                      feature1 = "nCount_RNA", 
                      feature2 = "nFeature_RNA") +
    geom_hline(yintercept = cut)
  ggsave(paste0("./qc/", file_name, "_cutpoint.pdf"), 
         plot = p, 
         height = 8, 
         width = 8)
  
  seurat_obj <- subset(seurat_obj, 
                       subset = mito.genes < 10 & nFeature_RNA < cut)
  return(seurat_obj)
}

annotate_with_singler <- function(sce, ref, ref_name) {
  com.res <- SingleR(sce, 
                     ref = ref, 
                     labels = ref$label.fine, 
                     assay.type.test = 1)
  df <- data.frame("labels" = com.res$labels, 
                   "pruned.labels" = com.res$pruned.labels)
  rownames(df) <- rownames(com.res)
  colnames(df) <- paste0(ref_name, ".", colnames(df))
  return(df)
}
