# Para consultar sobre a biblioteca xlsxwriter https://xlsxwriter.readthedocs.io/index.html 
# Para consultar sobre a biblioteca Pandas https://www.dataquest.io/blog/excel-and-pandas/
# https://medium.com/analytics-vidhya/common-excel-formulas-in-python-c5a7ce0ae07a

from arquivos import *
from funcoes import *
from classes import ComposicaoDF, ComposicaoDB, BaseDF

baseDF = BaseDF( arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in )
maximo_linhas_na_composicao = baseDF.max_apr()

composicoes_projeto = ['308321', '408031', '606841', '705371', '804215', '909621', '1108055', '2009619', '3009090', '4011287', '5213385', '6106188', '7119788']
equipamento_projeto = []
mao_de_obra_projeto = []
material_projeto = []

onerado = True #False #

complemento = 'onerado'
custo_produtivo = 'Custo pro onerado'
custo_improdutivo = 'Custo imp onerado'

if not onerado:
    complemento = 'desonerado'
    custo_produtivo = 'Custo pro desonerado'
    custo_improdutivo = 'Custo imp desonerado'

arquivo = '_'.join( ('SICRO_TO_07_2019_composicoes_montadas', complemento) )

dicionario_db = dict()

dicionario_df = dict()

lista_aa = list()
lista_eq = list()
lista_mo = list()
lista_ma = list()

lista_auxiliar = list()

for codigo_cp in composicoes_projeto:

    db_composicao = ComposicaoDB( codigo_cp, onerado )

    df_composicao = ComposicaoDF( db_composicao, baseDF )

    dicionario_db[ db_composicao.codigo ] = db_composicao

    dicionario_df[ db_composicao.codigo ] = df_composicao

    lista_aa = df_composicao.obter_lis_atividade_auxiliar()

    lista_auxiliar.append(codigo_cp)

    if ( lista_aa != None):
        
        for item in lista_aa:
            item = item[1]
            if item not in composicoes_projeto:
                composicoes_projeto.append( item )
            lista_auxiliar.append( item )

    lista_eq = df_composicao.obter_lis_equipamento()

    if( lista_eq != None):
        for item in lista_eq:
            item = item[1]
            if item not in equipamento_projeto:
                equipamento_projeto.append( item )

    lista_mo = df_composicao.obter_lis_mao_de_obra()

    if( lista_mo != None):
        for item in lista_mo:
            item = item[1]
            if item not in mao_de_obra_projeto:
                mao_de_obra_projeto.append( item )

    lista_ma = df_composicao.obter_lis_material()

    if( lista_ma != None):
        for item in lista_ma:
            item = item[1]
            if item not in material_projeto:
                material_projeto.append( item )

lista_auxiliar_reversa = list()

while(len(lista_auxiliar) != 0 ):
    ultimo = lista_auxiliar[-1]
    if ultimo not in lista_auxiliar_reversa:
        lista_auxiliar_reversa.append( ultimo )
    lista_auxiliar.pop()

def tratar_codigo_composicao( codigo: str, menor_tamanho_codigo=6 ) -> str:
    if len( codigo ) == menor_tamanho_codigo : 
        codigo = "0{}".format( codigo )
    return codigo


for item in lista_auxiliar_reversa:
    comp = tratar_codigo_composicao(item)
    dicionario_df[ comp ].calcular_custo_atividade_auxiliar(dicionario_db)
    dicionario_df[ comp ].calcular_subtotal_composto()
    dicionario_df[ comp ].calcular_custo_unitario_direto_total()
    dicionario_df[ comp ].dfr_insumo.sort_values(by=dicionario_df[ comp ].index_grupo, inplace=True)
    dicionario_df[ comp ].dfr_insumo.reset_index(drop=True, inplace=True)


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


escrever_arquivo_excel( arquivo, complemento, dicionario_df, maximo_linhas_na_composicao, equipamento_projeto, mao_de_obra_projeto, material_projeto)
