import pandas as pd
import numpy as np
import dateutil


class LeidingPlanning(object):
    def __init__(self, path):
        self.planning = pd.read_excel(path, sheet_name="Leiding Zaterdag", header=[0, 1, 2], index_col=[0,1])
        self.planning = self.planning.fillna(method='pad', axis=1)

        pairs = []
        for day, hour, minute in self.planning.columns:
            if isinstance(minute, str) and minute.startswith("Unnamed"):
                pairs += [(day, hour, 0)]
            else:
                pairs += [(day, hour, minute)]
        self.planning.columns = pd.MultiIndex.from_tuples(pairs)

    def __getitem__(self, querytime):
        return self.planning[(querytime.strftime("%Y-%m-%d"), querytime.hour, np.floor(querytime.minute/10)*10)]


if __name__ == "__main__":
    lp = LeidingPlanning(path="/home/loy/Dropbox/02_Scouting/Jotari/2017/Leidingplanning 2017.xlsx")
    print(lp[dateutil.parser.parse("2017-10-16 18:46")][('Remus', 'Lynn')])