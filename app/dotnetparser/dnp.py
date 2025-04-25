import re

import pandas as pd


class DotNetParser:
    def __init__(self, extension="NET"):
        self.__extension = extension

    def execute(self, text, obj_name):
        lines = text.split("\n")
        lines_split = [[sub_row for sub_row in row.split(" ") if sub_row] for row in lines]
        lines_split = self.__check_on_stars(lines_split)
        df = pd.DataFrame({"Name": [], "Number": []})
        for line in lines_split:
            for i in range(1, len(line)):
                if re.match(obj_name, line[i]):
                    obj_split = line[i].split("-")
                    if len(obj_split) > 1 and obj_split[0] == obj_name:
                        obj_split[1] = obj_split[1].replace(r"\n", "")
                        df = pd.concat(
                            [df, pd.DataFrame({"Name": [line[0]], "Number": [obj_split[1]]})],
                            ignore_index=True)
        df = df.map(lambda x: x.replace("\n", "") if isinstance(x, str) else x)

        result = ""
        for row in df.to_numpy():
            result += f"{row[0]} {row[1]}\n"
        return result

    @staticmethod
    def __check_on_stars(elements):
        result = []
        for row in elements:
            if row and row[0] == "*":
                for elem in row[1:]:
                    result[-1].append(elem)
            else:
                result.append(row)
        return result
