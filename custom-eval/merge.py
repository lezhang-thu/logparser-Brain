import pandas as pd
import sys
import os
import glob


def merge_results(file_brain, file_logppt, dir_name):
    df_brain = pd.read_csv(file_brain)
    df_logppt = pd.read_csv(file_logppt)
    series_logppt = df_logppt['EventTemplate'].reset_index(drop=True)

    merge_df = pd.concat(
        [df_brain.drop(columns='EventTemplate'), series_logppt], axis=1)

    majority = merge_df.groupby('EventId')['EventTemplate'].agg(
        lambda x: x.mode()[0]).to_dict()
    merge_df['EventTemplate'] = merge_df['EventId'].map(majority)

    file_name = os.path.basename(file_brain)
    merge_df.to_csv(os.path.join(dir_name, file_name), index=False)
    template_df = merge_df.groupby(
        'EventId').first().reset_index().loc[:, ['EventId', 'EventTemplate']]
    template_df.sort_values(
        by=['EventId'],
        inplace=True,
        key=lambda x: x.str.extract('(\d+)').astype(int).squeeze())
    x = '_'.join(file_name.split('_')[:-1] + ['templates.csv'])
    template_df.to_csv(os.path.join(dir_name, x), index=False)


if __name__ == '__main__':
    dir_name = sys.argv[3]
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    pattern = os.path.join(sys.argv[1], '*structured.csv')
    # debug - start - lezhang.thu
    print('brain path: {}'.format(sys.argv[1]))
    print('logppt path: {}'.format(sys.argv[2]))
    # debug - end - lezhang.thu
    matching_files = glob.glob(pattern)
    for file_brain in matching_files:
        file_logppt = os.path.join(sys.argv[2], os.path.basename(file_brain))
        assert os.path.isfile(file_logppt), "file NOT exists!!! error!!!"
        merge_results(file_brain, file_logppt, dir_name)
