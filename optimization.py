import numpy as np
import pandas as pd
import torch

def get_closest_train_sample(target, df_train, verbose=False):
    min_dist, min_config = 1000, -1
    best_match = None
    for c in np.unique(df_train.config_id.values):
        candidate = df_train[df_train.config_id == c]
        match = pd.merge(candidate, target, on=['LoadCase', 'Moment'], how='inner', suffixes=['_candidate', '_target'])
        dist = np.abs((match['y_ROM_candidate'] - match['y_ROM_target']).mean())
        if dist < min_dist:
            min_dist = dist
            min_config = c
            best_match = match

    if verbose:
        print("Closest configuration and distance:", min_config, min_dist)

    return best_match.iloc[0]

def get_rand_train_sample(target, df_train, verbose=False):
    rand_config_id = np.random.choice(df_train.config_id.values)
    candidate = df_train[df_train.config_id == rand_config_id]
    match = pd.merge(candidate, target, on=['LoadCase', 'Moment'], how='inner', suffixes=['_candidate', '_target'])
    dist = np.abs((match['y_ROM_candidate'] - match['y_ROM_target']).mean())

    if verbose:
        print("Random configuration and distance:", rand_config_id, dist)

    return match.iloc[0]

def get_rand_features(params_columns):
    rand = pd.Series(np.random.sample(len(params_columns)), index=params_columns)
    return rand

def out_of_range_loss(tensor, bound='both', norm='L1', reduction='mean', bound_value=None):
    result = 0
    if bound in ['both', 'positive']:
        bound_value = 1 if bound_value is None else bound_value
        if norm == 'L1':
            result += torch.abs(torch.clamp(tensor, max=bound_value) - tensor)
        elif norm == 'L2':
            result += torch.pow(torch.clamp(tensor, max=bound_value) - tensor, 2)
    if bound in ['both', 'negative']:
        bound_value = 0 if bound_value is None else bound_value
        if norm == 'L1':
            result += torch.abs(torch.clamp(tensor, min=bound_value) - tensor)
        elif norm == 'L2':
            result += torch.pow(torch.clamp(tensor, min=bound_value) - tensor, 2)
    if reduction == 'mean':
        result = torch.mean(result)
    elif reduction == 'sum':
        result = torch.sum(result)
    return result

