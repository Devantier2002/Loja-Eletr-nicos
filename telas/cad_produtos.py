import flet as ft
import requests
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 

API_URL = "http://localhost:3000/produtos"  

def cad_produtos(page):
    txt_nome = ft.TextField(label="Nome do Produto", expand=4)
    txt_marca = ft.TextField(label="Marca", expand=2)
    txt_categoria = ft.TextField(label="Categoria", expand=3)
    txt_quant = ft.TextField(label="Quant.", expand=1)
    txt_preco = ft.TextField(label="Preço R$", expand=2)

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Cód.")),
            ft.DataColumn(ft.Text("Nome do Produto")),
            ft.DataColumn(ft.Text("Marca")),
            ft.DataColumn(ft.Text("Categoria")),
            ft.DataColumn(ft.Text("Quant.")),
            ft.DataColumn(ft.Text("Preço R$")),
        ],
        rows=[],
    )

    def carregar_produtos_api():
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            
            produtos = response.json()

            tabela.rows.clear()
            for p in reversed(produtos):
                preco_f = locale.currency(p["preco"], grouping=True)
                tabela.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(p["id"])),
                    ft.DataCell(ft.Text(p["nome"])),
                    ft.DataCell(ft.Text(p["marca"])),
                    ft.DataCell(ft.Text(p["categoria"])),
                    ft.DataCell(ft.Text(str(p["quant"]))),
                    ft.DataCell(ft.Text(preco_f)),
                ]))
            page.update()
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar produtos: {err}"))
            page.snack_bar.open = True
            page.update()

    def enviar_click(e):
        valores = [txt_nome.value, txt_marca.value, txt_categoria.value, txt_quant.value, txt_preco.value]

        if any(v.strip() == "" for v in valores):
            e.page.snack_bar.content = ft.Text("Preencha todos os campos")
            e.page.snack_bar.open = True
            e.page.update()
            return

        try:
            produto = {
                "nome": txt_nome.value,
                "marca": txt_marca.value,
                "categoria": txt_categoria.value,
                "quant": int(txt_quant.value),
                "preco": float(txt_preco.value.replace(",", ".")),
            }

            response = requests.post(API_URL, json=produto)
            response.raise_for_status()

            e.page.snack_bar.content = ft.Text("Produto enviado com sucesso para a API")
            e.page.snack_bar.open = True

            txt_nome.value = txt_marca.value = txt_categoria.value = txt_quant.value = txt_preco.value = ""
            carregar_produtos_api()

        except ValueError:
            e.page.snack_bar.content = ft.Text("Erro: Quantidade deve ser número inteiro e preço um número válido")
            e.page.snack_bar.open = True
        except requests.exceptions.RequestException as err:
            e.page.snack_bar.content = ft.Text(f"Erro ao enviar: {err}")
            e.page.snack_bar.open = True

    def limpar_click(e):
        txt_nome.value = txt_marca.value = txt_categoria.value = txt_quant.value = txt_preco.value = ""
        e.page.update()

    layout = ft.Column([
        ft.Text("Cadastro de Produtos", size=24, weight="bold"),
        ft.Row([txt_nome, txt_marca], spacing=10),
        ft.Row([txt_categoria, txt_quant, txt_preco], spacing=10),
        ft.Row([
            ft.ElevatedButton("Enviar", on_click=enviar_click),
            ft.ElevatedButton("Limpar", on_click=limpar_click),
        ]),
        ft.Divider(),
        ft.Text("Lista dos Produtos Cadastrados:", size=20, weight="bold"),
        ft.Container(
            content=ft.Column(
                [tabela],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            ),
            height=400,
            padding=5,
            border=ft.border.all(1, ft.Colors.GREY_300),     
            border_radius=10,
            bgcolor=ft.Colors.GREY_100                       
        )        
    ], spacing=10)

    carregar_produtos_api()

    return layout  
