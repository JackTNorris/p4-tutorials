sudo nft add table input_table
sudo nft 'add chain input_table input {type filter hook input priority -300;}'
sudo nft 'add rule input_table input ip protocol udp udp checksum set 0'
