import pandas as pd
from projeto import (
                        Projeto,
                    )
from estrutura_dados import (
                        NohArvore,
                        NohPilha,
                        Pilha,
                        NohFila,
                        Fila,
                    )
from constantes import (
                        EQUIPAMENTO,
                        EQUIPAMENTO_CUSTO_HORARIO,
                        MAO_DE_OBRA,
                        MAO_DE_OBRA_CUSTO_HORARIO,
                        EXECUCAO_HORARIO,
                        EXECUCAO_UNITARIO,
                        MATERIAL,
                        MATERIAL_CUSTO_UNITARIO,
                        ATIVIDADE_AUXILIAR,
                        ATIVIDADE_AUXILIAR_CUSTO_TOTAL,
                        TEMPO_FIXO,
                        TEMPO_FIXO_CUSTO_TOTAL,
                        TRANSPORTE,
                        TRANSPORTE_CUSTO_TOTAL,
                        DIRETO_TOTAL_UNITARIO,
                        CODIGO_HORARIO,
                        CODIGO_HORARIO_EXECUCAO,
                        CODIGO_UNITARIO,
                        CODIGO_UNITARIO_DIRETO_TOTAL,
                        CODIGO_PRECO_TOTAL 
                    )


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
    format_valor_10decimais = workbook.add_format({'num_format': '#,##0.0000000000'})
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
    # format_cinza_claro = workbook.add_format({'font_color': '#DCDCDC'})
    # format_cinza_medio = workbook.add_format({'font_color': '#A9A9A9'})
    # format_azul_forte = workbook.add_format({'font_color': '#B0C4DE'})

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
        condicoes = [ (CODIGO_HORARIO, format_branco), (CODIGO_UNITARIO_DIRETO_TOTAL, format_branco), (CODIGO_HORARIO_EXECUCAO, format_branco), (CODIGO_UNITARIO, format_branco), (CODIGO_PRECO_TOTAL, format_branco)]
        for con in condicoes:
            worksheet_dfr_composicao.conditional_format( token, {'type':'text','criteria':'containing','value': con[0],'format':con[1]} )
        

        linha_inicio = linha_inicio + maximo_linhas_na_composicao

    # ##### começa a escrever equipamentos das composições ###################################
   
    dfr_equipamento = projeto.obter_dfr_equipamento()

    dfr_equipamento.to_excel( writer, index=False, sheet_name='equipamento_custo')

    worksheet_dfr_equipamento = writer.sheets['equipamento_custo']
    
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
    # repetindo primeira linha
    worksheet_dfr_equipamento.repeat_rows(0)

    # formatando colunas
    colunas = [ ('A:E', 1.2*modulo, format_centro), ('F:F', 8.0*modulo, format_esquerda), ('G:G', modulo, format_centro), ('H:I', 2.5*modulo, format_valor_4decimais) ]
    for col in colunas:
        worksheet_dfr_equipamento.set_column( col[0], col[1], col[2] )

    # ##### começa a escrever mão de obra das composições ###################################

    dfr_mao_de_obra = projeto.obter_dfr_mao_de_obra()

    dfr_mao_de_obra.to_excel( writer, index=False, sheet_name='mao_de_obra_custo')

    worksheet_dfr_mao_de_obra = writer.sheets['mao_de_obra_custo']
    
    tamanho = dfr_mao_de_obra.shape[0]

    area_de_impressao = '$A${}:$H${}'.format(1, tamanho )
    
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
    # repetindo primeira linha
    worksheet_dfr_mao_de_obra.repeat_rows(0)

    # formatando colunas
    colunas = [ ('A:E', 1.2*modulo, format_centro), ('F:F', 8.0*modulo, format_esquerda), ('G:G', modulo, format_centro), ('H:H', 2.5*modulo, format_valor_4decimais) ]
    for col in colunas:
        worksheet_dfr_mao_de_obra.set_column( col[0], col[1], col[2] )


   # ##### começa a escrever materiais das composições ###################################

    dfr_material = projeto.obter_dfr_material()

    dfr_material.to_excel( writer, index=False, sheet_name='material_custo')

    worksheet_dfr_material = writer.sheets['material_custo']
    
    tamanho = dfr_material.shape[0]

    area_de_impressao = '$A${}:$H${}'.format(1, tamanho )
    
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
    # repetindo primeira linha
    worksheet_dfr_material.repeat_rows(0)

    # formatando colunas
    colunas = [ ('A:E', 1.2*modulo, format_centro), ('F:F', 8.0*modulo, format_esquerda), ('G:G', modulo, format_centro), ('H:H', 2.5*modulo, format_valor_4decimais) ]
    for col in colunas:
        worksheet_dfr_material.set_column( col[0], col[1], col[2] )

   # ##### começa a escrever transportes das composições ###################################

    dfr_transporte = projeto.obter_dfr_transportes_servicos()
    
    dfr_transporte.to_excel( writer, index=True, sheet_name='transporte_servico_utilizacao')

    worksheet_dfr_transporte = writer.sheets['transporte_servico_utilizacao']
    
    tamanho = dfr_transporte.shape[0]

    area_de_impressao = '$A${}:$H${}'.format(1, tamanho )
    
    # definindo a área de impressão
    worksheet_dfr_transporte.print_area( area_de_impressao )
    # dimensionando as páginas largura por extensão
    worksheet_dfr_transporte.fit_to_pages(1, tamanho)
    # rotacionando a página
    worksheet_dfr_transporte.set_portrait()
    # definindo papel
    worksheet_dfr_transporte.set_paper(9) # índice 9 (papel A4) vem da documentação da biblioteca xlsxwriter
    # centralizando horizontalmente a tabela na página
    worksheet_dfr_transporte.center_horizontally()
    # repetindo primeira linha
    worksheet_dfr_transporte.repeat_rows(0)

    # formatando colunas
    colunas = [ ('A:A', 0.5*modulo, format_centro), ('B:D', 2.0*modulo, format_centro), ('E:E', 8.5*modulo, format_esquerda), ('F:G', 1.5*modulo, format_centro), ('H:H', 2.5*modulo, format_valor_10decimais) ]
    for col in colunas:
        worksheet_dfr_transporte.set_column( col[0], col[1], col[2] )


  # ##### começa a escrever equipamentos das composições ###################################

    dfr_equipamentos_ = projeto.obter_dfr_equipamentos_servicos()
    
    dfr_equipamentos_.to_excel( writer, index=True, sheet_name='equipamento_servico_utilizacao')

    worksheet_dfr_equipamentos_ = writer.sheets['equipamento_servico_utilizacao']
    
    tamanho = dfr_equipamentos_.shape[0]

    area_de_impressao = '$A${}:$J${}'.format(1, tamanho )
    
    # definindo a área de impressão
    worksheet_dfr_equipamentos_.print_area( area_de_impressao )
    # dimensionando as páginas largura por extensão
    worksheet_dfr_equipamentos_.fit_to_pages(1, tamanho)
    # rotacionando a página
    worksheet_dfr_equipamentos_.set_portrait()
    # definindo papel
    worksheet_dfr_equipamentos_.set_paper(9) # índice 9 (papel A4) vem da documentação da biblioteca xlsxwriter
    # centralizando horizontalmente a tabela na página
    worksheet_dfr_equipamentos_.center_horizontally()
    # repetindo primeira linha
    worksheet_dfr_equipamentos_.repeat_rows(0)

    # formatando colunas
    colunas = [ ('A:A', 0.5*modulo, format_centro), ('B:D', 2.0*modulo, format_centro), ('E:E', 8.5*modulo, format_esquerda), ('F:J', 2.5*modulo, format_valor_10decimais) ]
    for col in colunas:
        worksheet_dfr_equipamentos_.set_column( col[0], col[1], col[2] )


