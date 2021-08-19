
for f in results-*; do
  mv $f "${f%.*}"csv
done
