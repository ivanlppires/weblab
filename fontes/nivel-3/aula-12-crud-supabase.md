# Aula 12 — CRUD com banco em nuvem (Supabase)

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Comparar API própria (Express+MySQL), Firebase e Supabase, e justificar quando cada um é a escolha certa.
- Criar um projeto Supabase, entender a diferença entre chave `anon` e `service_role`, e nunca expor a segunda no front.
- Criar tabelas com SQL diretamente no SQL Editor, com `uuid` como chave primária e `timestamptz` para datas.
- Explicar o que é Row Level Security, por que o Supabase exige, e reconhecer a armadilha do `data: []` silencioso.
- Escrever policies de leitura pública, inserção autenticada e edição/exclusão restrita ao dono.
- Usar `@supabase/supabase-js` para `select`, `insert`, `update`, `delete`, joins e paginação, sempre tratando `{ data, error }`.
- Implementar login com Supabase Auth e conectar `auth.uid()` às policies.
- Assinar mudanças em tempo real com Realtime e implementar o padrão Adapter trocando o back-end via variável de ambiente.

## 📋 Pré-requisitos desta aula

Na Aula 11 fechamos o CRUD de eventos ponta a ponta: Vue chamando `services/`, Express validando e persistindo no MySQL, Firebase autenticando. Hoje mudamos de fornecedor: o mesmo recurso `evento`, agora falando direto com o **Supabase** — sem API própria no meio. É a mesma pergunta de arquitetura de sempre ("onde mora a lógica?"), respondida de um jeito diferente.

Checklist antes de começar:

