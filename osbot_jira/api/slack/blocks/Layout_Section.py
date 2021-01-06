from osbot_utils.utils import Misc

from osbot_jira.api.slack.blocks.Layout_Actions import Layout_Actions


class Layout_Section:
    def __init__(self, blocks, action_id=None,block_id=None):
        self.action_id = action_id
        self.block_id  = block_id
        self.blocks    = blocks
        self.text      = None
        self.fields    = []
        self.accessory = {}
        if block_id is None:
            self.block_id = Misc.random_string_and_numbers(4, 'block_')

    def add_text(self, text, text_type='mrkdwn', emoji=None, verbatim=None):
        element = {"text": text , "type": text_type }

        if emoji    is not None: element['emoji'   ] = emoji
        if verbatim is not None: element['verbatim'] = verbatim

        self.text = element
        return self

    def add_field(self, text, field_type='mrkdwn'):
        self.fields.append({ 'text': text, 'type': field_type})

    def add_fields(self, fields):
        for field in fields:
            self.add_field(field)

    # todo: refactor these (since at the moment we are reusing the methods from Layout_Actions
    def add_button(self, text, url=None, value=None, style=None,confirm=None):
        self.accessory = Layout_Actions(self.action_id,[]).add_button(text, value, url, style, confirm).elements.pop()
        return self

    def add_date_picker(self, text, action_id, initial_date=None, confirm=None):
        self.accessory = Layout_Actions(self.action_id, []).add_date_picker(text, action_id, initial_date, confirm).elements.pop()
        return self

    def add_overflow(self, options, action_id=None, confirm=None):
        self.accessory = Layout_Actions(self.action_id, []).add_overflow(options, action_id, confirm).elements.pop()
        return self

    def add_select(self, text, options=None, option_groups=None, action_id=None, initial_option=None, confirm=None):
        self.accessory = Layout_Actions(self.action_id, []).add_select(text,options, option_groups,action_id, initial_option, confirm).elements.pop()
        return self

    def add_select_users(self, text, action_id, initial_user=None, confirm=None):
        self.accessory = Layout_Actions(None, []).add_select_users(text, action_id, initial_user,confirm).elements.pop()
        return self

    def add_select_channel(self, text, action_id, initial_channel=None, confirm=None):
        self.accessory = Layout_Actions(None, []).add_select_channel(text, action_id, initial_channel,confirm).elements.pop()
        return self

    def add_select_external(self, text, action_id, initial_option=None, min_query_length=None, confirm=None):
        self.accessory = Layout_Actions(None, []).add_select_external(text, action_id, initial_option,min_query_length, confirm).elements.pop()
        return self

    def render(self):
        element = { "type": "section", "block_id": self.block_id }

        if self.accessory: element['accessory'] = self.accessory
        if self.fields   : element['fields'   ] = self.fields
        if self.text     : element['text'     ] = self.text

        self.blocks.append(element)
        return self
