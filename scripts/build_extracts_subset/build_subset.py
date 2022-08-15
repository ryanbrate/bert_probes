from itertools import combinations

import numpy as np
import pandas as pd
import json
import pathlib


def main():

    with open("build_subset_configs.json", "r") as f:
        configs = json.load(f)

    for config in configs:

        properties = config["properties"]  # list of properties of interest
        input_file = pathlib.Path(config["input_file"]).expanduser()
        output_file = pathlib.Path(config["output_file"]).expanduser()

        # load the df for only properties of interest
        df = pd.read_csv(input_file).loc[:, properties]

        # get a count of null elements per row for df.loc[:, properties]
        df["null_count"] = df.apply(lambda row: row.isnull().sum(), axis=1)

        # get subset with no missing property entries, wrt., properties
        df_subset = df.loc[df.loc[:, "null_count"] == 0, properties]

        # save
        output_file.parent.mkdir(exist_ok=True, parents=True)
        df_subset.to_csv(output_file, index=False)


if __name__ == "__main__":
    main()
