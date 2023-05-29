./configure.sh
sleep .5
simple_switch_CLI < rules.cmd
clear
python3 controller.py --terminate_after $1
