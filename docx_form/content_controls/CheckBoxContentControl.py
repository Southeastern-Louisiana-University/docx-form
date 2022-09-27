# Local Imports
from .DocxContentControl import DocxContentControl

# Package Imports
from lxml import etree

try:
    from type_aliases import Element
    from constants import XML_PREFIX, XML_CHECK
    from globals import Raw_XML
except ImportError:
    from ..type_aliases import Element
    from ..constants import XML_PREFIX, XML_CHECK
    from ..globals import Raw_XML
class CheckBoxContentControl(DocxContentControl):
    """
    This class contains the properties and functions associated with the Check Box content control.

    :param DocxContentControl: This class extends DocxContentControl
    """

    def __init__(self, root: Element, file_path: str):
        super().__init__(root, file_path)
        self.type = "CheckBox Content Control"

    def set_checkBox(self, check_value: bool):
        """
        This method sets a checkbox to checked or unchecked on a CheckBox Content Control 

        :param bool check_value: Sets checkbox to checked for true and unchecked for false
        """
        # Set values according to the boolean passed in
        if check_value == True:
            checkBoxVal = '1'
            box = '☒'
        else:
            checkBoxVal = '0'
            box = '☐'

        # The root of the document
        root: Element = etree.XML(Raw_XML.raw_xml)
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



                        
