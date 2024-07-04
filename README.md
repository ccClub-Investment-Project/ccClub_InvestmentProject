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
(Provide details about the project structure here.)

# Deploy to Render
(Provide details on how to deploy the project to Render here.)

# Linebot
(Provide details about the Linebot here.)


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