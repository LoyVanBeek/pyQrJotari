#!/usr/bin/python

import sys, os, itertools
"""
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length < 3)
            {
                Console.WriteLine("GEBRUIK: BarcodeGenerator <aantal Klein> <aantal Groot> <outputbestand>");
            }

            int kleinAmount = int.Parse(args[0]);
            int grootAmount = int.Parse(args[1]);
            string outfile = args[2];

            TextWriter writer = new StreamWriter(outfile);

            HtmlTextWriter html = new HtmlTextWriter(writer);

            html.RenderBeginTag(HtmlTextWriterTag.Html);
                html.RenderBeginTag(HtmlTextWriterTag.Head);
                    html.RenderBeginTag(HtmlTextWriterTag.Title);
                        html.Write("JOTARI QR-codes");
                    html.RenderEndTag();
                html.RenderEndTag();
                html.AddStyleAttribute(HtmlTextWriterStyle.FontFamily, "Arial");
                html.AddStyleAttribute(HtmlTextWriterStyle.FontSize, "20");
                html.Write(html.NewLine);
                html.RenderBeginTag(HtmlTextWriterTag.Body);
                    //html.RenderBeginTag(HtmlTextWriterTag.Table);
                        WriteQrCodes(html, kleinAmount, grootAmount, 3); 
                    //html.RenderEndTag();
                html.RenderEndTag();
            html.RenderEndTag();

            writer.Close();
        }

        private static void WriteQrCodes(HtmlTextWriter html, int kleinAmount, int grootAmount, int repeat)
        {
            html.RenderBeginTag(HtmlTextWriterTag.Table);

                for (int klein = 1; klein <= kleinAmount; klein++)
                {
                    html.RenderBeginTag(HtmlTextWriterTag.Tr);
                    for (int i=0; i<repeat; i++)
                    {
                        html.RenderBeginTag(HtmlTextWriterTag.Td);
                        GroupDiv(html, "Klein", klein);
                        html.RenderEndTag();
                    }
                    html.RenderEndTag();
                } 
                for (int groot = 1; groot <= grootAmount; groot++)
                {
                    html.RenderBeginTag(HtmlTextWriterTag.Tr);
                    for (int i = 0; i < repeat; i++)
                    {
                        html.RenderBeginTag(HtmlTextWriterTag.Td);
                        GroupDiv(html, "Groot", groot);
                        html.RenderEndTag();
                    }
                    html.RenderEndTag();
                }

            html.RenderEndTag();
        }

        private static string GroupDiv(string category, int number, int x, int y)
        {
            string code = @"<div style='border: solid 1px; 
                                        text-align: center; 
                                        width:  300px; 
                                        margin: 10px
                                        top:    {1}px'
                                        left:   {2}px'>
                        <img src='http://qrcode.kaywa.com/img.php?s=8&d={0}' alt='qrcode'/>
                        <br>
                            {0}
                        </div>";
            string html = String.Format(code, category + number.ToString(), y, x);
            return html;
        }

        private static string GroupDiv(string category, int number)
        {
            string code = @"<div style='border: solid 1px; text-align: center; width: 300px; margin:10px'>
                        <img src='http://qrcode.kaywa.com/img.php?s=8&d={0}' alt='qrcode'/>
                        <br>
                        {0}
                        </div>";
            string html = String.Format(code, category + number.ToString());
            return html;
        }

        private static void GroupDiv(HtmlTextWriter html, string category, int number)
        {
            html.AddStyleAttribute("border",      "solid 2px");
            html.AddStyleAttribute("text-align",  "center");
            html.AddStyleAttribute("width",       "320px");
            html.AddStyleAttribute("margin",      "10px");
            html.RenderBeginTag(HtmlTextWriterTag.Div);

            string imgSource = string.Format("http://qrcode.kaywa.com/img.php?s=8&d={0}", category + number.ToString());
            html.AddAttribute("src", imgSource);
            html.RenderBeginTag(HtmlTextWriterTag.Img); 
            html.RenderEndTag();

            html.RenderBeginTag(HtmlTextWriterTag.Br);
            html.RenderEndTag();
            html.Write(category + number.ToString());

            html.RenderEndTag();
        }
    }
}
"""

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
    # return """<div style='border: solid 1px; 
    #                                     text-align: center; 
    #                                     width:  300px; 
    #                                     margin: 10px>
    #                     <img src='http://chart.apis.google.com/chart?chs=200x200&cht=qr&chld=|0&chl={0}' alt='{0}'/>
    #                     <br>
    #                         {0}
    #                     </div>""".format(code)

    return """\t\t\t\t\t<div style='border: solid 1px; text-align: center; width: 200px; height: 240px; margin: 5px; vertical-align:bottom; padding: 10px'>
    \t\t\t\t\t\t<br>
\t\t\t\t\t\t{0}
\t\t\t\t\t\t<img src="http://api.qrserver.com/v1/create-qr-code/?data={0}&#38;size=200x200&#38;prov=goqrme" alt="{0}" title=""/>
\t\t\t\t\t</div>""".format(code)
                        #http://qrcode.kaywa.com/img.php?s=8&d={0}
                        #http://chart.apis.google.com/chart?chs=200x200&cht=qr&chld=|0&chl={0}
                        #http://api.qrserver.com/v1/create-qr-code/?data={0}
                        
#     return """\t\t\t\t\t<div style='border: solid 1px; text-align: center; width: 200px;height: 220px; margin: 10px;'>
# \t\t\t\t\t\t<br>
# \t\t\t\t\t\t{0}
# \t\t\t\t\t</div>""".format(code)

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
