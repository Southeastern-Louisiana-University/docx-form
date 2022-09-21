# Package Imports
from zipfile import ZipFile
from lxml import etree

# Local Imports
from .DocxContentControl import DocxContentControl

try:
    from type_aliases import Element
    from constants import XML_PREFIX
except ImportError:
    from ..type_aliases import Element
    from ..constants import XML_PREFIX


class PlainTextContentControl(DocxContentControl):
    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)

    def set_text(self, new_text: str):
        # Replace .docx with -modified.docx in the file path
        new_path = self.file_path.replace(".docx", "-modified.docx")

        # Open the current docx file and create a new one
        with ZipFile(self.file_path, "a") as old_doc, ZipFile(new_path, "w") as new_doc:
            # Copy all contents ecxept the "word/document.xml" file from the old docx to the new docx
            doc_list = old_doc.infolist()
            for item in doc_list:
                if item.filename != "word/document.xml":
                    new_doc.writestr(item, old_doc.read(item.filename))

            # The root of the document
            root: Element = etree.XML(old_doc.read("word/document.xml"))
            # The body of the document
            body: Element = root.getchildren()[0]

            # Find the plain text content control with the same id as self
            element: Element
            for element in body.getchildren():
                if element.tag == f"{XML_PREFIX}sdt":
                    child_tags: list[Element] = element.getchildren()
                    is_correct_tag = False
                    for grandchild_tag in child_tags:
                        if grandchild_tag.tag == f"{XML_PREFIX}sdtPr":
                            grandchild_tags: list[
                                Element
                            ] = grandchild_tag.getchildren()
                            for grandgrandchild_tag in grandchild_tags:
                                if grandgrandchild_tag.tag == f"{XML_PREFIX}id":
                                    if (
                                        grandgrandchild_tag.attrib[f"{XML_PREFIX}val"]
                                        == self.id
                                    ):
                                        is_correct_tag = True
                                        break
                        elif (
                            grandchild_tag.tag == f"{XML_PREFIX}sdtContent"
                            and is_correct_tag
                        ):
                            w_p_tag: Element = grandchild_tag.getchildren()[0]
                            w_p_tag_attributes = w_p_tag.attrib

                            # Make a new <w:p> tag with the same attributes as the old one
                            new_w_p_tag: Element = etree.Element(
                                f"{XML_PREFIX}p", w_p_tag_attributes
                            )

                            # Append a <w:r> tag with a <w:t> tag inside it
                            new_w_r_tag: Element = etree.Element(f"{XML_PREFIX}r")
                            new_w_t_tag: Element = etree.Element(f"{XML_PREFIX}t")
                            new_w_t_tag.text = new_text
                            new_w_r_tag.append(new_w_t_tag)
                            new_w_p_tag.append(new_w_r_tag)

                            # Replace the old <w:p> tag with the new one
                            grandchild_tag.replace(w_p_tag, new_w_p_tag)

                            # Insert the new document
                            new_doc.writestr("word/document.xml", etree.tostring(root))


                    test = CheckBoxContentControl(parent_tag.getchildren()[0])
                    return test.setCheckBox(True)
                    # return CheckBoxContentControl(parent_tag.getchildren()[0])

