from formatacao_dados import Precisao


class NohArvoreComposicao:
 
    def __init__( self, codigo_principal, quantidade, lista_noh_arvore_composicao ) -> None:
        self.codigo_principal_noh_arvore_composicao = codigo_principal
        self.noh_filhos = list()
        self.lista_auxiliar = lista_noh_arvore_composicao
        self.quantidade = quantidade

    def inserir_noh_arvore_composicao( self, codigo_principal: str, atividade_auxiliar: str, utilizacao: float ) -> bool:
        obj_arred = Precisao()
        produto = obj_arred.utilizacao( self.quantidade * utilizacao )
        sinal = False
        if codigo_principal == self.codigo_principal_noh_arvore_composicao:
            self.noh_filhos.append( NohArvoreComposicao( atividade_auxiliar, produto, self.lista_auxiliar ) )
            sinal = True
        else:
            for noh_pai in self.noh_filhos:
                noh_pai.inserir_noh_arvore_composicao( codigo_principal, atividade_auxiliar, utilizacao )
            sinal = True
        return sinal

    def configurar_lista_noh_arvore_composicao_in_order( self ) -> list:
        _obj_pilha = Pilha()
        _obj_pilha.colocar_noh_na_pilha( self )
        while _obj_pilha.verificar_se_pilha_estah_vazia() != True:
            self = _obj_pilha.obter_primeiro_noh_da_pilha()
            self.lista_auxiliar.append( (self.codigo_principal_noh_arvore_composicao, self.quantidade) )
            _obj_pilha.retirar_noh_da_pilha()
            for noh_pai in self.noh_filhos[::-1]:
                _obj_pilha.colocar_noh_na_pilha( noh_pai )
        return self.lista_auxiliar

    def configurar_lista_noh_arvore_composicao_pos_order( self ) -> list:
        _obj_pilha = Pilha()
        _obj_pilha.colocar_noh_na_pilha( self )
        while _obj_pilha.verificar_se_pilha_estah_vazia() != True:
            self = _obj_pilha.obter_primeiro_noh_da_pilha()
            self.lista_auxiliar.append( (self.codigo_principal_noh_arvore_composicao, self.quantidade) )
            _obj_pilha.retirar_noh_da_pilha()
            for noh_pai in self.noh_filhos:
                _obj_pilha.colocar_noh_na_pilha( noh_pai )
        return self.lista_auxiliar


class NohPilha():

    def __init__( self, codigo_principal_noh_arvore_composicao: NohArvoreComposicao, proximo_noh_da_pilha=None ) -> None:
        self.codigo_principal_noh_arvore_composicao = codigo_principal_noh_arvore_composicao
        self.proximo_noh_da_pilha = proximo_noh_da_pilha


class Pilha():

    def __init__( self ):
        self.primeiro_noh_da_pilha = None
        self.ultimo_noh_da_pilha = None
        self.quantidade_noh_na_pilha = 0

    def colocar_noh_na_pilha( self, noh_arvore_composicao: NohArvoreComposicao ) -> int:
        if self.quantidade_noh_na_pilha == 0:
            self.ultimo_noh_da_pilha = NohPilha( noh_arvore_composicao )
            self.primeiro_noh_da_pilha = self.ultimo_noh_da_pilha
        else:
            self.primeiro_noh_da_pilha = NohPilha( noh_arvore_composicao, self.primeiro_noh_da_pilha )
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

    def obter_primeiro_noh_da_pilha( self ) -> NohArvoreComposicao:
        return self.primeiro_noh_da_pilha.codigo_principal_noh_arvore_composicao

    def verificar_se_pilha_estah_vazia( self ) -> bool:
        return self.quantidade_noh_na_pilha == 0


class NohFila():

    def __init__( self, codigo_principal_noh_arvore_composicao: NohArvoreComposicao, proximo_noh_da_fila=None ) -> None:
        self.codigo_principal_noh_arvore_composicao = codigo_principal_noh_arvore_composicao
        self.proximo_noh_da_fila = proximo_noh_da_fila


class Fila():

    def __init__( self ) -> None:
        self.primeiro_noh_da_fila = None
        self.ultimo_noh_da_fila = None
        self.quantidade_noh_na_fila = 0

    def colocar_noh_na_fila( self, noh_arvore_composicao: NohArvoreComposicao ) -> int:
        if self.quantidade_noh_na_fila == 0:
            self.ultimo_noh_da_fila = NohFila( noh_arvore_composicao )
            self.primeiro_noh_da_fila = self.ultimo_noh_da_fila
        else:
            self.ultimo_noh_da_fila.proximo_noh_da_fila = self.ultimo_noh_da_fila
            self.ultimo_noh_da_fila = NohFila( noh_arvore_composicao )
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

    def obter_primeiro_noh_da_fila( self ) -> NohArvoreComposicao:
        return self.primeiro_noh_da_fila.codigo_principal_noh_arvore_composicao

    def verificar_se_fila_estah_vazia( self ) -> bool:
        return self.quantidade_noh_na_fila == 0


class ArvoreComposicao:

    def __init__( self ) -> None:
        self.noh_raiz_arvore_composicao = None
        self.lista = list()

    def inserir_noh_arvore_composicao( self, codigo_principal: str, atividade_auxiliar: str, quantidade: float=1.0 ) -> bool:
        sinal = False
        if self.noh_raiz_arvore_composicao == None:
            self.noh_raiz_arvore_composicao = NohArvoreComposicao( codigo_principal, quantidade, self.lista )
            sinal = True
        else:
            utilizacao = quantidade
            self.noh_raiz_arvore_composicao.inserir_noh_arvore_composicao( codigo_principal, atividade_auxiliar, utilizacao )
            sinal = True
        return sinal

    def obter_lista_noh_arvore_in_order( self ) -> list:
        if self.noh_raiz_arvore_composicao != None:
            lista_noh = self.noh_raiz_arvore_composicao.configurar_lista_noh_arvore_composicao_in_order()
        else:
            lista_noh = list()
        return lista_noh

    def obter_lista_noh_arvore_pos_order( self ) -> list:
        if self.noh_raiz_arvore_composicao != None:
            lista_noh = self.noh_raiz_arvore_composicao.configurar_lista_noh_arvore_composicao_pos_order()
        else:
            lista_noh = list()
        return lista_noh