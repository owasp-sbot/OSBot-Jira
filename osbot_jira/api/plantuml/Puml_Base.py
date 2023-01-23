from osbot_jira.api.plantuml.API_Plant_UML import API_Plant_UML
from osbot_utils.utils.Files import Files


class Puml_Base:

    def __init__(self):
        self.puml = ""
        self.api_plantuml = API_Plant_UML()

    def add_line(self, line):
        self.puml +=f"\t{line}\n"
        return self

    def png(self, path = None, use_lambda=True):
        if path:
            self.api_plantuml.tmp_png_file = path
        self.api_plantuml.puml_to_png(puml=self.puml, use_lambda=use_lambda)
        return self

    def save(self, path):
        Files.write(path,self.puml)
        return self

    def save_tmp(self, use_lambda=True):
        tmp_path_png = '/tmp/jira_graph.png'
        tmp_path_puml = '/tmp/jira_graph.puml'
        ( self.png (path=tmp_path_png, use_lambda=use_lambda)
              .save(path=tmp_path_puml                      ))
        return tmp_path_png,tmp_path_puml