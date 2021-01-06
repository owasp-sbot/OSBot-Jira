from osbot_utils.utils import Misc

class Layout_Context:
    def __init__(self, blocks, block_id):
        self.block_id = block_id
        self.blocks   = blocks
        self.elements = []
        if block_id is None:
            self.block_id = Misc.random_string_and_numbers(4, 'block_')


    def add_image(self, image_url, alt_text=None):
        if alt_text is None: alt_text = image_url

        element = { "type"      : "image",
                    "image_url" : image_url ,
                    "alt_text"  : alt_text  }
        self.elements.append(element)
        return self

    def add_text(self, text, text_type='mrkdwn', emoji=None, verbatim=None):
        element = {"text": text , "type": text_type }

        if emoji    is not None: element['emoji'   ] = emoji
        if verbatim is not None: element['verbatim'] = verbatim

        self.elements.append(element)
        return self

    def add_texts(self, texts):
        for text in texts:
            self.add_text(text)
        return self

    def render(self):
        self.blocks.append({"type": "context",
                            "block_id": self.block_id,
                            "elements": self.elements})
        return self