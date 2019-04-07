import os
import re

import pandas as pd
import numpy as np


def load_data(path, aggregate=True):
    train_csv_path = os.path.join(path, "train.csv")
    test_csv_path = os.path.join(path, "test.csv")
    train_data, test_data = pd.read_csv(train_csv_path), pd.read_csv(test_csv_path)
    attributes = train_data.columns.tolist()
    
    target = ['Cover_Type']
    categorical_attributes = ['Soil_Type', 'Wilderness_Type']
    attributes = train_data.columns.tolist()
    one_hot_columns = []
    for categorical_attribute in ['Soil_Type', 'Wilderness_Area']:
        one_hot_columns += train_data.loc[:, train_data.columns.str.startswith(categorical_attribute)].columns.tolist()
  
    numerical_attributes = np.setdiff1d(attributes, one_hot_columns + target + ["Id"]).tolist()

    # outliers removal
    first_quantiles = train_data[numerical_attributes].quantile(0.25)
    third_quantiles = train_data[numerical_attributes].quantile(0.75)

    outlier_ids = []

    for idx, numerical_attribute in enumerate(numerical_attributes):
        first_quantile = first_quantiles[numerical_attribute]
        third_quantile = third_quantiles[numerical_attribute]

        iqr = third_quantile - first_quantile

        without_outlier_df = train_data[train_data[numerical_attribute] > first_quantile - 1.5*iqr]
        without_outlier_df = without_outlier_df[without_outlier_df[numerical_attribute] < third_quantile + 1.5*iqr]

        outliers = train_data[~train_data.isin(without_outlier_df).all(1)]
        outlier_ids += outliers['Id'].values.tolist()
    
    if aggregate:
        train_data_aggregated = aggregate_categorical_column(train_data, "Soil")
        train_data_aggregated = aggregate_categorical_column(train_data_aggregated, "Wilderness")

        test_data_aggregated = aggregate_categorical_column(test_data, "Soil")
        test_data_aggregated = aggregate_categorical_column(test_data_aggregated, "Wilderness")
        
        numerical_attributes += categorical_attributes
        
        train_data_without_outliers = train_data_aggregated[~train_data_aggregated['Id'].isin(outlier_ids)]
    else:       
        categorical_attributes = one_hot_columns
        train_data_without_outliers = train_data[~train_data['Id'].isin(outlier_ids)]
        
    return {
        "train_data": train_data_without_outliers,
        "test_data": test_data,
        "attributes": attributes,
        "categorical_attributes": categorical_attributes,
        "numerical_attributes": numerical_attributes,
        "target": target
    }

def aggregate_categorical_column(df, column_name_starts_with):
    column_attributes = [attribute for attribute in df.columns.tolist() if column_name_starts_with in attribute]
    column_decoded = df[column_attributes].idxmax(1)
    column_decoded = column_decoded.apply(lambda x: int(re.match(".*_.*(\d+)", x).group(1)))
    df = df.drop(columns=column_attributes)
    df[column_name_starts_with + "_Type"] = column_decoded

    return df
