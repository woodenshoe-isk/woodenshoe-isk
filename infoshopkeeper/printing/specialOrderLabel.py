#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from reportlab import platypus
from reportlab import rl_config
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import barcode, renderPDF
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.pdfgen import canvas
from time import strftime

from config import etc

import os
import string
import subprocess
import tempfile

isbn='9780345497499'
booktitle='Kraken'
author='China Mieville'
price=28

customer_name = 'Markos Kapes'
customer_phone = '222 222 2222'
customer_email = 'test@gmail.com'

def print_special_order_label(isbn='', booktitle='', author='', price=0, customer_name='', customer_phone='', customer_email='', copies=1):
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
    format_price='$' + ('%3.2f' % float(unicode(price).strip('$')))
    doc_width = 2.4*inch
    doc_height = 4*inch
    margin = 0.1*inch
    column_width = doc_width - 2*margin
    column_height = doc_height - 2*margin
    second_field_margin = 0
    price_width = stringWidth('$888.88', font, font_size)
    debug = True
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    #breaks string at word boundary which is less than max width in pixels
    def truncate_by_word( booktitle, max_width=0, split_char=' ' ):
        title_array = []
        for i in booktitle.split(split_char):
           title_array.append(i)
           if stringWidth(string.join(title_array, split_char), font, font_size) > max_width:
                title_array.pop()
                break
        return string.join(title_array, split_char)
    
    canvas1 = canvas.Canvas(tmpfile, (doc_width, doc_height))
    #change coordinates so origin is now at left bottom margin corner
    canvas1.translate(margin, margin)
    #create barcode and draw it at the origin.
    price_string='5999'
    if 0 <= float(unicode(price).strip('$')) < 100:
        price_string='5' + ('%3.2f' % float(unicode(price).strip('$'))).replace('.', '').zfill(4)[-4:]
    barcode1=barcode.createBarcodeDrawing('EAN13', value=str(isbn + price_string), validate=True, width= column_width, height=1.4*inch, humanReadable=True, fontName=font)
    renderPDF.draw(barcode1, canvas1, 0,0)
    
    text_object = canvas1.beginText()
    text_object.setFont(font, font_size)
    text_object.setTextOrigin(0, column_height-margin)
    text_object.textOut( truncate_by_word(booktitle, max_width=(column_width - price_width - margin)))
    text_object.moveCursor(column_width - price_width, 0)
    text_object.textLine(unicode(format_price))
    #move cursor permanently moves margin, so we have to move back to zero
    text_object.setXPos( -text_object.getX())
    text_object.textLine(truncate_by_word(author, max_width=column_width, split_char=','))
    text_object.textLine('')
    text_object.textLine('On hold since %s for:' % strftime('%m/%d/%Y'))
    text_object.textLine(customer_name)
    if customer_phone:
        text_object.textOut('Phone:')
        text_object.moveCursor(45, 0)
        text_object.textLine(customer_phone)
    if customer_email:
        #move cursor permanently moves margin, so we have to move back to zero
        text_object.setXPos( -text_object.getX())
        text_object.textOut('E-mail:')
        text_object.moveCursor(45, 0)
        text_object.textLine(customer_email)
    text_object.setXPos(-text_object.getX())
    text_object.textLine('')
    for i in (u'First', u'Second', u'Third'):
            text_object.textLine(u'□ %s call on ___ by ___' % i)
    text_object.textLine('')
    text_object.textLine('Notes:')
    canvas1.drawText(text_object)
    canvas1.showPage()
    canvas1.save()
    
    #print_command_string = string.Template(u"export TMPDIR=$tmpdir; $gs_location -q -dSAFER -dNOPAUSE -sDEVICE=pdfwrite -sprice='$ourprice' -sisbnstring='$isbn' -sbooktitle='$booktitle' -sauthorstring='$authorstring' -sOutputFile=%pipe%'lpr -P $printer -# $num_copies -o media=Custom.175x120' barcode_label.ps 1>&2")
    tmpfile.close()
    print_command_string = string.Template(u"lpr -P $printer -# $numcopies -o orientation-requested=3 -o media=BrL063E078A5766 $filename")
    pcs_sub = print_command_string.substitute({'filename':tmpfile.name, 'printer':etc.label_printer_name, 'numcopies':copies})
    subprocess.check_call( pcs_sub.encode('utf8'), shell=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    #tmpfile.unlink(tmpfile.name)

#print_special_order_label(isbn=isbn, booktitle=booktitle, author=author, price=price, customer_name=customer_name, customer_phone=customer_phone, customer_email=customer_email)

def test_label():
    print_special_order_label(isbn=isbn, booktitle=booktitle, author=author, price=price, customer_name=customer_name, customer_phone=customer_phone, customer_email=customer_email, copies=1)
