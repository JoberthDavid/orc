import numpy as np
import pandas as pd
from funcoes import arred
from constantes import *


class GeradorDF:
    """Classe que gera um Data Frame e trata as suas colunas"""

    def __init__(self, arquivo: str) -> None:
        self.df = self.carregar_dados(arquivo)

    def carregar_dados( self, arquivo ) -> pd.core.frame.DataFrame:
        return pd.read_csv( arquivo, encoding=UTF )

    def tratar_df(self, lista=list()) -> pd.core.frame.DataFrame:
        self.df.columns = COLUNAS_DF_ORIGEM_CP + lista
        if lista[-1] == 'NONE':
            self.df.pop('NONE')
        return self.df


class BaseDF:
    """Classe que reune a base de Data Frame necessários para o projeto"""
    
    def __init__(self, arq_db_cp: str, arq_db_in: str, arq_apr_in: str, arq_cto_in: str) -> None:
        df_db_cp = GeradorDF(arq_db_cp)
        df_db_in = GeradorDF(arq_db_in)
        df_apr_in = GeradorDF(arq_apr_in)
        df_cto_in = GeradorDF(arq_cto_in)        
        self.df_dados_cp = self.tratar_df_dados_basicos_cp( df_db_cp )
        self.df_dados_in = self.tratar_df_dados_basicos_in( df_db_in )
        self.df_apropriacao_in = self.tratar_df_apropriacao_in( df_apr_in )
        self.df_custo_in = self.tratar_df_custo_in( df_cto_in )

    def tratar_df_dados_basicos_cp( self, df_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        return df_db.tratar_df( COLUNAS_DF_DADOS_BASICO_CP )

    def tratar_df_dados_basicos_in( self, df_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        return df_db.tratar_df( COLUNAS_DF_DADOS_BASICO_IN )

    def tratar_df_apropriacao_in( self, df_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        return df_db.tratar_df( COLUNAS_DF_APROPRIACAO_IN )

    def tratar_df_custo_in( self, df_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        return df_db.tratar_df( COLUNAS_DF_CUSTO_IN )

    def max_apr( self ) -> int:
        return self.df_apropriacao_in.groupby('Composicao_principal').size().max()


class ComposicaoDB:
    """Classe que representa os parâmetros mais importantes de cada composição do projeto"""

    def __init__(self, codigo: str, onerado=True) -> None:
        self.codigo = self.tratar_codigo_composicao( codigo )
        self.onerado = onerado
        self.descricao = ''
        self.unidade = ''
        self.fic = 0.0
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

    def calcular_custo_horario_execucao(self) -> float:
        self.custo_horario_execucao = arred( self.custo_horario_equipamento + self.custo_horario_mao_de_obra )
        return self.custo_horario_execucao

    def calcular_custo_unitario_execucao(self) -> float:
        self.custo_unitario_execucao = arred( self.custo_horario_execucao / self.produtividade )
        return self.custo_unitario_execucao

    def calcular_custo_unitario_total(self) -> float:
        self.custo_unitario_total = arred( self.custo_unitario_execucao + self.custo_unitario_material + self.custo_total_atividade_auxiliar + self.custo_total_tempo_fixo + self.custo_total_transporte )
        return self.custo_unitario_total

    def calcular_preco_unitario_total(self) -> float:
        self.preco_unitario_total = arred( self.custo_bdi + self.custo_unitario_total )
        return self.preco_unitario_total


class ComposicaoDF:
    """Classe que representa os data frames de cada composição do projeto que servirão para imprimir no arquivo Excel"""

    def __init__(self, composicao: ComposicaoDB, base: BaseDF) -> None:
        self.index_grupo = 'Grupo_x'
        self.composicao = composicao
        self.base = base
        self.df_dados_basicos = self.base.df_dados_cp
        self.df_custo_in = self.base.df_custo_in
        self.composicao.descricao = self.obter_descricao_composicao()
        self.composicao.unidade = self.obter_unidade_composicao()
        self.composicao.fic = self.obter_fic_composicao()
        self.composicao.produtividade = self.obter_produtividade_composicao()

        self.df_insumo = self.associar_custos_apropriacoes_insumos()
        self.inserir_coluna_dmt()
        self.configurar_custo_equipamento()
        self.configurar_custo_mao_de_obra()
        self.configurar_custo_material()
        self.df_insumo = self.df_insumo[ self.obter_lista_colunas() ]

        self.configurar_filtro_grupo()
        self.calcular_subtotal_simples()
        self.calcular_custo_horario_execucao()
        self.calcular_custo_unitario_execucao()

    def obter_df_dados_basicos_insumos( self ) -> pd.core.frame.DataFrame:
        return self.base.df_dados_in.query( "Código == '{}'".format( self.composicao.codigo ) )

    def obter_df_dados_basicos_composicao( self ) -> pd.core.frame.DataFrame:
        return self.base.df_dados_cp.query( "Composicao_principal == '{}'".format( self.composicao.codigo ) )

    def obter_df_apropriacoes_insumos( self ) -> pd.core.frame.DataFrame:
        return self.base.df_apropriacao_in.query( "Composicao_principal == '{}'".format( self.composicao.codigo ) )

    def obter_descricao_composicao( self ) -> str:
        auxiliar = self.obter_df_dados_basicos_insumos()
        return auxiliar['Descrição'].values[0]

    def obter_unidade_composicao( self ) -> str:
        auxiliar = self.obter_df_dados_basicos_insumos()
        return auxiliar['Unidade'].values[0]

    def obter_fic_composicao( self ) -> float:
        auxiliar = self.obter_df_dados_basicos_composicao()
        return auxiliar['FIC'].values[0]
    
    def obter_produtividade_composicao( self ) -> float:
        auxiliar = self.obter_df_dados_basicos_composicao()
        return auxiliar['Produtividade'].values[0]

    def associar_dados_basicos_apropriacoes_insumos( self ) -> pd.core.frame.DataFrame:
        return pd.merge( self.obter_df_apropriacoes_insumos(), self.base.df_dados_in, on='Código', how='left' )

    def obter_desoneracao_mao_de_obra( self ) -> str:
        if self.composicao.onerado:
            encargos_mao_de_obra = 'onerado'
        else:
            encargos_mao_de_obra = 'desonerado'
        return encargos_mao_de_obra

    def obter_descricao_custo_produtivo( self ) -> str:
        return 'Custo pro {}'.format( self.obter_desoneracao_mao_de_obra() )

    def obter_descricao_custo_improdutivo(self) -> str:
        return 'Custo imp {}'.format( self.obter_desoneracao_mao_de_obra() )

    def inserir_coluna_dmt( self ) -> None:
        self.df_insumo['DMT'] = ''

    def obter_lista_colunas( self ) -> list:
        self.lista_colunas = ['Composicao_principal', self.index_grupo, 'Código', 'Descrição', 'Item transporte', 'DMT', 'Unidade', 'Quantidade', 'Utilização', self.obter_descricao_custo_produtivo(), self.obter_descricao_custo_improdutivo(),'Preço unitário', 'Custo total']
        return self.lista_colunas

    def associar_custos_apropriacoes_insumos( self ) -> pd.core.frame.DataFrame:
        return pd.merge( self.associar_dados_basicos_apropriacoes_insumos(), self.df_custo_in, on='Código', how='left')

    def calcular_custo_equipamento( self ) -> pd.core.series.Series:
        qt = self.df_insumo['Quantidade']
        cp = self.df_insumo[ self.obter_descricao_custo_produtivo() ]
        ci = self.df_insumo[ self.obter_descricao_custo_improdutivo() ]
        ut = self.df_insumo['Utilização']
        return arred( qt * ( ( ut * cp ) + ( ( 1 - ut ) * ci ) ) )

    def calcular_custo_mao_de_obra( self ) -> pd.core.series.Series:
        qt = self.df_insumo['Quantidade']
        cp = self.df_insumo[ self.obter_descricao_custo_produtivo() ]
        return arred( qt * cp )

    def calcular_custo_material( self ) -> pd.core.series.Series:
        qt = self.df_insumo['Quantidade']
        pu = self.df_insumo['Preço unitário']
        return arred( qt * pu )

    def configurar_custo_equipamento( self ) -> pd.core.series.Series:
        self.df_insumo.loc[self.df_insumo[self.index_grupo] == EQUIPAMENTO, 'Custo total'] = self.calcular_custo_equipamento()
        return self.df_insumo.loc[self.df_insumo[self.index_grupo] == EQUIPAMENTO, 'Custo total']

    def configurar_custo_mao_de_obra( self ) -> pd.core.series.Series:
        self.df_insumo.loc[self.df_insumo[self.index_grupo] == MAO_DE_OBRA, 'Custo total'] = self.calcular_custo_mao_de_obra()
        return self.df_insumo.loc[self.df_insumo[self.index_grupo] == MAO_DE_OBRA, 'Custo total']

    def configurar_custo_material( self ) -> pd.core.series.Series:
        self.df_insumo.loc[self.df_insumo[self.index_grupo] == MATERIAL, 'Custo total'] = self.calcular_custo_material()
        return self.df_insumo.loc[self.df_insumo[self.index_grupo] == MATERIAL, 'Custo total']

    def configurar_filtro_grupo( self ) -> None:
        self.df_insumo = self.df_insumo.set_index( self.index_grupo )

####################

    def calcular_custo_atividade_auxiliar( self, dicionario: dict ) -> None:
        lista = self.obter_lista_atividade_auxiliar()
        for item in lista:
            grupo = item[0]
            item = item[1]
            self.df_insumo.loc[ self.df_insumo['Código'] == item,'Preço unitário'] = dicionario[ item ].custo_unitario_total 
            qt = self.df_insumo.loc[ self.df_insumo['Código'] == item, 'Quantidade']
            pu = self.df_insumo.loc[ self.df_insumo['Código'] == item, 'Preço unitário']
            if (grupo == TRANSPORTE): 
                dt = self.df_insumo.loc[ self.df_insumo['Código'] == item, 'DMT'] = 0
                self.df_insumo.loc[ self.df_insumo['Código'] == item, 'Custo total'] = arred( dt * qt * pu )
            else:
                self.df_insumo.loc[ self.df_insumo['Código'] == item, 'Custo total'] = arred( qt * pu )

    def calcular_custo_horario_execucao( self ) -> None:
        self.composicao.calcular_custo_unitario_execucao()
        for composicao, _df_insumo in self.df_insumo.groupby( ['Composicao_principal', 'Código'] ):
            codigo = composicao[1]
            auxiliar = None
            if ( codigo == CODIGO_HORARIO ):
                auxiliar = _df_insumo[['Custo total']].sum().rename( EXECUCAO_HORARIO )
                auxiliar['Composicao_principal'] = composicao[0]
                auxiliar['Descrição'] = 'Custo horário de execução'
                auxiliar['Código'] = CODIGO_HORARIO_EXECUCAO
                auxiliar['Custo total'] = self.composicao.custo_horario_execucao
                self.df_insumo = self.df_insumo.append( auxiliar )

    def calcular_custo_unitario_execucao( self ) -> None:
        for composicao, _df_insumo in self.df_insumo.groupby( ['Composicao_principal', 'Código'] ):
            codigo = composicao[1]
            auxiliar = None
            if ( codigo == CODIGO_HORARIO_EXECUCAO ):
                auxiliar = _df_insumo[['Custo total']].sum().rename( EXECUCAO_UNITARIO )
                auxiliar['Composicao_principal'] = composicao[0]
                auxiliar['Descrição'] = 'Custo unitário de execução'
                auxiliar['Código'] = CODIGO_UNITARIO
                auxiliar['Custo total'] = self.composicao.custo_unitario_execucao
                self.df_insumo = self.df_insumo.append( auxiliar )

    def calcular_custo_unitario_direto_total( self ) -> None:
        self.composicao.calcular_custo_unitario_execucao()
        for composicao, _df_insumo in self.df_insumo.groupby( ['Composicao_principal', 'Código'] ):
            codigo = composicao[1]
            auxiliar = None
            if ( codigo == CODIGO_UNITARIO ):
                auxiliar = _df_insumo[['Custo total']].sum().rename( DIRETO_TOTAL_UNITARIO )
                auxiliar['Composicao_principal'] = composicao[0]
                auxiliar['Descrição'] = 'Custo unitário direto total'
                auxiliar['Código'] = CODIGO_UNITARIO_DIRETO_TOTAL
                self.composicao.custo_unitario_total = auxiliar['Custo total']
                self.df_insumo = self.df_insumo.append( auxiliar )

    def calcular_subtotal_simples( self ) -> None:
        for composicao, _df_insumo in self.df_insumo.groupby( ['Composicao_principal', self.index_grupo] ):
            grupo = composicao[1]
            auxiliar = None
            if ( grupo == EQUIPAMENTO ):
                auxiliar = _df_insumo[['Custo total']].sum().rename( EQUIPAMENTO_CUSTO_HORARIO )
                auxiliar['Composicao_principal'] = composicao[0]
                auxiliar['Descrição'] = 'Custo horário equipamento'
                auxiliar['Código'] = CODIGO_HORARIO
                self.composicao.custo_horario_equipamento = auxiliar['Custo total']
                self.composicao.calcular_custo_horario_execucao()
                self.composicao.calcular_custo_unitario_execucao()
            elif ( grupo == MAO_DE_OBRA ):
                auxiliar = _df_insumo[['Custo total']].sum().rename( MAO_DE_OBRA_CUSTO_HORARIO )
                auxiliar['Composicao_principal'] = composicao[0]
                auxiliar['Descrição'] = 'Custo horário mão de obra'
                auxiliar['Código'] = CODIGO_HORARIO
                self.composicao.custo_horario_mao_de_obra = auxiliar['Custo total']
                self.composicao.calcular_custo_horario_execucao()
                self.composicao.calcular_custo_unitario_execucao()
            elif ( grupo == MATERIAL ):
                auxiliar = _df_insumo[['Custo total']].sum().rename( MATERIAL_CUSTO_UNITARIO )
                auxiliar['Composicao_principal'] = composicao[0]
                auxiliar['Descrição'] = 'Custo unitário material'
                auxiliar['Código'] = CODIGO_UNITARIO
                self.composicao.custo_unitario_material = auxiliar['Custo total']
            self.df_insumo = self.df_insumo.append( auxiliar )

    def calcular_subtotal_composto( self ) -> None:
        for composicao, _df_insumo in self.df_insumo.groupby( ['Composicao_principal', self.index_grupo] ):
            grupo = composicao[1]
            auxiliar = None
            if ( grupo == ATIVIDADE_AUXILIAR ):
                auxiliar = _df_insumo[['Custo total']].sum().rename( ATIVIDADE_AUXILIAR_CUSTO_TOTAL )
                auxiliar['Composicao_principal'] = composicao[0]
                auxiliar['Descrição'] = 'Custo unitário atividade auxiliar'
                auxiliar['Código'] = CODIGO_UNITARIO
                self.composicao.custo_total_atividade_auxiliar = auxiliar['Custo total']
            elif ( grupo == TEMPO_FIXO ):
                auxiliar = _df_insumo[['Custo total']].sum().rename( TEMPO_FIXO_CUSTO_TOTAL )
                auxiliar['Composicao_principal'] = composicao[0]
                auxiliar['Descrição'] = 'Custo unitário tempo fixo'
                auxiliar['Código'] = CODIGO_UNITARIO
                self.composicao.custo_total_tempo_fixo = auxiliar['Custo total']
            elif ( grupo == TRANSPORTE ):
                auxiliar = _df_insumo[['Custo total']].sum().rename( TRANSPORTE_CUSTO_TOTAL )
                auxiliar['Composicao_principal'] = composicao[0]
                auxiliar['Descrição'] = 'Custo unitário transporte'
                auxiliar['Código'] = CODIGO_UNITARIO
                self.composicao.custo_total_transporte = auxiliar['Custo total']
            self.df_insumo = self.df_insumo.append( auxiliar )

    def obter_operador_lista_insumo( self, insumo: int ) -> str:
        operador = '=='
        if insumo == ATIVIDADE_AUXILIAR:
            operador = '>='
        return operador

    def configurar_lista_insumo( self, consulta: pd.core.frame.DataFrame ) -> list:
        lista = list()
        if len( consulta[['Grupo', 'Código']].values ) != 0:
            for item in consulta[['Grupo', 'Código']].values:
                lista.append( item )
        return lista

    def obter_lista_insumo( self, insumo: int ) -> list:
        operador = self.obter_operador_lista_insumo(insumo)
        consulta = self.base.df_apropriacao_in.query( "Composicao_principal == '{}' & Grupo {} {}".format( self.composicao.codigo, operador, insumo ) )
        return self.configurar_lista_insumo( consulta )

    def obter_lista_atividade_auxiliar( self ) -> list:
        return self.obter_lista_insumo(ATIVIDADE_AUXILIAR)

    def obter_lista_equipamento( self ) -> list:
        return self.obter_lista_insumo(EQUIPAMENTO)

    def obter_lista_mao_de_obra( self ) -> list:
        return self.obter_lista_insumo(MAO_DE_OBRA)
    
    def obter_lista_material( self ) -> list:
        return self.obter_lista_insumo(MATERIAL)