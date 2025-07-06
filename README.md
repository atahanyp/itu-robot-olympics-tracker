# ITU Robot Olympics - Match Tracker

A live match tracking and display system for ITU Robot Olympics (Mini Sumo & Pul Toplayan categories).  
Includes a Python backend for data processing, a desktop GUI, and a web interface for live match display.

## Features

- Fetches match data from Google Sheets
- Displays current and upcoming matches
- Supports multiple categories (Mini Sumo, Pul Toplayan)
- Web interface for live display (Flask or similar can be added)
- Simple desktop GUI for local tracking

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Installation

```bash
git clone https://github.com/atahanyp/itu-robot-olympics-tracker.git
cd itu-robot-olympics-tracker
pip install -r requirements.txt
```

## Usage

### Desktop GUI

```bash
python main.py
```

## Project Structure

```
itu-robot-olympics-tracker/
│
├── main.py                 # Desktop GUI entry point
├── gui.py                  # GUI logic
├── match_data.py           # Data fetching and processing
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── pul_toplayan.html
├── static/
│   └── itu-logo.png
└── ...
```

## License

MIT License