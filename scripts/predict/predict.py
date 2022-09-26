"""
perform mask prediction on huggingface plms via transformers module
"""
import json
import pathlib
from functools import partial

import numpy as np
import pandas as pd
from tqdm import tqdm
from transformers import Pipeline, pipeline


def main():

    # load list of configs - each to be run sequentially
    with open("predict_configs.json", "r") as f:
        configs = json.load(f)

    # iterate over configs
    for config in configs:

        # load the config options
        model = config["model"]
        probe_columns = config["probe_columns"]
        input_file = pathlib.Path(config["input_file"]).expanduser()
        output_dir = pathlib.Path(config["output_dir"]).expanduser()
        default_columns = config["default_columns"]

        print(f"running probes from ... {input_file}")

        # setup pipeline
        unmasker = pipeline("fill-mask", model=model)

        # iterate over probe sets, consider each in-turn
        for probe_column in probe_columns:

            output_file = output_dir / f"{probe_column}.csv"

            if output_file.exists():
                continue
            else:

                # load the csv, with only default columns + specific probe column
                with open(input_file, "r") as f:
                    df_probe = pd.read_csv(f, sep="\t").loc[
                        :, default_columns + [probe_column]
                    ]

                # init prediction columns
                for i in range(1, 6):
                    df_probe[f"prediction_{i}"] = np.nan

                # append predictions to csv
                print(f"\t{probe_column}")
                tqdm.pandas()
                df_probe = df_probe.progress_apply(
                    partial(get_predictions, unmasker=unmasker, probe_column=probe_column),
                    axis=1,
                )

                # save the csv
                output_dir.mkdir(parents=True, exist_ok=True)
                with open(output_file, "w") as f:
                    df_probe.to_csv(f, index=False, sep="\t")


def get_predictions(row: pd.Series, *, unmasker: Pipeline, probe_column: str):
    """append predictions to row in-place"""

    # rank predictions in order of descending probability
    predictions: dict = sorted(
        unmasker(row[probe_column]), key=lambda x: x["score"], reverse=True
    )

    for i, prediction in enumerate(predictions, start=1):
        row[f"prediction_{str(i)}"] = prediction["token_str"]

    return row


if __name__ == "__main__":
    main()
