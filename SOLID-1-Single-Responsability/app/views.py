from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse

from .repositories import CategoriaRepository, ProdutoRepository


# formulario utilizado para edicao de registros de categorias
class CategoriaForm(forms.Form):
    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    descricao = forms.CharField(label='Descrição', max_length=30, required=True)

def _get_categoria_repo():
    return CategoriaRepository()


def listar_categorias(request):
    registros = _get_categoria_repo().listar()
    return render(request, 'categorias_listar.html', context={'registros': registros})


def incluir_categoria(request):
    return render(
        request,
        'categorias_editar.html',
        context={'acao': 'Inclusão', 'form': CategoriaForm()},
    )


def salvar_categoria(request):
    form_data = request.POST
    acao_form = form_data['acao']
    repo = _get_categoria_repo()

    if acao_form == 'Inclusão':
        repo.inserir(form_data['descricao'])
    elif acao_form == 'Exclusão':
        repo.excluir(form_data['id'])
    else:
        repo.atualizar(form_data['id'], form_data['descricao'])

    # Sempre retornar um HttpResponseRedirect após processar dados "POST".
    return HttpResponseRedirect(reverse('categorias'))


def editar_ou_excluir_categoria(request, categoria_id, acao):
    registro = _get_categoria_repo().obter_por_id(categoria_id)
    registro_dict = {'id': registro[0], 'descricao': registro[1]}
    acao = 'Alteração' if acao == 'alterar' else 'Exclusão'

    return render(
        request,
        'categorias_editar.html',
        context={'acao': acao, 'form': CategoriaForm(initial=registro_dict)},
    )


# Metodo responsavel por listar, incluir, alterar e excluir as Categorias.
def categorias(request, acao=None, id=None):
    '''
    Metodo responsavel por receber todas as rotas URL do cadastro de Categorias.

    De acordo com a "acao" e o "id" informados, esse metodo ira:
      - 'categorias/': Exibir a pagina de listagem
      - 'categorias/incluir/': Exibir a pagina de inclusao
      - 'categorias/alterar/<:id>/': Exibir a pagina de alteracao
      - 'categorias/excluir/<:id>/': Exibir a pagina de exclusao
      - 'categorias/salvar/': insere, altera ou exclui um registro
    '''
    try:
        if acao is None:
            return listar_categorias(request)
        if acao == 'salvar':
            return salvar_categoria(request)
        if acao == 'incluir':
            return incluir_categoria(request)
        if acao in ['alterar', 'excluir']:
            return editar_ou_excluir_categoria(request, id, acao)
        raise Exception('Ação inválida')
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})




# formulario utilizado para edicao de registros de produtos
class ProdutoForm(forms.Form):
    id = forms.IntegerField(label='ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
    descricao = forms.CharField(label='Descrição', max_length=30, required=True)
    preco_unitario = forms.DecimalField(label='Preço Unitário', max_digits=10, decimal_places=2, required=True)
    quantidade_estoque = forms.IntegerField(label='Qtd. Estoque', required=True)
    categoria_id = forms.ChoiceField(label='Categoria', required=True)

    # construtor do Formulario
    def __init__(self, *args, categoria_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria_id'].choices = categoria_choices or []


def _get_produto_repo():
    return ProdutoRepository()


def _categoria_choices():
    return _get_produto_repo().listar_categorias()


def _build_produto_form(initial=None):
    return ProdutoForm(initial=initial, categoria_choices=_categoria_choices())


def listar_produtos(request):
    registros = _get_produto_repo().listar_com_categoria()
    return render(request, 'produtos_listar.html', context={'registros': registros})


def incluir_produto(request):
    return render(
        request,
        'produtos_editar.html',
        context={'acao': 'Inclusão', 'form': _build_produto_form()},
    )


def salvar_produto(request):
    form_data = request.POST
    acao_form = form_data['acao']
    repo = _get_produto_repo()

    if acao_form == 'Inclusão':
        repo.inserir(
            form_data['descricao'],
            form_data['preco_unitario'],
            form_data['quantidade_estoque'],
            form_data['categoria_id'],
        )
    elif acao_form == 'Exclusão':
        repo.excluir(form_data['id'])
    else:
        repo.atualizar(
            form_data['id'],
            form_data['descricao'],
            form_data['preco_unitario'],
            form_data['quantidade_estoque'],
            form_data['categoria_id'],
        )

    # Sempre retornar um HttpResponseRedirect após processar dados "POST".
    return HttpResponseRedirect(reverse('produtos'))


def editar_ou_excluir_produto(request, produto_id, acao):
    registro = _get_produto_repo().obter_por_id(produto_id)
    registro_dict = {
        'id': registro[0],
        'descricao': registro[1],
        'preco_unitario': registro[2],
        'quantidade_estoque': registro[3],
        'categoria_id': registro[4],
        'categoria': registro[5],
    }
    acao = 'Alteração' if acao == 'alterar' else 'Exclusão'
    return render(
        request,
        'produtos_editar.html',
        context={'acao': acao, 'form': _build_produto_form(initial=registro_dict)},
    )


def produtos(request, acao=None, id=None):
    '''
    Metodo responsavel por receber todas as rotas URL do cadastro de Produtos.

    De acordo com a "acao" e o "id" informados, esse metodo ira:
      - 'produtos/': Exibir a pagina de listagem
      - 'produtos/incluir/': Exibir a pagina de inclusao
      - 'produtos/alterar/<:id>/': Exibir a pagina de alteracao
      - 'produtos/excluir/<:id>/': Exibir a pagina de exclusao
      - 'produtos/salvar/': insere, altera ou exclui um registro
    '''
    try:
        if acao is None:
            return listar_produtos(request)
        if acao == 'salvar':
            return salvar_produto(request)
        if acao == 'incluir':
            return incluir_produto(request)
        if acao in ['alterar', 'excluir']:
            return editar_ou_excluir_produto(request, id, acao)
        raise Exception('Ação inválida')
    except Exception as err:
        return render(request, 'home.html', context={'ERRO': err})

# Exibe a página inicial da aplicação
def home(request):
    '''Exibe a pagina inicial da aplicação'''
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)


