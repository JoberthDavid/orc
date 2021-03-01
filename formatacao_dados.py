class Precisao:
    
    def __init__( self ) -> None:
        self.d2 = 2
        self.d4 = 4
        self.d5 = 5

    def custo( self, valor: float ) -> float:
        return round( valor, self.d4 )

    def monetario( self, valor: float ) -> float:
        return round( valor, self.d2 )

    def utilizacao( self, valor: float ) -> float:
        return round( valor, self.d5 )


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