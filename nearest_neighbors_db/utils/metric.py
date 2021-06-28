import numpy as np

def compute_metric(keys, query, comparator):
    '''
    return score of query. low scores are better. metric does not necessarily follow triangle inequality
    and is thus not a true metric.
    '''
    if comparator == "cosine":
        '''
        general formula for cosine metric is
        (a*b)/(|a|*|b|)
        '''
        return 1 - (keys @ query) / np.linalg.norm(keys, axis=1)
    elif comparator == "inner":
        '''
        general formula for inner metric is
        (a*b)
        '''
        return - keys @ query
    elif comparator == "euclid":
        '''
        euclidian distance means (a-b)^2 = a^2 - 2ab + b^2
        '''
        return np.sqrt(np.linalg.norm(keys, axis=1) - 2*keys@query + query@query)
    else:
        raise ValueError("allowed comparators include `cosine, inner`")
