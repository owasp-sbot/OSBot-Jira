from osbot_graphsv.demo.Demo_Data import Demo_Data


class Demo_Data_Import:

    def __init__(self):
        self.demo_data = Demo_Data()
        self.graph_sv  = self.demo_data.graph_sv
        self.indexes   = self.graph_sv.indexes

    def import_Sample_Database_extracts__HR_Database(self):
        existing_summaries = self.indexes.by_fields_and_values().get('Summary').keys()
        issue_type = 'Person'
        data = self.demo_data.dataset__Sample_Database_extracts__HR_Database()
        results = []
        for item in data:
            item['Summary'] = "{0} {1}".format(item.get('Legal First Name'), item.get('Surname'))
            if item['Summary'] not in existing_summaries:
                results.append(self.graph_sv.issue_add(issue_type, item))
        return results