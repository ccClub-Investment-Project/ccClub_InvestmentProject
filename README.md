# ccClub InvestmentProject

A project to realize our investment strategy

### Motivation
(Provide the motivation behind the project here.)

### Developer
* Samantha
* Nina
* Sola
* Aila

# Project Structure
<img width="759" alt="截圖 2024-07-04 08 48 03" src="https://github.com/ccClub-Investment-Project/ccClub_InvestmentProject/assets/71652287/2d683b02-c2b5-4ca9-9ac2-20f5c68e97d3">

# Deploy to Render
[Demo Website](https://backtest-kk2m.onrender.com/apidocs/)

[Demo API](https://ccclub-investmentproject-9ika.onrender.com/)

# Linebot
<img width="268" alt="截圖 2024-07-04 09 15 37" src="https://github.com/ccClub-Investment-Project/ccClub_InvestmentProject/assets/71652287/06aeb0f0-c79a-4dd2-af26-bfdd5cc4d630">


## Development Environment (not for deploy)
### Install Docker (Windows, Linux, macOS)

Run the following command in the project directory to create containers:
- **dev_env**: Virtual Environment: ccclub
- **crawler**: For web scraping
```bash
docker compose up --build -d
```
### IDE: VScode
1. Launch VS Code.
2. Open the command palette:
   - **Windows/Linux**: Ctrl+Shift+P
   - **macOS**: Shift+Command+P
3. Type and select Dev Containers: Attach to Running Container....
4. From the list, choose your `dev_env` container.
### IDE: Jupyter Lab Desktop
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
