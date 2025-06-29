from typing import Any

import pandas as pd
import numpy as np
from pandas import DataFrame

from open_nc_file import val2val
from cat_sim import jaccard_similarity


from scipy.stats import chi2_contingency, pointbiserialr
from statsmodels.formula.api import ols
import statsmodels.api as sm

df1 = None
df2 = None

col_corr_list = []
def entryPoint(file1, file2, order):
    # Analyze the first CSV file
    columns_file1 = analyze_csv(file1)  # get the column names
    global df1, df2
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    col_result_list, correlation_list = generate_comparison_score(columns_file1, order)

    sum_el = sum(col_result_list)
    elements = len(col_result_list)

    avg = sum_el / elements if elements > 0 else 0

    return avg, correlation_list 



# Function to determine column data type
def find_column_data_type(df, column_name):
    dtype = df[column_name].dtype

    if np.issubdtype(dtype, np.number):  # Numeric (int, float)
        return "Numeric"

    elif pd.api.types.is_categorical_dtype(df[column_name]) or df[column_name].dtype == 'object':
        return "Categorical/String"

    else:
        return "Unknown"


def extract_column_to_list(column_name):
    # Extract the column values into a list
    column_values1 = df1[column_name].tolist()
    column_values2 = df2[column_name].tolist()

    return column_values1, column_values2


# Function to read a CSV file and analyze its columns
def analyze_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Extract column names
    column_names = list(df.columns)

    # Initialize a list to store the data types of each column
    column_data_types = []
    return column_names


def count_unique_values_in_columns(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Use the nunique() method to get the number of unique values for each column
    unique_counts = df.nunique()

    return unique_counts.tolist()


def count_rows_in_csv(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Get the number of rows (excluding the header)
    num_rows = df.shape[0]

    return num_rows


def find_column_range(column_name):
    # Read the CSV file into a DataFrame

    # Calculate the range: max - min for the specified column
    column_min = df1[column_name].min()
    column_max = df1[column_name].max()
    column_range = column_max - column_min
    print("column range  = " + str(column_range))
    return column_range

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, pointbiserialr

def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    if confusion_matrix.size == 0:
        return 0.0
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    if n == 0:
        return 0.0
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

def correlation(col1, col2, column_name="Unknown"):
    s1 = pd.Series(col1).dropna()
    s2 = pd.Series(col2).dropna()

    min_len = min(len(s1), len(s2))
    s1 = s1.iloc[:min_len]
    s2 = s2.iloc[:min_len]

    # Check for constant column
    if s1.nunique() <= 1 or s2.nunique() <= 1:
        print(f"Warning: Column '{column_name}' has constant values. Correlation is undefined. Returning 0.")
        return 0.0

    # Check types
    is_num1 = pd.api.types.is_numeric_dtype(s1)
    is_num2 = pd.api.types.is_numeric_dtype(s2)

    try:
        if is_num1 and is_num2:
            return s1.corr(s2)

        elif not is_num1 and not is_num2:
            return cramers_v(s1, s2)

        elif is_num1 != is_num2:
            # One is numeric, one is categorical → Point Biserial
            cat = s1 if not is_num1 else s2
            num = s2 if not is_num1 else s1

            # Encode categorical
            cat_encoded = pd.Series(pd.factorize(cat)[0])
            result = pointbiserialr(cat_encoded, num)
            return result.correlation if not np.isnan(result.correlation) else 0.0

        else:
            return 0.0
    except Exception as e:
        print(f"Correlation calculation failed for '{column_name}': {e}")
        return 0.0




def generate_comparison_score(cols1, order_matters):
    col_result_list = []
    correlation_list = []

    for col_name1 in cols1:
        print(f"Processing: {col_name1}")
        
        data_type = find_column_data_type(df1, col_name1)
        col1, col2 = extract_column_to_list(col_name1)
        
        # Similarity score
        if data_type == "Numeric":
            col_range = find_column_range(col_name1)
            col_result = val2val(col1, col2, order_matters, len(col1), col_range * 0.1)
        else:
            col_result = jaccard_similarity(col1, col2)

        col_result_list.append(col_result)

        # Correlation score
        corr_score = correlation(col1, col2, column_name=col_name1)
        correlation_list.append(corr_score)

    print("---------------------------------------------------------------------------")
    print("The avg correlation score is:")
    print(sum(correlation_list) / len(correlation_list))
    
    return col_result_list, correlation_list

