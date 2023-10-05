for i in {1..10}
do
    ./start-switch.sh $(($i * 5000 / 100)) >> new_jpt_1ms_time.txt
    sleep 5
done

