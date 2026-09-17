version=`grep -o '\d\+\.\d\+\.\d\+' package.json`
today=`date +'%Y-%m-%d'`
sed -i.bak "s/^version:.*$/version: $version/g" CITATION.cff && rm -f CITATION.cff.bak
sed -i.bak "s/^date-released:.*$/date-released: \'$today\'/g" CITATION.cff && rm -f CITATION.cff.bak
