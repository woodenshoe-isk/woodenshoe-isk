from reportlab.graphics import barcode
from reportlab.graphics.barcode import eanbc, widgets
from printing import eanbc as eanbc1

def getCodes():
    """Returns a dict mapping code names to widgets"""
    
    from reportlab.graphics.barcode.widgets import BarcodeI2of5, BarcodeCode128, BarcodeStandard93,\
        BarcodeExtended93, BarcodeStandard39, BarcodeExtended39,\
        BarcodeMSI, BarcodeCodabar, BarcodeCode11, BarcodeFIM,\
        BarcodePOSTNET, BarcodeUSPS_4State
    
    #newer codes will typically get their own module
    from eanbc import Ean13BarcodeWidget, Ean13Ext5BarcodeWidget, Ean8BarcodeWidget, Ean5BarcodeWidget, UPCA
    from reportlab.graphics.barcode.qr import QrCodeWidget
        
    #the module exports a dictionary of names to widgets, to make it easy for
    #apps and doc tools to display information about them.
    codes = {}
    for widget in (
                   BarcodeI2of5,
                   BarcodeCode128,
                   BarcodeStandard93,
                   BarcodeExtended93,
                   BarcodeStandard39,
                   BarcodeExtended39,
                   BarcodeMSI,
                   BarcodeCodabar,
                   BarcodeCode11,
                   BarcodeFIM,
                   BarcodePOSTNET,
                   BarcodeUSPS_4State,
                   Ean13BarcodeWidget,
                   Ean13Ext5BarcodeWidget,
                   Ean8BarcodeWidget,
                   Ean5BarcodeWidget,
                   UPCA,
                   QrCodeWidget,
                   ):
        codeName = widget.codeName
        codes[codeName] = widget
    
    return codes

barcode.getCodes = getCodes
barcode.eanbc = eanbc1

