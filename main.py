# Para consultar sobre a biblioteca xlsxwriter https://xlsxwriter.readthedocs.io/index.html 
# Para consultar sobre a biblioteca Pandas https://www.dataquest.io/blog/excel-and-pandas/
# https://medium.com/analytics-vidhya/common-excel-formulas-in-python-c5a7ce0ae07a

from arquivos import (
                        arq_db_cp,
                        arq_db_in,
                        arq_apr_in,
                        arq_cto_in,
                        arq_db_al_an,
                        arq_db_al_st,
                        arq_apr_al,
                        arq_dmt,
                    )

from funcoes import escrever_arquivo_excel
from projeto import BaseDF, Servico, BonificacaoDespesasIndiretas, Projeto, GeradorDF

from formatacao_dados import Data, DadosProjeto


baseDF = BaseDF( arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in )

codigos_servicos_projeto = [ '9999200', '9999100', '9999400', '9999307', '9999393', '9999322', '9999341', '9999352', '9999356', '9999361', '9999362', '9999400', '7119700', '308321', '408031', '606841', '705371', '804215', '909621', '1108055', '2009619', '3009090', '4011287', '5213385', '6106188', '7119788']
quantidade_servicos_projeto = [ 24, 12, 1, 1000, 1000, 200, 100, 15, 20, 60, 70, 50, 1, 100.001, 200.002, 300.003, 400.004, 500.005, 600.006, 700.007, 800.008, 900.009, 1100.011, 1200.021, 1300.031, 6]
bdi_servicos_projeto = [ False, False, False, True, True, True, True, True, True, True, True, True, False, True, False, True, False, False, False, False, False, False, False, False, False, False]
transporte_servicos_projeto = [ True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

lista_servicos_projeto = list()

for i, codigo in enumerate(codigos_servicos_projeto):
    lista_servicos_projeto.append( Servico( codigo, quantidade_servicos_projeto[ i ], bdi_servicos_projeto[ i ], transporte_servicos_projeto[ i ] ) )

situacao = False #True #
bdi = BonificacaoDespesasIndiretas( 0.267, 0.150, situacao )
projeto = Projeto( lista_servicos_projeto, baseDF, bdi )

DADOS_PROJETO = DadosProjeto(
                    unidade_federacao='GO',
                    rodovia='BR-060',
                    trecho_inicial='Div (A)',
                    trecho_final='Div (B)',
                    subtrecho_inicial='Acreúna',
                    subtrecho_final='Rio Verde',
                    segmento_inicial=0.0,
                    segmento_final=300.0,
                    snv_inicial='060BGO001',
                    snv_final='060BGO002',
                    versao_snv='2020Ba',
                    data_base=Data(10,2020),
                    situacao_complementar=situacao,
                )


arquivo = '-'.join( ('ORCAMENTO', DADOS_PROJETO.unidade_federacao, DADOS_PROJETO.data_base.data_completa, DADOS_PROJETO.situacao_complementar, Data().data_completa ) )

escrever_arquivo_excel( arquivo, projeto, baseDF.max_apr(), DADOS_PROJETO )