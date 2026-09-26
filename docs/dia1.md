# Registro Completo do Projeto — App SMS (Mensageria + Guia Local + Carteira)
**Data:** 26/09/2026 — Dia 1

---

## 1. Visão Geral

App mobile de mensagens que une conversa pessoal (estilo WhatsApp) e conversa com comércios/empresas no mesmo feed, com o usuário podendo alternar entre perfil pessoal e perfil comercial na mesma conta.

---

## 2. Escopo por Fases

1. **Fase 1 — Mensageria (Núcleo — MVP)**
   - Conversas 1:1 e em grupo
   - Alternância fluida entre perfil pessoal e perfil comercial
   - Status/stories (público para comércio, privado para pessoal, expiração de 24h)
   - "Pedido" não é rastreado por máquina de estados complexa — é conteúdo de mensagem/payload dentro de uma conversa marcada como `negocio`. Sem tabela de pedidos pesada na v1.
   - Bloco de notas pessoal ("Notas Fixo") e mensagens salvas.
   - Gestão de contatos com relações (família, amigo) e convites.

2. **Fase 2 — Guia Local / Mapa**
   - Empresa marca sua localização no mapa (PostGIS `geography(Point, 4326)`)
   - Upload de foto da fachada e ponto de referência
   - Configuração de horário de funcionamento (grade semanal + pausas pontuais do dia como "pausar 1h", "fechado hoje", "aviso na vitrine")
   - Cartões fixados no perfil da loja (Cozinha, Música, Pagamento)
   - Confirmação colaborativa de funcionamento pela comunidade ("está aberto?")
   - Catálogo/cardápio de produtos/serviços com preço e foto
   - Feed de publicações permanentes da empresa (Ambiente, Pratos, Bastidores) e avaliações com tags e respostas do proprietário.

3. **Fase 3 — Carteira Digital & Documentos**
   - Contas e pagamentos (saldo em conta, transferências Pix in/out, histórico de transações)
   - Cartões de pagamento sempre tokenizados via provedor externo (Asaas, Pagar.me, EFI, Mercado Pago) — nunca salvar o PAN (número do cartão bruto) no banco.
   - Documentos oficiais digitais (referência/token da integração Gov.br, nunca salvar dados brutos de CNH, RG, CNS, Título).

---

## 3. Stack Tecnológica

- **Backend**: Python + FastAPI (Uvicorn, asyncpg / SQLAlchemy, WebSockets para chat em tempo real)
- **Banco de Dados**: PostgreSQL + PostGIS (Neon ou Supabase; extensões `pgcrypto`, `postgis`, `pg_trgm`)
- **Mobile**: Python + **Flet** (compila nativamente para Flutter — mesmo código gera `.apk` para Android e `.ipa` para iOS sem precisar de Flutter/Dart/Swift manual)
- **Mapa**: MapLibre GL + tiles OpenStreetMap/MapTiler com consultas espaciais PostGIS (`ST_DWithin` para cálculo de raio/distância)
- **Armazenamento de Mídia**: Supabase Storage no início; migração para Cloudflare R2 quando escalar.
- **Design System**: Emerald & Cyan (Tokens do Stitch com tema Esmeralda `#0F766E` para Pessoal e Ciano `#0284C7` para Comercial, tipografia *Plus Jakarta Sans*).

---

## 4. Estratégia de Lançamento & Distribuição

- **Android Primeiro**:
  - Desenvolvimento com `flet run` (hot reload) no emulador ou aparelho físico via cabo/Wi-Fi.
  - Build de `.apk` com `flet build apk` para distribuição direta aos testadores (custo zero).
  - Publicação futura via Google Play Console (teste interno/aberto).
- **iOS Depois**:
  - `flet build ipa` sobre o mesmo código Flet (sem necessidade de reescrita), necessitando de Mac/Xcode ou pipeline CI/CD (GitHub Actions / Codemagic).

---

## 5. Segurança & Conformidade

