loop
set topic "xbee"
areadsensor x
rdata x a b c
data message topic c
print message
send message 0 45
delay 1000
