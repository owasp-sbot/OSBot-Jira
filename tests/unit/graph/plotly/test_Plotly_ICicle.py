from unittest import TestCase

from osbot_jira.api.graph.Jira_Graph import Jira_Graph
from osbot_jira.api.graph.plotly.Plotly_ICicle import Plotly_ICicle
from osbot_utils.utils.Dev import pprint


class test_Plotly_ICicle(TestCase):

    def setUp(self) -> None:
        self.plotly_icicle = Plotly_ICicle()

    def test_add_entry(self):
        self.plotly_icicle.add_entry("a","")
        self.plotly_icicle.add_entry("b", "a")

        (self.plotly_icicle.create_icicle()
                           .create_figure()
                           .save_as_jpg  ())

    def test_add_jira_graph(self):
        jira_graph = Jira_Graph()
        jira_graph.add_edge("a", "", "b")
        jira_graph.add_edge("a", "", "c")
        jira_graph.add_edge("a", "", "d")
        self.plotly_icicle.add_jira_graph(jira_graph)
        self.plotly_icicle.create_jpg()

    # def test_icicle(self):
    #     import plotly.express as px
    #     data = dict(
    #         character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura","abc","Enoch_2"],
    #         parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ,"Enoch","Cain"],
    #         value=[4, 2, 2, 1, 1, 1, 1, 1, 1, 1,1])
    #
    #
    #     fig =px.icicle(
    #         data,
    #         names='character',
    #         parents='parent',
    #         values='value',
    #         color='value',
    #         color_continuous_scale= ['lightblue','darkblue'],
    #
    #     )
    #     fig.layout.coloraxis.colorbar.title.text= 'aaaaa'
    #
    #     #fig.layout.coloraxis.colorbar.tickwidth = 0
    #     #fig.layout.coloraxis.colorbar.borderwidth = 0
    #     #fig.layout.coloraxis.colorbar.outlinewidth = 0
    #     #fig.layout.coloraxis.colorbar.update({"visible":False})
    #     #fig.layout.legend = {}
    #     #fig.layout.coloraxis.colorscale = 'blues'
    #     #fig.layout.showlegend= False
    #     #pprint(dir(fig))
    #     pprint(fig._layout)
    #     #pprint(fig._layout_defaults)
    #     #pprint(fig._layout_obj)
    #     #print(fig.plotly_relayout)
    #     fig.update(layout_showlegend=False)
    #     fig.update_traces(root_color="lightgrey",visible=True)
    #     fig.update_layout(margin = dict(t=50, l=25, r=25, b=25), showlegend=False)
    #     #fig.plotly_relayout(relayout_data=data)
    #     self.plotly_icicle.figure = fig
    #     self.plotly_icicle.save_as_jpg()
    #
    #
    # def test_icicle_2(self):
    #     import plotly.graph_objects as go
    #
    #     import plotly.express as px
    #     data = dict(
    #         character= ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura", "abc", "Enoch_2"],
    #         parent   = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve", "Enoch", "Cain"],
    #         value    = [4, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1])
    #
    #     ids     = ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura", "abc" , "Enoch_2","a", "b" , "c", "d"]
    #     labels  = ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura", "abc" , "Enoch_2", "a", "b", "c", "d"]
    #     parents = [""   , "Eve" , "Eve" , "Seth", "Seth", "Eve" , "Eve" , "Awan", "Eve"   , "Enos", "abc"   , "Seth" , "Seth","abc", "c"]
    #     values = [6     , 5     , 5     , 4     , 4     , 3     , 3     , 2     , 2     , 3     , 1 ,1, 1, 2, 1]
    #     colors  = ['red', 'green', 'blue', 'white', 'red']
    #     icicle = go.Icicle(ids= ids, labels=labels, parents=parents, values=values) #marker=dict(colors=colors)
    #     #icicle.marker.colors=colors
    #     icicle.marker.colorscale = ['lightBlue','darkBlue']
    #     fig = go.Figure(icicle)
    #     fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    #     pprint(icicle.marker)
    #     self.plotly_icicle.figure = fig
    #     self.plotly_icicle.save_as_jpg()
    #
    #
    #     # colors (blue)
    #     # #00008A
    #     # #0000A7
    #     # #0000C4
    #     # #0000E2
    #     # #0002FF
    #     # #0038FF
    #     # #0072FF
    #     # #00AFFF
    #     # #00EEFF
    #
    #     # colors (blue)
    #     ##00008A
    #     #0000C4
    #     #0002FF
    #     #0072FF
    #     #00EEFF