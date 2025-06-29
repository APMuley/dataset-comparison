# 📊 Datasets Comparison & Visualization

This project provides tools to **compare and visualize structured datasets**, including CSV files and NetCDF files. It supports both CLI-based and basic GUI-based interactions to help in dataset analysis.

---

## 📁 Project Structure

```
datasets-comparison-visualization/
├── UI.py                  # Simple UI to choose between functionalities
├── cat_sim.py             # Concatenates datasets and compares similarity
├── goodpar.py             # Compares datasets using "good parameter" logic
├── master.py              # Main script that integrates key functionalities
├── open_nc_file.py        # Parses and processes .nc (NetCDF) files
├── visualization_code.py  # Generates visualizations from datasets
├── test_files/            # Sample CSV datasets for testing
│   ├── f1.csv
│   ├── f2.csv
│   ├── output_2011.csv
│   ├── output_2012.csv
│   ├── output_2013.csv
├── requirements.txt       # Required Python libraries
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch the UI

```bash
python UI.py
```

Follow the prompts to select a comparison or visualization task.

---

## 🧰 Available Scripts

### `cat_sim.py`

- Compares the similarity between multiple datasets
- Useful for identifying mismatches or anomalies

### `goodpar.py`

- Implements logic to determine if datasets meet "good parameter" thresholds

### `visualization_code.py`

- Generates charts and plots (e.g., line plots) from multiple CSV files

### `open_nc_file.py`

- Opens `.nc` (NetCDF) files and parses the data for visualization or analysis

---

## 📂 Sample Data

Located in the `test_files/` folder:

- Use `f1.csv`, `f2.csv` or any of the `output_*.csv` files for testing and experimenting with the scripts.

---

## ✅ Requirements

Make sure you have the following Python packages:

```txt
pandas
matplotlib
numpy
netCDF4
```

Install them via:

```bash
pip install -r requirements.txt
```

---

## 📌 Notes

- The current version uses basic I/O via terminal or file selection.
- Visualization is done using `matplotlib`, with plots saved or displayed interactively.
- Designed for educational and exploratory data analysis use cases.

---

## 📜 License

MIT License. See `LICENSE` file if available.

---

## 👤 Author

Developed by [Leevan Herald](https://github.com/leevanherald)
