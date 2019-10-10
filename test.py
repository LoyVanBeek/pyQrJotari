#! /usr/bin/env python

import yaml
from schedule_reading.csv_interface import build_interface
import pyQRjotari
from dateutil import parser

if __name__ == "__main__":
    confpath = "configuration.yaml"
    conffile = open(confpath)
    config = yaml.load(conffile)

    klein, groot = build_interface()

    schedules = {'klein':klein, "groot":groot}

    def update(*args, **kwargs):
        print args, kwargs

    assert pyQRjotari.JotariQrBackend(schedules, update, '2019-10-19 09:35').lookup('klein1') == 'opening'
    assert klein[parser.parse('2019-10-19 09:25')][1] == 'Opbouw+voorbereiden'
    assert klein[parser.parse('2019-10-19 09:35')][2] == 'Opening'
    assert klein[parser.parse('2019-10-19 10:35')][3] == 'JOTI'
    assert klein[parser.parse('2019-10-19 11:05')][4] == 'JOTA'
    assert klein[parser.parse('2019-10-20 01:05')][4] == 'Slapen'
    assert klein[parser.parse('2019-10-20 16:05')][4] == 'Tot volgend jaar'

    assert groot[parser.parse('2019-10-19 09:35')][1] == 'Opening'
    assert groot[parser.parse('2019-10-19 10:35')][2] == 'Tocht naar GINDER'
    assert groot[parser.parse('2019-10-20 01:35')][2] == 'Slapen'
    assert groot[parser.parse('2019-10-20 16:05')][4] == 'Tot volgend jaar'