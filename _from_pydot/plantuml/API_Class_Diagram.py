from pbx_gs_python_utils.plantuml.API_Plant_UML import API_Plant_UML
from pbx_gs_python_utils.utils.slack.API_Slack import API_Slack
#from utils.Show_Img import Show_Img


class API_Class_Diagram:

    def __init__(self):
        self.plantuml = API_Plant_UML()
        self.nodes    = {}
        self.edges    = []


    def add_node(self,id, title, description  = None, icon_letter = None, color_letter = 'LightPink',
                                line_1        = None, line_2      = None, line_3     = None,
                                title_size    = None , title_color = None) :
        self.nodes[id] = { 'name'        : title         ,
                           'description' : description   ,
                           'icon_letter' : icon_letter   ,
                           'color_letter': color_letter  ,
                           'line_1'      : line_1        ,
                           'line_2'      : line_2        ,
                           'line_3'      : line_3        ,
                           'title_size'  : title_size    ,
                           'title_color' : title_color   }
        return self

    def add_edge(self, node_from, node_to, label):
        self.edges.append ({ "from": node_from , "to" : node_to , "label" : label } )

    def puml(self):

        puml = "@startuml                   \n"
        puml += "\ttop to bottom direction  \n"
        #puml += "\tleft to right direction  \n"
        #puml += "\tscale 3024 width   \n"

        for id, node in self.nodes.items():
            name = node['name']
            if node.get('title_size'): name = '<size:{0}>{1}</size>'.format(node['title_size'], name)
            if node.get('title_color'): name = '<color:{0}>{1}</color>'.format(node['title_color'], name)
            puml += '\tclass "{0}" as {1}    '.format(name, id)
            if node.get('icon_letter'):
                puml += '<< ({0},{1}) >>'.format(node['icon_letter'], node['color_letter'])
            puml += '{{\n\t\t{0}            \n'.format(node['description'])

            if node.get('line_1'): puml += '\t\t' + node['line_1'] + '\n'
            if node.get('line_2'): puml += '\t\t' + node['line_2'] + '\n'
            #if node.get('line_3'): puml += '\t\t' + node['line_3'] + '\n'

            puml += '\t}                    \n'
            puml += '                       \n'
        for edge in self.edges:
            puml += '\t{0:10} --> {1:10} : "{2}" \n'.format(edge['from'], edge['to'], edge['label'])
        puml += "@enduml"
        return puml

    # def show(self):
    #     png_file = self.plantuml.puml_to_png(self.puml())
    #
    #     #     Show_Img.from_path(png_file)
    #     Show_Img.from_path(png_file)
    #     return png_file


    def send_to_slack(self):
        puml = self.puml()
        #API_Slack().send_message('about to send puml to Slack')
        API_Slack().puml_to_slack(puml)


    # Jira specific helper methods (beggining of an DSL)

    def add_risk(self, key, summary, status, risk_rating, labels='', font_size = 20):
        risk = '+{0} risk'.format(risk_rating)
        self.add_node(key, summary, 'status: '+ status, 'R', 'LightPink', '--'+key+'--', risk, '-' + labels,font_size, '#Brown ')
