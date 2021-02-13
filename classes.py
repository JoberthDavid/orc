import numpy as np
import pandas as pd
from funcoes import arred
from constantes import *


class GeradorDF:
    """Classe que gera um Data Frame e trata as suas colunas"""

    def __init__(self, arquivo: str) -> None:
        self.dfr = self.carregar_dados(arquivo)

    def carregar_dados( self, arquivo ) -> pd.core.frame.DataFrame:
        return pd.read_csv( arquivo, encoding=UTF )

    def tratar_dfr(self, lista=list()) -> pd.core.frame.DataFrame:
        self.dfr.columns = COLUNAS_DFR_ORIGEM_CP + lista
        if lista[-1] == 'NONE':
            self.dfr.pop('NONE')
        return self.dfr


class BaseDF:
    """Classe que reune a base de Data Frame necessários para o projeto"""
    
    def __init__(self, arq_db_cp: str, arq_db_in: str, arq_apr_in: str, arq_cto_in: str) -> None:
        dfr_db_cp = GeradorDF(arq_db_cp)
        dfr_db_in = GeradorDF(arq_db_in)
        dfr_apr_in = GeradorDF(arq_apr_in)
        dfr_cto_in = GeradorDF(arq_cto_in)        
        self.dfr_dados_cp = self.tratar_dfr_dados_basicos_cp( dfr_db_cp )
        self.dfr_dados_in = self.tratar_dfr_dados_basicos_in( dfr_db_in )
        self.dfr_apropriacao_in = self.tratar_dfr_apropriacao_in( dfr_apr_in )
        self.dfr_custo_in = self.tratar_dfr_custo_in( dfr_cto_in )

    def tratar_dfr_dados_basicos_cp( self, dfr_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        return dfr_db.tratar_dfr( COLUNAS_DFR_DADOS_BASICO_CP )

    def tratar_dfr_dados_basicos_in( self, dfr_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        return dfr_db.tratar_dfr( COLUNAS_DFR_DADOS_BASICO_IN )

    def tratar_dfr_apropriacao_in( self, dfr_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        return dfr_db.tratar_dfr( COLUNAS_DFR_APROPRIACAO_IN )

    def tratar_dfr_custo_in( self, dfr_db: pd.core.frame.DataFrame ) -> pd.core.frame.DataFrame:
        return dfr_db.tratar_dfr( COLUNAS_DFR_CUSTO_IN )

    def max_apr( self ) -> int:
        return self.dfr_apropriacao_in.groupby('Composicao_principal').size().max()


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


class LinhaDF:

    def __init__(self, _dfr_insumo, composicao) -> None:
        self.linha = _dfr_insumo[['Custo total']].sum()
        self.linha['Composicao_principal'] = composicao
        self.composicao = self.linha['Composicao_principal']
        self.total = self.linha['Custo total']

class LinhaEquipamentoDF(LinhaDF):

    def __init__(self, _dfr_insumo, composicao) -> None:
        super().__init__(_dfr_insumo, composicao)
        self.configurar_linha_subtotal_equipamento()
        
    def configurar_linha_subtotal_equipamento(self) -> None:
        self.linha['Descrição'] = 'Custo horário equipamento'
        self.linha['Código'] = CODIGO_HORARIO
        self.linha['Grupo_x'] = EQUIPAMENTO_CUSTO_HORARIO


class LinhaMaoDeObraDF(LinhaDF):

    def __init__(self, _dfr_insumo, composicao) -> None:
        super().__init__(_dfr_insumo, composicao)
        self.configurar_linha_subtotal_mao_de_obra()

    def configurar_linha_subtotal_mao_de_obra(self) -> None:
        self.linha['Descrição'] = 'Custo horário mão de obra'
        self.linha['Código'] = CODIGO_HORARIO
        self.linha['Grupo_x'] = MAO_DE_OBRA_CUSTO_HORARIO


class LinhaMaterialDF(LinhaDF):

    def __init__(self, _dfr_insumo, composicao) -> None:
        super().__init__(_dfr_insumo, composicao)
        self.configurar_linha_subtotal_material()

    def configurar_linha_subtotal_material(self) -> None:
        self.linha['Descrição'] = 'Custo unitário material'
        self.linha['Código'] = CODIGO_UNITARIO
        self.linha['Grupo_x'] = MATERIAL_CUSTO_UNITARIO


class LinhaCustoHorarioExecucaoDF(LinhaDF):

    def __init__(self, _dfr_insumo, composicao) -> None:
        super().__init__(_dfr_insumo, composicao)
        self.configurar_linha_custo_horario_execucao()

    def configurar_linha_custo_horario_execucao(self) -> None:
        self.linha['Descrição'] = 'Custo horário de execução'
        self.linha['Código'] = CODIGO_HORARIO_EXECUCAO
        self.linha['Grupo_x'] = EXECUCAO_HORARIO


class ComposicaoDF:
    """Classe que representa os data frames de cada composição do projeto que servirão para gerar um arquivo xlsx"""

    def __init__(self, composicao: ComposicaoDB, base: BaseDF) -> None:
        self.index_grupo = 'Grupo_x'
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
        self.dfr_insumo = self.dfr_insumo[ self.obter_lis_colunas() ]

        self.calcular_subtotal_simples()
        self.calcular_custo_horario_execucao()
        self.calcular_custo_unitario_execucao()

    def obter_dfr_dados_basicos_insumos( self ) -> pd.core.frame.DataFrame:
        return self.base.dfr_dados_in.query( "Código == '{}'".format( self.composicao.codigo ) )

    def obter_dfr_dados_basicos_composicao( self ) -> pd.core.frame.DataFrame:
        return self.base.dfr_dados_cp.query( "Composicao_principal == '{}'".format( self.composicao.codigo ) )

    def obter_dfr_apropriacoes_insumos( self ) -> pd.core.frame.DataFrame:
        return self.base.dfr_apropriacao_in.query( "Composicao_principal == '{}'".format( self.composicao.codigo ) )

    def obter_descricao_composicao( self ) -> str:
        auxiliar = self.obter_dfr_dados_basicos_insumos()
        return auxiliar['Descrição'].values[0]

    def obter_unidade_composicao( self ) -> str:
        auxiliar = self.obter_dfr_dados_basicos_insumos()
        return auxiliar['Unidade'].values[0]

    def obter_fic_composicao( self ) -> float:
        auxiliar = self.obter_dfr_dados_basicos_composicao()
        return auxiliar['FIC'].values[0]
    
    def obter_produtividade_composicao( self ) -> float:
        auxiliar = self.obter_dfr_dados_basicos_composicao()
        return auxiliar['Produtividade'].values[0]

    def associar_dfr_dados_basicos_apropriacoes_insumos( self ) -> pd.core.frame.DataFrame:
        return pd.merge( self.obter_dfr_apropriacoes_insumos(), self.base.dfr_dados_in, on='Código', how='left' )

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

    def inserir_col_dmt( self ) -> None:
        self.dfr_insumo['DMT'] = ''

    def obter_lis_colunas( self ) -> list:
        self.lista_colunas = ['Composicao_principal', self.index_grupo, 'Código', 'Descrição', 'Item transporte', 'DMT', 'Unidade', 'Quantidade', 'Utilização', self.obter_descricao_custo_produtivo(), self.obter_descricao_custo_improdutivo(),'Preço unitário', 'Custo total']
        return self.lista_colunas

    def associar_dfr_custos_apropriacoes_insumos( self ) -> pd.core.frame.DataFrame:
        return pd.merge( self.associar_dfr_dados_basicos_apropriacoes_insumos(), self.dfr_custo_in, on='Código', how='left')

    def calcular_sre_custo_equipamento( self ) -> pd.core.series.Series:
        quantidade = self.dfr_insumo['Quantidade']
        custo_produtivo = self.dfr_insumo[ self.obter_descricao_custo_produtivo() ]
        custo_improdutivo = self.dfr_insumo[ self.obter_descricao_custo_improdutivo() ]
        utilizacao = self.dfr_insumo['Utilização']
        return arred( quantidade * ( ( utilizacao * custo_produtivo ) + ( ( 1 - utilizacao ) * custo_improdutivo ) ) )

    def calcular_sre_custo_mao_de_obra( self ) -> pd.core.series.Series:
        quantidade = self.dfr_insumo['Quantidade']
        custo_produtivo = self.dfr_insumo[ self.obter_descricao_custo_produtivo() ]
        return arred( quantidade * custo_produtivo )

    def calcular_sre_custo_material( self ) -> pd.core.series.Series:
        quantidade = self.dfr_insumo['Quantidade']
        preco_unitario = self.dfr_insumo['Preço unitário']
        return arred( quantidade * preco_unitario )

    def obter_dfr_custo_equipamento( self ) -> pd.core.frame.DataFrame:
        self.dfr_insumo.loc[self.dfr_insumo[self.index_grupo] == EQUIPAMENTO, 'Custo total'] = self.calcular_sre_custo_equipamento()
        return self.dfr_insumo

    def obter_dfr_custo_mao_de_obra( self ) -> pd.core.frame.DataFrame:
        self.dfr_insumo.loc[self.dfr_insumo[self.index_grupo] == MAO_DE_OBRA, 'Custo total'] = self.calcular_sre_custo_mao_de_obra()
        return self.dfr_insumo

    def obter_dfr_custo_material( self ) -> pd.core.frame.DataFrame:
        self.dfr_insumo.loc[self.dfr_insumo[self.index_grupo] == MATERIAL, 'Custo total'] = self.calcular_sre_custo_material()
        return self.dfr_insumo

    def criar_linha_subtotal_equipamento(self, _dfr_insumo, composicao) -> LinhaEquipamentoDF:
        return LinhaEquipamentoDF(_dfr_insumo, composicao)

    def criar_linha_subtotal_mao_de_obra(self, _dfr_insumo, composicao) -> LinhaMaoDeObraDF:
        return LinhaMaoDeObraDF(_dfr_insumo, composicao)

    def criar_linha_subtotal_material(self, _dfr_insumo, composicao) -> LinhaMaterialDF:
        return LinhaMaterialDF(_dfr_insumo, composicao)

####################

    def criar_linha_subtotal_atividade_auxiliar(self, _dfr_insumo, composicao) -> pd.core.series.Series:
        linha_subtotal = _dfr_insumo[['Custo total']].sum()
        linha_subtotal['Composicao_principal'] = composicao
        linha_subtotal['Descrição'] = 'Custo unitário atividade auxiliar'
        linha_subtotal['Código'] = CODIGO_UNITARIO
        linha_subtotal[self.index_grupo] = ATIVIDADE_AUXILIAR_CUSTO_TOTAL
        return linha_subtotal

    def criar_linha_subtotal_tempo_fixo(self, _dfr_insumo, composicao) -> pd.core.series.Series:
        linha_subtotal = _dfr_insumo[['Custo total']].sum()
        linha_subtotal['Composicao_principal'] = composicao
        linha_subtotal['Descrição'] = 'Custo unitário tempo fixo'
        linha_subtotal['Código'] = CODIGO_UNITARIO
        linha_subtotal[self.index_grupo] = TEMPO_FIXO_CUSTO_TOTAL
        return linha_subtotal

    def criar_linha_subtotal_transporte(self, _dfr_insumo, composicao) -> pd.core.series.Series:
        linha_subtotal = _dfr_insumo[['Custo total']].sum()
        linha_subtotal['Composicao_principal'] = composicao
        linha_subtotal['Descrição'] = 'Custo unitário transporte'
        linha_subtotal['Código'] = CODIGO_UNITARIO
        linha_subtotal[self.index_grupo] = TRANSPORTE_CUSTO_TOTAL
        return linha_subtotal

    def criar_linha_custo_unitario_direto_total(self, _dfr_insumo, composicao) -> pd.core.series.Series:
        linha_custo_unitario_direto_total = _dfr_insumo[['Custo total']].sum()
        linha_custo_unitario_direto_total['Composicao_principal'] = composicao
        linha_custo_unitario_direto_total['Descrição'] = 'Custo unitário direto total'
        linha_custo_unitario_direto_total['Código'] = CODIGO_UNITARIO_DIRETO_TOTAL
        linha_custo_unitario_direto_total[self.index_grupo] = DIRETO_TOTAL_UNITARIO
        return linha_custo_unitario_direto_total

    def criar_linha_custo_horario_execucao(self, _dfr_insumo, composicao) -> pd.core.series.Series:
        linha_custo_horario_execucao = _dfr_insumo[['Custo total']].sum()
        linha_custo_horario_execucao['Composicao_principal'] = composicao
        linha_custo_horario_execucao['Descrição'] = 'Custo horário de execução'
        linha_custo_horario_execucao['Código'] = CODIGO_HORARIO_EXECUCAO
        linha_custo_horario_execucao[self.index_grupo] = EXECUCAO_HORARIO
        return linha_custo_horario_execucao

    def criar_linha_custo_unitario_execucao(self, _dfr_insumo, composicao) -> pd.core.series.Series:
        linha_custo_unitario_execucao = _dfr_insumo[['Custo total']].sum()
        linha_custo_unitario_execucao['Composicao_principal'] = composicao
        linha_custo_unitario_execucao['Descrição'] = 'Custo unitário de execução'
        linha_custo_unitario_execucao['Código'] = CODIGO_UNITARIO
        linha_custo_unitario_execucao[self.index_grupo] = EXECUCAO_UNITARIO
        return linha_custo_unitario_execucao

    def calcular_subtotal_simples( self ) -> None:
        for composicao, _dfr_insumo in self.dfr_insumo.groupby( ['Composicao_principal', self.index_grupo] ):
            grupo = composicao[1]
            composicao = composicao[0]
            if ( grupo == EQUIPAMENTO ):
                obj_linha = self.criar_linha_subtotal_equipamento( _dfr_insumo, composicao )
                self.composicao.custo_horario_equipamento = obj_linha.total
                self.composicao.calcular_custo_horario_execucao()
                self.composicao.calcular_custo_unitario_execucao()
                linha = obj_linha.linha
            elif ( grupo == MAO_DE_OBRA ):
                obj_linha = self.criar_linha_subtotal_mao_de_obra( _dfr_insumo, composicao )
                self.composicao.custo_horario_mao_de_obra = obj_linha.total
                self.composicao.calcular_custo_horario_execucao()
                self.composicao.calcular_custo_unitario_execucao()
                linha = obj_linha.linha
            elif ( grupo == MATERIAL ):
                obj_linha = self.criar_linha_subtotal_material( _dfr_insumo, composicao )
                self.composicao.custo_unitario_material = obj_linha.total
                linha = obj_linha.linha
            else:
                linha = None
            self.dfr_insumo = self.dfr_insumo.append( linha, ignore_index=True )

    def calcular_subtotal_composto( self ) -> None:
        for composicao, _dfr_insumo in self.dfr_insumo.groupby( ['Composicao_principal', self.index_grupo] ):
            grupo = composicao[1]
            composicao = composicao[0]
            if ( grupo == ATIVIDADE_AUXILIAR ):
                linha_subtotal = self.criar_linha_subtotal_atividade_auxiliar( _dfr_insumo, composicao )
                self.composicao.custo_total_atividade_auxiliar = linha_subtotal['Custo total']
            elif ( grupo == TEMPO_FIXO ):
                linha_subtotal = self.criar_linha_subtotal_tempo_fixo( _dfr_insumo, composicao )
                self.composicao.custo_total_tempo_fixo = linha_subtotal['Custo total']
            elif ( grupo == TRANSPORTE ):
                linha_subtotal = self.criar_linha_subtotal_transporte( _dfr_insumo, composicao )
                self.composicao.custo_total_transporte = linha_subtotal['Custo total']
            else:
                linha_subtotal = None
            self.dfr_insumo = self.dfr_insumo.append( linha_subtotal, ignore_index=True )

    def calcular_custo_atividade_auxiliar( self, dicionario: dict ) -> None:
        lista = self.obter_lis_atividade_auxiliar()
        for item in lista:
            grupo = item[0]
            item = item[1]
            self.dfr_insumo.loc[ self.dfr_insumo['Código'] == item,'Preço unitário'] = dicionario[ item ].custo_unitario_total 
            quantidade = self.dfr_insumo.loc[ self.dfr_insumo['Código'] == item, 'Quantidade']
            preco_unitario = self.dfr_insumo.loc[ self.dfr_insumo['Código'] == item, 'Preço unitário']
            if (grupo == TRANSPORTE): 
                distancia_transporte = self.dfr_insumo.loc[ self.dfr_insumo['Código'] == item, 'DMT'] = 0
                self.dfr_insumo.loc[ self.dfr_insumo['Código'] == item, 'Custo total'] = arred( distancia_transporte * quantidade * preco_unitario )
            else:
                self.dfr_insumo.loc[ self.dfr_insumo['Código'] == item, 'Custo total'] = arred( quantidade * preco_unitario )

    def calcular_custo_unitario_direto_total( self ) -> None:
        self.composicao.calcular_custo_unitario_execucao()
        for composicao, _dfr_insumo in self.dfr_insumo.groupby( ['Composicao_principal', 'Código'] ):
            codigo = composicao[1]
            composicao = composicao[0]
            if ( codigo == CODIGO_UNITARIO ):
                linha_custo_unitario_direto_total = self.criar_linha_custo_unitario_direto_total( _dfr_insumo, composicao )
                self.composicao.custo_unitario_total = linha_custo_unitario_direto_total['Custo total']
                self.dfr_insumo = self.dfr_insumo.append( linha_custo_unitario_direto_total, ignore_index=True )

    def calcular_custo_horario_execucao( self ) -> None:
        self.composicao.calcular_custo_unitario_execucao()
        for composicao, _dfr_insumo in self.dfr_insumo.groupby( ['Composicao_principal', 'Código'] ):
            codigo = composicao[1]
            composicao = composicao[0]
            if ( codigo == CODIGO_HORARIO ):
                linha_custo_horario_execucao = self.criar_linha_custo_horario_execucao( _dfr_insumo, composicao )
                linha_custo_horario_execucao['Custo total'] = self.composicao.custo_horario_execucao
                self.dfr_insumo = self.dfr_insumo.append( linha_custo_horario_execucao, ignore_index=True )

    def calcular_custo_unitario_execucao( self ) -> None:
        for composicao, _dfr_insumo in self.dfr_insumo.groupby( ['Composicao_principal', 'Código'] ):
            codigo = composicao[1]
            composicao = composicao[0]
            if ( codigo == CODIGO_HORARIO_EXECUCAO ):
                linha_custo_unitario_execucao = self.criar_linha_custo_unitario_execucao( _dfr_insumo, composicao )
                linha_custo_unitario_execucao['Custo total'] = self.composicao.custo_unitario_execucao
                self.dfr_insumo = self.dfr_insumo.append( linha_custo_unitario_execucao, ignore_index=True )

    def obter_operador_lis_insumo( self, insumo: int ) -> str:
        if insumo == ATIVIDADE_AUXILIAR:
            operador = '>='
        else:
            operador = '=='
        return operador

    def configurar_lis_insumo( self, consulta: pd.core.frame.DataFrame ) -> list:
        lista = list()
        if len( consulta[['Grupo', 'Código']].values ) != 0:
            for item in consulta[['Grupo', 'Código']].values:
                lista.append( item )
        return lista

    def obter_lis_insumo( self, insumo: int ) -> list:
        operador = self.obter_operador_lis_insumo(insumo)
        consulta = self.base.dfr_apropriacao_in.query( "Composicao_principal == '{}' & Grupo {} {}".format( self.composicao.codigo, operador, insumo ) )
        return self.configurar_lis_insumo( consulta )

    def obter_lis_atividade_auxiliar( self ) -> list:
        return self.obter_lis_insumo(ATIVIDADE_AUXILIAR)

    def obter_lis_equipamento( self ) -> list:
        return self.obter_lis_insumo(EQUIPAMENTO)

    def obter_lis_mao_de_obra( self ) -> list:
        return self.obter_lis_insumo(MAO_DE_OBRA)
    
    def obter_lis_material( self ) -> list:
        return self.obter_lis_insumo(MATERIAL)