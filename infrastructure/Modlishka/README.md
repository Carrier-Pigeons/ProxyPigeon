# Modlishka

Modlishka was built from source and setup as a systemd service. 

Place configuration and executable files in the root user's home directory (same folder structure as they are here in GitHub). Edit the modlishka.json file as needed (proxyDomain, targetDomain, cert, and certKey parameters specifically). The existing .json configuration is largely based on Modlishka's example configuration for phishing google.com. 

Place the systemd file in /etc/systemd/system/ (again, same folder structure as in GitHub). Reload systemctl daemon so that it sees the new system service file:
```
sudo systemctl daemlon-reload
```

Enable and start the service created by the Podman quadlet:
```
sudo systemctl enable modlishka.service
sudo systemctl start modlishka.service
```

This will start Modlishka using the .json configuration file. 
