# Radarr Monitor

A Python script that monitors your Radarr queue and automatically handles failed downloads and XEM mapping issues.

## Features

- Continuously monitors Radarr's download queue
- Automatically handles failed downloads by:
  - Removing failed items from queue
  - Adding them to blocklist
  - Triggering a new search for the movie
- Skips downloads with pending XEM mappings to prevent unnecessary failures
- Configurable check interval

## Requirements

- Python 3.x
- `requests` library
- Running Radarr instance
- Radarr API key

## Installation

1. Clone this repository or download the `radarr-monitor.py` file
2. Install required Python package:
```bash
pip install requests
```

## Configuration

Edit `radarr-monitor.py` and update the following configuration variables at the top of the file:

```python
RADARR_API_URL = "http://192.168.1.3:7878/api/v3"  # Replace with your Radarr instance URL
RADARR_API_KEY = "your_radarr_api_key"             # Replace with your Radarr API key
CHECK_INTERVAL = 60                                 # Adjust check interval (in seconds) if needed
```

To find your Radarr API key:
1. Open Radarr web interface
2. Go to Settings > General
3. Find the API Key under "Security"

## Usage

Run the script using Python:

```bash
python radarr-monitor.py
```

The script will:
1. Check the Radarr queue every 60 seconds (configurable)
2. Process any failed downloads or import-blocked items
3. Skip items with pending XEM mappings
4. Log actions to the console

## How It Works

The script performs the following operations:

1. Queries the Radarr API to get the current download queue
2. For each item in the queue:
   - Checks for pending XEM mappings and skips those items
   - Identifies failed downloads or import-blocked items
   - Removes failed downloads and adds them to the blocklist
   - Triggers a new search for the affected movie

This helps maintain a healthy download queue by automatically handling common issues and retrying failed downloads.

## Note

This is a monitoring tool meant to run continuously. Consider setting it up as a service or using a process manager if you want it to run automatically on system startup.