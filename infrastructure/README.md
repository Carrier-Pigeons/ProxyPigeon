# Overview
We tested 7 proxies (ended up dropping Muraena, see later). Some of them were malicious and others were benign. 

## Testing
We did some manual tests, testing for different browsers and operating systems. From these we generated yara rules. Then we exposed the reverse proxy URLs to some CTFs to generate large amounts of traffic. The CTF traffic is likely to have less variety, perhaps most of it will be firefox in a kali box. 

We created a custom logging module for the Apache wordpress server as well. This log includes the source IP. Since we know which proxy has which IP, we will use these IPs to verify the accuracy of our yara rules.

## Security/Legal
The default configurations for some proxies harvest credentials. Make sure to turn these off. Users could put us in legal trouble if we do not do so.

## Website Certificates blocked by BYU's firewall
BYU's firewall, and quirks within some proxies, caused some difficulties getting TLS certificates. See [Certificates.md](Certificates.md) for more info.

# CTFs in Digital Ocean
We are setting up our proxies using VMs in Digital Ocean for the CTFs. 

# Proxy issues

## Muraena
Muranea was omitted from the CTFs. Muraena was unable to recognize fingerprint.byu.edu's certificate and thus would return an error message. Originally we thought Muraena was unable to recognize it's own server's certificate, but looking at the browser we could see the certificate was valid. Toggling the ssl settings in the config file did not fix the problem.

## HTTP traffic for TinyProxy and Squid
We were unable to get TinyProxy and Squid working with certificates. We still hosted them on the CTFs but using http without the s.