import unittest
import numpy as np
import pandas as pd
from constantes import *
from classes import BaseDF, ComposicaoDB, ComposicaoDF, GeradorDF
from arquivos import arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in


codigo_composicao = str(4011287)

class TestGeradorDF(unittest.TestCase):

    def setUp(self):
        self.obj_GeradorDF = GeradorDF( arq_db_cp )

    def test_create_GeradorDF(self):
        self.assertIsInstance( self.obj_GeradorDF, GeradorDF )


class TestBaseDF(unittest.TestCase):

    def setUp(self):
        self.obj_BaseDF = BaseDF( arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in )

    def test_instancia_de_BaseDF(self):
        self.assertIsInstance( self.obj_BaseDF, BaseDF )

    def test_instancia_de_carregar_df(self):
        self.assertIsInstance( self.obj_BaseDF.df_dados_cp, pd.core.frame.DataFrame )

    def test_resultado_de_tratar_df_dados_basicos_cp(self):
        obj_GeradorDF = GeradorDF( arq_db_cp )
        lista_colunas_df_dados_cp = obj_GeradorDF.tratar_df( COLUNAS_DF_DADOS_BASICO_CP ).columns
        self.assertEqual( len( self.obj_BaseDF.df_dados_cp.columns.values ), len( lista_colunas_df_dados_cp.values ) )


class TestComposicaoDB(unittest.TestCase):

    def setUp(self):
        self.obj_ComposicaoDB = ComposicaoDB( codigo_composicao )
        self.obj_ComposicaoDB.descricao = 'Base de solo melhorado com 4% de cimento e mistura na pista com material de jazida'
        self.obj_ComposicaoDB.unidade = 'm³'
        self.obj_ComposicaoDB.fic = 0.03149
        self.obj_ComposicaoDB.produtividade  = 146.23000
        self.obj_ComposicaoDB.custo_horario_equipamento = 655.3187
        self.obj_ComposicaoDB.custo_horario_mao_de_obra = 90.6054
        self.obj_ComposicaoDB.custo_horario_execucao = 745.9241
        self.obj_ComposicaoDB.custo_unitario_execucao = 5.1010
        self.obj_ComposicaoDB.custo_fic = 0.1606
        self.obj_ComposicaoDB.custo_fit = 0.0000
        self.obj_ComposicaoDB.custo_unitario_material = 39.2218
        self.obj_ComposicaoDB.custo_total_insumos = 44.4834
        self.obj_ComposicaoDB.custo_total_atividade_auxiliar = 1.0457
        self.obj_ComposicaoDB.custo_total_tempo_fixo = 3.7588
        self.obj_ComposicaoDB.custo_total_transporte = 0.0000
        self.obj_ComposicaoDB.custo_unitario_total = 49.29
        self.obj_ComposicaoDB.custo_bdi = 0.0000
        self.obj_ComposicaoDB.preco_unitario_total = 49.29

    def test_instancia_de_ComposicaoDB(self):
        self.assertIsInstance( self.obj_ComposicaoDB, ComposicaoDB )
    
    def test_resultado_de_calcular_custo_horario_execucao(self):
        resultado = round( self.obj_ComposicaoDB.custo_horario_equipamento + self.obj_ComposicaoDB.custo_horario_mao_de_obra, PRECISAO_CUSTO )
        esperado = self.obj_ComposicaoDB.calcular_custo_horario_execucao()
        self.assertEqual( resultado, esperado )

    def test_resultado_de_calcular_custo_unitario_execucao(self):
        resultado = round( self.obj_ComposicaoDB.custo_horario_execucao / self.obj_ComposicaoDB.produtividade, PRECISAO_CUSTO )
        esperado = self.obj_ComposicaoDB.calcular_custo_unitario_execucao()
        self.assertEqual( resultado, esperado )

    def test_resultado_de_calcular_custo_unitario_total(self):
        custo_insumos = self.obj_ComposicaoDB.custo_unitario_execucao + self.obj_ComposicaoDB.custo_unitario_material
        custo_servicos = self.obj_ComposicaoDB.custo_total_atividade_auxiliar + self.obj_ComposicaoDB.custo_total_tempo_fixo + self.obj_ComposicaoDB.custo_total_transporte
        resultado = round( custo_insumos + custo_servicos, PRECISAO_CUSTO )
        esperado = self.obj_ComposicaoDB.calcular_custo_unitario_total()
        self.assertEqual( resultado, esperado )

    def test_resultado_de_calcular_preco_unitario_total(self):
        resultado = round( self.obj_ComposicaoDB.custo_bdi + self.obj_ComposicaoDB.custo_unitario_total, PRECISAO_CUSTO )
        esperado = self.obj_ComposicaoDB.calcular_preco_unitario_total()
        self.assertEqual( resultado, esperado )


class TestComposicaoDF(unittest.TestCase):

    def setUp(self):
        obj_ComposicaoDB = ComposicaoDB( codigo_composicao )
        obj_BaseDF = BaseDF( arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in )
        self.obj_ComposicaoDF = ComposicaoDF( obj_ComposicaoDB, obj_BaseDF )

    def test_instancia_de_ComposicaoDF(self):
        self.assertIsInstance( self.obj_ComposicaoDF, ComposicaoDF )

    def test_resultado_de_retornar_argumento_query_apropriacao( self ):
        resultado = "Composicao_principal == '{}'".format( self.obj_ComposicaoDF.composicao.codigo )
        self.assertEqual( resultado, self.obj_ComposicaoDF.retornar_argumento_query_apropriacao() )

    def test_instancia_de_carregar_dados_basicos_insumos( self ):
        self.assertIsInstance( self.obj_ComposicaoDF.carregar_dados_basicos_insumos(), pd.core.frame.DataFrame )

    def test_resultado_de_retornar_desoneracao_mao_de_obra( self ):
        self.assertEqual( self.obj_ComposicaoDF.retornar_desoneracao_mao_de_obra(), 'onerado')
    
    def test_instancia_de_retornar_desoneracao_mao_de_obra( self ):
        self.assertIsInstance( self.obj_ComposicaoDF.retornar_desoneracao_mao_de_obra(), str )
    
    def test_resultado_de_retornar_custo_produtivo( self ):
        resultado = 'Custo pro {}'.format( self.obj_ComposicaoDF.retornar_desoneracao_mao_de_obra() )
        esperado = self.obj_ComposicaoDF.retornar_custo_produtivo()
        self.assertEqual( resultado, esperado )

    def test_resultado_de_retornar_custo_improdutivo( self ):
        resultado = 'Custo imp {}'.format( self.obj_ComposicaoDF.retornar_desoneracao_mao_de_obra() )
        esperado = self.obj_ComposicaoDF.retornar_custo_improdutivo()
        self.assertEqual( resultado, esperado )
    
    def test_resultado_de_retornar_lista_colunas( self ):
        resultado = self.obj_ComposicaoDF.retornar_lista_colunas()
        esperado = ['Composicao_principal', self.obj_ComposicaoDF.index_grupo, 'Código', 'Descrição', 'Item transporte', 'DMT', 'Unidade', 'Quantidade', 'Utilização', self.obj_ComposicaoDF.retornar_custo_produtivo(), self.obj_ComposicaoDF.retornar_custo_improdutivo(),'Preço unitário', 'Custo total']
        self.assertListEqual( resultado, esperado )



if __name__ == '__main__':
    unittest.main()


