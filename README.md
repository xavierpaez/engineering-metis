# Understanding Organizations Exempt from Income Tax
Deep dive on IRS Form 990 - Engineering Final Project

## Abstract
The idea of this project is facilitate access and straightforward visualization to the IRS Form 990 Data. This open data will to help nonprofits and nonprofit watch dog organizations have a the neccesary tools for driving impact.

Open 990 data allows nonprofit executives, policymakers, and the general public to understand trends in the field as well as to understand other nonprofits.

This data also helps donos in making more informed decisions by providing them with information on nonprofit missions, funding, governance, etc.

## Design
The workflow of this project consist on executing a pipeline that starts by connecting to BigQuery, then fetching the data for different years, and storing the results in a Postgres database. Once the data is stored, on a separate process, Streamlit and Pandas will be used to manipulate the data.

## Data

The data for this project was store in Google Big Query data warehouse.
This query combines IRS-990 filings and EIN data to list organizations that filed exempt status in 2015, 2016 and 2017.

For this project features as Revenue, Contributions, Total Expenses, Number of Employees, among other were used.

## Tools
* Big Query API Client
* PostgreSQL - Open Source Database
* SQLAlchemy - Python SQL toolkit and Object Relational Mapper
* Psycopg2 - PostgreSQL Databse Adapter for Python
* Pandas for Data Processing
* Streamlit for app deployment and dashboard
* Altair: Declarative Visualization in Python

## Communication

To view presentation [click here](https://docs.google.com/presentation/d/1uTkV4bE-jwWjWFNgFJukmwWgwIeSmfvi3u6hLmycmiw/edit?usp=sharing).

