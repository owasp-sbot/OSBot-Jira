class API_Slack_Dialog():
    def __init__(self):
        self.title            = ""
        self.callback_id      = ""
        self.submit_label     = "Submit"
        self.state            = "#3AA3E3"
        self.elements         = []
        self.notify_on_cancel = True

    # def add_button(self, name, text, value, style = 'default'):
    #     self.actions.append({
    #                             "name"  : name       ,
    #                             "text"  : text       ,
    #                             "type"  : "button"   ,
    #                             "value" : value      ,
    #                             "style" : style     })
    #     return self
    #
    # def set_callback_id(self, callback_id):
    #     self.callback_id = callback_id
    #     return self
    #
    # def set_text(self, text):
    #     self.text = text
    #     return self

    def add_element_text(self, label, name, value = None, optional = False, hint = None, placeholder = None):
        element = {
                        "type"         : "text"      ,
                        "label"        : label       ,
                        "name"         : name        ,
                        "value"        : value       ,
                        "optional"     : optional    ,
                        "hint"         : hint        ,
                        "placeholder"  : placeholder
                   }
        self.elements.append(element)

    def add_element_textarea(self, label, name, value = None, optional = False, hint = None, placeholder = None):
        element = {
                        "type"         : "textarea"  ,
                        "label"        : label       ,
                        "name"         : name        ,
                        "value"        : value       ,
                        "optional"     : optional    ,
                        "hint"         : hint        ,
                        "placeholder"  : placeholder
                   }
        self.elements.append(element)

    def add_element_select(self, label, name, options, value = None):
        element = {
                        "type"         : "select" ,
                        "label"        : label    ,
                        "name"         : name     ,
                        "value"        : value    ,
                        "options"      : []
                   }
        for item in options:
           element['options'].append({"label": item[0], "value": item[1]})

        self.elements.append(element)

    def add_element_select_external(self, label, name, placeholder = None, optional = False):
        element = {
                        "type"             : "select"    ,
                        "label"            : label       ,
                        "name"             : name        ,
                        "data_source"      : "external"  ,
                        "placeholder"      : placeholder ,
                        "optional"         : optional    ,
                        "options"          : []
                        #"min_query_length" : 3           ,

                   }

        self.elements.append(element)

    def test_render(self):
        self.callback_id = 'issue-suggestion'
        self.title       = 'This is a test'
        self.add_element_text           ("label 1", "name_1", "value 1", "hint 1", "placeholder 1")
        #self.add_element_text           ("label 2", "name-2", "value 2", "hint 2", "placeholder 2")
        self.add_element_text           ("label 3", "name-3",)
        self.add_element_textarea       ("label 4", "name-4", "value 4", "hint 4", "placeholder 4")
        self.add_element_select         ("label 5", "name-5" ,[("label-1", "value-1"), ("label-2", "value-2")], "value-2")
        self.add_element_select_external("label 6", "name-6")
        return self.render()

    def render(self):
        return {
                    "callback_id"      : self.callback_id     ,
                    "title"            : self.title           ,
                    "submit_label"     : self.submit_label    ,
                    "notify_on_cancel" : self.notify_on_cancel,
                    "elements"         : self.elements        }