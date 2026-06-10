import requests
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Allow cross-origin requests from HTML

# SurveyCTO Credentials
SCTO_EMAIL = "dflt2@sdpi.org"
SCTO_PASS = "Sdpi@dflt2"

# A session to keep cookies if SurveyCTO redirects or sets them
session = requests.Session()
# Use HTTP Basic Auth for SurveyCTO
session.auth = (SCTO_EMAIL, SCTO_PASS)

@app.route('/image')
def proxy_image():
    url = request.args.get('url')
    if not url:
        return "Missing url parameter", 400
    
    try:
        # Fetch from SurveyCTO using our authenticated session
        resp = session.get(url, stream=True)
        
        # Proxy the response back to the HTML client
        headers = {
            k: v for k, v in resp.headers.items() 
            if k.lower() not in ('content-encoding', 'content-length', 'transfer-encoding', 'connection')
        }
        return Response(resp.iter_content(chunk_size=8192), status=resp.status_code, headers=headers)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    print("Starting SurveyCTO Proxy Server on http://localhost:5000")
    print("Make sure your HTML is pointing to: http://localhost:5000/image?url=...")
    app.run(port=5000, debug=True)
