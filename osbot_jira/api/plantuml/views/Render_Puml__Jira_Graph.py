import textwrap

from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import path_combine, file_exists, file_contents_as_bytes, create_folder, file_copy
from osbot_utils.utils.Misc import upper, bytes_to_base64, word_wrap_escaped, trim

URL_GITHUB_ISSUE_REPO = "http://localhost:8080/jira_project_icons/" #"https://raw.githubusercontent.com/owasp-sbot/OSBot-Browser/master/osbot_browser/web_root/vivagraph/icons/"
class Render_Puml__Jira_Graph:

    def __init__(self, jira_graph:Jira_Graph):
        self.jira_graph                = jira_graph
        self.skin_params               = self.default_skin_params()
        self.created_png_file          = None
        self.on_resolve_card_color     = None
        self.on_resolve_card_text      = None
        self.show_project_icons        = True
        self.summary_wrap_at           = 50
        self.title                     = ''
        self.footer                    = ''
        self.save_png_copy_using_title = True
        self.folder_pngs_by_title    = '/tmp/pngs_by_title'
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
                 'linetype'             : 'polyline'   } #polyline | ortho
        # skinparam dpi 10
        #           handwritten True
    def on_add_node(self, element, card_text, id_plant_uml, id_jira):
        issue           = self.jira_graph.issues.get(id_jira)
        card_color      = 'white'
        if issue:
            issue_type      = upper(issue.get('Issue Type'))
            card_color      = self.resolve_card_color(issue)
            png_file        = path_combine(__file__, f"../../../../../../../modules/OSBot-Browser/osbot_browser/web_root/vivagraph/icons/{issue_type}.png")
            card_text       = self.resolve_card_text(issue)

            if self.show_project_icons and file_exists(png_file):
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

    def set_show_project_icons(self, value):
        self.show_project_icons = value
        return self

    def set_skin_param_linetype_ortho(self):
        self.skin_params['linetype'] = 'ortho'
        return self

    def set_skin_param_linetype_polyline(self):
        self.skin_params['linetype'] = 'polyline'
        return self

    def set_skin_param_linetype_splines(self):
        self.skin_params['linetype'] = 'splines'       # default
        return self

    def set_summary_wrap_at(self, value):
        self.summary_wrap_at = value
        return self

    def set_on_resolve_card_color(self, on_resolve_card_color):
        self.on_resolve_card_color = on_resolve_card_color
        return self

    def set_on_resolve_card_text(self, on_resolve_card_text):
        self.on_resolve_card_text = on_resolve_card_text
        return self

    def set_title(self, value):
        self.title = value or ''
        return self

    def set_footer(self, value):
        self.footer = value
        return self


    def render(self):
        self.apply_skin_params()
        self.jira_graph.set_puml_on_add_node(self.on_add_node)
        self.jira_graph.set_title (self.title)
        self.jira_graph.set_footer(self.footer)
        self.jira_graph.render_puml()
        return self

    def save_as_png(self):
        (self.created_png_file,_) = self.jira_graph.puml.save_tmp(use_lambda=False)
        if self.save_png_copy_using_title:
            create_folder(self.folder_pngs_by_title)
            fixed_title = self.title.replace('\\n','')
            target_png_file = path_combine(self.folder_pngs_by_title, f"{fixed_title}.png")
            file_copy(self.created_png_file, target_png_file)


    def resolve_card_color(self, issue):
        if self.on_resolve_card_color:
            return self.on_resolve_card_color(issue)
        issue_type = upper(issue.get('Issue Type'))                      # see all colors at https://plantuml.com/color or https://github.com/qywx/PlantUML-colors
        if issue_type == 'PERSON'               : return 'azure'
        if issue_type == 'CONTROL'              : return 'lightgreen'
        if issue_type == 'PENTEST'              : return 'MistyRose'
        if issue_type == 'SQUAD'                : return 'LightGoldenRodYellow'
        if issue_type == 'SUPPLIER'             : return 'LightGrey'
        if issue_type == 'RISK'                 : return 'MistyRose'# 'LightCoral'
        if issue_type == 'VULN'                 : return 'LightPink'
        if issue_type == 'PROJECT'              : return 'LightCyan'
        if issue_type == 'TEAM'                 : return 'LightSkyBlue'
        if issue_type == 'ROLE'                 : return 'LightSteelBlue'
        if issue_type == 'BUSINESS APPLICATION' : return 'LightYellow'
        if issue_type == 'OBJECTIVE'            : return 'LightYellow' #'OldLace'
        if issue_type == 'TASK'                 : return 'PowderBlue'
        if issue_type == 'PROGRAMME'            : return 'SeaShell'
        if issue_type == 'INCIDENT'             : return 'LavenderBlush'
        if issue_type == 'NIST CSF'             : return 'HoneyDew'
        if issue_type == 'GDPR'                 : return 'BlanchedAlmond'
        if issue_type == 'ENTITY'               : return 'Physical'
        if issue_type == 'ASSET'                : return 'Cornsilk'
        if issue_type == 'REQUEST'              : return 'FloralWhite'
        if issue_type == 'PRODUCT'              : return 'Gainsboro'
        if issue_type == 'MEETING'              : return 'Ivory'
        if issue_type == 'QUOTE'                : return 'Lavender'
        #if issue_type == 'CONTROL'              : return 'Linen'
        if issue_type == 'HIRING'               : return 'Motivation'
        if issue_type == 'ACTION'               : return 'MediumAquaMarine'
        if issue_type == 'POLICY'               : return 'MintCream'
        if issue_type == 'DECISION'             : return 'Moccasin'
        if issue_type == 'RACI'                 : return 'LightSeaGreen'
        if issue_type == 'QUESTION'             : return 'Azure'
        if issue_type == 'SLACK'                : return 'MintCream'
        if issue_type == 'DATE'                 : return 'LightBlue'
        if issue_type == 'PCIDSS'               : return 'MintCream' # duplicated
        if issue_type == 'EVIDENCE'             : return 'lightblue'
        if issue_type == 'RELEASE'              : return 'LightBlue' # duplicated
        if issue_type == 'APPROVAL'             : return 'Ivory'    # duplicated
        if issue_type == 'TRAINING'             : return 'White'    # duplicated
        if issue_type == 'SPRINT'               : return 'AquaMarine'
        if issue_type == 'KEY RESULT'           : return 'Aqua'


        # 'Aquamarine'
        # if issue_type == '': return 'LightSalmon'
        # if issue_type == '':  return ''

        print(f'[Render_Puml__Jira_Graph]no card color for: {issue_type}')
        return 'white'

    def resolve_card_text(self, issue):
        if self.on_resolve_card_text:
            card_text = self.on_resolve_card_text(issue)
            if card_text is not None:                         # if on_resolve_card_text returns None, return the default card_text
                return card_text
        id_jira         = issue.get('Key')
        status          = issue.get('Status')
        status_color    = self.resolve_status_color(status)
        summary_raw     = issue.get('Summary')
        if summary_raw:
            summary_wrapped = '\\n='.join(textwrap.wrap(summary_raw, self.summary_wrap_at))
            summary_wrapped = f"={summary_wrapped}\\n"
        else:
            summary_wrapped = ''

        if status:
            card_text = f"{summary_wrapped}<color:{status_color}>{status}</color>    |    {id_jira}"
        else:
            card_text = f"{summary_wrapped}{id_jira}"
        return card_text

    def resolve_status_color(self, status):
        blue_status  = ['Hired']
        green_status = ['Green (Active)', 'Active']
        red_status   = ['Red (Active)', 'No Resources', 'Needs Funding']
        amber_status = ['Amber (Active)']

        if status in amber_status : return 'darkGoldenRod'
        if status in blue_status  : return 'darkblue'
        if status in green_status : return 'darkgreen'
        if status in red_status   : return 'darkred'


        return 'black'