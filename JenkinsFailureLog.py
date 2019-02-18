import sys
import requests
import json
from base64 import b64encode
from CreateJiraREST import CreateJira

class GetJenkinsLog:
    def JenkinsGet(jobName):
        with open('InputParams.json','r') as inputs:
            inputParams = json.load(inputs)
            jenkinsBaseURL = inputParams['jenkinsParams']['jenkinsURL']
            username = inputParams['jenkinsParams']['jenkinsUsername']
            password = inputParams['jenkinsParams']['jenkinsPassword']

            userAndPass = username + ':' + password
            userAndPassEncrypt = b64encode(bytes(userAndPass, "utf-8")).decode("utf-8")

            jenkinsGetHeaders = {'Authorization': 'Basic %s' % userAndPassEncrypt}
            jenkinsGetURL = jenkinsBaseURL +jobName+'/lastUnsuccessfulBuild/testReport/api/json'

            getRes = requests.get(jenkinsGetURL, jenkinsGetHeaders)

            jenkinsLog = open(jobName+'_log.json', 'w')
            jenkinsLog.write(json.dumps(json.loads(getRes.text), indent=4, sort_keys=True))
            jenkinsLog.close()

if __name__ == '__main__':
    jobName = sys.argv[1]
    del sys.argv[1:]
    GetJenkinsLog.JenkinsGet(jobName=jobName)
    CreateJira.createJira(jobName=jobName)