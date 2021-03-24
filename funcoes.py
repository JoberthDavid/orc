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
from formatacao_dados import (
                        Codigo,
                        FormatacaoComposicao,
                        FormatacaoConsumoDesdobrado,
                    )


def carregar_data_frame(csv):
    # Abrir um arquivo csv a partir do Pandas
    data_frame_csv = pd.read_csv(csv, encoding='utf-8' )# encoding='ISO-8859-1' )
    return data_frame_csv

def tratar_data_frame(data_frame, lista=list()):
    # Renomeando os nomes das colunas com o método columns
    data_frame.columns = ['Origem', 'Estado', 'Publicacao'] + lista
    # Excluir a última coluna que está com caracteres de tabulação
    if lista[-1] == 'NONE':
        data_frame.pop( 'NONE' )
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
    obj_codigo = Codigo()
    dicionario = projeto.obter_dfr_composicao()
    numero_de_composicoes = len( dicionario )
    numero_linhas = numero_de_composicoes * maximo_linhas_na_composicao
    area_de_impressao = '$D${}:$N${}'.format(1, numero_de_composicoes * maximo_linhas_na_composicao )
    area_formatacao_condicional = '$D${}:$N${}'.format(1, numero_de_composicoes * maximo_linhas_na_composicao )

    # contador para as linhas das composições
    linha_inicio = 1

    # cria um objeto Excel
    writer = pd.ExcelWriter( '.'.join( (arquivo,'xlsx' ) ) , engine='xlsxwriter' )

    modulo = 10

    formato_consumo_desdobrado = FormatacaoConsumoDesdobrado( writer )  
    formato = FormatacaoComposicao( writer )

    for _df in dicionario.values():
        # dfr_insumo
        _df.dfr_insumo.to_excel( writer, startrow=( linha_inicio ), sheet_name='composicao', index=True )

        worksheet_dfr_composicao = writer.sheets['composicao']
        
        configurar_impressao(worksheet_dfr_composicao, area_de_impressao, numero_de_composicoes)

        # acrescentando a linha com dados da composição
        linhas = [ ( 'D', _df.composicao.codigo, formato.codigo_composicao ), ( 'E', _df.composicao.descricao, formato.descricao_composicao ), ( 'L', _df.composicao.produtividade, formato.produtividade_composicao ), ( 'M', _df.composicao.unidade, formato.unidade_composicao ), ( 'N', complemento, formato.onerado_composicao) ]
        for lin in linhas:
            worksheet_dfr_composicao.write( ''.join( (lin[0], str(linha_inicio)) ), lin[1], lin[2])

        # formatando colunas
        colunas = [ ( 'B:D', modulo, formato.codigo_insumo ), ( 'E:E', 12.0*modulo, formato.descricao_insumo), ( 'F:F', 1.5*modulo, formato.codigo_insumo ), ( 'G:G', modulo, formato.utilizacao_insumo), ( 'H:H', modulo, formato.codigo_insumo ), ( 'I:I', modulo, formato.quantidade_insumo), ( 'J:J', modulo, formato.utilizacao_insumo), ( 'K:N', 2.6*modulo, formato.custo_insumo) ]
        for col in colunas:
            worksheet_dfr_composicao.set_column( col[0], col[1], col[2] )

        # formatando as linhas de custos horários e unitários
        criterios = [ ( '"{}"'.format( obj_codigo.horario ), formato.custo_horario_total ), ( '"{}"'.format( obj_codigo.unitario ), formato.custo_unitario_total ), ( '"{}"'.format( obj_codigo.execucao ),formato.custo_horario_total ), ( '"{}"'.format( obj_codigo.direto_total ), formato.custo_unitario_direto_total), ( '"{}"'.format( obj_codigo.preco_unitario ), formato.preco_unitario_total) ]
        for cri in criterios:
            token = 'INDEX($B${inicio}:$N${fim},ROW(),3)={token}'.format(inicio=1, fim=numero_linhas, token=cri[0] )
            worksheet_dfr_composicao.conditional_format( area_formatacao_condicional, {'type':'formula','criteria': token,'format':cri[1]} )

        # formatação condicional código com ho, un e un_dt
        token = '$D${inicio}:$D${fim}'.format(inicio=1, fim=numero_linhas)
        condicoes = [ ( obj_codigo.horario, formato.nao_mostrar ), ( obj_codigo.direto_total, formato.nao_mostrar ), ( obj_codigo.execucao, formato.nao_mostrar ), ( obj_codigo.unitario, formato.nao_mostrar ), ( obj_codigo.preco_unitario, formato.nao_mostrar)]
        for con in condicoes:
            worksheet_dfr_composicao.conditional_format( token, {'type':'text','criteria':'containing','value': con[0],'format':con[1]} )
        

        linha_inicio = linha_inicio + maximo_linhas_na_composicao

    # ##### começa a escrever equipamentos das composições ###################################
   
    dfr_equipamento = projeto.obter_dfr_equipamento()

    dfr_equipamento.to_excel( writer, index=False, sheet_name='equipamento_custo' )

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
    colunas = [ ( 'A:E', 1.2*modulo, formato.codigo_insumo ), ( 'F:F', 8.0*modulo, formato.descricao_insumo), ( 'G:G', modulo, formato.codigo_insumo ), ( 'H:I', 2.5*modulo, formato.custo_insumo) ]
    for col in colunas:
        worksheet_dfr_equipamento.set_column( col[0], col[1], col[2] )

    # ##### começa a escrever mão de obra das composições ###################################

    dfr_mao_de_obra = projeto.obter_dfr_mao_de_obra()

    dfr_mao_de_obra.to_excel( writer, index=False, sheet_name='mao_de_obra_custo' )

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
    colunas = [ ( 'A:E', 1.2*modulo, formato.codigo_insumo ), ( 'F:F', 8.0*modulo, formato.descricao_insumo), ( 'G:G', modulo, formato.codigo_insumo ), ( 'H:H', 2.5*modulo, formato.custo_insumo) ]
    for col in colunas:
        worksheet_dfr_mao_de_obra.set_column( col[0], col[1], col[2] )


   # ##### começa a escrever materiais das composições ###################################

    dfr_material = projeto.obter_dfr_material()

    dfr_material.to_excel( writer, index=False, sheet_name='material_custo' )

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
    colunas = [ ( 'A:E', 1.2*modulo, formato.codigo_insumo ), ( 'F:F', 8.0*modulo, formato.descricao_insumo), ( 'G:G', modulo, formato.codigo_insumo ), ( 'H:H', 2.5*modulo, formato.custo_insumo) ]
    for col in colunas:
        worksheet_dfr_material.set_column( col[0], col[1], col[2] )

   # ##### começa a escrever transportes das composições ###################################

    dfr_transporte = projeto.obter_dfr_transportes_servicos()
    
    dfr_transporte.to_excel( writer, index=True, sheet_name='transporte_servico_utilizacao' )

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
    colunas = [ ( 'A:A', 0.5*modulo, formato.codigo_insumo ), ( 'B:D', 2.0*modulo, formato.codigo_insumo ), ( 'E:E', 8.5*modulo, formato.descricao_insumo), ( 'F:G', 1.5*modulo, formato.codigo_insumo ), ( 'H:H', 2.5*modulo, formato_consumo_desdobrado.formatado) ]
    for col in colunas:
        worksheet_dfr_transporte.set_column( col[0], col[1], col[2] )


  # ##### começa a escrever equipamentos das composições ###################################

    dfr_equipamentos_ = projeto.obter_dfr_equipamentos_servicos()
    
    dfr_equipamentos_.to_excel( writer, index=True, sheet_name='equipamento_servico_utilizacao' )

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
    colunas = [ ( 'A:A', 0.5*modulo, formato.codigo_insumo ), ( 'B:D', 2.0*modulo, formato.codigo_insumo ), ( 'E:E', 8.5*modulo, formato.descricao_insumo), ( 'F:J', 2.5*modulo, formato_consumo_desdobrado.formatado) ]
    for col in colunas:
        worksheet_dfr_equipamentos_.set_column( col[0], col[1], col[2] )


