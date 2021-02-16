import pandas as pd
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

def escrever_arquivo_excel( arquivo, complemento, dicionario, maximo_linhas_na_composicao, df_eq, df_mo, df_ma ):
    numero_de_composicoes = len( dicionario )
    numero_linhas = numero_de_composicoes * maximo_linhas_na_composicao
    area_de_impressao = '$D${}:$N${}'.format(1, numero_de_composicoes * maximo_linhas_na_composicao )
    area_formatacao_condicional = '$D${}:$N${}'.format(1, numero_de_composicoes * maximo_linhas_na_composicao )

    # contador para as linhas das composições
    linha_inicio = 1

    # cria um arquivo Excel
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
    format_unitario = workbook.add_format({'bold': True, 'bottom': 1, 'top': 1, 'bg_color':'#C0C0C0'})
    format_total = workbook.add_format({'bold': True, 'bottom': 1, 'top': 1, 'bg_color':'#808080'})
    format_descricao_composicao = workbook.add_format({'bold': True,'italic': True,'align': 'left'})
    format_codigo_composicao = workbook.add_format({'bold': True,'italic': True,'align': 'center'})
    format_complemento = workbook.add_format({'bold': True,'italic': True,'align': 'center', 'font_color': 'red'})
    format_white = workbook.add_format({'font_color': 'white'})
    format_silver = workbook.add_format({'font_color': '#C0C0C0'})
    format_gray = workbook.add_format({'font_color': '#808080'})

    for df in dicionario.values():
        # dfr_insumo
        df.dfr_insumo.to_excel( writer, startrow=(linha_inicio), sheet_name='composicao', index=True )

        worksheet = writer.sheets['composicao']
        
        configurar_impressao(worksheet, area_de_impressao, numero_de_composicoes)

        # acrescentando a linha com dados da composição
        linhas = [ ('D', df.composicao.codigo, format_codigo_composicao), ('E', df.composicao.descricao, format_descricao_composicao), ('L', df.composicao.produtividade, format_codigo_composicao), ('M', df.composicao.unidade, format_codigo_composicao), ('N', complemento, format_complemento) ]
        for lin in linhas:
            worksheet.write( ''.join( (lin[0], str(linha_inicio)) ), lin[1], lin[2])

        # formatando colunas
        colunas = [ ('B:D', modulo, format_centro), ('E:E', 6.0*modulo, format_esquerda), ('F:F', 1.5*modulo, format_centro), ('G:G', modulo, format_valor_2decimais), ('H:H', modulo, format_centro), ('I:I', modulo, format_valor_5decimais), ('J:J', modulo, format_valor_2decimais), ('K:N', 2.6*modulo, format_valor_4decimais) ]
        for col in colunas:
            worksheet.set_column( col[0], col[1], col[2] )

        # formatando as linhas de custos horários e unitários
        criterios = [ ('"{}"'.format(CODIGO_HORARIO), format_horario), ('"{}"'.format(CODIGO_UNITARIO),format_unitario), ('"{}"'.format(CODIGO_UNITARIO_DIRETO_TOTAL),format_total) ]
        for cri in criterios:
            token = 'INDEX($B${inicio}:$N${fim},ROW(),3)={token}'.format(inicio=1, fim=numero_linhas, token=cri[0] )
            worksheet.conditional_format( area_formatacao_condicional, {'type':'formula','criteria': token,'format':cri[1]} )

        # formatação condicional códgio com ho, un e un_dt
        token = '$D${inicio}:$D${fim}'.format(inicio=1, fim=numero_linhas)
        condicoes = [ (CODIGO_HORARIO, format_white), (CODIGO_UNITARIO_DIRETO_TOTAL, format_gray), (CODIGO_UNITARIO, format_silver)]
        for con in condicoes:
            worksheet.conditional_format( token, {'type':'text','criteria':'containing','value': con[0],'format':con[1]} )
        

        linha_inicio = linha_inicio + maximo_linhas_na_composicao

    ##### começa a escrever os insumos das composições
    df_eq.to_excel( writer, index=False, sheet_name='equipamento')
    df_mo.to_excel( writer, index=False, sheet_name='mao_de_obra')
    df_ma.to_excel( writer, index=False, sheet_name='material')

    writer.save()