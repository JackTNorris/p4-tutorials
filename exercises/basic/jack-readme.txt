To get started:

- run "make run"

- xterm into s1

- run "./configure.sh" to configure the interfaces on the switches

- run "simple_switch_CLI < rules.cmd" to install the table add_entries

- run "python3 controller.py" to start listening for digest messages

- xterm into h1 and run "python3 receive.py"

- xterm into h2 and run "python3 send.py 10.0.2.2"

- You should see your packets arrive at h2 and print on s1

- If you go back to switch 2 and run "simple_switch_CLI", run "register_read frac_sec_regs <reg_num>" to see the most recently
stored fracsecs from packets (0 = most recent, 2 = least recent)
