"""
Calculate the r-values of plm predictions
"""

import json
import pathlib
from functools import partial

import pandas as pd
from tqdm import tqdm


def main():

    with open("r_configs.json", "r") as f:
        configs = json.load(f)

    # container to store all configs R@n values
    r_values = {"description":[], "R@1": [], "R@5": []}

    # run each config
    for config in configs:

        # load the config options
        predictions_dir = pathlib.Path(config["predictions_dir"]).expanduser()
        labels_filepath = pathlib.Path(config["labels_filepath"]).expanduser()
        output_dir = pathlib.Path(config["output_dir"]).expanduser()
        desc = config["description"]

        print(desc)

        for predictions_filepath in predictions_dir.glob("*.csv"):

            output_filepath = output_dir / predictions_filepath.name

            # open predictions and labels
            with open(predictions_filepath, "r") as f:
                df_predictions = pd.read_csv(f, sep="\t")

            with open(labels_filepath, "r") as f:
                df_labels = pd.read_csv(f, sep=",")

            # merge labels into predictions
            df_combined = pd.merge(
                left=df_predictions,
                right=df_labels.loc[:, ["ID", "labels"]],
                how="left",
                left_on="ID",
                right_on="ID",
            )

            # get r@1 scores per item
            print("get R@1 scores")
            tqdm.pandas()
            df_combined["R@1"] = df_combined.progress_apply(partial(r_at, n=1), axis=1)

            # get r@5 scores per item
            print("get R@5 scores")
            tqdm.pandas()
            df_combined["R@5"] = df_combined.progress_apply(partial(r_at, n=5), axis=1)

            # update ...
            r_values["description"].append(desc + " " + predictions_filepath.stem)
            r_values["R@1"].append(df_combined["R@1"].mean())
            r_values["R@5"].append(df_combined["R@5"].mean())

            # save individual file
            output_filepath.parent.mkdir(exist_ok=True, parents=True)
            df_combined.to_csv(output_filepath, index=False, sep='\t')

    # save global summary
    pd.DataFrame(r_values).to_csv(output_dir.parent.parent / "summary.csv")

        

def r_at(row: pd.Series, *, n: int)->float:
    """calculate recall at n for a single datapoint"""
    assert n <= 5, "n must be <=5"

    predictions = [row[f"prediction_{i}"].lower().strip() for i in range(1, 5+1)]
    labels = [i.strip() for i in row["labels"].lower().split("|")]

    a = set(predictions[:1])
    b = set(labels)

    return len(set(predictions[:n]).intersection(set(labels))) / len(labels)


if __name__ == "__main__":
    main()
