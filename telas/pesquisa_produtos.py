import flet as ft
import requests

API_URL = "http://localhost:3000/produtos"

def pesquisa_produtos(page):

    drop_categoria = ft.Dropdown(label="Categoria", options=[], expand=3)
    drop_marca = ft.Dropdown(label="Marca", options=[], expand=3)

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Marca")),
            ft.DataColumn(ft.Text("Categoria")),
            ft.DataColumn(ft.Text("Quantidade")),
            ft.DataColumn(ft.Text("Preço")),
        ],
        rows=[]
    )

    produtos_cache = []  # para guardar produtos carregados

    def carregar_opcoes():
        nonlocal produtos_cache
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            produtos_cache = response.json()

            # Extrair categorias únicas
            categorias = sorted(set(p["categoria"] for p in produtos_cache))
            drop_categoria.options = [ft.dropdown.Option(c) for c in categorias]

            # Inicialmente marca vazio, ou poderia mostrar todas marcas
            drop_marca.options = []

            page.update()
        except Exception as err:
            page.snack_bar.content = ft.Text(f"Erro ao carregar opções: {err}")
            page.snack_bar.open = True
            page.update()

    def on_categoria_change(e):
        categoria_selecionada = e.control.value

        # Filtra marcas só da categoria selecionada
        marcas = sorted(set(p["marca"] for p in produtos_cache if p["categoria"] == categoria_selecionada))
        drop_marca.options = [ft.dropdown.Option(m) for m in marcas]

        # Limpa seleção atual de marca para forçar nova escolha
        drop_marca.value = None

        page.update()

    drop_categoria.on_change = on_categoria_change

    def buscar_click(e):
        filtro_categoria = drop_categoria.value
        filtro_marca = drop_marca.value

        try:
            # Usa o cache para evitar nova requisição
            produtos = produtos_cache

            filtrados = [
                p for p in produtos
                if (filtro_categoria is None or p["categoria"] == filtro_categoria) and
                   (filtro_marca is None or p["marca"] == filtro_marca)
            ]

            tabela.rows.clear()
            for p in filtrados:
                tabela.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(p["id"])),
                    ft.DataCell(ft.Text(p["nome"])),
                    ft.DataCell(ft.Text(p["marca"])),
                    ft.DataCell(ft.Text(p["categoria"])),
                    ft.DataCell(ft.Text(str(p["quant"]))),
                    ft.DataCell(ft.Text(f'R$ {p["preco"]:.2f}'.replace(".", ","))),
                ]))

            page.update()
        except Exception as err:
            page.snack_bar.content = ft.Text(f"Erro: {err}")
            page.snack_bar.open = True
            page.update()

    layout = ft.Column([
        ft.Text("Pesquisar Produtos", size=24, weight="bold"),
        ft.Row([
            drop_categoria,
            drop_marca,
            ft.ElevatedButton("Buscar", on_click=buscar_click)
        ], spacing=10),
        ft.Divider(),
        tabela
    ])

    carregar_opcoes()

    return layout
