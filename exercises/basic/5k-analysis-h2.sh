for i in {1..20}
do
    python3 receive.py --terminate_after 5000 evaluation/5k/received-$i-pct.csv
done

