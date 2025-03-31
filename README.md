# ProxyPigeon - HTTP Fingerprinting for Proxy Detection

## Overview

ProxyPigeon is a research project performed by a 2024/2025 BYU Capstone Team in connection with Sandia National Labs.  

The project is focused on detecting malicious Adversary in the Middle (AitM) layer 7 proxies that are used to phish credentials & session cookies. We identified several key changes that these proxies make to HTTP headers as they forward requests, and proved that these changes can be used to successfully identify malicious traffic. 

## Our Research & Data

In order to verify that the HTTP header changes we identified could be used to detect malicious proxies, we gathered data at scale through Pearl CTF 2025. We set up a web server and configured it to log full HTTP requests and IP addresses. We also set up 7 different reverse proxies, some of them malicious and some benign. CTF participants visited our site with and without proxies, and we collected each request. The IP addresses were used to confirm which proxy each request passed through. Once we identified key changes that each proxy made to the HTTP headers, we created a series of yara rules to detect each kind of proxy. 

## Navigating This Repo

* [/ctf/](./ctf/) - All the files needed for the challenge we ran in Pearl CTF 2025.  

* [/infrastructure/](./infrastructure/) - Documentation on our testing infrastructure. The goal is that anyone could use this to recreate our setup.  

## Other Important Repos

* [yara_rule_tester](https://github.com/Carrier-Pigeons/yara_rule_tester) - All of our yara rules, and the python scripts needed to test the rules against our database of requests.

* [mod_http_fingerprint_log](https://github.com/Carrier-Pigeons/mod_http_fingerprint_log) - Our custom Apache module for logging HTTP headers along with SSL data