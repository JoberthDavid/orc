import unittest
import numpy as np
import pandas as pd
from constantes import *
from classes import *#BaseDF, ComposicaoDB, LinhaEquipamentoDF, LinhaEquipamentoDF, LinhaEquipamentoDF, ComposicaoDF, GeradorDF
from arquivos import arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in

codigo_composicao_1 = str(307731)
codigo_composicao_2 = str(4011287)

class TestGeradorDF(unittest.TestCase):

    def setUp(self):
        self.obj_GeradorDF = GeradorDF( arq_db_cp )

    def test_create_GeradorDF(self):
        self.assertIsInstance( self.obj_GeradorDF, GeradorDF )


class TestBaseDF(unittest.TestCase):

    def setUp(self):
        self.obj_BaseDF = BaseDF( arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in )

    def test_instance_of_BaseDF(self):
        self.assertIsInstance( self.obj_BaseDF, BaseDF )

    def test_instance_of_carregar_df(self):
        self.assertIsInstance( self.obj_BaseDF.dfr_dados_cp, pd.core.frame.DataFrame )

    def test_result_of_tratar_dfr_dados_basicos_cp(self):
        obj_GeradorDF = GeradorDF( arq_db_cp )
        lista_colunas_dfr_dados_cp = obj_GeradorDF.tratar_dfr( COLUNAS_DFR_DADOS_BASICO_CP ).columns
        self.assertEqual( len( self.obj_BaseDF.dfr_dados_cp.columns.values ), len( lista_colunas_dfr_dados_cp.values ) )


class TestComposicaoDB(unittest.TestCase):

    def setUp(self):
        self.obj_ComposicaoDB = ComposicaoDB( codigo_composicao_1 )
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

    def test_instance_of_ComposicaoDB(self):
        self.assertIsInstance( self.obj_ComposicaoDB, ComposicaoDB )
    
    def test_instance_of_tratar_codigo_composicao( self ):
        self.assertEqual( self.obj_ComposicaoDB.codigo, self.obj_ComposicaoDB.tratar_codigo_composicao(codigo_composicao_1) )
        self.assertNotEqual( self.obj_ComposicaoDB.codigo, codigo_composicao_1 )
        self.assertIsInstance( self.obj_ComposicaoDB.codigo, str )

    def test_result_of_calcular_custo_horario_execucao(self):
        resultado = round( self.obj_ComposicaoDB.custo_horario_equipamento + self.obj_ComposicaoDB.custo_horario_mao_de_obra, PRECISAO_CUSTO )
        esperado = self.obj_ComposicaoDB.calcular_custo_horario_execucao()
        self.assertEqual( resultado, esperado )
        self.assertIsInstance( resultado, float )

    def test_result_of_calcular_custo_unitario_execucao(self):
        resultado = round( self.obj_ComposicaoDB.custo_horario_execucao / self.obj_ComposicaoDB.produtividade, PRECISAO_CUSTO )
        esperado = self.obj_ComposicaoDB.calcular_custo_unitario_execucao()
        self.assertEqual( resultado, esperado )
        self.assertIsInstance( resultado, float )

    def test_result_of_calcular_custo_unitario_total(self):
        custo_insumos = self.obj_ComposicaoDB.custo_unitario_execucao + self.obj_ComposicaoDB.custo_unitario_material
        custo_servicos = self.obj_ComposicaoDB.custo_total_atividade_auxiliar + self.obj_ComposicaoDB.custo_total_tempo_fixo + self.obj_ComposicaoDB.custo_total_transporte
        resultado = round( custo_insumos + custo_servicos, PRECISAO_CUSTO )
        esperado = self.obj_ComposicaoDB.calcular_custo_unitario_total()
        self.assertEqual( resultado, esperado )
        self.assertIsInstance( resultado, float )

    def test_result_of_calcular_preco_unitario_total(self):
        resultado = round( self.obj_ComposicaoDB.custo_bdi + self.obj_ComposicaoDB.custo_unitario_total, PRECISAO_CUSTO )
        esperado = self.obj_ComposicaoDB.calcular_preco_unitario_total()
        self.assertEqual( resultado, esperado )
        self.assertIsInstance( resultado, float )


