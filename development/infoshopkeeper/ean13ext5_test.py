from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
#I"ll be generating code39 barcodes, others are available
from reportlab.graphics import barcode, renderPDF

import tempfile
import subprocess
import string

import etc

tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')

# generate a canvas (A4 in this case, size doesn"t really matter)
canvas1=canvas.Canvas(tmpfile,(2.4*inch, 2*inch))
canvas1.saveState()


# create a barcode object
# (is not displayed yet)
# barHeight encodes how high the bars will be
# barWidth encodes how wide the "narrowest" barcode unit is
ean13ext5 = '978158322870851234'
barcode1=barcode.createBarcodeDrawing('EAN13EXT5', value=str(ean13ext5), validate=True, width= 2.4*inch, height=1.4*inch, humanReadable=True, fontName='Helvetica')
renderPDF.draw(barcode1, canvas1, 0,0)
canvas1.restoreState()
canvas1.showPage()
canvas1.save()
tmpfile.close()
print_command_string = string.Template(u"lpr -P $printer -# $num_copies -o media=Custom.175x120 $filename")
pcs_sub = print_command_string.substitute({'filename':tmpfile.name, 'printer': etc.label_printer_name, 'num_copies':1})
result=subprocess.call( ' '.join(pcs_sub.split()), shell=True)
tmpfile.unlink(tmpfile.name)

