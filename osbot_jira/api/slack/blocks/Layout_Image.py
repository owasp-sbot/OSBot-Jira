class Layout_Image:
    def __init__(self, block_id, blocks, image_url, title=None, alt_text=None):
        self.block_id  = block_id
        self.blocks    = blocks
        self.image_url = image_url
        self.title     = title
        self.alt_text  = alt_text

    def render(self):
        if self.alt_text is None: self.alt_text = self.image_url
        image = { "type"      : "image"       ,
                  "block_id"  : "image4"      ,
                  "image_url" : self.image_url,
                  "alt_text"  : self.alt_text
                }

        if self.title: image["title"]= { "type": "plain_text", "text": self.title}

        self.blocks.append(image)
        return self