# ##### começa a escrever mão de obra das composições ###################################

    dfr_mao_de_obra_ = projeto.obter_dfr_mao_de_obra_servicos()
    
    dfr_mao_de_obra_.to_excel( writer, index=True, sheet_name='mao_de_obra_servico_utilizacao')

    worksheet_dfr_mao_de_obra_ = writer.sheets['mao_de_obra_servico_utilizacao']
    
    tamanho = dfr_mao_de_obra_.shape[0]

    area_de_impressao = '$A${}:$G${}'.format(1, tamanho )
    
    # definindo a área de impressão
    worksheet_dfr_mao_de_obra_.print_area( area_de_impressao )
    # dimensionando as páginas largura por extensão
    worksheet_dfr_mao_de_obra_.fit_to_pages(1, tamanho)
    # rotacionando a página
    worksheet_dfr_mao_de_obra_.set_portrait()
    # definindo papel
    worksheet_dfr_mao_de_obra_.set_paper(9) # índice 9 (papel A4) vem da documentação da biblioteca xlsxwriter
    # centralizando horizontalmente a tabela na página
    worksheet_dfr_mao_de_obra_.center_horizontally()
    # repetindo primeira linha
    worksheet_dfr_mao_de_obra_.repeat_rows(0)

    # formatando colunas
    colunas = [ ('A:A', 0.5*modulo, format_centro), ('B:D', 2.0*modulo, format_centro), ('E:E', 8.5*modulo, format_esquerda), ('F:G', 2.5*modulo, format_valor_10decimais) ]
    for col in colunas:
        worksheet_dfr_mao_de_obra_.set_column( col[0], col[1], col[2] )


