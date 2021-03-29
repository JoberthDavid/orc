from arquivos import marca_dnit


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
        self.modulo = 10
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
                    'light-gray' : '#DCDCDC',#BFC3C6 #DCDCDC
                    'dark-gray' : '#A9A9A9', #58636B #A9A9A9
                    'light-blue' : '#B0C4DE',#0087CC #B0C4DE
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


class ConfiguraDataFrame:

    def __init__( self, data_frame, formatacao, linha_inicio=0 ):
        self.dfr = data_frame
        self.configurar_indice_iniciando_com_um()
        self.dfr.to_excel( formatacao.writer, startrow=( linha_inicio ), sheet_name=formatacao.nome_tabela, index=True )

    def configurar_indice_iniciando_com_um( self ):
        self.dfr['Item'] = [ x for x in range( 1, len( self.dfr ) + 1 ) ]
        self.dfr.set_index('Item', drop=True, inplace=True)

    def obter_data_frame_configurado( self ):
        return self.dfr

class Escrita:

    def __init__( self, formatacao, tamanho, numero_de_composicoes=0 ):
        self.writer = formatacao.writer
        self.formatacao = formatacao
        self.nome_tabela = self.formatacao.nome_tabela
        self.entrada_area_de_impressao = self.formatacao.entrada_area_de_impressao
        self.tamanho = tamanho
        self.numero_de_composicoes = numero_de_composicoes

    def configurar_area_impressao( self ):
        area_de_impressao = self.entrada_area_de_impressao.format(1, self.tamanho )
        self.writer.sheets[ self.nome_tabela ].print_area( area_de_impressao )

    def configurar_escala_para_largura_pagina( self ):
        if self.numero_de_composicoes > 0:
            self.writer.sheets[ self.nome_tabela ].fit_to_pages(1, self.numero_de_composicoes)
        else:
            self.writer.sheets[ self.nome_tabela ].fit_to_pages( 1, self.tamanho )
            self.configurar_cabecalho()
            self.configurar_repeticao_primeira_linha_tabela()
            self.configurar_linhas_de_grade()
        
    def configurar_orientacao_papel( self ):
        if self.formatacao.orientacao_retrato == True:
            self.writer.sheets[ self.nome_tabela ].set_portrait()
        else:
            self.writer.sheets[ self.nome_tabela ].set_landscape()

    def configurar_papel_a4( self ):
        # índice 9 (papel A4) vem da documentação da biblioteca xlsxwriter
        self.writer.sheets[ self.nome_tabela ].set_paper(9)

    def configurar_tabela_centro_pagina( self ):
        self.writer.sheets[ self.nome_tabela ].center_horizontally()

    def configurar_repeticao_primeira_linha_tabela( self ):
        self.writer.sheets[ self.nome_tabela ].repeat_rows(0)

    def configurar_formatacao_coluna_tabela( self ):
        for obj_entrada in self.formatacao.lista_entrada_formatacao:
            self.writer.sheets[ self.nome_tabela ].set_column( obj_entrada.coluna, obj_entrada.largura, obj_entrada.formatado )

    def configurar_linhas_de_grade( self ):
        self.writer.sheets[ self.nome_tabela ].hide_gridlines(option=0)

    def configurar_cabecalho( self ):
        self.writer.sheets[ self.nome_tabela ].set_header('&LDepartamento Nacional de Infraestrutura de Transportes')
        # self.writer.sheets[ self.nome_tabela ].set_margins(top=1.3)
        # self.writer.sheets[ self.nome_tabela ].set_header('&L&G', {'image_left': marca_dnit})

    def obter_escritor_configurado( self ):
        self.configurar_area_impressao()
        self.configurar_escala_para_largura_pagina()
        self.configurar_orientacao_papel()
        self.configurar_papel_a4()
        self.configurar_tabela_centro_pagina()
        self.configurar_formatacao_coluna_tabela()
        return self.writer


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