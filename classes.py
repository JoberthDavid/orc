import numpy as np
import pandas as pd

UTF='utf-8'

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
        self.subtotal_horario_execucao = 34
        self.subtotal_unitario_execucao = 35
        self.linha_vazia_execucao = 36
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

class Codigo:

    def __init__( self ) -> None:
        self.horario = 'ho'
        self.horario_execucao = 'ho_ex'
        self.unitario = 'un'
        self.unitario_direto_total = 'un_dt'


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
        return [ self.origem, self.estado, self.publicacao ]


class ListaColunaComposicaoDB(ListaColuna):

    def __init__( self ) -> None:
        super().__init__()

    def obter_lista( self ) -> list:
        return [ self.composicao_principal, self.fic, self.produtividade, self.tipo, self.none ]

class ListaColunaInsumoDB(ListaColuna):

    def __init__( self ) -> None:
        super().__init__()

    def obter_lista( self ) -> list:
        return [ self.codigo, self.descricao, self.unidade, self.none ]


class ListaColunaApropriacaoDB(ListaColuna):

    def __init__( self ) -> None:
        super().__init__()

    def obter_lista( self ) -> list:
        return [ self.composicao_principal, self.codigo, self.quantidade, self.utilizacao, self.item_transporte, 'Grupo', self.none ]

class ListaColunaCustoInsumoCT(ListaColuna):

    def __init__( self ) -> None:
        super().__init__()

    def obter_lista( self ) -> list:
        return [ self.codigo, self.custo_pro_onerado, self.custo_imp_onerado, self.custo_pro_desonerado, self.custo_imp_desonerado, self.preco_unitario, 'Grupo', self.none ]


class ListaColunaComposicaoDF(ListaColuna):

    def __init__( self, onerado: bool ) -> None:
        super().__init__()
        self.custo_produtivo = self.configurar_custo_produtivo( onerado )
        self.custo_improdutivo = self.configurar_custo_improdutivo( onerado )

    def obter_lista( self ) -> list:
        return [ self.composicao_principal, self.grupo, self.codigo, self.descricao, self.item_transporte, self.dmt, self.unidade, self.quantidade, self.utilizacao, self.custo_produtivo, self.custo_improdutivo, self.preco_unitario, self.custo_total ]

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


class GeradorDF:
    """Classe que gera um Data Frame e trata as suas colunas"""

    def __init__( self, arquivo: str ) -> None:
        self.dfr = self.carregar_dados(arquivo)

    def carregar_dados( self, arquivo ) -> pd.core.frame.DataFrame:
        return pd.read_csv( arquivo, encoding=UTF )

    def tratar_dfr( self, lista=list() ) -> pd.core.frame.DataFrame:
        obj_col_origem = ListaColunaOrigemCP()
        self.dfr.columns = obj_col_origem.obter_lista() + lista
        obj_col_origem.none
        if lista[-1] == obj_col_origem.none:
            self.dfr.pop( obj_col_origem.none )
        return self.dfr


