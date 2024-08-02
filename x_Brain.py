from datetime import datetime
from collections import Counter, defaultdict
import os
import pandas as pd
import regex as re

RED = "\033[31m"
RESET = "\033[0m"
PINK = "\033[38;2;255;192;203m"


class LogParser:
    sub_dict = defaultdict(
        list, {
            "HealthApp": [(":", ": "), ("=", "= "), ("\|", "| ")],
            "Android": [(":", ": "), ("=", "= ")],
            "HPC": [("=", "= "), ("-", "- "), (":", ": ")],
            "BGL": [("=", "= "), ("\.\.", ".. "), ("\(", "( "), ("\)", ") ")],
            "Hadoop": [("_", "_ "), (":", ": "), ("=", "= "), ("\(", "( "),
                       ("\)", ") ")],
            "HDFS": [(":", ": ")],
            "Linux": [("=", "= "), (":", ": ")],
            "Spark": [(":", ": ")],
            "Thunderbird": [(":", ": "), ("=", "= ")],
            "Windows": [(":", ": "), ("=", "= "), ("\[", "[ "), ("]", "] ")],
            "Zookeeper": [(":", ": "), ("=", "= ")]
        })

    def __init__(
        self,
        logname,
        log_format,
        indir="./",
        outdir="./result/",
        threshold=2,
        delimeter=[],
        rex=[],
    ):
        self.dataset = logname
        self.logformat = log_format
        self.path = indir
        self.savePath = outdir
        self.rex = rex
        self.df_log = None
        self.threshold = threshold
        self.delimeter = delimeter

    def parse(self, logName):
        print("Parsing file: " + os.path.join(self.path, logName))
        starttime = datetime.now()
        self.logName = logName

        self.load_data()

        sentences = self.df_log["Content"].tolist()
        tuple_vector = self.get_frequency_vector(sentences, self.rex,
                                                 self.delimeter)

        template_set = {}
        for key in tuple_vector.keys():
            tree = TupleTree(tuple_vector[key])
            root_set = tree.find_root()
            parse_result = tree.down_split(self.threshold, root_set)
            template_set.update(output_result(parse_result))

        endtime = datetime.now()
        print('x_Brain.py')
        print("Parsing done...")
        print("Time taken   =   " + PINK + str(endtime - starttime) + RESET)

        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)

        self.generateresult(template_set, sentences)

    def generateresult(self, template_set, sentences):
        template_ = len(sentences) * [0]
        EventID = len(sentences) * [0]
        IDnumber = 0
        df_out = []
        for k1 in template_set.keys():
            df_out.append(["E" + str(IDnumber), k1, len(template_set[k1])])
            group_accuracy = {""}
            group_accuracy.remove("")
            for i in template_set[k1]:
                template_[i] = " ".join(k1)
                EventID[i] = "E" + str(IDnumber)
            IDnumber += 1

        self.df_log["EventId"] = EventID
        self.df_log["EventTemplate"] = template_
        self.df_log.to_csv(os.path.join(self.savePath,
                                        self.logName + "_structured.csv"),
                           index=False)

        df_event = pd.DataFrame(
            df_out, columns=["EventId", "EventTemplate", "Occurrences"])
        df_event.to_csv(
            os.path.join(self.savePath, self.logName + "_templates.csv"),
            index=False,
            columns=["EventId", "EventTemplate", "Occurrences"],
        )

    def load_data(self):
        headers, regex = self.generate_logformat_regex(self.logformat)
        self.df_log = self.log_to_dataframe(
            os.path.join(self.path, self.logName), regex, headers,
            self.logformat)

    def generate_logformat_regex(self, logformat):
        """Function to generate regular expression to split log messages"""
        headers = []
        splitters = re.split(r"(<[^<>]+>)", logformat)
        regex = ""
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(" +", "\\\s+", splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip("<").strip(">")
                regex += "(?P<%s>.*?)" % header
                headers.append(header)
        regex = re.compile("^" + regex + "$")
        return headers, regex

    def log_to_dataframe(self, log_file, regex, headers, logformat):
        """Function to transform log file to dataframe"""
        log_messages = []
        linecount = 0
        with open(log_file, "r") as fin:
            for line in fin.readlines():
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
        logdf = pd.DataFrame(log_messages, columns=headers)
        logdf.insert(0, "LineId", None)
        logdf["LineId"] = [i + 1 for i in range(linecount)]
        return logdf

    def sub(self, s):
        for x in self.sub_dict[self.dataset]:
            s = re.sub(x[0], x[1], s)

        return s

    def get_frequency_vector(self, sentences, filter_x, delimiter):
        """
        Count each word's frequency in the dataset and convert each log into frequency vector
        Output:
            tuple_vector: the word in the log will be converted into a tuple (word_frequency, word_character, word_position)
        """
        group_len = defaultdict(list)
        fre_set = defaultdict(int)
        for line_id, s in enumerate(
                sentences):  # using delimiters to get split words
            for rgex in filter_x:
                s = re.sub(rgex, "<*>", s)
            for de in delimiter:
                s = re.sub(de, "", s)
            s = self.sub(s)
            s = re.sub(",", ", ", s)
            s = re.sub(" +", " ", s).split(" ")
            s.append(line_id)

            for col, token in enumerate(
                    s[:-1]):  # counting each word's frequency
                fre_set[str(col) + " " + token] += 1
            group_len[len(s) - 1].append(
                s)  # the first grouping: logs with the same length

        tuple_vector = defaultdict(list)
        for key in group_len.keys(
        ):  # use fre_set to generate frequency vector for the log
            for s in group_len[key]:  # within the log group of the same length
                frequency_full = []
                for col, token in enumerate(s[:-1]):
                    frequency = fre_set[str(col) + " " + token]
                    frequency_full.append((
                        frequency,
                        token,
                    ))

                # s[-1]: line_id
                frequency_full.append(s[-1])
                tuple_vector[key].append(frequency_full)
        return tuple_vector


class TupleTree:
    # **A** TupleTree for **A** specific length
    def __init__(
        self,
        tuple_vector_specific_len,
    ):
        self.tuple_vector_specific_len = tuple_vector_specific_len

    def find_root(self):
        root_set = defaultdict(list)
        for tv in self.tuple_vector_specific_len:
            key = Counter([x[0] for x in tv[:-1]]).most_common(1)[0]
            root_set[key].append(tv)
        return root_set

    def down_split(self, threshold, root_set):
        for key in root_set.keys():
            all_sents = root_set[key]
            first_sent = all_sents[0]

            variable = set()
            for i, token_tuple in enumerate(first_sent[:-1]):
                if token_tuple[0] != key[0]:
                    distinct_children = set([sent[i][1] for sent in all_sents])
                    if len(distinct_children) >= threshold:
                        variable = variable.union(distinct_children)

            for i in range(len(root_set[key])):
                for j in range(len(root_set[key][i]) - 1):
                    if root_set[key][i][j][1] in variable:
                        root_set[key][i][j] = (
                            root_set[key][i][j][0],
                            "<*>",
                        )
        return root_set


def output_result(parse_result):
    template_set = defaultdict(list)
    for key in parse_result.keys():
        for pr in parse_result[key]:
            template = []
            for i in range(len(pr) - 1):
                x = pr[i][1]
                if "<*>" in x:
                    template.append("<*>")
                elif exclude_digits(x):
                    template.append("<*>")
                else:
                    template.append(x)

            template = tuple(template)
            template_set[template].append(pr[len(pr) - 1])
    return template_set


def save_result(dataset, df_output, template_set):
    df_output.to_csv("Parseresult/" + dataset + "result.csv", index=False)
    with open("Parseresult/" + dataset + "_template.csv", "w") as f:
        for k1 in template_set.keys():
            f.write(" ".join(list(k1)))
            f.write("  " + str(len(template_set[k1])))
            f.write("\n")
        f.close()


def exclude_digits(string):
    """
    exclude the digits-domain words from partial constant
    """
    pattern = r"\d"
    digits = re.findall(pattern, string)
    if len(digits) == 0:
        return False
    return len(digits) / len(string) >= 0.3
