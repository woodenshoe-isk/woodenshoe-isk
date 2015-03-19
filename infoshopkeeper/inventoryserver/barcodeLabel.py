#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import barcode_monkeypatch

from reportlab import rl_config
from reportlab.graphics import barcode, renderPDF
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.pdfgen import canvas

import tempfile
import subprocess
import string

import etc

isbn1='9780345497499'
booktitle='Kraken Kraken Kraken Kraken Kraken'
author='China Mieville, CHina Mieville, CHinea Miefille'
ourprice=28
num_copies=1

def print_barcode_label(isbn='', booktitle='', author='', ourprice=0, listprice=0, num_copies=1):
    import sys
    print>>sys.stderr, type(isbn), type(isbn1), type(booktitle)
    rl_config.warnOnMissingFontGlyphs = 1
    try:
        registerFont(TTFont('Courier New', 'Courier New.ttf'))
        registerFont(TTFont('Courier New Bold', 'Courier New Bold.ttf'))
        registerFont(TTFont('Courier New Italic', 'Courier New Italic.ttf'))
        registerFont(TTFont('Courier New Bold Italic', 'Courier New Bold Italic.ttf'))
        registerFontFamily('Courier New', normal='Courier New', bold='Courier New Bold', italic='Courier New Italic', boldItalic='Courier New Bold Italic')
    except TTFError:
        registerFont(TTFont('Courier New', 'Courier_New.ttf'))
        registerFont(TTFont('Courier New Bold', 'Courier_New_Bold.ttf'))
        registerFont(TTFont('Courier New Italic', 'Courier_New_Italic.ttf'))
        registerFont(TTFont('Courier New Bold Italic', 'Courier_New_Bold_Italic.ttf'))
        registerFontFamily('Courier New', normal='Courier New', bold='Courier New Bold', italic='Courier New Italic', boldItalic='Courier New Bold Italic')

    font = 'Courier New Bold'
    font_size = 9
    format_ourprice='$' + ('%3.2f' % float(unicode(ourprice).strip('$')))
    doc_width = 2.4*inch
    doc_height = 2*inch
    margin = 0.1*inch
    column_width = doc_width - 2*margin
    column_height = doc_height - 2*margin
    ourprice_width = stringWidth('$888.88', font, font_size)
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    
    #breaks string at word boundary which is less than max width in pixels
    def truncate_by_word( booktitle, max_width=0, split_char=' ' ):
        title_array = []
        for i in booktitle.split(split_char):
           title_array.append(i)
           if stringWidth(string.join(title_array, split_char), font, font_size) > max_width:
                title_array.pop()
                break
        return string.join(title_array, split_char)
    
    saleBanner=False
    if float(unicode(ourprice).strip('$')) < float(unicode(listprice).strip('$')):
        saleBanner=True
        doc_height = doc_height + font_size*1.5
        column_height = doc_height -2*margin

    canvas1 = canvas.Canvas(tmpfile, (doc_width, doc_height))
    #change coordinates so origin is now at left bottom margin corner
    canvas1.translate(margin, margin)
    canvas1.saveState()
    text_object = canvas1.beginText()
    text_object.setTextOrigin(0, column_height-margin)
    if saleBanner==True:
        text_object.setFont(font, font_size+2)
        text_object.textLine("SALE! SALE! SALE! SALE!")
    text_object.setFont(font, font_size)
    text_object.textOut( truncate_by_word(booktitle, max_width=(column_width - ourprice_width - margin)))
    text_object.moveCursor(column_width - ourprice_width, 0)
    text_object.textLine(unicode(format_ourprice))
    #move cursor permanently moves margin, so we have to move back to zero
    text_object.setXPos( -text_object.getX())
    text_object.textLine(truncate_by_word(author, max_width=column_width, split_char=','))
    canvas1.drawText(text_object)
    
    price_string='5999'
    if 0 <= float(unicode(ourprice).strip('$')) < 100:
        price_string='5' + ('%3.2f' % float(unicode(ourprice).strip('$'))).replace('.', '').zfill(4)[-4:]
        
    #create barcode and draw it at the origin.
    barcode1=barcode.createBarcodeDrawing('EAN13EXT5', value=str(isbn + price_string), validate=True, width= column_width, height=1.4*inch, humanReadable=True, fontName=font)
    renderPDF.draw(barcode1, canvas1, 0,0)
    canvas1.restoreState()
    canvas1.showPage()
    canvas1.save()

    #print_command_string = string.Template(u"export TMPDIR=$tmpdir; $gs_location -q -dSAFER -dNOPAUSE -sDEVICE=pdfwrite -sourprice='$ourourprice' -sisbnstring='$isbn' -sbooktitle='$booktitle' -sauthorstring='$authorstring' -sOutputFile=%pipe%'lpr -P $printer -# $num_copies -o media=Custom.175x144' barcode_label.ps 1>&2")
    print tmpfile.name
    tmpfile.close()
    print_command_string = string.Template(u"lpr -P $printer -# $num_copies -o media=Custom.175x145 $filename")
    #print_command_string = string.Template(u"open $filename")
    pcs_sub = print_command_string.substitute({'filename':tmpfile.name, 'printer': etc.label_printer_name, 'num_copies':num_copies})
    result=subprocess.call( ' '.join(pcs_sub.split()), shell=True)
#    tmpfile.unlink(tmpfile.name)

def test_label():
    print_barcode_label(isbn=isbn1, booktitle=booktitle, author=author, ourprice=ourprice, listprice=ourprice)
