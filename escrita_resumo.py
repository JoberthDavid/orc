from formatacao_dados import Formatacao
from escrita_composicao import FormatacaoComposicaoDMT


class FormatacaoResumoID(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = 'A:A'
        self.largura = 0.5 * self.modulo


class FormatacaoResumoGrupo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 0.8 * self.modulo


class FormatacaoResumoOrigem(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 1.0 * self.modulo


class FormatacaoResumoEstado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 1.0 * self.modulo


class FormatacaoResumoPublicacao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 1.0 * self.modulo


class FormatacaoResumoCodigo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 1.5 * self.modulo


class FormatacaoResumoDescricao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 12.0 * self.modulo


class FormatacaoResumoUnidade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 0.8 * self.modulo


class FormatacaoResumoQuantidade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_significativo(4)
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 2.0 * self.modulo


class FormatacaoResumoPrecoUnitario(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_significativo(4)
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 2.5 * self.modulo


class FormatacaoResumoCustoTotal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_significativo(2)
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 2.5 * self.modulo


class FormatacaoResumoQuantidadeDesdobrada(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_significativo(10)
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 2.0 * self.modulo


class FormatacaoResumoCustoTotalDesdobrado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_significativo(10)
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 2.5 * self.modulo


class FormatacaoResumoPercentual(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_percentual()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 2.5 * self.modulo


class FormatacaoEscrita:

    def __init__( self, writer ) -> None:
        self.writer = writer
        self.obj_formatacao_id = FormatacaoResumoID( writer )
        self.obj_formatacao_grupo = FormatacaoResumoGrupo( writer )
        self.obj_formatacao_origem = FormatacaoResumoOrigem( writer )
        self.obj_formatacao_estado = FormatacaoResumoEstado( writer )
        self.obj_formatacao_publicacao = FormatacaoResumoPublicacao( writer )
        self.obj_formatacao_servico = FormatacaoResumoCodigo( writer )
        self.obj_formatacao_composicao = FormatacaoResumoCodigo( writer )
        self.obj_formatacao_codigo = FormatacaoResumoCodigo( writer )
        self.obj_formatacao_descricao = FormatacaoResumoDescricao( writer )
        self.obj_formatacao_unidade = FormatacaoResumoUnidade( writer )
        self.obj_formatacao_quantidade = FormatacaoResumoQuantidade( writer )
        self.obj_formatacao_preco_unitario = FormatacaoResumoPrecoUnitario( writer )
        self.obj_formatacao_custo_total = FormatacaoResumoCustoTotal( writer )
        self.obj_formatacao_quantidade_desdobrada = FormatacaoResumoQuantidadeDesdobrada( writer )
        self.obj_formatacao_dmt = FormatacaoComposicaoDMT( writer )
        self.obj_formatacao_momento_transporte_unitario = FormatacaoResumoQuantidadeDesdobrada( writer )
        self.obj_formatacao_momento_transporte_total = FormatacaoResumoQuantidadeDesdobrada( writer )
        self.obj_formatacao_custo_total_desdobrado = FormatacaoResumoCustoTotalDesdobrado( writer )
        self.obj_formatacao_percentual = FormatacaoResumoPercentual( writer )
        self.obj_formatacao_percentual_acumulado = FormatacaoResumoPercentual( writer )

class FormatacaoEscritaCustoEquipamento(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'CUSTO UNITÁRIO EQUIPAMENTO'
        self.entrada_area_de_impressao = '$A${}:$J${}'
        self.obj_formatacao_grupo.coluna = 'B:B'
        self.obj_formatacao_origem.coluna = 'C:C'
        self.obj_formatacao_estado.coluna = 'D:D'
        self.obj_formatacao_publicacao.coluna = 'E:E'
        self.obj_formatacao_codigo.coluna = 'F:F'
        self.obj_formatacao_descricao.coluna = 'G:G'
        self.obj_formatacao_unidade.coluna = 'H:H'
        self.obj_formatacao_preco_unitario.coluna = 'I:J'
        self.obj_formatacao_descricao.largura = 14 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_grupo,
                self.obj_formatacao_origem,
                self.obj_formatacao_estado,
                self.obj_formatacao_publicacao,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_unidade,
                self.obj_formatacao_preco_unitario,
            ]
        self.orientacao_retrato = False


class FormatacaoEscritaCustoMaoDeObra(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'CUSTO UNITÁRIO MÃO DE OBRA'
        self.entrada_area_de_impressao = '$A${}:$I${}'
        self.obj_formatacao_grupo.coluna = 'B:B'
        self.obj_formatacao_origem.coluna = 'C:C'
        self.obj_formatacao_estado.coluna = 'D:D'
        self.obj_formatacao_publicacao.coluna = 'E:E'
        self.obj_formatacao_codigo.coluna = 'F:F'
        self.obj_formatacao_descricao.coluna = 'G:G'
        self.obj_formatacao_unidade.coluna = 'H:H'
        self.obj_formatacao_preco_unitario.coluna = 'I:I'
        self.obj_formatacao_descricao.largura = 16.5 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_grupo,
                self.obj_formatacao_origem,
                self.obj_formatacao_estado,
                self.obj_formatacao_publicacao,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_unidade,
                self.obj_formatacao_preco_unitario,
            ]
        self.orientacao_retrato = False


class FormatacaoEscritaCustoMaterial(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'CUSTO UNITÁRIO MATERIAL'
        self.entrada_area_de_impressao = '$A${}:$I${}'
        self.obj_formatacao_grupo.coluna = 'B:B'
        self.obj_formatacao_origem.coluna = 'C:C'
        self.obj_formatacao_estado.coluna = 'D:D'
        self.obj_formatacao_publicacao.coluna = 'E:E'
        self.obj_formatacao_codigo.coluna = 'F:F'
        self.obj_formatacao_descricao.coluna = 'G:G'
        self.obj_formatacao_unidade.coluna = 'H:H'
        self.obj_formatacao_preco_unitario.coluna = 'I:I'
        self.obj_formatacao_descricao.largura = 16.5 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_grupo,
                self.obj_formatacao_origem,
                self.obj_formatacao_estado,
                self.obj_formatacao_publicacao,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_unidade,
                self.obj_formatacao_preco_unitario,
            ]
        self.orientacao_retrato = False


class FormatacaoEscritaResumoTransporte(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'TRANSPORTE POR UNIDADE SERVIÇO'
        self.entrada_area_de_impressao = '$A${}:$J${}'
        self.obj_formatacao_servico.coluna = 'B:B'
        self.obj_formatacao_composicao.coluna = 'C:D'
        self.obj_formatacao_descricao.coluna = 'E:E'
        self.obj_formatacao_unidade.coluna = 'F:F'
        self.obj_formatacao_codigo.coluna = 'G:G'
        self.obj_formatacao_quantidade_desdobrada.coluna = 'H:H'
        self.obj_formatacao_dmt.coluna = 'I:I'
        self.obj_formatacao_momento_transporte_unitario.coluna = 'J:J' # momento de transporte unitário
        self.obj_formatacao_momento_transporte_unitario.largura = 2.5 * self.obj_formatacao_momento_transporte_unitario.modulo
        self.obj_formatacao_dmt.largura = 1.0 * self.obj_formatacao_descricao.modulo
        self.obj_formatacao_descricao.largura = 12.9 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [
                self.obj_formatacao_id,
                self.obj_formatacao_servico,
                self.obj_formatacao_composicao,
                self.obj_formatacao_composicao,
                self.obj_formatacao_descricao,
                self.obj_formatacao_unidade,
                self.obj_formatacao_codigo,
                self.obj_formatacao_quantidade_desdobrada,
                self.obj_formatacao_dmt,
                self.obj_formatacao_momento_transporte_unitario,
            ]
        self.orientacao_retrato = False


class FormatacaoEscritaResumoEquipamento(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'EQUIPAMENTO POR UNIDADE SERVIÇO'
        self.entrada_area_de_impressao = '$A${}:$J${}'
        self.obj_formatacao_servico.coluna = 'B:B'
        self.obj_formatacao_composicao.coluna = 'C:C'
        self.obj_formatacao_codigo.coluna = 'D:D'
        self.obj_formatacao_descricao.coluna = 'E:E'
        self.obj_formatacao_quantidade_desdobrada.coluna = 'F:G'
        self.obj_formatacao_preco_unitario.coluna = 'H:I'
        self.obj_formatacao_custo_total_desdobrado.coluna = 'J:J'
        self.obj_formatacao_descricao.largura = 9 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_servico,
                self.obj_formatacao_composicao,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_quantidade_desdobrada,
                self.obj_formatacao_preco_unitario,
                self.obj_formatacao_custo_total_desdobrado
            ]
        self.orientacao_retrato = False


class FormatacaoEscritaResumoMaoDeObra(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'MÃO DE OBRA POR UNIDADE SERVIÇO'
        self.entrada_area_de_impressao = '$A${}:$G${}'
        self.obj_formatacao_servico.coluna = 'B:B'
        self.obj_formatacao_composicao.coluna = 'C:C'
        self.obj_formatacao_codigo.coluna = 'D:D'
        self.obj_formatacao_descricao.coluna = 'E:E'
        self.obj_formatacao_quantidade_desdobrada.coluna = 'F:F'
        self.obj_formatacao_preco_unitario.coluna = 'G:G'
        self.obj_formatacao_descricao.largura = 16.5 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_servico,
                self.obj_formatacao_composicao,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_quantidade_desdobrada,
                self.obj_formatacao_preco_unitario,                
            ]
        self.orientacao_retrato = False


class FormatacaoEscritaResumoMaterial(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'MATERIAL POR UNIDADE SERVIÇO'
        self.entrada_area_de_impressao = '$A${}:$G${}'
        self.obj_formatacao_servico.coluna = 'B:B'
        self.obj_formatacao_composicao.coluna = 'C:C'
        self.obj_formatacao_codigo.coluna = 'D:D'
        self.obj_formatacao_descricao.coluna = 'E:E'
        self.obj_formatacao_quantidade_desdobrada.coluna = 'F:F'
        self.obj_formatacao_preco_unitario.coluna = 'G:G'
        self.obj_formatacao_descricao.largura = 16.5 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_servico,
                self.obj_formatacao_composicao,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_quantidade_desdobrada,
                self.obj_formatacao_preco_unitario,
            ]
        self.orientacao_retrato = False


class FormatacaoEscritaResumoServico(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'RESUMO ORÇAMENTO'
        self.entrada_area_de_impressao = '$A${}:$G${}'
        self.obj_formatacao_servico.coluna = 'B:B'
        self.obj_formatacao_descricao.coluna = 'C:C'
        self.obj_formatacao_unidade.coluna = 'D:D'
        self.obj_formatacao_quantidade.coluna = 'E:E'
        self.obj_formatacao_preco_unitario.coluna = 'F:F'
        self.obj_formatacao_custo_total.coluna = 'G:G'
        self.obj_formatacao_descricao.largura = 16 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_servico,
                self.obj_formatacao_descricao,
                self.obj_formatacao_unidade,
                self.obj_formatacao_quantidade,
                self.obj_formatacao_preco_unitario,
                self.obj_formatacao_custo_total 
            ]
        self.orientacao_retrato = False


class FormatacaoEscritaResumoABCEquipamento(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'ABC EQUIPAMENTO ORÇAMENTO'
        self.entrada_area_de_impressao = '$A${}:$F${}'
        self.obj_formatacao_codigo.coluna = 'B:B'
        self.obj_formatacao_descricao.coluna = 'C:C'
        self.obj_formatacao_custo_total.coluna = 'D:D'
        self.obj_formatacao_percentual.coluna = 'E:E'
        self.obj_formatacao_percentual_acumulado.coluna = 'F:F'
        self.obj_formatacao_descricao.largura = 16.3 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_custo_total,
                self.obj_formatacao_percentual,
                self.obj_formatacao_percentual_acumulado,
            ]
        self.orientacao_retrato = False



class FormatacaoEscritaResumoABCMaoDeObra(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'ABC MÃO DE OBRA ORÇAMENTO'
        self.entrada_area_de_impressao = '$A${}:$F${}'
        self.obj_formatacao_codigo.coluna = 'B:B'
        self.obj_formatacao_descricao.coluna = 'C:C'
        self.obj_formatacao_custo_total.coluna = 'D:D'
        self.obj_formatacao_percentual.coluna = 'E:E'
        self.obj_formatacao_percentual_acumulado.coluna = 'F:F'
        self.obj_formatacao_descricao.largura = 16.3 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_custo_total,
                self.obj_formatacao_percentual,
                self.obj_formatacao_percentual_acumulado,
            ]
        self.orientacao_retrato = False


class FormatacaoEscritaResumoABCMaterial(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'ABC MATERIAL ORÇAMENTO'
        self.entrada_area_de_impressao = '$A${}:$F${}'
        self.obj_formatacao_codigo.coluna = 'B:B'
        self.obj_formatacao_descricao.coluna = 'C:C'
        self.obj_formatacao_custo_total.coluna = 'D:D'
        self.obj_formatacao_percentual.coluna = 'E:E'
        self.obj_formatacao_percentual_acumulado.coluna = 'F:F'
        self.obj_formatacao_descricao.largura = 16.3 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_custo_total,
                self.obj_formatacao_percentual,
                self.obj_formatacao_percentual_acumulado,
            ]
        self.orientacao_retrato = False


class FormatacaoEscritaResumoABCServico(FormatacaoEscrita):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        self.nome_tabela = 'ABC SERVIÇO ORÇAMENTO'
        self.entrada_area_de_impressao = '$A${}:$F${}'
        self.obj_formatacao_codigo.coluna = 'B:B'
        self.obj_formatacao_descricao.coluna = 'C:C'
        self.obj_formatacao_custo_total.coluna = 'D:D'
        self.obj_formatacao_percentual.coluna = 'E:E'
        self.obj_formatacao_percentual_acumulado.coluna = 'F:F'
        self.obj_formatacao_descricao.largura = 16.3 * self.obj_formatacao_descricao.modulo
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_custo_total,
                self.obj_formatacao_percentual,
                self.obj_formatacao_percentual_acumulado,
            ]
        self.orientacao_retrato = False


class FormatacaoCondicionalResumoPercentualAcumulado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.cor_fundo('amarelo-escuro-dnit')
        self.formatado = obj_formatacao.aplicar_formatacao()


class ObjetoCondicionalABCacumulado:

    def __init__( self, writer ) -> None:
        formatacao_condicional = FormatacaoCondicionalResumoPercentualAcumulado( writer )
        self.formatacao_condicional = formatacao_condicional.formatado
        self.criterio = '<='
        self.value = 0.8


class FormatacaoABCCondicionalAcumulado:

    def __init__( self, writer, nome_tabela, numero_linhas=500  ) -> None:
        self.writer = writer
        self.numero_linhas = numero_linhas
        self.nome_tabela = nome_tabela
        self.entrada_area_formatacao = '$F$1:$F${}'.format( numero_linhas )
        self.obj_formato_percentual_acumualdo = ObjetoCondicionalABCacumulado( writer )
        self.lista_entrada_formatacao = [ 
                self.obj_formato_percentual_acumualdo,
            ]


class FormatacaoCondicionalResumoPercentual(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.cor_fundo('azul-claro-dnit')
        self.formatado = obj_formatacao.aplicar_formatacao()


class ObjetoCondicionalABC:

    def __init__( self, writer ) -> None:
        formatacao_condicional = FormatacaoCondicionalResumoPercentual( writer )
        self.formatacao_condicional = formatacao_condicional.formatado
        self.criterio = '>='
        self.value = 0.04


class FormatacaoABCCondicional:

    def __init__( self, writer, nome_tabela, numero_linhas=500 ) -> None:
        self.writer = writer
        self.numero_linhas = numero_linhas
        self.nome_tabela = nome_tabela
        self.entrada_area_formatacao = '$E$1:$E${}'.format( numero_linhas )
        self.obj_formato_percentual_acumualdo = ObjetoCondicionalABC( writer )
        self.lista_entrada_formatacao = [ 
                self.obj_formato_percentual_acumualdo,
            ]