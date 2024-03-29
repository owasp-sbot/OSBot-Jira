from osbot_jira.api.plantuml.API_Plant_UML import API_Plant_UML
from osbot_jira.api.plantuml.Puml_Base import Puml_Base
from osbot_utils.utils import Misc
from osbot_utils.utils.Files            import Files
from osbot_utils.utils.Str import str_safe


class Puml(Puml_Base):
    def __init__(self):
        super().__init__()
        self.available_elements   = ["actor"   , "agent"    , "artifact"  ,"boundary" , "card"      , "cloud"   , "component" ,
                                     "control" , "database" , "entity"    , "file"    , "folder"    , "frame"   , "interface" ,
                                     "node"    , "package"  , "queue"     , "stack"   , "rectangle" , "storage" , "usecase"   ]
        self.available_directions = ['up', 'down','left','right']
        self.on_add_node           = None
        self.on_add_edge           = None
        #self.max_title             = 250

    def add_card     (self, title, id = None) : return self.add_node("card", title, id)
    def add_cloud    (self, title, id = None) : return self.add_node("cloud", title, id)
    def add_actor    (self, title, id = None) : return self.add_node("actor", title, id)
    def add_interface(self, title, id = None) : return self.add_node("interface", title, id)

    def add_node(self, element, title, id = None):

        #title = Misc.word_wrap(title, self.max_title)      # this was causing errors with large titles that broke plantuml

        if self.on_add_node:                                # if self.on_add_node is set, then use it for the node render bit
            id_fixed    = self.fix_id(id)
            puml_to_add = self.on_add_node(element, title, id_fixed, id)
            #print(puml_to_add)
            if puml_to_add:
                self.puml += "\t{0} \n".format(puml_to_add)
        else:
            if id:
                self.puml += '\t{0} "{1}" as {2} \n'.format(element, title, self.fix_id(id))
            else:
                self.puml += '\t{0} "{1}"\n'        .format(element, title)
        return self

    def add_edge(self, from_id, to_id, direction = 'down', label=""):
        self.puml += '\t{0} -{2}-> {1} : "{3}" \n'.format(self.fix_id(from_id), self.fix_id(to_id), direction ,label)
        return self



    def add_title(self, title):
        if title:
            self.add_line(f"title {title}")
        return self

    def add_footer(self, footer):
        if footer:
            self.add_line(f"\n\tcenter footer {footer}")
        return footer


    def get_puml(self):
        return self.puml

    def startuml(self):
        self.puml += "@startuml\n"
        return self

    def enduml(self):
        self.puml += "@enduml\n"
        return self

    def fix_id(self, id):
        return str_safe(id)
        #if id:
        #    return id.replace(' ','_').replace('-','_').replace(':','_').replace('/','_').replace('(','_').replace(')','_')



    def set_on_add_node(self, callback): self.on_add_node = callback ; return self
    def set_on_add_edge(self, callback): self.on_add_edge = callback ; return self

    def __str__(self):
        return self.puml


