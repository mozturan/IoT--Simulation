loop
areadsensor v
set topic "random"
if(v!="X")
	print v
	rdata v a b c
	data message topic c
	send message 43
end
delay 1000