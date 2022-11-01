from plotly import graph_objects

from osbot_utils.utils.Files import file_create_bytes


class Plotly_ICicle:

    def __init__(self):
        self.figure            = None
        self.icicle            = None
        self.jpg_scale         = 1.0
        self.jpg_path          = f"/tmp/icicle-graph.jpg"
        self.issue_value_key   = 'Summary'
        #self.colorscale        = ['lightBlue','darkBlue']
        self.text_color        = "black"
        self.text_minsize      = None
        self.marker_color      = "lightBlue"
        self.label_add_jira_id = False
        self.ids               = []
        self.labels            = []
        self.parents           = []
        self.values            = []
        self.colors            = []
        self.pl_margin_top     = 0
        self.pl_margin_left    = 0
        self.pl_margin_right   = 0
        self.pl_margin_bottom  = 0
        self.on_add_label      = None
        self.on_add_color      = None
        self.on_create_icicle  = None
        self.on_create_figure  = None

    def set_label_add_jira_id(self,value):
        self.label_add_jira_id = value
        return self

    def set_on_add_color(self, on_add_color):
        self.on_add_color = on_add_color
        return self

    def set_on_add_label(self, on_add_label):
        self.on_add_label = on_add_label
        return self

    def set_on_create_figure(self, on_create_figure):
        self.on_create_figure = on_create_figure
        return self

    def set_on_create_icicle(self, on_create_icicle):
        self.on_create_icicle = on_create_icicle
        return self


    def add_entry(self, id, parent, value=1,  label=None, color=None):
        self.ids     .append(id         )
        self.parents .append(parent     )
        self.values  .append(value      )
        self.labels  .append(label or id)
        self.colors  .append(color)
        return self


    def add_jira_graph(self, jira_graph, root_node= None):
        def get_label(jira_id):
            issue = issues.get(jira_id, {})
            text = issue.get(self.issue_value_key, '')
            if self.label_add_jira_id:
                text += f" - {jira_id}"
            if self.on_add_label:
                return self.on_add_label(jira_id, text, issue)
            return text

        def get_color(jira_id):
            if self.on_add_color:
                issue = issues.get(jira_id, {})
                return self.on_add_color(issue)
            return self.marker_color

        issues = jira_graph.issues or {}
        if root_node:
            if root_node is list:
                for key in root_node:
                    self.add_entry(id=key, parent="", label=get_label(key), color=get_color(key))
            else:
                self.add_entry(id=root_node, parent="", label=get_label(root_node), color=get_color(root_node))
        for (from_id, link_type, to_id) in jira_graph.edges:
            self.add_entry(id=to_id, parent=from_id, label=get_label(to_id), color=get_color(to_id))
        return self

    def create_icicle(self):
        # can replace graph_objects.Icicle with graph_objects.Treemap
        self.icicle = graph_objects.Icicle(ids      = self.ids      ,
                                           labels   = self.labels   ,
                                           parents  = self.parents  ,
                                           values   = self.values   ,
                                           textfont = dict(color=self.text_color))
                                           #tiling = dict(orientation='v',flip='x'))
        #self.icicle.tiling =
        #self.icicle.marker.colorscale = ['lightBlue', 'darkBlue']
        self.icicle.marker.colors = self.colors
        if self.on_create_icicle:
            self.on_create_icicle(self.icicle)
        return self

    def create_figure(self):
        self.figure = graph_objects.Figure(self.icicle)
        self.figure.update_layout(margin=dict(t=self.pl_margin_top, l=self.pl_margin_left,  r=self.pl_margin_right, b=self.pl_margin_bottom))
        if self.text_minsize:
            self.figure.update_layout(uniformtext = dict(minsize=self.text_minsize, mode='show'))

        if self.on_create_figure:
            self.on_create_figure(self.figure)
        return self

    def create_jpg(self):
        (self.create_icicle()
             .create_figure()
             .save_as_jpg  ())
        return self

    def set_jpg_scale(self, value):
        self.jpg_scale = value
        return self

    def save_as_jpg(self):
        if self.figure:
            image_bytes = self.figure.to_image(format='jpg', scale=self.jpg_scale)
            file_create_bytes(path=self.jpg_path, bytes=image_bytes)
        return self