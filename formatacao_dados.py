class Precisao:
    
    def __init__( self ) -> None:
        self._02_algarismos = 2
        self._04_algarismos = 4
        self._05_algarismos = 5
        self._10_algarismos = 10

    def custo( self, valor: float ) -> float:
        return round( valor, self._04_algarismos )

    def monetario( self, valor: float ) -> float:
        return round( valor, self._02_algarismos )

    def utilizacao( self, valor: float ) -> float:
        return round( valor, self._05_algarismos )

    def utilizacao_transporte( self, valor: float ) -> float:
        return round( valor, self._10_algarismos )

    def utilizacao_equipamento( self, valor: float ) -> float:
        return round( valor, self._10_algarismos )

    def utilizacao_material( self, valor: float ) -> float:
        return round( valor, self._10_algarismos )

    def utilizacao_mao_de_obra( self, valor: float ) -> float:
        return round( valor, self._10_algarismos )


class Formatacao:

    def __init__( self, writer ):
        self.workbook = writer.book
        self.dicionario_formatacao = dict()
        self.dicionario_formatacao['italic'] = False
        self.dicionario_formatacao['bold'] = False
        self.dicionario_cor = {
                    'black' : '#000000',
                    'blue' : '#0000FF',
                    'brown' : '#800000',
                    'cyan' : '#00FFFF',
                    'green' : '#008000',
                    'lime' : '#00FF00',
                    'magenta' : '#FF00FF',
                    'navy' : '#000080',
                    'orange' : '#FF6600',
                    'pink' : '#FF00FF',
                    'purple' : '#800080',
                    'red' : '#FF0000',
                    'light-gray' : '#DCDCDC',
                    'dark-gray' : '#A9A9A9',
                    'light-blue' : '#B0C4DE',
                    'white' : 'white',
                    'yellow' : '#FFFF00',
                    }

    def alinhamento_centro( self ):
        self.dicionario_formatacao.update( {'align':'center'} )

    def alinhamento_esquerda( self ):
        self.dicionario_formatacao.update( {'align':'left'} )

    def alinhamento_direita( self ):
        self.dicionario_formatacao.update( {'align':'right'} )

    def linha_grade_superior( self ):
        self.dicionario_formatacao.update( {'top':1} )

    def linha_grade_inferior( self ):
        self.dicionario_formatacao.update( {'bottom':1} )

    def cor_letra( self, cor: str='black' ) -> bool:
        if cor in self.dicionario_cor:
            self.dicionario_formatacao.update( {'font_color': self.dicionario_cor[cor] } )
        else:
            self.dicionario_formatacao.update( {'font_color':'black'} )

    def cor_fundo( self, cor: str='white' ):
        if cor in self.dicionario_cor:
            self.dicionario_formatacao.update( {'bg_color': self.dicionario_cor[cor] } )
        else:
            self.dicionario_formatacao.update( {'bg_color':'white'} )

    def algarismo_significativo( self, numero: int):
        representacao_valor = '###,###,###,##0'
        if numero > 0:
            representacao_valor = representacao_valor + '.'
            while numero > 0:
                representacao_valor = representacao_valor + '0'
                numero -= 1
        self.dicionario_formatacao.update( {'num_format': representacao_valor} )

    def negrito( self ):
        if self.dicionario_formatacao['bold'] == True:
            valor = False
        else:
            valor = True
        self.dicionario_formatacao.update( {'bold': valor} )

    def italico( self ):
        if self.dicionario_formatacao['italic'] == True:
            valor = False
        else:
            valor = True
        self.dicionario_formatacao.update( {'italic': valor} )

    def aplicar_formatacao( self ):
        return self.workbook.add_format( self.dicionario_formatacao )


