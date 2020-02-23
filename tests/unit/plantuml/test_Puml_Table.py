import unittest

from osbot_jira.api.plantuml.Puml_Table import Puml_Table


class Test_Puml_Table(unittest.TestCase):

    def setUp(self):
        self.table = Puml_Table()



    def test_add_title(self):
        table_obj = {
                        "key 1" : "value 1" ,
                        "key 2" : "value 2" ,
                        "key 3" : "value 3" ,
                        "key 4" : "value 4"
                    }
        (
            self.table.set_title("\n<b>This is the table's title</b>\n")
                       .set_object(table_obj)
                       .render()
        )

        print(self.table.save_tmp())