- [ ] `unieventos-web` funcionando com o CRUD da Aula 11 (Express+MySQL+Firebase).
- [ ] Conta no [supabase.com](https://supabase.com) (login com GitHub é o mais rápido).
- [ ] Node.js 22.22.2 e npm 10.9.7 instalados.
- [ ] Confortável com SQL básico (`SELECT`, `INSERT`, `CREATE TABLE`) — revisado na Aula 09 no contexto do MySQL.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Comparação Express×Firebase×Supabase; criar projeto; chaves; criar tabelas por SQL; Row Level Security e policies |
| 2 | 50 min | `@supabase/supabase-js`: CRUD completo, joins, paginação, Supabase Auth |
| 3 | 50 min | Storage, Realtime, padrão Adapter, laboratório comparativo |

## 1. Três formas de resolver o mesmo problema

O UniEventos já tem back-end funcionando: Express + MySQL, com autenticação Firebase por cima. Por que aprender mais uma abordagem?

Porque na vida profissional você vai escolher — e a escolha tem trade-offs reais, não é só gosto. Comparação honesta:

| Critério | API própria (Express+MySQL) | Firebase | Supabase |
|---|---|---|---|
| O que resolve | Controle total sobre lógica e dados | Auth + Firestore/Storage prontos, sem servidor próprio | Postgres gerenciado + Auth + Storage, sem servidor próprio |
| Banco de dados | Você escolhe e administra (MySQL aqui) | Firestore (NoSQL, documentos) | Postgres (SQL relacional, o mesmo paradigma do MySQL) |
| Onde mora a regra de negócio | No seu back-end, você escreve tudo | Cloud Functions (custo extra) ou no front (arriscado) | SQL/policies no banco, ou funções Postgres, ou API própria por cima |
| Curva de aprendizado | Alta (você monta tudo) | Média (SDK, mas modelo de dados diferente) | Baixa se já sabe SQL |
| Vendor lock-in | Nenhum — seu código, seu servidor | Alto — Firestore não é portável | Médio — é Postgres puro por baixo, mais fácil de migrar |
| Quando escolher | Regra de negócio complexa, controle fino, já tem back-end | Protótipo rápido, app mobile-first, tempo real nativo | Precisa de SQL relacional gerenciado, quer Postgres sem administrar servidor |

> **💡 Dica**
> Não existe "o melhor" fora de contexto. O UniEventos usa MySQL porque a disciplina precisa ensinar SQL relacional e arquitetura em camadas. Se o requisito fosse "app mobile com sincronização offline automática", Firebase seria mais natural. Se o requisito fosse "preciso de Postgres gerenciado sem administrar servidor, com auth pronta", Supabase entra bem. Custo de saída (trocar de fornecedor depois) também pesa: Postgres é um padrão aberto, então uma base Supabase se exporta e migra com muito menos atrito que uma base Firestore.

### Sobre custo, e por que isso importa desde já

Os três caminhos têm modelos de cobrança bem diferentes, e vale entender isso antes de escolher, não depois que a fatura chegar:

- **API própria (Express+MySQL):** você paga o servidor (VM, container, PaaS) e o banco, direto, independente de quantas requisições ou quanto tráfego passa. Previsível, mas você também é responsável por escalar, fazer backup e manter tudo no ar.
- **Firebase:** camada gratuita generosa para protótipos, mas cobra por leituras/escritas no Firestore e por armazenamento e tráfego de saída (egress) — em produtos com alto volume de leitura (uma lista que recarrega toda hora, por exemplo), o custo pode crescer rápido e de forma menos previsível.
- **Supabase:** também tem camada gratuita (com o projeto "pausando" após um tempo sem uso no plano free), e cobra por armazenamento de banco, egress e por hora de computação do banco nos planos pagos. Como é Postgres puro por baixo, migrar para um Postgres autogerenciado depois (se o custo justificar) é factível sem reescrever o modelo de dados.

**"Custo de saída" (egress)** é o valor cobrado por dados que **saem** do provedor em direção ao seu usuário — toda resposta de `select`, toda imagem baixada do Storage, conta. É um item fácil de esquecer ao estimar custo de um app com uso intenso de leitura, como uma lista de eventos que recarrega a cada navegação.

> **📌 Vale gravar**
> Os três modelos resolvem "onde guardar e servir dados", mas com contratos de responsabilidade diferentes: API própria = você administra tudo, custo previsível, controle total. Firebase = NoSQL gerenciado, ótimo para tempo real e mobile, lock-in alto. Supabase = Postgres gerenciado, SQL relacional, lock-in menor por ser padrão aberto.

## 2. Criando o projeto no Supabase

1. Em [supabase.com](https://supabase.com), **New project**. Escolha organização, nome (`unieventos`), senha do banco (guarde — é a senha do Postgres, usada em conexões diretas) e região (mais próxima do Brasil, ex. São Paulo/`sa-east-1` se disponível).
2. Aguarde o provisionamento (1–2 minutos).
3. No painel do projeto, vá em **Project Settings → API**. Anote:
   - **Project URL** — algo como `https://xxxxxxxxxxxx.supabase.co`.
   - **anon / public key** — chave longa, começando com `eyJ...` (é um JWT também). Pode ir no front.
   - **service_role key** — outra chave longa. **Nunca vai para o front.**

> **⚠️ Atenção**
> A chave `anon` é pública por design — ela vai no bundle JavaScript do seu front, qualquer pessoa que abrir o DevTools consegue vê-la. Isso é esperado e seguro **desde que o Row Level Security esteja configurado corretamente** (seção 4): a chave `anon` só consegue fazer o que as policies permitirem. Já a `service_role` **ignora RLS completamente** — com ela, qualquer requisição lê e escreve qualquer linha de qualquer tabela, sem checagem nenhuma. Se ela vazar no front, é o mesmo que vazar acesso total ao banco. Use `service_role` só em ambiente de servidor (scripts administrativos, back-end próprio), nunca em código que roda no navegador.

### SQL Editor e Table Editor

No menu lateral: **SQL Editor** (para rodar comandos SQL diretamente, o que faremos agora) e **Table Editor** (interface visual tipo planilha, útil para inspecionar dados rapidamente — mas hoje vamos criar tudo por SQL, para reforçar o que você já sabe da Aula 09).

## 3. Criando as tabelas

No **SQL Editor**, uma nova query:

```sql
-- Tabela de eventos. uuid como PK (padrão do Supabase/Postgres,
-- gerado automaticamente, sem depender de auto-incremento sequencial).
create table eventos (
  id uuid primary key default gen_random_uuid(),
  titulo text not null,
  descricao text not null,
  categoria text not null check (categoria in ('palestra', 'minicurso', 'workshop')),
  data_hora timestamptz not null,
  local text not null,
  vagas integer not null check (vagas > 0),
  imagem_url text,
  usuario_id uuid not null references auth.users(id),
  criado_em timestamptz not null default now()
);

-- Tabela de inscrições, referenciando eventos e o usuário autenticado.
create table inscricoes (
  id uuid primary key default gen_random_uuid(),
  evento_id uuid not null references eventos(id) on delete cascade,
  usuario_id uuid not null references auth.users(id),
  criado_em timestamptz not null default now(),
  unique (evento_id, usuario_id) -- um usuário não se inscreve duas vezes no mesmo evento
);
```

> **🔎 Por baixo do capô**
> `timestamptz` (timestamp with time zone) guarda o instante em UTC internamente e converte na leitura/escrita conforme o fuso da sessão — é o tipo certo para datas que cruzam fusos horários, diferente de um `timestamp` sem fuso, que é ambíguo. `auth.users` é uma tabela que o próprio Supabase Auth já cria e mantém — é para lá que `signUp`/`signInWithPassword` gravam. `references auth.users(id)` garante, no nível do banco, que todo evento pertence a um usuário real.

Rode o SQL (botão **Run** ou `Ctrl+Enter`). Confirme no **Table Editor** que as duas tabelas apareceram.

## 4. Row Level Security: a armadilha nº1

Toda tabela criada pelo **SQL Editor** (o caminho que usamos na §3) nasce **sem RLS habilitado** — o que na prática significa "qualquer um com a chave `anon` lê e escreve tudo", porque o Postgres do Supabase é acessado via API REST autogerada por cima do banco. Isso é perigoso, então o primeiro passo depois de criar uma tabela de verdade é:

```sql
alter table eventos enable row level security;
alter table inscricoes enable row level security;
```

Rode isso agora e tente buscar eventos do front (ou do próprio SQL Editor simulando a role `anon`) — o retorno vai ser uma lista vazia, **sem nenhum erro**:

```json
{ "data": [], "error": null }
```

> **⚠️ Atenção — a armadilha nº1 do Supabase**
> Uma tabela com RLS **habilitado** e **sem nenhuma policy** não gera erro de permissão — ela simplesmente se comporta como se estivesse vazia para quem não é dono/`service_role`. É a causa mais comum de "meu código está certo mas não retorna nada" com Supabase. Sempre que você habilitar RLS numa tabela nova, o próximo passo, sem exceção, é escrever as policies dela.

### O que é RLS e por que existe

Row Level Security é um recurso nativo do Postgres: em vez de controlar acesso só por tabela (você pode ou não fazer `SELECT` em `eventos`), ele controla acesso **linha por linha**, com uma condição SQL avaliada para cada linha. O Supabase se apoia nisso porque expõe o banco diretamente via API para o front — sem RLS, qualquer chave `anon` vazada (e ela É pública) daria acesso irrestrito. RLS é o que torna seguro o front conversar direto com o banco.

> **🧠 Você sabia?**
> A "API REST autogerada" do Supabase não é código deles: é o **PostgREST**, projeto de código aberto criado por Joe Nelson em 2014 que transforma qualquer schema Postgres em uma API HTTP. Cada `supabase.from('eventos').select('*').eq('categoria', 'palestra')` vira, na prática, um `GET /rest/v1/eventos?select=*&categoria=eq.palestra` — e é o PostgREST que repassa o seu JWT ao Postgres para que `auth.uid()` funcione dentro das policies. O RLS, por sua vez, existe no Postgres desde a versão 9.5, lançada em 2016 — bem antes de o Supabase existir.

### Policies: leitura pública, inserção autenticada, edição/exclusão só do dono

```sql
-- LEITURA: qualquer pessoa (mesmo não autenticada) pode ver eventos.
create policy "eventos_leitura_publica"
on eventos for select
using (true);

-- INSERÇÃO: só usuários autenticados podem criar evento, e o evento
-- criado precisa pertencer a quem está criando (não dá para criar
-- em nome de outro usuário).
create policy "eventos_insercao_autenticada"
on eventos for insert
to authenticated
with check (auth.uid() = usuario_id);

-- EDIÇÃO: só o dono do evento pode editar.
create policy "eventos_edicao_dono"
on eventos for update
to authenticated
using (auth.uid() = usuario_id)
with check (auth.uid() = usuario_id);

-- EXCLUSÃO: só o dono pode excluir.
create policy "eventos_exclusao_dono"
on eventos for delete
to authenticated
using (auth.uid() = usuario_id);
```

```sql
-- Inscrições: leitura pública (para mostrar vagas ocupadas),
-- inserção só autenticado e só em nome de si mesmo,
-- exclusão só de si mesmo (cancelar a própria inscrição).
create policy "inscricoes_leitura_publica"
on inscricoes for select
using (true);

create policy "inscricoes_insercao_propria"
on inscricoes for insert
to authenticated
with check (auth.uid() = usuario_id);

create policy "inscricoes_exclusao_propria"
on inscricoes for delete
to authenticated
using (auth.uid() = usuario_id);
```

### `USING` × `WITH CHECK`

As duas cláusulas parecem sinônimos, mas checam momentos diferentes:

- **`USING`** filtra quais linhas **existentes** a operação pode enxergar/afetar. Vale para `SELECT`, `UPDATE` e `DELETE` — é a condição "essa linha, que já está no banco, pode ser vista/alterada/apagada por você?".
- **`WITH CHECK`** valida os dados da linha **depois** da operação (ou os dados que vão ser inseridos). Vale para `INSERT` e `UPDATE` — é a condição "o resultado desta escrita é permitido?".

Em um `UPDATE`, as duas coexistem e respondem perguntas diferentes: `USING` decide se você pode tocar naquela linha específica (ex.: só se `usuario_id` já era seu); `WITH CHECK` decide se o **novo** valor que você está tentando gravar é aceitável (ex.: impedir que você mude `usuario_id` da linha para outra pessoa, "roubando" o evento).

> **📌 Vale gravar**
> `USING` = filtro sobre a linha que já existe (quem pode ver/mexer). `WITH CHECK` = validação sobre o dado que está sendo escrito (o resultado é permitido?). `INSERT` só tem `WITH CHECK` (não existe linha "antes"). `SELECT`/`DELETE` só têm `USING`. `UPDATE` tem os dois.

## 🧩 Padrão de projeto em uso — Adapter

O padrão **Adapter** (estrutural) permite que duas interfaces incompatíveis trabalhem juntas, criando uma camada intermediária que traduz uma para a outra. É exatamente o que vamos construir na seção 8: duas implementações de `eventosRepo` — uma fala com a API Express (Aula 11), outra fala direto com o Supabase — mas **as duas expõem a mesma interface** (`listar()`, `buscarPorId()`, `criar()`, `atualizar()`, `remover()`). O resto do front (store, telas) não sabe, e não precisa saber, qual das duas está em uso. Trocar de fornecedor de dados vira uma linha de variável de ambiente, não uma reescrita de tela.

## 5. `@supabase/supabase-js`: cliente e operações básicas

```bash
npm install @supabase/supabase-js@2.112.3
```

```js
// src/services/supabase.js
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

```bash
# .env
VITE_SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
```

### `select`, filtros, ordenação e paginação

```js
// consultas de exemplo — cole no console do navegador ou num componente de teste

// Selecionar colunas específicas
const { data, error } = await supabase
  .from('eventos')
  .select('id, titulo, categoria, data_hora, vagas')

// Filtros: eq, neq, gt, lt, like, ilike, in
const { data: palestras } = await supabase
  .from('eventos')
  .select('*')
  .eq('categoria', 'palestra')

const { data: buscaPorTitulo } = await supabase
  .from('eventos')
  .select('*')
  .ilike('titulo', '%semana%') // ilike = LIKE case-insensitive

const { data: futuros } = await supabase
  .from('eventos')
  .select('*')
  .gt('data_hora', new Date().toISOString())

const { data: algumasCategorias } = await supabase
  .from('eventos')
  .select('*')
  .in('categoria', ['palestra', 'workshop'])

// Ordenação
const { data: ordenados } = await supabase
  .from('eventos')
  .select('*')
  .order('data_hora', { ascending: true })

// Paginação: range(inicio, fim), ambos inclusive, base 0
const pagina = 1
const porPagina = 10
const inicio = (pagina - 1) * porPagina
const fim = inicio + porPagina - 1

const { data: pagina1, count } = await supabase
  .from('eventos')
  .select('*', { count: 'exact' }) // pede o total de linhas junto
  .order('data_hora', { ascending: true })
  .range(inicio, fim)

// Buscar um único registro (lança erro se vier mais de uma linha
// ou se nenhuma linha for encontrada)
const { data: evento, error: erroUnico } = await supabase
  .from('eventos')
  .select('*')
  .eq('id', 'algum-uuid-aqui')
  .single()
```

> **⚠️ Atenção**
> `single()` **estoura em erro** se a consulta não retornar exatamente uma linha — nem zero, nem duas ou mais. Se o `id` pode não existir (ex.: usuário editou a URL na mão), trate o `error` em vez de assumir que `data` sempre vem preenchido. Para o caso "pode não existir, e tudo bem", use `.maybeSingle()` no lugar de `.single()` — ele devolve `data: null` sem erro quando não encontra.

> **🔬 Investigue**
> Rode a consulta paginada acima (com `count: 'exact'`) com a aba Network aberta e filtre por `rest/v1`. Abra a requisição: repare na URL (`/rest/v1/eventos?select=*&order=data_hora.asc`), nos cabeçalhos `apikey` (a chave `anon`) e `Authorization: Bearer ...` (a mesma chave `anon` quando você está deslogado; o token de sessão do usuário quando está logado), no cabeçalho de requisição `Range: 0-9` e no de resposta `Content-Range: 0-9/34`. Agora peça `.range(500, 509)` numa tabela com poucas linhas e anote o status e o `Content-Range` que voltam — eles explicam por que uma página "além do fim" merece tratamento na sua store.

### `{ data, error }`: por que `try/catch` sozinho não basta

O `supabase-js` **não lança exceção** para a maioria dos erros de banco (violação de policy, coluna inexistente, `check constraint` falhando). Em vez disso, ele sempre resolve a Promise com sucesso e devolve um objeto `{ data, error }` — se `error` não for `null`, a operação falhou, mas nenhuma exceção foi lançada e um `try/catch` ao redor não pega nada:

```js
// ERRADO — o try/catch aqui nunca vê o erro de RLS/validação
try {
  const { data } = await supabase.from('eventos').insert({ titulo: 'X' })
  console.log('Criado:', data) // data pode ser null e o código nem percebe
} catch (e) {
  console.error('Nunca chega aqui para erros de policy/validação')
}

// CORRETO — sempre desestruture e cheque error explicitamente
const { data, error } = await supabase.from('eventos').insert({ titulo: 'X' })
if (error) {
  console.error('Falha ao criar evento:', error.message)
  // trate aqui: mostrar mensagem, não seguir o fluxo, etc.
} else {
  console.log('Criado:', data)
}
```

> **🔎 Por baixo do capô**
> Isso é uma escolha de design da biblioteca: erros de banco de dados (RLS negou, constraint violada, coluna não existe) são tratados como **resultado esperado da operação**, não como falha excepcional do programa — parecido com como uma função de parsing pode devolver `null` em vez de lançar. `try/catch` continua útil para erros de rede (sem internet, timeout), mas a lógica de negócio do Supabase sempre passa pelo `error` do objeto retornado. Esqueça isso e você vai debugar "por que meu insert não fez nada" sem nunca ver a mensagem real.

### `insert`, `update`, `delete`

```js
// INSERT — .select() no final devolve a linha criada (senão, data vem null)
const { data: novoEvento, error: erroInsert } = await supabase
  .from('eventos')
  .insert({
    titulo: 'Minicurso de Docker',
    descricao: 'Introdução prática a containers',
    categoria: 'minicurso',
    data_hora: '2030-12-10T14:00:00-04:00',
    local: 'Laboratório 3',
    vagas: 30,
    usuario_id: (await supabase.auth.getUser()).data.user.id,
  })
  .select()
  .single()

// UPDATE — sempre com .eq() para não atualizar a tabela inteira
const { data: eventoAtualizado, error: erroUpdate } = await supabase
  .from('eventos')
  .update({ vagas: 40 })
  .eq('id', novoEvento.id)
  .select()
  .single()

// DELETE
const { error: erroDelete } = await supabase
  .from('eventos')
  .delete()
  .eq('id', novoEvento.id)
```

> **⚠️ Atenção**
> Um `update()` ou `delete()` **sem `.eq(...)`** (ou outro filtro) tenta afetar a tabela inteira. O RLS te protege de estragos globais (a policy `usuario_id = auth.uid()` limita às suas próprias linhas), mas mesmo dentro das suas linhas isso é raramente o que você quer. Sempre filtre pelo identificador específico.

### Joins por relacionamento

O Supabase entende as `foreign keys` que você declarou e permite buscar dados relacionados dentro do mesmo `select`, sem escrever `JOIN` manualmente:

```js
// Buscar eventos já trazendo as inscrições relacionadas
const { data: eventosComInscritos, error } = await supabase
  .from('eventos')
  .select('*, inscricoes(*)')

// eventosComInscritos[0].inscricoes é um array com as inscrições daquele evento

// Contagem de relacionados sem trazer todas as linhas
const { data: eventosComContagem } = await supabase
  .from('eventos')
  .select('*, inscricoes(count)')
```

## 6. Supabase Auth

```js
// src/services/supabaseAuthService.js
import { supabase } from './supabase'

export async function cadastrar(email, senha) {
  const { data, error } = await supabase.auth.signUp({ email, password: senha })
  if (error) throw new Error(error.message)
  return data.user
}

export async function entrar(email, senha) {
  const { data, error } = await supabase.auth.signInWithPassword({ email, password: senha })
  if (error) throw new Error(error.message)
  return data.user
}

export async function sair() {
  const { error } = await supabase.auth.signOut()
  if (error) throw new Error(error.message)
}

export async function obterSessaoAtual() {
  const { data } = await supabase.auth.getSession()
  return data.session
}

// Observa login/logout/renovação de token, igual ao onAuthStateChanged
// do Firebase que vimos na Aula 10.
export function observarAutenticacao(callback) {
  const { data: assinatura } = supabase.auth.onAuthStateChange((_evento, sessao) => {
    callback(sessao)
  })
  // devolvemos uma função que chama o método NO objeto — passar
  // `assinatura.subscription.unsubscribe` solto perderia o `this`
  return () => assinatura.subscription.unsubscribe()
}
```

A ligação entre Auth e RLS é direta: quando o front faz uma chamada autenticada, o `supabase-js` anexa automaticamente o token de sessão, e as policies usam `auth.uid()` para saber quem está pedindo. É o mesmo princípio do middleware `autenticar` da Aula 10 (ler o token, extrair a identidade) — só que aqui a checagem acontece **dentro do banco**, não numa camada de middleware que você escreve.

A store de autenticação segue exatamente a mesma forma da Aula 10 — Pinia, estado `usuario`/`carregando`/`inicializado`, Promise resolvida no primeiro evento do observador, guard de rota aguardando essa Promise. Só troca o serviço por baixo: `observarAutenticacao` do Supabase no lugar de `onAuthStateChanged` do Firebase.

```js
// src/stores/authStoreSupabase.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { obterSessaoAtual, observarAutenticacao } from '@/services/supabaseAuthService'

export const useAuthStore = defineStore('auth', () => {
  const usuario = ref(null)
  const carregando = ref(false)
  const inicializado = ref(false)

  let promessaInicializacao = null

  function inicializar() {
    if (promessaInicializacao) return promessaInicializacao

    promessaInicializacao = new Promise((resolve) => {
      // Primeiro, lê a sessão já persistida (ex.: recarregou a página).
      obterSessaoAtual().then((sessao) => {
        usuario.value = sessao?.user ?? null
      })

      // Depois, mantém o estado sincronizado com login/logout/renovação.
      observarAutenticacao((sessao) => {
        usuario.value = sessao?.user ?? null
        if (!inicializado.value) {
          inicializado.value = true
          resolve()
        }
      })
    })

    return promessaInicializacao
  }

  const estaLogado = computed(() => usuario.value !== null)

  return { usuario, carregando, inicializado, inicializar, estaLogado }
})
```

```js
// src/router/index.js — guard idêntico em espírito ao da Aula 10,
// trocando authStore de Firebase pela variante Supabase.
router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  await authStore.inicializar()

  if (to.meta.requerAuth && !authStore.estaLogado) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  return true
})
```

> **💡 Dica**
> Repare que a *forma* do problema — "aguardar a primeira resolução do observador antes de deixar o guard decidir" — é idêntica entre Firebase e Supabase, mesmo os dois SDKs sendo de fornecedores diferentes. É um sinal de que o problema (evitar redirecionamento indevido no F5) é estrutural do padrão "autenticação assíncrona no cliente", não uma peculiaridade de um SDK específico.

## 7. Storage e Realtime

### Storage: bucket público, upload, URL pública

No painel: **Storage → New bucket**, nome `eventos-imagens`, marque **Public bucket**.

```js
// src/services/supabaseStorageService.js
import { supabase } from './supabase'

