from formatacao_dados import Precisao


class NohArvore:
 
    def __init__( self, codigo_principal, quantidade, lista_noh_arvore, insumo=None ) -> None:
        self.codigo_principal_noh_arvore = codigo_principal
        self.noh_filhos = list()
        self.lista_auxiliar = lista_noh_arvore
        self.quantidade = quantidade
        self.insumo = insumo

    def inserir_noh_arvore( self, codigo_principal: str, atividade_auxiliar: str, utilizacao: float ) -> bool:
        # obj_arred = Precisao()
        produto = utilizacao#obj_arred.utilizacao( self.quantidade * utilizacao )
        sinal = False
      
        if codigo_principal == self.codigo_principal_noh_arvore:
            self.noh_filhos.append( NohArvore( atividade_auxiliar, produto, self.lista_auxiliar ) )
            sinal = True
        else:
            for noh_pai in self.noh_filhos:
                noh_pai.inserir_noh_arvore( codigo_principal, atividade_auxiliar, utilizacao )
            sinal = True
        return sinal

    def inserir_transporte_noh_arvore( self, codigo_principal: str, atividade_auxiliar: str, insumo: str, utilizacao: float ) -> bool:
        obj_arred = Precisao()
        produto = obj_arred.utilizacao( self.quantidade * utilizacao )
        sinal = False
        self.insumo = insumo
        if codigo_principal == self.codigo_principal_noh_arvore:
            self.noh_filhos.append( NohArvore( atividade_auxiliar, produto, self.lista_auxiliar, self.insumo ) )
            sinal = True
        else:
            for noh_pai in self.noh_filhos:  
                noh_pai.inserir_transporte_noh_arvore( codigo_principal, atividade_auxiliar, self.insumo, utilizacao )
            sinal = True

        return sinal

    def configurar_lista_auxiliares_noh_arvore_in_order( self ) -> list:
        _obj_pilha = Pilha()
        _obj_pilha.colocar_noh_na_pilha( self )
        while _obj_pilha.verificar_se_pilha_estah_vazia() != True:
            self = _obj_pilha.obter_primeiro_noh_da_pilha()
            self.lista_auxiliar.append( (self.codigo_principal_noh_arvore, self.quantidade) )
            _obj_pilha.retirar_noh_da_pilha()
            for noh_pai in self.noh_filhos[::-1]:
                _obj_pilha.colocar_noh_na_pilha( noh_pai )
        return self.lista_auxiliar

    def configurar_lista_auxiliares_noh_arvore_pos_order( self ) -> list:
        _obj_pilha = Pilha()
        _obj_pilha.colocar_noh_na_pilha( self )
        while _obj_pilha.verificar_se_pilha_estah_vazia() != True:
            self = _obj_pilha.obter_primeiro_noh_da_pilha()
            self.lista_auxiliar.append( (self.codigo_principal_noh_arvore, self.quantidade) )
            _obj_pilha.retirar_noh_da_pilha()
            for noh_pai in self.noh_filhos:
                _obj_pilha.colocar_noh_na_pilha( noh_pai )
        return self.lista_auxiliar

    def configurar_lista_transporte_noh_arvore_in_order( self ) -> list:
        _obj_pilha = Pilha()
        _obj_pilha.colocar_noh_na_pilha( self )
        while _obj_pilha.verificar_se_pilha_estah_vazia() != True:
            self = _obj_pilha.obter_primeiro_noh_da_pilha()
            self.lista_auxiliar.append( (self.codigo_principal_noh_arvore, self.insumo, self.quantidade) )
            _obj_pilha.retirar_noh_da_pilha()
            for noh_pai in self.noh_filhos[::-1]:
                _obj_pilha.colocar_noh_na_pilha( noh_pai )
        return self.lista_auxiliar

    def configurar_lista_transporte_noh_arvore_pos_order( self ) -> list:
        _obj_pilha = Pilha()
        _obj_pilha.colocar_noh_na_pilha( self )
        while _obj_pilha.verificar_se_pilha_estah_vazia() != True:
            self = _obj_pilha.obter_primeiro_noh_da_pilha()
            self.lista_auxiliar.append( (self.codigo_principal_noh_arvore, self.insumo, self.quantidade) )
            _obj_pilha.retirar_noh_da_pilha()
            for noh_pai in self.noh_filhos:
                _obj_pilha.colocar_noh_na_pilha( noh_pai )
        return self.lista_auxiliar

