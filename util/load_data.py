import os
import re

import pandas as pd
import numpy as np


def load_data(path, aggregate=True):
    train_csv_path = os.path.join(path, "train.csv")
    test_csv_path = os.path.join(path, "test.csv")
    train_data, test_data = pd.read_csv(train_csv_path), pd.read_csv(test_csv_path)

    if aggregate:
        train_data = aggregate_categorical_column(train_data, "Soil")
        train_data = aggregate_categorical_column(train_data, "Wilderness")

        test_data = aggregate_categorical_column(test_data, "Soil")
        test_data = aggregate_categorical_column(test_data, "Wilderness")

        categorical_attributes = ['Soil_Type', 'Wilderness_Type']
    else:
        categorical_attributes = []

    attributes = train_data.columns.tolist()
    target = ['Cover_Type']
    numerical_attributes = np.setdiff1d(attributes, categorical_attributes + target + ["Id"]).tolist()

    return {
        "train_data": train_data,
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
