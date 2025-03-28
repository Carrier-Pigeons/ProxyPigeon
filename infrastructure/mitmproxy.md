# CTF issue
Since the CTF uses Python Flask for the /echo endpoint, Python Flask strictly requires a trailing / at the /echo endpiont, such that it is /echo/. If Python Flask encounters /echo, it will return a 308 permanent redirect. mitmproxy will return this redirect which will redirect to fingerprint.byu.edu. As such, we had to change our CTF homepage's /echo endpoints to /echo/ so that mitmproxy would not redirect to fingerprint.byu.edu


# Setup
Here are the steps to set up mitmproxy:
1. Set up a python virtual environment.
    - ```
      python3 -m venv myenv
      ```
    - ```
      source myenv/bin/activate
      ```
2. ```
    pip install mitmproxy
    ```
3. Download the certificates using certbot. See [Certificates.md](Certificates.md).
4. ```
    nohup mitmdump –mode reverse:https://fingerprint.byu.edu –listen-host 0.0.0.0 –listen-port 443 --set block_global=false --certs mitmproxy.httpcarrierpigeons.xyz=/etc/letsencrypt/live/mitmproxy.httpcarrierpigeons.xyz/combined.pem
    ```

# Testing
Steps to test after setting up with previous steps:
1. ```
    source myenv/bin/activate
    ```
2. ```
    mitmdump –mode reverse:https://fingerprint.byu.edu –listen-host 0.0.0.0 –listen-port 443 --set block_global=false --certs mitmproxy.httpcarrierpigeons.xyz=/etc/letsencrypt/live/mitmproxy.httpcarrierpigeons.xyz/combined.pem
    ```

Note that the nohup command has been ommitted from the testing command. Nohup redirects output, such as error messages, to a nohup.out file instead of the terminal, thus making testing a little more tedious. The utility of nohup is that it causes the proxy to continue running after the shell is terminated, rather than terminating together with the shell which is the default behavior.

