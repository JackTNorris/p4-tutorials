for i in {1..20}
do
    python3 ../../send.py --time_sent_file sent-{$i}pct.csv --drop_indexes missing-5k-{$i}pct.csv ../../pmu8_5k.csv
    sleep 2
done

