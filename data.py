import math
import pandas as pd

FEATURES = ['LoadCase', 'Moment', 'C10Nucleus', 'C01Nucleus', 'C10Annulus', 'K1Annulus', 'K2Annulus', 'Kappa', 
                    'K1Circ', 'K2Circ', 'K1Rad', 'K2Rad', 'FiberAngle', 'FiberAngleCirc', 'FiberAngleRad']

def load_df(input_file, output_files):
    input_config = pd.read_csv(input_file)

    # open and parse load cases files
    cases = list()
    for i, load_case in enumerate(output_files):
        rom_df = read_output_table(pd.read_csv(load_case['ROM']), "ROM")
        idp_df = read_output_table(pd.read_csv(load_case['IDP']), "IDP")

        # create a single df for both input and output
        output_df = pd.merge(rom_df, idp_df, on=['config_id', 'Moment'])
        df = output_df.join(input_config, on=['config_id'])

        # add case id column
        df['LoadCase'] = i

        # remove rows in which one of the outputs is zero
        df = df[(df['y_IDP'] != 0) & (df['y_ROM'] != 0)]

        cases.append(df)

    # concat all load cases
    df = pd.concat(cases, axis='rows', ignore_index=True)

    return df
    

def normalize_columns(df, column_bounds, train=True, keep_target=False):    
    # add boundaries for moments outputs etc. when training.
    # in test, we read the bounderies from file
    if train:
        column_bounds.index = ['min', 'max']
        column_bounds['Moment'] = [df.Moment.min(), df.Moment.max()]
        rom_max = math.ceil(df.y_ROM.max() + 1)
        column_bounds['y_ROM'] = [0, rom_max]
        column_bounds['y_IDP'] = [-1, 1]
        loadcase_max = math.ceil(df.LoadCase.max()) if 'LoadCase' in df.columns else 0
        column_bounds['LoadCase'] = [0, loadcase_max]

    # normalize columns for which bounds are defined
    common_columns = df.columns.intersection(column_bounds.columns)
    for column in common_columns:
        df[column] = (df[column] - column_bounds[column]['min']) / (column_bounds[column]['max'] - column_bounds[column]['min'])
    
    columns_order = FEATURES
    
    if train or keep_target:
        columns_order = ['config_id'] + columns_order + ['y_ROM', 'y_IDP']

    df = df[[c for c in columns_order if c in df.columns]]

    if train:
        return df, column_bounds
    else:
        return df

def denormalize_columns(df, column_bounds, also_target=False):
    df_denrom = df.copy()
    common_columns = df.columns.intersection(column_bounds.columns)

    # remove y_ROM from common columns
    if not also_target:
        common_columns = common_columns.drop('y_ROM')

    for column in common_columns:
        df_denrom[column] = df_denrom[column] * (column_bounds[column]['max'] - column_bounds[column]['min']) + column_bounds[column]['min']

    if also_target:
        for column in df.columns:
            if column not in common_columns and 'y_ROM' in column:
                df_denrom[column] = df_denrom[column] * (column_bounds['y_ROM']['max'] - column_bounds['y_ROM']['min']) + column_bounds['y_ROM']['min']

    return df_denrom

def read_output_table(table, output_name):
    df = table.copy()
    
    # remove moment of zero from the output table
    for zero in ["0", "0.0"]:
        if zero in df.columns:
            df.drop(columns=[zero], inplace=True)
            break

    # create an output column
    df = df.melt(var_name='Moment', value_name="y_" + output_name, ignore_index=False)
    df['Moment'] = df['Moment'].astype(float)

    # keep the original configuration id
    df.reset_index(names="config_id", inplace=True)

    return df
