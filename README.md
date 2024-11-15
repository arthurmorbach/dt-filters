# Transfer Function Visualization App

This project provides a **Transfer Function Visualization Tool** built with Python, using **Streamlit** for the user interface. It includes tools to calculate and analyze the frequency response of different filter types, plot magnitude responses, and manage transfer function data in a database.

## Features

- **Standalone and Capacitor Bank Analysis**:
  - Analyze standalone transfer functions or capacitor bank configurations.
- **Filter Types Supported**:
  - 4/4 Band-Pass Filter (BPF44)
  - 4/8 Band-Pass Filter (BPF48)
  - 4/8 Band-Pass Filter with Cross-Coupling (BPF48CC)
- **Interactive Input**:
  - Adjust parameters like capacitance, sampling frequency, and gain dynamically.
- **Database Integration**:
  - Save, delete, and visualize transfer functions stored in a SQLite database.
- **Dynamic Plots**:
  - Generate interactive plots of magnitude responses with detailed information annotations.

---

## Files in the Project

### 1. `tfVisualizationApp.py`
This is the main application file:
- Provides a user-friendly interface via Streamlit.
- Supports both standalone transfer function calculations and capacitor bank visualizations.
- Plots magnitude responses interactively.
- Integrates with the database to manage transfer functions.

### 2. `filters.py`
Contains core functions for computing the transfer functions:
- **Supported Filters**:
  - BPF44
  - BPF48
  - BPF48CC
- Uses numerical methods to calculate frequency responses and related parameters.

### 3. `create_db.py`
Defines the database structure and ORM configuration:
- Uses SQLAlchemy to manage a SQLite database.
- Stores transfer function data, including parameters and calculation results.

---

## How to Run

1. **Install Dependencies**:
   - Install the required Python packages using the following command:
     ```bash
     pip install -r requirements.txt
     ```

2. **Start the App**:
   - Run the Streamlit application:
     ```bash
     streamlit run tfVisualizationApp.py
     ```

3. **Usage**:
   - Open the provided URL in your browser.
   - Choose filter types and parameters in the sidebar.
   - Click **Generate** to view the magnitude response.
   - Save or delete transfer functions from the database.

---

## Database Structure

The project uses a SQLite database to store transfer function data. Key columns include:
- `tf_name`: Transfer function name.
- `filter_type`: Type of filter used (e.g., BPF44, BPF48, BPF48CC).
- `Cr`, `Ch`: Capacitance values.
- `fs`: Sampling frequency.
- `beta`: Gain factor (for BPF48CC).
- `fc`: Center frequency.
- `Zo`: Impedance.
- `time`: Timestamp of creation.

---

## Requirements

- Python 3.8 or later
- Dependencies listed in `requirements.txt`:
  - `streamlit`
  - `numpy`
  - `pandas`
  - `plotly`
  - `sqlalchemy`

---

## License

This project is licensed under the MIT License.

---

## Author

**Arthur Morbach**

