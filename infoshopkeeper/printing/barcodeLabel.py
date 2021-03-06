#!/usr/bin/env python

-*- coding: future_fstrings -*-
# -*- coding: UTF-8 -*-

from printing import barcode_monkeypatch

from reportlab import rl_config
from reportlab.graphics import barcode, renderPDF
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont, TTFError
from reportlab.pdfgen import canvas

import treepoem
import plotly.express as px
import plotly.graph_objects as go

import tempfile
import subprocess
import string

from config.config import configuration

isbn1='9780345497499'
booktitle='Kraken Kraken Kraken Kraken Kraken'
author='China Mieville, CHina Mieville, CHinea Miefille'
ourprice=28
num_copies=1

def print_barcode_label(isbn='', booktitle='', author='', ourprice=0, listprice=0, num_copies=1):
    #make sure it's a float
    if type(ourprice) != float:
        if type(ourprice) == str:
            ourprice.strip('$')
        ourprice = float(ourprice)
    if type(listprice) != float:
        if type(listprice) == str:
            listprice.strip('$')
        listprice = float(listprice)

    #we need a string of format '9780804732185 52295'
    #in other words, isbn plus currency code (5 for USD) plus price
    #ean5 only allows for prices up to 99.99.
    #the convention in the protocol is to make the barcode price 99.99
    if ourprice > 100:
        ourprice1 = 99.99
    else:
        ourprice1 = ourprice
    barcode_price_string = f'{ourprice1:05.2f}'.replace('.', '')
    barcode_string = isbn + ' 5' + barcode_price_string
    print(barcode_string)
    ean13 = treepoem.generate_barcode('ean13', barcode_string,
                                      {'includetext':True, 'guardwhitespace':True,'height':1.75})
    #convert to bitmap.
    ean13 = ean13.convert('1')
    font = "Monaco, monospaced"

    #add ean13+5 to canvas
    fig = px.imshow(ean13,color_continuous_scale='gray')
    fig.update_layout(coloraxis_showscale=False)

    #we are using annotations for the title, author, etc info
    annotations=[
        go.layout.Annotation(
            x= 0,
            y= 1.18,
            showarrow=False,
            text=author,
            name= 'author',
            xref="paper",
            yref="paper"
        ),
        go.layout.Annotation(
            x=1,
            y=1.18,
            showarrow=False,
            text= f'${ourprice:.2f}',
            name='price',
            xref="paper",
            yref="paper"
        ),
        go.layout.Annotation(
            x=0,
            y=1.28,
            showarrow=False,
            text= booktitle,
            name= 'title',
            xref="paper",
            yref="paper"
        )
    ]

    #only show sale banner if it's a sale book
    if ourprice < listprice:
        annotations.append(
            go.layout.Annotation(
                x=0,
                y=1.40,
                showarrow=False,
                text= '<b> Sale!! Sale!! Sale!! Sale!!  <b>',
                name = 'sale',
                font=dict(
                    color="white"
                ),
                bgcolor = 'black',
                xref="paper",
                yref="paper"
            )
        )

    fig.update_layout(
        annotations = annotations
    )

    fig.update_layout(
        autosize = True,
        font=dict(
            family=font,
            size=16,
            color="black"
        ),
        #don't show grid (image is effectively a graph)
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        #small margin l, r. top margin is space for title, etc.
        margin=dict(l=2, r=2, t=75, b=0),
        paper_bgcolor="white"
    )

    #assume 0.18 width to height.
    #72 points per inch btw
    #this is completely empirical-- replace with font metrics
    char_width = 0.35 * 16
    for ann in fig.layout.annotations:
        #correct for potential overflow
        if ann.name == 'title':

            num_char_allowed = (2.4 * 72) // char_width
            booktitle1 = booktitle[:int(num_char_allowed)]
            booktitle1 = booktitle1[:booktitle1.rfind(' ')]
            ann.text = booktitle1
        if ann.name == 'author':
            num_char_allowed = (2.4 * 72) // char_width
            #leave room for for price
            num_char_allowed = num_char_allowed - 8
            author1 = author[:int(num_char_allowed)]
            author1 = author1[:author1.rfind(',')]
            ann.text = author1
    fig.show(renderer='png', width=300, height=250)
    label_img = fig.to_image(format='png', width=300, height=250)

    print_string = f"lpr -P {configuration.get('label_printer_name')} -#  {num_copies} -o fit-to-page=ON  -o orientation-requested=3 -o media=Custom.62x62mm"
    print(print_string)
    with subprocess.Popen(print_string.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1, shell=True) as process:
        pass
        #out, err = process.communicate(input=label_img)
    os.unlink('/User/mkapes/fig1.png')
    fig.write_image('/User/mkapes/fig1.png')
    return fig, ean13


def print_barcode_label_old(isbn='', booktitle='', author='', ourprice=0, listprice=0, num_copies=1):
    import sys
    print(type(isbn), type(isbn1), type(booktitle), file=sys.stderr)
    print(isbn, booktitle, author, ourprice, listprice, num_copies, file=sys.stderr)
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
    format_ourprice='$' + ('%3.2f' % float(str(ourprice).strip('$')))
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
           if stringWidth(split_char.join(title_array), font, font_size) > max_width:
                title_array.pop()
                break
        return split_char.join(title_array)

    saleBanner=False
    if float(str(ourprice).strip('$')) < float(str(listprice).strip('$')):
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
    text_object.textLine(str(format_ourprice))
    #move cursor permanently moves margin, so we have to move back to zero
    text_object.setXPos( -text_object.getX())
    text_object.textLine(truncate_by_word(author, max_width=column_width, split_char=','))
    canvas1.drawText(text_object)

    price_string='59999'
    if 0 <= float(str(ourprice).strip('$')) < 100:
        price_string='5' + ('%3.2f' % float(str(ourprice).strip('$'))).replace('.', '').zfill(4)[-4:]

    #create barcode and draw it at the origin.
    barcode1=barcode.createBarcodeDrawing('EAN13EXT5', value=str(isbn + price_string), validate=True, width= column_width, height=1.4*inch, humanReadable=True, fontName=font)
    renderPDF.draw(barcode1, canvas1, 0, 0)
    canvas1.restoreState()
    canvas1.showPage()
    canvas1.save()

    #print_command_string = string.Template(u"export TMPDIR=$tmpdir; $gs_location -q -dSAFER -dNOPAUSE -sDEVICE=pdfwrite -sourprice='$ourourprice' -sisbnstring='$isbn' -sbooktitle='$booktitle' -sauthorstring='$authorstring' -sOutputFile=%pipe%'lpr -P $printer -# $num_copies -o media=Custom.175x144' barcode_label.ps 1>&2")
    print(tmpfile.name)
    tmpfile.close()
    print_command_string = string.Template("lpr -P $printer -# $num_copies -o orientation-requested=3 -o media=60x60 $filename")
    #print_command_string = string.Template(u"open $filename")
    pcs_sub = print_command_string.substitute({'filename':tmpfile.name, 'printer': configuration.get('label_printer_name'), 'num_copies':num_copies})
    result=subprocess.call( ' '.join(pcs_sub.split()), shell=True)
    print(pcs_sub, file=sys.stderr)
#    tmpfile.unlink(tmpfile.name)

def test_label():
    print_barcode_label(isbn=isbn1, booktitle=booktitle, author=author, ourprice=ourprice, listprice=ourprice)
