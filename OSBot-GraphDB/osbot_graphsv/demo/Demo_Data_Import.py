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
        self.indexes.rebuild()
        self.import_People_Role_Reporting_line()
        self.import_Role_Team_Function_Business()
        self.import_Device_Person_Account_Application__by_Device()
        self.import_Device_Person_Account_Application__by_Person()
        self.import__Device_Person_Account_Application__by_Account()
        self.import_dataset__Device_Detections()
        self.import_dataset__Control_Capabilities_Role_People()
        self.import_Impacts()
        self.indexes.rebuild()


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
            persons = all_persons.get(item.
                                      get('Person'))
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

    def import_Role_Team_Function_Business(self):
        data      = self.demo_data.dataset__Role_Team_Function_Business()
        teams     = []
        functions = []
        biz_units = []

        for item in data:
            teams    .append(item.get('Team'         ).strip())
            functions.append(item.get('Function'     ).strip())
            biz_units.append(item.get('Business Unit').strip())


        teams     = list(set(teams))
        functions = list(set(functions))
        biz_units = list(set(biz_units))

        for team in teams:
            item = {'Summary': team}
            self.add_if_new('Team', item)

        for function in functions:
            item = {'Summary': function}
            self.add_if_new('Function', item)

        for biz_unit in biz_units:
            item = {'Summary': biz_unit}
            self.add_if_new('Business Unit', item)

        all_roles          = self.issues.roles()
        all_persons        = self.issues.persons()
        all_teams          = self.issues.teams()
        all_functions      = self.issues.functions()
        all_business_units = self.issues.business_units()

        for item in data:
            persons        = all_persons.get(item.get('Person'))
            roles          = all_roles.get(item.get('Role'))
            teams          = all_teams.get(item.get('Team'))
            functions      = all_functions.get(item.get('Function'))
            business_units = all_business_units.get(item.get('Business Unit'))
            edge_1         = item.get('edge_1')
            edge_2         = item.get('edge_2')
            edge_3         = item.get('edge_3')
            edge_4         = item.get('edge_4')

            for person_id in persons:
                for role_id in roles:
                    self.graph_sv.link_add(person_id, edge_1, role_id)
                    for team_id in teams:
                        self.graph_sv.link_add(role_id, edge_2, team_id)
                        for function_id in functions:
                            self.graph_sv.link_add(team_id, edge_3, function_id)
                            for business_unit_id in business_units:
                                self.graph_sv.link_add(function_id, edge_4, business_unit_id)

    def import_Device_Person_Account_Application__by_Device(self):
        data = self.demo_data.dataset__Device_Person_Account_Application__by_Device()
        devices         = []
        persons         = []
        accounts        = []
        business_assets = []
        for item in data:
            devices        .append(item.get('Device'        ).strip())
            persons        .append(item.get('Person'        ).strip())
            accounts       .append(item.get('Account'       ).strip())
            business_assets.append(item.get('Business Asset').strip())

        devices = list(set(devices))
        #persons = list(set(persons))
        accounts = list(set(accounts))
        business_assets = list(set(business_assets))[1:]

        for device in devices:
            item = {'Summary': device}
            self.add_if_new('Device', item)

        for account in accounts:
            item = {'Summary': account}
            self.add_if_new('Account', item)

        for business_asset in business_assets:
            item = {'Summary': business_asset}
            self.add_if_new('Business Asset', item)

        all_accounts        = self.issues.accounts()
        all_business_assets = self.issues.business_assets()
        all_devices         = self.issues.devices()
        all_persons         = self.issues.persons()

        for item in data:
            devices         = all_devices .get(item.get('Device' ))
            persons         = all_persons .get(item.get('Person' ))
            accounts        = all_accounts.get(item.get('Account'))
            business_assets = all_business_assets.get(item.get('Business Asset'))


            edge_1 = item.get('edge_1')
            edge_2 = item.get('edge_2')
            edge_3 = item.get('edge_3')

            for device_id in devices:
                for person_id in persons:
                    self.graph_sv.link_add(device_id, edge_1, person_id)
                    for account_id in accounts:
                        self.graph_sv.link_add(person_id, edge_2, account_id)
                        if edge_3:
                            for business_asset_id in business_assets:
                                self.graph_sv.link_add(account_id, edge_3, business_asset_id)



    def import_Device_Person_Account_Application__by_Person(self):
        data = self.demo_data.dataset__Device_Person_Account_Application__by_Person()
        persons         = []
        accounts        = []
        applications    = []
        business_assets = []
        for item in data:
            persons        .append(item.get('Person').strip())
            accounts       .append(item.get('Account').strip())
            applications   .append(item.get('Application').strip())
            business_assets.append(item.get('Business Asset').strip())

        accounts = list(set(accounts))
        applications = list(set(applications))
        business_assets = list(set(business_assets))

        for account in accounts:
            item = {'Summary': account}
            self.add_if_new('Account', item)

        for application in applications:
            item = {'Summary': application}
            self.add_if_new('Application', item)

        for business_asset in business_assets:
            item = {'Summary': business_asset}
            self.add_if_new('Business Asset', item)

        all_persons = self.issues.persons()
        all_applications = self.issues.applications()
        all_accounts = self.issues.accounts()
        all_business_assets = self.issues.business_assets()

        for item in data:
            persons         = all_persons.get(item.get('Person'))
            accounts        = all_accounts.get(item.get('Account'))
            applications    = all_applications .get(item.get('Application' ))
            business_assets = all_business_assets.get(item.get('Business Asset'))

            edge_1 = item.get('edge_1')
            edge_2 = item.get('edge_2')
            edge_3 = item.get('edge_3')

            for person_id in persons:
                for account_id in accounts:
                    self.graph_sv.link_add(person_id, edge_1, account_id)
                    for application_id in applications:
                        self.graph_sv.link_add(account_id, edge_2, application_id)
                        for business_asset_id in business_assets:
                            self.graph_sv.link_add(application_id, edge_3, business_asset_id)

    def import__Device_Person_Account_Application__by_Account(self):
        data = self.demo_data.dataset__Device_Person_Account_Application__by_Account()
        accounts = []
        business_assets = []

        for item in data:
            accounts       .append(item.get('Account').strip())
            business_assets.append(item.get('Business Asset').strip())

        accounts = list(set(accounts))
        business_assets = list(set(business_assets))[1:]

        all_accounts = self.issues.accounts()
        all_business_assets = self.issues.business_assets()

        for item in data:
            accounts        = all_accounts.get(item.get('Account'))
            business_assets = all_business_assets.get(item.get('Business Asset'))

            edge_1 = item.get('edge_1')

            if business_assets:
                for account_id in accounts:
                    for business_asset_id in business_assets:
                        self.graph_sv.link_add(account_id, edge_1, business_asset_id)

    def import_dataset__Device_Detections(self):
        data = self.demo_data.dataset__Device_Detections()
        #devices = []
        detections = []
        applications = []

        for item in data:
            #devices        .append(item.get('Device Name').strip())
            detections     .append(item.get('Detection').strip())
            applications   .append(item.get('Application').strip())

        #devices      = list(set(devices))
        detections   = list(set(detections))
        applications = list(set(applications))


        for detection in detections:
            item = {'Summary': detection}
            self.add_if_new('Detection', item)

        for application in applications:
            item = {'Summary': application}
            self.add_if_new('Application', item)

        all_devices      = self.issues.devices()
        all_detections   = self.issues.detections()
        all_applications = self.issues.applications()

        for item in data:
            devices         = all_devices.get(item.get('Device Name').strip())
            detections      = all_detections.get(item.get('Detection').strip())
            applications    = all_applications .get(item.get('Application').strip())

            edge_1 = item.get('edge_1')
            edge_2 = item.get('edge_2')

            for device_id in devices:
                for detection_id in detections:
                    self.graph_sv.link_add(device_id, edge_1, detection_id)
                    for application_id in applications:
                        self.graph_sv.link_add(detection_id, edge_2, application_id)

        #return all_applications

    def import_dataset__Control_Capabilities_Role_People(self):
        data = self.demo_data.dataset__Control_Capabilities_Role_People()

        pillars      = []
        capabilities = []
        roles        = []
        persons      = []

        for item in data:
            pillars        .append(item.get('Pillar').strip())
            capabilities   .append(item.get('Capability').strip())
            roles          .append(item.get('Role').strip())
            persons        .append(item.get('Person').strip())

        pillars = list(set(pillars))
        capabilities = list(set(capabilities))
        roles = list(set(roles))
        persons = list(set(persons))

        for pillar in pillars:
            item = {'Summary': pillar}
            self.add_if_new('Pillar', item)

        for capability in capabilities:
            item = {'Summary': capability}
            self.add_if_new('Capability', item)

        for role in roles:
            item = {'Summary': role}
            self.add_if_new('Role', item)

        for person in persons:
            item = {'Summary': person}
            self.add_if_new('Person', item)

        all_pillars      = self.issues.pillars()
        all_capabilities = self.issues.capabilities()
        all_roles        = self.issues.roles()
        all_persons      = self.issues.persons()

        for item in data:
            pillars        = all_pillars.get(item.get('Pillar').strip())
            capabilities   = all_capabilities.get(item.get('Capability').strip())
            roles          = all_roles.get(item.get('Role'))
            persons        = all_persons.get(item.get('Person').strip())

            edge_1 = item.get('edge_1')
            edge_2 = item.get('edge_2')
            edge_3 = item.get('edge_3')

            for pillar_id in pillars:
                for capability_id in capabilities:
                    self.graph_sv.link_add(pillar_id, edge_1, capability_id)
                    for role_id in roles:
                        self.graph_sv.link_add(capability_id,edge_2, role_id)
                        for person_id in persons:
                            self.graph_sv.link_add(role_id, edge_3, person_id)

    def import_Impacts(self):
        data = self.demo_data.dataset__Impacts()

        security_impacts = []
        for item in data:
            security_impacts.append(item.get('Security Impact_1').strip())
            security_impacts.append(item.get('Security Impact_2').strip())
            security_impacts.append(item.get('Security Impact_3').strip())

        security_impacts = list(set(security_impacts))

        for security_impact in security_impacts:
            item = {'Summary': security_impact}
            self.add_if_new('Security Impact', item)

        all_security_impacts = self.issues.security_impacts()

        for item in data:
            security_impacts_1 = all_security_impacts.get(item.get('Security Impact_1').strip())
            security_impacts_2 = all_security_impacts.get(item.get('Security Impact_2').strip())
            security_impacts_3 = all_security_impacts.get(item.get('Security Impact_3').strip())

            edge_1 = item.get('edge_1')
            edge_2 = item.get('edge_2')

            for security_impact_1 in security_impacts_1:
                for security_impact_2 in security_impacts_2:
                    self.graph_sv.link_add(security_impact_1, edge_1, security_impact_2)
                    for security_impact_3 in security_impacts_3:
                        self.graph_sv.link_add(security_impact_2, edge_2, security_impact_3)
