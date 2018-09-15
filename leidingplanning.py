import pandas as pd
import numpy as np
import dateutil


class LeidingPlanning(object):
    def __init__(self, path):
        zaterdag = self.parse(path, "Leiding Zaterdag")
        # zondag = self.parse(path, "Leiding Zondag")

        # self.planning = pd.concat([zaterdag, zondag], axis=1)#, join_axes=[df1.index])
        self.planning = pd.concat([zaterdag], axis=1)#, join_axes=[df1.index])

    @staticmethod
    def parse(path, sheet):
        planning = pd.read_excel(path, sheet_name=sheet, header=[0, 1, 2], index_col=[0, 1])
        planning = planning.fillna(method='pad', axis=1)
        pairs = []
        for day, hour, minute in planning.columns:
            if isinstance(minute, str) and minute.startswith("Unnamed"):
                pairs += [(day, hour, 0)]
            else:
                pairs += [(day, hour, minute)]
        planning.columns = pd.MultiIndex.from_tuples(pairs)

        return planning

    def __getitem__(self, querytime):
        try:
            return self.planning[(querytime.strftime("%Y-%m-%d"), querytime.hour, np.floor(querytime.minute/10)*10)]
        except KeyError:
            raise KeyError("There is no program on {0}".format(querytime))


if __name__ == "__main__":
    lp = LeidingPlanning(path="/home/loy/Dropbox/02_Scouting/Jotari/2017/Leidingplanning 2017.xlsx")
    print(lp[dateutil.parser.parse("2017-10-16 09:46")][('Remus', 'Lynn')])
    print(lp[dateutil.parser.parse("2017-10-17 09:46")][('Remus', 'Lynn')])