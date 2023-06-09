for i in {1..20}
do
    ./start-switch.sh $(($i * 5000 / 100))
    sleep 4
done

