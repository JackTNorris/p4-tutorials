fuser -k 9090/tcp
p4c basic.p4
/home/jtnorris/behavioral-model/targets/simple_switch/simple_switch -i 1@s1-eth1 -i 2@s1-eth2 basic.json &
#simple_switch_CLI < rules.cmd
