import os

import pandas as pd


def load_data(path):
    train_csv_path = os.path.join(path, "train.csv")
    test_csv_path = os.path.join(path, "test.csv")
    return pd.read_csv(train_csv_path), pd.read_csv(test_csv_path)
