import base64
import datetime
import json
from email._parseaddr import parsedate_tz, mktime_tz

from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
from httplib2 import Http
from oauth2client import file

from utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files
from utils.aws.secrets import Secrets


class API_GMail:

    def __init__(self):
        self.secret_id = 'socalerts-api-access'
        self.service   = None
        self.user_id   = 'me'


    def labels(self):
        results = self.service.users().labels().list(userId='me').execute()
        labels = {}
        for item in results.get('labels', []):
            labels[item['name']] = item
        return labels

    def list(self, labelIds = None, query='', max_results = 100):
        response = self.service.users().messages().list(userId=self.user_id,q=query, labelIds=labelIds, maxResults = max_results).execute()
        if response.get('messages') is None:
            Dev.pprint('NO MESSAGES for {0} - {1}'.format(labelIds,response))
            return []
        return (message['id'] for message in response['messages'])

    def list_all(self, labelIds = None, query=''):
        response = self.service.users().messages().list(userId=self.user_id,q=query, labelIds=labelIds).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = self.service.users().messages().list(userId=self.user_id, q=query, labelIds=labelIds, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return (message['id'] for message in messages)

    def messages(self, messages_ids):
        #results = self.service.users().messages().list(userId='me', maxResults=100, labelIds= labelIds).execute()
        #Dev.pprint(len(results['messages']))
        results = []
        batch = BatchHttpRequest()

        def handle_message(index, message, error):
            results.append(self.parse_Message(message))

        for message_id in messages_ids:
            batch.add(self.service.users().messages().get(userId='me', id=message_id), callback=handle_message )
        batch.execute()
        return results

    def messages_from_label(self, label):
        messages_ids = self.list_all(label)
        return self.messages(messages_ids)

    def parse_Message(self, message):
        headers = {}

        if message.get('payload') is None:
            Dev.pprint("no payload for message: {0}".format(message))
            return {}
        for item in message['payload']['headers']:
           headers[item['name']] = item['value']

        tt = parsedate_tz(headers['Date'    ])
        timestamp = mktime_tz(tt)

        result = {
                    'subject'   : headers['Subject' ],
                    'date'      : datetime.datetime.fromtimestamp(timestamp),
                    'date_raw'  : headers['Date'    ],
                    'from'      : headers['From'    ],
                    'id'        : message['id'      ],
                    'labels'    : message['labelIds'],
                    'threadId'  : message['threadId'],
                    'snippet'   : message['snippet' ],
                    'size'      : message['sizeEstimate'],
                    # 'headers'   : headers,
                    #'raw'       : message
                 }
        if message['payload']['body'].get('data'):
            result['body'] = base64.urlsafe_b64decode(message['payload'].get('body').get('data').encode('ASCII')).decode()
            #result['body'] = base64.decodebytes(message['payload']['body']['data'].encode()).decode()
        else:
            if message['payload'].get('parts'):
                for part in message['payload'].get('parts'):
                    if part.get('body').get('data'):
                        result['body'] = base64.urlsafe_b64decode(part.get('body').get('data').encode('ASCII')).decode()
        return result


    def setup(self):
        secret_data  = json.loads(Secrets(self.secret_id).value())
        storage_file = '/tmp/gmail_storage_token.json'
        Files.write(storage_file, secret_data['storage'])
        store       = file.Storage(storage_file)
        creds       = store.get()
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))
        # note: 'storage.json file created using storage
        # SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        # if not creds or creds.invalid:
        #    flow = client.flow_from_clientsecrets(self.credentials_file, SCOPES)
        #    flags = argparser.parse_args('--auth_host_name localhost --logging_level INFO'.split())
        #    creds = run_flow(flow, store, flags)
        return self