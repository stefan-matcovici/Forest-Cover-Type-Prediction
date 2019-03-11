def outliers_statistics(outliers_ids):
    import scipy.io
    
    mat = scipy.io.loadmat('../data/cover.mat')
    
    outliers_mapping = zip(mat["X"][:, 0], mat["y"][:, 0])
    
    entry_ids_mapping = {
        "outliers_ids": [id for id, is_outlier in outliers_mapping if is_outlier],
        "non_outliers_ids": [id for id, is_outlier in outliers_mapping if not is_outlier]
    }
    
    TP = len(set(entry_ids_mapping["outliers_ids"]) & set(outliers_ids))
    FP = len(set(entry_ids_mapping["non_outliers_ids"]) & set(outliers_ids))
    FN = len(set(entry_ids_mapping["outliers_ids"]) - set(outliers_ids))
    
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