export async function enviarImagemEvento(arquivo) {
  const nomeUnico = `${Date.now()}-${arquivo.name}`

  const { error } = await supabase.storage
    .from('eventos-imagens')
    .upload(nomeUnico, arquivo)

  if (error) throw new Error('Falha ao enviar imagem: ' + error.message)

  const { data } = supabase.storage
    .from('eventos-imagens')
    .getPublicUrl(nomeUnico)

  return data.publicUrl
}
```

### Realtime: a lista se atualizando sozinha

**Antes do código, um passo no painel:** o Realtime só emite eventos de tabelas incluídas na publicação de replicação lógica, e nenhuma tabela entra nela por padrão. Vá em **Database → Replication**, abra a publicação `supabase_realtime` e marque a tabela `eventos`. Sem isso, o `subscribe()` conecta, não dá erro nenhum, e simplesmente nada acontece — é o motivo nº 1 de "meu Realtime não funciona".

```js
// trecho de EventosListaView.vue (variante Supabase)
import { onMounted, onUnmounted } from 'vue'
import { supabase } from '@/services/supabase'

let canal = null

onMounted(() => {
  canal = supabase
    .channel('eventos-mudancas')
    .on(
      'postgres_changes',
      { event: '*', schema: 'public', table: 'eventos' },
      (payload) => {
        console.log('Mudança recebida:', payload.eventType, payload.new ?? payload.old)
        eventosStore.carregar() // recarrega a lista quando algo muda
      },
    )
    .subscribe()
})

