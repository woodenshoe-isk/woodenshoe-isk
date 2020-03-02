from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch

# I"ll be generating code39 barcodes, others are available
from reportlab.graphics import barcode, renderPDF

import tempfile


def test_ean13():
    # generate a canvas (A4 in this case, size doesn"t really matter)
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    # generate a canvas (A4 in this case, size doesn"t really matter)
    canvas1 = canvas.Canvas(tmpfile, (2.4 * inch, 2 * inch))
    canvas1.saveState()
    canvas1.saveState()

    # create a barcode object
    # (is not displayed yet)
    # barHeight encodes how high the bars will be
    # barWidth encodes how wide the "narrowest" barcode unit is
    ean13 = "9781583228708"
    barcode1 = barcode.createBarcodeDrawing(
        "EAN13",
        value=str(ean13),
        validate=True,
        width=2.4 * inch,
        height=1.4 * inch,
        humanReadable=True,
        fontName="Helvetica",
    )
    renderPDF.draw(barcode1, canvas1, 0, 0)
    canvas1.restoreState()
    canvas1.showPage()
    canvas1.save()
