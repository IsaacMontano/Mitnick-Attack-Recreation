This project is a recreation of the Mitnick Attack to further understand the relationship between SYN and ACK packets. 
This was a collaboration between myself, Isaac Montano, and Jasmin Gonzalez. 
This project's idea and tasks were provided by SeedLabs and assistance was provided by Dr. Lavanya Mandava from Bradley University. 

Abstract
------------------
The Mitnick attack was created and named after Kevin Mitnick, one of the most well-known hackers in the US and on the FBI’s most wanted list. 
Mitnick successfully launched an attack on Tsutomu Shimomura, a researcher working at the San Diego Supercomputer Center on cellular phone 
network security. Mitnick exploited vulnerabilities in the TCP protocol and trusted relationship between two of Shimomura’s computers with 
the aim of accessing code he needed to hack into the cellular network. Host A was the machine that Mitnick wanted to attack and Host B was 
a trusted server. Mitnick had to impersonate the trusted server so he did not need to provide a password for Host A. 

![model](https://github.com/IsaacMontano/Mitnick-Attack-Recreation/blob/main/mitnick%20presentation%20photos/Abstract.png)

The Attack: How it Works?
-
1) Sequence Number Prediction: 
  Mitnick sent SYN requests to Machine A and received SYN+ACK responses. Then he sent RESET packet to Machine A.
After repeating this 20 times, he found the pattern between two successive TCP ISNs which allowed him to predict future ISNs.
2) SYN Flooding Attack on the Trusted Server:
  Mitnick needed to send out a SYN packet from the trusted server to Machine A. To override the 3-way handshake,
Mitnick launched a SYN flooding attack to shutdown the trusted server and silence it from sending RESET packets back to Machine A.
3) Spoofing a TCP Connection: 
He created a TCP connection between the two machines and then ran a remote shell inside this connection. A SYN request was sent to
machine A using the trusted server’s IP as the source IP address. The trusted server could not send the reset packets due to being silenced.
An ACK packet was spoofed to secure the connection, which must acknowledge the sequence number in Machine A’s SYN+ACK packet. Due to the
prior investigation, Mitnick was able to predict what this number was. 
4) Running the Remote Shell: 
Using the established TCP connection, Mitnick remote shelled into Machine A, asking it to run a command. He created a backdoor so he can repeat
login without repeating the attack.

Task 1: Simulated SYN Flooding:
-
To simulate the SYN flooding that Mitnick preformed previously, we shut off the server so that the trusted machine and server could not communicate with 
each other. While this is a simple task, we need to ensure that there are no packets shared between both computers and modern networking advancements makes 
actually SYN flooding difficult. Since the SYN flooding was not the main focus ofthe project, we accepted this solution. As server needed to be shutdown, We 
need to ensure that the data from ARP table would not go away. We set a flag so Machine A knows to keep the ipand MAC addresses from the server permanently.

![model](https://github.com/IsaacMontano/Mitnick-Attack-Recreation/blob/main/mitnick%20presentation%20photos/task1%20simulated%20syn%20flooding.png)
example of the trusted machine's ARP table

Task 2.1 Spoof 1st TCP connection: 
![model](https://github.com/IsaacMontano/Mitnick-Attack-Recreation/blob/main/mitnick%20presentation%20photos/Task2_1%20spoof%201st%20tcp.png)
Following code spoofed a SYN packet sent as the "trusted server" to Machine A to initialize the 3 way handshake. In the main() function, we implemented 
time.sleep for 10 seconds to wait for Machine A to send back a [ACK, SYN] packet to our attacker machine. Our spoof_pkt function then sends back another 
packet in response to finish the 3 way handshake. Notice, the variables from spoof_pkt, specifically the sequence number, have to be based on the previous
packet to keep the 3 way handshake successful. 


**Results**
![Model](https://github.com/IsaacMontano/Mitnick-Attack-Recreation/blob/main/mitnick%20presentation%20photos/task2_1%20results.png)
Results captured from Wireshark. The 1st line is the 3 way handshake being initialized, the 3rd line is Machine A's response, and the 7th line is the completed
handshake from our end. 

Task 2.1.1: Spoofing a rsh packet:
-
We need to add a section in our previous code for a spoofed RSH packet. 
![model](https://github.com/IsaacMontano/Mitnick-Attack-Recreation/blob/main/mitnick%20presentation%20photos/task2_1_1%20spoofing%20rsh%20packet.png)
We can see that Wireshark shows that our RSH packet was sent successfully and a session was "established", however, no data can be sent through _yet_.

Task 2.2: Spoofing a 2nd TCP connection:
-
We need to create another packet to continue the TCP connectino past the handshake. This connection will be used for our RSH packet. If this does not
take place, the rsh session will stop. The following program spoofs a SYN+ACK response to the recieved SYN packet from Machine A. 

We can also see our wireshark results. Our code is shown successul from the last packet in this next screenshot, and the connection is continued!
![model](https://github.com/IsaacMontano/Mitnick-Attack-Recreation/blob/main/mitnick%20presentation%20photos/task2_2%20spoofing%202nd%20tcp.png)
