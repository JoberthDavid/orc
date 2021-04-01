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
                        EscritaCabecalho,
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
                        FormatacaoCabecalho,
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
    writer = pd.ExcelWriter( '{}.{}'.format( arquivo, 'xlsx' ), engine='xlsxwriter' )

    formato = FormatacaoComposicao( writer )

    for _df in dicionario.values():
        obj_configura_data_frame = ConfiguraDataFrame( _df.dfr_insumo, formato, linha_inicio)
        obj_formatacao_cabecalho = FormatacaoCabecalho( writer, _df.composicao )
        obj_escrita = EscritaCabecalho( obj_formatacao_cabecalho, linha_inicio )
        writer = obj_escrita.obter_escritor_configurado()
        _df.dfr_insumo = obj_configura_data_frame.obter_data_frame_configurado()
        linha_inicio = linha_inicio + maximo_linhas_na_composicao

    obj_escrita = Escrita( formato, numero_linhas, numero_de_composicoes )
    writer = obj_escrita.obter_escritor_configurado()


    # # formatando as linhas de custos horários e unitários
    # criterios = [
    #             ( '"{}"'.format( obj_codigo.horario ), formato.custo_horario_total ),
    #             ( '"{}"'.format( obj_codigo.unitario ), formato.custo_unitario_total ),
    #             ( '"{}"'.format( obj_codigo.execucao ), formato.custo_horario_total ),
    #             ( '"{}"'.format( obj_codigo.direto_total ), formato.custo_unitario_direto_total),
    #             ( '"{}"'.format( obj_codigo.preco_unitario ), formato.preco_unitario_total)
    #         ]
    # for cri in criterios:
    #     token = 'INDEX($B${inicio}:$N${fim},ROW(),3)={token}'.format(inicio=1, fim=numero_linhas, token=cri[0] )
    #     writer.sheets[ formato.nome_tabela ].conditional_format( area_formatacao_condicional, {'type':'formula','criteria': token,'format':cri[1]} )

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
    #     writer.sheets[ formato.nome_tabela ].conditional_format( token, {'type':'text','criteria':'containing','value': con[0],'format':con[1]} )
    

    ##### escreve custos de equipamentos das composições
    obj_format = FormatacaoEscritaCustoEquipamento( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_equipamento(), obj_format)
    dfr_equipamento_custo = obj_configura_data_frame.obter_data_frame_configurado()
    obj_escrita = Escrita( obj_format, dfr_equipamento_custo.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

    ##### escreve custos de mão de obra das composições
    obj_format = FormatacaoEscritaCustoMaoDeObra( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_mao_de_obra(), obj_format)
    dfr_mao_de_obra_custo = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_mao_de_obra_custo.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

    ##### escreve custos de materiais das composições
    obj_format = FormatacaoEscritaCustoMaterial( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_material(), obj_format)
    dfr_material_custo = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_material_custo.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

    ##### escreve utilizações de transportes das composições
    obj_format = FormatacaoEscritaResumoTransporte( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_transportes_servicos(), obj_format)
    dfr_transporte_utilizacao = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_transporte_utilizacao.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

    ##### escreve utilizações de equipamentos das composições
    obj_format = FormatacaoEscritaResumoEquipamento( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_equipamentos_servicos(), obj_format)
    dfr_equipamento_utilizacao = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_equipamento_utilizacao.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

    ##### escreve utilizações de mão de obra das composições
    obj_format = FormatacaoEscritaResumoMaoDeObra( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_mao_de_obra_servicos(), obj_format)
    dfr_mao_de_obra_utilizacao = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_mao_de_obra_utilizacao.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

    ##### escreve utilizações de materiais das composições
    obj_format = FormatacaoEscritaResumoMaterial( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_materiais_servicos(), obj_format)
    dfr_material_utilizacao = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_material_utilizacao.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

    ##### escreve resumo de serviços do projeto
    obj_format = FormatacaoEscritaResumoServico( writer )
    obj_configura_data_frame = ConfiguraDataFrame( projeto.obter_dfr_servicos_projeto(), obj_format)
    dfr_servico_resumo = obj_configura_data_frame.obter_data_frame_configurado()    
    obj_escrita = Escrita( obj_format, dfr_servico_resumo.shape[0] )
    writer = obj_escrita.obter_escritor_configurado()

    writer.save()