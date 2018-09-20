#! /usr/bin/env python

import pandas as pd
import numpy as np
import datetime
import dateutil
import yaml

class LeidingPlanning(object):
    def __init__(self, path_zaterdag, path_zondag):
        self._zaterdag = self.parse_preformatted(path_zaterdag, "Leiding Zaterdag")
        self._zondag = self.parse_preformatted(path_zondag, "Leiding Zondag")

    @staticmethod
    def parse_smart(path, sheet):
        """Smart parsing tries to do use the sheet as-is, without any human alterations"""
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

    @staticmethod
    def parse_preformatted(path, sheet):
        """Smart parsing tries to do use the sheet as-is, without any human alterations"""
        df = pd.read_excel(path, sheet_name=sheet, index_col=[0, 1])
        planning = df.fillna(method='pad', axis=1)
        return planning

    @staticmethod
    def round_time(querytime, radix=10):
        rounded = datetime.datetime(year=querytime.year,
                                    month=querytime.month,
                                    day=querytime.day,
                                    hour=querytime.hour,
                                    minute=int(np.floor(querytime.minute / radix) * radix),
                                    second=querytime.second
                                    )
        return rounded

    def __getitem__(self, querytime):
        rounded = LeidingPlanning.round_time(querytime)
        if rounded in self._zaterdag:
            try:
                return self._zaterdag[rounded]
            except Exception:
                raise KeyError("There is no program on {0}".format(rounded))
        if rounded in self._zondag:
            try:
                return self._zondag[rounded]
            except Exception:
                raise KeyError("There is no program on {0}".format(rounded))
        raise KeyError("There is no program on {0}".format(rounded))

def build_interface():
    confpath = "configuration.yaml"
    conffile = open(confpath)
    config = yaml.load(conffile)

    leiding_schedule = [sub for sub in config if 'leiding_schedule' in sub][0]['leiding_schedule']
    path_zat = leiding_schedule['path_zaterdag']
    path_zon = leiding_schedule['path_zondag']

    return LeidingPlanning(path_zat, path_zon)

if __name__ == "__main__":
    lp = LeidingPlanning(
        path_zaterdag="/home/loy/Dropbox/02_Scouting/Jotari/2017/Leidingplanning 2017 date formatted zaterdag.xlsx",
        path_zondag="/home/loy/Dropbox/02_Scouting/Jotari/2017/Leidingplanning 2017 date formatted zondag.xlsx")

    zaterdag_ochtend = dateutil.parser.parse("2017-10-16 09:46")
    try:
        print(lp[zaterdag_ochtend][('Remus', 'Lynn')])
    except Exception as e:
        print(e)

    zondag_ochtend = dateutil.parser.parse("2017-10-17 09:46")
    try:
        print(lp[zondag_ochtend][('Remus', 'Lynn')])
    except Exception as e:
        print(e)