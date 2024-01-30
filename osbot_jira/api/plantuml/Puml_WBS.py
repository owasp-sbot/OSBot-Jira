from osbot_jira.api.plantuml.Puml_Base import Puml_Base
from osbot_jira.api.plantuml.Puml_Style import Puml_Style
from osbot_utils.utils.Int import int_is_even

DEFAULT_BOX_COLOR = 'WhiteSmoke'

class Puml_WBS(Puml_Base):

    def __init__(self):
        super().__init__()
        self.style                    = Puml_Style()
        self.cut_of_point__remove_box = 5
        self.cut_of_point__even_odd   = 2
        pass

    def add_line(self, line):
        self.puml +=f"{line}\n"
        return self

    def add_tree_node(self, tree_node, level=1, index=1):
        text      = tree_node.get('text')
        style     = tree_node.get('style')

        direction = ""

        if level > self.cut_of_point__remove_box:
            direction += '_'
        elif level > self.cut_of_point__even_odd:
            if  int_is_even(index):
                direction = '<'
        # add current node
        self.add_item(text, direction=direction, level=level, style=style)
        # process child nodes
        for child_index, child_node in enumerate(tree_node.get('children', [])):
            self.add_tree_node(child_node, level=level+1, index=child_index)
        pass

    def add_item(self, text, direction='', level=1, style=None):
        prefix     = f"{'*' * level}{direction}"
        line       = f"    {prefix} {text}"
        if style:
            line += f" <<{style}>>"
        self.puml += f"    {line}\n"
        return self

    def add_style(self):
        style = self.style.render()
        self.puml += f"{style}\n"

    def create_from_tree_data(self, tree_data):
        self.startuml()
        self.add_line("scale 2")
        self.add_style()
        self.add_tree_node(tree_data)
        self.enduml()

    def startuml(self):
        self.puml += "@startwbs\n"
        return self

    def enduml(self):
        self.puml += "@endwbs\n"
        return self

