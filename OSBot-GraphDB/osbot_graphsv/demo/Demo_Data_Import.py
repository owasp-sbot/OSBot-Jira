from osbot_graphsv.demo.Demo_Data import Demo_Data


class Demo_Data_Import:

    def __init__(self):
        self.demo_data  = Demo_Data()
        self.graph_sv   = self.demo_data.graph_sv
        self.indexes    = self.graph_sv.indexes
        self.issues     = self.graph_sv.issues
        self._summaries = None

    # helper methods
    def add_if_new(self,issue_type_name, item):
        if self.summary_not_exists(item):
            return self.graph_sv.issue_add(issue_type_name, item)

    def summaries(self):
        if self._summaries is None:
            data = self.indexes.by_fields_and_values()
            if data:
                self._summaries =  data.get('Summary').keys()
            else:
                self._summaries = []
        return self._summaries

    def summary_not_exists(self, item):
        return item.get('Summary') not in self.summaries()

    # import methods
    def import_all(self):
        self.import_Sample_Database_extracts__HR_Database()
        self.import_Sample_Database_extracts__Sunways_application_user_extract()
        self.import_People_Role_Reporting_line()

    def import_Sample_Database_extracts__HR_Database(self):
        data = self.demo_data.dataset__Sample_Database_extracts__HR_Database()
        for item in data:
            item['Summary'] = "{0} {1}".format(item.get('Legal First Name').strip(), item.get('Surname').strip())
            self.add_if_new('Person', item)

    def import_Sample_Database_extracts__Sunways_application_user_extract(self):
        data = self.demo_data.dataset__Sample_Database_extracts__Sunways_application_user_extract()
        for item in data:
            person = { "Email": item.get('Email').strip() , "Summary": item.get('Name').strip()}
            self.add_if_new('Person', person)

    def import_People_Role_Reporting_line(self):
        data = self.demo_data.dataset__People_Role_Reporting_line()
        roles = []
        for item in data:
            roles.append(item.get('Role_1').strip())
            roles.append(item.get('Role_2').strip())
        roles = list(set(roles))[1:]
        for role in roles:
            item = {'Summary': role}
            self.add_if_new('Role', item)
        all_roles   = self.issues.roles()
        all_persons = self.issues.persons()

        for item in data:
            persons = all_persons.get(item.get('Person'))
            roles_1 = all_roles.get(item.get('Role_1'))
            roles_2 = all_roles.get(item.get('Role_2'))
            edge_1  = item.get('edge_1')
            edge_2  = item.get('edge_2')
            if persons and roles_1:
                for person_id in persons:
                    for role_id_1 in roles_1:
                        self.graph_sv.link_add(person_id,edge_1, role_id_1)
                        if roles_2:
                            for role_id_2 in roles_2:
                                self.graph_sv.link_add(role_id_1, edge_2, role_id_2)



        #return persons