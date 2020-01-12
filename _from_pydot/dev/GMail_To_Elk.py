from API_GMail import API_GMail
from utils.Dev import Dev
from pbx_gs_python_utils.utils.Elastic_Search import Elastic_Search


class GMail_To_Elk:

    def __init__(self):
        self.api_gmail   = API_GMail().setup()
        self.secret_id = 'elastic-jira-dev-2'
        self.index     = 'soc-alerts-data'
        self.elastic = Elastic_Search()._setup_Elastic_on_cloud_via_AWS_Secret(self.index, self.secret_id)

    def create_indexes(self):
        self.elastic.index = 'soc-alerts-data'
        self.elastic.create_index()
        #self.elastic.create_index_pattern()
        #self.elastic.index = 'soc-alerts-raw'
        #self.elastic.create_index()

    def delete_all_index_data(self):
        self.elastic.delete_using_query({  "query": { "match_all": {} } })

    def send_messages_to_elk(self, label_id,label_name):
        messages = self.api_gmail.messages_from_label(label_id)
        for message in messages:
            message['label_id'  ] = label_id
            message['label_name'] = label_name
        count =  self.elastic.add_bulk(messages,'id')
        Dev.pprint('processed: {0} messages from {1}'.format(count, label_name))
        #Dev.pprint(messages)