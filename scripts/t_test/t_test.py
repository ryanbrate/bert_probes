""" Perform paired t-test to compare whether 
"""

import json
import pathlib
import statistics
import math

import pandas as pd
import scipy


def main():

    with open("test_configs.json", "r") as f:
        configs = json.load(f)

    for config in configs:

        # set options
        desc = config["description"]
        set1_filepath = pathlib.Path(config["greater_set_filepath"]).expanduser()
        set2_filepath = pathlib.Path(config["lesser_set_filepath"]).expanduser()
        column = config["column"]
        alternative = config["alternative"]

        # load the paired datasets
        treatment1: pd.Series = pd.read_csv(set1_filepath, sep="\t").loc[:, column]
        treatment2: pd.Series = pd.read_csv(set2_filepath, sep="\t").loc[:, column]

        # test statistic
        diffs: pd.Series = treatment1 - treatment2
        df = len(diffs) - 1
        n = len(diffs)
        d_bar: float = sum(diffs) / n
        se = statistics.stdev(diffs) / math.sqrt(n)  # sampling distribution standard deviation
        x = (d_bar - 0) / se

        if alternative == "greater":

            # p-value
            p_value = 1 - scipy.stats.t.cdf(x, df)
            cv = scipy.stats.t.ppf(0.95, df)*se+0

            # power: i.e., P(signficicant observation | observed properties)
            power = 1-scipy.stats.t.cdf((cv-d_bar)/se, df)

        elif alternative == "lesser":

            # p-value
            p_value = scipy.stats.t.cdf(x, df)
            cv = scipy.stats.t.ppf(0.05, df)*se+0

            # power
            power = scipy.stats.t.cdf((cv-d_bar)/se, df)

        else:

            # p-value
            p_value = 2 * scipy.stats.t.cdf(-abs(x), df)
            cv = scipy.stats.t.ppf(0.025, df)

            # power
            power = 2*scipy.stats.t.cdf(-1*abs(cv-x), df)

        # report
        print(f"{desc}: d_bar = {d_bar}, x = {x}, p_value = {p_value}, power={power}")


if __name__ == "__main__":
    main()
