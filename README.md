# 🖥️ Loja de Eletrônicos - Aplicação Flet + API

Este é um projeto acadêmico desenvolvido com **Python** e a biblioteca **Flet**, que simula uma aplicação de cadastro e análise de produtos eletrônicos, consumindo dados de uma **API REST** mockada via `json-server`. A aplicação possui interface gráfica moderna e interativa, permitindo diversas operações sobre os dados.

## 🚀 Funcionalidades

- 📋 **Cadastro de Produtos**  
  Inserção de novos produtos com nome, marca, categoria, quantidade e preço. Dados enviados via POST à API.

- 📊 **Gráfico por Marcas**  
  Exibe um gráfico de barras horizontais agrupando a quantidade de produtos por marca.

- 📈 **Gráfico dos Produtos + Caros**  
  Mostra os produtos mais caros do sistema, ordenados visualmente por preço.

- 🔍 **Pesquisa de Produtos**  
  Busca por nome e categoria simultaneamente, retornando resultados em uma tabela dinâmica.

- ⚖️ **Comparação de Categorias**  
  Compara produtos entre duas categorias, utilizando operações de conjuntos:  
  - Interseção (ambas as categorias)  
  - Diferença (A - B ou B - A)  
  - União (qualquer uma das categorias)  
  Resultados são exibidos ordenados por preço (decrescente).

## 🧰 Tecnologias Utilizadas

- `Python 3`
- `Flet` (GUI Reactiva com Python)
- `json-server` (API fake local)
- `requests` (requisições HTTP)

## 🛠️ Como Executar

### 1. Instale as dependências:
  ```bash
  pip install flet requests
```
### 2. Suba o servidor fake com o JSON:
  ```bash
  json server --watch db.json --port 3000
```
### 3. Execute a aplicação:
```bash
  python loja_esportes
