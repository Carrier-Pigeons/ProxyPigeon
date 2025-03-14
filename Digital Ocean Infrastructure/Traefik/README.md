# Traefik

Traefik was installed as a Podman container. 

Install Podman:
```
sudo apt install podman
```

Place all configuration files in the root user's home directory (same folder structure as they are here in GitHub). Make sure the acme.json file has permissions of 600. Edit the config.yml file to change the proxy domain and change where you are pointing to (either an IP address or another domain).

Place the Podman quadlet file in /etc/containers/systemd/ (again, same folder structure as in GitHub). Reload systemctl daemon so that it sees the new Podman quadlet file:
```
sudo systemctl daemon-reload
```

Enable and start the service created by the Podman quadlet:
```
sudo systemctl enable traefik.service
sudo systemctl start traefik.service
```

This will pull and use the latest version of Traefik. For the data collection portion of our study, that was version 3.3.4.
