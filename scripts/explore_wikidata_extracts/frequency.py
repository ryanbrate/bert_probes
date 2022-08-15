""" get the frequency for each column
"""

import json
import pandas as pd


def main():

    with open("combinations_configs.json", "r") as f:
        configs = json.load(f)

    for config in configs:

        input_file = config["input_file"]

        df = pd.read_csv(input_file)
        
        print(df.info())


if __name__ == "__main__":
    main()
