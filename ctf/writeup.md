# HTTP Carrier Pigeons

## Description
Challenge category: forensics

Challenge rating: easy

Give the following to competitors:
```
Modern threat actors are using layer 7 proxies to create phishing websites that are capable of stealing usernames, passwords, and session cookies, even when protected by 2FA. These proxies make slight changes to HTTP headers that we can use to identify them. 
We recently received the following two requests. You need to identify which proxies they've passed through. This website will help you. 
Flag format: pearl{proxyname1_proxyname2}
```
Limit the number of guesses to 5 in order to prevent brute forcing. 

Also give competitors `request1.log` & `request2.log`, which contain the requests. 

## Solve Theory
Competitors need to send a request through each proxy and identify what changes each time. As they start to develop a ruleset they can narrow the first proxy down to HAproxy and the second proxy down to Evilginx. 

## Hosting
Hosting for this challenge is pretty complex. It requires no less than 9 dedicated public IP addresses so that the web traffic doesn't need to pass through any extra proxies. 

For Pearl CTF the challenge is being hosted by BYU Cyberia. The following servers, domain names, and IP addresses are being used:

* Apache Web Server - fingerprint.byu.edu - 128.187.49.100
* Evilginx - evilginx.httpcarrierpigeons.xyz - 152.42.144.176
* Modlishka - modlishka.httpcarrierpigeons.xyz - 159.223.246.244
* Traefik - traefik.httpcarrierpigeons.xyz - 157.230.193.72
* Mitmproxy - mitmproxy.httpcarrierpigeons.xyz - 164.90.244.123
* Squid - squid.httpcarrierpigeons.xyz - 159.203.55.228
* HAProxy - haproxy.httpcarrierpigeons.xyz - 170.64.248.63
* Tinyproxy - tinyproxy.httpcarrierpigeons.xyz - 209.38.52.54

The Apache server is set up to echo back as the response whatever HTTP request it receives. The rest of the servers are acting as reverse proxies to the Apache server. 