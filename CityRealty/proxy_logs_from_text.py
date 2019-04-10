import pandas as pd
import json

def proxy():
    http = []
    https = []
    ftp = []
    with open('') as source:
        for line in source:
            data = json.loads(line)
            host = data['host']
            http_proxy = "http://" + host + ":80"
            https_proxy = "https://" + host + ":443"
            ftp_proxy = "ftp://" + host + ":21"
            http.append(http_proxy)
            https.append(https_proxy)
            ftp.append(ftp_proxy)
    df = pd.DataFrame([http, https, ftp]).T
    df.columns = ['http', 'https', 'ftp']
    return df
