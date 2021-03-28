from formatacao_dados import Formatacao


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