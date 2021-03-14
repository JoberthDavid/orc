import numpy as np
import pandas as pd
from estrutura_dados import *
from formatacao_dados import *


ENCODING = 'utf-8' #'ISO-8859-1'

class GeradorDF:
    """Classe que gera um Data Frame e trata as suas colunas"""

    def __init__( self, arquivo: str ) -> None:
        self.dfr = self.carregar_dados( arquivo )

    def carregar_dados( self, arquivo ) -> pd.core.frame.DataFrame:
        return pd.read_csv( arquivo, encoding=ENCODING, sep=',' )

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
        dfr_db_cp = GeradorDF( arq_db_cp )
        dfr_db_in = GeradorDF( arq_db_in )
        dfr_apr_in = GeradorDF( arq_apr_in )
        dfr_cto_in = GeradorDF( arq_cto_in )
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
        quantidade_linhas_fixas = 21
        obj_col_db_ap = ListaColunaApropriacaoDB()
        return quantidade_linhas_fixas + self.dfr_apropriacao_in.groupby( obj_col_db_ap.composicao_principal ).size().max()


class BonificacaoDespesasIndiretas:

    def __init__(self, principal: float, diferenciado: float, onerado=True) -> None:
        self.principal = principal
        self.diferenciado = diferenciado
        self.onerado = onerado


