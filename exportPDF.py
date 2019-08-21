import time, os
from database import Database
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
paper = '58mm'

def makePDF(soId = 1, osType = 2):
    banco = Database('database.db')
    # companies info
    resultc = banco.queryDB(f"""SELECT logo, name, slogan, adress, number,
    adress2, district, city, state, phone3, phone1, phone2, email, site FROM companies WHERE id=1""")
    logo = resultc[0][0]
    compName = resultc[0][1]
    slogan = resultc[0][2]
    compAdress = f'{resultc[0][3]}, {resultc[0][4]}, {resultc[0][5]}, {resultc[0][6]}, {resultc[0][7]} - {resultc[0][8]}'
    companyPhones = f'{resultc[0][9]} / {resultc[0][10]}'
    compEmail = resultc[0][12]
    compSite = resultc[0][13]
    # END companies info

    # OS info
    result = banco.queryDB(f'SELECT clients.name, entryDate, clients.adress, clients.number,clients.adress2, clients.district, clients.city, clients.state, clients.phone3, clients.phone1, clients.phone2, deviceType, brand, model, color, acessories, deviceStatus, defect, defectFound, obs1, obs2, status, serviceValue FROM serviceOrders INNER JOIN clients ON clients.id=serviceOrders.idCli WHERE serviceOrders.id={soId}')
    print('RES: ', result)
    osNumber = soId
    cliName = result[0][0]
    entryDate = result[0][1]
    adress = f'{result[0][2]}, {result[0][3]}, {result[0][4]}, {result[0][5]}, {result[0][6]}, {result[0][7]}'
    cliPhones = f'{result[0][8]} {result[0][9]} {result[0][10]}'
    device = result[0][11]
    brand = result[0][12]
    model = result[0][13]
    color = result[0][14]
    acessories = result[0][15]
    deviceStatus = result[0][16]
    defect = result[0][17]
    defectFound = result[0][18]
    obs = result[0][19]
    obs2 = result[0][19]
    status = result[0][21]
    resultParts = banco.queryDB(f"""SELECT * FROM soProducts WHERE soId={soId}""")
    print('SQL PARTS: ', resultParts)
    if resultParts:
        partTotalValue = 0.0
        data=[('Descrição', 'Quantidade', 'Valor Un')]
        for part in resultParts:
            partTotalValue += part[2] * part[3]
            part = list(part)
            part.pop(0)
            data.append(part)
        print('DATA: ', data)
    else:
        partTotalValue = 0.0
        data=[]
    serviceValue = result[0][22]
    total = serviceValue + partTotalValue
    printDate = time.strftime("%d/%m/%Y %H:%M:%S")
    Terms = [
    'Ao deixar seu equipamento retire o chip e cartão de memória, não nos responsabilizamos por estes itens.',
    'Os aparelhos não retirados no prazo máximo de 90 dias contados a partir da data em que for orçado, será cobrado uma taxa de R$10,00 por dia para cobrir custos de armazenamento.',
    'O aparelho só será devolvido para o titular deste documento, caso necessário o titular poderá solicitar retirada por terceiros.']
    warrantyTerms = [
    'A empresa da 90 dias de garantia nas PEÇAS E VALORES e serviços realizados.',
    'A garantia não cobre defeitos causados pelo usuário ou mau uso do aparelho, como quebra ou arranhões nas peças trocas.',
    'A violação do lacre de garantia ou a desmontagem do aparelho por pessoas não autorizadas acarretará na perca da garantia.']
    # END OS info

    def entryA4():
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
        ptext = f"{companyPhones}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{compEmail}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{compSite}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{compAdress}"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 12))
        # END HEAD
        # OS DATA
        trace = f"{'-'*109}"
        Story.append(Paragraph(trace, style["center"]))
        Story.append(Spacer(1, 12))
        style.add(ParagraphStyle(name='left', fontSize=12, spaceAfter=3, alignment=TA_LEFT))
        ptext = f"<b>COMPROVANTE DE ENTRADA OS Nº</b>{osNumber}"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(trace, style["center"]))
        Story.append(Spacer(1, 12))
        ptext = f"<b>Nome:</b> {cliName}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>End'80mm'ereço:</b> {adress}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Tel.:</b> {cliPhones}"
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
        ptext = f"<b>Status atual:</b> {status}"
        Story.append(Paragraph(ptext, style["left"]))
        Story.append(Spacer(1, 12))
        # END OS DATA

        # warranty Terms
        ptext = '<b>LEIA COM ATENÇÃO!</b>'
        Story.append(Paragraph(ptext, style["center"]))
        ptext = '<b>CONDIÇÕES DE SERVIÇOS:</b>'
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 12))
        for n, l in enumerate(Terms, 1):
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

    def budgetA4():
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
        style.add(ParagraphStyle(name='center', fontSize=12, alignment=TA_CENTER, spaceAfter=3))
        ptext = f"<b>{compName}</b>"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{slogan}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{companyPhones}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{compEmail}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{compSite}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{compAdress}"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 12))
        # END HEAD
        # OS DATA
        trace = f"{'-'*109}"
        Story.append(Paragraph(trace, style["center"]))
        Story.append(Spacer(1, 12))
        style.add(ParagraphStyle(name='left', fontSize=12, spaceAfter=3, alignment=TA_LEFT))
        ptext = f"<b>ORÇAMENTO ORDEM DE SERVIÇO Nº</b>{osNumber}"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(trace, style["center"]))
        Story.append(Spacer(1, 12))
        ptext = f"<b>Nome:</b> {cliName}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Tel.:</b> {cliPhones}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Equipamento:</b> {device}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Marca:</b> {brand}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Modelo:</b> {model}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Cor:</b> {color}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Problema relatado:</b> {defect}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Defeito encontrado:</b> {defectFound}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Observações:</b> {obs2}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Data de Entrada:</b> {entryDate}"
        Story.append(Paragraph(ptext, style["left"]))
        Story.append(Spacer(1, 12))
        # END OS DATA

        ptext = '<b>PEÇAS E VALORES:</b>'
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 20))
        if data:
            table = Table(data)
            table.setStyle(TableStyle([('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
                                    ('BOX', (0,0), (-1, -1), 0.25, colors.black),
                                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                    ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
            Story.append(table)
            Story.append(Spacer(1, 20))
        ptext = f'<b>Valor total de peças:</b> {partTotalValue}'
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f'<b>Valor da Mão de Obra</b>: {serviceValue}'
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f'<b>Valor Total a Pagar:</b> {total}'
        Story.append(Paragraph(ptext, style["center"]))
        ptext = 'Orçamento válido por 10 dias.'
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 12))
        ptext = f'Hoje {printDate} declaro ter recebido e assinado este orçamento e autorizo o andamento do serviço.'
        Story.append(Paragraph(ptext, style["center"]))
        # Assignature
        Story.append(Spacer(1, 12))
        ptext = "_________________________________________________"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 20))
        ptext = f'Visto: {cliName}'
        Story.append(Paragraph(ptext, style["center"]))
        # END Assignature

        doc.build(Story)

    def entry58mm():
        fileName = f'{os.getcwd()}/OS_DIR/os{osNumber}.pdf'
        pagesize=(57.86*mm, 209.9*mm)
        doc = SimpleDocTemplate(fileName ,pagesize=pagesize, rightMargin=7, leftMargin=8, topMargin=0, bottomMargin=0)
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
        ptext = f"{companyPhones}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{compEmail}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{compSite}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"{compAdress}"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))
        # END HEAD

        ptext = "------------------------------------"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))

        # OS DATA
        style.add(ParagraphStyle(name='left', fontsize=9, spaceAfter=1, alignment=TA_LEFT))
        ptext = f"<b>COMPROVANTE DE ENTRADA OS Nº</b>{osNumber}"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))
        ptext = "------------------------------------"
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
        ptext = f"<b>Tel.:</b> {cliPhones}"
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
        for n, l in enumerate(Terms, 1):
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

    def budget58mm():
        fileName = f'{os.getcwd()}/OS_DIR/os{osNumber}.pdf'
        pagesize=(57.86*mm, 209.9*mm)
        doc = SimpleDocTemplate(fileName ,pagesize=pagesize, rightMargin=7, leftMargin=8, topMargin=0, bottomMargin=0)
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
        ptext = f"{companyPhones}"
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

        # OS DATA
        style.add(ParagraphStyle(name='left', fontsize=9, spaceAfter=1, alignment=TA_LEFT))
        ptext = f"<b>ORÇAMENTO OS Nº</b>{osNumber}"
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f"------------------------------------"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))
        ptext = f"<b>Nome:</b> {cliName}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Tel.:</b> {cliPhones}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Equipamento:</b> {device}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Marca:</b> {brand}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Modelo:</b> {model}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Cor:</b> {color}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Problema relatado:</b> {defect}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Defeito encontrado:</b> {defectFound}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Observações:</b> {obs2}"
        Story.append(Paragraph(ptext, style["left"]))
        ptext = f"<b>Data de Entrada:</b> {entryDate}"
        Story.append(Paragraph(ptext, style["left"]))
        Story.append(Spacer(1, 3))
        # END OS DATA

        ptext = '<b>PEÇAS E VALORES:</b>'
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 3))
        if data:
            table = Table(data)
            table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.50, colors.black),
                                    ('BOX', (0,0), (-1, -1), 0.50, colors.black),
                                    ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
                                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                    ('FONTSIZE', (0,0), (-1,-1), 5),
                                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
            Story.append(table)
            Story.append(Spacer(1, 3))
        ptext = f'<b>Valor total de peças:</b> {partTotalValue}'
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f'<b>Valor da Mão de Obra</b>: {serviceValue}'
        Story.append(Paragraph(ptext, style["center"]))
        ptext = f'<b>Valor Total a Pagar:</b> {total}'
        Story.append(Paragraph(ptext, style["center"]))
        ptext = 'Orçamento válido por 10 dias.'
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 12))
        ptext = f'Hoje {printDate} declaro ter recebido e assinado este orçamento e autorizo o andamento do serviço.'
        Story.append(Paragraph(ptext, style["center"]))
        # Assignature
        Story.append(Spacer(1, 12))
        ptext = "_______________________"
        Story.append(Paragraph(ptext, style["center"]))
        Story.append(Spacer(1, 20))
        ptext = f'Visto: {cliName}'
        Story.append(Paragraph(ptext, style["center"]))
        # END Assignature

        doc.build(Story)

    def entry80mm():
        pass

    if not 'OS_DIR' in os.listdir():
        os.mkdir('OS_DIR')

# # TODO: implementar modelos de 80mm e modelos de notas de saída em todas medidas
    if osType == 1:
        if paper == 'A4':
            entryA4()
        if paper == '58mm':
            entry58mm()
        if paper == '80mm':
            entry80mm()
    elif osType == 2:
        if paper == 'A4':
            budgetA4()
        if paper == '58mm':
            budget58mm()
        if paper == '80mm':
            budget80mm()

    elif osType == 3:
        if paper == 'A4':
            outA4()
        if paper == '58mm':
            out58mm()
        if paper == '80mm':
            out80mm()
