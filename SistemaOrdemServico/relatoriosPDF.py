import webbrowser
from datetime import datetime
from tkinter import simpledialog, messagebox, filedialog
from reportlab.lib import pagesizes, colors, units
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER


import sqlite3


class ManipularCriacaodeRelatorios():
    def __init__(self, db_manager):
        self.db_manager = db_manager

    @staticmethod
    def calculate_column_widths(data):
        column_widths = []

        for col in range(len(data[0])):
            max_width = max([len(str(row[col])) for row in data if col < len(row)])
            column_widths.append(max_width * 6.5)  # Ajuste esse multiplicador conforme necessário

        return column_widths  
    
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
    
    def selecionalLocalSalvarRelatorio(self, relatorioSalvar):
        # Solicitar o local onde o usuário deseja salvar o relatório
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if not file_path:
            return  # O usuário cancelou a operação de salvamento

        # Copie o relatório gerado para o local escolhido pelo usuário
        try:
            import shutil
            shutil.copy(relatorioSalvar, file_path)
            messagebox.showinfo("Relatório Salvo", f"O relatório foi salvo em:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Erro ao Salvar Relatório", f"Ocorreu um erro ao salvar o relatório:\n{str(e)}")
                
    def gerarRelatorioOdensServicoNAOfaturadas(self):
        # Conectar ao banco de dados
        cursor = self.db_manager.get_cursor()

        
        # Obter os dados da tabela
        cursor.execute("""
            SELECT 
                os.os_dtServico,
                os.os_codCliente,
                os.os_cliente,
                os.os_codServico,
                os.os_descServico,
                SUM(os.os_qtd) as total_quantidade,
                os.os_vlrUnit,
                SUM(os.os_total) as total_valor_total,
                c.cli_qtdNFisenta
            FROM tb_ordens_servicos AS os
            LEFT JOIN tb_cliente AS c ON os.os_codCliente = c.cli_codCliente
            WHERE os.os_faturado = 'NÃO'
            GROUP BY os.os_cliente, os.os_codServico, os.os_descServico, c.cli_qtdNFisenta
            ORDER BY os.os_cliente, os.os_codServico
        """)
        column_names = [desc[0] for desc in cursor.description]  # Obter nomes das colunas

        data = cursor.fetchall()

        # Configurações de estilo
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        footer_style = styles['Normal']

        output_file = 'relatorio.pdf'
        # Criar um documento PDF
        doc = SimpleDocTemplate(output_file, pagesize=landscape(A4),
                                leftMargin=1*units.cm, rightMargin=1*units.cm)
        elements = []

        # Título do PDF centralizado
        title = Paragraph("Relatório Ordens a Faturar", title_style)
        title.alignment = 1  # 0 para alinhar à esquerda, 1 para centralizar, 2 para alinhar à direita
        elements.append(title)
        elements.append(Spacer(1, 10))  # Espaço entre o título e a tabela

        # Inicialize as variáveis de total
        total_total_novo = 0
        
        # Criar a tabela com os dados do banco de dados
        table_data = [['Data', 'Código\nCliente', 'Cliente', 'Código\nServiço', 'Descrição do Serviço', 'NF\nDesconto','Quantidade','Quantidade\n(-)\nDesconto', 'Valor\nUnitário', 'Total\nCódigo\nServiço']]
        
        for row in data:
            row_dict = dict(zip(column_names, row))  # Converter a tupla em um dicionário
            os_codServico = row_dict['os_codServico']
            cli_qtdNFisenta = (row_dict['cli_qtdNFisenta'])
            total_quantidade = row_dict['total_quantidade']
            total_novo = row_dict['total_valor_total']
            vlrUnitario_novo = row_dict['os_vlrUnit']

            # Verifica se os_codServico é igual a 22
            if os_codServico == 22:
                # Subtrai cli_qtdNFisenta de total_quantidade
                quantidade = total_quantidade - cli_qtdNFisenta
                total_novo = quantidade * vlrUnitario_novo
            else:
                quantidade = total_quantidade

            # Adiciona a linha à tabela com a quantidade calculada
            table_data.append([
                row_dict['os_dtServico'],
                row_dict['os_codCliente'],
                row_dict['os_cliente'],
                row_dict['os_codServico'],
                row_dict['os_descServico'],
                row_dict['cli_qtdNFisenta'],
                row_dict['total_quantidade'],
                quantidade,  # Usamos a quantidade calculada aqui
                row_dict['os_vlrUnit'],
                f'{total_novo:.2f}'               
            ])
            # Atualize os totais
            total_total_novo += total_novo

        # Adicione a linha com os totais
        total_row = ['TOTAL À FATURAR', '', '', '', '', '', '', '', '', f'{total_total_novo:.2f}']
        table_data.append(total_row)

        # Calcula a largura das colunas com base no conteúdo
        col_widths = [60, 40, 210, 40, 210,50, 60, 60, 50, 50]  # Ajuste conforme necessário

        # Crie a tabela com as larguras de coluna calculadas
        table = Table(table_data, colWidths=col_widths)

        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento horizontal no centro
                                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey)]))
        
        # Defina um estilo para a célula de total
        total_style = TableStyle([
                                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),  # Define a cor de fundo da última linha
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),  # Alinhamento horizontal no centro para a última linha
                                ('LINEBELOW', (0, -1), (-1, -1), 2, colors.grey),  # Adicione uma linha abaixo da última linha
                                ('SPAN', (0, -1), (-2, -1)),  # Mesclar todas as colunas, exceto a última, na última linha
                            ])

        table.setStyle(total_style)
        
        elements.append(table)

        elements.append(Spacer(1, 20))  # Espaço entre a tabela e o rodapé

        # Espaçamento para o rodapé
        footer_text = "Gerado em: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        footer = Paragraph(footer_text, footer_style)
        elements.append(footer)

        doc.build(elements)

        # Abrir o PDF no navegador padrão
        #webbrowser.open(output_file, new=2)
        return output_file
        
    def gerarRelatorioOdensServicoTodas(self, output_file):
        # Conectar ao banco de dados
        cursor = self.db_manager.get_cursor()

        # Obter os dados da tabela
        cursor.execute("SELECT * FROM tb_ordens_servicos AS os ORDER BY os.os_dtServico")
        data = cursor.fetchall()

        # Configurações de estilo
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        footer_style = styles['Normal']

        # Criar um documento PDF
        
        doc = SimpleDocTemplate(output_file, pagesize=landscape(A4),
                                topMargin=1*units.cm, bottomMargin=1*units.cm)
        elements = []

        # Título do PDF centralizado
        title = Paragraph("Relatório Geral dos Serviços", title_style)
        title.alignment = TA_CENTER
        elements.append(title)        
        elements.append(Spacer(1, 20))  # Espaço entre o título e a tabela

        # Criar a tabela com os dados do banco de dados
        table_data = [['ID', 'Data', 'Código\nCliente', 'Cliente', 'Código\nServiço', 'Descrição do Serviço', 'Qtd','Valor\nUnit.', 'Valor\nTotal', 'Descr.\nCompl.', 'Sit.\nFat.', 'Data\nFaturamento', 'Responsável']]
        table_data.extend(data)

        table = Table(table_data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento horizontal no centro
                                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
                                ('FONTSIZE', (0, 0), (-1, -1), 8)]))
        elements.append(table)
        
        elements.append(Spacer(1, 20))  # Espaço entre a tabela e o rodapé

        # Espaçamento para o rodapé
        footer_text = "Gerado em: {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        footer = Paragraph(footer_text, footer_style)
        elements.append(footer)

        doc.build(elements)
        
        # Abrir o PDF no navegador padrão
        webbrowser.open(output_file, new=2)