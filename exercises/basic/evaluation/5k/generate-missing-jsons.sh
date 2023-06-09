for i in {1..20}
do
    python3 ../generate_missing_indexes.py  -m $i --data_size 5000 -o missing-5k-$i-pct.json
done