#Save plots with consistent formatting
save_plot <- function(plot, filename, height = 3, width = 3, dpi = 300) {
  ggsave(filename = filename, plot = plot, height = height, width = width, 
         dpi = dpi)
}

# Calculate QC metrics
calculate_qc_metrics <- function(seurat_obj) {
  seurat_obj$nCount_RNA <- colSums(seurat_obj@assays$RNA@layers$counts)
  seurat_obj$nFeature_RNA <- colSums(seurat_obj@assays$RNA@layers$counts != 0)
  seurat_obj[["mito.genes"]] <- PercentageFeatureSet(seurat_obj, 
                                                     pattern = "^MT-")
  seurat_obj[["ribo.genes"]] <- PercentageFeatureSet(seurat_obj, 
                                                     pattern = "^RPS|RPL-")
  return(seurat_obj)
}

# Plot QC metrics
plot_qc_metrics <- function(seurat_obj, file_name, qc_dir) {
  p <- VlnPlot(
    object = seurat_obj,
    features = c("nCount_RNA", "nFeature_RNA", "mito.genes", "ribo.genes"),
    pt.size = 0,
    cols = "grey"
  ) +
    theme_minimal() +
    theme(legend.position = "none") +
    plot_layout(ncol = 2)
  
  save_plot(p, 
            file.path(qc_dir, paste0(file_name, "_metrics.pdf")), 
            height = 8, 
            width = 8)
}

# Filter cells based on QC metrics
filter_cells <- function(seurat_obj, file_name, qc_dir) {
  standev <- sd(log(seurat_obj$nFeature_RNA)) * 2
  mean_val <- mean(log(seurat_obj$nFeature_RNA))
  cut <- round(exp(standev + mean_val))
  
  p <- FeatureScatter(seurat_obj, 
                      feature1 = "nCount_RNA", 
                      feature2 = "nFeature_RNA") +
    geom_hline(yintercept = cut)
  
  save_plot(p, file.path(qc_dir, 
                         paste0(file_name, "_cutpoint.pdf")), 
            height = 8, 
            width = 8)
  
  seurat_obj <- subset(seurat_obj, 
                       subset = mito.genes < 10 & nFeature_RNA < cut)
  return(seurat_obj)
}

custom_theme <- theme_minimal(base_size = 8) +
  theme(
    axis.title = element_text(size = 8, color = "black"),
    axis.text = element_text(size = 6, color = "black"),
    legend.text = element_text(size = 4, color = "black"),
    legend.key.size = unit(0.1, "cm"),
    legend.title = element_text(size = 4, color = "black"),
    legend.position = c(1, 1),
    legend.justification = c("right", "top"),
    legend.box.just = "right",
    legend.margin = margin(6, 6, 6, 6),
    legend.spacing.y = unit(2, "cm")
  )