onUnmounted(() => {
  if (canal) supabase.removeChannel(canal)
})
```

Abra o UniEventos em duas abas lado a lado. Crie um evento em uma; a lista da outra atualiza sozinha, sem F5. É o tipo de momento que mais impressiona quando demonstrado ao vivo — vale ver isso funcionando antes de explicar o código.

> **🔎 Por baixo do capô**
> Realtime do Supabase se apoia na replicação lógica do Postgres (`logical replication`): o banco publica um fluxo de mudanças (`postgres_changes`), e o `supabase-js` mantém um WebSocket assinando esse fluxo filtrado pela tabela/evento que você configurou. Não é polling — é o próprio banco avisando o cliente quando algo muda.

## 💻 Mão na massa — CRUD direto com Supabase e, depois, o Adapter

### Passo 1 — Testando a conexão no console do navegador

Antes de montar telas, confirme que o cliente conecta e que as policies estão certas. Com `unieventos-web` rodando (`npm run dev`), abra o DevTools no navegador, importe o cliente e rode uma consulta:

```js
// cole no console do navegador, na página do seu app rodando com Vite
const { supabase } = await import('/src/services/supabase.js')

const { data, error } = await supabase.from('eventos').select('*')
console.log({ data, error })
```

Se `data` vier `[]` e `error` vier `null`, e você já cadastrou alguma linha pelo Table Editor, é a armadilha da seção 4: falta a policy de leitura. Se `error` trouxer uma mensagem sobre coluna ou relação inexistente, revise o SQL de criação da tabela.

### Passo 2 — Tela de listagem consumindo o Supabase diretamente

Antes de introduzir o Adapter, vale montar a versão mais direta — a store chamando o `supabase-js` sem nenhuma camada de repositório no meio. É o ponto de partida mais simples, e o que a maioria dos tutoriais mostra.

```js
// src/stores/eventosStoreSupabase.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { supabase } from '@/services/supabase'

export const useEventosStore = defineStore('eventos', () => {
  const lista = ref([])
  const itemAtual = ref(null)
  const carregando = ref(false)
  const erro = ref(null)
  const paginacao = ref({ pagina: 1, porPagina: 10, total: 0, totalPaginas: 0 })

  async function carregar({ pagina = 1, porPagina = 10 } = {}) {
    carregando.value = true
    erro.value = null

    const inicio = (pagina - 1) * porPagina
    const fim = inicio + porPagina - 1

    const { data, error, count } = await supabase
      .from('eventos')
      .select('*', { count: 'exact' })
      .order('data_hora', { ascending: true })
      .range(inicio, fim)

    if (error) {
      erro.value = error.message
    } else {
      lista.value = data
      paginacao.value = { pagina, porPagina, total: count, totalPaginas: Math.ceil(count / porPagina) }
    }

    carregando.value = false
  }

  async function carregarUm(id) {
    carregando.value = true
    erro.value = null

    const { data, error } = await supabase.from('eventos').select('*').eq('id', id).maybeSingle()

    if (error) {
      erro.value = error.message
    } else if (!data) {
      erro.value = 'Evento não encontrado.'
    } else {
      itemAtual.value = data
    }

    carregando.value = false
  }

  async function criar(evento) {
    carregando.value = true
    erro.value = null

    const { data: sessao } = await supabase.auth.getUser()
    const { data, error } = await supabase
      .from('eventos')
      .insert({ ...evento, usuario_id: sessao.user.id })
      .select()
      .single()

    carregando.value = false
    if (error) {
      erro.value = error.message
      throw new Error(error.message)
    }

    lista.value = [data, ...lista.value]
    return data
  }

  async function atualizar(id, evento) {
    carregando.value = true
    erro.value = null

    const { data, error } = await supabase.from('eventos').update(evento).eq('id', id).select().single()

    carregando.value = false
    if (error) {
      erro.value = error.message
      throw new Error(error.message)
    }

    const indice = lista.value.findIndex((e) => e.id === id)
    if (indice !== -1) lista.value[indice] = data
    return data
  }

  async function remover(id) {
    carregando.value = true
    erro.value = null

    const { error } = await supabase.from('eventos').delete().eq('id', id)

    carregando.value = false
    if (error) {
      erro.value = error.message
      throw new Error(error.message)
    }

    lista.value = lista.value.filter((e) => e.id !== id)
  }

  return { lista, itemAtual, carregando, erro, paginacao, carregar, carregarUm, criar, atualizar, remover }
})
```

```vue
<!-- src/views/EventosListaSupabaseView.vue -->
<script setup>
import { onMounted } from 'vue'
import { useEventosStore } from '@/stores/eventosStoreSupabase'
import { useAuthStore } from '@/stores/authStoreSupabase'

