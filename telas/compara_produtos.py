import flet as ft
import requests


API_URL = "http://localhost:3000/produtos"

def compara_produtos(page):

    drop_cat_a = ft.Dropdown(label="Categoria A", options=[], expand=1)
    drop_cat_b = ft.Dropdown(label="Categoria B", options=[], expand=1)

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

    produtos_cache = []  

    def carregar_categorias():
        nonlocal produtos_cache
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            produtos_cache = response.json()

            categorias = sorted(set(p["categoria"] for p in produtos_cache))
            opcoes = [ft.dropdown.Option(c) for c in categorias]

            drop_cat_a.options = opcoes
            drop_cat_b.options = opcoes

            page.update()
        except Exception as err:
            page.snack_bar.content = ft.Text(f"Erro ao carregar categorias: {err}")
            page.snack_bar.open = True
            page.update()

    def buscar_click(e):
        cat_a = drop_cat_a.value
        cat_b = drop_cat_b.value
        operacao = operacao_radio_group.value

        if not cat_a or not cat_b:
            page.snack_bar.content = ft.Text("Selecione as duas categorias")
            page.snack_bar.open = True
            page.update()
            return

        set_a = {p["id"] for p in produtos_cache if p["categoria"] == cat_a}
        set_b = {p["id"] for p in produtos_cache if p["categoria"] == cat_b}

        if operacao == "intersection":
            ids_resultado = set_a.intersection(set_b)
        elif operacao == "diff_a_b":
            ids_resultado = set_a.difference(set_b)
        elif operacao == "diff_b_a":
            ids_resultado = set_b.difference(set_a)
        elif operacao == "union":
            ids_resultado = set_a.union(set_b)
        else:
            ids_resultado = set()

        resultados = sorted(
        [p for p in produtos_cache if p["id"] in ids_resultado],
        key=lambda p: p["preco"],
        reverse=False  
        )

        tabela.rows.clear()
        for p in resultados:
            tabela.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(p["id"])),
                ft.DataCell(ft.Text(p["nome"])),
                ft.DataCell(ft.Text(p["marca"])),
                ft.DataCell(ft.Text(p["categoria"])),
                ft.DataCell(ft.Text(str(p["quant"]))),
                ft.DataCell(ft.Text(f'R$ {p["preco"]:.2f}'.replace(".", ","))),
            ]))

        page.update()

    operacao_radio_group = ft.RadioGroup(
        content=ft.Row([
        ft.Radio(value="intersection", label="Ambas as Categorias"),
        ft.Radio(value="diff_a_b", label="Categoria A Apenas"),
        ft.Radio(value="diff_b_a", label="Categoria B Apenas"),
        ft.Radio(value="union", label="Qualquer Categoria"),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
        value="intersection"
)

    layout = ft.Column([
        ft.Text("Comparação de Categorias", size=24, weight="bold"),
        ft.Row([drop_cat_a, drop_cat_b], alignment=ft.MainAxisAlignment.START, spacing=20),
        operacao_radio_group,
        ft.ElevatedButton("Buscar", on_click=buscar_click),
        ft.Divider(),
        tabela
    ], horizontal_alignment=ft.CrossAxisAlignment.START)

    carregar_categorias()

    return layout
