# Red Team Authorized Load Testing Dashboard

This is a complete Streamlit dashboard that orchestrates load tests using Locust in headless mode and visualizes the results.

⚠️ **Disclaimer:** This tool is strictly for authorized testing on infrastructure you own or control. Do not implement any DDoS or attack logic.

## Features
- **Configure load-test parameters:** Target URL, Concurrent users, Spawn rate, Duration, Think time, Request paths.
- **Run Locust in headless mode:** Executes test processes in the background securely.
- **Collect CSV outputs:** Automatically stores metrics.
- **Visualize performance:** Plots Requests per Second (RPS), error rates, and response time percentiles.
- **Compare multiple runs:** Overlay charts to compare two different load tests.

## Requirements

The project requires the following Python libraries:
- `streamlit`
- `locust`
- `pandas`
- `matplotlib`

## Installation

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

2. Install the required dependencies:
```bash
pip install streamlit locust pandas matplotlib
```

## Running the Dashboard

Start the Streamlit application by running the following command in your terminal:
```bash
streamlit run app.py
```

This will launch the dashboard in your default web browser.

## How to Use
1. **Configure Parameters:** Use the sidebar on the left to set up your test (Target URL, Users, Rates, etc.).
2. **Run Test:** Click "Run Test" to start executing Locust in headless mode.
3. **Monitor Live Dashboard:** Wait for the dashboard to automatically refresh and populate metrics and charts.
4. **Compare Past Runs:** Switch to the "Compare Past Runs" tab to evaluate previous benchmarks against each other.
