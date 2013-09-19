#!/usr/bin/python

import sys, os, itertools

def main(klein, groot):

    yield """<html>\n\t<head>\n\t\t<title>\n\t\t\tJotari QR Codes\n\t\t</title>\n\t</head>\n\t"""
    yield """<body style="font-family:arial; font-size:20px">"""

    yield "\n".join(write_QRcodes(klein, groot))

    yield """\n\t</body></html>"""

def write_QRcodes(klein, groot, columns=4):
    rows, rest = divmod(len(klein)+len(groot), columns)
    if rest:
        rows += 1 #if there is a rest left after the divmod, make one more row.

    klein_cells = generate_cells("klein", klein)
    groot_cells = generate_cells("groot", groot)
    cells = iter(sorted(list(itertools.chain(klein_cells, groot_cells))))

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
    address = "http://www.scoutingboxtel.nl/qr/{0}.asp".format(code)
    return """\t\t\t\t\t<div style='border: solid 1px; text-align: center; width: 200px; height: 240px; margin: 5px; vertical-align:bottom; padding: 10px'>
    \t\t\t\t\t\t<br>
\t\t\t\t\t\t{0}
\t\t\t\t\t\t<img src="http://api.qrserver.com/v1/create-qr-code/?data={1}&#38;size=200x200&#38;prov=goqrme" alt="{0}" title=""/>
\t\t\t\t\t</div>""".format(code, address)

def generate_cells(text, numbers):
    for i in numbers:
        code = text+str(i)
        yield generate_cell(code)

if __name__ == "__main__":
    filepath = sys.argv[1]

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
                    [24]    *4 + \
                    [25]    *4 + \
                    [26]    *4 + \
                    [27]    *4 + \
                    [28]    *4
    # #print klein_array
    # klein_array = [1,2,3,4,5]
    groot_array =   [1]     * 3 + \
                    [2]     * 3 + \
                    [3]     * 3 + \
                    [4]     * 3 + \
                    [5]     * 3 + \
                    [6]     * 3 + \
                    [7]     * 3 + \
                    [8]     * 3 + \
                    [9]     * 3 + \
                    [10]    * 3 + \
                    [11]    * 3 + \
                    [12]    * 3 + \
                    [13]    * 3 + \
                    [14]    * 3 + \
                    [15]    * 3 + \
                    [16]    * 3 + \
                    [17]    * 3 + \
                    [18]    * 3 + \
                    [19]    * 3 + \
                    [20]    * 3 + \
                    [21]    * 3 + \
                    [22]    * 3 + \
                    [23]    * 3 + \
                    [24]    * 3 

    print len(klein_array)+len(groot_array)

    with file(filepath, "w+") as f:
        for html in main(klein_array, groot_array):
            f.write(html)
