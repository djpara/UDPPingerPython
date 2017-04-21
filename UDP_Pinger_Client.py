import sys, time
from socket import *

# Constant
CRLF = "\r\n"

# Calculate average function
def ave(lst):
        total = 0
        for i in range (len(lst)):
                total += lst[i]
        return total/len(lst)

# Process command-line arguments
argv = sys.argv                   
if len(argv) < 2:
	print("Usage: python PingServer hostname port\n")
	sys.exit(-1)

# Get the server hostname and port as command line arguments
host = argv[1]
port = argv[2]
timeout = 1 # in second, change as needed

# Create UDP client socket
# Note the use of SOCK_DGRAM for UDP datagram packet
clientsocket = socket(AF_INET, SOCK_DGRAM)
# Set socket timeout as 1 second
clientsocket.settimeout(timeout)
# Command line argument is a string, change the port into integer
port = int(port)  
# Sequence number of the ping message
ptime = 0
# Packets transmitted
ptransmitted = 0
# Packets lost
plost = 0
# RTTs for each packet
rttlst = []

# Ping for 10 times
while ptime < 10: 
	ptime += 1
	# Format the message to be sent. 
        # use time.asctime() for currTime
	data =  "PING seq#="+ str(ptime) + str(" time="+time.asctime())+" "
	try:
	# Sent time. from time.time()
		RTTb = time.time()
	# Send the UDP packet with the ping message
		clientsocket.sendto(data.encode(),(host, port))
		ptransmitted += 1
	# Receive the server response
		message, address = clientsocket.recvfrom(1024)  
	# Received time. use time.time()
		RTTa = time.time()
	# Display the server response as an output
		print(message)
	# Round trip time is the difference between sent and received time
                rtt = int((RTTa-RTTb)*1000)
                rttlst.append(rtt)
		print("RTT: " + str(rtt)+" ms"+CRLF)
	except:
	# Server does not response
	# Assume the packet is lost
                plost += 1
		print ("Request timed out."+CRLF)
		continue

# Compute stats
preceived = ptransmitted-plost
ppacketloss = (float(plost)/ptransmitted)*100

# Min max ave variables
minimum = 0;
maximum = 0;
average = 0;

# Compute rtt min max ave if rttLst is not empty
if rttlst:
	minimum = min(rttlst)
	maximum = max(rttlst)
	average = ave(rttlst)

# Close the client socket
print("--- ping statistics ---"+CRLF+CRLF+str(ptransmitted)+" packets transmitted, "
      +str(preceived)+" received, "+str(ppacketloss)+"% packet loss"
      +CRLF+CRLF+"rtt min/avg/max = "+str(minimum)+" / "+str(average)+" / "
      +str(maximum)+" ms"+CRLF)
clientsocket.close()


 