class TestComposicaoDF(unittest.TestCase):

    def setUp( self ):
        obj_ComposicaoDB = ComposicaoDB( codigo_composicao_2 )
        obj_BaseDF = BaseDF( arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in )
        self.obj_ComposicaoDF = ComposicaoDF( obj_ComposicaoDB, obj_BaseDF )

    def test_instance_of_ComposicaoDF(self):
        self.assertIsInstance( self.obj_ComposicaoDF, ComposicaoDF )

    def test_result_and_instance_of_obter_dfr_dados_basicos_insumos( self ):
        resultado = self.obj_ComposicaoDF.obter_dfr_dados_basicos_insumos()
        esperado = self.obj_ComposicaoDF.base.dfr_dados_in.query( "Código == '{}'".format( self.obj_ComposicaoDF.composicao.codigo ) )
        pd._testing.assert_frame_equal( resultado, esperado )
        self.assertIsInstance( resultado, pd.core.frame.DataFrame )

    def test_result_and_instance_of_obter_dfr_dados_basicos_composicao( self ):
        resultado = self.obj_ComposicaoDF.obter_dfr_dados_basicos_composicao()
        esperado = self.obj_ComposicaoDF.base.dfr_dados_cp.query( "Composicao_principal == '{}'".format( self.obj_ComposicaoDF.composicao.codigo ) )
        pd._testing.assert_frame_equal( resultado, esperado )
        self.assertIsInstance( resultado, pd.core.frame.DataFrame )

    def test_result_and_instance_of_obter_dfr_apropriacoes_insumos( self ):
        resultado = self.obj_ComposicaoDF.obter_dfr_apropriacoes_insumos()
        esperado = self.obj_ComposicaoDF.base.dfr_apropriacao_in.query( "Composicao_principal == '{}'".format( self.obj_ComposicaoDF.composicao.codigo ) )
        pd._testing.assert_frame_equal( resultado, esperado )
        self.assertIsInstance( resultado, pd.core.frame.DataFrame )

    def test_result_and_instance_of_obter_descricao_composicao( self ):
        resultado = self.obj_ComposicaoDF.obter_descricao_composicao()
        esperado = self.obj_ComposicaoDF.composicao.descricao
        self.assertEqual( resultado, esperado )
        self.assertIsInstance( resultado, str )

    def test_result_and_instance_of_obter_unidade_composicao( self ):
        resultado = self.obj_ComposicaoDF.obter_unidade_composicao()
        esperado = self.obj_ComposicaoDF.composicao.unidade
        self.assertEqual( resultado, esperado )
        self.assertIsInstance( resultado, str )

    def test_result_and_instance_of_obter_fic_composicao( self ):
        resultado = self.obj_ComposicaoDF.obter_fic_composicao()
        esperado = self.obj_ComposicaoDF.composicao.fic
        self.assertEqual( resultado, esperado )
        self.assertIsInstance( resultado, float )
    
    def test_result_and_instance_of_obter_produtividade_composicao( self ):
        resultado = self.obj_ComposicaoDF.obter_produtividade_composicao()
        esperado = self.obj_ComposicaoDF.composicao.produtividade
        self.assertEqual( resultado, esperado )
        self.assertIsInstance( resultado, float )

    def test_instance_of_obter_dados_basicos_apropriacoes_insumos( self ):
        resultado = self.obj_ComposicaoDF.associar_dfr_dados_basicos_apropriacoes_insumos()
        self.assertIsInstance( resultado, pd.core.frame.DataFrame )

    def test_result_and_instance_of_obter_desoneracao_mao_de_obra( self ):
        resultado = self.obj_ComposicaoDF.obter_desoneracao_mao_de_obra()
        self.assertEqual( resultado, 'onerado')
        self.assertIsInstance( resultado, str )
    
    def test_instance_of_obter_desoneracao_mao_de_obra( self ):
        resultado = self.obj_ComposicaoDF.obter_desoneracao_mao_de_obra()
        self.assertIsInstance( resultado, str )
    
    def test_result_and_instance_of_obter_descricao_custo_produtivo( self ):
        resultado = 'Custo pro {}'.format( self.obj_ComposicaoDF.obter_desoneracao_mao_de_obra() )
        esperado = self.obj_ComposicaoDF.obter_descricao_custo_produtivo()
        self.assertEqual( resultado, esperado )
        self.assertIsInstance( resultado, str )

    def test_result_of_obter_descricao_custo_improdutivo( self ):
        resultado = 'Custo imp {}'.format( self.obj_ComposicaoDF.obter_desoneracao_mao_de_obra() )
        esperado = self.obj_ComposicaoDF.obter_descricao_custo_improdutivo()
        self.assertEqual( resultado, esperado )
    
    def test_result_of_inserir_cl_dmt( self ):
        self.obj_ComposicaoDF.inserir_col_dmt()
        resultado = self.obj_ComposicaoDF.dfr_insumo['DMT'].to_list()
        esperado = ['','','','','','','','','','','','','','','','','','','','','','']
        self.assertListEqual( resultado, esperado )

    def test_result_of_obter_lis_colunas( self ):
        resultado = self.obj_ComposicaoDF.obter_lis_colunas()
        esperado = ['Composicao_principal', self.obj_ComposicaoDF.index_grupo, 'Código', 'Descrição', 'Item transporte', 'DMT', 'Unidade', 'Quantidade', 'Utilização', self.obj_ComposicaoDF.obter_descricao_custo_produtivo(), self.obj_ComposicaoDF.obter_descricao_custo_improdutivo(),'Preço unitário', 'Custo total']
        self.assertListEqual( resultado, esperado )

    def test_result_of_associar_dfr_custos_apropriacoes_insumos( self ):
        resultado = self.obj_ComposicaoDF.associar_dfr_custos_apropriacoes_insumos()
        esperado = pd.merge( self.obj_ComposicaoDF.associar_dfr_dados_basicos_apropriacoes_insumos(), self.obj_ComposicaoDF.dfr_custo_in, on='Código', how='left' )
        pd._testing.assert_frame_equal( resultado, esperado )
    
    def test_result_of_calcular_sre_custo_equipamento( self ):
        resultado = 0
        for composicao, _dfr_insumo in self.obj_ComposicaoDF.dfr_insumo.groupby( ['Composicao_principal', self.obj_ComposicaoDF.index_grupo] ):
            if composicao[1] == EQUIPAMENTO:
              resultado = _dfr_insumo['Custo total'].sum()
        esperado = self.obj_ComposicaoDF.composicao.custo_horario_equipamento
        self.assertEqual( resultado, esperado )

    def test_result_of_calcular_sre_custo_mao_de_obra( self ):
        resultado = 0
        for composicao, _dfr_insumo in self.obj_ComposicaoDF.dfr_insumo.groupby( ['Composicao_principal', self.obj_ComposicaoDF.index_grupo] ):
            if composicao[1] == MAO_DE_OBRA:
              resultado = _dfr_insumo['Custo total'].sum()
        esperado = self.obj_ComposicaoDF.composicao.custo_horario_mao_de_obra
        self.assertEqual( resultado, esperado )
        
    def test_result_of_calcular_sre_custo_material( self ):
        resultado = 0
        for composicao, _dfr_insumo in self.obj_ComposicaoDF.dfr_insumo.groupby( ['Composicao_principal', self.obj_ComposicaoDF.index_grupo] ):
            if composicao[1] == MATERIAL:
              resultado = _dfr_insumo['Custo total'].sum()
        esperado = self.obj_ComposicaoDF.composicao.custo_unitario_material
        self.assertEqual( resultado, esperado )

    def test_result_of_obter_dfr_custo_equipamento(self):
        resultado = self.obj_ComposicaoDF.dfr_insumo.query( '{} == {}'.format(self.obj_ComposicaoDF.index_grupo, EQUIPAMENTO ) )
        esperado = [161.4524, 2.0687, 166.7428, 127.8386, 121.9713, 75.2449]
        self.assertListEqual( resultado['Custo total'].to_list(), esperado )
    
    def test_result_of_obter_dfr_custo_mao_de_obra(self):
        resultado = self.obj_ComposicaoDF.dfr_insumo.query( '{} == {}'.format(self.obj_ComposicaoDF.index_grupo, MAO_DE_OBRA ) )
        esperado = [90.6054]
        self.assertListEqual( resultado['Custo total'].to_list(), esperado )

    def test_result_of_obter_dfr_custo_material(self):
        resultado = self.obj_ComposicaoDF.dfr_insumo.query( '{} == {}'.format(self.obj_ComposicaoDF.index_grupo, MATERIAL ) )
        esperado = [39.2218]
        self.assertListEqual( resultado['Custo total'].to_list(), esperado )

    def test_instance_of_criar_linha_subtotal_equipamento(self):
        _dfr_insumo = self.obj_ComposicaoDF.dfr_insumo.query( '{} == {}'.format(self.obj_ComposicaoDF.index_grupo, EQUIPAMENTO ) )
        resultado = self.obj_ComposicaoDF.criar_linha_subtotal_equipamento( _dfr_insumo, codigo_composicao_2 )
        self.assertIsInstance( resultado, LinhaEquipamentoDF)

    def test_instance_of_criar_linha_subtotal_mao_de_obra(self):
        _dfr_insumo = self.obj_ComposicaoDF.dfr_insumo.query( '{} == {}'.format(self.obj_ComposicaoDF.index_grupo, MAO_DE_OBRA ) )
        resultado = self.obj_ComposicaoDF.criar_linha_subtotal_mao_de_obra( _dfr_insumo, codigo_composicao_2 )
        self.assertIsInstance( resultado, LinhaMaoDeObraDF)

    def test_instance_of_criar_linha_subtotal_material(self):
        _dfr_insumo = self.obj_ComposicaoDF.dfr_insumo.query( '{} == {}'.format(self.obj_ComposicaoDF.index_grupo, MATERIAL ) )
        resultado = self.obj_ComposicaoDF.criar_linha_subtotal_material( _dfr_insumo, codigo_composicao_2 )
        self.assertIsInstance( resultado, LinhaMaterialDF)

if __name__ == '__main__':
    unittest.main()


