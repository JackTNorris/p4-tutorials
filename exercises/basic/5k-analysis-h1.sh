for i in {1..20}
do
    python3 send.py --time_sent_file evaluation/5k/sent-$i-pct.csv --drop_indexes evaluation/5k/missing-5k-$i-pct.json pmu8_5k.csv
    sleep 10
done

