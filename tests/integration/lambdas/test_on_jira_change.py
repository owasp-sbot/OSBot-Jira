from osbot_utils.utils.Dev import Dev

from gw_bot.Deploy import Deploy
from osbot_aws.apis.Lambda import Lambda

from osbot_aws.helpers.Test_Helper import Test_Helper
from osbot_jira.lambdas.on_jira_change import run


class test_lambda_gsbot_gs_jira(Test_Helper):

    def setUp(self):
        super().setUp()
        self.lambda_name = 'osbot_jira.lambdas.on_jira_change'
        self.aws_lambda = Lambda(self.lambda_name)
        self.result     = None

    def tearDown(self):
        if self.result is not None:
            Dev.pprint(self.result)

    def test_lambda_update(self):
        Deploy().deploy_lambda__jira(self.lambda_name)

    def test_lambda_update_and_invoke(self):
        self.test_lambda_update()
        payload = {'an_field' : 42}
        self.result = self.aws_lambda.invoke(payload)



    def test_direct_invoke_issue_link_deleted(self):
        body = '{"timestamp":1580287523796,"webhookEvent":"jira:issue_deleted","user":{"self":"https://glasswall.atlassian.net/rest/api/2/user?accountId=5dee69782c44a60edee17525","accountId":"5dee69782c44a60edee17525","avatarUrls":{"48x48":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=48&s=48","24x24":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=24&s=24","16x16":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=16&s=16","32x32":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=32&s=32"},"displayName":"Dinis Cruz","active":true,"timeZone":"America/Chicago","accountType":"atlassian"},"issue":{"id":"10977","self":"https://glasswall.atlassian.net/rest/api/2/10977","key":"TASK-23","fields":{"statuscategorychangedate":"2020-01-28T18:45:58.098-0600","customfield_10070":null,"fixVersions":[],"resolution":null,"lastViewed":"2020-01-28T18:49:45.745-0600","customfield_10060":null,"customfield_10061":null,"customfield_10062":null,"customfield_10063":null,"customfield_10065":null,"customfield_10066":null,"customfield_10067":null,"priority":{"self":"https://glasswall.atlassian.net/rest/api/2/priority/3","iconUrl":"https://glasswall.atlassian.net/images/icons/priorities/medium.svg","name":"Medium","id":"3"},"customfield_10068":null,"customfield_10069":null,"labels":[],"timeestimate":null,"aggregatetimeoriginalestimate":null,"versions":[],"issuelinks":[],"assignee":null,"status":{"self":"https://glasswall.atlassian.net/rest/api/2/status/1","description":"The issue is open and ready for the assignee to start work on it.","iconUrl":"https://glasswall.atlassian.net/images/icons/statuses/open.png","name":"Open","id":"1","statusCategory":{"self":"https://glasswall.atlassian.net/rest/api/2/statuscategory/2","id":2,"key":"new","colorName":"blue-gray","name":"To Do"}},"components":[],"customfield_10050":null,"customfield_10051":null,"customfield_10052":null,"customfield_10053":null,"customfield_10054":null,"customfield_10055":null,"customfield_10056":null,"customfield_10057":null,"customfield_10058":null,"customfield_10059":null,"customfield_10049":null,"aggregatetimeestimate":null,"creator":{"self":"https://glasswall.atlassian.net/rest/api/2/user?accountId=5dee69782c44a60edee17525","name":"dcruz","key":"dcruz","accountId":"5dee69782c44a60edee17525","avatarUrls":{"48x48":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=48&s=48","24x24":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=24&s=24","16x16":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=16&s=16","32x32":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=32&s=32"},"displayName":"Dinis Cruz","active":true,"timeZone":"America/Chicago","accountType":"atlassian"},"subtasks":[],"customfield_10040":null,"customfield_10041":null,"customfield_10042":null,"customfield_10043":null,"reporter":{"self":"https://glasswall.atlassian.net/rest/api/2/user?accountId=5dee69782c44a60edee17525","name":"dcruz","key":"dcruz","accountId":"5dee69782c44a60edee17525","avatarUrls":{"48x48":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=48&s=48","24x24":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=24&s=24","16x16":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=16&s=16","32x32":"https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=32&s=32"},"displayName":"Dinis Cruz","active":true,"timeZone":"America/Chicago","accountType":"atlassian"},"aggregateprogress":{"progress":0,"total":0},"customfield_10044":null,"customfield_10045":[],"customfield_10046":null,"customfield_10047":null,"customfield_10048":null,"customfield_10038":null,"progress":{"progress":0,"total":0},"votes":{"self":"https://glasswall.atlassian.net/rest/api/2/issue/TASK-23/votes","votes":0,"hasVoted":false},"worklog":{"startAt":0,"maxResults":20,"total":0,"worklogs":[]},"issuetype":{"self":"https://glasswall.atlassian.net/rest/api/2/issuetype/10001","id":"10001","description":"A small, distinct piece of work.","iconUrl":"https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10541&avatarType=issuetype","name":"Task","subtask":false,"avatarId":10541},"timespent":null,"customfield_10030":0.0,"customfield_10031":0.0,"project":{"self":"https://glasswall.atlassian.net/rest/api/2/project/10000","id":"10000","key":"TASK","name":"Tasks","projectTypeKey":"business","simplified":false,"avatarUrls":{"48x48":"https://glasswall.atlassian.net/secure/projectavatar?pid=10000&avatarId=10519","24x24":"https://glasswall.atlassian.net/secure/projectavatar?size=small&s=small&pid=10000&avatarId=10519","16x16":"https://glasswall.atlassian.net/secure/projectavatar?size=xsmall&s=xsmall&pid=10000&avatarId=10519","32x32":"https://glasswall.atlassian.net/secure/projectavatar?size=medium&s=medium&pid=10000&avatarId=10519"}},"customfield_10032":1.0,"customfield_10033":null,"customfield_10034":null,"aggregatetimespent":null,"customfield_10035":null,"customfield_10036":null,"customfield_10037":null,"customfield_10028":0.0,"customfield_10029":0.0,"resolutiondate":null,"workratio":-1,"watches":{"self":"https://glasswall.atlassian.net/rest/api/2/issue/TASK-23/watchers","watchCount":1,"isWatching":true},"created":"2020-01-28T18:45:57.987-0600","customfield_10020":null,"customfield_10021":null,"customfield_10022":null,"customfield_10023":null,"customfield_10016":null,"customfield_10017":null,"customfield_10018":{"hasEpicLinkFieldDependency":false,"showField":false,"nonEditableReason":{"reason":"PLUGIN_LICENSE_ERROR","message":"Portfolio for Jira must be licensed for the Parent Link to be available."}},"customfield_10019":"0|i005vb:","updated":"2020-01-29T02:42:10.538-0600","timeoriginalestimate":null,"description":"aaaaaa","customfield_10010":null,"customfield_10014":null,"timetracking":{},"customfield_10015":null,"customfield_10005":null,"customfield_10006":null,"customfield_10007":null,"security":null,"customfield_10008":null,"attachment":[],"customfield_10009":null,"summary":"Test task 123","customfield_10000":"{}","customfield_10001":null,"customfield_10002":null,"customfield_10003":null,"customfield_10004":null,"environment":null,"duedate":null,"comment":{"comments":[],"maxResults":0,"total":0,"startAt":0}}}}'
        payload = {'body': body}
        self.result = run(payload, {})

    def test_data(self):
    
        data = {
  "timestamp": 1580257954906,
  "webhookEvent": "jira:issue_updated",
  "issue_event_type_name": "issue_updated",
  "user": {
    "self": "https://glasswall.atlassian.net/rest/api/2/user?accountId=5dee69782c44a60edee17525",
    "accountId": "5dee69782c44a60edee17525",
    "avatarUrls": {
      "48x48": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=48&s=48",
      "24x24": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=24&s=24",
      "16x16": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=16&s=16",
      "32x32": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=32&s=32"
    },
    "displayName": "Dinis Cruz",
    "active": True,
    "timeZone": "America/Chicago",
    "accountType": "atlassian"
  },
  "issue": {
    "id": "10105",
    "self": "https://glasswall.atlassian.net/rest/api/2/10105",
    "key": "SQUAD-10",
    "fields": {
      "statuscategorychangedate": "2019-12-09T20:47:41.025-0600",
      "customfield_10070": None,
      "fixVersions": [
        
      ],
      "resolution": None,
      "lastViewed": "2020-01-28T18:29:20.997-0600",
      "customfield_10060": None,
      "customfield_10061": None,
      "customfield_10062": None,
      "customfield_10063": None,
      "customfield_10065": None,
      "customfield_10066": None,
      "customfield_10067": None,
      "priority": {
        "self": "https://glasswall.atlassian.net/rest/api/2/priority/3",
        "iconUrl": "https://glasswall.atlassian.net/images/icons/priorities/medium.svg",
        "name": "Medium",
        "id": "3"
      },
      "customfield_10068": None,
      "customfield_10069": None,
      "labels": [
        "needs-description"
      ],
      "aggregatetimeoriginalestimate": None,
      "timeestimate": None,
      "versions": [
        
      ],
      "issuelinks": [
        {
          "id": "10155",
          "self": "https://glasswall.atlassian.net/rest/api/2/issueLink/10155",
          "type": {
            "id": "10018",
            "name": "Outcome",
            "inward": "has outcome",
            "outward": "is outcome of",
            "self": "https://glasswall.atlassian.net/rest/api/2/issueLinkType/10018"
          },
          "inwardIssue": {
            "id": "10126",
            "key": "OUTCOME-3",
            "self": "https://glasswall.atlassian.net/rest/api/2/issue/10126",
            "fields": {
              "summary": "Implement Security Projects that align with CISO objectives",
              "status": {
                "self": "https://glasswall.atlassian.net/rest/api/2/status/10009",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/statuses/generic.png",
                "name": "Draft",
                "id": "10009",
                "statusCategory": {
                  "self": "https://glasswall.atlassian.net/rest/api/2/statuscategory/2",
                  "id": 2,
                  "key": "new",
                  "colorName": "blue-gray",
                  "name": "To Do"
                }
              },
              "priority": {
                "self": "https://glasswall.atlassian.net/rest/api/2/priority/3",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/priorities/medium.svg",
                "name": "Medium",
                "id": "3"
              },
              "issuetype": {
                "self": "https://glasswall.atlassian.net/rest/api/2/issuetype/10010",
                "id": "10010",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10539&avatarType=issuetype",
                "name": "Outcome",
                "subtask": False,
                "avatarId": 10539
              }
            }
          }
        },
        {
          "id": "10252",
          "self": "https://glasswall.atlassian.net/rest/api/2/issueLink/10252",
          "type": {
            "id": "10016",
            "name": "Squad - Developer",
            "inward": "has squad developer",
            "outward": "is squad developer of",
            "self": "https://glasswall.atlassian.net/rest/api/2/issueLinkType/10016"
          },
          "inwardIssue": {
            "id": "10037",
            "key": "PERSON-17",
            "self": "https://glasswall.atlassian.net/rest/api/2/issue/10037",
            "fields": {
              "summary": "Max Bussell",
              "status": {
                "self": "https://glasswall.atlassian.net/rest/api/2/status/10006",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/statuses/generic.png",
                "name": "Active",
                "id": "10006",
                "statusCategory": {
                  "self": "https://glasswall.atlassian.net/rest/api/2/statuscategory/4",
                  "id": 4,
                  "key": "indeterminate",
                  "colorName": "yellow",
                  "name": "In Progress"
                }
              },
              "priority": {
                "self": "https://glasswall.atlassian.net/rest/api/2/priority/3",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/priorities/medium.svg",
                "name": "Medium",
                "id": "3"
              },
              "issuetype": {
                "self": "https://glasswall.atlassian.net/rest/api/2/issuetype/10003",
                "id": "10003",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10512&avatarType=issuetype",
                "name": "Person",
                "subtask": False,
                "avatarId": 10512
              }
            }
          }
        },
        {
          "id": "10249",
          "self": "https://glasswall.atlassian.net/rest/api/2/issueLink/10249",
          "type": {
            "id": "10016",
            "name": "Squad - Developer",
            "inward": "has squad developer",
            "outward": "is squad developer of",
            "self": "https://glasswall.atlassian.net/rest/api/2/issueLinkType/10016"
          },
          "inwardIssue": {
            "id": "10039",
            "key": "PERSON-19",
            "self": "https://glasswall.atlassian.net/rest/api/2/issue/10039",
            "fields": {
              "summary": "Lewis Henderson",
              "status": {
                "self": "https://glasswall.atlassian.net/rest/api/2/status/10006",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/statuses/generic.png",
                "name": "Active",
                "id": "10006",
                "statusCategory": {
                  "self": "https://glasswall.atlassian.net/rest/api/2/statuscategory/4",
                  "id": 4,
                  "key": "indeterminate",
                  "colorName": "yellow",
                  "name": "In Progress"
                }
              },
              "priority": {
                "self": "https://glasswall.atlassian.net/rest/api/2/priority/3",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/priorities/medium.svg",
                "name": "Medium",
                "id": "3"
              },
              "issuetype": {
                "self": "https://glasswall.atlassian.net/rest/api/2/issuetype/10003",
                "id": "10003",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10512&avatarType=issuetype",
                "name": "Person",
                "subtask": False,
                "avatarId": 10512
              }
            }
          }
        },
        {
          "id": "10952",
          "self": "https://glasswall.atlassian.net/rest/api/2/issueLink/10952",
          "type": {
            "id": "10016",
            "name": "Squad - Developer",
            "inward": "has squad developer",
            "outward": "is squad developer of",
            "self": "https://glasswall.atlassian.net/rest/api/2/issueLinkType/10016"
          },
          "inwardIssue": {
            "id": "10041",
            "key": "PERSON-21",
            "self": "https://glasswall.atlassian.net/rest/api/2/issue/10041",
            "fields": {
              "summary": "Abbas Haidar",
              "status": {
                "self": "https://glasswall.atlassian.net/rest/api/2/status/10006",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/statuses/generic.png",
                "name": "Active",
                "id": "10006",
                "statusCategory": {
                  "self": "https://glasswall.atlassian.net/rest/api/2/statuscategory/4",
                  "id": 4,
                  "key": "indeterminate",
                  "colorName": "yellow",
                  "name": "In Progress"
                }
              },
              "priority": {
                "self": "https://glasswall.atlassian.net/rest/api/2/priority/3",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/priorities/medium.svg",
                "name": "Medium",
                "id": "3"
              },
              "issuetype": {
                "self": "https://glasswall.atlassian.net/rest/api/2/issuetype/10003",
                "id": "10003",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10512&avatarType=issuetype",
                "name": "Person",
                "subtask": False,
                "avatarId": 10512
              }
            }
          }
        },
        {
          "id": "10251",
          "self": "https://glasswall.atlassian.net/rest/api/2/issueLink/10251",
          "type": {
            "id": "10016",
            "name": "Squad - Developer",
            "inward": "has squad developer",
            "outward": "is squad developer of",
            "self": "https://glasswall.atlassian.net/rest/api/2/issueLinkType/10016"
          },
          "inwardIssue": {
            "id": "10046",
            "key": "PERSON-26",
            "self": "https://glasswall.atlassian.net/rest/api/2/issue/10046",
            "fields": {
              "summary": "Harry Georgiou",
              "status": {
                "self": "https://glasswall.atlassian.net/rest/api/2/status/10006",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/statuses/generic.png",
                "name": "Active",
                "id": "10006",
                "statusCategory": {
                  "self": "https://glasswall.atlassian.net/rest/api/2/statuscategory/4",
                  "id": 4,
                  "key": "indeterminate",
                  "colorName": "yellow",
                  "name": "In Progress"
                }
              },
              "priority": {
                "self": "https://glasswall.atlassian.net/rest/api/2/priority/3",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/priorities/medium.svg",
                "name": "Medium",
                "id": "3"
              },
              "issuetype": {
                "self": "https://glasswall.atlassian.net/rest/api/2/issuetype/10003",
                "id": "10003",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10512&avatarType=issuetype",
                "name": "Person",
                "subtask": False,
                "avatarId": 10512
              }
            }
          }
        },
        {
          "id": "10250",
          "self": "https://glasswall.atlassian.net/rest/api/2/issueLink/10250",
          "type": {
            "id": "10016",
            "name": "Squad - Developer",
            "inward": "has squad developer",
            "outward": "is squad developer of",
            "self": "https://glasswall.atlassian.net/rest/api/2/issueLinkType/10016"
          },
          "inwardIssue": {
            "id": "10047",
            "key": "PERSON-27",
            "self": "https://glasswall.atlassian.net/rest/api/2/issue/10047",
            "fields": {
              "summary": "Jonathon Green",
              "status": {
                "self": "https://glasswall.atlassian.net/rest/api/2/status/10006",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/statuses/generic.png",
                "name": "Active",
                "id": "10006",
                "statusCategory": {
                  "self": "https://glasswall.atlassian.net/rest/api/2/statuscategory/4",
                  "id": 4,
                  "key": "indeterminate",
                  "colorName": "yellow",
                  "name": "In Progress"
                }
              },
              "priority": {
                "self": "https://glasswall.atlassian.net/rest/api/2/priority/3",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/priorities/medium.svg",
                "name": "Medium",
                "id": "3"
              },
              "issuetype": {
                "self": "https://glasswall.atlassian.net/rest/api/2/issuetype/10003",
                "id": "10003",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10512&avatarType=issuetype",
                "name": "Person",
                "subtask": False,
                "avatarId": 10512
              }
            }
          }
        },
        {
          "id": "10141",
          "self": "https://glasswall.atlassian.net/rest/api/2/issueLink/10141",
          "type": {
            "id": "10016",
            "name": "Squad - Developer",
            "inward": "has squad developer",
            "outward": "is squad developer of",
            "self": "https://glasswall.atlassian.net/rest/api/2/issueLinkType/10016"
          },
          "inwardIssue": {
            "id": "10071",
            "key": "PERSON-51",
            "self": "https://glasswall.atlassian.net/rest/api/2/issue/10071",
            "fields": {
              "summary": "Adam  Hewitt",
              "status": {
                "self": "https://glasswall.atlassian.net/rest/api/2/status/10006",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/statuses/generic.png",
                "name": "Active",
                "id": "10006",
                "statusCategory": {
                  "self": "https://glasswall.atlassian.net/rest/api/2/statuscategory/4",
                  "id": 4,
                  "key": "indeterminate",
                  "colorName": "yellow",
                  "name": "In Progress"
                }
              },
              "priority": {
                "self": "https://glasswall.atlassian.net/rest/api/2/priority/3",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/priorities/medium.svg",
                "name": "Medium",
                "id": "3"
              },
              "issuetype": {
                "self": "https://glasswall.atlassian.net/rest/api/2/issuetype/10003",
                "id": "10003",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10512&avatarType=issuetype",
                "name": "Person",
                "subtask": False,
                "avatarId": 10512
              }
            }
          }
        },
        {
          "id": "10140",
          "self": "https://glasswall.atlassian.net/rest/api/2/issueLink/10140",
          "type": {
            "id": "10015",
            "name": "Squad - Leader",
            "inward": "has squad leader",
            "outward": "is squad leader of",
            "self": "https://glasswall.atlassian.net/rest/api/2/issueLinkType/10015"
          },
          "inwardIssue": {
            "id": "10062",
            "key": "PERSON-42",
            "self": "https://glasswall.atlassian.net/rest/api/2/issue/10062",
            "fields": {
              "summary": "Dinis Cruz",
              "status": {
                "self": "https://glasswall.atlassian.net/rest/api/2/status/10006",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/statuses/generic.png",
                "name": "Active",
                "id": "10006",
                "statusCategory": {
                  "self": "https://glasswall.atlassian.net/rest/api/2/statuscategory/4",
                  "id": 4,
                  "key": "indeterminate",
                  "colorName": "yellow",
                  "name": "In Progress"
                }
              },
              "priority": {
                "self": "https://glasswall.atlassian.net/rest/api/2/priority/3",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/priorities/medium.svg",
                "name": "Medium",
                "id": "3"
              },
              "issuetype": {
                "self": "https://glasswall.atlassian.net/rest/api/2/issuetype/10003",
                "id": "10003",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10512&avatarType=issuetype",
                "name": "Person",
                "subtask": False,
                "avatarId": 10512
              }
            }
          }
        },
        {
          "id": "11118",
          "self": "https://glasswall.atlassian.net/rest/api/2/issueLink/11118",
          "type": {
            "id": "10029",
            "name": "Tribe",
            "inward": "has squad",
            "outward": "is squad of",
            "self": "https://glasswall.atlassian.net/rest/api/2/issueLinkType/10029"
          },
          "outwardIssue": {
            "id": "10614",
            "key": "TRIBE-8",
            "self": "https://glasswall.atlassian.net/rest/api/2/issue/10614",
            "fields": {
              "summary": "Glasswall Operations",
              "status": {
                "self": "https://glasswall.atlassian.net/rest/api/2/status/10005",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/status_generic.gif",
                "name": "New",
                "id": "10005",
                "statusCategory": {
                  "self": "https://glasswall.atlassian.net/rest/api/2/statuscategory/2",
                  "id": 2,
                  "key": "new",
                  "colorName": "blue-gray",
                  "name": "To Do"
                }
              },
              "priority": {
                "self": "https://glasswall.atlassian.net/rest/api/2/priority/3",
                "iconUrl": "https://glasswall.atlassian.net/images/icons/priorities/medium.svg",
                "name": "Medium",
                "id": "3"
              },
              "issuetype": {
                "self": "https://glasswall.atlassian.net/rest/api/2/issuetype/10025",
                "id": "10025",
                "description": "",
                "iconUrl": "https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10552&avatarType=issuetype",
                "name": "Tribe",
                "subtask": False,
                "avatarId": 10552
              }
            }
          }
        }
      ],
      "assignee": {
        "self": "https://glasswall.atlassian.net/rest/api/2/user?accountId=5dee69782c44a60edee17525",
        "name": "dcruz",
        "key": "dcruz",
        "accountId": "5dee69782c44a60edee17525",
        "avatarUrls": {
          "48x48": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=48&s=48",
          "24x24": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=24&s=24",
          "16x16": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=16&s=16",
          "32x32": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=32&s=32"
        },
        "displayName": "Dinis Cruz",
        "active": True,
        "timeZone": "America/Chicago",
        "accountType": "atlassian"
      },
      "status": {
        "self": "https://glasswall.atlassian.net/rest/api/2/status/10006",
        "iconUrl": "https://glasswall.atlassian.net/images/icons/statuses/generic.png",
        "name": "Active",
        "id": "10006",
        "statusCategory": {
          "self": "https://glasswall.atlassian.net/rest/api/2/statuscategory/4",
          "id": 4,
          "key": "indeterminate",
          "colorName": "yellow",
          "name": "In Progress"
        }
      },
      "components": [
        
      ],
      "customfield_10050": None,
      "customfield_10051": None,
      "customfield_10052": None,
      "customfield_10053": None,
      "customfield_10054": None,
      "customfield_10055": None,
      "customfield_10056": None,
      "customfield_10057": None,
      "customfield_10058": None,
      "customfield_10059": None,
      "customfield_10049": None,
      "aggregatetimeestimate": None,
      "creator": {
        "self": "https://glasswall.atlassian.net/rest/api/2/user?accountId=5dee69782c44a60edee17525",
        "name": "dcruz",
        "key": "dcruz",
        "accountId": "5dee69782c44a60edee17525",
        "avatarUrls": {
          "48x48": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=48&s=48",
          "24x24": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=24&s=24",
          "16x16": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=16&s=16",
          "32x32": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=32&s=32"
        },
        "displayName": "Dinis Cruz",
        "active": True,
        "timeZone": "America/Chicago",
        "accountType": "atlassian"
      },
      "subtasks": [
        
      ],
      "customfield_10040": None,
      "customfield_10041": None,
      "customfield_10042": None,
      "reporter": {
        "self": "https://glasswall.atlassian.net/rest/api/2/user?accountId=5dee69782c44a60edee17525",
        "name": "dcruz",
        "key": "dcruz",
        "accountId": "5dee69782c44a60edee17525",
        "avatarUrls": {
          "48x48": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=48&s=48",
          "24x24": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=24&s=24",
          "16x16": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=16&s=16",
          "32x32": "https://secure.gravatar.com/avatar/cd5c7a867913b97100b706e92add842b?d=https%3A%2F%2Favatar-management--avatars.us-west-2.prod.public.atl-paas.net%2Finitials%2FDC-3.png&size=32&s=32"
        },
        "displayName": "Dinis Cruz",
        "active": True,
        "timeZone": "America/Chicago",
        "accountType": "atlassian"
      },
      "customfield_10043": None,
      "customfield_10044": None,
      "aggregateprogress": {
        "progress": 0,
        "total": 0
      },
      "customfield_10045": [
        
      ],
      "customfield_10046": None,
      "customfield_10047": None,
      "customfield_10048": None,
      "customfield_10038": None,
      "progress": {
        "progress": 0,
        "total": 0
      },
      "votes": {
        "self": "https://glasswall.atlassian.net/rest/api/2/issue/SQUAD-10/votes",
        "votes": 0,
        "hasVoted": False
      },
      "issuetype": {
        "self": "https://glasswall.atlassian.net/rest/api/2/issuetype/10005",
        "id": "10005",
        "description": "",
        "iconUrl": "https://glasswall.atlassian.net/secure/viewavatar?size=medium&avatarId=10520&avatarType=issuetype",
        "name": "Squad",
        "subtask": False,
        "avatarId": 10520
      },
      "timespent": None,
      "customfield_10030": 0.0,
      "customfield_10031": 9.0,
      "project": {
        "self": "https://glasswall.atlassian.net/rest/api/2/project/10006",
        "id": "10006",
        "key": "SQUAD",
        "name": "Squad",
        "projectTypeKey": "business",
        "simplified": False,
        "avatarUrls": {
          "48x48": "https://glasswall.atlassian.net/secure/projectavatar?pid=10006&avatarId=10518",
          "24x24": "https://glasswall.atlassian.net/secure/projectavatar?size=small&s=small&pid=10006&avatarId=10518",
          "16x16": "https://glasswall.atlassian.net/secure/projectavatar?size=xsmall&s=xsmall&pid=10006&avatarId=10518",
          "32x32": "https://glasswall.atlassian.net/secure/projectavatar?size=medium&s=medium&pid=10006&avatarId=10518"
        }
      },
      "customfield_10032": 3.0,
      "customfield_10033": None,
      "aggregatetimespent": None,
      "customfield_10034": None,
      "customfield_10035": None,
      "customfield_10036": None,
      "customfield_10037": None,
      "customfield_10028": 0.0,
      "customfield_10029": 0.0,
      "resolutiondate": None,
      "workratio": -1,
      "watches": {
        "self": "https://glasswall.atlassian.net/rest/api/2/issue/SQUAD-10/watchers",
        "watchCount": 2,
        "isWatching": True
      },
      "created": "2019-12-09T18:20:43.271-0600",
      "customfield_10020": None,
      "customfield_10021": None,
      "customfield_10022": None,
      "customfield_10023": None,
      "customfield_10016": None,
      "customfield_10017": None,
      "customfield_10018": {
        "hasEpicLinkFieldDependency": False,
        "showField": False,
        "nonEditableReason": {
          "reason": "PLUGIN_LICENSE_ERROR",
          "message": "Portfolio for Jira must be licensed for the Parent Link to be available."
        }
      },
      "customfield_10019": "0|i000n3:",
      "updated": "2020-01-28T18:32:34.874-0600",
      "timeoriginalestimate": None,
      "description": "an description (test)",
      "customfield_10010": None,
      "customfield_10014": None,
      "timetracking": {
        
      },
      "customfield_10015": None,
      "customfield_10005": None,
      "customfield_10006": None,
      "security": None,
      "customfield_10007": None,
      "customfield_10008": None,
      "customfield_10009": None,
      "attachment": [
        
      ],
      "summary": "CISO",
      "customfield_10000": "{}",
      "customfield_10001": None,
      "customfield_10002": None,
      "customfield_10003": None,
      "customfield_10004": None,
      "environment": None,
      "duedate": None
    }
  },
  "changelog": {
    "id": "17324",
    "items": [
      {
        "field": "description",
        "fieldtype": "jira",
        "fieldId": "description",
        "from": None,
        "fromString": "…….",
        "to": None,
        "toString": "an description (test)"
      }
    ]
  }
}
        event_type = data.get('issue_event_type_name')
        issue_raw  = data.get('issue')
        change_log = data.get('changelog')
        key        = issue_raw.get('key')

        from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
        api_jira_rest = API_Jira_Rest()
        issue = api_jira_rest.convert_issue(issue_raw)
        self.result = f"updated issue '{key}' after event '{event_type}' , change log: {change_log}"
