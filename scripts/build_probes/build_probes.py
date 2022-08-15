""" build probe statements from formatted wikidata extracts subset
"""
import json
import pathlib
import typing
from functools import partial

import pandas as pd
from tqdm import tqdm


def main():

    # read in wikidata properties
    with open("build_configs.json", "r") as f:
        configs = json.load(f)

    # iterate over configs
    for config in tqdm(configs):

        # get options
        input_file = pathlib.Path(config["input_file"]).expanduser()
        output_file = pathlib.Path(config["output_file"]).expanduser()
        add = config["add"]  # columns to add to query, in order of addition
        item_name_col = config["item_name_col"]

        start_str = config["start_str"]
        add_f = eval(config["add_f"])  # lambda functlion
        end_str = config["end_str"]

        # read in csv of wikidata formatted properties
        df = pd.read_csv(input_file, index_col=0)

        # construct each probe permutation
        for i in range(0, len(add) + 1):

            if len(add) > 0:
                columns = add[:i]
            else:
                columns = []

            # build probes
            df[f"probes_{i}"] = df.apply(
                partial(
                    build,
                    item_name_col=item_name_col,
                    columns=columns,
                    start_str=start_str,
                    add_f=add_f,
                    end_str=end_str,
                ),
                axis=1,
            )

        # save
        output_file.parent.mkdir(exist_ok=True, parents=True)
        with open(output_file, "w") as f:
            df.to_csv(f, sep="\t")

        # save config
        with open(output_file.parent / "config.json", "w") as f:
            json.dump(config, f)


def build(
    row: pd.Series,
    *,
    item_name_col: str,
    columns: list,
    start_str: str,
    add_f: typing.Callable,
    end_str: str,
):
    """ Create a probe string.
    """

    # start it off
    probe = start_str.format(row[item_name_col])

    # append each property to probe
    for col in columns:
        probe += add_f(col, str(row[col]))

    probe += end_str

    return probe


if __name__ == "__main__":
    main()
