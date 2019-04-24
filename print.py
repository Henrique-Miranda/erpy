import time
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# Company info
logo = "IMG/logoblack.png"
company = 'HL INFORMÁTICA'
slogan = 'Assistência Técnica'
compAdress = 'Rua Manuel Gonçalves do Monte, Nº39, Rio do Ouro, São Gonçalo - RJ'
compTel = '(21) 2617-4353 / (21) 98584-5457'
compEmail = 'contato@hlinformatica.com'
compSite = 'www.hlinformatica.com'
# END Company info

# OS info
osNumber = 'OS_DIR/00001.pdf'
cliName = 'Henrique Miranda'
entryDate = '23/04/2019 22:14'
adress = 'Rio do Ouro, São Gonçalo, RJ'
adress2 = 'Casa 2'
tel = '(21) 2617-4353 / (21) 98584-5457'
device = 'Notebook'
brand = 'DELL'
model = 'Inspiron 1540'
color = 'Preto'
acessories = 'Fonte e capa'
deviceStatus = 'Teclado sem tecla "M"'
defect = 'Sistema não liga.'
obs = 'Após uma queda de energia, sistema parou de iniciar'
printDate = time.strftime("%d/%m/%Y %H:%M:%S")
warrantyTerms = [
'Ao deixar seu equipamento retire todos acessórios como chip e cartão de memória, não nos responsabilizamos por estes itens.',
'Os aparelhos não retirados no prazo máximo de 3 meses(90 dias contados a partir da data em que for orçado), será cobrado uma taxa de R$10,00 por dia para cobrir custos de despesas e armazenamento.',
'O aparelho só será devolvido para o titular deste documento, caso necessário o titular poderá solicitar retirada por terceiros.']
# END OS info

doc = SimpleDocTemplate(osNumber ,pagesize=A4, rightMargin=72,leftMargin=72, topMargin=30,bottomMargin=18)
Story=[]
# LOGO
im = Image(logo, 30*mm, 30*mm, hAlign='CENTER')
Story.append(im)
Story.append(Spacer(1, 12))
# END LOGO

# HEAD
style=getSampleStyleSheet()
style.add(ParagraphStyle(name='center', fontSize=12, alignment=TA_CENTER))
ptext = f"<b>{company}</b>"
Story.append(Paragraph(ptext, style["center"]))
ptext = f"{slogan}"
Story.append(Paragraph(ptext, style["center"]))
ptext = f"{compTel}"
Story.append(Paragraph(ptext, style["center"]))
ptext = f"{compEmail}"
Story.append(Paragraph(ptext, style["center"]))
ptext = f"{compSite}"
Story.append(Paragraph(ptext, style["center"]))
ptext = f"{compAdress}"
Story.append(Paragraph(ptext, style["center"]))
Story.append(Spacer(1, 12))

# END HEAD

ptext = f"-------------------------------------------------------------"
Story.append(Paragraph(ptext, style["center"]))
Story.append(Spacer(1, 12))

# OS DATA

style.add(ParagraphStyle(name='left', fontSize=12, spaceAfter=3, alignment=TA_LEFT))
ptext = f"<b>COMPROVANTE DE ENTRADA OS Nº</b>{osNumber}"
Story.append(Paragraph(ptext, style["center"]))
Story.append(Spacer(1, 12))
ptext = f"-------------------------------------------------------------"
Story.append(Paragraph(ptext, style["center"]))
Story.append(Spacer(1, 12))
ptext = f"<b>Nome:</b> {cliName}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Endereço:</b> {adress}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Complemento:</b> {adress2}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Tel.:</b> { tel}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Equipamento:</b> {device}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Marca:</b> {brand}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Modelo:</b> {model}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Cor:</b> {color}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Acessórios:</b> {acessories}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Estado do equipamento:</b> {deviceStatus}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Problema relatado:</b> {defect}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Observações:</b> {obs}"
Story.append(Paragraph(ptext, style["left"]))
ptext = f"<b>Data de Entrada:</b> {entryDate}"
Story.append(Paragraph(ptext, style["left"]))
Story.append(Spacer(1, 12))
# END OS DATA

# warranty Terms
ptext = '<b>LEIA COM ATENÇÃO!</b>'
Story.append(Paragraph(ptext, style["center"]))
ptext = '<b>CONDIÇÕES DE SERVIÇOS:</b>'
Story.append(Paragraph(ptext, style["center"]))
Story.append(Spacer(1, 12))
for n, l in enumerate(warrantyTerms, 1):
    ptext = f'<b>{n}</b> - {l}'
    Story.append(Paragraph(ptext, style["left"]))
Story.append(Spacer(1, 20))
# END warranty Terms

# Assignature
ptext = 'Eu li este documento e estou ciente.'
Story.append(Paragraph(ptext, style["center"]))
Story.append(Spacer(1, 12))
ptext = "_________________________________________________"
Story.append(Paragraph(ptext, style["center"]))
Story.append(Spacer(1, 5))
ptext = f'Visto: {cliName}'
Story.append(Paragraph(ptext, style["center"]))
# END Assignature

# Print Date
Story.append(Spacer(1, 12))
ptext = f'Impresso em: {printDate}'
Story.append(Paragraph(ptext, style["center"]))
# END Print Date

doc.build(Story)
