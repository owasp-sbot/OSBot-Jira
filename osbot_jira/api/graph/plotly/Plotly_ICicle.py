from plotly import graph_objects

from osbot_utils.utils.Files import file_create_bytes


class Plotly_ICicle:

    def __init__(self):
        self.figure           = None
        self.icicle           = None
        self.jpg_scale        = 1.0
        self.jpg_path         = f"/tmp/plotly.jpg"
        self.issue_value_key  = 'Summary'
        self.colorscale       = ['lightBlue','darkBlue']
        self.ids              = []
        self.labels           = []
        self.parents          = []
        self.values           = []
        self.on_create_icicle = None
        self.on_create_figure = None

    def add_entry(self, id, parent, value=1,  label=None):
        self.ids     .append(id         )
        self.parents .append(parent     )
        self.values  .append(value      )
        self.labels  .append(label or id)
        return self


    def add_jira_graph(self, jira_graph, root_node= None):
        def get_label(jira_id):
            text = issues.get(jira_id, {}).get(self.issue_value_key)
            #return f"{text} - ({jira_id})"
            return text
        issues = jira_graph.issues or {}
        if root_node:
           self.add_entry(id=root_node, parent="", label=get_label(root_node))
        for (from_id, link_type, to_id) in jira_graph.edges:
            self.add_entry(id=to_id, parent=from_id, label=get_label(to_id))
        return self

    def create_icicle(self):
        self.icicle = graph_objects.Icicle(ids=self.ids, labels=self.labels, parents=self.parents, values=self.values)
        self.icicle.marker.colorscale = ['lightBlue', 'darkBlue']
        if self.on_create_icicle:
            self.on_create_icicle(self.icicle)
        return self

    def create_figure(self):
        self.figure = graph_objects.Figure(self.icicle)
        self.figure.update_layout(margin=dict(t=0, l=0,  r=0, b=0))
        #uniformtext = dict(minsize=40, mode='show')
        if self.on_create_figure:
            self.on_create_figure(self.icicle)
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