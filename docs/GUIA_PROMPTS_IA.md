# Guia de Engenharia e Prompts para IAs (ChatGPT, Jules e Codex)
**Projeto:** SMS — App Mobile de Mensageria, Guia Local e Carteira Digital  
**Linguagem & Framework:** Python 3.10+ com **Flet** (Engine Flutter)  
**Design System:** Emerald & Cyan (`app/core/theme.py` e `docs/dia1.md`)

---

## 1. Instruções Gerais para as IAs

Qualquer IA (ChatGPT com visão, Jules ou Codex) deve seguir rigorosamente as seguintes diretrizes:

1. **Contexto de Execução:** O aplicativo é **100% Mobile**. A interface deve ser projetada para viewport de celular (baseline de 390px a 430px de largura).
2. **Tokens de Design (Mandatórios):**
   - **Modo Pessoal:** Cor Primária Esmeralda `#0F766E`, Superfícies `#FAF8FF` / `#FFFFFF`, Avatares circulares (`border_radius=9999`).
   - **Modo Comercial:** Cor Secundária Ciano Elétrico `#0284C7`, Avatares comerciais em formato Squircle (`border_radius=8`).
   - **Bordas & Divisores:** Linhas ultrafinas de 0.5px com cor `#E2E8F0`.
   - **Tipografia:** `Plus Jakarta Sans`.
3. **Local de Destino dos Arquivos:**
   - Telas completas: `app/views/<nome_da_tela>_view.py`
   - Componentes reutilizáveis (botões, bolhas, drawers, carrosséis): `app/components/<nome_do_componente>.py`
   - Tokens de Tema: `app/core/theme.py`

---

## 2. Prompt Mestre para o ChatGPT (Análise Visual do PNG + HTML)

> **Como usar:** No ChatGPT (com suporte a upload de arquivos/imagens), anexe o arquivo `screen.png` e o `code.html` da pasta da tela desejada em `projeto_geral/` e envie o prompt abaixo:

```text
Você é um Arquiteto de Software e Engenheiro Frontend sênior especializado em Python e Flet (Flutter).

Analise a imagem em anexo (screen.png) e a estrutura semântica do arquivo HTML (code.html). Sua tarefa é transcrever essa tela com fidelidade visual milimétrica para um módulo nativo em Python utilizando a biblioteca FLET.

Contexto do Projeto SMS:
- App mobile de mensageria pessoal e comercial estilo WhatsApp + Google Maps + Carteira.
- Utilizamos os tokens de tema definidos no módulo `app.core.theme` (Colors, Radius, Typography).
- A tela deve ser responsiva para celular (largura 390px-430px).

Estrutura esperada do código:
1. Crie uma classe ou função geradora `def build_view(page: ft.Page, on_navigate=None) -> ft.Control:`.
2. Mapeie todos os elementos visuais da imagem: TopAppBar, listas, carrosséis, badges, botões flutuantes, inputs e cartões.
3. Utilize os componentes nativos do Flet: `ft.Container`, `ft.Row`, `ft.Column`, `ft.ListView`, `ft.Icon`, `ft.CircleAvatar`, `ft.TextField`, `ft.ElevatedButton`, `ft.Badge`.
4. Garanta espaçamentos, paddings, tamanhos de fonte e cores idênticos ao protótipo.
5. Não utilize código placeholder; entregue o código completo, funcional e pronto para rodar.

Entregue o código Python formatado indicando o caminho exato onde o arquivo deve ser salvo (ex: `app/views/feed_unificado_view.py`).
```

---

## 3. Prompt para o Jules / Codex (Geração Automatizada de Código no Repositório)

> **Como usar:** Para o Jules ou agentes com acesso direto ao terminal e sistema de arquivos:

```text
Atue como o desenvolvedor responsável por implementar as views do app SMS em Flet.

Tarefa:
Leia o arquivo de código em `projeto_geral/{NOME_DA_PASTA}/code.html` e a especificação de design em `docs/dia1.md`.
Converta essa tela para um arquivo Python limpo em `app/views/{NOME_DA_VIEW}.py` utilizando a biblioteca `flet`.

Diretrizes obrigatórias:
1. Importe os tokens de estilo: `from app.core.theme import Colors, Radius, Typography`.
2. Encapsule a view retornando um `ft.Container` ou `ft.Column` expansível que se ajuste ao container mobile.
3. Se houver componentes reutilizáveis (ex: StoryRing, ChatBubble, BusinessCard), crie-os separadamente na pasta `app/components/`.
4. Adicione interatividade aos botões (ex: alternar estados visuais, callbacks de clique e navegação).
5. Certifique-se de que não haja dependências quebradas e que o código possa ser importado diretamente no `app/main.py`.
```

---

## 4. Tabela de Conversão das 14 Telas do Projeto

Utilize esta lista para instruir a ordem de execução para a IA:

| # | Pasta Original (`projeto_geral/`) | Arquivo Alvo no Flet | Descrição da Tela |
|---|---|---|---|
| 1 | `conversas_feed_principal` | `app/views/feed_view.py` | Feed principal de mensagens com carrossel de stories |
| 2 | `conversas_feed_unificado_pessoal_comercial` | `app/views/feed_unificado_view.py` | Feed com filtro segmented bar (Tudo, Bistrô, Pessoal) |
| 3 | `conversas_perfil_pessoal_mariana` | `app/views/profile_pessoal_view.py` | Perfil pessoal com notas fixas e abas de amigos/família |
| 4 | `conversas_perfil_comercial_caf_bistr` | `app/views/profile_comercial_view.py` | Perfil do lojista com switch de status "Loja Aberta" |
| 5 | `conversa_ativa_card_pio` | `app/views/chat_active_view.py` | Conversa ativa com cards de cardápio e pedido |
| 6 | `feed_e_gerenciador_de_status` | `app/views/status_feed_view.py` | Feed e anéis segmentados de stories |
| 7 | `criar_e_publicar_status` | `app/views/status_create_view.py` | Editor e publicador de novo status/story |
| 8 | `guia_local_mapa_da_cidade` | `app/views/map_view.py` | Mapa da cidade com marcadores de estabelecimentos |
| 9 | `guia_local_hor_rios_e_status_de_funcionamento` | `app/views/local_guide_view.py` | Lista de lojas com filtros de raio e horários |
| 10 | `perfil_do_estabelecimento_rota` | `app/views/business_detail_view.py` | Detalhe do comércio, fotos, avaliações e rotas |
| 11 | `configura_o_da_loja_hor_rios_flex_veis` | `app/views/store_settings_view.py` | Configuração de horários semanais e pausas de 1h |
| 12 | `menu_lateral_perfis_com_fotos_bordas_distintas` | `app/components/side_drawer.py` | Menu lateral com lista de contas conectadas |
| 13 | `menu_lateral_troca_de_perfil_carteira` | `app/components/side_drawer.py` | Menu lateral com atalho para a carteira digital |
| 14 | `carteira_digital_documentos` | `app/views/wallet_view.py` | Carteira com saldo, Pix e documentos Gov.br |
