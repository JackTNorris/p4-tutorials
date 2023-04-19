kill $(netstat -ap | grep 9090 | awk '{print }' | grep /simple_switch | cut -d '/' -f 1)
