from docx_form.Features.DocxContentControl import DocxContentControl

class DatePickerContentControl(DocxContentControl):
    def __init__(self, id, type, text, dateFormat, languageId, storeMappedDateAs, calander):
        super().__init__(id, type, text)
        self.id = id
        self.dateFormat = dateFormat
        self.languageId = languageId
        self.storeMappedDateAs = storeMappedDateAs