class ComposicaoDB:
    """Classe que representa os parâmetros mais importantes de cada composição do projeto"""

    def __init__( self, codigo: str, bdi: BonificacaoDespesasIndiretas, diferenciado=False ) -> None:
        self.obj_arred = Precisao()
        self.codigo = self.tratar_codigo_composicao( codigo )
        self.bdi = bdi
        self.diferenciado = diferenciado
        self.onerado = self.bdi.onerado
        self.descricao = ''
        self.unidade = ''
        self.fic = 0.0000
        self.fit = 0.0000
        self.bdi_valor_utilizado = self.obter_valor_bdi()
        self.produtividade  = 1.00
        self.custo_horario_equipamento = 0.0000
        self.custo_horario_mao_de_obra = 0.0000
        self.custo_execucao = 0.0000
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
        codigo = str( codigo )
        codigo = codigo.zfill(7)
        return codigo

    def obter_valor_bdi( self ):
        if self.diferenciado:
            bdi = self.bdi.diferenciado
        else:
            bdi = self.bdi.principal
        return bdi

    def configurar_custo_execucao( self ) -> float:
        self.custo_execucao = self.obj_arred.custo( self.custo_horario_equipamento + self.custo_horario_mao_de_obra )
        return self.custo_execucao

    def configurar_custo_unitario_execucao( self ) -> float:
        self.custo_unitario_execucao = self.obj_arred.custo( self.custo_execucao / self.produtividade )
        return self.custo_unitario_execucao

    def configurar_custo_fic( self ) -> float:
        self.custo_fic = self.obj_arred.custo( self.custo_unitario_execucao * self.fic )
        return self.custo_fic

    def configurar_custo_fit( self ) -> float:
        self.custo_fit = self.obj_arred.custo( self.custo_unitario_execucao * self.fit )
        return self.custo_fit

    def configurar_custo_bdi( self ) -> float:
        self.custo_bdi = self.obj_arred.custo( self.custo_unitario_total * self.bdi_valor_utilizado )
        return self.custo_bdi

    def configurar_custo_unitario_total( self ) -> float:
        custos_execucao = self.custo_unitario_execucao + self.custo_fic + self.custo_fit
        custos_atividades_auxiliares = self.custo_total_atividade_auxiliar + self.custo_total_tempo_fixo + self.custo_total_transporte
        self.custo_unitario_total = self.obj_arred.custo( custos_execucao + self.custo_unitario_material + custos_atividades_auxiliares )
        return self.custo_unitario_total

    def configurar_preco_unitario_total( self ) -> float:
        self.preco_unitario_total = self.obj_arred.monetario( self.custo_bdi + self.custo_unitario_total )
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
        self.configurar_linha_custo_execucao()

    def configurar_linha_custo_execucao( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo horário de execução'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.execucao
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_execucao
        self.linha[ self.obj_col_dfr.custo_total ] = self.obj_arred.custo( self.composicao.configurar_custo_execucao() )


class LinhaCustoUnitarioExecucaoDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_custo_unitario_execucao()

    def configurar_linha_custo_unitario_execucao( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo unitário de execução'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.unitario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_unitario_execucao
        self.linha[ self.obj_col_dfr.custo_total ] = self.obj_arred.custo( self.composicao.configurar_custo_unitario_execucao() )


class LinhaFatorInfluenciaChuvaDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_subtotal_fic()

    def configurar_linha_subtotal_fic( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo do FIC'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.unitario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_unitario_fic
        self.linha[ self.obj_col_dfr.quantidade ] = self.composicao.fic
        self.linha[ self.obj_col_dfr.preco_unitario ] = self.composicao.custo_unitario_execucao
        self.linha[ self.obj_col_dfr.custo_total ] = self.obj_arred.custo( self.composicao.configurar_custo_fic() )


class LinhaFatorInterferenciaTrafegoDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_subtotal_fit()

    def configurar_linha_subtotal_fit( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo do FIT'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.unitario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_unitario_fit
        self.linha[ self.obj_col_dfr.quantidade ] = self.composicao.fit
        self.linha[ self.obj_col_dfr.preco_unitario ] = self.composicao.custo_unitario_execucao
        self.linha[ self.obj_col_dfr.custo_total ] = self.obj_arred.custo( self.composicao.configurar_custo_fit() )


class LinhaBdiDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_subtotal_bdi()

    def configurar_linha_subtotal_bdi( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Custo do BDI'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.direto_total
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.subtotal_unitario_bdi
        self.linha[ self.obj_col_dfr.quantidade ] = self.composicao.bdi_valor_utilizado
        self.linha[ self.obj_col_dfr.preco_unitario ] = self.composicao.custo_unitario_total
        self.linha[ self.obj_col_dfr.custo_total ] = self.obj_arred.custo( self.composicao.configurar_custo_bdi() )


class LinhaPrecoUnitarioDF(LinhaDF):

    def __init__( self, _dfr_insumo, composicao, obj_col ) -> None:
        super().__init__(_dfr_insumo, composicao, obj_col)
        self.configurar_linha_preco_unitario()

    def configurar_linha_preco_unitario( self ) -> None:
        self.linha[ self.obj_col_dfr.descricao ] = 'Preço unitário'
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.preco_unitario
        self.linha[ self.obj_col_dfr.grupo ] = self.obj_grupo.total_preco_unitario
        self.linha[ self.obj_col_dfr.custo_total ] = self.obj_arred.custo( self.composicao.configurar_preco_unitario_total() )


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
        self.linha[ self.obj_col_dfr.codigo ] = self.obj_codigo.direto_total
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
        
        self.configurar_codigo_composicao_principal()
        
        self.calcular_subtotal_simples()

        # self.obter_lis_tr()


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

    def criar_linha_custo_execucao( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaCustoHorarioExecucaoDF:
        return LinhaCustoHorarioExecucaoDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_custo_unitario_execucao( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaCustoUnitarioExecucaoDF:
        return LinhaCustoUnitarioExecucaoDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_custo_fic( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaFatorInfluenciaChuvaDF:
        return LinhaFatorInfluenciaChuvaDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_custo_fit( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaFatorInterferenciaTrafegoDF:
        return LinhaFatorInterferenciaTrafegoDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_custo_bdi( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaBdiDF:
        return LinhaBdiDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_preco_unitario( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaPrecoUnitarioDF:
        return LinhaPrecoUnitarioDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_subtotal_atividade_auxiliar(self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaAtividadeAuxiliarDF:
        return LinhaAtividadeAuxiliarDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_subtotal_tempo_fixo( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaTempoFixoDF:
        return LinhaTempoFixoDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_subtotal_transporte( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaTransporteDF:
        return LinhaTransporteDF( _dfr_insumo, composicao, obj_col )

    def criar_linha_custo_direto_total( self, _dfr_insumo: pd.core.frame.DataFrame, composicao: ComposicaoDB, obj_col: ListaColunaComposicaoDF ) -> LinhaCustoUnitarioDiretoTotalDF:
        return LinhaCustoUnitarioDiretoTotalDF( _dfr_insumo, composicao, obj_col )

    def obter_dfr_equipamento( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format( self.obj_col_dfr.grupo, self.obj_grupo.insumo_equipamento ) )

    def obter_dfr_mao_de_obra( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format( self.obj_col_dfr.grupo, self.obj_grupo.insumo_mao_de_obra ) )

    def obter_dfr_material( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format( self.obj_col_dfr.grupo, self.obj_grupo.insumo_material ) )

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

    def obter_dfr_execucao( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format(self.obj_col_dfr.grupo, self.obj_grupo.subtotal_execucao ) )

    def obter_dfr_subtotal_execucao( self ):
        obj_linha_he = self.criar_linha_custo_execucao( self.obter_dfr_execucao(), self.composicao, self.obj_col_dfr )
        return obj_linha_he

    def obter_dfr_unitario_execucao( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format(self.obj_col_dfr.grupo, self.obj_grupo.subtotal_unitario_execucao ) )

    def obter_dfr_subtotal_unitario_execucao( self ):
        obj_linha_ue = self.criar_linha_custo_unitario_execucao( self.obter_dfr_unitario_execucao(), self.composicao, self.obj_col_dfr )
        return obj_linha_ue

    def obter_dfr_fic( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format(self.obj_col_dfr.grupo, self.obj_grupo.subtotal_unitario_fic ) )

    def obter_dfr_custo_fic( self ):
        obj_linha_fic = self.criar_linha_custo_fic( self.obter_dfr_fic(), self.composicao, self.obj_col_dfr )
        return obj_linha_fic

    def obter_dfr_fit( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format(self.obj_col_dfr.grupo, self.obj_grupo.subtotal_unitario_fit ) )

    def obter_dfr_custo_fit( self ):
        obj_linha_fit = self.criar_linha_custo_fit( self.obter_dfr_fit(), self.composicao, self.obj_col_dfr )
        return obj_linha_fit

    def obter_dfr_bdi( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format(self.obj_col_dfr.grupo, self.obj_grupo.subtotal_unitario_bdi ) )

    def obter_dfr_custo_bdi( self ):
        obj_linha_bdi = self.criar_linha_custo_bdi( self.obter_dfr_bdi(), self.composicao, self.obj_col_dfr )
        return obj_linha_bdi

    def obter_dfr_pu( self ) -> pd.core.frame.DataFrame:
        return self.dfr_insumo.query( '{} == {}'.format(self.obj_col_dfr.grupo, self.obj_grupo.total_preco_unitario ) )

    def obter_dfr_preco_unitario( self ):
        obj_linha_pu = self.criar_linha_preco_unitario( self.obter_dfr_pu(), self.composicao, self.obj_col_dfr )
        return obj_linha_pu

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
        obj_linha_he = self.obter_dfr_subtotal_execucao()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_he.linha, ignore_index=True )
        # unitário execução
        obj_linha_ue = self.obter_dfr_subtotal_unitario_execucao()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_ue.linha, ignore_index=True )
        # fic
        obj_linha_fic = self.obter_dfr_custo_fic()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_fic.linha, ignore_index=True )
        # fit
        obj_linha_fit = self.obter_dfr_custo_fit()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_fit.linha, ignore_index=True )

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
        obj_linha_cd = self.criar_linha_custo_direto_total( self.obter_dfr_unitario_direto(), self.composicao, self.obj_col_dfr )
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
        # bdi
        obj_linha_bdi = self.obter_dfr_custo_bdi()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_bdi.linha, ignore_index=True )
        # preço unitário
        obj_linha_pu = self.obter_dfr_preco_unitario()
        self.dfr_insumo = self.dfr_insumo.append( obj_linha_pu.linha, ignore_index=True )

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
        lista = [ self.obj_grupo.linha_vazia_inicial, self.obj_grupo.linha_vazia_equipamento, self.obj_grupo.linha_vazia_mao_de_obra, self.obj_grupo.linha_vazia_execucao, self.obj_grupo.linha_vazia_material, self.obj_grupo.linha_vazia_atividade_auxiliar, self.obj_grupo.linha_vazia_tempo_fixo, self.obj_grupo.linha_vazia_transporte ]
        for item in lista:
            self.dfr_insumo = self.dfr_insumo.append( [ { self.obj_col_dfr.composicao_principal : self.composicao.codigo, self.obj_col_dfr.grupo : item } ], ignore_index=True )

    def configurar_codigo_composicao_principal( self ) -> None:
        self.dfr_insumo[ self.obj_col_dfr.composicao_principal ] = self.composicao.codigo

    def obter_lis_aa( self, codigo ):
        consulta = self.base.dfr_apropriacao_in.query( "{} == '{}' & Grupo == {}".format( self.obj_col_dfr.composicao_principal, codigo, self.obj_grupo.insumo_atividade_auxiliar ) )
        return consulta

    def obter_lis_tr( self ):
        dfr_aa = self.obter_lis_aa( self.composicao.codigo )
        lista_aa = dfr_aa[['Composicao_principal','Código','Quantidade']].to_dict(orient='records')
        for item in lista_aa:
            print( str(item['Composicao_principal']) + ' ; ' + str(item['Código']) + ' ; ' + str(item['Quantidade']) )


class Servico:

    def __init__(self, codigo: str, quantidade: float, diferenciado: bool) -> None:
        self.codigo = codigo
        self.diferenciado = diferenciado
        self.quantidade = quantidade


class Projeto:

    def __init__(self, lista_servico: list, baseDF: BaseDF, bdi: BonificacaoDespesasIndiretas) -> None:
        self.baseDF = baseDF
        self.bdi = bdi
        self.onerado = self.bdi.onerado
        self.obj_col_dfr = ListaColunaComposicaoDF(self.onerado)
        self.obj_bdi_zero = BonificacaoDespesasIndiretas(0.0, 0.0, self.onerado)
        self.obj_grupo = Grupo()
        self.servicos = lista_servico
        self.composicoes_projeto = list()
        self.transportes_projeto = list()
        self.composicoes_com_bdi = list()
        self.equipamento_projeto = list()
        self.mao_de_obra_projeto = list()
        self.material_projeto = list()
        self.dic_db_projeto = dict()
        self.dic_df_composicao = dict()
        self.lista_auxiliar = list()
        self.configurar_lista_composicoes_projeto()
        self.gerar_dicionario_dados_basicos_composicoes_projeto()
        self.obter_lista_atividades_auxiliares_servicos_projeto()

    def configurar_lista_composicoes_projeto( self ):
        for item in self.servicos:
            self.composicoes_projeto.append( self.tratar_codigo_composicao( item.codigo ) )
        self.composicoes_com_bdi = self.composicoes_projeto.copy()

    def instanciar_composicao_db( self, codigo: str, posicao_em_servicos: int ) -> ComposicaoDB:
        if codigo in self.composicoes_com_bdi:
            obj_composicao_db = ComposicaoDB( codigo, self.bdi, self.servicos[posicao_em_servicos].diferenciado )
        else:
            obj_composicao_db = ComposicaoDB( codigo, self.obj_bdi_zero )
        return obj_composicao_db

    def instanciar_composicao_df( self, obj_composicao_db: ComposicaoDB ) -> ComposicaoDF:
        return ComposicaoDF( obj_composicao_db, self.baseDF ) 

    def obter_lis_insumo_projeto( self, lista_auxiliar: list, lista_projeto: list ) -> list:
        if( lista_auxiliar != None):
            for item in lista_auxiliar:
                item = item[1]
                if item not in lista_projeto:
                    lista_projeto.append( item ) 
        return lista_projeto

    def obter_lista_auxiliar( self, lista_auxiliar: list ) -> list:
        if ( lista_auxiliar != None):
            for item in lista_auxiliar:
                item = item[1]
                self.lista_auxiliar.append( item )
        return self.lista_auxiliar

    def gerar_dicionario_dados_basicos_composicoes_projeto( self ):
        for i, codigo in enumerate(self.composicoes_projeto):

            obj_composicao_db = self.instanciar_composicao_db( codigo, i )
            obj_composicao_df = self.instanciar_composicao_df( obj_composicao_db )   

            self.dic_db_projeto[ obj_composicao_db.codigo ] = obj_composicao_db
            self.dic_df_composicao[ obj_composicao_db.codigo ] = obj_composicao_df
           
            self.lista_auxiliar.append( codigo )
            self.composicoes_projeto = self.obter_lis_insumo_projeto( obj_composicao_df.obter_lis_atividade_auxiliar(), self.composicoes_projeto )
            self.lista_auxiliar = self.obter_lista_auxiliar( obj_composicao_df.obter_lis_atividade_auxiliar() )
            self.equipamento_projeto = self.obter_lis_insumo_projeto( obj_composicao_df.obter_lis_equipamento(), self.equipamento_projeto )
            self.mao_de_obra_projeto = self.obter_lis_insumo_projeto( obj_composicao_df.obter_lis_mao_de_obra(), self.mao_de_obra_projeto )
            self.material_projeto = self.obter_lis_insumo_projeto( obj_composicao_df.obter_lis_material(), self.material_projeto )

    def tratar_composicoes_projeto(self) -> list:
        lista_auxiliar_reversa = list()
        while( len( self.lista_auxiliar ) != 0 ):
            ultimo = self.lista_auxiliar[-1]
            if ultimo not in lista_auxiliar_reversa:
                lista_auxiliar_reversa.append( ultimo )
            self.lista_auxiliar.pop()
        return lista_auxiliar_reversa

    def tratar_codigo_composicao( self, codigo: str ) -> str:
        codigo = str( codigo )
        codigo = codigo.zfill(7)
        return codigo

    def obter_dfr_composicao( self ) -> dict:
        lista_auxiliar_reversa = self.tratar_composicoes_projeto()
        for item in lista_auxiliar_reversa:
            self.dic_df_composicao[ item ].calcular_custo_atividade_auxiliar( self.dic_db_projeto )
            self.dic_df_composicao[ item ].calcular_subtotal_composto()
            self.dic_df_composicao[ item ].criar_linhas_vazias()
            self.dic_df_composicao[ item ].dfr_insumo.sort_values( by =[ self.dic_df_composicao[ item ].obj_col_dfr.grupo, self.dic_df_composicao[ item ].obj_col_dfr.item_transporte ], inplace=True )
            self.dic_df_composicao[ item ].dfr_insumo.reset_index( drop=True, inplace=True )
        return self.dic_df_composicao
    
    def obter_dfr_equipamento( self ) -> pd.core.frame.DataFrame:
        dfr_equipamento = pd.DataFrame({'Código': self.equipamento_projeto})
        dfr_equipamento = pd.merge( dfr_equipamento, self.baseDF.dfr_dados_in, on='Código', how='left' )
        dfr_equipamento = pd.merge( dfr_equipamento, self.baseDF.dfr_custo_in, on='Código', how='left' )
        lista_colunas_eq = ['Grupo', 'Origem_x', 'Estado_x', 'Publicacao_x', 'Código', 'Descrição', 'Unidade', 'Custo produtivo desonerado', 'Custo improdutivo desonerado']
        return dfr_equipamento[lista_colunas_eq]
    
    def obter_dfr_mao_de_obra( self ) -> pd.core.frame.DataFrame:
        dfr_mao_de_obra = pd.DataFrame({'Código': self.mao_de_obra_projeto})
        dfr_mao_de_obra = pd.merge( dfr_mao_de_obra, self.baseDF.dfr_dados_in, on='Código', how='left' )
        dfr_mao_de_obra = pd.merge( dfr_mao_de_obra, self.baseDF.dfr_custo_in, on='Código', how='left' )
        lista_colunas_mo = ['Grupo', 'Origem_x', 'Estado_x', 'Publicacao_x', 'Código', 'Descrição', 'Unidade', 'Custo produtivo desonerado']
        return dfr_mao_de_obra[lista_colunas_mo]
    
    def obter_dfr_material( self ) -> pd.core.frame.DataFrame:
        dfr_material = pd.DataFrame({'Código': self.material_projeto})
        dfr_material = pd.merge( dfr_material, self.baseDF.dfr_dados_in, on='Código', how='left' )
        dfr_material = pd.merge( dfr_material, self.baseDF.dfr_custo_in, on='Código', how='left' )
        lista_colunas_ma = ['Grupo', 'Origem_x', 'Estado_x', 'Publicacao_x', 'Código', 'Descrição', 'Unidade', 'Preço unitário']
        return dfr_material[lista_colunas_ma]

    def obter_lista_transportes_servico( self, codigo ):
        consulta = self.baseDF.dfr_apropriacao_in.query( "{} == '{}' & Grupo == {}".format( self.obj_col_dfr.composicao_principal, codigo, self.obj_grupo.insumo_transporte ) )
        return consulta

    def obter_lista_auxiliares_servico( self, codigo ):
        consulta = self.baseDF.dfr_apropriacao_in.query( "{} == '{}' & Grupo == {}".format( self.obj_col_dfr.composicao_principal, codigo, self.obj_grupo.insumo_atividade_auxiliar ) )
        consulta = consulta[[self.obj_col_dfr.composicao_principal, self.obj_col_dfr.codigo, self.obj_col_dfr.quantidade]].values.tolist()
        return consulta

    def obter_lista_atividades_auxiliares_servicos_projeto( self ) -> list:
        lista_primaria = list()
        for item in self.servicos:

            quantidade = 1.0

            obj_arvore_servico = Arvore( self.baseDF, self.obj_col_dfr, self.obj_grupo )
            
            encapsulada = Capsula( item.codigo, item.codigo, quantidade )

            obj_arvore_servico.inserir_auxiliar_noh_arvore( encapsulada )

            print( obj_arvore_servico.obter_lista_auxiliares_noh_arvore_in_order() )
            
        return lista_primaria