class NohPilha():

    def __init__( self, codigo_principal_noh_arvore: NohArvore, proximo_noh_da_pilha=None ) -> None:
        self.codigo_principal_noh_arvore = codigo_principal_noh_arvore
        self.proximo_noh_da_pilha = proximo_noh_da_pilha


class Pilha():

    def __init__( self ):
        self.primeiro_noh_da_pilha = None
        self.ultimo_noh_da_pilha = None
        self.quantidade_noh_na_pilha = 0

    def colocar_noh_na_pilha( self, noh_arvore: NohArvore ) -> int:
        if self.quantidade_noh_na_pilha == 0:
            self.ultimo_noh_da_pilha = NohPilha( noh_arvore )
            self.primeiro_noh_da_pilha = self.ultimo_noh_da_pilha
        else:
            self.primeiro_noh_da_pilha = NohPilha( noh_arvore, self.primeiro_noh_da_pilha )
        self.quantidade_noh_na_pilha += 1
        return self.quantidade_noh_na_pilha

    def retirar_noh_da_pilha( self ) -> int:
        if self.quantidade_noh_na_pilha == 1:
            self.ultimo_noh_da_pilha = None
            self.primeiro_noh_da_fila = self.ultimo_noh_da_pilha
            self.quantidade_noh_na_pilha -= 1
        elif self.quantidade_noh_na_pilha > 1:
            self.primeiro_noh_da_pilha = self.primeiro_noh_da_pilha.proximo_noh_da_pilha
            self.quantidade_noh_na_pilha -= 1
        return self.quantidade_noh_na_pilha

    def obter_primeiro_noh_da_pilha( self ) -> NohArvore:
        return self.primeiro_noh_da_pilha.codigo_principal_noh_arvore

    def verificar_se_pilha_estah_vazia( self ) -> bool:
        return self.quantidade_noh_na_pilha == 0


class NohFila():

    def __init__( self, codigo_principal_noh_arvore: NohArvore, proximo_noh_da_fila=None ) -> None:
        self.codigo_principal_noh_arvore = codigo_principal_noh_arvore
        self.proximo_noh_da_fila = proximo_noh_da_fila


class Fila():

    def __init__( self ) -> None:
        self.primeiro_noh_da_fila = None
        self.ultimo_noh_da_fila = None
        self.quantidade_noh_na_fila = 0

    def colocar_noh_na_fila( self, noh_arvore: NohArvore ) -> int:
        if self.quantidade_noh_na_fila == 0:
            self.ultimo_noh_da_fila = NohFila( noh_arvore )
            self.primeiro_noh_da_fila = self.ultimo_noh_da_fila
        else:
            self.ultimo_noh_da_fila.proximo_noh_da_fila = self.ultimo_noh_da_fila
            self.ultimo_noh_da_fila = NohFila( noh_arvore )
        self.quantidade_noh_na_fila += 1
        return self.quantidade_noh_na_fila

    def retirar_noh_da_fila( self ) -> int:
        if self.quantidade_noh_na_fila == 1:
            self.ultimo_noh_da_fila = None
            self.primeiro_noh_da_fila = self.ultimo_noh_da_fila
            self.quantidade_noh_na_fila -= 1
        elif self.quantidade_noh_na_fila > 1:
            self.primeiro_noh_da_fila = self.primeiro_noh_da_fila.proximo_noh_da_fila
            self.quantidade_noh_na_fila -= 1
        return self.quantidade_noh_na_fila

    def obter_primeiro_noh_da_fila( self ) -> NohArvore:
        return self.primeiro_noh_da_fila.codigo_principal_noh_arvore

    def verificar_se_fila_estah_vazia( self ) -> bool:
        return self.quantidade_noh_na_fila == 0


