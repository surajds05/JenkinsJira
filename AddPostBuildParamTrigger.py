import requests
from base64 import b64encode
import csv
import json

class PostBuildParamTtrigger():
    def addParamTrigger():
        with open('InputParams.json','r') as inputs:
            inputParams = json.load(inputs)
            jenkinsBaseURL = inputParams['jenkinsParams']['jenkinsURL']
            username = inputParams['jenkinsParams']['jenkinsUsername']
            password = inputParams['jenkinsParams']['jenkinsPassword']
            userAndPass = username + ':' + password
            userAndPassEncrypt = b64encode(bytes(userAndPass, "utf-8")).decode("utf-8")

        with open('JenkinsJobs.csv') as inputCSV:
            jobNames = csv.reader(inputCSV)
            next(jobNames, None)
            for i in jobNames:
                jenkinsApiURL = jenkinsBaseURL + i[0] + '/config.xml'
                userAndPass = b64encode(b"analytics:cerner").decode("ascii")
                jenkinsGetHeaders = {'Authorization': 'Basic %s' % userAndPassEncrypt}
                jenkinsPostHeader = {'Authorization': 'Basic %s' % userAndPassEncrypt, 'Content-Type': 'text/xml'}

                with open('ParamTriggerConfig.xml') as inputXML:
                    paramTriggerXMLNode = inputXML.read()

                final_xml = ""

                getRes = requests.get(jenkinsApiURL, jenkinsGetHeaders)
                if 'hudson.plugins.parameterizedtrigger.BuildTrigger' not in getRes.text:
                    for line in getRes.text.splitlines():
                        if "</publishers>" in line:
                            val = line.replace(line, paramTriggerXMLNode)
                            final_xml = final_xml+val+"</publishers>"
                        else:
                            final_xml = final_xml+line
                    postRes = requests.post(jenkinsApiURL, data=final_xml, headers=jenkinsPostHeader)
                    print(postRes.text)