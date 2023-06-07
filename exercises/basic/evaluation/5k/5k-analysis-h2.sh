for i in {1..20}
do
    python3 ../../receive.py --terminate_after 5000 received-{$i}pct.csv
done

