from unittest import TestCase

from gs_elk.Graph_Commands.Commands_Helper import Commands_Helper
from gs_elk.Graph_Commands.Nodes           import Nodes


class Test_Commands_Helper(TestCase):

    def setUp(self):
        self.commands_helper = Commands_Helper(Nodes)
        self.channel         = 'DDKUZTK6X'

    def test__init__(self):
        assert self.commands_helper.target == Nodes

    def test_available_methods(self):
        methods = self.commands_helper.available_methods()
        assert 'add' in methods

    def test_help(self):
        (text, attachments) = self.commands_helper.help()
        assert text == '*Here are the `Nodes` commands available:*'

    def test_invoke__no_command(self):
        self.commands_helper.invoke(self.channel, [])

    def test_invoke__bad_command(self):
        self.commands_helper.invoke(self.channel, "AAAA".split(' '))

    def test_invoke__not_enough_commands(self):
        self.commands_helper.invoke(self.channel, "add Graph_000 ".split(' '))

    def test_invoke__graph_add(self):
        self.commands_helper.invoke(self.channel, "add graph_WLA id_1 label".split(' '))

