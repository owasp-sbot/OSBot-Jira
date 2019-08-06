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

        self.indexes.rebuild()
        self.import_Role_Team_Function_Business()
        self.import_Device_Person_Account_Application__by_Device()
        self.import_Device_Person_Account_Application__by_Person()
        self.import__Device_Person_Account_Application__by_Account()
        self.import_dataset__Device_Detections()
        self.import_dataset__Control_Capabilities_Role_People()
        self.import_Impacts()

        self.indexes.rebuild()
        self.import_Impact_Vulnerability_Incident_Fact_Control()

        self.indexes.rebuild()
        #self.import_Incident()

        #self.indexes.rebuild()
        #self.import_Vulnerability_Risk_Role()

        #self.indexes.rebuild()


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

    def import_Impact_Vulnerability_Incident_Fact_Control(self):

        data = self.demo_data.dataset__Impact_Vulnerability_Incident_Fact_Control()

        security_impacts = []
        vulnerabilities  = []
        incident_facts   = []
        capabilities     = []

        for item in data:
            security_impacts.append(item.get('Security Impact').strip())
            vulnerabilities.append(item.get('Vulnerability').strip())
            incident_facts.append(item.get('Incident Fact').strip())
            capabilities.append(item.get('Capability').strip())

        security_impacts = sorted(list(set(security_impacts)))[1:]
        vulnerabilities  = sorted(list(set(vulnerabilities)))[1:]
        incident_facts   = sorted(list(set(incident_facts)))
        capabilities     = sorted(list(set(capabilities)))

        for security_impact in security_impacts:
            item = { 'Summary': security_impact }
            self.add_if_new('Security Impact', item)

        for vulnerability in vulnerabilities:
            item = { 'Summary': vulnerability }
            self.add_if_new('Vulnerability', item)

        for incident_fact in incident_facts:
            item = { 'Summary': incident_fact }
            self.add_if_new('Incident Fact', item)

        for capability in capabilities:
            item = { 'Summary': capability }
            self.add_if_new('Capability', item)


        all_security_impacts = self.issues.security_impacts()
        all_vulnerabilities = self.issues.vulnerabilities()
        all_incident_facts = self.issues.incident_facts()
        all_capabilities = self.issues.capabilities()

        for item in data:
            security_impacts = all_security_impacts.get(item.get('Security Impact').strip())
            vulnerabilities  = all_vulnerabilities .get(item.get('Vulnerability'  ).strip())
            incident_facts   = all_incident_facts  .get(item.get('Incident Fact'  ).strip())
            capabilities     = all_capabilities    .get(item.get('Capability'     ).strip())

            edge_1 = item.get('edge_1')
            edge_2 = item.get('edge_2')
            edge_3 = item.get('edge_3')
            if security_impacts:
                for security_impact_id in security_impacts:
                    for vulnerability_id in vulnerabilities:
                        self.graph_sv.link_add(security_impact_id, edge_1, vulnerability_id)
                        for incident_fact_id in incident_facts:
                            self.graph_sv.link_add(vulnerability_id, edge_2,incident_fact_id)
                            for capability_id in capabilities:
                                self.graph_sv.link_add(incident_fact_id, edge_3, capability_id)
            else:
                if vulnerabilities:
                    for vulnerability_id in vulnerabilities:
                        for incident_fact_id in incident_facts:
                            self.graph_sv.link_add(vulnerability_id, edge_2,incident_fact_id)
                            for capability_id in capabilities:
                                self.graph_sv.link_add(incident_fact_id, edge_3, capability_id)

                else:
                    for incident_fact_id in incident_facts:
                        for capability_id in capabilities:
                            self.graph_sv.link_add(incident_fact_id, edge_3, capability_id)


    def import_Incident(self):
        data = self.demo_data.dataset__Incident()


        incidents             = []
        investigation_threads = []
        incident_tasks        = []
        incident_fact         = []
        timeline_fact         = []

        for item in data:
            incidents            .append(item.get('Incident'            ).strip())
            investigation_threads.append(item.get('Investigation Thread').strip())
            incident_tasks       .append(item.get('Incident Task'       ).strip())
            incident_fact        .append(item.get('Incident Fact'       ).strip())
            timeline_fact        .append(item.get('Timeline Fact'       ).strip())

        incidents             = sorted(list(set(incidents)))
        investigation_threads = sorted(list(set(investigation_threads)))
        incident_tasks        = sorted(list(set(incident_tasks)))[1:]
        incident_facts        = sorted(list(set(incident_fact)))[1:]
        timeline_facts        = sorted(list(set(timeline_fact)))[1:]

        for incident in incidents:
            item = { 'Summary': incident }
            self.add_if_new('Incident', item)

        for investigation_thread in investigation_threads:
            item = { 'Summary': investigation_thread }
            self.add_if_new('Investigation Thread', item)

        for incident_task in incident_tasks:
            item = { 'Summary': incident_task }
            self.add_if_new('Incident Task', item)

        for incident_fact in incident_facts:
            item = { 'Summary': incident_fact }
            self.add_if_new('Incident Fact', item)

        for timeline_fact in timeline_facts:
            item = { 'Summary': timeline_fact }
            self.add_if_new('Timeline Fact', item)

        all_incidents             = self.issues.incidents()
        all_investigation_threads = self.issues.investigation_threads()
        all_incident_tasks        = self.issues.incident_tasks()
        all_incident_facts        = self.issues.incident_facts()
        all_timeline_facts        = self.issues.timeline_facts()

        for item in data:
            incidents               = all_incidents             .get(item.get('Incident'            ).strip())
            investigation_threads   = all_investigation_threads .get(item.get('Investigation Thread').strip())
            incident_tasks          = all_incident_tasks        .get(item.get('Incident Task'       ).strip())
            incident_facts          = all_incident_facts        .get(item.get('Incident Fact'       ).strip())
            timeline_facts          = all_timeline_facts        .get(item.get('Timeline Fact'       ).strip())

            edge_1 = item.get('edge_1')
            edge_2 = item.get('edge_2')
            edge_3 = item.get('edge_3')
            edge_4 = item.get('edge_4')

            for incident_id in incidents:
                for investigation_thread_id in investigation_threads:
                    self.graph_sv.link_add(incident_id, edge_1, investigation_thread_id)
                    if incident_tasks:
                        for incident_task_id in incident_tasks:
                            self.graph_sv.link_add(investigation_thread_id ,edge_2, incident_task_id)
                            if incident_facts:
                                for incident_fact_id in incident_facts:
                                    self.graph_sv.link_add(incident_task_id,edge_3, incident_fact_id)
                                    if timeline_facts:
                                        for timeline_fact_id in timeline_facts:
                                            self.graph_sv.link_add(incident_fact_id, edge_4, timeline_fact_id)

    def import_Vulnerability_Risk_Role(self):
        data = self.demo_data.dataset__Vulnerability_Risk_Role()

        vulnerabilities = []
        risks           = []
        roles           = []

        for item in data:
            vulnerabilities.append(item.get('Vulnerability').strip())
            risks          .append(item.get('Risk ').strip())
            roles          .append(item.get('Role').strip())

        vulnerabilities = sorted(list(set(vulnerabilities)))
        risks           = sorted(list(set(risks)))[1:]
        roles           = sorted(list(set(roles)))[1:]

        for vulnerability in vulnerabilities:
            item = { 'Summary': vulnerability }
            self.add_if_new('Vulnerability', item)

        for risk in risks:
            item = { 'Summary': risk }
            self.add_if_new('Risk', item)

        for role in roles:
            item = { 'Summary': role }
            self.add_if_new('Role', item)

        all_vulnerabilities = self.issues.vulnerabilities()
        all_risks           = self.issues.risks()
        all_roles           = self.issues.roles()


        for item in data:
            vulnerabilities = all_vulnerabilities.get(item.get('Vulnerability').strip())
            risks           = all_risks          .get(item.get('Risk '        ).strip())
            roles           = all_roles          .get(item.get('Role'         ).strip())

            edge_1 = item.get('edge_1')
            edge_2 = item.get('edge_2')

            for vulnerability_id in vulnerabilities:
                if risks:
                    for risk_id in risks:
                        self.graph_sv.link_add(vulnerability_id, edge_1, risk_id)
                    if roles:
                        for role_id in roles:
                            self.graph_sv.link_add(risk_id, edge_2, role_id)