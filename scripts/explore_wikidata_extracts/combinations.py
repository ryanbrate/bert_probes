from itertools import combinations

import numpy as np
import pandas as pd
import json
import pathlib
from tqdm import tqdm


def main():

    with open("combinations_configs.json", "r") as f:
        configs = json.load(f)

    for config in configs:

        # get config options
        n = int(config["n"])
        input_file = pathlib.Path(config["input_file"]).expanduser()
        columns_of_interest = config["columns_of_interest"]
        print(f"\n\nconfig: input_file={input_file}, n={n}")

        # load the df
        df = pd.read_csv(input_file)
        columns = df.columns

        # set values to 1 or 0 for presence or absence of info
        df = pd.DataFrame(np.where(df.isna(), df, 1))
        df.fillna(0, inplace=True)
        df.columns = columns

        # consider column combinations
        print("considering all permutations for coincident count")
        results = []
        for c in tqdm(combinations(columns_of_interest, n)):
            sum_by_row = len(list(filter(lambda x: x==n, df.loc[:, c].apply(sum, axis=1))))
            results.append((c, sum_by_row))

        print("\tsorting")
        results = sorted(results, key = lambda x: x[1], reverse=True)

        i = 0
        for c, sum_by_row in results:
            if i==10:
                break
            else:
                print(f"\tnumber of rows with all columns full in {c} is {sum_by_row}")
                i+=1



if __name__ == "__main__":
    main()
