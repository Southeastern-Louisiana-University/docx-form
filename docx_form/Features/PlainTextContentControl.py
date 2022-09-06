from docx_form.Features.DocxContentControl import DocxContentControl


class PlainTextContentControl(DocxContentControl):
    def __init__(self, id, type, text):
        super().__init__(id, type, text)
        self.id = id