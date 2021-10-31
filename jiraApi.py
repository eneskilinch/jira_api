import requests
from requests.auth import HTTPBasicAuth

from JiraUserInfo import user, apikey


class Jira:
    def __init__(self, user, apikey):
        self.user = user
        self.apikey = apikey
        self.qaEfforts = []
        self.keyLists = []
        self.adSoyad = input('ad soyad: ')
        self.searchq = 'https://winsider.atlassian.net/rest/api/2/user/search?query=' + self.adSoyad
        self.jql = 'https://winsider.atlassian.net/rest/api/2/search?jql='
        self.s = requests.Session()

    def getAccountID(self):
        response = self.s.get(self.searchq, auth = HTTPBasicAuth(self.user, self.apikey))
        data = response.json()
        self.accountID = data[0]['accountId']
        self.emailAddress = data[0]['emailAddress']

    def getIssues(self):
        query = (
            'assignee was ' + self.accountID + 
            ' AND status changed by ' + self.accountID + 
            ' from "QA InProg" to %28"QA Done", "UAT OPAM", BLOCKED%29 during %28startOfMonth(), endOfMonth()%29 ORDER BY cf[14664] ASC&maxResults=100'
        )
        response = self.s.get(self.jql+query, auth = HTTPBasicAuth(self.user, self.apikey))
        data = response.json()
        issues = data['issues']
        for issue in issues:
            self.qaEfforts.append(int(issue['fields']['customfield_14664']))
            self.keyLists.append(issue['key'])
        count = self.qaEfforts.count(0)
        print(f'email adres: {self.emailAddress}')
        print(f'toplam task: {len(self.qaEfforts)}')
        print(f'toplam efor: {sum(self.qaEfforts)}')
        print(f'eforsuz task: {count}')
        if count > 0:
            for i in range(count):
                print(f'eforsuz tasklar: {self.keyLists[i]}')


jira = Jira(user, apikey)
jira.getAccountID()
jira.getIssues()