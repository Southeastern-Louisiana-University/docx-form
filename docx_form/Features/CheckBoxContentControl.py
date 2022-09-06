from docx_form.Features.DocxContentControl import DocxContentControl

class CheckBoxContentControl(DocxContentControl):
    def __init__(self, id, type, text, checked, checkedState, uncheckedState):
        super().__init__(id, type, text)
        self.id = id
        self.checked = checked
        self.checkedState = checkedState
        self.uncheckedState = uncheckedState