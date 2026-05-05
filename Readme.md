# PricePulse

Intelligent Apple product price tracker with AI-powered anomaly detection — built for the Bangladeshi market.

## Problem Statement

Buying an Apple product in Bangladesh means manually checking multiple sellers every day. Prices change without notice. PricePulse automates this — tracking 150+ Apple products across 3 Bangladeshi retailers and flagging unusual price movements using an unsupervised ML model.

## Live Demo

- Dashboard: https://cost-insight-station.lovable.app
- API Docs: https://price-tracker-production-1583.up.railway.app/docs

## Features

- Real-time price tracking across Startech, Apple Gadgets BD, and Dazzle
- AI-powered anomaly detection using PyTorch autoencoder
- Buy/Wait recommendation based on price history
- Price volatility indicator
- Competitor price comparison
- Telegram alerts when unusual price movements are detected
- Automated daily scraping via GitHub Actions

## Architecture

Startech + Apple Gadgets BD + Dazzle → Scraper → SQLite DB → PyTorch Autoencoder → FastAPI → Lovable Dashboard

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python + BeautifulSoup | Static site scraping |
| Playwright | JavaScript-rendered site scraping |
| SQLite | Price history storage |
| PyTorch | Anomaly detection model |
| FastAPI | REST API |
| GitHub Actions | Automated daily scraping |
| Telegram Bot API | Price anomaly alerts |
| Lovable | Dashboard frontend |
| Railway | API deployment |

## Model Performance

- Approach: Unsupervised autoencoder — no labeled anomaly data needed
- Precision: 1.000
- Recall: 0.904
- Threshold: 0.213 (mean + 3 standard deviations of reconstruction error)

## API Endpoints

- GET /products — all tracked products
- GET /price-history/{id} — price history with date filter
- GET /anomalies/recent — recent anomalies
- GET /price-changes/{id} — price change frequency
- POST /detect-anomaly — manual anomaly detection

## Local Setup

    git clone https://github.com/IamFaizul/price-tracker
    cd price-tracker
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python -m playwright install chromium
    python -m scripts.run_scraper
    python -m src.model.train
    uvicorn src.api.main:app --reload

## Project Structure

    src/
    scraper/     - BeautifulSoup + Playwright scrapers
    db/          - SQLite models
    model/       - PyTorch autoencoder
    api/         - FastAPI endpoints
    scheduler.py - APScheduler

## Data Collection

Price data collected daily from publicly accessible product listing pages of Bangladeshi electronics retailers for portfolio demonstration purposes. Data collection period: 7 days.

## Disclaimer

Price data is scraped from publicly accessible pages for educational and portfolio demonstration purposes only. Some anomalies shown in the dashboard are synthetically injected for demonstration. This tool is not affiliated with any retailer. Do not make purchasing decisions based solely on this data.

## Limitations and Future Work

- Ryans.com not included due to Cloudflare bot protection
- Anomaly evaluation uses synthetic injection — no real labeled data available
- Email or SMS notification not yet implemented
- User accounts and personalized alerts not yet implemented