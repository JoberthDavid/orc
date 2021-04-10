# Para consultar sobre a biblioteca xlsxwriter https://xlsxwriter.readthedocs.io/index.html 
# Para consultar sobre a biblioteca Pandas https://www.dataquest.io/blog/excel-and-pandas/
# https://medium.com/analytics-vidhya/common-excel-formulas-in-python-c5a7ce0ae07a

from arquivos import (
                        arq_db_cp,
                        arq_db_in,
                        arq_apr_in,
                        arq_cto_in
                    )

from funcoes import escrever_arquivo_excel
from projeto import BaseDF, Servico, BonificacaoDespesasIndiretas, Projeto

from formatacao_dados import Data

baseDF = BaseDF( arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in )

codigos_servicos_projeto = ['308321', '408031', '606841', '705371', '804215', '909621', '1108055', '2009619', '3009090', '4011287', '5213385', '6106188', '7119788']
quantidade_servicos_projeto = [1000.001, 2000.002, 3000.003, 4000.004, 5000.005, 6000.006, 7000.007, 8000.008, 9000.009, 11000.011, 12000.021, 13000.031, 14000.041]
bdi_servicos_projeto = [True, False, True, False, False, False, False, False, False, False, False, False, False]

servicos_projeto = list()

for i, codigo in enumerate(codigos_servicos_projeto):
    servicos_projeto.append( Servico( codigo, quantidade_servicos_projeto[ i ], bdi_servicos_projeto[ i ] ) )

onerado = True #False #
bdi = BonificacaoDespesasIndiretas(0.267, 0.150, onerado)
projeto = Projeto(servicos_projeto, baseDF, bdi)

COMPLEMENTO = 'ONERADO'
custo_produtivo = 'Custo produtivo onerado'
custo_improdutivo = 'Custo improdutivo onerado'

if not onerado:
    COMPLEMENTO = 'DESONERADO'
    custo_produtivo = 'Custo produtivo desonerado'
    custo_improdutivo = 'Custo improdutivo desonerado'

UF = 'GO'

DATA_BASE = '10-2020'

hoje = Data()
print( type(hoje.data) )
DATA_ELABORACAO = hoje.data_completa


arquivo = '-'.join( ('ORCAMENTO', UF, DATA_BASE, COMPLEMENTO, DATA_ELABORACAO) )


escrever_arquivo_excel( arquivo, COMPLEMENTO, projeto, baseDF.max_apr(), DATA_BASE )