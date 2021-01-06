from osbot_jira.api.plantuml.Puml import Puml


class Puml_Table(Puml):

    def __init__(self):
        self.title     = ""
        self.table_obj = {}
        super().__init__()

    def set_title(self,title):
        self.title = title
        return self

    def set_object(self, table_obj):
        self.table_obj = table_obj
        return self

    def render(self):
        self.startuml()
        self.add_line("title")
        self.add_line(self.title)
        self.render_table_obj()
        self.add_line("endtitle")
        self.enduml()
        return self

    def render_table_obj(self):
        keys = sorted(list(set(self.table_obj)))
        self.add_line("| key | value |")                                # title
        for key in keys:
            value = self.table_obj[key]
            line  = "| {0} | {1} |".format(key, value)           \
                                   .replace('\r', '')            \
                                   .replace('\n', ' ')                  # make remove new line chars
            self.add_line(line)
        return