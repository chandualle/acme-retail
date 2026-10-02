# Acme Retail Data Platform

A production-style data engineering project built on Google Cloud.

## Objective

Build a reliable data pipeline that ingests customer,
product, store, order, payment, and inventory data
and produces analytics-ready datasets in BigQuery.

## Technology

- Python
- SQL
- Google Cloud Storage
- BigQuery
- Dataflow
- Pub/Sub
- Cloud Composer / Airflow
- Terraform
- GitHub

## Architecture

Source Systems
    ↓
Cloud Storage
    ↓
BigQuery RAW
    ↓
STAGING
    ↓
ANALYTICS
    ↓
BI / Analytics