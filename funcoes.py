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
                        ConfiguraDataFrame,
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
                        FormatacaoComposicaoCabecalho,
                    )


def escrever_arquivo_excel( arquivo, complemento, projeto: Projeto, maximo_linhas_na_composicao):
    # obj_codigo = Codigo()
    dicionario = projeto.obter_dfr_composicao()
    numero_de_composicoes = len( dicionario )
    numero_linhas = numero_de_composicoes * maximo_linhas_na_composicao
    # area_formatacao_condicional = '$D${}:$N${}'.format(1, numero_de_composicoes * maximo_linhas_na_composicao )

    # contador para as linhas das composições
    linha_inicio = 1

    # cria um objeto Excel
    writer = pd.ExcelWriter( '.'.join( (arquivo,'xlsx' ) ) , engine='xlsxwriter' )

    formato = FormatacaoComposicao( writer )
    cabecalho = FormatacaoComposicaoCabecalho( writer )

    for _df in dicionario.values():

        obj_configura_data_frame = ConfiguraDataFrame( _df.dfr_insumo, formato, linha_inicio)

        # acrescentando a linha com dados da composição
        parametros = [ 
                ( cabecalho.obj_formato_codigo.coluna, _df.composicao.codigo, cabecalho.obj_formato_codigo.formatado ),
                ( cabecalho.obj_formato_descricao.coluna, _df.composicao.descricao, cabecalho.obj_formato_descricao.formatado ),
                ( cabecalho.obj_formato_produtividade.coluna, _df.composicao.produtividade, cabecalho.obj_formato_produtividade.formatado ),
                ( cabecalho.obj_formato_unidade.coluna, _df.composicao.unidade, cabecalho.obj_formato_unidade.formatado ),
                ( cabecalho.obj_formato_onerado.coluna, complemento, cabecalho.obj_formato_onerado.formatado ),
            ]
        for par in parametros:
            writer.sheets[ formato.nome_tabela ].write( ''.join( (par[0], str(linha_inicio)) ), par[1], par[2] )

        _df.dfr_insumo = obj_configura_data_frame.obter_data_frame_configurado()

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
        writer.sheets[ formato.nome_tabela ].set_column( col.coluna, col.largura, col.formatado )

    obj_escrita = Escrita( formato, numero_linhas, numero_de_composicoes )
    writer = obj_escrita.obter_escritor_configurado()

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
    obj_format = FormatacaoEscritaCustoEquipamento( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_equipamento(), obj_format)
    dfr_equipamento_custo = obj_configura_data_frame.obter_data_frame_configurado()
    obj_escrita = Escrita( obj_format, dfr_equipamento_custo.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

    ##### começa a escrever custos de mão de obra das composições ###################################
    obj_format = FormatacaoEscritaCustoMaoDeObra( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_mao_de_obra(), obj_format)
    dfr_mao_de_obra_custo = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_mao_de_obra_custo.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

   # ##### começa a escrever custos de materiais das composições ###################################
    obj_format = FormatacaoEscritaCustoMaterial( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_material(), obj_format)
    dfr_material_custo = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_material_custo.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

   # ##### começa a escrever utilizações de transportes das composições ###################################
    obj_format = FormatacaoEscritaResumoTransporte( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_transportes_servicos(), obj_format)
    dfr_transporte_utilizacao = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_transporte_utilizacao.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

  # ##### começa a escrever utilizações de equipamentos das composições ###################################
    obj_format = FormatacaoEscritaResumoEquipamento( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_equipamentos_servicos(), obj_format)
    dfr_equipamento_utilizacao = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_equipamento_utilizacao.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

# ##### começa a escrever utilizações de mão de obra das composições ###################################
    obj_format = FormatacaoEscritaResumoMaoDeObra( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_mao_de_obra_servicos(), obj_format)
    dfr_mao_de_obra_utilizacao = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_mao_de_obra_utilizacao.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

# ##### começa a escrever utilizações de materiais das composições ###################################
    obj_format = FormatacaoEscritaResumoMaterial( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_materiais_servicos(), obj_format)
    dfr_material_utilizacao = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_material_utilizacao.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

# ##### começa a escrever resumo de serviços do projeto ###################################
    obj_format = FormatacaoEscritaResumoServico( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_servicos_projeto(), obj_format)
    dfr_servico_resumo = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_servico_resumo.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

    writer.save()