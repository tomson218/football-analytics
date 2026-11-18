"""
pearson_corr.py — Pearson correlation between HT and FT result.
Encoding: H=1, D=0, A=-1.
"""
import pandas as pd
from scipy.stats import pearsonr


def pearson_correlation(df: pd.DataFrame):
    """
    Calculates Pearson correlation coefficient between half-time result
    (HTResult) and full-time result (FTResult).
    Encoding: H=1, D=0, A=-1.
    """
    HTResult = df["HTResult"]
    FTResult = df["FTResult"]

    mapping = {"H": 1, "D": 0, "A": -1}
    HT_num = [mapping[x] for x in HTResult]
    FT_num = [mapping[x] for x in FTResult]

    r, p_value = pearsonr(HT_num, FT_num)
    return r, p_value
