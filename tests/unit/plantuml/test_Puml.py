import random
import unittest

from osbot_jira.api.plantuml.Puml import Puml


class Test_Puml(unittest.TestCase):

    def setUp(self):
        self.puml = Puml().startuml()
        self.path_png = '/tmp/test_simple_diagram.png'
        self.path_puml = '/tmp/test_simple_diagram.puml'

    def create_png(self):
        self.puml.enduml() \
            .png(self.path_png)
        #self.puml.save(self.path_puml)      # doesn't work when PyCharm auto test execution is on


    def test_add_element(self):
        (self.puml  .add_node("node", "I'm an node")
         .add_node("actor", "ABC")
         .add_node("actor", "XYZ")
         .add_edge("ABC", "XYZ", "down"))
        self.create_png()



    def test____show_all_elements(self):
        self.puml.add_node('usecase', "*", "center")
        for name in self.puml.available_elements:
            self.puml.add_node(name, name, name)
            self.puml.add_edge('center',name,random.sample(self.puml.available_directions, 1).pop())
        self.create_png()


    def test___adding_cards_and_edges(self):
        puml = self.puml
        (   puml.add_card   ("this AAAA is A", "a"    )
                .add_card   ("this is B", "b"    )
                .add_actor  ("this is C", "c"    )
                .add_actor  ("this is D", "d"    )
                .add_edge   ("a", "b", "right"   )
                .add_edge   ("a", "c", "down"    )
                .add_edge   ("b", "c", "up"      )
                .add_edge   ("a", "d", "right"   )
                .add_node("node", "am queue")
                .enduml()                        )
        self.create_png()


