import pandas as pd
from typing import List, Dict, Callable

# Initial DataFrame and list of columns for distinct count
df: pd.DataFrame = ...  # Replace with your DataFrame
count_columns: List[str] = ['my_column1', 'my_column2']  # Replace with your list of columns

# Define a dictionary where each key is a string description of a condition and each value is a function (lambda) representing that condition
criteria_dict: Dict[str, Callable[[pd.DataFrame], pd.Series]] = {
    'Column1 > 0': lambda df: df['column1'] > 0,  # condition 1
    'Column2 != "value"': lambda df: df['column2'] != 'value',  # condition 2
    # Add more conditions as needed
}

def apply_conditions(df: pd.DataFrame, criteria_dict: Dict[str, Callable[[pd.DataFrame], pd.Series]], count_columns: List[str]) -> pd.DataFrame:
    """Applies each condition from criteria_dict to the DataFrame for each column in count_columns and returns a report."""
    
    all_reports: List[pd.DataFrame] = []  # Initialize list to hold reports for each count column

    # Loop through each count column
    for count_column in count_columns:
        # Calculate the initial number of unique values for the count column
        records_initial: int = df[count_column].nunique()
        total_dropped: int = 0  # Initialize total dropped records
        records_prev: int = records_initial  # Set previous records number to initial number

        # Initialize DataFrame to hold report for this count column
        report: pd.DataFrame = pd.DataFrame(columns=['Count_Column', 'Criteria_Number', 'Description', 'Records_Remaining',
                                                     'Records_Removed', 'Total_Records_Dropped', 'Records_Not_Dropped', 
                                                     'Records_After_Step'])

        # Loop through each condition
        for i, (description, condition) in enumerate(criteria_dict.items()):
            df_new: pd.DataFrame = df.loc[condition(df)].copy()  # Apply condition and make a copy of the filtered DataFrame

            # Calculate number of unique values after applying condition
            records_new: int = df_new[count_column].nunique()
            # Calculate number of records removed by this condition
            records_removed: int = records_prev - records_new
            # Update total dropped records
            total_dropped += records_removed
            # Calculate number of records not dropped
            records_not_dropped: int = records_initial - total_dropped
            # Calculate number of records remaining after all steps
            records_after_step: int = records_initial - total_dropped

            # Add this row to the report
            report.loc[i] = [count_column, i+1, description, records_new, records_removed, 
                             total_dropped, records_not_dropped, records_after_step]

            records_prev = records_new  # Update previous records number to current number

        # Ensure Criteria_Number is integer type
        report['Criteria_Number'] = report['Criteria_Number'].astype(int)

        all_reports.append(report)  # Add this report to the list of all reports

    final_report: pd.DataFrame = pd.concat(all_reports, ignore_index=True)  # Concatenate all reports into one DataFrame

    return final_report

report = apply_conditions(df, criteria_dict, count_columns)
print(report)
