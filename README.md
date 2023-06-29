import pandas as pd
from typing import List, Dict, Callable

# Initial DataFrame and list of columns for distinct count
df: pd.DataFrame = ...  # Replace with your DataFrame
count_columns: List[str] = ['my_column1', 'my_column2']  # Replace with your list of columns

# Define a dictionary where each key is a string description of a condition and each value is a function (lambda) representing that condition
criteria_dict: Dict[str, Callable[[pd.DataFrame], pd.Series[bool]]] = {
    'Column1 > 0': lambda df: df['column1'] > 0,  # condition 1
    'Column2 != "value"': lambda df: df['column2'] != 'value',  # condition 2
    # Add more conditions as needed
}

def apply_conditions(df: pd.DataFrame, criteria_dict: Dict[str, Callable[[pd.DataFrame], pd.Series[bool]]], count_columns: List[str]) -> pd.DataFrame:
    """
    Applies each condition from criteria_dict to the DataFrame for each column in count_columns and returns a report.

    :param df: The input DataFrame.
    :param criteria_dict: A dictionary where each key is a string description of a condition and each value is a function (lambda) representing that condition.
    :param count_columns: A list of columns to be considered for counting distinct values.
    :return: A report DataFrame that shows the results of applying each condition to each count_column in the input DataFrame.
    """
    df_copy = df.copy()  # make a copy of the input DataFrame to avoid modifying original data

    # Calculate the initial number of unique values for each count column
    records_initial: Dict[str, int] = {col: df_copy[col].nunique() for col in count_columns}

    # This list will hold the report rows
    report_data: List[Dict] = []

    # Loop through each condition
    for i, (description, condition) in enumerate(criteria_dict.items()):
        # Apply condition and get the filtered DataFrame
        df_copy = df_copy.loc[condition(df_copy)]

        # Initialize dictionary to hold total dropped records for each count column
        total_dropped: Dict[str, int] = {col: 0 for col in count_columns}

        # Loop through each count column
        for count_column in count_columns:
            # Calculate number of unique values after applying condition
            records_new: int = df_copy[count_column].nunique()
            # Calculate number of records removed by this condition
            records_removed: int = records_initial[count_column] - records_new
            # Update total dropped records
            total_dropped[count_column] += records_removed
            # Calculate number of records not dropped
            records_not_dropped: int = records_initial[count_column] - total_dropped[count_column]
            # Calculate number of records remaining after all steps
            records_after_step: int = records_initial[count_column] - total_dropped[count_column]

            # Prepare a dictionary for the report row and add it to the list
            report_data.append({'Count_Column': count_column, 
                                'Criteria_Number': i+1, 
                                'Description': description, 
                                'Records_Remaining': records_new, 
                                'Records_Removed': records_removed, 
                                'Total_Records_Dropped': total_dropped[count_column], 
                                'Records_Not_Dropped': records_not_dropped, 
                                'Records_After_Step': records_after_step})

    # Convert the list of dictionaries to a DataFrame
    final_report: pd.DataFrame = pd.DataFrame(report_data)

    # Ensure Criteria_Number is integer type
    final_report['Criteria_Number'] = final_report['Criteria_Number'].astype(int)

    return final_report

report = apply_conditions(df, criteria_dict, count_columns)
print(report)
