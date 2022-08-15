""" Perform formatting to wikidata extract subset
"""

import json
import pathlib

import pandas as pd


def main():

    with open("format_configs.json", "r") as f:
        configs = json.load(f)

    # run each config separately
    for config in configs:

        # ------
        # get options
        # ------

        input_file = pathlib.Path(config["input_file"]).expanduser()  # wiki extracts
        output_file = pathlib.Path(
            config["output_file"]
        ).expanduser()  # outputted, formatted extracts

        # get a dict of key=lambda function, values=list of columns to applu to
        apply_to_columns: dict = config["apply_to_columns"]

        # get a dict of column name: new column name
        columns_name_changes: dict = config["column_name_changes"]

        # open the subset dataframe
        with open(input_file, "r") as f:
            df = pd.read_csv(f)

        # make en-mass value changes to columns
        for lambda_fun, relevant_columns in apply_to_columns.items():
            for col in relevant_columns:
                df[col] = df[col].apply(eval(lambda_fun))

        # make column name changes
        df = df.rename(columns=columns_name_changes)


        # save formatted data
        output_file.parent.mkdir(exist_ok=True, parents=True)
        df.to_csv(output_file, index=False)

        # save config out output_folder
        with open(output_file.parent / "config.json", "w") as f:
            json.dump(config, f, indent=4)


if __name__ == "__main__":
    main()