const eventosStore = useEventosStore()
const authStore = useAuthStore()

onMounted(() => eventosStore.carregar())

function formatarData(isoString) {
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(isoString))
}
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-4">Eventos (Supabase)</h1>

    <v-progress-linear v-if="eventosStore.carregando" indeterminate color="primary" class="mb-2" />
    <v-alert v-if="eventosStore.erro" type="error" class="mb-4">{{ eventosStore.erro }}</v-alert>

    <v-row>
      <v-col v-for="evento in eventosStore.lista" :key="evento.id" cols="12" sm="6" md="4">
        <v-card>
          <v-img v-if="evento.imagem_url" :src="evento.imagem_url" height="140" cover />
          <v-card-title>{{ evento.titulo }}</v-card-title>
          <v-card-subtitle>{{ formatarData(evento.data_hora) }} · {{ evento.local }}</v-card-subtitle>
          <v-card-text>{{ evento.descricao }}</v-card-text>
          <v-card-actions v-if="authStore.usuario?.id === evento.usuario_id">
            <v-btn variant="text" :to="`/eventos-supabase/${evento.id}/editar`">Editar</v-btn>
            <v-btn variant="text" color="error" @click="eventosStore.remover(evento.id)">Excluir</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <p v-if="!eventosStore.carregando && eventosStore.lista.length === 0">Nenhum evento cadastrado ainda.</p>
  </v-container>
</template>
```

> **⚠️ Atenção**
> `authStore.usuario?.id === evento.usuario_id` no template controla só a **exibição** do botão — é UX, igual ao guard de rota da Aula 10. A garantia de verdade é a policy `eventos_edicao_dono` (seção 4): mesmo que alguém forje uma requisição de `update` para um evento alheio direto contra a API do Supabase, o banco recusa porque `auth.uid()` não bate com `usuario_id`.

### Do CRUD direto ao Adapter

Com o CRUD direto funcionando, damos o passo seguinte: extrair uma interface comum que permita alternar entre a API Express (Aula 11) e o Supabase sem tocar em store nem em tela.

Repare numa diferença que a tela do Passo 2 deixou passar de propósito: falando **direto** com o Supabase, o front recebe as colunas cruas do Postgres (`evento.data_hora`, `evento.imagem_url`) e o template se adaptou a elas. Do lado da API Express, o mesmo evento chega em camelCase (`dataHora`, `imagemUrl`), porque o repositório do back-end traduz. Duas implementações da "mesma" interface devolvendo nomes de campo diferentes não é um Adapter — é um vazamento. No Passo 4, a conversão passa a ser responsabilidade explícita do adaptador Supabase, e a tela volta a falar um vocabulário só.

### Passo 3 — Interface comum e implementação para a API Express

```js
// src/repositories/eventosRepoExpress.js
import http from '@/services/http'

export const eventosRepoExpress = {
  async listar({ pagina = 1, porPagina = 10 } = {}) {
    const resposta = await http.get('/eventos', { params: { pagina, porPagina } })
    return resposta.data // { dados, paginacao }
  },

  async buscarPorId(id) {
    const resposta = await http.get(`/eventos/${id}`)
    return resposta.data
  },

  async criar(evento) {
    const resposta = await http.post('/eventos', evento)
    return resposta.data
  },

  async atualizar(id, evento) {
    const resposta = await http.put(`/eventos/${id}`, evento)
    return resposta.data
  },

  async remover(id) {
    await http.delete(`/eventos/${id}`)
  },
}
```

### Passo 4 — Mesma interface, implementação Supabase

```js
// src/repositories/eventosRepoSupabase.js
import { supabase } from '@/services/supabase'

// mesma tradução snake_case → camelCase que o repositório MySQL faz na Aula 11
function linhaParaEvento(linha) {
  if (!linha) return null
  return {
    id: linha.id,
    titulo: linha.titulo,
    descricao: linha.descricao,
    categoria: linha.categoria,
    dataHora: linha.data_hora,
    local: linha.local,
    vagas: linha.vagas,
    imagemUrl: linha.imagem_url,
    usuarioId: linha.usuario_id,
  }
}

// e o caminho inverso, para insert/update
function eventoParaLinha(evento) {
  return {
    titulo: evento.titulo,
    descricao: evento.descricao,
    categoria: evento.categoria,
    data_hora: evento.dataHora,
    local: evento.local,
    vagas: evento.vagas,
    imagem_url: evento.imagemUrl || null,
  }
}

export const eventosRepoSupabase = {
  async listar({ pagina = 1, porPagina = 10 } = {}) {
    const inicio = (pagina - 1) * porPagina
    const fim = inicio + porPagina - 1

    const { data, error, count } = await supabase
      .from('eventos')
      .select('*', { count: 'exact' })
      .order('data_hora', { ascending: true })
      .range(inicio, fim)

    if (error) throw new Error(error.message)

    // Formato devolvido igual ao da API Express — é isso que faz o
    // Adapter funcionar: a FORMA da resposta precisa ser a mesma.
    // Inclusive o NOME DOS CAMPOS: as colunas do Postgres são snake_case
    // (data_hora, imagem_url), mas o contrato do front é camelCase desde a
    // Aula 06. Do lado Express quem traduz é o repositório do back-end; aqui,
    // como não existe back-end nosso no meio, a tradução é obrigação do Adapter.
    return {
      dados: data.map(linhaParaEvento),
      paginacao: { pagina, porPagina, total: count, totalPaginas: Math.ceil(count / porPagina) },
    }
  },

  async buscarPorId(id) {
    const { data, error } = await supabase.from('eventos').select('*').eq('id', id).single()
    if (error) throw new Error(error.message)
    return linhaParaEvento(data)
  },

  async criar(evento) {
    const { data: sessao } = await supabase.auth.getUser()
    const { data, error } = await supabase
      .from('eventos')
      .insert({ ...eventoParaLinha(evento), usuario_id: sessao.user.id })
      .select()
      .single()
    if (error) throw new Error(error.message)
    return linhaParaEvento(data)
  },

  async atualizar(id, evento) {
    const { data, error } = await supabase
      .from('eventos')
      .update(eventoParaLinha(evento))
      .eq('id', id)
      .select()
      .single()
    if (error) throw new Error(error.message)
    return linhaParaEvento(data)
  },

  async remover(id) {
    const { error } = await supabase.from('eventos').delete().eq('id', id)
    if (error) throw new Error(error.message)
  },
}
```

### Passo 5 — Trocando a implementação por variável de ambiente

```js
// src/repositories/eventosRepo.js
import { eventosRepoExpress } from './eventosRepoExpress'
import { eventosRepoSupabase } from './eventosRepoSupabase'

