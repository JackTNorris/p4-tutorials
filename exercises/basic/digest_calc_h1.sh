for i in {1..50}
do
    python3 send.py --time_sent_file stuff.csv pmu8_1k.csv --num_packet 100
    sleep 5
done