class FormatacaoDMT(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(1)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoOnerado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.cor_letra( 'red' )
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoNaoMostrar(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.cor_letra( 'white' )
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoProdutividade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.algarismo_significativo(5)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoDescricaoComposicao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoDescricaoInsumo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCusto(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(4)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoUtilizacao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(2)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoConsumoDesdobrado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(10)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoQuantidade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.algarismo_significativo(5)
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoUnidadeComposicao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        obj_formatacao.negrito()
        obj_formatacao.italico()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCodigoComposicao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.negrito()
        obj_formatacao.italico()
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCodigoInsumo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCustoHorarioTotal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.negrito()
        obj_formatacao.linha_grade_inferior()
        obj_formatacao.linha_grade_superior()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCustoUnitarioTotal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.cor_fundo( 'light-gray' )
        obj_formatacao.negrito()
        obj_formatacao.linha_grade_inferior()
        obj_formatacao.linha_grade_superior()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoCustoUnitarioDiretoTotal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.negrito()
        obj_formatacao.cor_fundo( 'dark-gray' )
        obj_formatacao.linha_grade_inferior()
        obj_formatacao.linha_grade_superior()
        self.formatado = obj_formatacao.aplicar_formatacao()


class FormatacaoPrecoUnitarioTotal(Formatacao):

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
        obj_formato_nao_mostrar = FormatacaoNaoMostrar( writer )
        obj_formato_codigo_composicao = FormatacaoCodigoComposicao( writer )
        obj_formato_descricao_composicao = FormatacaoDescricaoComposicao( writer )
        obj_formato_produtividade_composicao = FormatacaoProdutividade( writer )
        obj_formato_unidade_composicao = FormatacaoUnidadeComposicao( writer )
        obj_formato_onerado_composicao = FormatacaoOnerado( writer )
        obj_formato_codigo_insumo = FormatacaoCodigoInsumo( writer )
        obj_formato_descricao_insumo = FormatacaoDescricaoInsumo( writer )
        obj_formato_utilizacao_insumo = FormatacaoUtilizacao( writer )
        obj_formato_quantidade_insumo = FormatacaoQuantidade( writer )
        obj_formato_custo_insumo = FormatacaoCusto( writer )
        obj_formato_custo_horario_total = FormatacaoCustoHorarioTotal( writer )
        obj_formato_custo_unitario_total = FormatacaoCustoUnitarioTotal( writer )
        obj_formato_custo_unitario_direto_total = FormatacaoCustoUnitarioDiretoTotal( writer )
        obj_formato_preco_unitario_total = FormatacaoPrecoUnitarioTotal( writer )
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


class Grupo:

    def __init__( self ) -> None:
        self.linha_vazia_inicial = 13
        self.insumo_equipamento = 20
        self.subtotal_horario_equipamento = 22
        self.linha_vazia_equipamento = 23
        self.insumo_mao_de_obra = 30
        self.subtotal_horario_mao_de_obra = 32
        self.linha_vazia_mao_de_obra = 33
        self.subtotal_execucao = 34
        self.subtotal_unitario_execucao = 35
        self.subtotal_unitario_fic = 36
        self.subtotal_unitario_fit = 37
        self.linha_vazia_execucao = 38
        self.insumo_material = 40
        self.subtotal_unitario_material = 42
        self.linha_vazia_material = 43
        self.insumo_atividade_auxiliar = 50
        self.subtotal_unitario_atividade_auxiliar = 52
        self.linha_vazia_atividade_auxiliar = 53
        self.insumo_tempo_fixo = 60
        self.subtotal_unitario_tempo_fixo = 62
        self.linha_vazia_tempo_fixo = 63
        self.insumo_transporte = 70
        self.subtotal_unitario_transporte = 72
        self.linha_vazia_transporte = 73
        self.total_unitario_direto = 80
        self.linha_vazia_unitario_direto = 81
        self.subtotal_unitario_bdi = 90
        self.linha_vazia_bdi = 91
        self.total_preco_unitario = 100


class Codigo:

    def __init__( self ) -> None:
        self.horario = 'ho'
        self.execucao = 'ex'
        self.unitario = 'un'
        self.direto_total = 'dt'
        self.preco_unitario = 'pu'


class ListaColuna:

    def __init__( self ) -> None:
        self.codigo = 'Código'
        self.composicao_principal = 'Composicao_principal'
        self.grupo = 'Grupo_x'
        self.descricao = 'Descrição'
        self.item_transporte = 'Item transportado'
        self.preco_unitario = 'Preço unitário'
        self.quantidade = 'Quantidade'
        self.unidade = 'Unidade'
        self.utilizacao = 'Utilização'
        self.custo_total = 'Custo total'
        self.dmt = 'DMT'
        self.estado = 'Estado'
        self.fic = 'FIC'
        self.produtividade = 'Produtividade'
        self.publicacao = 'Publicacao'
        self.tipo = 'Tipo'
        self.origem = 'Origem'
        self.custo_imp_desonerado = 'Custo improdutivo desonerado'
        self.custo_imp_onerado = 'Custo improdutivo onerado'
        self.custo_improdutivo = 'Custo improdutivo'
        self.custo_pro_desonerado = 'Custo produtivo desonerado'
        self.custo_pro_onerado = 'Custo produtivo onerado'
        self.custo_produtivo = 'Custo produtivo'
        self.none = 'NONE'


class ListaColunaOrigemCP(ListaColuna):

    def __init__( self ) -> None:
        super().__init__()

    def obter_lista( self ) -> list:
        return [
                    self.origem,
                    self.estado,
                    self.publicacao
                ]


class ListaColunaComposicaoDB(ListaColuna):

    def __init__( self ) -> None:
        super().__init__()

    def obter_lista( self ) -> list:
        return [
                    self.composicao_principal,
                    self.fic,
                    self.produtividade,
                    self.tipo,
                    self.none
                ]


class ListaColunaInsumoDB(ListaColuna):

    def __init__( self ) -> None:
        super().__init__()

    def obter_lista( self ) -> list:
        return [
                    self.codigo,
                    self.descricao,
                    self.unidade,
                    self.none
                ]


class ListaColunaApropriacaoDB(ListaColuna):

    def __init__( self ) -> None:
        super().__init__()

    def obter_lista( self ) -> list:
        return [
                    self.composicao_principal,
                    self.codigo,
                    self.quantidade,
                    self.utilizacao,
                    self.item_transporte,
                    'Grupo',
                    self.none
                ]


class ListaColunaCustoInsumoCT(ListaColuna):

    def __init__( self ) -> None:
        super().__init__()

    def obter_lista( self ) -> list:
        return [ 
                    self.codigo,
                    self.custo_pro_onerado,
                    self.custo_imp_onerado,
                    self.custo_pro_desonerado,
                    self.custo_imp_desonerado,
                    self.preco_unitario,
                    'Grupo',
                    self.none
                ]


class ListaColunaComposicaoDF(ListaColuna):

    def __init__( self, onerado: bool ) -> None:
        super().__init__()
        self.custo_produtivo = self.configurar_custo_produtivo( onerado )
        self.custo_improdutivo = self.configurar_custo_improdutivo( onerado )

    def obter_lista( self ) -> list:
        return [ 
                    self.composicao_principal,
                    self.grupo, self.codigo,
                    self.descricao,
                    self.item_transporte,
                    self.dmt,
                    self.unidade,
                    self.quantidade,
                    self.utilizacao,
                    self.custo_produtivo,
                    self.custo_improdutivo,
                    self.preco_unitario,
                    self.custo_total
                ]

    def configurar_custo_produtivo( self, onerado: bool ) -> str:
        if onerado:
            situacao = self.custo_pro_onerado
        else:
            situacao = self.custo_pro_desonerado
        return situacao

    def configurar_custo_improdutivo( self, onerado: bool ) -> str:
        if onerado:
            situacao = self.custo_imp_onerado
        else:
            situacao = self.custo_imp_desonerado
        return situacao