import time
from database import Database
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm

def makePDF(compId, osId, paper):
    banco = Database('database.db')
    # Company info
    result = resultc = banco.queryDB(f"""SELECT logo, name, slogan, adress, number,
    adress2, district, city, state, tel, cell1, cell2, email, site FROM company WHERE id={compId}""")
    logo = resultc[0][0]
    compName = resultc[0][1]
    slogan = resultc[0][2]
    compAdress = f'{resultc[0][3]}, {resultc[0][4]}, {resultc[0][5]}, {resultc[0][6]}, {resultc[0][7]} - {resultc[0][8]}'
    compTel = f'{resultc[0][9]} / {resultc[0][10]} / {resultc[0][11]}'
    compEmail = resultc[0][12]
    compSite = resultc[0][13]
    # END Company info

    # OS info
    result = banco.queryDB(f'SELECT clients.name, entryDate, clients.adress, clients.number,clients.adress2, clients.district, clients.city, clients.state, clients.tel, clients.cell1, clients.cell2, deviceType, brand, model, color, acessories, deviceStatus, defect, obs1 FROM service_order INNER JOIN clients ON clients.id=service_order.idCli WHERE service_order.id={osId}')
    print('RES: ', result)
    osNumber = osId
    cliName = result[0][0]
    entryDate = result[0][1]
    adress = f'{result[0][2]}, {result[0][3]}, {result[0][4]}, {result[0][5]}, {result[0][6]}, {result[0][7]}'
    tel = f'{result[0][8]} {result[0][9]} {result[0][10]}'
    device = result[0][11]
    brand = result[0][12]
    model = result[0][13]
    color = result[0][14]
    acessories = result[0][15]
    deviceStatus = result[0][16]
    defect = result[0][17]
    obs = result[0][18]
    printDate = time.strftime("%d/%m/%Y %H:%M:%S")
    warrantyTerms = [
    'Ao deixar seu equipamento retire o chip e cartão de memória, não nos responsabilizamos por estes itens.',
    'Os aparelhos não retirados no prazo máximo de 90 dias contados a partir da data em que for orçado, será cobrado uma taxa de R$10,00 por dia para cobrir custos de armazenamento.',
    'O aparelho só será devolvido para o titular deste documento, caso necessário o titular poderá solicitar retirada por terceiros.']
    # END OS info

    def docA4():
        import os
        fileName = f'{os.getcwd()}/OS_DIR/os{osNumber}.pdf'
        doc = SimpleDocTemplate(fileName ,pagesize=A4, rightMargin=72, leftMargin=72, topMargin=30, bottomMargin=18)
        Story=[]
        # LOGO
        im = Image(logo, 30*mm, 30*mm, hAlign='CENTER')
        Story.append(im)
        Story.append(Spacer(1, 12))
        # END LOGO

        # HEAD
        style=getSampleStyleSheet()
        style.add(ParagraphStyle(name='center', fontSize=12, alignment=TA_CENTER))
        ptext = f"<b>{compName}</b>"
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
        '''
        ptext = f"<b>Complemento:</b> {adress2}"
        Story.append(Paragraph(ptext, style["left"]))
        '''
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
        Story.append(Spacer(1, 20))
        ptext = f'Visto: {cliName}'
        Story.append(Paragraph(ptext, style["center"]))
        # END Assignature

        # Print Date
        Story.append(Spacer(1, 12))
        ptext = f'Impresso em: {printDate}'
        Story.append(Paragraph(ptext, style["center"]))
        # END Print Date

        doc.build(Story)

    def doc58mm():
        import os
        fileName = f'{os.getcwd()}/OS_DIR/os{osNumber}.pdf'
        pagesize=(57.86*mm, 209.9*mm)
        doc = SimpleDocTemplate(fileName ,pagesize=pagesize, rightMargin=5, leftMargin=10, topMargin=5, bottomMargin=5)
        Story=[]
        # LOGO
        im = Image(logo, 15*mm, 15*mm, hAlign='CENTER')
        Story.append(im)
        Story.append(Spacer(1, 3))
        # END LOGO

        # HEAD
        style=getSampleStyleSheet()
        style.add(ParagraphStyle(name='center', fontsize=9, alignment=TA_CENTER))
        ptext = f"<b>{compName}</b>"
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
        Story.append(Spacer(1, 3))
        # END HEAD

        ptext = f"------------------------------------"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))

        # OS DATA
        style.add(ParagraphStyle(name='left', fontsize=9, spaceAfter=1, alignment=TA_LEFT))
        ptext = f"<b>COMPROVANTE DE ENTRADA OS Nº</b>{osNumber}"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))
        ptext = f"------------------------------------"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))
        ptext = f"<b>Nome:</b> {cliName}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Endereço:</b> {adress}"
        Story.append(Paragraph(ptext, style["left"]))
        '''
        ptext = f"<b>Complemento:</b> {adress2}"
        Story.append(Paragraph(ptext, style["left"]))
        '''
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
        Story.append(Spacer(1, 3))
        # END OS DATA

        # warranty Terms
        ptext = '<b>LEIA COM ATENÇÃO!</b>'
        Story.append(Paragraph(ptext, style["center"]))
        ptext = '<b>CONDIÇÕES DE SERVIÇOS:</b>'
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))
        for n, l in enumerate(warrantyTerms, 1):
            ptext = f'<b>{n}</b> - {l}'
            Story.append(Paragraph(ptext, style["left"]))
        Story.append(Spacer(1, 5))
        # END warranty Terms

        # Assignature
        ptext = 'Eu li este documento e estou ciente.'
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))
        ptext = "_______________________"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))
        ptext = f'Visto: {cliName}'
        Story.append(Paragraph(ptext, style["center"]))
        # END Assignature

        # Print Date
        Story.append(Spacer(1, 3))
        ptext = f'Impresso em: {printDate}'
        Story.append(Paragraph(ptext, style["center"]))
        # END Print Date

        doc.build(Story)

    def doc80mm():
        pass

    if paper == 'A4':
        docA4()
    elif paper == '58mm':
        doc58mm()
    elif paper == '80mm':
        doc80mm()
