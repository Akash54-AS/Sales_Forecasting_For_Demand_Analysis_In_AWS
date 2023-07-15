# Hi, I'm Akash! 👋


## 🚀 About Me
I'm a Data Engineer with good hands-on experience leveraging data and business principles to solve large-scale data infrastructure problems. I am very fascinated by Data Science, AI, Blockchain, and Robotics. If you have such exciting projects and want me to the part of them, I am happy to join you aboard.



## 🛠 Skills

💻 Programming Languages: C, C++, Python, SQL, Unix Shell Scripting

⛅ Clouds: Google Cloud Platform (GCP), Microsoft Azure, Amazon Web Services (AWS)

🌐 Big Data: Hadoop, Spark, Docker, Airflow, Snowflake, NiFi, ETL, Data Science, Data Modeling, Data Analytics, Distributed Systems, Data Quality, Data Engineering, and Data Solutions.

📙 IT Constructs Machine Learning, Data Structures, and Algorithms, DBMS, Operating Systems.

📱Software: Git, Jira, Bitbucket, Confluence, VS Code.



## 🔗 Links
[![Github repo](https://github.com/Akash54-AS/Akash54-AS/blob/main/GitHub-Mark-Light-32px.png)](https://github.com/Akash54-AS)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/akashwaitage/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/AkashWaitage54)

# Sales Forecasting for Demand Analysis in AWS
This project uses the sales data which is into the
S3 bucket to upload into MySQL database using AWS RDS service for supporting web application and then using EMR services it running the migrated spark script from on-prem for predicting the future sales. all the data will be finally loaded into the Redshift, for Visualisation Quicksight is used.

## Architecture 
[![Github repo](https://github.com/Akash54-AS/Sales_Forecasting_For_Demand_Analysis_In_AWS/blob/Dev/Images/Architecture.png)](https://github.com/Akash54-AS)


## Business Scenario
The mid-size company wants to migrate the whole infrastructure to the cloud and it has been decided to use AWS cloud as most of the employees are comfortable working with AWS. The company has various data and jobs that they want to migrate to the cloud but in this scenario, we are only considering sales data. But due to complience and security issues, we still want to have an on-premise data center and daily new data will be sent to AWS. We have to perform migration in such a way that all the business requirements mentioned below should be satisfied with less cost and with the highest optimization possible.

### Business Requirement

✅ Company wants to store sales data in the relational database for running web applications on top of the system. Relational databases can help in supporting high reads and write which will be a feasible solution for supporting web applications.

✅ Company has a machine learning model which is written in the spark to forecast future demand which helps the company to manage their inventory beforehand. They want to migrate this job while keeping costs as minimum as possible and also want to use AWS-managed service to remove the need of managing servers.

✅ Finally, they want to create a dashboard based on forecasted data for analysis so they can make a better business decision, which will indirectly lead to an increase in revenue for the company.

## Solution
