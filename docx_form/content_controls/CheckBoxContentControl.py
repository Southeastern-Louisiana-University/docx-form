# Local Imports
from calendar import c
from .DocxContentControl import DocxContentControl

# Package Imports
from zipfile import ZipFile
from lxml import etree

try:
    from type_aliases import Element
    from constants import XML_PREFIX
    from constants import XML_CHECK
    from globals import Raw_XML
except ImportError:
    from ..type_aliases import Element
    from ..constants import XML_PREFIX, XML_CHECK
    from ..globals import Raw_XML
class CheckBoxContentControl(DocxContentControl):
    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)

    def setCheckBox(self, boolean: bool):
# Replace .docx with -modified.docx in the file path
        new_path = self.file_path.replace(".docx", "-modified.docx")
        # Set values according to the boolean passed in
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

            foundIdTag = False
            element: Element
            for element in body.iter():               
                if(element.tag == f"{XML_PREFIX}id"):
                    # Find the check box content control with the same id as self
                    if(element.attrib[f"{XML_PREFIX}val"] == self.id):
                        foundIdTag = True
                        while element.tag != f"{XML_CHECK}checked":
                            element = element.getnext()
                            if(element == None):
                                break
                            elif(element != None):
                                checkBoxChildren: list[
                                    Element
                                ] = element.getchildren()
                                for checkBoxChild in checkBoxChildren:
                                    if(checkBoxChild.tag == f"{XML_CHECK}checked"):
                                        # Set attribute value, add new checked tag and remove old checked tag
                                        checkBoxChild.attrib[f"{XML_CHECK}val"] = checkBoxVal
                                        newCheckBox : Element = etree.Element(f"{XML_CHECK}checked", checkBoxChild.attrib) 
                                        checkBoxChild.addnext(newCheckBox)
                                        checkBoxChild.getparent().remove(checkBoxChild)
                # Set the value of the text box to the correct check box
                elif(foundIdTag == True):
                    if(element.tag == f"{XML_PREFIX}t"):
                        element.text = box
                        Raw_XML.raw_xml = etree.tostring(root)
                        return



                        
