import pdfkit

def html2pdf_file(src,dst):
    pdfkit.from_file(src, dst)

def html2pdf_url(url,dst):
    pdfkit.from_url(url, dst)

def html2pdf_string(str,dst):
    pdfkit.from_file(str,dst)