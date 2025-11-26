# Division Wars Website

Welcome to the Division Wars Website project! This application serves as the central hub for tracking scores, fixtures, and results for the Division Wars event, covering both Sports and Cultural activities.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### 🛠️ Setup Instructions

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd division-wars-website
    ```

2.  **Set up the Virtual Environment**:
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    # Create virtual environment
    python -m venv Backend/venv

    # Activate virtual environment
    # Windows:
    Backend\venv\Scripts\activate
    # macOS/Linux:
    source Backend/venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r Backend/requirements.txt
    ```

## 🏃‍♂️ Running the Application

To start the Streamlit frontend, run the following command from the root directory:

```bash
streamlit run Frontend/app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## 📂 Project Structure

```
division-wars-website/
├── Backend/
│   ├── Cultural/           # Cultural events data
│   │   └── overall_points_table.csv
│   ├── Sports/             # Sports events data and logic
│   │   ├── SportsData/     # CSV files for fixtures, points, results
│   │   └── SportsLogic/    # Python logic for sports (e.g., throwball.py)
│   ├── venv/               # Virtual environment (not in git)
│   └── requirements.txt    # Python dependencies
├── Frontend/
│   └── app.py              # Main Streamlit application
├── .gitignore
└── README.md
```

## 📊 Data Management

The application relies on CSV files located in `Backend/Sports/SportsData` and `Backend/Cultural`.
- **Overall Tables**: `overall_table.csv` (Sports) and `overall_points_table.csv` (Cultural).
- **Sport Specifics**: Naming convention is `[sportname]_fixtures.csv`, `[sportname]_points.csv`, `[sportname]_results.csv`.

**Note**: Ensure all CSV files are saved with **UTF-8 encoding** to avoid errors.

## 🤝 Contribution

1.  Create a new branch for your feature.
2.  Make your changes.
3.  Test locally using `streamlit run Frontend/app.py`.
4.  Push and create a Pull Request.
