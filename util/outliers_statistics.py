def outliers_statistics(train_data, outliers_ids):
    entry_ids_mapping = {
        "outliers_ids": train_data[train_data['target'] == 1].index.values.tolist(),
        "non_outliers_ids": train_data[train_data['target'] == 0].index.values.tolist()
    }
 
    TP = len(set(entry_ids_mapping["outliers_ids"]) & set(outliers_ids))
    FP = len(set(entry_ids_mapping["non_outliers_ids"]) & set(outliers_ids))
    FN = len(set(entry_ids_mapping["outliers_ids"]) - set(outliers_ids))
    
    print("TP: " + str(TP))
    print("FP: " + str(FP))
    print("FN: " + str(FN))
    
    if TP + FP > 0:
        precision = TP / (TP + FP)
    else:
        precision = 1
    
    if TP + FN > 0:
        recall = TP / (TP + FN)
    else:
        recall = 1
        
    F1_score = 2 * (precision * recall) / (precision + recall)
    
    return precision, recall, F1_score