Datasets Comparison & Visualization

This project provides tools to **compare and visualize structured datasets**, including CSV files and NetCDF files. It supports both CLI-based and basic GUI-based interactions to help in dataset analysis.

---
Project Structure

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

How To Run

1. Install Dependencies

```bash
pip install -r requirements.txt
```

2. Launch the UI

```bash
python UI.py
```

