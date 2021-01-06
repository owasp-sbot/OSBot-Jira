import csv
from osbot_utils.utils.Files import Files

from osbot_graphsv.api.Graph_SV import Graph_SV


class Demo_Data:
    def __init__(self):
        self.root_folder = Files.path_combine(__file__        , '../../../GraphSV-demo-data')
        self.data_folder = Files.path_combine(self.root_folder,'csv-demo-data'              )
        self.graph_sv    = Graph_SV(self.root_folder)


    def file_system(self):
        return self.graph_sv.file_system

    # helper methods
    def file_lines(self, title):
        lines = []
        file_path = self.file_path(title)
        with open(file_path) as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                lines.append(row)
        return lines

    def file_path(self, title):
        return Files.path_combine(self.data_folder, title)

    def file_data(self, title, header_row, row_count):
        data = []
        index_start = header_row  + 1
        index_end   = index_start + row_count
        lines = self.file_lines(title)
        headers = lines[header_row]
        # print(lines[index_start: index_end])
        # return

        for line in lines[index_start: index_end]:
            item={}
            for index, cell in enumerate(line):
                header = headers[index]
                if header:
                    item[header] = cell
            data.append(item)

        return data

    # data sets
    def dataset__Sample_Database_extracts__HR_Database(self):
        return self.file_data('1.Sample Database extracts.csv', 1, 6)

    def dataset__Sample_Database_extracts__Sunways_application_user_extract(self):
        return self.file_data('1.Sample Database extracts.csv', 10, 6)

    def dataset__People_Role_Reporting_line(self):
        return self.file_data('2.People, Role, Reporting line.csv', 0, 6)

    def dataset__Role_Team_Function_Business(self):
        return self.file_data('3.Role, Team, Function, Business.csv', 0, 6)

    def dataset__Device_Person_Account_Application__by_Device(self):
        return self.file_data('4.Device, Person, Account, Application.csv', 0, 6)

    def dataset__Device_Person_Account_Application__by_Person(self):
        return self.file_data('4.Device, Person, Account, Application.csv', 9, 6)

    def dataset__Device_Person_Account_Application__by_Account(self):
        return self.file_data('4.Device, Person, Account, Application.csv', 17, 6)

    def dataset__Business_Asset(self):
        return self.file_data('5.Business Asset.csv', 0, 6)

    def dataset__Device_Detections(self):
        data = self.file_data('6.Device, Detections.csv', 0, 28)
        del data[6:8]           # remove the headers in these locations since
        del data[12:14]         # they don't represent new types of mappings
        del data[15:17]         # which means we can reuse row's 1 headers
        del data[17:19]
        return data

    def dataset__Account_Detections_2FA(self):
        data = self.file_data('7.Account, Detections, 2FA.csv', 0, 30)
        del data[22:24]
        del data[14:16]
        del data[6:8]
        return data

    def dataset__Control_Capabilities_Role_People(self):
        return self.file_data('8.Control Capabilities, Role, People.csv', 0, 30)

    def dataset__Impacts(self):
        return self.file_data('9.Impacts.csv', 0, 75)

    def dataset__Impact_Vulnerability_Incident_Fact_Control(self):
        return self.file_data('10.Impact, Vulnerability, Incident Fact, Control.csv', 0, 24)

    def dataset__Incident(self):
        return self.file_data('11.Incident.csv', 0, 40)

    def dataset__Vulnerability_Risk_Role(self):
        return self.file_data('12.Vulnerability, Risk, Role.csv', 0, 11)
