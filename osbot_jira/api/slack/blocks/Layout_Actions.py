from osbot_utils.utils import Misc


class Layout_Actions:
    def __init__(self, action_id, blocks, block_id=None):
        self.action_id = action_id
        self.block_id  = block_id
        self.blocks    = blocks
        self.elements  = []


    def resolve_action_id(self,text):
        method = text.replace(' ','_').lower()
        return "class_method::{0}::{1}".format(self.action_id, method)

    def add_button(self, text, value=None, action_id=None, url=None, style=None,confirm=None):
        if action_id is None:
            action_id = text
        button = {'type'     : "button"                              ,
                  'text'     : {"type": 'plain_text', "text": text } ,
                  'action_id': self.resolve_action_id(action_id)     }
        if url      : button['url'      ] = url
        if style    : button['style'    ] = style
        if value    : button['value'    ] = value
        if confirm  : button['confirm'  ] = confirm

        self.elements.append(button)
        return self

    def add_date_picker(self, text,  action_id, initial_date=None, confirm=None):
        date_picker = { "type"       : "datepicker" ,
                        "placeholder": { "type": "plain_text","text": text }}

        if action_id   : date_picker['action_id'   ] = action_id
        if confirm     : date_picker['confirm'     ] = confirm
        if initial_date: date_picker['initial_date'] = initial_date

        self.elements.append(date_picker)
        return self

    def add_overflow(self, options, action_id=None, confirm=None):
        select = { "type"       : "overflow" ,
                   "options"    : []}

        if action_id : select['action_id'] = action_id
        if confirm   : select['confirm'  ] = confirm

        for option in options:
            item = { "text" : {"type": "plain_text","text": option[0]},"value": option[1]}
            select['options'].append(item)

        self.elements.append(select)
        return self

    def add_select(self, text, options=None, option_groups=None, initial_option=None, confirm=None):

        select = { "type"       : "static_select"                      ,
                   "placeholder": { "type": "plain_text","text": text  },
                   'action_id'  : self.resolve_action_id(text         )}


        if confirm   : select['confirm'  ] = confirm

        if options:
            select['options'] = []
            for option in options:
                item = { "text" : {"type": "plain_text","text": option[0]},"value": option[1]}
                select['options'].append(item)
                if initial_option and option[1] == initial_option:
                    select['initial_option'] = item
        if option_groups:
            select['option_groups'] = []
            for option_group in option_groups:
                group = { "label" : { "type": "plain_text","text": option_group[0]},
                          "options": []}
                for option in option_group[1]:
                    item = { "text" : {"type": "plain_text","text": option[0]},"value": option[1]}
                    group['options'].append(item)
                    if initial_option and option[1] == initial_option:
                        select['initial_option'] = item
                select['option_groups'].append(group)
        self.elements.append(select)
        return self

    def add_select_users(self, text, action_id, initial_user=None, confirm=None):
        select = { "action_id"   : action_id      ,
                   "type"        : "users_select" ,
                   "placeholder" : { "type": "plain_text","text": text }}
        if initial_user: select['initial_user'] = initial_user
        if confirm     : select['confirm'     ] = confirm
        self.elements.append(select)
        return self

    def add_select_channel(self, text, action_id, initial_channel=None, confirm=None):
        select = { "action_id"   : action_id      ,
                   "type"        : "channels_select" ,
                   "placeholder" : { "type": "plain_text","text": text }}

        if initial_channel: select['initial_channel'] = initial_channel
        if confirm        : select['confirm'        ] = confirm

        self.elements.append(select)
        return self

    def add_select_external(self,text, action_id, initial_option=None, min_query_length=None, confirm=None):
        select = {"action_id"   : action_id,
                  "type"        : "external_select",
                  "placeholder" : {"type": "plain_text", "text": text}}

        if initial_option  : select['initial_option'  ] = initial_option
        if min_query_length: select['min_query_length'] = min_query_length
        if confirm         : select['confirm'         ] = confirm

        self.elements.append(select)
        return self

    def render(self):
        if self.block_id is None:
            self.block_id = Misc.random_string_and_numbers(4, 'block_')
        self.blocks.append({"type"    : "actions"      ,
                            "block_id": self.block_id  ,
                            "elements": self.elements} )
        return self