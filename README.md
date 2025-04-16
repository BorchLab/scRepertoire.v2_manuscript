This is the repository for the analysis of erythema migrans skin and lesional data set used in the scRepertoire v2 manuscript. 

More information on the original data set can be found at: [JCI Insights](https://insight.jci.org/articles/view/148035).

### Folder Structure
```
├── Analysis.Qmd
├── Analysis.pdf
├── inputs
│   ├── data - general processing script
│   │   ├── GSE169440 - Aligned Runs from the Geo Omnibus Accession
│   │   ├──IntegratedSeuratObject.rds - Intergrated Seurat Object
│   │   └── processedData - Individual Seurat Objects by sequencing Run
│   └── scGateDB - models for scGate
├── outputs - Visualizations
├── qc - Visualizations of quality control metrics during processing
└── README.md

```
