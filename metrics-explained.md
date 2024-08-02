# Metrics Explained

## Group Accuracy

See `evaluator.py`, where `accuracy` is focusing on `accurate_events`.

The idea is that gt is a partition of logs, and the parser result is also a partition. Consider a group within the partition given by the parser. We check whether there exists exactly the **same** group in the partition given by the gt. If "yes," then `accurate_events` will be added up by the size of the group.

### Code

`series_groundtruth_logId_valuecounts.size == 1` means `logIds` are all of the same gt group. Next, `logIds.size == series_groundtruth[series_groundtruth == groundtruth_eventId].size` means it is also **complete**. So with the above two, "exactly the **same** group" holds.
