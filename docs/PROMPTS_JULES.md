# Diretrizes e Prompts de Tradução de UI/Código para o Jules

Este documento serve como guia de engenharia e conjunto de **Prompts Estruturados** para o **Jules** (ou agentes de IA) converterem as 14 telas (`code.html` e `screen.png`) do diretório `projeto_geral/` em componentes e views nativas em **Python + Flet**, mantendo fidelidade visual milimétrica com o `DESIGN.md`.

---

## 1. Mapeamento das 14 Telas $\rightarrow$ Componentes Flet

| Diretório Original (`projeto_geral/`) | View Flet Alvo (`app/views/`) | Componentes Reutilizáveis |
|---|---|---|
| `conversas_feed_principal` | `app/views/feed_view.py` | `TopAppBar`, `StoryCarousel`, `ChatRow`, `SegmentedToggle` |
| `conversas_feed_unificado_pessoal_comercial`| `app/views/feed_unificado_view.py` | `PillFilter`, `CategoryChip`, `UnreadBadge` |
| `conversas_perfil_pessoal_mariana` | `app/views/profile_pessoal_view.py` | `ContactCard`, `PersonalNotesSection`, `SwitchAccountRow` |
| `conversas_perfil_comercial_caf_bistr` | `app/views/profile_comercial_view.py`| `BusinessHeader`, `StoreStatusPill`, `QuickActionBar` |
| `conversa_ativa_card_pio` | `app/views/chat_active_view.py` | `ChatBubbleInbound`, `ChatBubbleOutbound`, `CatalogCard`, `AudioPlayerWaveform` |
| `feed_e_gerenciador_de_status` | `app/views/status_feed_view.py` | `StorySegmentedRing`, `StatusViewerModal`, `StoryMetrics` |
| `criar_e_publicar_status` | `app/views/status_create_view.py` | `MediaEditorCanvas`, `StickerOverlay`, `StoryPublishDock` |
| `guia_local_mapa_da_cidade` | `app/views/map_view.py` | `MapPin`, `DistanceBadge`, `QuickFilterScroller` |
| `guia_local_hor_rios_e_status_de_funcionamento` | `app/views/local_guide_list_view.py` | `BusinessListCard`, `OpenStatusIndicator`, `RatingStars` |
| `perfil_do_estabelecimento_rota` | `app/views/business_detail_view.py` | `HeroPhotoGallery`, `HighlightsGrid`, `ReviewsList`, `CommunityAccordance` |
| `configura_o_da_loja_hor_rios_flex_veis` | `app/views/store_settings_view.py` | `WeekdayScheduleEditor`, `OverridePauseDrawer`, `CatalogManager` |
| `menu_lateral_perfis_com_fotos_bordas_distintas` | `app/components/side_drawer.py` | `ProfileSwitcherList`, `BorderAvatar`, `DeviceList` |
| `menu_lateral_troca_de_perfil_carteira` | `app/components/side_drawer.py` | `WalletShortcutCard`, `QuickAccountSwitch` |
| `carteira_digital_documentos` | `app/views/wallet_view.py` | `BalanceCard`, `PixActionButton`, `GovBrDocumentCard`, `TransactionRow` |

---

## 2. Prompt Mestre para o Jules: "Tradutor de Telas Stitch (HTML/CSS) para Flet (Python)"

```markdown
Você é um Engenheiro Frontend Especialista em Python e Flet (Flutter Engine).
Sua missão é traduzir a tela HTML/CSS de: `projeto_geral/<NOME_DA_TELA>/code.html` e sua captura `screen.png` para uma View modular em Flet (`app/views/<NOME_DA_VIEW>.py`).

### Regras Mandatórias:
1. **Design System & Tokens**:
   - Use rigorosamente as cores e fontes de `app/core/theme.py` (baseado no `docs/dia1.md` e `DESIGN.md`).
   - Modo Pessoal: Cor Primária Esmeralda `#0F766E`, Superfície `#FAFAFA` / `#F8FAFC`, Borda `#E2E8F0`.
   - Modo Comercial: Cor Secundária Ciano `#0284C7`, Squircle nos avatares comerciais (`border_radius=8`).
   - Fonte: "Plus Jakarta Sans".

2. **Componentização Flet**:
   - Estruture a tela como uma classe herdando de `ft.Container` ou função geradora `def render_<nome_da_tela>(page: ft.Page, app_state) -> ft.Control:`.
   - Separe elementos visuais repetitivos em `app/components/` (ex: botões, cartões, chips).
   - Use `ft.ResponsiveRow`, `ft.Column`, `ft.Row`, `ft.Container` com paddings e bordas fiéis aos protótipos.

3. **Interatividade e Estado**:
   - Conecte cliques de troca de modo (Pessoal vs Comercial), abrindo o menu lateral ou alternando o feed.
   - Deixe ganchos para WebSockets e APIs REST do FastAPI (`backend/app/api/`).

Entregue o código Python completo, sem omissões e 100% tipado.
```

---

## 3. Prompt para o Backend Jules: "Geração de Rotas FastAPI + WebSockets da Fase 1"

```markdown
Você é um Arquiteto Backend Especialista em FastAPI, SQLAlchemy Assíncrono e PostgreSQL/PostGIS.
Sua missão é implementar os endpoints e WebSockets da Fase 1 (Identidade e Mensageria) respeitando o schema `docs/schema-sms.sql`.

### Escopo da Fase 1:
1. **Auth & Perfis (`/api/v1/auth`, `/api/v1/profiles`)**:
   - Criação de usuário, login por telefone/e-mail, listagem e alternância de perfis (Pessoal/Comercial).
2. **Conversas & Mensagens (`/api/v1/conversations`, `/api/v1/messages`)**:
   - Listar feed unificado com filtros `context` ('pessoal'/'negocio') e `tag` ('cliente', 'familia', etc.).
   - Envio de mensagem com suporte a `metadata` JSONB (áudio, waveform, dados de pedido).
3. **WebSocket Realtime (`/ws/chat/{profile_id}`)**:
   - Entrega instantânea de novas mensagens, eventos de digitação e confirmações de leitura (✓✓).
4. **Status / Stories (`/api/v1/statuses`)**:
   - Publicar story com expiração de 24h e registro de visualizações únicas.

Utilize Pydantic v2 para validação e asyncpg/SQLAlchemy para consultas assíncronas de alta performance.
```