- **Fase 1**: TLS padrão (HTTPS/WSS) protegendo dados em trânsito.
- **Evolução Criptográfica**: Futuro upgrade para criptografia ponta a ponta (E2EE) com **PyNaCl** (X25519 + cifras simétricas) ou protocolo **python-olm** (Signal/Matrix).
- **PCI-DSS & LGPD**: Zero armazenamento de PAN de cartão ou fotos/documentos brutos — uso exclusivo de tokens PSP e Gov.br.

---

## 6. Schema DDL Completo (PostgreSQL + PostGIS)

```sql
-- =========================================================
-- Schema do App SMS — Mensageria + Guia Local + Carteira
-- PostgreSQL + PostGIS
-- Revisão 2 — auditado contra as 14 telas do protótipo
-- =========================================================

create extension if not exists pgcrypto;
create extension if not exists postgis;
create extension if not exists pg_trgm;

create or replace function set_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

-- =========================================================
-- FASE 1 — IDENTIDADE
-- =========================================================

create table users (
  id            uuid primary key default gen_random_uuid(),
  phone         text unique,
  email         text unique,
  auth_provider text not null default 'password',
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  constraint users_phone_or_email check (phone is not null or email is not null)
);
create trigger trg_users_updated_at before update on users
  for each row execute function set_updated_at();

-- preferências gerais da conta (tema, notificações) — "Tema Claro" no menu
create table user_settings (
  user_id               uuid primary key references users(id) on delete cascade,
  theme                 text not null default 'claro' check (theme in ('claro', 'escuro')),
  notifications_enabled boolean not null default true,
  updated_at            timestamptz not null default now()
);
create trigger trg_user_settings_updated_at before update on user_settings
  for each row execute function set_updated_at();

-- "Dispositivos Conectados — Web & Mac ativos"
create table linked_devices (
  id             uuid primary key default gen_random_uuid(),
  user_id        uuid not null references users(id) on delete cascade,
  device_name    text not null,
  device_type    text not null check (device_type in ('mobile', 'web', 'desktop')),
  last_active_at timestamptz not null default now(),
  created_at     timestamptz not null default now(),
  revoked_at     timestamptz
);
create index idx_devices_user on linked_devices(user_id);

-- um user pode ter N perfis: pessoal e/ou comercial(is)
create table profiles (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null references users(id) on delete cascade,
  type         text not null check (type in ('pessoal', 'comercial')),
  display_name text not null,
  avatar_id    uuid, -- fk para attachments, ligada depois de attachments existir
  bio          text,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);
create index idx_profiles_user on profiles(user_id);
create trigger trg_profiles_updated_at before update on profiles
  for each row execute function set_updated_at();

-- =========================================================
-- FASE 1 — MENSAGERIA
-- =========================================================

create table attachments (
  id                      uuid primary key default gen_random_uuid(),
  uploaded_by_profile_id  uuid not null references profiles(id) on delete cascade,
  storage_url             text not null,
  mime_type               text not null,
  size_bytes              bigint,
  created_at              timestamptz not null default now()
);
create index idx_attachments_uploader on attachments(uploaded_by_profile_id);

alter table profiles
  add constraint fk_profiles_avatar
  foreign key (avatar_id) references attachments(id) on delete set null;

-- 'negocio' separa o feed pessoal do feed comercial na interface.
-- 'tag' é o rótulo livre visto nas listas (cliente, fornecedor, familia,
-- amigos, orcamento, evento) — organização visual, não é rastreio de pedido.
create table conversations (
  id          uuid primary key default gen_random_uuid(),
  kind        text not null check (kind in ('direta', 'grupo')),
  context     text not null default 'pessoal' check (context in ('pessoal', 'negocio')),
  tag         text check (tag in ('cliente', 'fornecedor', 'familia', 'amigos', 'orcamento', 'evento')),
  title       text, -- usado em grupos ("Família Silva")
  avatar_id   uuid references attachments(id) on delete set null,
  created_at  timestamptz not null default now()
);

create table conversation_participants (
  conversation_id uuid not null references conversations(id) on delete cascade,
  profile_id      uuid not null references profiles(id) on delete cascade,
  role            text not null default 'membro' check (role in ('membro', 'admin')),
  joined_at       timestamptz not null default now(),
  muted           boolean not null default false,
  primary key (conversation_id, profile_id)
);
create index idx_participants_profile on conversation_participants(profile_id);

create table messages (
  id                   uuid primary key default gen_random_uuid(),
  conversation_id      uuid not null references conversations(id) on delete cascade,
  sender_profile_id    uuid not null references profiles(id) on delete cascade,
  content_type         text not null check (content_type in ('texto', 'imagem', 'audio', 'documento')),
  content_text         text,
  attachment_id        uuid references attachments(id) on delete set null,
  reply_to_message_id  uuid references messages(id) on delete set null,
  metadata             jsonb not null default '{}'::jsonb, -- Indicação: Antigravity (áudio waveform, duração, dados de pedido)
  created_at           timestamptz not null default now()
);
create index idx_messages_conversation on messages(conversation_id, created_at);
create index idx_messages_sender on messages(sender_profile_id);

-- leitura por participante (necessário para grupos, onde "lido" não é único)
create table message_status (
  message_id  uuid not null references messages(id) on delete cascade,
  profile_id  uuid not null references profiles(id) on delete cascade,
  status      text not null check (status in ('enviado', 'entregue', 'lido')),
  updated_at  timestamptz not null default now(),
  primary key (message_id, profile_id)
);

-- "Mensagens Salvas 28"
create table saved_messages (
  profile_id  uuid not null references profiles(id) on delete cascade,
  message_id  uuid not null references messages(id) on delete cascade,
  saved_at    timestamptz not null default now(),
  primary key (profile_id, message_id)
);

-- "Notas Fixo" — bloco de notas pessoal, sem relação com chat
create table personal_notes (
  id          uuid primary key default gen_random_uuid(),
  profile_id  uuid not null references profiles(id) on delete cascade,
  content     text not null,
  pinned      boolean not null default true,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
create trigger trg_notes_updated_at before update on personal_notes
  for each row execute function set_updated_at();

-- relação entre perfis (família/amigo) e status de convite —
-- base para as abas "Família / Amigos / Grupos" e "Convidar amigos"
create table contacts (
  owner_profile_id   uuid not null references profiles(id) on delete cascade,
  contact_profile_id uuid not null references profiles(id) on delete cascade,
  relation_label     text not null check (relation_label in ('familia', 'amigo')),
  status             text not null default 'pendente' check (status in ('pendente', 'aceito')),
  created_at         timestamptz not null default now(),
  primary key (owner_profile_id, contact_profile_id)
);

-- =========================================================
-- FASE 1 — STATUS / STORIES
-- =========================================================

create table statuses (
  id              uuid primary key default gen_random_uuid(),
  profile_id      uuid not null references profiles(id) on delete cascade,
  attachment_id   uuid not null references attachments(id) on delete cascade,
  caption         text,
  visibility      text not null check (visibility in ('publico', 'privado')),
  catalog_item_id uuid, -- fk para business_catalog_items, ligada na Fase 2
  created_at      timestamptz not null default now(),
  expires_at      timestamptz not null default (now() + interval '24 hours')
);
create index idx_statuses_profile on statuses(profile_id);
create index idx_statuses_expires on statuses(expires_at);

create table status_views (
  status_id         uuid not null references statuses(id) on delete cascade,
  viewer_profile_id uuid not null references profiles(id) on delete cascade,
  viewed_at         timestamptz not null default now(),
  primary key (status_id, viewer_profile_id)
);

-- =========================================================
-- FASE 2 — GUIA LOCAL / MAPA
-- =========================================================

create table business_categories (
  id   uuid primary key default gen_random_uuid(),
  name text not null unique -- ex: 'Alimentação', 'Serviços', 'Saúde', 'Moda'
);

create table businesses (
  id              uuid primary key default gen_random_uuid(),
  profile_id      uuid not null unique references profiles(id) on delete cascade,
  category_id     uuid references business_categories(id),
  description     text,
  address_text    text,
  reference_point text, -- "Em frente à Praça da Matriz, ao lado do Café Colonial"
  phone           text,
  location        geography(Point, 4326) not null,
  facade_photo_id uuid references attachments(id) on delete set null,
  verified        boolean not null default false,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);
create index idx_businesses_location on businesses using gist(location);
create index idx_businesses_category on businesses(category_id);
create trigger trg_businesses_updated_at before update on businesses
  for each row execute function set_updated_at();

create table business_hours (
  id           uuid primary key default gen_random_uuid(),
  business_id  uuid not null references businesses(id) on delete cascade,
  weekday      smallint not null check (weekday between 0 and 6), -- 0 = domingo
  opens_at     time,
  closes_at    time,
  is_closed    boolean not null default false,
  unique (business_id, weekday)
);

-- pausas pontuais do dia ("pausar 1h", "fechou mais cedo hoje", aviso na vitrine)
create table business_status_overrides (
  id            uuid primary key default gen_random_uuid(),
  business_id   uuid not null references businesses(id) on delete cascade,
  override_type text not null check (override_type in ('pausa', 'fechado_hoje', 'aviso')),
  note          text,
  starts_at     timestamptz not null default now(),
  ends_at       timestamptz,
  created_at    timestamptz not null default now()
);
create index idx_overrides_business on business_status_overrides(business_id);

-- "Status Fixados do Estabelecimento": Cozinha, Música, Pagamento etc —
-- cartões informativos fixados no perfil, diferente do aviso temporário acima
create table business_highlights (
  id          uuid primary key default gen_random_uuid(),
  business_id uuid not null references businesses(id) on delete cascade,
  category    text not null check (category in ('cozinha', 'musica', 'pagamento', 'geral')),
  title       text not null,
  description text,
  created_at  timestamptz not null default now(),
  expires_at  timestamptz
);
create index idx_highlights_business on business_highlights(business_id);

-- confirmação colaborativa ("clientes confirmam se está aberto")
create table business_open_confirmations (
  id                    uuid primary key default gen_random_uuid(),
  business_id           uuid not null references businesses(id) on delete cascade,
  confirming_profile_id uuid not null references profiles(id) on delete cascade,
  is_open               boolean not null,
  confirmed_at          timestamptz not null default now()
);
create index idx_confirmations_business on business_open_confirmations(business_id, confirmed_at);

-- catálogo/cardápio do comércio ("Enviar Catálogo", "Novo Menu Primavera R$ 38,00")
create table business_catalog_items (
  id                uuid primary key default gen_random_uuid(),
  business_id       uuid not null references businesses(id) on delete cascade,
  name              text not null,
  price             numeric(12,2),
  photo_attachment_id uuid references attachments(id) on delete set null,
  description       text,
  active            boolean not null default true,
  created_at        timestamptz not null default now()
);
create index idx_catalog_business on business_catalog_items(business_id);

alter table statuses
  add constraint fk_statuses_catalog_item
  foreign key (catalog_item_id) references business_catalog_items(id) on delete set null;

-- "Publicações do Local" — posts permanentes do perfil comercial
-- (diferente de status/stories, que expiram em 24h)
create table business_posts (
  id            uuid primary key default gen_random_uuid(),
  business_id   uuid not null references businesses(id) on delete cascade,
  attachment_id uuid references attachments(id) on delete set null,
  category      text check (category in ('ambiente', 'pratos', 'bastidores', 'geral')),
  caption       text not null,
  created_at    timestamptz not null default now()
);
create index idx_business_posts_business on business_posts(business_id, created_at);

create table business_post_likes (
  post_id     uuid not null references business_posts(id) on delete cascade,
  profile_id  uuid not null references profiles(id) on delete cascade,
  created_at  timestamptz not null default now(),
  primary key (post_id, profile_id)
);

-- avaliações da comunidade, com resposta do dono e curtidas
create table business_reviews (
  id                uuid primary key default gen_random_uuid(),
  business_id       uuid not null references businesses(id) on delete cascade,
  reviewer_profile_id uuid not null references profiles(id) on delete cascade,
  rating            smallint not null check (rating between 1 and 5),
  comment           text,
  tags              text[], -- ex: {'Atendimento ágil','Comida impecável'}
  created_at        timestamptz not null default now(),
  unique (business_id, reviewer_profile_id)
);
create index idx_reviews_business on business_reviews(business_id);

create table business_review_replies (
  id         uuid primary key default gen_random_uuid(),
  review_id  uuid not null unique references business_reviews(id) on delete cascade,
  reply_text text not null,
  created_at timestamptz not null default now()
);

create table business_review_likes (
  review_id  uuid not null references business_reviews(id) on delete cascade,
  profile_id uuid not null references profiles(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (review_id, profile_id)
);

-- =========================================================
-- FASE 3 — CARTEIRA DIGITAL
-- =========================================================

create table wallet_accounts (
  id          uuid primary key default gen_random_uuid(),
  profile_id  uuid not null unique references profiles(id) on delete cascade,
  balance     numeric(14,2) not null default 0,
  currency    text not null default 'BRL',
  updated_at  timestamptz not null default now()
);
create trigger trg_wallet_updated_at before update on wallet_accounts
  for each row execute function set_updated_at();

create table wallet_transactions (
  id                uuid primary key default gen_random_uuid(),
  wallet_account_id uuid not null references wallet_accounts(id) on delete cascade,
  type              text not null check (type in ('credito', 'debito', 'pix_in', 'pix_out')),
  amount            numeric(14,2) not null,
  external_provider text, -- ex: 'asaas', 'pagarme', 'efi'
  external_ref      text, -- id da transação no provedor
  status            text not null default 'concluida' check (status in ('pendente', 'concluida', 'falhou')),
  created_at        timestamptz not null default now()
);
create index idx_wallet_tx_account on wallet_transactions(wallet_account_id, created_at);

-- cartões: sempre token do provedor, nunca o PAN
create table payment_methods (
  id             uuid primary key default gen_random_uuid(),
  profile_id     uuid not null references profiles(id) on delete cascade,
  provider       text not null, -- ex: 'asaas', 'pagarme'
  provider_token text not null, -- token/id do cartão no provedor
  brand          text,          -- 'visa', 'mastercard' etc, só para exibição
  last4          char(4),
  is_default     boolean not null default false,
  created_at     timestamptz not null default now()
);
create index idx_payment_methods_profile on payment_methods(profile_id);

-- documentos: só referência ao Gov.br, nunca o dado bruto
create table identity_documents (
  id          uuid primary key default gen_random_uuid(),
  profile_id  uuid not null references profiles(id) on delete cascade,
  doc_type    text not null check (doc_type in ('cnh', 'rg_cin', 'cns', 'titulo_eleitor')),
  govbr_ref   text not null, -- token/referência da integração, não o número do documento
  status      text not null default 'valido' check (status in ('valido', 'expirado', 'pendente')),
  verified_at timestamptz,
  updated_at  timestamptz not null default now(),
  unique (profile_id, doc_type)
);
create trigger trg_docs_updated_at before update on identity_documents
  for each row execute function set_updated_at();

-- Busca textual rápida de perfis e comércios
create index ifnot exists idx_profiles_name_trgm on profiles using gin(display_name gin_trgm_ops);
```