// VITE_BACKEND=express ou VITE_BACKEND=supabase no .env
const backendEscolhido = import.meta.env.VITE_BACKEND ?? 'express'

export const eventosRepo = backendEscolhido === 'supabase' ? eventosRepoSupabase : eventosRepoExpress
```

```js
// src/services/eventosService.js — reescrito para usar o Adapter
import { eventosRepo } from '@/repositories/eventosRepo'

export function listarEventos(params) {
  return eventosRepo.listar(params)
}

export function buscarEvento(id) {
  return eventosRepo.buscarPorId(id)
}

export function criarEvento(evento) {
  return eventosRepo.criar(evento)
}

export function atualizarEvento(id, evento) {
  return eventosRepo.atualizar(id, evento)
}

export function removerEvento(id) {
  return eventosRepo.remover(id)
}
```

```bash
# .env — uma linha decide qual back-end o front usa
VITE_BACKEND=supabase
```

Nenhuma linha da store (`eventosStore.js`) ou das telas (`EventosListaView.vue`, `EventoFormView.vue`) precisa mudar. Isso é o Adapter cumprindo sua função: a store continua chamando `eventosService.listarEventos(...)`, que continua chamando `eventosRepo.listar(...)` — só a implementação por trás mudou, escolhida por uma variável de ambiente.

> **📌 Vale gravar**
> Facade (Aula 11) simplifica uma interface complexa. Adapter (esta aula) traduz uma interface para outra, permitindo trocar a implementação sem o cliente perceber. A camada `services/` do UniEventos usa os dois: é Facade em relação às telas (esconde detalhes de HTTP/Supabase) e se apoia num Adapter (`eventosRepo`) para trocar de fornecedor por baixo.

### Como testar

O teste do Adapter é o mesmo roteiro executado **duas vezes**, com uma linha de `.env` de diferença. Faça assim:

1. Com `VITE_BACKEND=express` no `.env` (e a `unieventos-api` + MySQL rodando), abra o UniEventos: liste, crie, edite e exclua um evento. Anote o que aparece na aba Network: requisições para `http://localhost:3000/api/eventos`.
2. Pare o `npm run dev`, troque para `VITE_BACKEND=supabase`, suba de novo e **repita exatamente os mesmos quatro passos**. Agora as requisições saem para `https://<seu-projeto>.supabase.co/rest/v1/eventos`.

Resultado esperado: as duas rodadas se comportam igual na tela — mesma lista, mesmo formulário preenchido na edição, mesma data formatada (sinal de que a tradução `data_hora` → `dataHora` do Passo 4 está funcionando), mesmo comportamento do botão de excluir. Nenhum arquivo dentro de `stores/` ou `views/` foi tocado entre uma rodada e outra: confirme com `git status`.

Dois testes negativos fecham a verificação:

3. **RLS de verdade** — deslogado, tente criar um evento pelo console do navegador: `await supabase.from('eventos').insert({ titulo: 'teste' })`. Resultado esperado: `error` de violação de policy, `data: null` — a tela nem precisa impedir, o banco impede.
4. **Realtime** — com a replicação habilitada, abra o UniEventos em duas abas e crie um evento numa delas. Resultado esperado: a lista da outra aba se atualiza sozinha, sem F5.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** A tabela `eventos` está com RLS habilitado e tem **só** a policy `eventos_leitura_publica`. Um usuário autenticado roda `supabase.from('eventos').insert({ ... }).select()`. Preveja o que vem em `{ data, error }` — e compare com o que vem num `select` quando não existe policy nenhuma. Por que os dois casos se comportam de forma diferente?

Resultado esperado: o `insert` devolve `data: null` e um `error` de violação de policy (código `42501`), porque não existe policy de `insert`; o `select` sem policy nenhuma devolve `data: []` e `error: null` — silêncio, não erro. RLS nega por padrão, e negar uma leitura é simplesmente não devolver linhas.

**A2.** Complete as lacunas da policy que permite a um usuário alterar **apenas as próprias** inscrições, sem poder transferi-las para outra pessoa. Depois diga qual das duas cláusulas impede o "roubo" de uma inscrição.

```sql
create policy "inscricoes_edicao_propria"
on inscricoes for update
to authenticated
using (________________)
with check (________________);
```

Resultado esperado: `using (auth.uid() = usuario_id)` e `with check (auth.uid() = usuario_id)`. É o `with check` que impede o roubo: ele valida a linha **depois** da alteração, barrando um `update` que tente trocar o `usuario_id` para outra pessoa.

**A3.** Verdadeiro ou falso, com justificativa: "Um `try/catch` ao redor de `await supabase.from('eventos').delete().eq('id', id)` captura a violação de policy quando o usuário tenta apagar um evento alheio."

Resultado esperado: falso — o `supabase-js` não lança exceção nesses casos; ele resolve a Promise com `{ data, error }`. Um `delete` que não casa com a policy nem chega a ser erro: afeta zero linhas e volta `error: null`. Só olhando o retorno (e o `count`) é que você descobre o que aconteceu.

**A4.** Uma tabela tem 15 eventos. Preveja `data.length` e `count` para `.select('*', { count: 'exact' }).range(10, 19)`. E para `.range(0, 4)`? Que combinação de `pagina`/`porPagina` da store produz cada chamada?

Resultado esperado: `.range(10, 19)` devolve `data.length === 5` (só existem 15 linhas) e `count === 15` — `count` é sempre o total da consulta, não o da fatia; corresponde a `pagina: 2, porPagina: 10`. `.range(0, 4)` devolve `data.length === 5` e `count === 15`, correspondendo a `pagina: 1, porPagina: 5`.

**A5.** Em duas linhas: a chave `anon` vai para o bundle público do front e isso é seguro por design; a `service_role` não pode ir. O que exatamente cada uma "respeita" ou "ignora" dentro do Postgres?

Resultado esperado: a `anon` entra como o papel `anon`/`authenticated` e **respeita** todas as policies de RLS — por isso pode ser pública. A `service_role` **ignora** o RLS por completo (é `BYPASSRLS`): com ela, qualquer pessoa lê e escreve qualquer linha de qualquer tabela. Ela só existe para código de servidor.

**A6.** `carregarUm(id)` da store usa `.maybeSingle()`; `buscarPorId` do `eventosRepoSupabase` usa `.single()`. Para um `id` inexistente, preveja o `{ data, error }` de cada um e diga qual dos dois comportamentos o `eventosRepoExpress` (que devolve `404`) espelha melhor.

Resultado esperado: `.maybeSingle()` devolve `data: null, error: null`; `.single()` devolve `data: null` e um `error` (`PGRST116` — 0 linhas onde se esperava exatamente 1). O `.single()` espelha melhor o Express, porque também transforma "não encontrei" em erro, que é o que a store precisa para exibir "Evento não encontrado".

### Nível B — Aplicação

**B1.** Projeto e tabelas. Crie seu projeto no Supabase e as tabelas da sua entidade principal (autoral), com `uuid` como PK, `timestamptz` para datas e RLS habilitado desde o início.

Resultado esperado: as tabelas aparecem no Table Editor e um `select` feito do front devolve `data: []` sem erro — o sinal de que o RLS está ligado e ainda não há policy.

<details markdown="1">
<summary>Dica</summary>

Habilite RLS na mesma migração/script SQL em que cria a tabela — não deixe para depois, é fácil esquecer.
</details>

**B2.** Policies completas. Escreva as quatro policies (leitura pública, inserção autenticada, edição e exclusão só do dono) para sua tabela principal.

Resultado esperado: deslogado, `select` funciona e `insert` devolve `error` de policy; logado como A, editar uma linha de B afeta zero linhas.

