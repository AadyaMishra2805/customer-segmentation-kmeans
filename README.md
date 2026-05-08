# Customer Segmentation using K-Means Clustering

## Overview

This project performs customer segmentation using the Mall Customer dataset and K-Means clustering. The goal is to group customers based on their annual income and spending behavior to help businesses understand customer patterns and improve marketing strategies.

## Features

* Data preprocessing and normalization
* K-Means clustering from K=2 to K=8
* Elbow Method for optimal cluster selection
* Cluster visualization using matplotlib
* Business insights and observations
* Bonus comparison with DBSCAN clustering

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Jupyter Notebook

## Dataset

Dataset used: Mall Customer Dataset

Features used for clustering:

* Annual Income (k$)
* Spending Score (1-100)

## Project Workflow

1. Load and preprocess dataset
2. Scale features using StandardScaler
3. Apply K-Means clustering
4. Use Elbow Method to determine optimal K
5. Visualize customer clusters
6. Compare results with DBSCAN
7. Generate business insights

## Elbow Method

The Elbow Method was used to determine the optimal number of clusters and identify the best value of K for customer segmentation.

## K-Means Clustering Result

The customers were segmented into different groups based on spending patterns and annual income using K-Means clustering.

## DBSCAN Comparison

DBSCAN was implemented as a bonus clustering algorithm to compare clustering behavior and identify density-based groups.

## Business Insights

* High-income high-spending customers are ideal targets for premium services and loyalty programs.
* High-income low-spending customers may need personalized marketing campaigns.
* Moderate spenders represent stable and consistent customers.
* Low-income low-spending customers are more price-sensitive and respond better to discounts.

## K-Means vs DBSCAN

| K-Means                           | DBSCAN                               |
| --------------------------------- | ------------------------------------ |
| Requires predefined K             | No need to define number of clusters |
| Works well for spherical clusters | Works well for irregular clusters    |
| Faster and easier to interpret    | Detects noise and outliers           |
| Better for this dataset           | Some points classified as noise      |

## Results

* Optimal K selected using Elbow Method: 5
* Clear customer groups identified
* K-Means produced more interpretable clusters for business analysis

## Repository Structure

```text
customer-segmentation-kmeans/
│
├── customer_segmentation_kmeans.ipynb
├── Mall_Customers.csv
├── README.md
├── elbow_method.png
├── kmeans_clusters.png
└── dbscan_clusters.png
```

## How to Run

```bash
pip install pandas numpy matplotlib scikit-learn
```

Run the notebook:

```bash
jupyter notebook
```

## Author

Aadya Mishra

