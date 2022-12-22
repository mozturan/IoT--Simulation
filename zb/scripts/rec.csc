//Receiver
loop
wait
read v
rdata v topic value
time t
printfile t topic value
print v
