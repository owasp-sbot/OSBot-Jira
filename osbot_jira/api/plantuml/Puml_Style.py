from osbot_utils.utils.Dev import pprint


class Puml_Style:
    def __init__(self):
        self.style         = ""
        self.styles        = {}
        self.custom_styles = {}

    def add_style(self, name, data, depth=None):
        self.styles[name] = data #{ "data": data, "depth": depth }
        return self

    def add_style_node(self, data, depth=None):
        return self.add_style('node', data, depth)

    def add_custom_style(self, name, data):
        self.custom_styles[name] = data
        return self

    def render(self):
        self.style = "<style>\n"
        self.render_styles()
        self.render_custom_styles()
        self.style += "</style>\n"

        return self.style

    def render_styles(self):
        styles = ""
        for name, data in self.styles.items():
            styles += f"\t{name} {{\n"
            for key, value, in data.items():
                if type(value) is not dict:
                    styles += f"\t\t{key}  {value}\n"
                else:
                    styles += f"\t\t\t{key} {{\n"
                    for sub_key, sub_value in value.items():
                        styles += f"\t\t\t\t{sub_key}  {sub_value}\n"
                    styles += f"\t\t\t}}\n"
            styles += "\t}\n"

        self.style += styles

    def render_custom_styles(self):
        custom_styles = ""
        for name, data in self.custom_styles.items():
            custom_styles += f".{name} {{\n"
            for key, value, in data.items():
                custom_styles += f"    {key}  {value}\n"
            custom_styles += "}\n"
        self.style += custom_styles