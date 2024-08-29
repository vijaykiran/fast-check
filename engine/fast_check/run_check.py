import pandas as pd
from pprint import pprint

def run_check(check_type, column: str, values, data: pd.DataFrame)-> tuple[pd.DataFrame, pd.DataFrame]:
    # check_types = ['in_list', 'values_in_range']
    if check_type=='in_list':
        query = data[column].isin(values)
    elif check_type=='values_in_range':
        query = data[column].between(values[0], values[1])
    elif check_type=='not_null':
        query = data[column].isnull()
    return (data[query], data[~query])

def get_columns(dataset_path: str)->dict:
    df = pd.read_csv(dataset_path)    
    return {'error_code':0, 'columns': list(df.columns)}

def execute_check(column_name: str, check_type, values, dataset_path: str) -> dict:
    """
    load the dataset from the passed location using azure library.
    """
    df = pd.read_csv(dataset_path)    
    hits, passing = run_check(check_type, column_name, values, df)
    return {'error_code': 0, 'data': {'hits': hits.values.tolist(), 'passing': passing.values.tolist()}}
