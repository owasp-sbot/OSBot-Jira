from osbot_jira.api.plantuml.Puml_Base import Puml_Base


class Puml_WBS(Puml_Base):

    def __init__(self):
        super().__init__()
        pass


    def startuml(self):
        self.puml += "@startuml\n"
        return self

    def enduml(self):
        self.puml += "@enduml\n"
        return self

