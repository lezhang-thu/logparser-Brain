# Brain

### Main Takeaways
1. The original Brain involves two splits, i.e., `up_split` and `down_split`. We remove the `up_split` (as it actually never gets executed) and only keep the `down_split`.
2. Only `tuple_vector` is kept for constructing the `TupleTree`, where each log is translated into a list of `(frequency, token)`'s.
3. The official Brain repo departs from the paper. The ideas can be summarized into four steps:
    1. Group logs (pre-processed as lists of tokens) according to their lengths.
    2. For a log within a specific group, conduct the translation: `token` >> `(frequency, token)`, where frequency can be interpreted as *column* frequency if we view the group as a **matrix**.
    3. Construct a `TupleTree` for each group, where the next split criterion is the *longest common pattern* as illustrated in the paper.
    4. For other frequencies that are *not* the most common, recheck the number of distinct tokens within the corresponding column. If **the number** is no less than a threshold, then the tokens for this column are all interpreted as variables (i.e., NOT constant).

Actually, as one can see, there are no trees constructed, as the process above is NOT recursive. Anyway, the above algorithm WORKS!

### Run

Run the following scripts to execute the benchmark:

```
python benchmark.py
```

### Benchmark

Running the benchmark script on Loghub_2k datasets, get the **SAME** results as the [original Brain implementation][brain].

|   Dataset   | F1_measure | Accuracy |
|:-----------:|:----------|:---------|
|  Proxifier  | 1          | 1        |
|     HDFS    | 0.999984   | 0.9975   |
|    Hadoop   | 0.998749   | 0.949    |
|    Spark    | 0.99998    | 0.9975   |
|  Zookeeper  | 0.9998     | 0.9875   |
|     BGL     | 0.999932   | 0.986    |
|     HPC     | 0.997707   | 0.945    |
| Thunderbird | 0.999933   | 0.971    |
|   Windows   | 0.999995   | 0.997    |
|    Linux    | 0.999992   | 0.996    |
|   Android   | 0.996837   | 0.9605   |
|  HealthApp  | 1          | 1        |
|    Apache   | 1          | 1        |
|   OpenSSH   | 1          | 1        |
|  OpenStack  | 1          | 1        |
|     Mac     | 0.995821   | 0.942    |


### 🔥 Citation

If you use the code or benchmarking results in your publication, please kindly cite the following papers.

+ [**TSC'23**] Siyu Yu, Pinjia He, Ningjiang Chen, and Yifan Wu. [Brain: Log Parsing with Bidirectional Parallel Tree](https://ieeexplore.ieee.org/abstract/document/10109145), *IEEE Transactions on Service Computing*, 2023.
+ [**ICSE'19**] Jieming Zhu, Shilin He, Jinyang Liu, Pinjia He, Qi Xie, Zibin Zheng, Michael R. Lyu. [Tools and Benchmarks for Automated Log Parsing](https://arxiv.org/pdf/1811.03509.pdf). *International Conference on Software Engineering (ICSE)*, 2019.

[brain]: https://github.com/logpai/logparser/blob/main/logparser/Brain/Brain.py