# ##### começa a escrever materiais das composições ###################################

    dfr_materiais_ = projeto.obter_dfr_materiais_servicos()
    
    dfr_materiais_.to_excel( writer, index=True, sheet_name='material_servico_utilizacao')

    worksheet_dfr_materiais_ = writer.sheets['material_servico_utilizacao']
    
    tamanho = dfr_materiais_.shape[0]

    area_de_impressao = '$A${}:$G${}'.format(1, tamanho )
    
    # definindo a área de impressão
    worksheet_dfr_materiais_.print_area( area_de_impressao )
    # dimensionando as páginas largura por extensão
    worksheet_dfr_materiais_.fit_to_pages(1, tamanho)
    # rotacionando a página
    worksheet_dfr_materiais_.set_portrait()
    # definindo papel
    worksheet_dfr_materiais_.set_paper(9) # índice 9 (papel A4) vem da documentação da biblioteca xlsxwriter
    # centralizando horizontalmente a tabela na página
    worksheet_dfr_materiais_.center_horizontally()
    # repetindo primeira linha
    worksheet_dfr_materiais_.repeat_rows(0)

    # formatando colunas
    colunas = [ ('A:A', 0.5*modulo, format_centro), ('B:D', 2.0*modulo, format_centro), ('E:E', 8.5*modulo, format_esquerda), ('F:G', 2.5*modulo, format_valor_10decimais) ]
    for col in colunas:
        worksheet_dfr_materiais_.set_column( col[0], col[1], col[2] )


# ##### começa a escrever serviços do projeto ###################################

    dfr_servico_ = projeto.obter_dfr_servicos_projeto()
    
    dfr_servico_.to_excel( writer, index=True, sheet_name='servico')

    worksheet_dfr_servico_ = writer.sheets['servico']
    
    tamanho = dfr_servico_.shape[0]

    area_de_impressao = '$A${}:$G${}'.format(1, tamanho )
    
    # definindo a área de impressão
    worksheet_dfr_servico_.print_area( area_de_impressao )
    # dimensionando as páginas largura por extensão
    worksheet_dfr_servico_.fit_to_pages(1, tamanho)
    # rotacionando a página
    worksheet_dfr_servico_.set_portrait()
    # definindo papel
    worksheet_dfr_servico_.set_paper(9) # índice 9 (papel A4) vem da documentação da biblioteca xlsxwriter
    # centralizando horizontalmente a tabela na página
    worksheet_dfr_servico_.center_horizontally()
    # repetindo primeira linha
    worksheet_dfr_servico_.repeat_rows(0)

    # formatando colunas
    colunas = [ ('A:A', 0.5*modulo, format_centro), ('B:B', 2.0*modulo, format_centro), ('C:C', 10.0*modulo, format_esquerda), ('D:D', 1.0*modulo, format_centro), ('E:F', 2.5*modulo, format_valor_4decimais), ('G:G', 2.5*modulo, format_valor_2decimais) ]
    for col in colunas:
        worksheet_dfr_servico_.set_column( col[0], col[1], col[2] )

    writer.save()