<details markdown="1">
<summary>Dica</summary>

Teste cada uma isoladamente: logado como usuário A, tente editar uma linha do usuário B — deve falhar silenciosamente (nenhuma linha afetada), não com erro.
</details>

**B3.** CRUD com `supabase-js`. Implemente `select`, `insert`, `update`, `delete` da sua entidade, sempre desestruturando `{ data, error }` e tratando o erro.

Resultado esperado: cada operação passa por um `if (error)`; um `insert` que viola uma `check constraint` mostra a mensagem real do Postgres na tela, não um `null` silencioso.

<details markdown="1">
<summary>Dica</summary>

Se `data` vier vazio sem erro nenhum, sua primeira suspeita deve ser RLS sem policy — releia a seção 4 antes de procurar bug no seu código.
</details>

**B4.** Realtime funcionando. Assine mudanças na sua tabela principal e demonstre, em duas abas, uma lista atualizando sozinha.

Resultado esperado: criar um registro numa aba faz a lista da outra atualizar em menos de um segundo, sem F5, e sair da tela remove o canal (`removeChannel`).

<details markdown="1">
<summary>Dica</summary>

Confirme que o Realtime está habilitado para a tabela em Database → Replication no painel do Supabase — em alguns planos/tabelas ele vem desligado por padrão.
</details>

### Nível C — Desafio

**C1.** Adapter comparativo. Implemente as duas versões do repositório (`Repo...Express` e `Repo...Supabase`) para sua entidade principal, com a mesma interface, e alterne entre elas por variável de ambiente. Atenção a dois detalhes que costumam quebrar. (1) Os `id` são `INT` no MySQL e `uuid` no Supabase — a store e as rotas precisam funcionar com os dois. (2) A tabela do Supabase tem uma coluna de **dono** (`usuario_id`, exigida pelas policies de RLS) que a tabela MySQL das Aulas 09/11 não tem: decida se o Adapter devolve esse campo só num dos lados (e a tela lida com `undefined`) ou se você acrescenta `criado_por` também no MySQL — e escreva a decisão em uma linha no README.

Resultado esperado: trocar `VITE_BACKEND` no `.env` e reiniciar o `npm run dev` mantém a tela funcionando sem tocar em nenhuma linha de `store` ou `view`, inclusive o formulário de edição.

<details markdown="1">
<summary>Dica</summary>

O ponto de verificação: você deve conseguir trocar `VITE_BACKEND` no `.env`, reiniciar o `npm run dev`, e a tela continuar funcionando sem tocar em nenhuma linha de `store` ou `view`. Se a edição quebrar só num dos back-ends, procure um `Number(id)` que não deveria estar na store.
</details>

## 🏆 Desafios

### ⭐ A tabela que parecia vazia
Tags: supabase, seguranca, bug, investigacao

Um colega criou a tabela de comentários de eventos com o SQL abaixo e reclamou de dois "bugs do Supabase": visitantes deslogados não veem comentário nenhum (a página fica vazia, sem erro), e um usuário conseguiu "roubar" o comentário de outro. Os dois problemas estão nas policies — o Supabase está fazendo exatamente o que foi mandado.

```sql
create table comentarios (
  id uuid primary key default gen_random_uuid(),
  evento_id uuid not null references eventos(id) on delete cascade,
  usuario_id uuid not null references auth.users(id),
  texto text not null check (char_length(texto) between 1 and 500),
  criado_em timestamptz not null default now()
);

alter table comentarios enable row level security;

create policy "comentarios_leitura"
on comentarios for select
to authenticated
using (true);

create policy "comentarios_insercao"
on comentarios for insert
to authenticated
with check (auth.uid() = usuario_id);

create policy "comentarios_edicao"
on comentarios for update
to authenticated
using (auth.uid() = usuario_id);
```

**Critérios de pronto**

- Você reproduz os dois problemas antes de corrigir: um `select` deslogado devolvendo `data: []` e um `update({ usuario_id: '<uuid de outro usuário>' })` bem-sucedido feito pelo dono original.
- As policies corrigidas: leitura pública de verdade e edição que não permite trocar o dono.
- Um teste manual documentado em `docs/policies-comentarios.md`: quatro chamadas (`select` deslogado, `insert` deslogado, `update` do próprio texto, `update` tentando mudar `usuario_id`) com o `{ data, error }` observado em cada uma.
- A policy de `delete` para o dono, que estava faltando.

<details markdown="1">
<summary>Pistas</summary>

1. Releia "USING × WITH CHECK" na seção 4: uma das policies só tem metade do que precisa.
2. `to authenticated` exclui explicitamente o papel `anon` — e qual é o papel de quem nunca fez login?
3. Para testar como outro usuário sem trocar de conta, procure "Testing policies" na documentação de RLS do Supabase: a ideia é trocar o papel (`set role authenticated`) e injetar o `sub` do JWT antes da consulta no SQL Editor.
</details>

### ⭐⭐ O que dá para fazer só com a chave pública
Tags: supabase, seguranca, http, investigacao

Rode `npm run build` e procure `eyJ` dentro de `dist/assets/*.js`: a sua chave `anon` está lá, legível para qualquer pessoa que abrir o site. Isso é esperado — mas o que exatamente alguém consegue fazer com ela e um terminal? Descubra usando só `curl` contra a API REST do seu projeto, sem `supabase-js`, e mostre que a única coisa entre a chave pública e os seus dados são as policies.

**Critérios de pronto**

- Um script `docs/anon-vs-rls.sh` com pelo menos quatro chamadas `curl` a `https://<projeto>.supabase.co/rest/v1/eventos`: `GET` sem token, `POST` sem token, `POST` com o token de sessão de um usuário logado e `DELETE` de um evento de outro usuário com esse mesmo token.
- Cada chamada tem, em comentário, o status HTTP e o corpo observados — e a policy (ou a falta dela) que explica o resultado.
- O token de sessão é obtido pela própria API de auth (`/auth/v1/token?grant_type=password`), não copiado do DevTools.
- Um parágrafo final responde: se você desabilitasse o RLS de `eventos` por um minuto, o que o segundo `curl` passaria a fazer?

<details markdown="1">
<summary>Pistas</summary>

1. A API REST espera dois cabeçalhos: `apikey: <anon>` e `Authorization: Bearer <anon ou token de sessão>`. Sem `Authorization`, a resposta já é reveladora.
2. Para o login por `curl`: `POST /auth/v1/token?grant_type=password` com `Content-Type: application/json` e `{ "email": "...", "password": "..." }` — o `access_token` vem na resposta.
3. Um `DELETE` barrado por policy não devolve erro: devolve `204` e não apaga nada. Confira com um `GET` em seguida — ou peça `Prefer: return=representation` para ver o que foi afetado.
4. Nunca cole a `service_role` nesse script — o objetivo é provar o que a chave **pública** consegue.
</details>

### ⭐⭐ Vagas ao vivo: inscrições com join, contagem e Realtime
Tags: supabase, crud, vue, banco-de-dados

O card de evento mostra `vagas`, mas não quantas já foram ocupadas — e o botão "Inscrever-se" nem existe na versão Supabase. Construa o fluxo completo usando só o que a aula ensinou: contagem de relacionados no `select`, `insert`/`delete` em `inscricoes` respeitando as policies, e Realtime para que "12/40 vagas" mude na tela de todo mundo quando alguém se inscreve.

**Critérios de pronto**

