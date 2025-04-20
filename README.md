## scRepertoire v2 Manuscript

This is the repository for scRepertoire v2 manuscript. 

More information on the original data set can be found at: 

* Figure 1: [JCI Insights](https://insight.jci.org/articles/view/148035).
* Supplemental Figure 2: [JCI Insights](https://insight.jci.org/articles/view/174776).
* Supplemental Figure 3: [Nature Immunology](https://www.nature.com/articles/s41590-024-01888-9).

### Folder Structure
```
├── Analysis.qmd                   # Main Figure Creation
├── inputs
│   ├── data 
│   │   ├── GSE169440              # Aligned Runs from the GEO
│   │   ├── IntegratedSeuratObject # Intergrated Seurat Object
│   │   └── processedData          # Individual Seurat Objects 
│   ├── scGateDB                   # models for scGate
│   └── supplemental               # Cohort and Benchmarking analyses
├── outputs                        # Figue Viz
├── qc                             # Visualizations of quality control metrics 
├── R                              # General processing scripts
├── README.md 
└── SupplementalAnalysis.qmd       # Supplemental Figure Creation

```

### Paper

Preprint located [here](https://www.biorxiv.org/content/10.1101/2024.12.31.630854v1.abstract)