class BaseDF:
    """Classe que reune a base de Data Frame necessários para o projeto"""
    
    def __init__( self, arq_db_cp: str, arq_db_in: str, arq_apr_in: str, arq_cto_in: str ) -> None:
        dfr_db_cp = GeradorDF(arq_db_cp)
        dfr_db_in = GeradorDF(arq_db_in)
        dfr_apr_in = GeradorDF(arq_apr_in)
        dfr_cto_in = GeradorDF(arq_cto_in)        
        self.dfr_dados_cp = self.tratar_dfr_dados_basicos_cp( dfr_db_cp )
        self.dfr_dados_in = self.tratar_dfr_dados_basicos_in( dfr_db_in )
        self.dfr_apropriacao_in = self.tratar_dfr_apropriacao_in( dfr_apr_in )
        self.dfr_custo_in = self.tratar_dfr_custo_in( dfr_cto_in )

    def tratar_dfr_dados_basicos_cp( self, dfr_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        obj_col_db_cp = ListaColunaComposicaoDB()
        return dfr_db.tratar_dfr( obj_col_db_cp.obter_lista() )

    def tratar_dfr_dados_basicos_in( self, dfr_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        obj_col_db_in = ListaColunaInsumoDB()
        return dfr_db.tratar_dfr( obj_col_db_in.obter_lista() )

    def tratar_dfr_apropriacao_in( self, dfr_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        obj_col_db_ap = ListaColunaApropriacaoDB()
        return dfr_db.tratar_dfr( obj_col_db_ap.obter_lista() )

    def tratar_dfr_custo_in( self, dfr_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        obj_col_ct_in = ListaColunaCustoInsumoCT()
        return dfr_db.tratar_dfr( obj_col_ct_in.obter_lista() )

    def max_apr( self ) -> int:
        obj_col_db_ap = ListaColunaApropriacaoDB()
        return self.dfr_apropriacao_in.groupby( obj_col_db_ap.composicao_principal ).size().max()


class ComposicaoDB:
    """Classe que representa os parâmetros mais importantes de cada composição do projeto"""

    def __init__( self, codigo: str, onerado=True ) -> None:
        self.obj_arred = Precisao()
        self.codigo = self.tratar_codigo_composicao( codigo )
        self.onerado = onerado
        self.descricao = ''
        self.unidade = ''
        self.fic = 0.0000
        self.produtividade  = 1.00
        self.custo_horario_equipamento = 0.0000
        self.custo_horario_mao_de_obra = 0.0000
        self.custo_horario_execucao = 0.0000
        self.custo_unitario_execucao = 0.0000
        self.custo_fic = 0.0000
        self.custo_fit = 0.0000
        self.custo_unitario_material = 0.0000
        self.custo_total_insumos = 0.0000
        self.custo_total_atividade_auxiliar = 0.0000
        self.custo_total_tempo_fixo = 0.0000
        self.custo_total_transporte = 0.0000
        self.custo_unitario_total = 0.0000
        self.custo_bdi = 0.0000
        self.preco_unitario_total = 0.0000

    def tratar_codigo_composicao( self, codigo: str ) -> str:
        if len( codigo ) == 6 : 
            codigo = "0{}".format( codigo )
        return codigo

    def configurar_custo_horario_execucao( self ) -> float:
        self.custo_horario_execucao = self.obj_arred.custo( self.custo_horario_equipamento + self.custo_horario_mao_de_obra )
        return self.custo_horario_execucao

    def configurar_custo_unitario_execucao( self ) -> float:
        self.custo_unitario_execucao = self.obj_arred.custo( self.custo_horario_execucao / self.produtividade )
        return self.custo_unitario_execucao

    def configurar_custo_unitario_total( self ) -> float:
        self.custo_unitario_total = self.obj_arred.custo( self.custo_unitario_execucao + self.custo_unitario_material + self.custo_total_atividade_auxiliar + self.custo_total_tempo_fixo + self.custo_total_transporte )
        return self.custo_unitario_total

    def configurar_preco_unitario_total( self ) -> float:
        self.preco_unitario_total = self.obj_arred.custo( self.custo_bdi + self.custo_unitario_total )
        return self.preco_unitario_total

class LinhaDF:

    def __init__( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> None:
        self.obj_col_dfr = obj_col
        self.obj_arred = Precisao()
        self.obj_codigo = Codigo()
        self.linha = _dfr_insumo[ [obj_col.custo_total] ].sum()
        self.composicao = composicao
        self.linha[ obj_col.composicao_principal ] = self.composicao.codigo
        self.total = self.linha[ self.obj_col_dfr.custo_total ]
        self.obj_grupo = Grupo()


class LinhaEquipamentoDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_subtotal_equipamento()
        
    def configurar_linha_subtotal_equipamento( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo horário equipamento'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.horario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_horario_equipamento


class LinhaMaoDeObraDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_subtotal_mao_de_obra()

    def configurar_linha_subtotal_mao_de_obra( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo horário mão de obra'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.horario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_horario_mao_de_obra


class LinhaMaterialDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_subtotal_material()

    def configurar_linha_subtotal_material( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo unitário material'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.unitario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_unitario_material


class LinhaCustoHorarioExecucaoDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_custo_horario_execucao()

    def configurar_linha_custo_horario_execucao( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo horário de execução'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.horario_execucao
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_horario_execucao
        self.linha[ self.obj_col_dfr.custo_total ] = self.obj_arred.custo( self.composicao.configurar_custo_horario_execucao() )


class LinhaCustoUnitarioExecucaoDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_custo_unitario_execucao()

    def configurar_linha_custo_unitario_execucao( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo unitário de execução'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.unitario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_unitario_execucao
        self.linha[ self.obj_col_dfr.custo_total ] = self.obj_arred.custo( self.composicao.configurar_custo_unitario_execucao() )


class LinhaAtividadeAuxiliarDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_subtotal_atividade_auxiliar()

    def configurar_linha_subtotal_atividade_auxiliar( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo unitário atividade auxiliar'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.unitario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_unitario_atividade_auxiliar


class LinhaTempoFixoDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_subtotal_tempo_fixo()

    def configurar_linha_subtotal_tempo_fixo( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo unitário tempo fixo'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.unitario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_unitario_tempo_fixo


class LinhaTransporteDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_subtotal_transporte()

    def configurar_linha_subtotal_transporte( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo unitário transporte'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.unitario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_unitario_transporte


class LinhaCustoUnitarioDiretoTotalDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_total_unitario_direto()

    def configurar_linha_total_unitario_direto( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo unitário direto total'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.unitario_direto_total
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.total_unitario_direto
        self.linha[ self.obj_col_dfr.custo_total ] = self.obj_arred.custo( self.composicao.configurar_custo_unitario_total() )


class ComposicaoDF:
    """Classe que representa os data frames de cada composição do projeto que servirão para gerar um arquivo xlsx"""

    def __init__( self, composicao: ComposicaoDB, base: BaseDF ) -> None:
        self.obj_col_dfr = ListaColunaComposicaoDF(composicao.onerado)
        self.obj_col_cp = ListaColunaComposicaoDB()
        self.obj_grupo = Grupo()
        self.obj_arred = Precisao()
        self.composicao = composicao
        self.base = base
        self.dfr_dados_basicos = self.base.dfr_dados_cp
        self.dfr_custo_in = self.base.dfr_custo_in
        self.composicao.descricao = self.obter_descricao_composicao()
        self.composicao.unidade = self.obter_unidade_composicao()
        self.composicao.fic = self.obter_fic_composicao()
        self.composicao.produtividade = self.obter_produtividade_composicao()

        self.dfr_insumo = self.associar_dfr_custos_apropriacoes_insumos()
        self.inserir_col_dmt()
        self.dfr_insumo = self.obter_dfr_custo_equipamento()
        self.dfr_insumo = self.obter_dfr_custo_mao_de_obra()
        self.dfr_insumo = self.obter_dfr_custo_material()
        self.dfr_insumo = self.dfr_insumo[ self.obj_col_dfr.obter_lista() ]

        self.calcular_subtotal_simples()


    def obter_dfr_dados_basicos_insumos( self ) -> pd.core.frame.DataFrame:
        return self.base.dfr_dados_in.query( "{} == '{}'".format( self.obj_col_dfr.codigo, self.composicao.codigo ) )

    def obter_dfr_dados_basicos_composicao( self ) -> pd.core.frame.DataFrame:
        return self.base.dfr_dados_cp.query( "{} == '{}'".format( self.obj_col_dfr.composicao_principal, self.composicao.codigo ) )

    def obter_dfr_apropriacoes_insumos( self ) -> pd.core.frame.DataFrame:
        return self.base.dfr_apropriacao_in.query( "{} == '{}'".format( self.obj_col_dfr.composicao_principal, self.composicao.codigo ) )

    def obter_descricao_composicao( self ) -> str:
        auxiliar = self.obter_dfr_dados_basicos_insumos()
        return auxiliar[ self.obj_col_cp.descricao ].values[0]

    def obter_unidade_composicao( self ) -> str:
        auxiliar = self.obter_dfr_dados_basicos_insumos()
        return auxiliar[ self.obj_col_cp.unidade ].values[0]

    def obter_fic_composicao( self ) -> float:
        auxiliar = self.obter_dfr_dados_basicos_composicao()
        return auxiliar[ self.obj_col_cp.fic ].values[0]
    
    def obter_produtividade_composicao( self ) -> float:
        auxiliar = self.obter_dfr_dados_basicos_composicao()
        return auxiliar[ self.obj_col_cp.produtividade ].values[0]

    def associar_dfr_dados_basicos_apropriacoes_insumos( self ) -> pd.core.frame.DataFrame:
        return pd.merge( self.obter_dfr_apropriacoes_insumos(), self.base.dfr_dados_in, on=self.obj_col_dfr.codigo, how='left' )

    def inserir_col_dmt( self ) -> None:
        self.dfr_insumo[ self.obj_col_dfr.dmt ] = ''

    def associar_dfr_custos_apropriacoes_insumos( self ) -> pd.core.frame.DataFrame:
        return pd.merge( self.associar_dfr_dados_basicos_apropriacoes_insumos(), self.dfr_custo_in, on=self.obj_col_dfr.codigo, how='left')

    def calcular_sre_custo_equipamento( self ) -> pd.core.series.Series:
        quantidade = self.dfr_insumo[ self.obj_col_dfr.quantidade ]
        custo_produtivo = self.dfr_insumo[ self.obj_col_dfr.custo_produtivo ]
        custo_improdutivo = self.dfr_insumo[ self.obj_col_dfr.custo_improdutivo ]
        utilizacao = self.dfr_insumo[ self.obj_col_dfr.utilizacao ]
        return self.obj_arred.custo( quantidade * ( ( utilizacao * custo_produtivo ) + ( ( 1 - utilizacao ) * custo_improdutivo ) ) )

    def calcular_sre_custo_mao_de_obra( self ) -> pd.core.series.Series:
        quantidade = self.dfr_insumo[ self.obj_col_dfr.quantidade ]
        custo_produtivo = self.dfr_insumo[ self.obj_col_dfr.custo_produtivo ]
        return self.obj_arred.custo( quantidade * custo_produtivo )

    def calcular_sre_custo_material( self ) -> pd.core.series.Series:
        quantidade = self.dfr_insumo[ self.obj_col_dfr.quantidade ]
        preco_unitario = self.dfr_insumo[ self.obj_col_dfr.preco_unitario ]
        return self.obj_arred.custo( quantidade * preco_unitario )

    def obter_dfr_custo_equipamento( self ) -> pd.core.frame.DataFrame:
        self.dfr_insumo.loc[self.dfr_insumo[self.obj_col_dfr.grupo] == self.obj_grupo.insumo_equipamento, self.obj_col_dfr.custo_total ] = self.calcular_sre_custo_equipamento()
        return self.dfr_insumo

    def obter_dfr_custo_mao_de_obra( self ) -> pd.core.frame.DataFrame:
        self.dfr_insumo.loc[self.dfr_insumo[self.obj_col_dfr.grupo] == self.obj_grupo.insumo_mao_de_obra, self.obj_col_dfr.custo_total ] = self.calcular_sre_custo_mao_de_obra()
        return self.dfr_insumo

    def obter_dfr_custo_material( self ) -> pd.core.frame.DataFrame:
        self.dfr_insumo.loc[self.dfr_insumo[self.obj_col_dfr.grupo] == self.obj_grupo.insumo_material, self.obj_col_dfr.custo_total ] = self.calcular_sre_custo_material()
        return self.dfr_insumo

    def criar_linha_subtotal_equipamento( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaEquipamentoDF:
        return LinhaEquipamentoDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_subtotal_mao_de_obra( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaMaoDeObraDF:
        return LinhaMaoDeObraDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_subtotal_material( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaMaterialDF:
        return LinhaMaterialDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_custo_horario_execucao( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaCustoHorarioExecucaoDF:
        return LinhaCustoHorarioExecucaoDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_custo_unitario_execucao( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaCustoUnitarioExecucaoDF:
        return LinhaCustoUnitarioExecucaoDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_subtotal_atividade_auxiliar(self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaAtividadeAuxiliarDF:
        return LinhaAtividadeAuxiliarDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_subtotal_tempo_fixo( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaTempoFixoDF:
        return LinhaTempoFixoDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_subtotal_transporte( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaTransporteDF:
        return LinhaTransporteDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_custo_unitario_direto_total( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaCustoUnitarioDiretoTotalDF:
        return LinhaCustoUnitarioDiretoTotalDF( _dfr_insumo, composicao, obj_col )

    def obter_dfr_equipamento( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format( self.obj_col_dfr.grupo, self.obj_grupo.insumo_equipamento ) )

    def obter_dfr_mao_de_obra( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format( self.obj_col_dfr.grupo, self.obj_grupo.insumo_mao_de_obra ) )

    def obter_dfr_material( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format( self.obj_col_dfr.grupo, self.obj_grupo.insumo_material ) )

####################

    def obter_dfr_subtotal_equipamento( self ):
        obj_linha_eq = self.criar_linha_subtotal_equipamento( self.obter_dfr_equipamento(), self.composicao, self.obj_col_dfr )
        self.composicao.custo_horario_equipamento = obj_linha_eq.total
        return obj_linha_eq

    def obter_dfr_subtotal_mao_de_obra( self ):
        obj_linha_mo = self.criar_linha_subtotal_mao_de_obra( self.obter_dfr_mao_de_obra(), self.composicao, self.obj_col_dfr )
        self.composicao.custo_horario_mao_de_obra = obj_linha_mo.total
        return obj_linha_mo

    def obter_dfr_subtotal_material( self ):
        obj_linha_ma = self.criar_linha_subtotal_material( self.obter_dfr_material(), self.composicao, self.obj_col_dfr )
        self.composicao.custo_unitario_material = obj_linha_ma.total
        return obj_linha_ma

    def obter_dfr_horario_execucao( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format(self.obj_col_dfr.grupo, self.obj_grupo.subtotal_horario_execucao ) )

    def obter_dfr_subtotal_horario_execucao( self ):
        obj_linha_he = self.criar_linha_custo_horario_execucao( self.obter_dfr_horario_execucao(), self.composicao, self.obj_col_dfr )
        return obj_linha_he

    def obter_dfr_unitario_execucao( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format(self.obj_col_dfr.grupo, self.obj_grupo.subtotal_unitario_execucao ) )

    def obter_dfr_subtotal_unitario_execucao( self ):
        obj_linha_ue = self.criar_linha_custo_unitario_execucao( self.obter_dfr_unitario_execucao(), self.composicao, self.obj_col_dfr )
        return obj_linha_ue

    def calcular_subtotal_simples( self ) -> None:
        # equipamento
        obj_linha_eq = self.obter_dfr_subtotal_equipamento()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_eq.linha, ignore_index=True )
        # mão de obra
        obj_linha_mo = self.obter_dfr_subtotal_mao_de_obra()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_mo.linha, ignore_index=True )
        # material
        obj_linha_ma = self.obter_dfr_subtotal_material()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_ma.linha, ignore_index=True )
        # horário execução
        obj_linha_he = self.obter_dfr_subtotal_horario_execucao()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_he.linha, ignore_index=True )
        # unitário execução
        obj_linha_ue = self.obter_dfr_subtotal_unitario_execucao()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_ue.linha, ignore_index=True )

    def obter_dfr_atividade_auxiliar( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format( self.obj_col_dfr.grupo, self.obj_grupo.insumo_atividade_auxiliar ) )
        
    def obter_dfr_subtotal_atividade_auxiliar( self ):
        obj_linha_aa = self.criar_linha_subtotal_atividade_auxiliar( self.obter_dfr_atividade_auxiliar(), self.composicao, self.obj_col_dfr )
        self.composicao.custo_total_atividade_auxiliar = obj_linha_aa.total
        return obj_linha_aa

    def obter_dfr_tempo_fixo( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format( self.obj_col_dfr.grupo, self.obj_grupo.insumo_tempo_fixo ) )

    def obter_dfr_subtotal_tempo_fixo( self ):
        obj_linha_tf = self.criar_linha_subtotal_tempo_fixo( self.obter_dfr_tempo_fixo(), self.composicao, self.obj_col_dfr )
        self.composicao.custo_total_tempo_fixo = obj_linha_tf.total
        return obj_linha_tf

    def obter_dfr_transporte( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format( self.obj_col_dfr.grupo, self.obj_grupo.insumo_transporte ) )

    def obter_dfr_subtotal_transporte( self ):
        obj_linha_tr = self.criar_linha_subtotal_transporte( self.obter_dfr_transporte(), self.composicao, self.obj_col_dfr )
        self.composicao.custo_total_transporte = obj_linha_tr.total
        return obj_linha_tr

    def obter_dfr_unitario_direto( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format( self.obj_col_dfr.grupo, self.obj_grupo.total_unitario_direto ) )

    def obter_dfr_total_unitario_direto( self ):
        obj_linha_cd = self.criar_linha_custo_unitario_direto_total( self.obter_dfr_unitario_direto(), self.composicao, self.obj_col_dfr )
        return obj_linha_cd

    def calcular_subtotal_composto( self ) -> None:
        # atividade auxiliar
        obj_linha_aa = self.obter_dfr_subtotal_atividade_auxiliar()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_aa.linha, ignore_index=True )
        # tempo fixo
        obj_linha_tf = self.obter_dfr_subtotal_tempo_fixo()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_tf.linha, ignore_index=True )
        # transporte
        obj_linha_tr = self.obter_dfr_subtotal_transporte()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_tr.linha, ignore_index=True )
        # unitário direto total
        obj_linha_cd = self.obter_dfr_total_unitario_direto()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_cd.linha, ignore_index=True )

    def calcular_custo_atividade_auxiliar( self, dicionario: dict ) -> None:
        lista = self.obter_lis_atividade_auxiliar()
        for item in lista:
            grupo = item[0]
            item = item[1]
            self.dfr_insumo.loc[ self.dfr_insumo[ self.obj_col_dfr.codigo ] == item,self.obj_col_dfr.preco_unitario ] = dicionario[ item ].custo_unitario_total 
            quantidade = self.dfr_insumo.loc[ self.dfr_insumo[ self.obj_col_dfr.codigo ] == item, self.obj_col_dfr.quantidade ]
            preco_unitario = self.dfr_insumo.loc[ self.dfr_insumo[ self.obj_col_dfr.codigo ] == item, self.obj_col_dfr.preco_unitario ]
            if ( grupo == self.obj_grupo.insumo_transporte ):
                distancia_transporte = self.dfr_insumo.loc[ self.dfr_insumo[ self.obj_col_dfr.codigo ] == item, self.obj_col_dfr.dmt ] = 0.00
                self.dfr_insumo.loc[ self.dfr_insumo[ self.obj_col_dfr.codigo ] == item, self.obj_col_dfr.custo_total ] = self.obj_arred.custo( distancia_transporte * quantidade * preco_unitario )
            else:
                self.dfr_insumo.loc[ self.dfr_insumo[ self.obj_col_dfr.codigo ] == item, self.obj_col_dfr.custo_total ] = self.obj_arred.custo( quantidade * preco_unitario )

    def obter_operador_lis_insumo( self, insumo: int ) -> str:
        if ( insumo == self.obj_grupo.insumo_atividade_auxiliar ):
            operador = '>='
        else:
            operador = '=='
        return operador

    def configurar_lis_insumo( self, consulta: pd.core.frame.DataFrame ) -> list:
        lista = list()
        obj_col_in = ListaColunaInsumoDB() 
        if len( consulta[ ['Grupo', obj_col_in.codigo] ].values ) != 0:
            for item in consulta[ ['Grupo', obj_col_in.codigo] ].values:
                lista.append( item )
        return lista

    def obter_lis_insumo( self, insumo: int ) -> list:
        operador = self.obter_operador_lis_insumo( insumo )
        consulta = self.base.dfr_apropriacao_in.query( "{} == '{}' & Grupo {} {}".format( self.obj_col_dfr.composicao_principal, self.composicao.codigo, operador, insumo ) )
        return self.configurar_lis_insumo( consulta )

    def obter_lis_atividade_auxiliar( self ) -> list:
        return self.obter_lis_insumo( self.obj_grupo.insumo_atividade_auxiliar )

    def obter_lis_equipamento( self ) -> list:
        return self.obter_lis_insumo( self.obj_grupo.insumo_equipamento )

    def obter_lis_mao_de_obra( self ) -> list:
        return self.obter_lis_insumo( self.obj_grupo.insumo_mao_de_obra )
    
    def obter_lis_material( self ) -> list:
        return self.obter_lis_insumo( self.obj_grupo.insumo_material )

    def criar_linhas_vazias( self ) -> None:
        self.dfr_insumo = self.dfr_insumo.append( [ { self.obj_col_dfr.composicao_principal : self.composicao.codigo, self.obj_col_dfr.grupo : self.obj_grupo.linha_vazia_inicial } ], ignore_index=True )
        self.dfr_insumo = self.dfr_insumo.append( [ { self.obj_col_dfr.composicao_principal : self.composicao.codigo, self.obj_col_dfr.grupo : self.obj_grupo.linha_vazia_equipamento } ], ignore_index=True )
        self.dfr_insumo = self.dfr_insumo.append( [ { self.obj_col_dfr.composicao_principal : self.composicao.codigo, self.obj_col_dfr.grupo : self.obj_grupo.linha_vazia_mao_de_obra } ], ignore_index=True )
        self.dfr_insumo = self.dfr_insumo.append( [ { self.obj_col_dfr.composicao_principal : self.composicao.codigo, self.obj_col_dfr.grupo : self.obj_grupo.linha_vazia_execucao } ], ignore_index=True )
        self.dfr_insumo = self.dfr_insumo.append( [ { self.obj_col_dfr.composicao_principal : self.composicao.codigo, self.obj_col_dfr.grupo : self.obj_grupo.linha_vazia_material } ], ignore_index=True )
        self.dfr_insumo = self.dfr_insumo.append( [ { self.obj_col_dfr.composicao_principal : self.composicao.codigo, self.obj_col_dfr.grupo : self.obj_grupo.linha_vazia_atividade_auxiliar } ], ignore_index=True )
        self.dfr_insumo = self.dfr_insumo.append( [ { self.obj_col_dfr.composicao_principal : self.composicao.codigo, self.obj_col_dfr.grupo : self.obj_grupo.linha_vazia_tempo_fixo } ], ignore_index=True )
        self.dfr_insumo = self.dfr_insumo.append( [ { self.obj_col_dfr.composicao_principal : self.composicao.codigo, self.obj_col_dfr.grupo : self.obj_grupo.linha_vazia_transporte } ], ignore_index=True )


class Projeto:

    def __init__(self, lista: list, baseDF: BaseDF, onerado=True) -> None:
        self.baseDF = baseDF
        self.onerado = onerado
        self.composicoes_projeto = lista
        self.equipamento_projeto = list()
        self.mao_de_obra_projeto = list()
        self.material_projeto = list()
        self.dic_db_projeto = dict()
        self.dic_df_projeto = dict()
        self.lista_auxiliar = list()
        self.gerar_dicionario_dados_basicos_composicoes_projeto()

    def gerar_dicionario_dados_basicos_composicoes_projeto( self ):
        for codigo_cp in self.composicoes_projeto:
            obj_composicao_db = ComposicaoDB( codigo_cp, self.onerado )
            obj_composicao_df = ComposicaoDF( obj_composicao_db, self.baseDF )
            self.dic_db_projeto[ obj_composicao_db.codigo ] = obj_composicao_db
            self.dic_df_projeto[ obj_composicao_db.codigo ] = obj_composicao_df
            lista_eq = obj_composicao_df.obter_lis_equipamento()
            lista_mo = obj_composicao_df.obter_lis_mao_de_obra()
            lista_ma = obj_composicao_df.obter_lis_material()
            lista_aa = obj_composicao_df.obter_lis_atividade_auxiliar()
            self.lista_auxiliar.append( codigo_cp )
            
            if ( lista_aa != None):
                for item in lista_aa:
                    item = item[1]
                    if item not in self.composicoes_projeto:
                        self.composicoes_projeto.append( item )
                    self.lista_auxiliar.append( item )

            if( lista_eq != None):
                for item in lista_eq:
                    item = item[1]
                    if item not in self.equipamento_projeto:
                        self.equipamento_projeto.append( item )

            if( lista_mo != None):
                for item in lista_mo:
                    item = item[1]
                    if item not in self.mao_de_obra_projeto:
                        self.mao_de_obra_projeto.append( item )
            
            if( lista_ma != None):
                for item in lista_ma:
                    item = item[1]
                    if item not in self.material_projeto:
                        self.material_projeto.append( item )

    def tratar_composicoes_projeto(self) -> list:
        lista_auxiliar_reversa = list()
        while( len( self.lista_auxiliar ) != 0 ):
            ultimo = self.lista_auxiliar[-1]
            if ultimo not in lista_auxiliar_reversa:
                lista_auxiliar_reversa.append( ultimo )
            self.lista_auxiliar.pop()
        return lista_auxiliar_reversa

    def tratar_codigo_composicao( self, codigo: str, menor_tamanho_codigo=6 ) -> str:
        if len( codigo ) == menor_tamanho_codigo : 
            codigo = "0{}".format( codigo )
        return codigo

    def obter_dfr_projeto( self ) -> dict:
        lista_auxiliar_reversa = self.tratar_composicoes_projeto()
        for item in lista_auxiliar_reversa:
            comp = self.tratar_codigo_composicao( item )
            self.dic_df_projeto[ comp ].calcular_custo_atividade_auxiliar( self.dic_db_projeto )
            self.dic_df_projeto[ comp ].calcular_subtotal_composto()
            self.dic_df_projeto[ comp ].criar_linhas_vazias()
            self.dic_df_projeto[ comp ].dfr_insumo.sort_values( by = self.dic_df_projeto[ comp ].obj_col_dfr.grupo, inplace=True )
            self.dic_df_projeto[ comp ].dfr_insumo.reset_index( drop=True, inplace=True )
        return self.dic_df_projeto