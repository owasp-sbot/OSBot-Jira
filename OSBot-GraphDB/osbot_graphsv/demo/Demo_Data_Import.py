from osbot_graphsv.demo.Demo_Data import Demo_Data


class Demo_Data_Import:

    def __init__(self):
        self.demo_data = Demo_Data()
        self.graph_sv  = self.demo_data.graph_sv

    def import_Sample_Database_extracts__HR_Database(self):
        issue_type = 'Person'
        data = self.demo_data.dataset__Sample_Database_extracts__HR_Database()
        item = data[0]
        item['Summary'] = "{0} {1}".format(item.get('Legal First Name'), item.get('Surname'))

        return self.graph_sv.issue_add(issue_type, item)


        return item