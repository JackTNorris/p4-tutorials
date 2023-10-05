for i in {1..10}
do
    python3 receive.py --terminate_after 5000 evaluation/new-0ms-5k/received-$i-pct.csv
done

