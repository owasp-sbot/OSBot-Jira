import  datetime

from pbx_gs_python_utils.utils.Elastic_Search import Elastic_Search


class Save_To_ELK():

    def __init__(self, index = None):
        if index is None:
            index = 'save_to_elk'
        self.secret_id = 'elastic-logs-server-1'
        self.elastic = self.setup(index)

    def add_document(self, doc_type, doc_data):
        return self.add_document_with_id(doc_type, None, doc_data)

    def add_document_with_id(self, doc_type, doc_id, doc_data):
        if isinstance(doc_data, str):
            doc_data = { "str" : doc_data }             # data doc_data to be an object and not a string (since once there is a string in the data field in ELK , string values will throw an exception)

        item = { 'doc_type' : doc_type            ,
                 'doc_data' : doc_data            ,
                 'date'     : datetime.datetime.utcnow()}
        return self.elastic.add(item, doc_id)

    def get_most_recent_version_of_document(self, lucene_query):
        try:
            values = self.elastic.search_using_lucene_index_by_id(lucene_query, 1, "date:desc").values()
            if values and len(values) == 1:
                return list(values).pop().get('doc_data')
        except:
            return None
        return None

    def find_documents(self, lucene_query):
        return self.elastic.search_using_lucene_index_by_id(lucene_query)

    def find_documents_of_type(self, dock_type):
        return self.find_documents("doc_type:{0}".format(dock_type))

    def delete_documents_with_id(self, doc_id):
        return self.elastic.delete_data_by_id(doc_id)

    def delete_documents_with_type(self, doc_type):
        keys = self.find_documents_of_type(doc_type).keys()
        for key in keys:
            self.elastic.delete_data_by_id(key)

    def create(self):
        if self.elastic.exists() is False:
            self.elastic.create_index().create_index_pattern()
        return self.elastic.exists()

    def setup(self, index):
        return Elastic_Search()._setup_Elastic_on_cloud_via_AWS_Secret(index, self.secret_id)
