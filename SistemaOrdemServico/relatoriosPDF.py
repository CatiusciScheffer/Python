import webbrowser
from datetime import datetime
from reportlab.lib import pagesizes, colors, units
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


class ManipularCriacaodeRelatorios():
    def __init__(self, db_manager):
        self.db_manager = db_manager

    
    def gerarRelatorioCadServ(self, output_file):
        
        # Conectar ao banco de dados
        cursor = self.db_manager.get_cursor()

        # Obter os dados da tabela
        cursor.execute("SELECT serv_id, serv_codServ, serv_descrServico, serv_vlrUnit FROM tb_servicos_vlr")
        data = cursor.fetchall()

        # Configurações de estilo
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        footer_style = styles['Normal']

        # Criar um documento PDF
        doc = SimpleDocTemplate(output_file, pagesize=pagesizes.A4,
                                topMargin=1.5*units.cm, bottomMargin=1.5*units.cm)
        elements = []

        # Título do PDF centralizado
        title = Paragraph("Relatório dos Serviços Cadastrados", title_style)
        title.alignment = TA_CENTER
        elements.append(title)        
        elements.append(Spacer(1, 20))  # Espaço entre o título e a tabela

        # Criar a tabela com os dados do banco de dados
        table_data = [['ID', 'Código do Serviço', 'Descrição do Serviço', 'Valor Unitário']]
        table_data.extend(data)

        table = Table(table_data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   # ... (estilos da tabela)
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(table)
        
        elements.append(Spacer(1, 20))  # Espaço entre a tabela e o rodapé

        # Espaçamento para o rodapé
        footer_text = "Gerado em: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        footer = Paragraph(footer_text, footer_style)
        elements.append(footer)

        doc.build(elements)
        
        # Abrir o PDF no navegador padrão
        webbrowser.open(output_file, new=2)
        
    def gerarRelatorioCadCliente(self, output_file):
        
        # Conectar ao banco de dados
        cursor = self.db_manager.get_cursor()

        # Obter os dados da tabela
        cursor.execute("SELECT cli_id, cli_codCliente, cli_nomeCliente, cli_qtdNFisenta FROM tb_cliente")
        data = cursor.fetchall()

        # Configurações de estilo
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        footer_style = styles['Normal']

        # Criar um documento PDF
        doc = SimpleDocTemplate(output_file, pagesize=pagesizes.A4,
                                topMargin=1.5*units.cm, bottomMargin=1.5*units.cm)
        elements = []

        # Título do PDF centralizado
        title = Paragraph("Relatório dos Clientes Cadastrados", title_style)
        title.alignment = TA_CENTER
        elements.append(title)        
        elements.append(Spacer(1, 20))  # Espaço entre o título e a tabela

        # Criar a tabela com os dados do banco de dados
        table_data = [['ID', 'Código do Cliente', 'Razão Social', 'Qtd Isenção de NF']]
        table_data.extend(data)

        table = Table(table_data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   # ... (estilos da tabela)
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(table)
        
        elements.append(Spacer(1, 20))  # Espaço entre a tabela e o rodapé

        # Espaçamento para o rodapé
        footer_text = "Gerado em: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        footer = Paragraph(footer_text, footer_style)
        elements.append(footer)

        doc.build(elements)
        
        # Abrir o PDF no navegador padrão
        webbrowser.open(output_file, new=2)