---

## 7. Dicionário de Dados & Mapeamento das 14 Telas

| Tabela | Para quê serve | Tela de Origem (Protótipo) |
|---|---|---|
| `users` | Conta de login (telefone/e-mail) | Base de autenticação |
| `user_settings` | Tema claro/escuro, notificações | Menu Lateral (Ajustes) |
| `linked_devices` | "Dispositivos Conectados — Web & Mac" | Menu Lateral |
| `profiles` | Perfil pessoal e/ou comercial na mesma conta | Alternar Contas |
| `attachments` | Qualquer mídia enviada (foto, PDF, áudio) | Todas as telas com anexo |
| `conversations` | Conversa 1:1 ou grupo; `context` (pessoal/negocio) e `tag` | Feed Unificado, Feed Pessoal, Feed Comercial |
| `conversation_participants` | Participantes do chat (pessoal/grupo) | Feed Unificado |
| `messages` | Mensagens de texto, áudio, anexo e metadados JSONB | Conversa Ativa |
| `message_status` | Status de entrega/leitura por participante (✓✓) | Conversa Ativa |
| `saved_messages` | "Mensagens Salvas — 28" | Menu Lateral |
| `personal_notes` | "Notas Fixo" — bloco de notas pessoal | Perfil Pessoal |
| `contacts` | Relações de amizade/família + status de convites | Abas Família/Amigos/Grupos, Convidar amigos |
| `statuses` | Story de 24h público ou privado | Criar e Publicar Status |
| `status_views` | Contagem de visualizações únicas de stories | Feed de Status |
| `business_categories` | Categorias (Alimentação, Saúde, Serviços) | Guia Local |
| `businesses` | Dados do comércio (Localização PostGIS, fachada, telefone) | Perfil do Estabelecimento, Guia Local |
| `business_hours` | Grade de horários semanais | Configuração da Loja |
| `business_status_overrides` | Pausa temporária (1h), fechado hoje, avisos de vitrine | Configuração da Loja |
| `business_highlights` | Cartões fixados (Cozinha, Música, Pagamento) | Perfil do Estabelecimento |
| `business_open_confirmations` | Confirmações da comunidade ("está aberto?") | Configuração da Loja |
| `business_catalog_items` | Itens de cardápio/catálogo com preços e fotos | Conversa Ativa, Cardápio, Stories |
| `business_posts` | Posts permanentes (Ambiente, Pratos, Bastidores) | Perfil do Estabelecimento |
| `business_post_likes` | Curtidas em posts permanentes | Perfil do Estabelecimento |
| `business_reviews` | Avaliações com notas de 1 a 5 e tags | Perfil do Estabelecimento |
| `business_review_replies` | Respostas do proprietário às avaliações | Perfil do Estabelecimento |
| `business_review_likes` | Curtidas em avaliações | Perfil do Estabelecimento |
| `wallet_accounts` | Saldo em conta e moeda | Carteira Digital |
| `wallet_transactions` | Histórico de transações Pix e transferências | Carteira Digital |
| `payment_methods` | Cartões de crédito tokenizados | Carteira Digital |
| `identity_documents` | Token do Gov.br para CNH/RG/CNS/Título | Carteira Digital |

