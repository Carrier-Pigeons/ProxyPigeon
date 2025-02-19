from flask import Flask, request, jsonify
import yara

app = Flask(__name__)

rules = {
    "modlishka": yara.compile(filepath="rules/modlishka.yar"),
    "traefik": yara.compile(filepath="rules/traefik.yar"),
    "muraena": yara.compile(filepath="rules/muraena.yar"),
    "mitmproxy": yara.compile(filepath="rules/mitmproxy.yar")
}

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/process_log', methods=['POST'])
def process_log():
    data = request.get_json()
    log_text = data.get('logText')

    if not log_text:
        return jsonify({"error": "No log text provided"}), 400

    # Scan with each rule
    matches = {}
    for name, rule in rules.items():
        match = rule.match(data=log_text)
        if match:
            matches[name] = [m.rule for m in match]

    # Return detected proxies
    if matches:
        detected = [{"proxy": proxy, "rules_triggered": results} for proxy, results in matches.items()]
        return jsonify({"proxy_detected": True, "details": detected})
    else:
        return jsonify({"proxy_detected": False, "details": []})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
