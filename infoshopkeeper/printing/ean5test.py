from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
#I"ll be generating code39 barcodes, others are available
from reportlab.graphics import barcode, renderPDF

import tempfile
import subprocess
import string

from config.config import configuration

tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')

# generate a canvas (A4 in this case, size doesn"t really matter)
canvas1=canvas.Canvas(tmpfile, (2.4*inch, 2*inch))
canvas1.saveState()

# create a barcode object
# (is not displayed yet)
# barHeight encodes how high the bars will be
# barWidth encodes how wide the "narrowest" barcode unit is
ean5 = '51234'
barcode1=barcode.createBarcodeDrawing('EAN5', value=str(ean5), validate=True, width= 2.4*inch, height=1.4*inch, humanReadable=True, fontName='Helvetica')
renderPDF.draw(barcode1, canvas1, 0, 0)
canvas1.restoreState()
canvas1.showPage()
canvas1.save()
tmpfile.close()
print_command_string = string.Template("lpr -P $printer -# $num_copies -o media=Custom.175x120 $filename")
pcs_sub = print_command_string.substitute({'filename':'/tmp/ean13ext.jpg', 'printer': configuration.get('label_printer_name'), 'num_copies':1})
result=subprocess.call( ' '.join(pcs_sub.split()), shell=True)
tmpfile.unlink(tmpfile.name)

