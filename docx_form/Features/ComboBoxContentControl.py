from docx_form.Features.DocxContentControl import DocxContentControl

class ComboBoxContentControl(DocxContentControl):
    def __init__(self, id, type, text, listItem):
        super().__init__(id, type, text)
        self.id = id
        self.listItem = listItem