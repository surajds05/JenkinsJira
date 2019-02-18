from base64 import b64encode
import requests
import json

class CreateJira():
    def createJira(jobName):
        with open('InputParams.json','r') as inputs:
            inputParams = json.load(inputs)
            jiraURL = inputParams['jiraParams']['jiraURL']
            username = inputParams['jiraParams']['jiraUsername']
            password = inputParams['jiraParams']['jiraPassword']
            data = inputParams['jiraParams']['JiraJsonData']

            inputParams['jiraParams']['JiraJsonData']['fields']['summary'] = jobName+" failed"
            inputParams['jiraParams']['JiraJsonData']['fields']['description'] = "Creating an issue due to failure of " + jobName +".\n Attached the log for your reference"

            userAndPass = username + ':' + password
            userAndPassEncrypt = b64encode(bytes(userAndPass, "utf-8")).decode("utf-8")
            jiraPostHeaders = {'Authorization': 'Basic %s' % userAndPassEncrypt, 'Content-Type': 'application/json'}

            data = json.dumps(data)
            createJiraReq = requests.post(url=jiraURL, data=data, headers=jiraPostHeaders)
            print(createJiraReq.json()['key'] + " has been created to track the failure of " + jobName )

            attachmentURL = jiraURL + createJiraReq.json()['key'] + '/attachments/'
            attachmentHeaders = {'Authorization': 'Basic %s' % userAndPassEncrypt, 'X-Atlassian-Token': 'no-check'}
            attachmentData = inputParams['jiraParams']['attachmentJsonData']

            inputParams['jiraParams']['attachmentJsonData']['filename'] = jobName + '_log.json'
            data = json.dumps(attachmentData)
            file = inputParams['jiraParams']['fileJsonData']
            inputParams['jiraParams']['fileJsonData']['file'] = open(jobName+'_log.json', 'r')
            attachmentReq = requests.post(attachmentURL, files= file , headers=attachmentHeaders)