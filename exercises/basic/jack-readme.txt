To get started:

- run "make run"

- xterm into s1

- run "./start-switch" to compile the p4 code, configure the switch interfaces, populate the match action tables, and start the local controller

- xterm into h2 and run "python3 receive.py"

- xterm into h1 and run "python3 send.py 10.0.2.2"

- You should see your packets arrive at h2, with missing ones generated and shown on s1
