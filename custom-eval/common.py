import argparse


def is_abstract(x, y):
    """
    Determine if template_x is more abstract than template_y.

    :param x: a template (str)
    :param y: a template or a message (str)
    :return: True if x is more abstract (general) than y
    """

    if y is np.nan:
        return False

    m = re.match(get_pattern_from_template(x), y)
    if m:
        return True
    else:
        return False


def common_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-otc',
        '--oracle_template_correction',
        help="Set this if you want to use corrected oracle templates",
        default=False,
        action='store_true')
    parser.add_argument('-full',
                        '--full_data',
                        help="Set this if you want to test on full dataset",
                        default=False,
                        action='store_true')
    parser.add_argument('--complex',
                        type=int,
                        help="Set this if you want to test on complex dataset",
                        default=0)
    parser.add_argument('--frequent',
                        type=int,
                        help="Set this if you want to test on frequent dataset",
                        default=0)
    parser.add_argument('--shot',
                        type=int,
                        help="Set this if you want to test on complex dataset",
                        default=0)
    parser.add_argument('--example_size',
                        type=int,
                        help="Set this if you want to test on frequent dataset",
                        default=0)
    parser.add_argument('--parsed_file',
                        help="The parsed file to evaluate.",
                        type=str,
                        required=True)
    parser.add_argument('--alg',
                        help="The algorithm name",
                        type=str,
                        required=True)
    args = parser.parse_args()
    return args
