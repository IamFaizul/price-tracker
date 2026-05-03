# PricePulse

Intelligent Apple product price tracker with anomaly detection — built for the Bangladeshi market.

## Problem Statement

Buying an Apple product in Bangladesh means manually checking Startech, Ryans, and multiple other sellers every day. Prices change without notice. PricePulse automates this — tracking 79+ Apple products across multiple sellers and flagging unusual price movements using an unsupervised ML model.

## Live Demo

- Dashboard: [PricePulse](#)
- API Docs: https://price-tracker-production-1583.up.railway.app/docs

## Architecture

Startech + Ryans → Scraper → SQLite DB → PyTorch Autoencoder → FastAPI → Lovable Dashboard

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python + BeautifulSoup | Web scraping |
| SQLite | Price history storage |
| PyTorch | Anomaly detection model |
| FastAPI | REST API |
| APScheduler | Automated scraping |
| Lovable | Dashboard frontend |
| Railway | API deployment |

## Model Performance

- Approach: Unsupervised autoencoder — no labeled anomaly data needed
- Precision: 1.000
- Recall: 0.904
- Threshold: 0.213 (mean + 3 standard deviations of reconstruction error)

## Local Setup

    git clone https://github.com/IamFaizul/price-tracker
    cd price-tracker
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python -m scripts.run_scraper
    python -m src.model.train
    uvicorn src.api.main:app --reload

## Project Structure

    src/
    scraper/     - BeautifulSoup scrapers
    db/          - SQLite models
    model/       - PyTorch autoencoder
    api/         - FastAPI endpoints
    scheduler.py - APScheduler

## Limitations and Future Work

- Anomaly evaluation uses synthetic injection — no real labeled data available
- JavaScript-rendered sites like Apple Gadgets BD not yet supported — requires Selenium
- Email or SMS notification not yet implemented
- Currently tracks MacBook, iPhone, iPad, iMac, Apple Watch, AirPods, Mac Mini