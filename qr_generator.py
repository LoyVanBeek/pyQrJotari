#!/usr/bin/python

import sys, os, itertools, csv

def main(klein, groot, leiding_tuples):

    yield """<html>\n\t<head>\n\t\t<title>\n\t\t\tJotari QR Codes\n\t\t</title>\n\t</head>\n\t"""
    yield """<body style="font-family:arial; font-size:20px">"""

    yield "\n".join(write_QRcodes(klein, groot))
    yield "\n".join(generate_leiding_table(leiding_tuples))


    yield """\n\t</body></html>"""

def write_QRcodes(klein, groot, columns=4):
    rows, rest = divmod(len(klein)+len(groot), columns)
    if rest:
        rows += 1 #if there is a rest left after the divmod, make one more row.

    klein_cells = generate_cells("klein", klein)
    groot_cells = generate_cells("groot", groot)
    cells = itertools.chain(klein_cells, groot_cells)

    yield "\n\t\t<table>"
    for rowno in range(rows):
        yield "\t\t\t<tr>"
        for i in range(columns):
            #print rowno, i
            try:
                cell = cells.next()
                yield "\t\t\t\t<td>"
                yield cell
                yield "\t\t\t\t</td>"
            except StopIteration:
                break
        #import pdb; pdb.set_trace()
        yield "\t\t\t</tr>"
    yield "\t\t</table>"

def generate_cell(code):
    address = "http://www.scoutingboxtel.nl/qr.asp?groep={0}".format(code)
    return """\t\t\t\t\t<div style='border: solid 1px; text-align: center; width: 200px; height: 240px; margin: 5px; vertical-align:bottom; padding: 10px'>
    \t\t\t\t\t\t<br>
\t\t\t\t\t\t{0}
\t\t\t\t\t\t<img src="http://api.qrserver.com/v1/create-qr-code/?data={1}&#38;size=200x200&#38;prov=goqrme" alt="{0}" title=""/>
\t\t\t\t\t</div>""".format(code, address)

def generate_leiding_cell(speltak, voornaam):
    code = "leiding:{}:{}".format(speltak, voornaam)
    address = "http://www.scoutingboxtel.nl/qr.asp?groep={0}".format(code)
    return """\t\t\t\t\t<div style='border: solid 1px; text-align: center; width: 200px; height: 240px; margin: 5px; vertical-align:bottom; padding: 10px'>
        \t\t\t\t\t\t<br>
    \t\t\t\t\t\t{0}
    \t\t\t\t\t\t<img src="http://api.qrserver.com/v1/create-qr-code/?data={1}&#38;size=200x200&#38;prov=goqrme" alt="{0}" title=""/>
    \t\t\t\t\t</div>""".format(code, address)

def generate_leiding_table(leiding_tuples, columns=4):
    cells = (generate_leiding_cell(speltak, voornaam) for speltak, voornaam in leiding_tuples)

    rows, rest = divmod(len(leiding_tuples), columns)
    if rest:
        rows += 1 #if there is a rest left after the divmod, make one more row.

    yield "\n\t\t<table>"
    for rowno in range(rows):
        yield "\t\t\t<tr>"
        for i in range(columns):
            # print rowno, i
            try:
                yield "\t\t\t\t<td>"
                yield cells.next()
                yield "\t\t\t\t</td>"
            except StopIteration:
                break
        # import pdb; pdb.set_trace()
        yield "\t\t\t</tr>"
    yield "\t\t</table>"


def generate_cells(text, numbers):
    for i in numbers:
        code = text+str(i)
        yield generate_cell(code)

if __name__ == "__main__":
    filename = sys.argv[1]

    leiding_path = sys.argv[2]
    lr = csv.DictReader(open(leiding_path))

    speleenheid2short_map = {"Bevers":"Bevers",
                             "Scout-Angels":"Sc. Angels",
                             "Dwergen":"Dwergen",
                             "Gidsen":"Gidsen",
                             "Maten van Scouting Boxtel":"Overige",
                             "ondersteuningsteam":"Overige",
                             "Rowans":"Rowans",
                             "Sherpa's":"Sherpa's",
                             "Stam":"Stam",
                             "Stichtingsbestuur":"Overige",
                             "Trollen":"Trollen",
                             "Verenigingsbestuur":"Overige",
                             "Verkenners (vrijdag)":"Verk. Vr",
                             "Verkenners (woensdag)":"Verk. Wo",
                             "Welpen (Remus)":"Remus",
                             "Welpen (Romulus)":"Romulus",
                             "Welpen (woensdag)":"Welpen wo"}

    leiding_tuples = [(speleenheid2short_map.get(row["Speleenheid"], row["Speleenheid"]),
                       row["Lid voornaam"]) for row in lr]

    klein_array =   [1]     *4 + \
                    [2]     *4 + \
                    [3]     *4 + \
                    [4]     *4 + \
                    [5]     *4 + \
                    [6]     *4 + \
                    [7]     *4 + \
                    [8]     *4 + \
                    [9]     *4 + \
                    [10]    *4 + \
                    [11]    *4 + \
                    [12]    *4 + \
                    [13]    *4 + \
                    [14]    *4 + \
                    [15]    *4 + \
                    [16]    *4 + \
                    [17]    *4 + \
                    [18]    *4 + \
                    [19]    *4 + \
                    [20]    *4 + \
                    [21]    *4 + \
                    [22]    *4 + \
                    [23]    *4 + \
                    [24]    *4# + \
#                    [25]    *4 + \
#                    [26]    *4 + \
#                    [27]    *4 + \
#                    [28]    *4
    # #print klein_array
    # klein_array = [1,2,3,4,5]
    groot_array =   [1]     * 4 + \
                    [2]     * 4 + \
                    [3]     * 4 + \
                    [4]     * 4 + \
                    [5]     * 4 + \
                    [6]     * 4 + \
                    [7]     * 4 + \
                    [8]     * 4 + \
                    [9]     * 4 + \
                    [10]    * 4 + \
                    [11]    * 4 + \
                    [12]    * 4 + \
                    [13]    * 4 + \
                    [14]    * 4 + \
                    [15]    * 4 + \
                    [16]    * 4 + \
                    [17]    * 4 + \
                    [18]    * 4 + \
                    [19]    * 4 + \
                    [20]    * 4 + \
                    [21]    * 4 + \
                    [22]    * 4 + \
                    [23]    * 4 + \
                    [24]    * 4 + \
                    [25]    * 4 + \
                    [26]    * 4 + \
                    [27]    * 4 + \
                    [28]    * 4

    print len(klein_array)+len(groot_array)

    with file(filename, "w+") as f:
        for html in main(klein_array, groot_array, leiding_tuples):
            f.write(html)
