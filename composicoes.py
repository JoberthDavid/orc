# Para consultar sobre a biblioteca xlsxwriter https://xlsxwriter.readthedocs.io/index.html 
# Para consultar sobre a biblioteca Pandas https://www.dataquest.io/blog/excel-and-pandas/
# https://medium.com/analytics-vidhya/common-excel-formulas-in-python-c5a7ce0ae07a

from arquivos import *
from funcoes import *
from classes import *


baseDF = BaseDF( arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in )
maximo_linhas_na_composicao = baseDF.max_apr()

composicoes_projeto = ['308321', '408031', '606841', '705371', '804215', '909621', '1108055', '2009619', '3009090', '4011287', '5213385', '6106188', '7119788']

####### escrita no xlsx
onerado = False
projeto = Projeto(composicoes_projeto, baseDF, onerado)
lista_composicoes = projeto.obter_dfr_projeto()

equipamento_projeto = projeto.equipamento_projeto
mao_de_obra_projeto = projeto.mao_de_obra_projeto
material_projeto = projeto.material_projeto

complemento = 'onerado'
custo_produtivo = 'Custo produtivo onerado'
custo_improdutivo = 'Custo improdutivo onerado'

if not onerado:
    complemento = 'desonerado'
    custo_produtivo = 'Custo produtivo desonerado'
    custo_improdutivo = 'Custo improdutivo desonerado'

arquivo = '_'.join( ('SICRO_TO_07_2019_composicoes_montadas', complemento) )

equipamento_projeto = pd.DataFrame({'Código': equipamento_projeto})
equipamento_projeto = pd.merge( equipamento_projeto, baseDF.dfr_dados_in, on='Código', how='left' )
equipamento_projeto = pd.merge( equipamento_projeto, baseDF.dfr_custo_in, on='Código', how='left' )
lista_colunas_eq = ['Grupo', 'Origem_x', 'Estado_x', 'Publicacao_x', 'Código', 'Descrição', 'Unidade', custo_produtivo, custo_improdutivo]
equipamento_projeto = equipamento_projeto[lista_colunas_eq]

mao_de_obra_projeto = pd.DataFrame({'Código': mao_de_obra_projeto})
mao_de_obra_projeto = pd.merge( mao_de_obra_projeto, baseDF.dfr_dados_in, on='Código', how='left' )
mao_de_obra_projeto = pd.merge( mao_de_obra_projeto, baseDF.dfr_custo_in, on='Código', how='left' )
lista_colunas_mo = ['Grupo', 'Origem_x', 'Estado_x', 'Publicacao_x', 'Código', 'Descrição', 'Unidade', custo_produtivo]
mao_de_obra_projeto = mao_de_obra_projeto[lista_colunas_mo]

material_projeto = pd.DataFrame({'Código': material_projeto})
material_projeto = pd.merge( material_projeto, baseDF.dfr_dados_in, on='Código', how='left' )
material_projeto = pd.merge( material_projeto, baseDF.dfr_custo_in, on='Código', how='left' )
lista_colunas_ma = ['Grupo', 'Origem_x', 'Estado_x', 'Publicacao_x', 'Código', 'Descrição', 'Unidade', 'Preço unitário']
material_projeto = material_projeto[lista_colunas_ma]



escrever_arquivo_excel( arquivo, complemento, lista_composicoes, maximo_linhas_na_composicao, equipamento_projeto, mao_de_obra_projeto, material_projeto)
