# System Health Utility - Basic Instructions
Deployed at [https://udi-ta.github.io/System_health_check/#](https://udi-ta.github.io/System_health_check/#)

This document provides basic instructions on how to run the System Health Utility on your system. This version requires running the utility directly from the Python source code.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Python 3:** The utility is written in Python 3. You can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* **pip:** Pip is the package installer for Python. It usually comes bundled with Python installations. You can check if you have it by opening your terminal or command prompt and running `pip --version`. If not installed, follow the instructions on the pip website: [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/)

## Installation (Running from Source)

1.  **Download and Extract:**
    * Download the `system-health-utility.zip` file (available from the project website).
    * Extract the contents of the zip file to a location on your computer. You should find a folder named `system-health-utility` containing `main.py`, `config.ini`, and `requirements.txt`.

2.  **Install Dependencies:**
    * Open your terminal (macOS/Linux) or command prompt (Windows) and navigate into the extracted `system-health-utility` folder.
    * Run the following command to install the necessary Python libraries:
        ```bash
        pip install -r requirements.txt
        ```
        (The `requirements.txt` file in this folder lists the dependencies: `psutil`, `schedule`, `requests`.)

## Configuration (Dummy API)

In this initial version, the utility is configured to use a **dummy API endpoint**. You **do not need to configure** the `api_endpoint` in the `config.ini` file. The utility will still attempt to send data to this dummy endpoint (which won't store it), allowing you to test the functionality of the utility itself.

You can still adjust the `reporting_interval_minutes` in the `config.ini` file to control how frequently the utility checks your system health.

## Running the Utility in the Background (as a daemon)

Once the dependencies are installed, you can run the utility in the background.

**macOS/Linux:**

* Navigate to the `system-health-utility` folder in your terminal and run:
    ```bash
    nohup python main.py &
    ```
    This will run the utility in the background. You can check if it's running using `ps aux | grep "python main.py"`. To stop it, find the process ID (PID) and use `kill <PID>`.

**Windows:**

* Open Command Prompt or PowerShell, navigate to the `system-health-utility` folder, and run:
    ```bash
    start python main.py
    ```
    This will open a new console window for the utility running in the background. You can close the terminal you used to start it. To stop it, find the Python process in Task Manager and end it.

## Backend Status

Please be aware that the backend server (API and storage) for this project is currently under development. The utility in this version is configured to send data to a dummy API endpoint for testing purposes. Real-time data display and historical data will be available once the backend is complete.
