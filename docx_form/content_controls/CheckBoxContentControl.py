# Local Imports
from .DocxContentControl import DocxContentControl

# Package Imports
from zipfile import ZipFile
from lxml import etree

try:
    from type_aliases import Element
    from constants import XML_PREFIX
    from constants import XML_CHECK
except ImportError:
    from ..type_aliases import Element
    from ..constants import XML_PREFIX, XML_CHECK
class CheckBoxContentControl(DocxContentControl):
    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)

    def setCheckBox(self, boolean: bool):
# Replace .docx with -modified.docx in the file path
        new_path = self.file_path.replace(".docx", "-modified.docx")
        if boolean == True:
            checkBoxVal = '1'
            box = '☒'
        else:
            checkBoxVal = '0'
            box = '☐'
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
            found = False
            element: Element
            for element in body.getiterator():
                if(element.tag == f"{XML_PREFIX}t"):
                    if(found == True):
                        found = False
                        element.text = box
                        new_doc.writestr("word/document.xml", etree.tostring(root))
                elif(element.tag == f"{XML_PREFIX}id"):
                    if(element.attrib[f"{XML_PREFIX}val"] == self.id):
                        found = True
                        if(element != None):
                            while element.tag != f"{XML_CHECK}checked":
                                element = element.getnext()
                                if(element == None):
                                    break
                                elif(element != None):
                                    print(element.tag)
                                    checkBoxChildren: list[
                                        Element
                                    ] = element.getchildren()
                                    for ele in checkBoxChildren:
                                        print(ele.tag)
                                        if(ele.tag == f"{XML_CHECK}checked"):
                                            print(ele.attrib)
                                            ele.attrib[f"{XML_CHECK}val"] = checkBoxVal
                                            newCheckBox : Element = etree.Element(f"{XML_CHECK}checked", ele.attrib) 
                                            ele.addnext(newCheckBox)
                                            ele.getparent().remove(ele)



                        