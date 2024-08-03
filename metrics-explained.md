# Metrics Explained

## Group Accuracy

See `evaluator.py`, where `accuracy` is focusing on `accurate_events`.

The idea is that gt is a partition of logs, and the parser result is also a partition. Consider a group within the partition given by the parser. We check whether there exists exactly the **same** group in the partition given by the gt. If "yes," then `accurate_events` will be added up by the size of the group.

### Code

```
        if series_groundtruth_logId_valuecounts.size == 1:
```
means `logIds` are all of the same gt group. Next,
```
            if logIds.size == series_groundtruth[series_groundtruth ==
                                                 groundtruth_eventId].size:
```
means it is also **complete**. So with the above two, "exactly the **same** group" holds.

## Precision & recall

Consider a specific group within the partition given by the parser. We then re-partition this specific group according to the gt. This results in a collection of subgroups. For each subgroup of size $k>2$, we increase `accurate_pairs` by $k \choose 2$.

## FGA in [loghub-2.0](#1)

GA and FGA lie in the code [here](https://github.com/logpai/loghub-2.0/blob/main/benchmark/logparser/utils/evaluator.py), i.e., the **codebase within loghub-2.0**, rather than in logparser official repo.
The code is
```
                    accurate_events += len(group)
                    accurate_templates += 1
```
where we can compare with the original code of logparser `evaluator.py`:
```
                accurate_events += logIds.size
```
So one sees that now FGA counts only 1 by `+= 1`.

## References
<a id="1">loghub-2.0</a>
A Large-Scale Evaluation for Log Parsing Techniques: How Far Are We?
