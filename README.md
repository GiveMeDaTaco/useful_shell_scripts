# useful_shell_scripts
import pandas as pd

# df is your DataFrame
df = ...
# list of columns for distinct count
count_columns = ['my_column1', 'my_column2']

# conditions and descriptions together in a dictionary
criteria_dict = {
    'Column1 > 0': lambda df: df['column1'] > 0,
    'Column2 != "value"': lambda df: df['column2'] != 'value',
    # add more conditions as needed
}

def apply_conditions(df, criteria_dict, count_columns):
    records_initial = {col: df[col].nunique() for col in count_columns}

    report = pd.DataFrame()

    for count_column in count_columns:
        df_report = pd.DataFrame(columns=pd.MultiIndex.from_product([[count_column], 
                                                                     ['Criteria_Number', 'Logic', 'Description', 'Records_Remaining',
                                                                      'Records_Removed', 'Total_Records_Dropped', 'Records_Not_Dropped', 
                                                                      'Records_After_Step']]))

        records_prev = records_initial[count_column]
        total_dropped = 0

        for i, (description, condition) in enumerate(criteria_dict.items()):
            df_new = df.loc[condition(df)]

            records_new = df_new[count_column].nunique()
            records_removed = records_prev - records_new
            total_dropped += records_removed
            records_not_dropped = records_initial[count_column] - total_dropped
            records_after_step = records_initial[count_column] - total_dropped

            df_report.loc[i] = [(i+1, condition, description, records_new, records_removed, total_dropped,
                                records_not_dropped, records_after_step)]

            records_prev = records_new
            df = df_new

        report = pd.concat([report, df_report], axis=1)

    return report

report = apply_conditions(df, criteria_dict, count_columns)
print(report)
