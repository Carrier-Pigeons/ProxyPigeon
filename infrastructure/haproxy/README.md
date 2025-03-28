# Steps for setup

1. Download the certificates using certbot.
2. Add the following to the /etc/haproxy/haproxy.cfg file:
    ```
    frontend http_front
	bind *:443 ssl crt /etc/letencrypt/live/haproxy.httpcarrierpigeons.xyz/combined.pem
	acl host_haproxy hdr(host) -i haproxy.httpcarrierpigeons.xyz
	use_backend http_backend if host_haproxy

    backend http_backend
	server server1 fingerprint.byu.edu:443 ssl verify none
    ```
3. ```
    systemctl restart haproxy
    ```