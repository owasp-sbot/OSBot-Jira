from pbx_gs_python_utils.plantuml.Puml import Puml


class API_Simple_Diagram (Puml):

    def add_anchor(self, id, direction='down'):
        return self.add_line("(*) -{0}-> {1}".format(direction,id))

    def create(self):
        (
            self.startuml()
                #.add_anchor("asd",'left')
                #.add_anchor("123", "up")
                .add_card("this is A"  , "a")
                .add_card("this is B"  , "b")
                .add_actor("this is C" , "c")
                .add_actor("this is D" , "d")
                .add_edge("a", "b" , "right")
                .add_edge("a", "c" , "down")
                .add_edge("b", "c" , "up" )
                .add_edge("a", "d", "right")
                .enduml()
        )
        return self

