import httplib2
from base64 import b64encode

base_url = 'https://jazz.cerner.com:9443/qm/'
http = httplib2.Http()
headers = {'Content-type': 'text/xml'}
username = 'SD056953'
password = 'Sd$@0502'
userAndPass = username + ':' + password
userAndPassEncrypt = b64encode(bytes(userAndPass, "utf-8")).decode("utf-8")
getHeaders = {'Authorization': 'Basic %s' % userAndPassEncrypt}
headers = {'Content-type': 'text/xml'}
resp, content = http.request(base_url + "/oslc/workitems/35452.xml", 'GET', headers=headers)
# content = http.request(base_url + "/oslc/workitems/35452.xml", 'GET', headers=getHeaders)
print(resp)