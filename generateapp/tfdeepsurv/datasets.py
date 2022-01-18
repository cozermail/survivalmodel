"""Survival dataset preview or pre-processing functionality.
"""
import pandas as pd
from sklearn.model_selection import ShuffleSplit

from .vision import plot_km_survf
from .simulator import SimulatedData


def survival_stats(data, t_col="t", e_col="e", plot=False):
    """
    Print statistics of survival data.

    Parameters
    ----------
    data: pandas.DataFrame
        Survival data you specified.
    t_col: str
        Column name of data indicating time.
    e_col: str
        Column name of data indicating events or status.
    plot: boolean
        Whether plot survival curve.
    """
    # print("# --------------- Survival Data Statistics ---------------")
    # N = len(data)
    # print("# Rows:", N)
    # print("# Columns: %d + %s + %s" % (len(data.columns) - 2, e_col, t_col))
    # print("# Event Percentage: %.2f%%" % (100.0 * data[e_col].sum() / N))
    # print("# Min Time:", data[t_col].min())
    # print("# Max Time:", data[t_col].max())
    # print("")
    if plot:
        plot_km_survf(data, t_col=t_col, e_col=e_col)

def survival_df(data, t_col="t", e_col="e", label_col="Y", exclude_col=[]):
    """
    Transform original DataFrame to survival dataframe that would be used in model 
    training or predicting.

    Parameters
    ----------
    data: DataFrame
        Survival data to be transformed.
    t_col: str
        Column name of data indicating time.
    e_col: str
        Column name of data indicating events or status.
    label_col: str
        Name of new label in transformed survival data.
    exclude_col: list
        Columns to be excluded.

    Returns
    -------
    DataFrame:
        Transformed survival data. Negtive values in label are taken as right censored.
    """
    x_cols = [c for c in data.columns if c not in [t_col, e_col] + exclude_col]

    # Negtive values are taken as right censored
    data.loc[:, label_col] = data.loc[:, t_col]
    data.loc[data[e_col] == 0, label_col] = - data.loc[data[e_col] == 0, label_col]

    return data[x_cols + [label_col]]

def load_simulated_data(hr_ratio,
        N=1000, num_features=10, num_var=2,
        average_death=5, end_time=15,
        method="gaussian",
        gaussian_config={},
        seed=42):
    """
    Load simulated data generated by the exponentional distribution.

    Parameters
    ----------
    hr_ratio: int or float
        `lambda_max` hazard ratio.
    N: int
        The number of observations.
    average_death: int or float
        Average death time that is the mean of the Exponentional distribution.
    end_time: int or float
        Censoring time that represents an 'end of study'. Any death 
        time greater than end_time will be censored.
    num_features: int
        Size of observation vector. Default: 10.
    num_var: int
        Number of varaibles simulated data depends on. Default: 2.
    method: string
        The type of simulated data. 'linear' or 'gaussian'.
    gaussian_config: dict
        Dictionary of additional parameters for gaussian simulation.
    seed: int
        Random state.

    Returns
    -------
    pandas.DataFrame
        A simulated survival dataset following the given args.

    Notes
    -----
    Peter C Austin. Generating survival times to simulate cox proportional
    hazards models with time-varying covariates. Statistics in medicine,
    31(29):3946-3958, 2012.
    """
    generator = SimulatedData(hr_ratio, average_death=average_death, end_time=end_time, 
                              num_features=num_features, num_var=num_var)
    raw_data = generator.generate_data(N, method=method, gaussian_config=gaussian_config, seed=seed)
    
    # Transform to DataFrame
    df = pd.DataFrame(raw_data['x'], columns=['x_' + str(i) for i in range(num_features)])
    df['e'] = raw_data['e']
    df['t'] = raw_data['t']
    
    return df

def load_data(file_path, t_col='t', e_col='e', excluded_cols=[],
              split_ratio=1.0, normalize=False, seed=42):
    """
    load csv file and return a standard survival data for traning or testing.

    Parameters
    ----------
    file_path: str
        File path. Only support for csv file.
    t_col: str
        Column name of observed time in your data.
    e_col: str
        Column name of observed status in your data.
    excluded_cols: list
        Columns will not be included in the final data.
    split_ratio: float
        If `split_ratio` is set to 1.0, then full data will be obtained. Otherwise, the 
        splitted data will be returned.
    normalize: bool
        If true, then data will be normalized by Min-Max scale.
    seed: int
        Random seed for splitting data.

    Returns
    ------
    pandas.DataFrame
        Or tuple of two DataFrames if split_ratio is less than 1.0.
    """
    # Read csv data
    data_all = pd.read_csv(file_path)
    
    # list columns out
    Y_cols = [t_col, e_col]
    _not_int_x_cols = Y_cols + excluded_cols
    X_cols = [x for x in data_all.columns if x not in _not_int_x_cols]

    X = data_all[X_cols]
    y = data_all[Y_cols]

    # Normalized data
    if normalize:
        for col in X_cols:
            X[col + "_norm"] = (X[col] - X[col].mean()) / (X[col].max() - X[col].min())
        X.drop(columns=X_cols, inplace=True)
    
    # Split data
    if split_ratio == 1.0:
        train_X, train_y = X, y
        return pd.concat([train_X, train_y], axis=1)
    else:
        sss = ShuffleSplit(n_splits=1, test_size=1 - split_ratio, random_state=seed)
        for train_index, test_index in sss.split(X, y):
            train_X, test_X = X.loc[train_index, :], X.loc[test_index, :]
            train_y, test_y = y.loc[train_index, :], y.loc[test_index, :]

        return pd.concat([train_X, train_y], axis=1), pd.concat([test_X, test_y], axis=1)