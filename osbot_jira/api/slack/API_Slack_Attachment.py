class API_Slack_Attachment():
    def __init__(self, text = None, color = "#3AA3E3"):
        self.text        = text
        self.fallback    = None # "Sorry this feature is not supported in your device"
        self.callback_id = ""
        self.color       = color
        self.actions     = []

    def add_button(self, name, text, value, style = 'default'):
        self.actions.append({
                                "name"  : name       ,
                                "text"  : text       ,
                                "type"  : "button"   ,
                                "value" : value      ,
                                "style" : style     })
        return self

    def add_select(self, name, text, options):
        select = {  "name"    : name    ,
                    "text"    : text    ,
                    "type"    : "select",
                    "options" : []      }
        for option in options:
            select['options'].append({ "text": option[0], "value": option[1]})
        self.actions.append(select)
        return self

    def add_select_users        (self, name, text): return self.add_select_data_source(name, text, "users"        )
    def add_select_channels     (self, name, text): return self.add_select_data_source(name, text, "channels"     )
    def add_select_conversations(self, name, text): return self.add_select_data_source(name, text, "conversations")
    def add_select_external     (self, name, text): return self.add_select_data_source(name, text, "external"     )

    def add_select_data_source(self, name, text, data_source):
        select = {  "name"       : name    ,
                    "text"       : text    ,
                    "type"       : "select",
                    "data_source": data_source }
        self.actions.append(select)
        return self

    def set_callback_id(self, callback_id):
        self.callback_id = callback_id
        return self

    def set_color(self, color):
        self.color = color
        return self

    def set_text(self, text):
        self.text = text
        if self.fallback is None:
            self.fallback = text
        return self


    def render(self):
        item = {
                    "text"       : self.text        ,
                    "fallback"   : self.fallback    ,
                    "callback_id": self.callback_id ,
                    "color"      : self.color       ,
                    "actions"    : self.actions
                }
        return [item]

# class API_Slack_Button():
#     def init(self):
#         data = []
