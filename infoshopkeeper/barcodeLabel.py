from reportlab import platypus
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import barcode, renderPDF
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

isbn='9780345497499'
booktitle='Kraken Kraken Kraken Kraken Kraken'
author='China Mieville, CHina Mieville, CHinea Miefille'
price=28

def print_barcode_label(isbn='', booktitle='', author='', price=0):
    font = 'Courier'
    font_size = 9
    format_price='$' + ('%3.2f' % float(unicode(price).strip('$')))
    doc_width = 2.4*inch
    doc_height = 2*inch
    margin = 0.1*inch
    column_width = doc_width - 2*margin
    column_height = doc_height - 2*margin
    price_width = stringWidth('$888.88', font, font_size)
    
    #breaks string at word boundary which is less than max width in pixels
    def truncate_by_word( booktitle, max_width=0, split_char=' ' ):
        title_array = []
        for i in booktitle.split(split_char):
           title_array.append(i)
           if stringWidth(string.join(title_array, split_char), font, font_size) > max_width:
                title_array.pop()
                break
        return string.join(title_array, split_char)
    
    canvas1 = canvas.Canvas('/tmp/test.pdf', (doc_width, doc_height))
    #change coordinates so origin is now at left bottom margin corner
    canvas1.translate(margin, margin)
    canvas1.saveState()
    text_object = canvas1.beginText()
    text_object.setFont(font, font_size)
    text_object.setTextOrigin(0, column_height-margin)
    text_object.textOut( truncate_by_word(booktitle, max_width=(column_width - price_width - margin)))
    text_object.moveCursor(column_width - price_width, 0)
    text_object.textLine(unicode(format_price))
    #move cursor permanently moves margin, so we have to move back to zero
    text_object.setXPos( -text_object.getX())
    text_object.textLine(truncate_by_word(author, max_width=column_width, split_char=','))
    canvas1.drawText(text_object)
    #create barcode and draw it at the origin.
    barcode1=barcode.createBarcodeDrawing('EAN13', value=isbn, validate=True, width= column_width, height=1.4*inch, humanReadable=True)
    renderPDF.draw(barcode1, canvas1, 0,0)
    canvas1.restoreState()
    canvas1.showPage()
    canvas1.save()
    
print_barcode_label(isbn=isbn, booktitle=booktitle, author=author, price=price)
