import pandas as pd
from projeto import *
from constantes import *


def carregar_data_frame(csv):
    # Abrir um arquivo csv a partir do Pandas
    data_frame_csv = pd.read_csv(csv, encoding='utf-8')# encoding='ISO-8859-1')
    return data_frame_csv

def tratar_data_frame(data_frame, lista=list()):
    # Renomeando os nomes das colunas com o método columns
    data_frame.columns = ['Origem', 'Estado', 'Publicacao'] + lista
    # Excluir a última coluna que está com caracteres de tabulação
    if lista[-1] == 'NONE':
        data_frame.pop('NONE')
    return data_frame

def configurar_impressao(worksheet, area_de_impressao, numero_de_composicoes):
    # definindo a área de impressão
    worksheet.print_area( area_de_impressao )
    # dimensionando as páginas largura por extensão
    worksheet.fit_to_pages(1, numero_de_composicoes)
    # rotacionando a página
    worksheet.set_landscape()
    # definindo papel
    worksheet.set_paper(9) # índice 9 (papel A4) vem da documentação da biblioteca xlsxwriter
    # centralizando horizontalmente a tabela na página
    worksheet.center_horizontally()

def escrever_arquivo_excel( arquivo, complemento, projeto: Projeto, maximo_linhas_na_composicao):
    dicionario = projeto.obter_dfr_composicao()
    numero_de_composicoes = len( dicionario )
    numero_linhas = numero_de_composicoes * maximo_linhas_na_composicao
    area_de_impressao = '$D${}:$N${}'.format(1, numero_de_composicoes * maximo_linhas_na_composicao )
    area_formatacao_condicional = '$D${}:$N${}'.format(1, numero_de_composicoes * maximo_linhas_na_composicao )

    # contador para as linhas das composições
    linha_inicio = 1

    # cria um objeto Excel
    writer = pd.ExcelWriter( '.'.join( (arquivo,'xlsx') ) , engine='xlsxwriter' )
    
    workbook  = writer.book 

    modulo = 10

    # Add some cell formats.
    format_valor_5decimais = workbook.add_format({'num_format': '#,##0.00000'})
    format_valor_4decimais = workbook.add_format({'num_format': '#,##0.0000'})
    format_valor_2decimais = workbook.add_format({'num_format': '#,##0.00'})
    format_centro = workbook.add_format({'align': 'center'})
    format_esquerda = workbook.add_format({'align': 'left'})
    format_horario = workbook.add_format({'bold': True, 'bottom': 1, 'top': 1})
    format_unitario = workbook.add_format({'bold': True, 'bottom': 1, 'top': 1, 'bg_color':'#DCDCDC'})
    format_total = workbook.add_format({'bold': True, 'bottom': 1, 'top': 1, 'bg_color':'#A9A9A9'})
    format_preco_unitario = workbook.add_format({'bold': True, 'bottom': 1, 'top': 1, 'bg_color':'#B0C4DE'})
    format_descricao_composicao = workbook.add_format({'bold': True,'italic': True,'align': 'left'})
    format_codigo_composicao = workbook.add_format({'bold': True,'italic': True,'align': 'center'})
    format_produtividade_composicao = workbook.add_format({'bold': True,'italic': True,'align': 'right', 'num_format': '#,##0.00000'})
    format_unidade_composicao = workbook.add_format({'bold': True,'italic': True,'align': 'left'})
    format_complemento = workbook.add_format({'bold': True,'italic': True,'align': 'center', 'font_color': 'red'})
    format_branco = workbook.add_format({'font_color': 'white'})
    format_cinza_claro = workbook.add_format({'font_color': '#DCDCDC'})
    format_cinza_medio = workbook.add_format({'font_color': '#A9A9A9'})
    format_azul_forte = workbook.add_format({'font_color': '#B0C4DE'})

    for df in dicionario.values():
        # dfr_insumo
        df.dfr_insumo.to_excel( writer, startrow=(linha_inicio), sheet_name='composicao', index=True )

        worksheet_dfr_composicao = writer.sheets['composicao']
        
        configurar_impressao(worksheet_dfr_composicao, area_de_impressao, numero_de_composicoes)

        # acrescentando a linha com dados da composição
        linhas = [ ('D', df.composicao.codigo, format_codigo_composicao), ('E', df.composicao.descricao, format_descricao_composicao), ('L', df.composicao.produtividade, format_produtividade_composicao), ('M', df.composicao.unidade, format_unidade_composicao), ('N', complemento, format_complemento) ]
        for lin in linhas:
            worksheet_dfr_composicao.write( ''.join( (lin[0], str(linha_inicio)) ), lin[1], lin[2])

        # formatando colunas
        colunas = [ ('B:D', modulo, format_centro), ('E:E', 12.0*modulo, format_esquerda), ('F:F', 1.5*modulo, format_centro), ('G:G', modulo, format_valor_2decimais), ('H:H', modulo, format_centro), ('I:I', modulo, format_valor_5decimais), ('J:J', modulo, format_valor_2decimais), ('K:N', 2.6*modulo, format_valor_4decimais) ]
        for col in colunas:
            worksheet_dfr_composicao.set_column( col[0], col[1], col[2] )

        # formatando as linhas de custos horários e unitários
        criterios = [ ('"{}"'.format(CODIGO_HORARIO), format_horario), ('"{}"'.format(CODIGO_UNITARIO),format_unitario), ('"{}"'.format(CODIGO_HORARIO_EXECUCAO),format_horario), ('"{}"'.format(CODIGO_UNITARIO_DIRETO_TOTAL),format_total), ('"{}"'.format(CODIGO_PRECO_TOTAL),format_preco_unitario) ]
        for cri in criterios:
            token = 'INDEX($B${inicio}:$N${fim},ROW(),3)={token}'.format(inicio=1, fim=numero_linhas, token=cri[0] )
            worksheet_dfr_composicao.conditional_format( area_formatacao_condicional, {'type':'formula','criteria': token,'format':cri[1]} )

        # formatação condicional códgio com ho, un e un_dt
        token = '$D${inicio}:$D${fim}'.format(inicio=1, fim=numero_linhas)
        condicoes = [ (CODIGO_HORARIO, format_branco), (CODIGO_UNITARIO_DIRETO_TOTAL, format_cinza_medio), (CODIGO_HORARIO_EXECUCAO, format_branco), (CODIGO_UNITARIO, format_cinza_claro), (CODIGO_PRECO_TOTAL, format_azul_forte)]
        for con in condicoes:
            worksheet_dfr_composicao.conditional_format( token, {'type':'text','criteria':'containing','value': con[0],'format':con[1]} )
        

        linha_inicio = linha_inicio + maximo_linhas_na_composicao

    # ##### começa a escrever equipamentos das composições ###################################
   
    dfr_equipamento = projeto.obter_dfr_equipamento()

    dfr_equipamento.to_excel( writer, index=False, sheet_name='equipamento')

    worksheet_dfr_equipamento = writer.sheets['equipamento']
    
    tamanho = dfr_equipamento.shape[0]

    area_de_impressao = '$A${}:$I${}'.format(1, tamanho )
    
    # definindo a área de impressão
    worksheet_dfr_equipamento.print_area( area_de_impressao )
    # dimensionando as páginas largura por extensão
    worksheet_dfr_equipamento.fit_to_pages(1, tamanho)
    # rotacionando a página
    worksheet_dfr_equipamento.set_portrait()
    # definindo papel
    worksheet_dfr_equipamento.set_paper(9) # índice 9 (papel A4) vem da documentação da biblioteca xlsxwriter
    # centralizando horizontalmente a tabela na página
    worksheet_dfr_equipamento.center_horizontally()

    # formatando colunas
    colunas = [ ('A:E', 1.2*modulo, format_centro), ('F:F', 8.0*modulo, format_esquerda), ('G:G', modulo, format_centro), ('H:I', 2.5*modulo, format_valor_4decimais) ]
    for col in colunas:
        worksheet_dfr_equipamento.set_column( col[0], col[1], col[2] )

    # ##### começa a escrever mão de obra das composições ###################################

    dfr_mao_de_obra = projeto.obter_dfr_mao_de_obra()

    dfr_mao_de_obra.to_excel( writer, index=False, sheet_name='mao_de_obra')

    worksheet_dfr_mao_de_obra = writer.sheets['mao_de_obra']
    
    tamanho = dfr_mao_de_obra.shape[0]

    area_de_impressao = '$A${}:$I${}'.format(1, tamanho )
    
    # definindo a área de impressão
    worksheet_dfr_mao_de_obra.print_area( area_de_impressao )
    # dimensionando as páginas largura por extensão
    worksheet_dfr_mao_de_obra.fit_to_pages(1, tamanho)
    # rotacionando a página
    worksheet_dfr_mao_de_obra.set_portrait()
    # definindo papel
    worksheet_dfr_mao_de_obra.set_paper(9) # índice 9 (papel A4) vem da documentação da biblioteca xlsxwriter
    # centralizando horizontalmente a tabela na página
    worksheet_dfr_mao_de_obra.center_horizontally()

    # formatando colunas
    colunas = [ ('A:E', 1.2*modulo, format_centro), ('F:F', 8.0*modulo, format_esquerda), ('G:G', modulo, format_centro), ('H:H', 2.5*modulo, format_valor_4decimais) ]
    for col in colunas:
        worksheet_dfr_mao_de_obra.set_column( col[0], col[1], col[2] )


   # ##### começa a escrever materiais das composições ###################################

    dfr_material = projeto.obter_dfr_material()

    dfr_material.to_excel( writer, index=False, sheet_name='material')

    worksheet_dfr_material = writer.sheets['material']
    
    tamanho = dfr_material.shape[0]

    area_de_impressao = '$A${}:$I${}'.format(1, tamanho )
    
    # definindo a área de impressão
    worksheet_dfr_material.print_area( area_de_impressao )
    # dimensionando as páginas largura por extensão
    worksheet_dfr_material.fit_to_pages(1, tamanho)
    # rotacionando a página
    worksheet_dfr_material.set_portrait()
    # definindo papel
    worksheet_dfr_material.set_paper(9) # índice 9 (papel A4) vem da documentação da biblioteca xlsxwriter
    # centralizando horizontalmente a tabela na página
    worksheet_dfr_material.center_horizontally()

    # formatando colunas
    colunas = [ ('A:E', 1.2*modulo, format_centro), ('F:F', 8.0*modulo, format_esquerda), ('G:G', modulo, format_centro), ('H:H', 2.5*modulo, format_valor_4decimais) ]
    for col in colunas:
        worksheet_dfr_material.set_column( col[0], col[1], col[2] )

   # ##### começa a escrever transportes das composições ###################################

    dfr_transporte = projeto.obter_dfr_transporte()

    dfr_transporte.to_excel( writer, index=False, sheet_name='transporte')

    writer.save()

