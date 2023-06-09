for i in {1..50}
do
    python3 digest-receive.py stuff2.csv --terminate_after 100 >> digest.txt
done
