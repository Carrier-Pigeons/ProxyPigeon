# Overview
We tested 7 proxies (ended up dropping Muraena, see later). Some of them were malicious and others were benign. 

## Testing
We did some manual tests, testing for different browsers and operating systems. From these we generated yara rules. Then we exposed the reverse proxy URLs to some CTFs to generate large amounts of traffic. The CTF traffic is likely to have less variety, perhaps most of it will be firefox in a kali box. 

We created a custom logging module for the Apache wordpress server as well. This log includes the source IP. Since we know which proxy has which IP, we will use these IPs to verify the accuracy of our yara rules.

## Security/Legal
The default configurations for some proxies harvest credentials. Make sure to turn these off. Users could put us in legal trouble if we do not do so.

# BYU wordpress website
We set up a wordpress website on a server obtained from the CSR.

## Website Certificates blocked by BYU's firewall
BYU's firewall, and quirks within some proxies, caused some difficulties getting TLS certificates. See [Certificates.md](Certificates.md) for more info.

## ssh
The BYU soc requested that we set up ssh on port 1337. They only allowed ssh on the internal network (the firewall blocked it on the external network), so we had to vpn into itc-vpn.byu.edu (the network our server was located at) using GlobalProtect.
There was an issue that ssh would not work when we had two NICs (the public and private NIC) on the web server. The ssh request would go to the server on the internal network but then be sent out to the void on the public network. To fix this we had to set up a static route so that all 10.0.0.0/8 traffic went out the NIC connected to the internal network.

# CTFs in Digital Ocean
We are setting up our proxies using VMs in Digital Ocean for the CTFs. 

# Proxy issues

## Muraena
Muranea was omitted from the CTFs. Muraena was unable to recognize fingerprint.byu.edu's certificate and thus would return an error message. Originally we thought Muraena was unable to recognize it's own server's certificate, but looking at the browser we could see the certificate was valid. Toggling the ssl settings in the config file did not fix the problem.

## HTTP traffic for TinyProxy and Squid
We were unable to get TinyProxy and Squid working with certificates. We still hosted them on the CTFs but using http without the s.