- O card mostra `ocupadas/vagas` vindo de um único `select` com `inscricoes(count)` — sem uma segunda consulta por evento.
- "Inscrever-se" vira "Cancelar inscrição" quando o usuário logado já tem inscrição naquele evento; deslogado, o botão leva ao login.
- Tentar se inscrever duas vezes mostra a mensagem da constraint `unique (evento_id, usuario_id)` traduzida para o usuário, não o texto cru do Postgres.
- Com duas abas abertas, inscrever-se em uma faz o contador da outra mudar sem F5, assinando a tabela `inscricoes` (não `eventos`).
- Um comentário no código explica por que o contador pode, por alguns instantes, estar errado numa aba que perdeu a conexão WebSocket.

<details markdown="1">
<summary>Pistas</summary>

1. `select('*, inscricoes(count)')` devolve `inscricoes: [{ count: 12 }]` — um array com um objeto, não um número.
2. Para saber se "eu" estou inscrito sem uma consulta por card, busque as inscrições do usuário logado uma vez (`.eq('usuario_id', id)`) e guarde os `evento_id` num `Set` na store.
3. O código de violação de `unique` no Postgres é `23505`; `error.code` chega intacto no `supabase-js`.
4. O Realtime precisa estar habilitado para `inscricoes` em Database → Replication; o `.on('postgres_changes', { table: 'inscricoes' }, ...)` pode simplesmente recarregar a lista.
</details>

### ⭐⭐⭐ A última vaga, sem condição de corrida — dentro do banco
Tags: supabase, banco-de-dados, seguranca, api

Na Aula 11, a última vaga foi protegida com uma transação e `FOR UPDATE` dentro do Express. Com Supabase não existe "seu servidor" para colocar essa lógica — e um `select` de contagem seguido de `insert` no front deixa a porta aberta: vinte pessoas clicando ao mesmo tempo num evento com cinco vagas podem gerar vinte inscrições. Resolva onde o Supabase espera que você resolva: numa **função Postgres** chamada por `supabase.rpc()`, que confere e insere de forma atômica.

**Critérios de pronto**

- Existe a função `inscrever(p_evento_id uuid)` no schema `public`, que lê o evento com trava de linha, conta as inscrições, recusa com uma exceção clara quando não há vaga e insere a inscrição para `auth.uid()` — tudo na mesma transação.
- O front chama `supabase.rpc('inscrever', { p_evento_id })` e mostra "Evento lotado" quando `error.message` indicar isso.
- Um script no console dispara 20 chamadas simultâneas com `Promise.all` (com 20 usuários de teste, ou temporariamente sem a `unique`) contra um evento de 5 vagas; o `count` final é 5.
- Um ADR curto (`docs/adr/000X-inscricao-por-rpc.md`, no formato que a Aula 14 apresenta) registra por que a regra foi para o banco e o que se perde com isso (testes unitários em JS, portabilidade).
- A função não pode ser usada para inscrever outra pessoa: `usuario_id` vem de `auth.uid()`, nunca de parâmetro.

<details markdown="1">
<summary>Pistas</summary>

1. Leia "Database Functions" e a parte sobre `security definer` na documentação de RLS do Supabase; decida se a função roda como `security invoker` (respeita RLS) ou `security definer` (ignora RLS e, por isso, precisa checar `auth.uid()` sozinha).
2. O esqueleto é `create or replace function inscrever(p_evento_id uuid) returns uuid language plpgsql as $$ declare ... begin ... end $$;` — dentro, `select vagas into v_vagas from eventos where id = p_evento_id for update;` é a trava.
3. `raise exception 'SEM_VAGAS'` aborta a transação inteira; o texto chega em `error.message` no front.
4. Para o teste de concorrência, `Promise.all(Array.from({ length: 20 }, () => supabase.rpc('inscrever', { p_evento_id })))` no console — e conte com `select count(*) from inscricoes where evento_id = '...'` no SQL Editor.
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `data: []` sem erro nenhum | RLS habilitado, sem policy correspondente à operação | Escrever a policy que falta; conferir se cobre `select`/`insert`/`update`/`delete` conforme necessário |
| Erro "JWT expired" ou 401 genérico | Chave `anon` errada, ou copiada de outro projeto | Reconferir `VITE_SUPABASE_URL` e `VITE_SUPABASE_ANON_KEY` em Project Settings → API |
| `insert`/`update` falha sem mensagem clara na tela | Esqueceu de checar `error` do retorno (usou só `try/catch`) | Sempre desestruturar `{ data, error }` e tratar `error` explicitamente |
| Policy de `update` "não funciona" mesmo parecendo certa | Faltou `with check`, então a policy só filtra a linha original mas aceita qualquer novo valor (ou vice-versa) | Escrever `using` e `with check` juntos em policies de `update` |
| Erro de sintaxe SQL mencionando palavra reservada | Coluna nomeada `order`, `user`, `group` etc. sem aspas | Evitar nomes reservados; se inevitável, usar aspas duplas (`"order"`) em todo lugar |
| `.single()` lança erro "multiple (or no) rows returned" | Consulta não bateu em exatamente uma linha | Usar `.maybeSingle()` se zero linhas é um caso válido; revisar o filtro se esperava uma única linha |
| Realtime não dispara nada | Tabela sem replicação habilitada, ou canal não te inscreveu no evento certo | Checar Database → Replication; conferir `schema: 'public', table: 'nome_certo'` no `.on(...)` |

## 🏠 Para praticar depois da aula (1 h)

Recrie o CRUD da sua entidade principal usando Supabase (se ainda não completou no laboratório) e escreva uma **análise comparativa de 1 página** entre a abordagem Express+MySQL (Aula 11) e a abordagem Supabase (hoje), cobrindo: quantidade de código escrito em cada uma, onde ficou a validação e a regra de negócio em cada caso, o que foi mais rápido de implementar, o que você confiaria menos sem testes automatizados, e qual você escolheria para o seu projeto autoral final — com justificativa. **Guarde este texto: é exatamente o tipo de comparação técnica que volta na retrospectiva de padrões da Aula 15.**

**Critério de pronto:** CRUD Supabase funcionando (RLS + policies + operações básicas) e o texto comparativo entregue, com pelo menos os cinco pontos acima abordados.

## ✅ Checkpoint do projeto autoral

- [ ] Projeto Supabase criado, com `VITE_SUPABASE_URL` e `VITE_SUPABASE_ANON_KEY` no `.env` (nunca a `service_role`).
- [ ] Tabelas da entidade principal criadas por SQL, com `uuid` como PK e `timestamptz` onde há data/hora.
- [ ] RLS habilitado em toda tabela nova, com as quatro policies (leitura pública, inserção autenticada, edição e exclusão do dono) escritas e testadas.
- [ ] CRUD completo com `supabase-js`, sempre tratando `{ data, error }`.
- [ ] Login/logout via Supabase Auth conectado às policies por `auth.uid()`.
- [ ] Realtime funcionando em pelo menos uma tela.
- [ ] `eventosRepo` (ou equivalente autoral) implementado nas duas versões (API própria e Supabase), com troca por variável de ambiente.
- [ ] Análise comparativa de 1 página escrita e guardada no repositório.

## 📚 Para aprofundar

- [Supabase — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Supabase — `supabase-js` reference](https://supabase.com/docs/reference/javascript/introduction)
- [Supabase — Auth](https://supabase.com/docs/guides/auth)
- [Supabase — Realtime](https://supabase.com/docs/guides/realtime)
- [PostgreSQL — `timestamptz` e tipos de data](https://www.postgresql.org/docs/current/datatype-datetime.html)
- Plano de curso, Unidade 3: banco de dados em nuvem e padrões estruturais.

A Aula 13 muda de foco: em vez de mais um fornecedor, vamos **refatorar e consolidar o back-end** do UniEventos — revisando a arquitetura em camadas, aplicando injeção de dependência e organizando tudo o que construímos nas Aulas 07 a 12 num back-end coeso e defensável.
