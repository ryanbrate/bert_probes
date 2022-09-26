""" Perform sign test to compare whether 
"""

import json
import pathlib
import pandas as pd
from scipy.stats import binom_test

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
        treatment1: pd.Series = pd.read_csv(set1_filepath, sep='\t').loc[:, column]
        treatment2: pd.Series = pd.read_csv(set2_filepath, sep='\t').loc[:, column]

        # create paired tuples where the treatment outcomes differ only (ignore sames)
        diffs = [(x1, x2) for x1, x2 in zip(treatment1, treatment2) if x1 != x2]
        n: int = len(diffs)  # i.e., counts of differences

        if n == 0:

            print(f"{desc}: NO DIFFERENCE")

        else:

            # counts of x1 > x2
            x: int = len(list(filter(lambda t: t[0] > t[1], diffs)))

            # binom test
            p_value: float = binom_test(x, n, p=0.5, alternative=alternative)
            print(f"{desc}: x={x}, n={n}, p_value = {p_value}")


        
        
if __name__ == "__main__":
    main()
