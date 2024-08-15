import pandas as pd
import numpy as np
import os


def post_average(metric_file, tech, complex, frequent):
    df = pd.read_csv(metric_file, index_col=False)
    df = df.drop_duplicates(['Dataset'])
    # we have changed the round from 2 to 3 to get more precise average metrics
    mean_row = df.select_dtypes(include=[np.number]).mean().round(3)
    new_row = pd.DataFrame([['Average']], columns=['Dataset']).join(
        pd.DataFrame([mean_row.values], columns=mean_row.index))
    df = pd.concat([df, new_row], ignore_index=True)
    output_path = os.path.join("result", "{}.csv".format(tech))
    if complex != 0:
        output_path = os.path.join("result", "complex", "{}.csv".format(tech))
    if frequent != 0:
        output_path = os.path.join("result", "frequent", "{}.csv".format(tech))
    df.to_csv(output_path, index=False)
    df = pd.read_csv(output_path)
    transposed_df = df.transpose()
    transposed_df.to_csv(output_path)
