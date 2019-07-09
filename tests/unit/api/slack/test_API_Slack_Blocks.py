from unittest import TestCase

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jira.api.slack.API_Slack_Blocks import API_Slack_Blocks


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
        actions = self.api.add_layout_actions("actionblock789")
        actions.add_button('first button', 'action_id_1')
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

    def test_add_layout_actions__images(self):
        actions = self.api.add_layout_actions("action_block")
        actions.add_button('an button', style='primary')
        actions.add_image()
        actions.render()



    # add element blocks

    def test_add_attachments(self):
        self.api.set_text('an text').add_attachment({"pretext": "pre-hello", "text": "text-world"})


    def test_add_button(self):
        self.api.add_button("Click Me", value='click_me_123', action_id="button")

    def test_add_divider(self):
        self.api.add_divider()

    def test_add_image(self):
        self.api.add_image("http://placekitten.com/700/500", "Multiple cute kittens")
