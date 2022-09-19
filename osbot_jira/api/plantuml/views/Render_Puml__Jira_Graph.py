from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, file_exists, file_contents_as_bytes
from osbot_utils.utils.Misc import upper, bytes_to_base64

URL_GITHUB_ISSUE_REPO = "http://localhost:8080/jira_project_icons/" #"https://raw.githubusercontent.com/owasp-sbot/OSBot-Browser/master/osbot_browser/web_root/vivagraph/icons/"
class Render_Puml__Jira_Graph:

    def __init__(self, jira_graph:Jira_Graph):
        self.jira_graph  = jira_graph
        self.skin_params = self.default_skin_params()
        # self.skin_params =  [('CardBorderColor'      , 'gray'    ),
        #                      ('CardBackgroundColor'  , 'white'   ),
        #                      ('Shadowing'            , True      ),
        #                      ('Padding'              , 0         ),
        #                      ('ArrowThickness'       , 1.5       ),
        #                      ('ArrowColor'           , 'darkblue'),
        #                      ('ArrowFontSize'        , 10        ),
        #                      ('roundCorner'          , 25        ),
        #                      ('linetype'             , 'ortho') # polyline | ortho
        #                      ]
                             #('handwritten'        , True     )

    def default_skin_params(self):
        return { 'CardBorderColor'      : 'gray'    ,
                 'CardBackgroundColor'  : 'white'   ,
                 'Shadowing'            : True      ,
                 'Padding'              : 0         ,
                 'ArrowThickness'       : 1.5       ,
                 'ArrowColor'           : 'darkblue',
                 'ArrowFontSize'        : 10        ,
                 'roundCorner'          : 25        ,
                 'linetype'             : 'ortho'   } #polyline | ortho

        #    ('CardBorderColor'      , 'gray'    ),
        #                      ('CardBackgroundColor'  , 'white'   ),
        #                      ('Shadowing'            , True      ),
        #                      ('Padding'              , 0         ),
        #                      ('ArrowThickness'       , 1.5       ),
        #                      ('ArrowColor'           , 'darkblue'),
        #                      ('ArrowFontSize'        , 10        ),
        #                      ('roundCorner'          , 25        ),
        #                      ('linetype'             , 'ortho') # polyline | ortho
        #                      ]
                             #('handwritten'        , True     )

    def on_add_node(self, element, card_text, id_plant_uml, id_jira):

        issue        = self.jira_graph.issues.get(id_jira)
        issue_type   = upper(issue.get('Issue Type'))
        summary      = issue.get('Summary')
        status       = issue.get('Status')
        status_color = self.resolve_status_color(status)
        card_color   = self.resolve_card_color(issue_type)
        png_file     = path_combine(__file__, f"../../../../../../../modules/OSBot-Browser/osbot_browser/web_root/vivagraph/icons/{issue_type}.png")
        card_text    = f"={summary}\\n<color:{status_color}>{status}</color>    |    {id_jira}"

        if file_exists(png_file):
            img_base64 = bytes_to_base64(file_contents_as_bytes(png_file))
            card_text = f"<img:data:image/png;base64,{img_base64}>  \\n{card_text}"


        puml_card = f'{element} "{card_text}" as {id_plant_uml} #{card_color}'#.format(element, card_text, id_plant_uml)
        #print(puml_card)
        return puml_card

    def set_skin_params(self, skin_params):
        self.skin_params.update(skin_params)
        return self

    def apply_skin_params(self):
        if self.skin_params:
            for name, value in self.skin_params.items():
                self.jira_graph.set_skin_param(name=name, value=value)
        return self

    def set_skin_param_linetype_ortho(self):
        self.skin_params['linetype'] = 'ortho'

    def set_skin_param_linetype_polyline(self):
        self.skin_params['linetype'] = 'polyline'

    def render(self):
        self.apply_skin_params()
        self.jira_graph.set_puml_on_add_node(self.on_add_node)
        self.jira_graph.render_puml()
        return self

    def save_as_png(self):
        return self.jira_graph.puml.save_tmp(use_lambda=False)

    def resolve_card_color(self, issue_type):
        if issue_type == 'PERSON'               : return 'lightblue'
        if issue_type == 'CONTROL'              : return 'lightgreen'
        if issue_type == 'PENTEST'              : return 'MistyRose'
        if issue_type == 'SQUAD'                : return 'LightGoldenRodYellow'
        if issue_type == 'SUPPLIER'             : return 'LightGrey'
        if issue_type == 'RISK'                 : return 'LightCoral'
        if issue_type == 'VULN'                 : return 'LightPink'
        if issue_type == 'PERSON'               : return 'LightSalmon'
        if issue_type == 'PROJECT'              : return 'LightCyan'
        if issue_type == 'TEAM'                 : return 'LightSkyBlue'
        if issue_type == 'ROLE'                 : return 'LightSteelBlue'
        if issue_type == 'BUSINESS APPLICATION' : return 'LightYellow'
        if issue_type == 'OBJECTIVE'            : return 'OldLace'
        if issue_type == 'TASK'                 : return 'PowderBlue'
        if issue_type == 'PROGRAMME'            : return 'SeaShell'
        if issue_type == 'INCIDENT'             : return 'LavenderBlush'
        if issue_type == 'NIST CSF'             : return 'HoneyDew'
        if issue_type == 'GDPR'                 : return 'BlanchedAlmond'
        if issue_type == 'ENTITY'               : return 'Azure'
        if issue_type == 'ASSET'                : return 'Cornsilk'
        if issue_type == 'REQUEST'              : return 'FloralWhite'
        if issue_type == 'PRODUCT'              : return 'Gainsboro'
        if issue_type == 'MEETING'              : return 'Ivory'
        if issue_type == 'QUOTE'                : return 'Lavender'
        if issue_type == 'CONTROL'              : return 'Linen'
        if issue_type == 'HIRING'               : return 'Motivation'
        if issue_type == 'ACTION'               : return 'MediumAquaMarine'
        if issue_type == 'POLICY'               : return 'MintCream'
        if issue_type == 'DECISION'             : return 'Moccasin'
        #if issue_type == '': return 'LightSeaGreen'

        print(issue_type)
        return 'white'

    def resolve_status_color(self, status):
        blue_status  = ['Hired']
        green_status = ['Green (Active)', 'Active']
        red_status   = ['Red (Active)', 'No Resources', 'Needs Funding']
        amber_status = ['Amber (Active)']

        if status in amber_status: return 'darkGoldenRod'
        if status in blue_status  : return 'darkblue'
        if status in green_status : return 'darkgreen'
        if status in red_status   : return 'darkred'


        return 'black'