---

## 8. Indicações de Melhorias & Recomendações Técnicas

1. **Campo `metadata JSONB` na tabela `messages`:**
   - Adicionado para acomodar com máxima flexibilidade metadados ricos de mensagens, como: duração de áudio (`duration_ms`), array de amplitudes para waveform (`[10, 45, 80...]`), e payload formatado de pedidos sem acoplar tabelas complexas na Fase 1.
   - *— Indicação: Antigravity*

2. **Índices de Busca Textual Trigram (`pg_trgm` com GIN):**
   - Criação do índice `idx_profiles_name_trgm` na coluna `display_name` da tabela `profiles`, garantindo busca instantânea e com tolerância a digitação ("fuzzy search") nas listas de contatos e no Guia Local.
   - *— Indicação: Antigravity*

3. **Validação de Unicidade em Conversas Diretas (1:1):**
   - Garantir na camada de serviço do FastAPI que a abertura de um chat direto entre dois `profile_id` reutilize a conversa existente em vez de duplicar registros em `conversations`.
   - *— Indicação: Antigravity*

4. **Gerenciamento de Estado Reativo e Tema no Mobile (Flet):**
   - Criar um módulo centralizador de tokens de design `app/core/theme.py` que leia dinamicamente o `DESIGN.md` e alterne dinamicamente a paleta principal entre **Verde Esmeralda (`#0F766E`)** no Perfil Pessoal e **Ciano Elétrico (`#0284C7`)** no Perfil Comercial.
   - *— Indicação: Antigravity*
