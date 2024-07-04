# ccClub InvestmentProject

A project to realize our investment strategy

### Motivation
"Domestic ETF component stocks are periodically rebalanced based on selection logic. Investors can anticipate these changes and use the same logic to select high-quality, high-dividend stocks as entry targets."
### Developer
* Samantha
* Nina
* Sola
* Aila

# Project Structure
<img width="759" alt="截圖 2024-07-04 08 48 03" src="https://github.com/ccClub-Investment-Project/ccClub_InvestmentProject/assets/71652287/2d683b02-c2b5-4ca9-9ac2-20f5c68e97d3">

# ETFExplorer (Deploy on Render)

[Demo Website](https://ccclub-investmentproject-9ika.onrender.com/)

[Demo API](https://backtest-kk2m.onrender.com/apidocs/)

<img width="1410" alt="截圖 2024-07-04 11 02 39" src="https://github.com/ccClub-Investment-Project/ccClub_InvestmentProject/assets/71652287/d148ddef-1ff6-4e68-8a58-ea198086a878">

<img width="1408" alt="截圖 2024-07-04 11 04 49" src="https://github.com/ccClub-Investment-Project/ccClub_InvestmentProject/assets/71652287/15b13051-3b0a-44ca-8a09-defd3e58bb2d">




> Note: Render periodically resets the SQL database, which may cause the demo to fail.

# ETFLinebot (Deploy on Render)

<img width="680" alt="截圖 2024-07-04 11 57 01" src="https://github.com/ccClub-Investment-Project/ccClub_InvestmentProject/assets/71652287/3bb66b9f-10e7-446d-8a7b-b84b72dc3dd1">
<br>
<img width="268" alt="截圖 2024-07-04 09 15 37" src="https://github.com/ccClub-Investment-Project/ccClub_InvestmentProject/assets/71652287/06aeb0f0-c79a-4dd2-af26-bfdd5cc4d630">


> Note: Render's free plan includes periodic sleeping, causing delayed responses. We use a cron job to wake up the website and Line bot every ten minutes. If inactive, this may lead to server dormancy.

# APIs Used in Project

## Data Collection and Processing
- **yfinance**
- **selenium**
- **beautifulsoup4**
- **requests**
- **pandas**
- **twstock**
- **matplotlib**
- **lxml**

## Database Integration
- **postgreSQL**
- **sqlalchemy**
- **psycopg2**

## Web Frameworks and Tools
- **flask**
- **gunicorn**
- **python-dotenv**
- **flasgger**
- **line-bot-sdk**
- **flask_caching**

## Financial and Trading Tools
- **backtrader**

## Web Scraping and API Interaction
- **requests**

## Asynchronous Task Management
- **celery**
- **redis**

# Development Environment (not for deploy)
## Install Docker (Windows, Linux, macOS)

Run the following command in the project directory to create containers:
- **dev_env**: Virtual Environment: ccclub
- **crawler**: For web scraping
```bash
docker compose up --build -d
```
## IDE: VScode
1. Launch VS Code.
2. Open the command palette:
   - **Windows/Linux**: Ctrl+Shift+P
   - **macOS**: Shift+Command+P
3. Type and select Dev Containers: Attach to Running Container....
4. From the list, choose your `dev_env` container.
## IDE: Jupyter Lab Desktop
1. Copy the script from the `docker/scripts` folder to your desired location:
   - **Windows**: Copy `open_jupyterlab.bat`
   - **macOS/Linux**: Copy `open_jupyterlab.sh`

2. Execute the script by running:
   - **Windows**:
     ```cmd
     open_jupyterlab.bat
     ```
   - **macOS/Linux**:
     ```sh
     sh open_jupyterlab.sh
     ```
