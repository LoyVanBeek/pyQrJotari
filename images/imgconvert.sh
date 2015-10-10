for i in *.jpg; do convert "$i" "${i%.jpg}.gif"; done
for i in *.png; do convert "$i" "${i%.png}.gif"; done
for i in *.jpeg; do convert "$i" "${i%.jpeg}.gif"; done