# ##### começa a escrever mão de obra das composições ###################################

    dfr_mao_de_obra_ = projeto.obter_dfr_mao_de_obra_servicos()
    
    dfr_mao_de_obra_.to_excel( writer, index=True, sheet_name='mao_de_obra_servico_utilizacao' )

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
    colunas = [ ( 'A:A', 0.5*modulo, formato.codigo_insumo ), ( 'B:D', 2.0*modulo, formato.codigo_insumo ), ( 'E:E', 8.5*modulo, formato.descricao_insumo), ( 'F:G', 2.5*modulo, formato_consumo_desdobrado.formatado) ]
    for col in colunas:
        worksheet_dfr_mao_de_obra_.set_column( col[0], col[1], col[2] )


# ##### começa a escrever materiais das composições ###################################

    dfr_materiais_ = projeto.obter_dfr_materiais_servicos()
    
    dfr_materiais_.to_excel( writer, index=True, sheet_name='material_servico_utilizacao' )

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
    colunas = [ ( 'A:A', 0.5*modulo, formato.codigo_insumo ), ( 'B:D', 2.0*modulo, formato.codigo_insumo ), ( 'E:E', 8.5*modulo, formato.descricao_insumo), ( 'F:G', 2.5*modulo, formato_consumo_desdobrado.formatado) ]
    for col in colunas:
        worksheet_dfr_materiais_.set_column( col[0], col[1], col[2] )


# ##### começa a escrever serviços do projeto ###################################

    dfr_servico_ = projeto.obter_dfr_servicos_projeto()
    
    dfr_servico_.to_excel( writer, index=True, sheet_name='servico' )

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
    colunas = [ ( 'A:A', 0.5*modulo, formato.codigo_insumo ), ( 'B:B', 2.0*modulo, formato.codigo_insumo ), ( 'C:C', 10.0*modulo, formato.descricao_insumo), ( 'D:D', 1.0*modulo, formato.codigo_insumo ), ( 'E:F', 2.5*modulo, formato.custo_insumo), ( 'G:G', 2.5*modulo, formato.utilizacao_insumo) ]
    for col in colunas:
        worksheet_dfr_servico_.set_column( col[0], col[1], col[2] )

    writer.save()

