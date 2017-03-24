import reportlab
import printing

from reportlab.graphics import barcode
from reportlab.graphics.barcode import eanbc, widgets
from reportlab.graphics.shapes import Group, String, Rect
from reportlab.graphics.widgetbase import Widget
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.validators import isNumber, isColor, isString, Validator, isBoolean
from reportlab.lib.attrmap import *
from reportlab.graphics.charts.areas import PlotArea
from reportlab.lib.units import mm, inch


class Ean13Ext5BarcodeWidget(PlotArea):
    codeName = "EAN13EXT5"

    _attrMap = AttrMap(BASE=PlotArea,
                       value = AttrMapValue(eanbc.nDigits(18), desc='the number'),
                       fontName = AttrMapValue(isString, desc='fontName'),
                       fontSize = AttrMapValue(isNumber, desc='font size'),
                       x = AttrMapValue(isNumber, desc='x-coord'),
                       y = AttrMapValue(isNumber, desc='y-coord'),
                       barFillColor = AttrMapValue(isColor, desc='bar color'),
                       barHeight = AttrMapValue(isNumber, desc='Height of bars.'),
                       barWidth = AttrMapValue(isNumber, desc='Width of bars.'),
                       barStrokeWidth = AttrMapValue(isNumber, desc='Width of bar borders.'),
                       barStrokeColor = AttrMapValue(isColor, desc='Color of bar borders.'),
                       textColor = AttrMapValue(isColor, desc='human readable text color'),
                       humanReadable = AttrMapValue(isBoolean, desc='if human readable'),
                       quiet = AttrMapValue(isBoolean, desc='if quiet zone to be used'),
                       lquiet = AttrMapValue(isBoolean, desc='left quiet zone length'),
                       rquiet = AttrMapValue(isBoolean, desc='right quiet zone length'),
                       shouldValidate = AttrMapValue(isBoolean, desc='validate or not'),
                       barcode13 = AttrMapValue(isAnything, desc='isbn barcode'),
                       barcode5 = AttrMapValue(isAnything, desc='ean5 barcode')
                       )

    _digits=18
    quiet = 1
    rquiet = lquiet = None
    fontSize = 8        #millimeters
    fontName = 'Helvetica'
    textColor = barFillColor = colors.black
    barStrokeColor = None
    barStrokeWidth = 0
    x = 0
    y = 0

    def __init__(self, value='123456789012345678', **kw):
        for k, v in list(kw.items()):
            setattr(self, k, v)
        ean13 = value[0:12]
        
        self.barcode13=barcode.createBarcodeDrawing('EAN13', value=str(ean13), validate=True, width= 1.44*inch, height=1.4*inch, humanReadable=self.humanReadable, fontName=self.fontName)
        ean5 = value[13:18]
        self.barcode5 = barcode.createBarcodeDrawing('EAN5', value=str(ean5), validate=True, width= 0.72*inch, height=1.4*inch, barHeight = self.barcode13.height*0.66, humanReadable=self.humanReadable, fontName=self.fontName)
        self.barcode5.contents[0].barHeight = self.barcode13.contents[0].barHeight - self.fontSize
        self.barcode5.translate(2.8*inch, 0)
 
    def draw(self):
        """Just return a group"""
        return Group(self.barcode13, self.barcode5)

def getCodes():
    """Returns a dict mapping code names to widgets"""
    
    from reportlab.graphics.barcode.widgets import BarcodeI2of5, BarcodeCode128, BarcodeStandard93,\
        BarcodeExtended93, BarcodeStandard39, BarcodeExtended39,\
        BarcodeMSI, BarcodeCodabar, BarcodeCode11, BarcodeFIM,\
        BarcodePOSTNET, BarcodeUSPS_4State
    
    #newer codes will typically get their own module
    from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget, Ean8BarcodeWidget, Ean5BarcodeWidget, UPCA
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

reportlab.graphics.barcode.getCodes = getCodes
barcode.eanbc.Ean13Ext5BarcodeWidget = Ean13Ext5BarcodeWidget

