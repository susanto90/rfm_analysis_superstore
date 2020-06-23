# Customer Segmentation based on RFM Analysis using K-Means Clustering Method

RFM analysis is a marketing analysis tool used to identify a company's or an organization's best customers by using three quantitative measures 
which are Recency (R), Frequency (F), Monetary (M).
For this project, I use superstore data from Kaggle which can be downloaded <a href="https://www.kaggle.com/jr2ngb/superstore-data" target="_blank">here</a>. The completed dashboard for the RFM analysis can be found <a href="https://rfm-analysis-superstore.herokuapp.com/" target="_blank">here</a> 

<br>
There are three metrics used on RFM analysis:

* **Recency (R)** <br>
   Elapsed time (e.g. days, weeks, months, etc.) since last order / purchase / engagement of a customer with a service / product.
* **Frequency (F)** <br>
  Total number of orders / purchases or average times between visit / engagement of a customer with a service / product.
* **Monetary (M)** <br>
  Total or average of transaction value (e.g. total amount spent on transactions of a customer with a service / product).

<br>
I use K-Means method to cluster the customers of the superstore and it results with 3 main clusters as explained below.

* **Cluster 1 (Best Customers)** <br>
   Customers in this cluster has low recency, high frequency, and high monetary. It means that these customers just purchased recently, 
   frequently purchased in the past, and spent a good amount of money from the store. There are 317 customers (40%) within this cluster.
* **Cluster 2 (Loyalist Customers)** <br>
   Customers in this cluster has low recency, low frequency, and low monetary. It means that these customers just purchased recently, 
   however they rarely purchased in the past and spent a smaller amount of money from the store. There are 369 customers (46.5%) within this cluster.
* **Cluster 3 (At Risk Customers)** <br>
   Customers in this cluster has high recency. It means that these customers have not purchased from the store for quite some time. 
   In this cluster, there are customers with low frequency-monetary and high frequency-monetary. Further action should be carried out to
   distinguish them. There are 107 customers (13.5%) within this cluster.


Aside from the 3 clusters above, there are customers that cannot be grouped within those clusters. These customers, who I called as **Lost Customers**, are the customers that have very high recency compared to other customers. 

<br>
Based on the clustering result, marketing teams can conduct specific promotional campaign to different customer's clusters to 
retain more customers and maximize the store's profit.
