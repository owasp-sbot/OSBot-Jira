from    unittest        import TestCase

from osbot_jira.api.plantuml.API_Plant_UML import API_Plant_UML
from osbot_utils.utils.Dev import pprint


class Test_API_Plant_UML(TestCase):
    def setUp(self):
        self.plantuml = API_Plant_UML()


    def test_pump_to_png_via_local_server(self):                            # needs plantuml docker version to be running
        target_file = '/tmp/puml_test.png'
        puml     =  "@startuml \n aaaaaaa->bbb \n @enduml"
        #puml     = Files.contents('../../data/puml/simple.puml')
        png_file = self.plantuml.puml_to_png_via_local_server(puml=puml, target_file=target_file)

        pprint(target_file)
        #Show_Img.from_path(png_file)


    def test_puml_to_png_using_lambda_function(self):
        puml = "@startuml \n aaa->bbb \n @enduml"
        png_file = self.plantuml.puml_to_png_using_lambda_function(puml)

        #Show_Img.from_path(png_file)











