from formatacao_dados import Formatacao


class FormatacaoComposicaoDMT(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(1)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoOnerado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.cor_letra( 'red' )
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoNaoMostrar(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.cor_letra( 'white' )
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoProdutividade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.algarismo_significativo(5)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoDescricaoComposicao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoDescricaoInsumo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoCusto(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(4)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoUtilizacao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(2)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoConsumoDesdobrado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(10)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoQuantidade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(5)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoUnidadeComposicao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoCodigoComposicao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoCodigoInsumo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
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
        obj_formato_nao_mostrar = FormatacaoComposicaoNaoMostrar( writer )
        obj_formato_codigo_composicao = FormatacaoComposicaoCodigoComposicao( writer )
        obj_formato_descricao_composicao = FormatacaoComposicaoDescricaoComposicao( writer )
        obj_formato_produtividade_composicao = FormatacaoComposicaoProdutividade( writer )
        obj_formato_unidade_composicao = FormatacaoComposicaoUnidadeComposicao( writer )
        obj_formato_onerado_composicao = FormatacaoComposicaoOnerado( writer )
        obj_formato_codigo_insumo = FormatacaoComposicaoCodigoInsumo( writer )
        obj_formato_descricao_insumo = FormatacaoComposicaoDescricaoInsumo( writer )
        obj_formato_utilizacao_insumo = FormatacaoComposicaoUtilizacao( writer )
        obj_formato_quantidade_insumo = FormatacaoComposicaoQuantidade( writer )
        obj_formato_custo_insumo = FormatacaoComposicaoCusto( writer )
        obj_formato_custo_horario_total = FormatacaoComposicaoCustoHorarioTotal( writer )
        obj_formato_custo_unitario_total = FormatacaoComposicaoCustoUnitarioTotal( writer )
        obj_formato_custo_unitario_direto_total = FormatacaoComposicaoCustoUnitarioDiretoTotal( writer )
        obj_formato_preco_unitario_total = FormatacaoComposicaoPrecoUnitarioTotal( writer )
        self.nao_mostrar = obj_formato_nao_mostrar.formatado
        self.codigo_composicao = obj_formato_codigo_composicao.formatado
        self.descricao_composicao = obj_formato_descricao_composicao.formatado
        self.produtividade_composicao = obj_formato_produtividade_composicao.formatado
        self.unidade_composicao = obj_formato_unidade_composicao.formatado
        self.onerado_composicao = obj_formato_onerado_composicao.formatado
        self.codigo_insumo = obj_formato_codigo_insumo.formatado
        self.descricao_insumo = obj_formato_descricao_insumo.formatado
        self.utilizacao_insumo = obj_formato_utilizacao_insumo.formatado
        self.quantidade_insumo = obj_formato_quantidade_insumo.formatado
        self.custo_insumo = obj_formato_custo_insumo.formatado
        self.custo_horario_total = obj_formato_custo_horario_total.formatado
        self.custo_unitario_total = obj_formato_custo_unitario_total.formatado
        self.custo_unitario_direto_total = obj_formato_custo_unitario_direto_total.formatado
        self.preco_unitario_total = obj_formato_preco_unitario_total.formatado