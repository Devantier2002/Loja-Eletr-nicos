import flet as ft
import requests

API_URL = "http://localhost:3000/produtos" 

def graf_marcas(page):

    def obter_produtos_api():
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()

        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao carregar produtos: {err}"))
            page.snack_bar.open = True
            page.update()
            return []

    produtos = obter_produtos_api()
    
    dicionario = {}

    # dicionario = {"Adidas": 2, "Nike": 1}
    for p in produtos:
        marca = p['marca']
        dicionario[marca] = dicionario.get(marca, 0) + 1

    if not dicionario:
        return ft.Text("Nenhum dado disponível.")

    cores = [
        ft.Colors.BLUE,
        ft.Colors.GREEN,
        ft.Colors.ORANGE,
        ft.Colors.PINK,
        ft.Colors.PURPLE,
        ft.Colors.CYAN,
        ft.Colors.RED,
        ft.Colors.YELLOW,
        ft.Colors.AMBER,
        ft.Colors.BROWN
    ]

    largura_max = 1000

    linhas = []

    dicionario2 = dict(sorted(dicionario.items(), 
                        key=lambda item: item[1], reverse=True))

    total_produtos = sum(dicionario2.values())
    
    # converte os valores do dicionario em lista (para poder "fatiar")
    lista_valores = list(dicionario2.values())
    outras = sum(lista_valores[10:])    

    maior_qtd = max(lista_valores[0], outras)

    for i, (marca, qtd) in enumerate(dicionario2.items()):
        
        if i == 10:
            break
        
        largura_barra = (qtd / maior_qtd) * largura_max
        percentual = (qtd / total_produtos) * 100
        cor = cores[i % len(cores)]

        barra = ft.Container(
            width=largura_barra,
            height=30,
            bgcolor=cor,
            border_radius=5,
        )

        linha = ft.Row(
            [
                ft.Text(marca, width=100),
                barra,
                ft.Text(f"{qtd} produto(s) — {percentual:.1f}%", width=160, text_align=ft.TextAlign.RIGHT)
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        linhas.append(linha)

    # linha das outras marcas
    largura_barra = (outras / maior_qtd) * largura_max
    percentual = (outras / total_produtos) * 100
    cor = ft.Colors.GREY

    barra = ft.Container(
        width=largura_barra,
        height=30,
        bgcolor=cor,
        border_radius=5,
    )

    linha = ft.Row(
        [
            ft.Text("Outras Marcas", width=100),
            barra,
            ft.Text(f"{outras} produto(s) — {percentual:.1f}%", width=160, text_align=ft.TextAlign.RIGHT)
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10
    )

    linhas.append(linha)

    return ft.Column(
        [ft.Text("Produtos por Marca", size=22, weight="bold")] + linhas,
        spacing=10,
        scroll=ft.ScrollMode.AUTO
    )
