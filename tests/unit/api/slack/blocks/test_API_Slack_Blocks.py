from unittest import TestCase

from osbot_utils.utils.Dev import Dev

from osbot_jira.api.slack.blocks.API_Slack_Blocks import API_Slack_Blocks


class test_API_Slack_Blocks(TestCase):
    def setUp(self):
        self.api     = API_Slack_Blocks()
        self.result  = None
        self.channel = 'DDKUZTK6X'
        self.team_id = 'T7F3AUXGV'
        #self.team_id = 'T0SDK1RA8'
        #self.channel = 'C77N26S9K' #, 'DJXSMSQH3' #''GJKBUSLJE' #'DG30MH0KV'

    def tearDown(self):
        self.send_message()
        if self.result is not None:
            Dev.pprint(self.result)

    def send_message(self):
        result = self.api.send_message(self.channel, self.team_id)
        if result.get('ok') is False:
            self.result = result
        else:
            assert result.get('ok') is True

    def test_set_icon_emoji(self):
        self.api.set_text('before 1st test').set_as_user(True)      # this seems to reset the use of emojies in Slack
        self.send_message()
        self.api.set_text('with chart_with_upwards_trend').set_as_user(False).set_icon_emoji(':chart_with_upwards_trend:')
        self.send_message()
        self.api.set_text('before 2nd test').set_as_user(True)
        self.send_message()
        self.api.set_text('with point_right').set_as_user(False).set_icon_emoji(':point_right:')

    def test_set_icon_url(self):
        self.api.set_text('before 1st test').set_as_user(True)  # this seems to reset the use of emojies in Slack
        self.send_message()
        self.api.set_text('with icon url').set_as_user(False).set_icon_url('http://lorempixel.com/48/48')

    def test_set_link_names(self): # todo: not working as expected
        names = '@dinis.cruz  | #general'
        self.api.set_text('with set_link_names = False: ' + names)
        self.send_message()
        self.api.set_link_names(True).set_text('now set to True: ' + names)
        self.send_message()
        self.api.set_link_names(False).set_text('back to False: ' + names)


    def test_set_text(self):
        self.api.set_text('this is an text using the api that supports blocks')

    def test_set_mrkdwn(self): # todo: not working as expected
        text = 'this `is` some *markdown* formating  \n - abc \n -xyz'
        self.api.set_text(text).set_mrkdwn(False)
        self.send_message()
        assert self.api.kwargs.get('mrkdwn') is False
        self.api.set_text(text).set_mrkdwn(True)
        self.send_message()
        assert self.api.kwargs.get('mrkdwn') is True

    def test_set_parse(self): # todo: not working as expected
        text = '(for parse) this `is` some *markdown* formating  \n - abc \n -xyz'
        self.api.set_text(text)
        self.send_message()     # defaults to none
        self.api.set_parse('full')

    def test_set_username(self):
        self.api.set_text('This is from an not existing user')   \
                .set_as_user(False)                              \
                .set_icon_url('http://lorempixel.com/48/48')     \
                .set_username('User XYZ')

    # add layouts

    def test_add_layout_actions(self):
        self.api.set_text('with action layouts')
        actions = self.api.add_layout_actions('action_id_1',"actionblock789")
        actions.add_button('first button')
        actions.add_button('primary'  , style='primary')
        actions.add_button('danger', style='danger')
        actions.add_button('bbx',  value='abc', url='https://news.bbc.co.uk',
                                   confirm={
                                              "title": {
                                                  "type": "plain_text",
                                                  "text": "Are you sure?"
                                              },
                                              "text": {
                                                  "type": "mrkdwn",
                                                  "text": "Wouldn't you prefer a good game of _chess_?"
                                              },
                                              "confirm": {
                                                  "type": "plain_text",
                                                  "text": "Do it"
                                              },
                                              "deny": {
                                                  "type": "plain_text",
                                                  "text": "Stop, I've changed my mind!"
                                              }
                                            })
        actions.add_button('text 123 ','action_id_2')
        actions.add_button('another button')
        actions.add_button('6th button')
        actions.add_button('8th button')
        actions.add_button('9th button')
        actions.add_button('10th button')
        actions.add_button('11th button')
        actions.add_button('12th button')
        actions.render()

    def test_add_layout_actions__select(self):
        actions = self.api.add_layout_actions("action_block")
        actions.add_button('an button'  , style='primary')
        actions.add_date_picker('chose an date', 'an_date', initial_date='2019-07-01')
        actions.add_overflow(options=[('option 1', 'value 1'), ('option 2', 'value 2')])
        actions.add_select('an select 1', options=[('option 1', 'value 1'), ('option 2', 'value 2')])
        actions.add_select('an select 2', options=[('option 1', 'value 1'), ('option 2', 'value 2')], initial_option='value 2')

        actions.add_select('an select 3', option_groups = [('group_1', [('option 1', 'value 1'), ('option 2', 'value 2')]) ,
                                                           ('group_2', [('option 3', 'value 3'), ('option 4', 'value 4')])],
                                          initial_option='value 4')
        actions.add_select_external('pick one', 'an_select', min_query_length=2)
        actions.add_select_users   ('select user'   , 'an_user'        , initial_user='U7ESE1XS7')
        actions.add_select_channel ('select channel', 'an_conversation', initial_channel=self.channel)

        actions.render()

    def test_add_layout_context(self):
        context = self.api.add_layout_context("context_block")
        context.add_image('https://image.freepik.com/free-photo/red-drawing-pin_1156-445.jpg')
        context.add_image('https://image.freepik.com/free-vector/modern-check-list-illustration_79603-146.jpg')
        context.add_image('https://image.freepik.com/free-vector/flat-people-going-university_23-2148221026.jpg')
        context.add_text('an text')
        context.add_text('now with *markdown* :point_left:')
        context.add_text('now without *markdown*', 'plain_text')
        context.add_text('emoji is True  :point_right:', 'plain_text', emoji   =True )
        context.add_text('emoji is False :point_right:', 'plain_text', emoji   =False)
        context.add_text('verbatim is True: https://www.google.com'  , verbatim=True )
        context.add_text('verbatim is False: https://www.google.com' , verbatim=False)
        context.render()

    def test_add_layout_image(self):
        url = 'https://image.freepik.com/free-vector/modern-check-list-illustration_79603-146.jpg'
        image = self.api.add_layout_image("image_block", url, 'image title')
        image.render()
        #self.api.add_divider()

    def test_add_layout_section__text(self):
        section = self.api.add_layout_section()
        section.add_text('this is an section')
        section.render()

    def test_add_layout_section__fields(self):
        section = self.api.add_layout_section()
        section.add_text('*Here are a bunch of fields:*')           # this is optional
        section.add_field('field *mrkdwn*:', 'mrkdwn')
        section.add_field('field *mrkdwn*', 'plain_text')
        section.add_field('another one')
        section.add_fields(['123', '`456`','789','a','*b*','- c' ,'d'])
        section.add_button('an button')
        #section.add_date_picker('an picker', 'action_id')
        #section.add_overflow([('a','b'), ('c','d')])
        #section.add_select('an select', [('a','b'), ('c','d')])
        #section.add_select_users   ('select user', 'an_user'   , initial_user    ='U7ESE1XS7'  )
        #section.add_select_channel ('select user', 'an_channel', initial_channel =self.channel )
        #section.add_select_external('pick one'   , 'an_select' , min_query_length=2            )
        section.render()

    # add element blocks

    def test_add_attachments(self):
        self.api.set_text('an text').add_attachment({"pretext": "pre-hello", "text": "text-world"})


    def test_add_divider(self):
        self.api.add_divider()

    # def test_add_image(self):
    #     url = 'https://image.freepik.com/free-vector/modern-check-list-illustration_79603-146.jpg'
    #     self.api.add_image(url, "an image")
