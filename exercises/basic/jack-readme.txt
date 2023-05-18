To get started:

- run "make run"

- xterm into s1

- run "./start-switch" to compile the p4 code, configure the switch interfaces, populate the match action tables, and start the local controller

- xterm into h2 and run "python3 receive.py"

- if you want missing data:

a) run "python3 evaluation/generate_missing_indexes.py -m <number missing packets> -o <missing index json file you want> --data_size <number of packets you're sending from h1>"
b) xterm into h1 and run "python3 send.py pmu12.csv --drop_indexes <name of generated json> --ip 10.0.2.2"

- otherwise:

- xterm into h1 and run "python3 send.py pmu12.csv --ip 10.0.2.2"

- You should see your packets arrive at h2, with missing ones generated and shown on s1
