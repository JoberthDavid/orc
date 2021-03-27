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
        self.largura = 1.2 * self.modulo


class FormatacaoResumoOrigem(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 1.2 * self.modulo


class FormatacaoResumoEstado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 1.2 * self.modulo


class FormatacaoResumoPublicacao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 1.2 * self.modulo


class FormatacaoResumoCodigo(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 2.0 * self.modulo


class FormatacaoResumoDescricao(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_esquerda()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 14.0 * self.modulo


class FormatacaoResumoUnidade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_centro()
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 1.0 * self.modulo


class FormatacaoResumoQuantidade(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_significativo(4)
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 2.5 * self.modulo


class FormatacaoResumoPrecoUnitario(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_significativo(4)
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 3.0 * self.modulo


class FormatacaoResumoCustoTotal(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_significativo(2)
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 3.0 * self.modulo

class FormatacaoResumoQuantidadeDesdobrada(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_significativo(10)
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 2.5 * self.modulo


class FormatacaoResumoCustoTotalDesdobrado(Formatacao):

    def __init__( self, writer ) -> None:
        super().__init__( writer )
        obj_formatacao = Formatacao( writer )
        obj_formatacao.alinhamento_direita()
        obj_formatacao.algarismo_significativo(10)
        self.formatado = obj_formatacao.aplicar_formatacao()
        self.coluna = ''
        self.largura = 3.0 * self.modulo


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



class FormatacaoEscrita:

    def __init__( self, writer ):
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
        self.obj_formatacao_custo_total_desdobrado = FormatacaoResumoCustoTotalDesdobrado( writer )


class FormatacaoEscritaCustoEquipamento(FormatacaoEscrita):

    def __init__( self, writer ):
        super().__init__( writer )
        self.nome_tabela = 'resumo_equipamento_custo'
        self.entrada_area_de_impressao = '$A${}:$J${}'
        self.obj_formatacao_grupo.coluna = 'B:B'
        self.obj_formatacao_origem.coluna = 'C:C'
        self.obj_formatacao_estado.coluna = 'D:D'
        self.obj_formatacao_publicacao.coluna = 'E:E'
        self.obj_formatacao_codigo.coluna = 'F:F'
        self.obj_formatacao_descricao.coluna = 'G:G'
        self.obj_formatacao_unidade.coluna = 'H:H'
        self.obj_formatacao_preco_unitario.coluna = 'I:J'
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
        self.orientacao_retrato = True


class FormatacaoEscritaCustoMaoDeObra(FormatacaoEscrita):

    def __init__( self, writer ):
        super().__init__( writer )
        self.nome_tabela = 'resumo_mao_de_obra_custo'
        self.entrada_area_de_impressao = '$A${}:$I${}'
        self.obj_formatacao_grupo.coluna = 'B:B'
        self.obj_formatacao_origem.coluna = 'C:C'
        self.obj_formatacao_estado.coluna = 'D:D'
        self.obj_formatacao_publicacao.coluna = 'E:E'
        self.obj_formatacao_codigo.coluna = 'F:F'
        self.obj_formatacao_descricao.coluna = 'G:G'
        self.obj_formatacao_unidade.coluna = 'H:H'
        self.obj_formatacao_preco_unitario.coluna = 'I:I'
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
        self.orientacao_retrato = True


class FormatacaoEscritaCustoMaterial(FormatacaoEscrita):

    def __init__( self, writer ):
        super().__init__( writer )
        self.nome_tabela = 'resumo_material_custo'
        self.entrada_area_de_impressao = '$A${}:$I${}'
        self.obj_formatacao_grupo.coluna = 'B:B'
        self.obj_formatacao_origem.coluna = 'C:C'
        self.obj_formatacao_estado.coluna = 'D:D'
        self.obj_formatacao_publicacao.coluna = 'E:E'
        self.obj_formatacao_codigo.coluna = 'F:F'
        self.obj_formatacao_descricao.coluna = 'G:G'
        self.obj_formatacao_unidade.coluna = 'H:H'
        self.obj_formatacao_preco_unitario.coluna = 'I:I'
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
        self.orientacao_retrato = True


class FormatacaoEscritaResumoTransporte(FormatacaoEscrita):

    def __init__( self, writer ):
        super().__init__( writer )
        self.nome_tabela = 'resumo_transporte_utilizado'
        self.entrada_area_de_impressao = '$A${}:$H${}'
        self.obj_formatacao_servico.coluna = 'B:B'
        self.obj_formatacao_composicao.coluna = 'C:D'
        self.obj_formatacao_descricao.coluna = 'E:E'
        self.obj_formatacao_unidade.coluna = 'F:F'
        self.obj_formatacao_codigo.coluna = 'G:G'
        self.obj_formatacao_quantidade_desdobrada.coluna = 'H:H'
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_servico,
                self.obj_formatacao_composicao,
                self.obj_formatacao_composicao,
                self.obj_formatacao_descricao,
                self.obj_formatacao_unidade,
                self.obj_formatacao_codigo,
                self.obj_formatacao_quantidade_desdobrada,
            ]
        self.orientacao_retrato = True


class FormatacaoEscritaResumoEquipamento(FormatacaoEscrita):

    def __init__( self, writer ):
        super().__init__( writer )
        self.nome_tabela = 'resumo_equipamento_utilizado'
        self.entrada_area_de_impressao = '$A${}:$J${}'
        self.obj_formatacao_servico.coluna = 'B:B'
        self.obj_formatacao_composicao.coluna = 'C:C'
        self.obj_formatacao_codigo.coluna = 'D:D'
        self.obj_formatacao_descricao.coluna = 'E:E'
        self.obj_formatacao_quantidade_desdobrada.coluna = 'F:G'
        self.obj_formatacao_preco_unitario.coluna = 'H:I'
        self.obj_formatacao_custo_total_desdobrado.coluna = 'J:J'
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_servico,
                self.obj_formatacao_composicao,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_quantidade_desdobrada,
                self.obj_formatacao_preco_unitario,
                self.obj_formatacao_custo_total_desdobrado,
            ]
        self.orientacao_retrato = True


class FormatacaoEscritaResumoMaoDeObra(FormatacaoEscrita):

    def __init__( self, writer ):
        super().__init__( writer )
        self.nome_tabela = 'resumo_mao_de_obra_utilizado'
        self.entrada_area_de_impressao = '$A${}:$G${}'
        self.obj_formatacao_servico.coluna = 'B:B'
        self.obj_formatacao_composicao.coluna = 'C:C'
        self.obj_formatacao_codigo.coluna = 'D:D'
        self.obj_formatacao_descricao.coluna = 'E:E'
        self.obj_formatacao_quantidade_desdobrada.coluna = 'F:F'
        self.obj_formatacao_custo_total_desdobrado.coluna = 'G:G'
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_servico,
                self.obj_formatacao_composicao,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_quantidade_desdobrada,
                self.obj_formatacao_custo_total_desdobrado,
            ]
        self.orientacao_retrato = True


class FormatacaoEscritaResumoMaterial(FormatacaoEscrita):

    def __init__( self, writer ):
        super().__init__( writer )
        self.nome_tabela = 'resumo_material_utilizado'
        self.entrada_area_de_impressao = '$A${}:$G${}'
        self.obj_formatacao_servico.coluna = 'B:B'
        self.obj_formatacao_composicao.coluna = 'C:C'
        self.obj_formatacao_codigo.coluna = 'D:D'
        self.obj_formatacao_descricao.coluna = 'E:E'
        self.obj_formatacao_quantidade_desdobrada.coluna = 'F:F'
        self.obj_formatacao_custo_total_desdobrado.coluna = 'G:G'
        self.lista_entrada_formatacao = [ 
                self.obj_formatacao_id,
                self.obj_formatacao_servico,
                self.obj_formatacao_composicao,
                self.obj_formatacao_codigo,
                self.obj_formatacao_descricao,
                self.obj_formatacao_quantidade_desdobrada,
                self.obj_formatacao_custo_total_desdobrado,
            ]
        self.orientacao_retrato = True


class FormatacaoEscritaResumoServico(FormatacaoEscrita):

    def __init__( self, writer ):
        super().__init__( writer )
        self.nome_tabela = 'resumo_servico'
        self.entrada_area_de_impressao = '$A${}:$G${}'
        self.obj_formatacao_servico.coluna = 'B:B'
        self.obj_formatacao_descricao.coluna = 'C:C'
        self.obj_formatacao_unidade.coluna = 'D:D'
        self.obj_formatacao_quantidade.coluna = 'E:E'
        self.obj_formatacao_preco_unitario.coluna = 'F:F'
        self.obj_formatacao_custo_total.coluna = 'G:G'
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


class Escrita:

    def __init__( self, data_frame, formatacao ):
        self.dfr = data_frame
        self.configurar_indice_iniciando_com_um()
        self.writer = formatacao.writer
        self.formatacao = formatacao
        self.nome_tabela = self.formatacao.nome_tabela
        self.entrada_area_de_impressao = self.formatacao.entrada_area_de_impressao
        self.dfr.to_excel( self.writer, index=True, sheet_name=self.nome_tabela )
        self.tamanho = self.dfr.shape[0]

    def configurar_area_impressao( self ):
        area_de_impressao = self.entrada_area_de_impressao.format(1, self.tamanho )
        self.writer.sheets[ self.nome_tabela ].print_area( area_de_impressao )

    def configurar_escala_para_largura_pagina( self ):
        self.writer.sheets[ self.nome_tabela ].fit_to_pages( 1, self.tamanho )
        
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

    def configurar_primeira_linha_tabela( self ):
        self.writer.sheets[ self.nome_tabela ].repeat_rows(0)

    def configurar_formatacao_coluna_tabela( self ):
        for obj_entrada in self.formatacao.lista_entrada_formatacao:
            self.writer.sheets[ self.nome_tabela ].set_column( obj_entrada.coluna, obj_entrada.largura, obj_entrada.formatado )

    def configurar_indice_iniciando_com_um( self ):
        self.dfr['Item'] = [ x for x in range( 1, len( self.dfr ) + 1 ) ]
        self.dfr.set_index('Item', drop=True, inplace=True)

    def obter_escritor_configurado( self ):
        self.configurar_area_impressao()
        self.configurar_escala_para_largura_pagina()
        self.configurar_orientacao_papel()
        self.configurar_papel_a4()
        self.configurar_tabela_centro_pagina()
        self.configurar_primeira_linha_tabela()
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