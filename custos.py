from funcoes import *

#################### Preços de equipamentos

# arquivo_custos_equipamentos = 'TXT//SICRO_TO_07_2019_sintetico_equipamento_custo_unitario.txt'

# df_preco_eq = carregar_data_frame(arquivo_custos_equipamentos)
# lista_colunas_preco_eq = ['Equipamento','Custo_improdutivo','Custo_produtivo','NONE']

# eq = tratar_dados(df_preco_eq, lista_colunas_preco_eq)

#################### Preços de mão-de-obra

# arquivo_preco_mao_de_obra = 'TXT//SICRO_TO_07_2019_sintetico_mao_de_obra_custo_unitario.txt'

# df_preco_mo = carregar_data_frame(arquivo_preco_mao_de_obra)
# lista_colunas_preco_mo = ['Mao_de_obra','Custo_unitario','NONE']

# mo = tratar_dados(df_preco_mo, lista_colunas_preco_mo)

#################### Preços de material

# arquivo_preco_material = 'TXT//SICRO_TO_07_2019_sintetico_material_custo_unitario.txt'

# df_preco_ma = carregar_data_frame(arquivo_preco_material)
# lista_colunas_preco_ma = ['Material','Custo_unitario','NONE']

# ma = tratar_dados(df_preco_ma, lista_colunas_preco_ma)


#################### Preços de insumos

arquivo_custos_insumos = 'TXT//SICRO_TO_07_2019_insumos_custos_unitarios.txt'

df_preco_ins = carregar_data_frame(arquivo_custos_insumos)
lista_colunas_preco_ins = ['Insumo','Custo_pro_one','Custo_imp_one','Custo_pro_des','Custo_imp_des','Custo','NONE']

ins = tratar_dados(df_preco_ins, lista_colunas_preco_ins)

# cria um arquivo com várias planilhas
writer = pd.ExcelWriter('SICRO_TO_07_2019_insumos_custos_unitarios.xlsx', engine='xlsxwriter')
ins.to_excel(writer, index=False, sheet_name='custos_insumos')
# eq.to_excel(writer, index=False, sheet_name='PU_Equipamento')
# mo.to_excel(writer, index=False, sheet_name='PU_Mao_de_obra')
# ma.to_excel(writer, index=False, sheet_name='PU_Material')
writer.save()
