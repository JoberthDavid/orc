from formatacao_dados import Formatacao


    # colunas = [
    #             ( 'B:B', 01.0 * modulo, formato.codigo_composicao ), #
    #             ( 'C:C', 01.0 * modulo, formato.grupo ), #
    #             ( 'D:D', 01.0 * modulo, formato.codigo_insumo ), #
    #             ( 'E:E', 12.0 * modulo, formato.descricao_insumo), #
    #             ( 'F:F', 01.5 * modulo, formato.transportado_insumo ), #
    #             ( 'G:G', 01.0 * modulo, formato.dmt_insumo ), #
    #             ( 'H:H', 01.0 * modulo, formato.unidade_insumo ), #
    #             ( 'I:I', 01.0 * modulo, formato.quantidade_insumo ), #
    #             ( 'J:J', 01.0 * modulo, formato.utilizacao_insumo ), #
    #             ( 'K:K', 02.6 * modulo, formato.custo_produtivo_insumo ), #
    #             ( 'L:L', 02.6 * modulo, formato.custo_improdutivo_insumo ), #
    #             ( 'M:M', 02.6 * modulo, formato.preco_unitario_insumo ), #
    #             ( 'N:N', 02.6 * modulo, formato.custo_total_insumo ), #
    #         ]

class FormatacaoComposicaoCodigoPrincipal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.coluna = 'B:B'
        self.largura = 2.0 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoGrupo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.coluna = 'C:C'
        self.largura = 1.0 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoCodigoInsumo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.coluna = 'D:D'
        self.largura = 1.0 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoDescricaoInsumo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        self.coluna = 'E:E'
        self.largura = 12.0 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoItemTransportado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.coluna = 'F:F'
        self.largura = 1.7 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoDMT(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(1)
        self.coluna = 'G:G'
        self.largura = 1.5 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoUnidade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.coluna = 'H:H'
        self.largura = 1.0 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoQuantidade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(5)
        self.coluna = 'I:I'
        self.largura = 1.0 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoUtilizacao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(2)
        self.coluna = 'J:J'
        self.largura = 1.0 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoCustoProdutivo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(4)
        self.coluna = 'K:K'
        self.largura = 2.7 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoCustoImrodutivo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(4)
        self.coluna = 'L:L'
        self.largura = 2.7 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoPrecoUnitario(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(4)
        self.coluna = 'M:M'
        self.largura = 2.7 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoCustoTotal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(4)
        self.coluna = 'N:N'
        self.largura = 2.7 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


############

class FormatacaoCabecalhoComposicaoOnerado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.cor_letra( 'red' )
        self.coluna = 'N'
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoNaoMostrar(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.cor_letra( 'white' )
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCabecalhoComposicaoProdutividade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.algarismo_significativo(5)
        self.coluna = 'L'
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCabecalhoComposicaoUnidade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        self.coluna = 'M'
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCabecalhoComposicaoDescricao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        self.coluna = 'E'
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCabecalhoComposicaoCodigo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.alinhamento_centro()
        self.coluna = 'D'
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoCustoHorarioTotal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.negrito()
        obj_formatacao.linha_grade_inferior()
        obj_formatacao.linha_grade_superior()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoCustoUnitarioTotal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.cor_fundo( 'light-gray' )
        obj_formatacao.negrito()
        obj_formatacao.linha_grade_inferior()
        obj_formatacao.linha_grade_superior()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoCustoUnitarioDiretoTotal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.negrito()
        obj_formatacao.cor_fundo( 'dark-gray' )
        obj_formatacao.linha_grade_inferior()
        obj_formatacao.linha_grade_superior()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoPrecoUnitarioTotal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao
        obj_formatacao.negrito()
        obj_formatacao.cor_fundo( 'light-blue' )
        obj_formatacao.linha_grade_inferior()
        obj_formatacao.linha_grade_superior()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicao:

    def __init__( self, writer ) -> None:
        self.obj_formato_composicao_principal = FormatacaoComposicaoCodigoPrincipal( writer )
        self.obj_formato_composicao_grupo = FormatacaoComposicaoGrupo( writer )
        self.obj_formato_composicao_codigo_insumo = FormatacaoComposicaoCodigoInsumo( writer )
        self.obj_formato_composicao_descricao_insumo = FormatacaoComposicaoDescricaoInsumo( writer )
        self.obj_formato_composicao_item_transportado = FormatacaoComposicaoItemTransportado( writer )
        self.obj_formato_composicao_dmt = FormatacaoComposicaoDMT( writer )
        self.obj_formato_composicao_unidade_insumo = FormatacaoComposicaoUnidade( writer )
        self.obj_formato_composicao_quantidade = FormatacaoComposicaoQuantidade( writer )
        self.obj_formato_composicao_utilizacao = FormatacaoComposicaoUtilizacao( writer )
        self.obj_formato_composicao_custo_produtivo = FormatacaoComposicaoCustoProdutivo( writer )
        self.obj_formato_composicao_custo_improdutivo = FormatacaoComposicaoCustoImrodutivo( writer )
        self.obj_formato_composicao_preco_unitario = FormatacaoComposicaoPrecoUnitario( writer )
        self.obj_formato_composicao_custo_total = FormatacaoComposicaoCustoTotal( writer )

class FormatoComposicaoCabecalho:

    def __init__( self, writer ) -> None:
        self.obj_formato_codigo = FormatacaoCabecalhoComposicaoCodigo( writer )
        self.obj_formato_descricao = FormatacaoCabecalhoComposicaoDescricao( writer )
        self.obj_formato_produtividade = FormatacaoCabecalhoComposicaoProdutividade( writer )
        self.obj_formato_unidade = FormatacaoCabecalhoComposicaoUnidade( writer )
        self.obj_formato_onerado = FormatacaoCabecalhoComposicaoOnerado( writer )