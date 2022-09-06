from docx_form.Features.DocxContentControl import DocxContentControl


class RichTextContentControl(DocxContentControl):
    def __init__(self, id, type, text):
        super().__init__(id, type, text)