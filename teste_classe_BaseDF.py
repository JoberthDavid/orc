import unittest
import numpy as np
import pandas as pd
from constantes import *
from classes import BaseDF, ComposicaoDB, ComposicaoDF, GeradorDF
from arquivos import arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in


codigo_composicao = str(308321)
instance_of_GeradorDF = GeradorDF( arq_db_cp )
instance_of_ComposicaoDB = ComposicaoDB( codigo_composicao )
instance_of_BaseDF = BaseDF( arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in )
instance_of_ComposicaoDF = ComposicaoDF( instance_of_ComposicaoDB, instance_of_BaseDF )
dados_cp = pd.read_csv( arq_db_cp, encoding=UTF)
lista_colunas_df_dados_cp = instance_of_GeradorDF.tratar_df( COLUNAS_DF_DADOS_BASICO_CP ).columns


class TestGeradorDF(unittest.TestCase):

    def test_create_GeradorDF(self):
        self.assertIsInstance( instance_of_GeradorDF, GeradorDF )


class TestBaseDF(unittest.TestCase):

    def test_create_BaseDF(self):
        self.assertIsInstance( instance_of_BaseDF, BaseDF )

    def test_carregar_df(self):
        self.assertIsInstance( instance_of_BaseDF.df_dados_cp, pd.core.frame.DataFrame )

    def test_tratar_df_dados_basicos_cp(self):
        self.assertEqual( len( instance_of_BaseDF.df_dados_cp.columns.values ), len( lista_colunas_df_dados_cp.values ) )


class TestComposicaoDB(unittest.TestCase):

    def test_create_ComposicaoDB(self):
        self.assertIsInstance( instance_of_ComposicaoDB, ComposicaoDB )       


class TestComposicaoDF(unittest.TestCase):

    def test_create_ComposicaoDF(self):
        self.assertIsInstance( instance_of_ComposicaoDF, ComposicaoDF )


if __name__ == '__main__':
    unittest.main()


