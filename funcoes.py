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
                        Escrita,
                    )
from escrita_resumo import (
                        FormatacaoEscritaCustoEquipamento,
                        FormatacaoEscritaCustoMaoDeObra,
                        FormatacaoEscritaCustoMaterial,
                        FormatacaoEscritaResumoTransporte,
                        FormatacaoEscritaResumoEquipamento,
                        FormatacaoEscritaResumoMaoDeObra,
                        FormatacaoEscritaResumoMaterial,
                        FormatacaoEscritaResumoServico,
                    )
from escrita_composicao import  (
                        FormatacaoComposicao,
                        FormatoComposicaoCabecalho,
                    )


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

    formato = FormatacaoComposicao( writer )
    formato_cabecalho = FormatoComposicaoCabecalho( writer )

    for _df in dicionario.values():
        # dfr_insumo
        _df.dfr_insumo.to_excel( writer, startrow=( linha_inicio ), sheet_name='composicao', index=True )
        
        configurar_impressao( writer.sheets['composicao'], area_de_impressao, numero_de_composicoes )

        # acrescentando a linha com dados da composição
        parametros = [ 
                ( formato_cabecalho.obj_formato_codigo.coluna, _df.composicao.codigo, formato_cabecalho.obj_formato_codigo.formatado ),
                ( formato_cabecalho.obj_formato_descricao.coluna, _df.composicao.descricao, formato_cabecalho.obj_formato_descricao.formatado ),
                ( formato_cabecalho.obj_formato_produtividade.coluna, _df.composicao.produtividade, formato_cabecalho.obj_formato_produtividade.formatado ),
                ( formato_cabecalho.obj_formato_unidade.coluna, _df.composicao.unidade, formato_cabecalho.obj_formato_unidade.formatado ),
                ( formato_cabecalho.obj_formato_onerado.coluna, complemento, formato_cabecalho.obj_formato_onerado.formatado ),
            ]
        for par in parametros:
            writer.sheets['composicao'].write( ''.join( (par[0], str(linha_inicio)) ), par[1], par[2] )

        linha_inicio = linha_inicio + maximo_linhas_na_composicao

    # formatando colunas
    colunas = [
                formato.obj_formato_composicao_principal,
                formato.obj_formato_composicao_grupo,
                formato.obj_formato_composicao_codigo_insumo,
                formato.obj_formato_composicao_descricao_insumo,
                formato.obj_formato_composicao_item_transportado,
                formato.obj_formato_composicao_dmt,
                formato.obj_formato_composicao_unidade_insumo,
                formato.obj_formato_composicao_quantidade,
                formato.obj_formato_composicao_utilizacao,
                formato.obj_formato_composicao_custo_produtivo,
                formato.obj_formato_composicao_custo_improdutivo,
                formato.obj_formato_composicao_preco_unitario,
                formato.obj_formato_composicao_custo_total,
            ]
    for col in colunas:
        writer.sheets['composicao'].set_column( col.coluna, col.largura, col.formatado )

    # # formatando as linhas de custos horários e unitários
    # criterios = [
    #             ( '"{}"'.format( obj_codigo.horario ),formato.custo_horario_total ),
    #             ( '"{}"'.format( obj_codigo.unitario ), formato.custo_unitario_total ),
    #             ( '"{}"'.format( obj_codigo.execucao ),formato.custo_horario_total ),
    #             ( '"{}"'.format( obj_codigo.direto_total ), formato.custo_unitario_direto_total),
    #             ( '"{}"'.format( obj_codigo.preco_unitario ), formato.preco_unitario_total)
    #         ]
    # for cri in criterios:
    #     token = 'INDEX($B${inicio}:$N${fim},ROW(),3)={token}'.format(inicio=1, fim=numero_linhas, token=cri[0] )
    #     worksheet_dfr_composicao.conditional_format( area_formatacao_condicional, {'type':'formula','criteria': token,'format':cri[1]} )

    # # formatação condicional código com ho, un e un_dt
    # token = '$D${inicio}:$D${fim}'.format(inicio=1, fim=numero_linhas)
    # condicoes = [ 
    #             ( obj_codigo.horario, formato.nao_mostrar ),
    #             ( obj_codigo.direto_total, formato.nao_mostrar ),
    #             ( obj_codigo.execucao, formato.nao_mostrar ),
    #             ( obj_codigo.unitario, formato.nao_mostrar ),
    #             ( obj_codigo.preco_unitario, formato.nao_mostrar)
    #         ]
    # for con in condicoes:
    #     worksheet_dfr_composicao.conditional_format( token, {'type':'text','criteria':'containing','value': con[0],'format':con[1]} )
    

    # ##### começa a escrever custos de equipamentos das composições ###################################
   
    dfr_equipamento_custo = projeto.obter_dfr_equipamento()
    obj_format = FormatacaoEscritaCustoEquipamento( writer )
    obj_escrita = Escrita( dfr_equipamento_custo, obj_format )
    writer = obj_escrita.obter_escritor_configurado()

    # ##### começa a escrever custos de mão de obra das composições ###################################

    dfr_mao_de_obra_custo = projeto.obter_dfr_mao_de_obra()
    obj_format = FormatacaoEscritaCustoMaoDeObra( writer )
    obj_escrita = Escrita( dfr_mao_de_obra_custo, obj_format )
    writer = obj_escrita.obter_escritor_configurado()

   # ##### começa a escrever custos de materiais das composições ###################################

    dfr_material_custo = projeto.obter_dfr_material()
    obj_format = FormatacaoEscritaCustoMaterial( writer )
    obj_escrita = Escrita( dfr_material_custo, obj_format )
    writer = obj_escrita.obter_escritor_configurado()

   # ##### começa a escrever utilizações de transportes das composições ###################################

    dfr_transporte_utilizacao = projeto.obter_dfr_transportes_servicos()
    obj_format = FormatacaoEscritaResumoTransporte( writer )
    obj_escrita = Escrita( dfr_transporte_utilizacao, obj_format )
    writer = obj_escrita.obter_escritor_configurado()

  # ##### começa a escrever utilizações de equipamentos das composições ###################################

    dfr_equipamento_utilizacao = projeto.obter_dfr_equipamentos_servicos()
    obj_format = FormatacaoEscritaResumoEquipamento( writer )
    obj_escrita = Escrita( dfr_equipamento_utilizacao, obj_format )
    writer = obj_escrita.obter_escritor_configurado()

# ##### começa a escrever utilizações de mão de obra das composições ###################################

    dfr_mao_de_obra_utilizacao = projeto.obter_dfr_mao_de_obra_servicos()
    obj_format = FormatacaoEscritaResumoMaoDeObra( writer )
    obj_escrita = Escrita( dfr_mao_de_obra_utilizacao, obj_format )
    writer = obj_escrita.obter_escritor_configurado()

# ##### começa a escrever utilizações de materiais das composições ###################################

    dfr_material_utilizacao = projeto.obter_dfr_materiais_servicos()
    obj_format = FormatacaoEscritaResumoMaterial( writer )
    obj_escrita = Escrita( dfr_material_utilizacao, obj_format )
    writer = obj_escrita.obter_escritor_configurado()

# ##### começa a escrever resumo de serviços do projeto ###################################

    dfr_servico_resumo = projeto.obter_dfr_servicos_projeto()
    obj_format = FormatacaoEscritaResumoServico( writer )
    obj_escrita = Escrita( dfr_servico_resumo, obj_format )
    writer = obj_escrita.obter_escritor_configurado()

    writer.save()