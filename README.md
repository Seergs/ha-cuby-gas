# Cuby Gas Sensor Integration for Home Assistant

Custom integration for Cuby LP Gas Sensor

## Features

- Monitor LP gas levels from you Cuby gas sensor
- Real-time updates from the Cuby cloud API
- Easy configuration through Home Assistant UI

## Installation

### HACS (Recommended)

1. Add this repository as a custom repository in HACS:
    1. Open HACS
    2. Go to Integrations
    3. Click the three dot menu (top right)
    4. Select "Custom repositories"
    5. Add repository URL: https://github.com/seergs/ha-cuby-gas
    6. Category: Integration
    7. Click "Add"
2. Find "Cuby Gas Sensor" in HACS and click "Download"
3. Restart Home Assistant

## Configuration

1. Go to Settings -> Devices & Services
2. Click "+ Add Integration"
3. Search for "Cuby Gas Sensor"
4. Enter your credentials:
    - **Email**: Your Cuby account email
    - **Password**: Your Cuby account password
    - **Device ID**: Found in the Cuby mobile app
5. Click Submit

## Entities

This integration creates the following entity:

- **Gas Level Sensor**: Shows the current LP gas level from your Cuby sensor

## Requirements

- Active Cuby account
- Cuby gas sensor registered in the Cuby app
- Internet connection (uses Cuby cloud API)