class Arvore:

    def __init__( self, baseDF, obj_col_dfr, obj_grupo ) -> None:
        self.baseDF = baseDF
        self.obj_col_dfr = obj_col_dfr
        self.obj_grupo = obj_grupo
        self.noh_raiz_arvore_composicao = None
        self.lista = list()

    def obter_lista_auxiliares_servico( self, codigo ):
        consulta = self.baseDF.dfr_apropriacao_in.query( "{} == '{}' & Grupo == {}".format( self.obj_col_dfr.composicao_principal, codigo, self.obj_grupo.insumo_atividade_auxiliar ) )
        consulta = consulta[[self.obj_col_dfr.composicao_principal, self.obj_col_dfr.codigo, self.obj_col_dfr.quantidade]].values.tolist()
        return consulta

    def inserir_auxiliar_noh_arvore( self, codigo_principal: str, atividade_auxiliar: str, quantidade: float=1.0 ) -> bool:
        sinal = False
        codigo_principal = codigo_principal.zfill(7)
        atividade_auxiliar = atividade_auxiliar.zfill(7)
        if self.noh_raiz_arvore_composicao == None:
            self.noh_raiz_arvore_composicao = NohArvore( codigo_principal, quantidade, self.lista )

            for item in self.obter_lista_auxiliares_servico( codigo_principal ):
                self.inserir_auxiliar_noh_arvore( codigo_principal, item[1], item[2] )

            sinal = True
        else:
            obj_arred = Precisao()
            utilizacao = quantidade
            self.noh_raiz_arvore_composicao.inserir_noh_arvore( codigo_principal, atividade_auxiliar, utilizacao )

            for item in self.obter_lista_auxiliares_servico( atividade_auxiliar ):
                produto = obj_arred.utilizacao( utilizacao * item[2] )
                self.inserir_auxiliar_noh_arvore( atividade_auxiliar, item[1], produto )

            sinal = True

        return sinal

    def inserir_noh_arvore( self, codigo_principal: str, atividade_auxiliar: str, quantidade: float=1.0 ) -> bool:
        sinal = False
        if self.noh_raiz_arvore_composicao == None:
            self.noh_raiz_arvore_composicao = NohArvore( codigo_principal, quantidade, self.lista )
            sinal = True
        else:
            utilizacao = quantidade
            self.noh_raiz_arvore_composicao.inserir_noh_arvore( codigo_principal, atividade_auxiliar, utilizacao )
            sinal = True
        return sinal

    def inserir_transporte_noh_arvore( self, codigo_principal: str, atividade_auxiliar: str, insumo: str, quantidade: float ) -> bool:
        sinal = False
        if self.noh_raiz_arvore_composicao == None:
            self.noh_raiz_arvore_composicao = NohArvore( codigo_principal, quantidade, self.lista )
            sinal = True
        else:
            utilizacao = quantidade
            self.noh_raiz_arvore_composicao.inserir_transporte_noh_arvore( codigo_principal, atividade_auxiliar, insumo, utilizacao )
            sinal = True
        return sinal

    def obter_lista_auxiliares_noh_arvore_in_order( self ) -> list:
        if self.noh_raiz_arvore_composicao != None:
            lista_noh = self.noh_raiz_arvore_composicao.configurar_lista_auxiliares_noh_arvore_in_order()
        else:
            lista_noh = list()
        return lista_noh

    def obter_lista_auxiliares_noh_arvore_pos_order( self ) -> list:
        if self.noh_raiz_arvore_composicao != None:
            lista_noh = self.noh_raiz_arvore_composicao.configurar_lista_auxiliares_noh_arvore_pos_order()
        else:
            lista_noh = list()
        return lista_noh
    
    def obter_lista_transporte_noh_arvore_in_order( self ) -> list:
        if self.noh_raiz_arvore_composicao != None:
            lista_noh = self.noh_raiz_arvore_composicao.configurar_lista_transporte_noh_arvore_in_order()
        else:
            lista_noh = list()
        return lista_noh

    def obter_lista_transporte_noh_arvore_pos_order( self ) -> list:
        if self.noh_raiz_arvore_composicao != None:
            lista_noh = self.noh_raiz_arvore_composicao.configurar_lista_transporte_noh_arvore_pos_order()
        else:
            lista_noh = list()
        return lista_noh