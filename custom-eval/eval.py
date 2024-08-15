import os

from common import common_args
from evaluator_main import evaluator, prepare_results
from postprocess import post_average

datasets_2k = [
    "Proxifier",
    "Linux",
    "Apache",
    "Zookeeper",
    "Hadoop",
    "HealthApp",
    "OpenStack",
    "HPC",
    "Mac",
    "OpenSSH",
    "Spark",
    "Thunderbird",
    "BGL",
    "HDFS",
]

datasets_full = [
    "Proxifier",
    "Linux",
    "Apache",
    "Zookeeper",
    "Hadoop",
    "HealthApp",
    "OpenStack",
    "HPC",
    "Mac",
    "OpenSSH",
    "Spark",
    "Thunderbird",
    "BGL",
    "HDFS",
]

if __name__ == "__main__":
    args = common_args()
    data_type = "full" if args.full_data else "2k"
    input_dir = os.path.join('..', "{}_dataset".format(data_type))
    output_dir = args.parsed_file
    if not os.path.exists("result"):
        os.makedirs("result")

    result_file = prepare_results(args.alg,
                                  otc=args.oracle_template_correction,
                                  complex=args.complex,
                                  frequent=args.frequent)

    if args.full_data:
        datasets = datasets_full
    else:
        datasets = datasets_2k
    for dataset in datasets:
        log_file = os.path.join(dataset, "{}_{}.log".format(dataset, data_type))
        # run evaluator for a dataset
        evaluator(dataset=dataset,
                  input_dir=input_dir,
                  output_dir=output_dir,
                  log_file=log_file,
                  LogParser=None,
                  param_dict={},
                  otc=args.oracle_template_correction,
                  complex=args.complex,
                  frequent=args.frequent,
                  result_file=result_file
                 )  # it internally saves the results into a summary file
    metric_file = result_file
    post_average(
        metric_file,
        f"{args.alg}_{data_type}_complex_{args.complex}_frequent_{args.frequent}",
        args.complex, args.frequent)
