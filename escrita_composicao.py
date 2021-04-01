from formatacao_dados import Formatacao


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
        self.largura = 1.8 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoDescricaoInsumo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        self.coluna = 'E:E'
        self.largura = 14.0 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoItemTransportado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.coluna = 'F:F'
        self.largura = 1.8 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoDMT(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(1)
        self.coluna = 'G:G'
        self.largura = 0.8 * self.modulo
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoComposicaoUnidade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.coluna = 'H:H'
        self.largura = 0.8 * self.modulo
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
class FormatacaoComposicaoNaoMostrar(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.cor_letra( 'white' )
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCabecalhoComposicaoOnerado(Formatacao):

    def __init__( self, writer, composicao ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.cor_letra( 'red' )
        self.coluna = 'N'
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.conteudo = self.obter_conteudo( composicao.onerado )

    def obter_conteudo( self, onerado ):
        if onerado:
            conteudo = 'Onerado'
        else:
            conteudo = 'Desonerado'
        return conteudo


class FormatacaoCabecalhoComposicaoProdutividade(Formatacao):

    def __init__( self, writer, composicao ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.algarismo_significativo(5)
        self.coluna = 'L'
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.conteudo = composicao.produtividade


class FormatacaoCabecalhoComposicaoUnidade(Formatacao):

    def __init__( self, writer, composicao ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        self.coluna = 'M'
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.conteudo = composicao.unidade


class FormatacaoCabecalhoComposicaoDescricao(Formatacao):

    def __init__( self, writer, composicao ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        self.coluna = 'E'
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.conteudo = composicao.descricao


class FormatacaoCabecalhoComposicaoCodigo(Formatacao):

    def __init__( self, writer, composicao ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.alinhamento_centro()
        self.coluna = 'D'
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.conteudo = composicao.codigo


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
        self.writer = writer
        self.nome_tabela = 'CCU'
        self.entrada_area_de_impressao = '$D${}:$N${}'
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
        self.lista_entrada_formatacao = [ 
                self.obj_formato_composicao_principal,
                self.obj_formato_composicao_grupo,
                self.obj_formato_composicao_codigo_insumo,
                self.obj_formato_composicao_descricao_insumo,
                self.obj_formato_composicao_item_transportado,
                self.obj_formato_composicao_dmt,
                self.obj_formato_composicao_unidade_insumo,
                self.obj_formato_composicao_quantidade,
                self.obj_formato_composicao_utilizacao,
                self.obj_formato_composicao_custo_produtivo,
                self.obj_formato_composicao_custo_improdutivo,
                self.obj_formato_composicao_preco_unitario,
                self.obj_formato_composicao_custo_total,
            ]
        self.orientacao_retrato = False
 

class FormatacaoCabecalho:

    def __init__( self, writer, composicao ) -> None:
        self.writer = writer
        self.nome_tabela = 'CCU'
        self.obj_formato_codigo = FormatacaoCabecalhoComposicaoCodigo( self.writer, composicao )
        self.obj_formato_descricao = FormatacaoCabecalhoComposicaoDescricao( self.writer, composicao )
        self.obj_formato_produtividade = FormatacaoCabecalhoComposicaoProdutividade( self.writer, composicao )
        self.obj_formato_unidade = FormatacaoCabecalhoComposicaoUnidade( self.writer, composicao )
        self.obj_formato_onerado = FormatacaoCabecalhoComposicaoOnerado( self.writer, composicao )
        self.lista_entrada_formatacao = [ 
                self.obj_formato_codigo,
                self.obj_formato_descricao,
                self.obj_formato_produtividade,
                self.obj_formato_unidade,
                self.obj_formato_onerado,
            ]