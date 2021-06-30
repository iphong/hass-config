#!bin/bash

sudo printf %"s\n" \
"interface=wlan0" \
"driver=nl80211" \
"ssid=BorderRouter-AP" \
"hw_mode=g" \
"channel=6" \
"ieee80211n=1" \
"wmm_enabled=1" \
"ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]" \
"macaddr_acl=0" \
"auth_algs=1" \
"ignore_broadcast_ssid=0" \
"wpa=2" \
"wpa_key_mgmt=WPA-PSK" \
"wpa_passphrase=12345678" \
"rsn_pairwise=CCMP" > /etc/hostapd/hostapd.conf


echo "DAEMON_CONF=\"/etc/hostapd/hostapd.conf\"" >> /etc/default/hostapd

systemctl unmask hostapd
systemctl start hostapd

# Create file /etc/systemd/system/hostapd.service

printf %"s\n" \
"[Unit]" \
"Description=Hostapd IEEE 802.11 Access Point" \
"After=sys-subsystem-net-devices-wlan0.device" \
"BindsTo=sys-subsystem-net-devices-wlan0.device" \
"" \
"[Service]" \
"Type=forking" \
"PIDFile=/var/run/hostapd.pid" \
"ExecStart=/usr/sbin/hostapd -B /etc/hostapd/hostapd.conf -P /var/run/hostapd.pid" \
"" \
"[Install]" \
"WantedBy=multi-user.target" > /etc/systemd/system/hostapd.service


echo "service hostapd start" >> /etc/rc.local
