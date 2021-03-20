import pandas as pd

from arquivos import (
                        arq_db_cp,
                        arq_db_in,
                        arq_apr_in,
                        arq_cto_in
                    )
from projeto import BaseDF

# criando objeto BaseDF
baseDF = BaseDF( arq_db_cp, arq_db_in, arq_apr_in, arq_cto_in )

# cria um arquivo Excel com várias planilhas
writer = pd.ExcelWriter( 'SICRO_TO_07_2019_analitico_composicoes_apropriacoes.xlsx', engine='xlsxwriter' )
baseDF.dfr_apropriacao_in.to_excel(writer, index=False, sheet_name='apropriacao_insumo')
baseDF.dfr_custo_in.to_excel(writer, index=False, sheet_name='custos_insumos')
baseDF.dfr_dados_cp.to_excel(writer, index=False, sheet_name='dados_basicos_composicoes')
baseDF.dfr_dados_in.to_excel(writer, index=False, sheet_name='dados_basicos_insumos')
writer.save()