# Capítulo 08 — Bancos de dados na nuvem

> **Deploy & Ferramentas** · Unidade 3: Infraestrutura, automação e qualidade
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 2 a 3 h · estudo autônomo, em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Explicar o que um banco gerenciado entrega além do banco em si (backup automático, alta disponibilidade, atualizações, métricas) e quando ele não compensa.
- Criar um Postgres no Supabase, ler o painel e escolher entre conexão direta, pooler de sessão e pooler de transação, sabendo o que cada um resolve.
- Conectar a API ao banco na nuvem com `pg` (Postgres) ou `mysql2/promise` (MySQL), sempre com pool e TLS verificado, e configurar tudo por uma única variável `DATABASE_URL`.
- Traduzir um schema MySQL para Postgres (tipos, chaves, placeholders, `RETURNING`) sem quebrar o código da API.
- Versionar mudanças de schema com migrations em SQL numeradas e escrever um seed idempotente.
- Fazer backup e restauração com `pg_dump`/`psql` e `mysqldump`/`mysql`, automatizar com `cron` e **provar** que o backup restaura.
- Reconhecer os erros clássicos de conexão na nuvem: IPv6, TLS, limite de conexões e RLS.

## 📋 Pré-requisitos

- [ ] `unieventos-api` na forma da Aula 13 do Nível 3: camadas (`controllers`, `services`, `repositories`), `src/config/index.js` validando o ambiente com zod, `migrations/*.sql` e `npm run migrar`.
- [ ] Docker e `docker compose` funcionando (Capítulo 07) — você vai usá-los para testar restaurações sem sujar nada.
- [ ] Conta no GitHub (Capítulo 02) — o login do Supabase e do Neon pode ser feito por ela.
- [ ] Cliente de linha de comando do banco: `psql` (pacote `postgresql-client`) e/ou `mysql` + `mysqldump` (pacote `mysql-client`).
- [ ] Um `.env` local funcionando, e a certeza de que ele **não** está no Git (Capítulo 02) nem na imagem (Capítulo 07).

> No Capítulo 07 a `unieventos-api` e o MySQL viraram contêineres, e o volume `dados-mysql` guardou os dados no disco do VPS. Funciona — mas repare no que você comprou junto: se aquele VPS morrer, os dados morrem com ele; se o disco encher, o MySQL para; se você quiser rodar a API em dois lugares (um teste no Render e a produção no VPS), são dois bancos diferentes, cada um com uma verdade. Backup, atualização de versão, ajuste de memória e monitoramento também passaram a ser trabalho seu. Hoje o banco sai do servidor e vira um **serviço gerenciado** — Supabase, Neon ou um MySQL na nuvem —, acessível pela internet, com backup automático e uma URL só sua: você vai conectar a API por TLS, versionar o schema com migrations, popular com um seed e, principalmente, aprender a fazer e **testar** um backup. No Capítulo 09 o GitHub Actions vai construir a imagem, rodar os testes e publicar tudo sozinho, e um banco gerenciado é o que torna esse deploy automático seguro: a máquina pode ser recriada do zero sem levar os dados junto.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Por que tirar o banco do servidor; o mapa dos serviços; projeto no Supabase e as três strings de conexão |
| 2 | 50 min | Conectando com `pg` e `mysql2/promise`: pool, TLS, `DATABASE_URL`; traduzindo o schema para Postgres |
| 3 | 50 min | Migrations, seed, backup e restauração testada; Passo a passo e Laboratório |

## 1. Por que tirar o banco do servidor

Um banco de dados é o único componente da sua aplicação que **não pode ser recriado**. O código está no GitHub; a imagem está no GHCR; o servidor você reinstala em vinte minutos com os comandos do Capítulo 06. Os dados, não: se sumirem, sumiram.

Rodar o banco no mesmo VPS da API cria três riscos que só aparecem quando é tarde:

1. **Falha única.** O disco do VPS é um só. Provedores baratos usam disco local sem réplica; um problema de hardware leva o servidor inteiro.
2. **Concorrência por recursos.** Um pico de acesso faz o Node consumir CPU, o MySQL fica sem CPU, as consultas ficam lentas, as requisições se acumulam, o Node consome mais memória — e o kernel escolhe alguém para matar. Em um VPS de 1 GB, quem morre quase sempre é o banco.
3. **Manutenção esquecida.** Atualização de versão, `innodb_buffer_pool_size`, verificação de backup, monitoramento de espaço. Tudo isso é trabalho contínuo que ninguém faz até dar errado.

Um **banco gerenciado** é um servidor de banco operado por outra empresa, que entrega para você apenas o endereço e as credenciais. O que vem junto:

| Você deixa de fazer | O serviço faz | Cuidado que continua seu |
|---|---|---|
| Instalar e atualizar o SGBD | versões corrigidas, patches de segurança | testar a aplicação depois de uma atualização maior |
| Configurar backup | snapshots automáticos com retenção | conferir que o backup **restaura** |
| Dimensionar disco e memória | crescimento automático ou com um clique | acompanhar o consumo e o custo |
| Monitorar | painel com conexões, consultas lentas, uso de CPU | olhar o painel de vez em quando |

O que **não** muda: modelagem, índices, consultas eficientes e segurança da aplicação continuam sendo responsabilidade sua. Um banco gerenciado com uma consulta sem índice é lento igual.

> **🧠 Você sabia?**
> A palavra "nuvem" esconde uma máquina muito concreta. Quando você cria um Postgres gratuito no Supabase ou no Neon, ele nasce em uma região específica — `sa-east-1` é São Paulo, `us-east-1` é a Virgínia. A luz percorre cerca de 200 km por milissegundo em fibra óptica, e o caminho nunca é reto: de Sinop até a Virgínia e de volta, uma única ida e volta custa por volta de 120 ms, contra uns 20 ms até São Paulo. Uma página que faz 10 consultas em sequência sente essa diferença como um segundo inteiro de espera. Região não é detalhe de cadastro: é decisão de arquitetura.

> **🔬 Investigue**
> Meça a latência até três regiões antes de escolher a sua. No terminal, rode `ping -c 5 aws-0-sa-east-1.pooler.supabase.com` e compare com `ping -c 5 aws-0-us-east-1.pooler.supabase.com` (se o `ping` for bloqueado, use `curl -o /dev/null -s -w "%{time_connect}\n" https://supabase.com` como aproximação). Anote os dois tempos médios. Depois multiplique o maior por 10 — é quanto uma tela que faz 10 consultas sequenciais vai esperar só de rede. Esse número é o argumento para escolher a região mais próxima e para trocar 10 consultas por 1 `JOIN`.

## 2. O mapa dos serviços

Os três caminhos que interessam para os projetos desta trilha:

| Serviço | Banco | Encaixa bem quando |
|---|---|---|
| **Supabase** | Postgres | você já usou o `supabase-js` na Aula 12 e quer o mesmo banco também por SQL direto |
| **Neon** | Postgres | você quer *branches* de banco: uma cópia instantânea do banco por pull request |
| **MySQL gerenciado** (Aiven, Railway, RDS…) | MySQL 8 | o projeto já é MySQL e você não quer traduzir o schema agora |

Planos gratuitos existem nos três, com limites que mudam com frequência (tamanho do banco, número de projetos, tempo de retenção de backup, suspensão por inatividade). **Confira o plano no site antes de decidir** — e nunca coloque um projeto que você quer manter no ar em um plano que suspende o banco depois de uma semana sem uso sem você saber disso.

Três características valem mais que o preço nesta escolha:

- **Região disponível.** Se o serviço não oferece São Paulo, cada consulta vai custar mais de 100 ms.
- **Compatibilidade de rede.** Alguns endereços só existem em IPv6 (§4). Se o seu VPS ou o runner do GitHub Actions só tem IPv4, você precisa do endereço alternativo.
- **Backup que você controla.** Snapshot automático do provedor é ótimo, mas você também precisa de um `.sql` seu, guardado em outro lugar (§8).

> **💡 Dica**
> O Supabase é bem mais que um Postgres: traz autenticação, Storage, Realtime e a API REST automática que você usou na Aula 12 do Nível 3. Neste capítulo usamos **só o banco**, conectando por SQL como faríamos com qualquer Postgres. As duas formas convivem: o front pode falar com o `supabase-js` e a sua API Express falar com o mesmo banco por `pg`.

## 3. Criando o Postgres no Supabase

No painel do Supabase, **New project**: escolha a organização, dê um nome (`unieventos`), gere uma senha forte para o banco e escolha a região **South America (São Paulo)**.

> **⚠️ Atenção**
> A senha do banco aparece **uma vez**. Guarde-a no gerenciador de senhas antes de clicar em criar. Se perder, dá para redefinir em **Settings → Database → Reset database password**, mas isso invalida todas as strings de conexão que já estiverem em uso — inclusive a do servidor em produção.

Enquanto o projeto sobe (leva cerca de um minuto), conheça as três abas que você mais vai usar:

- **Table Editor** — as tabelas em forma de planilha, para conferir dados.
- **SQL Editor** — um terminal SQL no navegador. É onde você roda consultas de conferência.
- **Settings → Database** — as strings de conexão, o certificado TLS e o número de conexões em uso.

### As três strings de conexão

Este é o ponto que mais confunde. O Supabase oferece **três** endereços para o mesmo banco:

| Forma | Porta | Para que serve |
|---|---|---|
| Conexão direta (`db.<ref>.supabase.co`) | 5432 | processos longos, migrations, `pg_dump`; costuma resolver só em IPv6 |
| Pooler de sessão (`...pooler.supabase.com`) | 5432 | APIs que ficam no ar (a nossa): uma conexão por sessão, IPv4 |
| Pooler de transação (mesmo host) | 6543 | funções serverless, que abrem e fecham conexão a cada requisição |

As strings têm esta forma (o `<ref>` é o identificador do projeto, e repare no usuário diferente no pooler):

```text
# conexão direta
postgresql://postgres:SUA_SENHA@db.abcdefghijklmnop.supabase.co:5432/postgres

# pooler de sessão (recomendado para a unieventos-api)
postgresql://postgres.abcdefghijklmnop:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:5432/postgres

# pooler de transação (serverless)
postgresql://postgres.abcdefghijklmnop:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

O **pooler** (o Supabase usa o Supavisor) é um intermediário que mantém um punhado de conexões abertas com o Postgres e as empresta aos clientes. Ele existe porque cada conexão do Postgres custa memória de verdade — o servidor cria um processo por conexão — e o limite de um plano gratuito é da ordem de algumas dezenas. Sem pooler, três instâncias da API com `max: 10` já ocupam 30 conexões, e a próxima que tentar abrir recebe `sorry, too many clients already` — inclusive o `psql` que você usaria para investigar o problema.

A diferença entre os dois modos:

- **Sessão (5432)** — o cliente recebe uma conexão e fica com ela até desconectar. Tudo funciona como no Postgres normal: `SET`, prepared statements, transações longas. É o modo certo para um servidor Express que sobe uma vez e fica no ar.
- **Transação (6543)** — o cliente recebe uma conexão apenas durante cada transação e a devolve em seguida. Muitas conexões de clientes cabem em poucas conexões reais, mas **prepared statements nomeados não sobrevivem** entre transações: o erro clássico é `prepared statement "s1" already exists`. É o modo para código serverless, que sobe e morre a cada requisição.

> **🔎 Por baixo do capô**
> A conexão direta de projetos novos costuma ter só endereço IPv6. Se a sua máquina, o seu VPS ou o runner de CI não tiver IPv6, o Node falha com `Error: connect ENETUNREACH 2600:1f1c:…:5432` — um erro que parece de firewall, mas é de protocolo. Teste com `curl -6 https://ifconfig.co` (responde se você tem IPv6) e `curl -4 https://ifconfig.co`. Por isso o padrão deste capítulo é o **pooler de sessão**, que atende também em IPv4.

## 4. Conectando do Node com `pg`

Instale o driver oficial do Postgres:

```bash
cd unieventos-api
npm install pg
```

O `pg` ainda é distribuído como CommonJS. Em um projeto com `"type": "module"` (o nosso, desde a Aula 07 do Nível 3), você importa o pacote inteiro e pega as classes de dentro:

```js
// src/db/pool.js — pool de conexões com o Postgres na nuvem
import { readFileSync } from 'node:fs'
import pg from 'pg'                       // CommonJS: importe o módulo, não { Pool }
import { config } from '../config/index.js'

// Certificado da autoridade do provedor, baixado no painel (§4.1).
// config.DATABASE_CA guarda o caminho relativo à raiz do projeto (§4.2).
const certificadoDaAutoridade = readFileSync(new URL(`../../${config.DATABASE_CA}`, import.meta.url))

export const pool = new pg.Pool({
  connectionString: config.DATABASE_URL,
  ssl: {
    ca: certificadoDaAutoridade,
    rejectUnauthorized: true,             // recusa a conexão se o certificado não bater
  },
  max: 10,                                // conexões simultâneas DESTE processo
  idleTimeoutMillis: 30_000,              // devolve ao servidor conexões ociosas por 30 s
  connectionTimeoutMillis: 10_000,        // falha rápido se o banco não responder em 10 s
})

// Conexões ociosas podem cair (rede, manutenção do provedor). Sem este tratador,
// o erro sobe como exceção não capturada e derruba o processo inteiro.
pool.on('error', (erro) => {
  console.error('erro em conexão ociosa do pool:', erro.message)
})

/** Executa uma consulta e devolve só as linhas, avisando quando ela demora demais. */
export async function consultar(sql, parametros = []) {
  const inicio = Date.now()
  const resultado = await pool.query(sql, parametros)
  const duracao = Date.now() - inicio
  if (duracao > 200) {
    console.warn(`consulta lenta (${duracao} ms): ${sql.trim().slice(0, 70)}`)
  }
  return resultado.rows
}
```

Três decisões dentro desse arquivo merecem explicação:

- **`max: 10` é por processo.** Se você roda dois contêineres da API, são 20 conexões no pooler. Some as instâncias antes de escolher o número; em um plano gratuito, `max: 5` costuma ser mais do que suficiente para várias pessoas testando ao mesmo tempo.
- **`rejectUnauthorized: true` com `ca`.** Sem TLS, a senha do banco viaja em texto puro pela internet. Com TLS mas sem verificar o certificado (`rejectUnauthorized: false`), você está protegido contra quem só escuta, mas não contra quem se coloca no meio da conversa. O certificado da autoridade fecha essa porta.
- **O tratador de `pool.on('error')`.** É o item que separa uma API que sobrevive à noite de uma que amanhece morta.

### 4.1 O certificado da autoridade

No Supabase: **Settings → Database → SSL Configuration → Download certificate**. Salve o arquivo como `certs/banco-ca.crt` na raiz da API. Ele é público (é um certificado, não uma chave), então pode ir para o Git — mas o `.dockerignore` do Capítulo 07 precisa **não** barrá-lo, ou a imagem sobe sem o arquivo e a API morre com `ENOENT`.

```bash
mkdir -p certs
# copie o arquivo baixado para certs/banco-ca.crt
ls -l certs/banco-ca.crt
```

> **⚠️ Atenção**
> Você vai encontrar muito tutorial usando `ssl: { rejectUnauthorized: false }`. Isso desliga a verificação do certificado: qualquer servidor que responda no endereço passa a ser aceito. Em um trabalho de faculdade ninguém morre por causa disso; em um sistema com dados de pessoas, é uma falha de segurança que tem nome (*man-in-the-middle*). Use o certificado.

### 4.2 `DATABASE_URL` na configuração

Até agora a API guardava `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` e `DB_NAME` separados. Serviços gerenciados entregam **uma URL só**, e essa virou a convenção do mercado (Render, Railway, Fly, Heroku e o próprio Docker Compose usam `DATABASE_URL`). Ajuste o `src/config/index.js` da Aula 13:

```js
// src/config/index.js — trecho: o banco agora é uma URL única
const esquemaDeAmbiente = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().int().positive().default(3000),

  // postgresql://usuario:senha@host:porta/banco
  DATABASE_URL: z
    .string()
    .min(1, 'DATABASE_URL é obrigatória')
    .startsWith('postgres', 'DATABASE_URL deve começar com postgres:// ou postgresql://'),
  DATABASE_CA: z.string().default('certs/banco-ca.crt'),

  FIREBASE_PROJECT_ID: z.string().min(1, 'FIREBASE_PROJECT_ID é obrigatória'),
  CORS_ORIGEM_PERMITIDA: z.string().min(1, 'CORS_ORIGEM_PERMITIDA é obrigatória'),
})
```

```text
# .env.example — copie para .env e preencha; o .env NUNCA vai para o Git
NODE_ENV=development
PORT=3000

DATABASE_URL=postgresql://postgres.SEU_REF:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:5432/postgres
DATABASE_CA=certs/banco-ca.crt

FIREBASE_PROJECT_ID=unieventos-12345
CORS_ORIGEM_PERMITIDA=http://localhost:5173
```

> **💡 Dica**
> Senha com caractere especial (`@`, `:`, `/`, `#`) quebra a URL: o `@` da senha é confundido com o separador do host. Ou gere uma senha só com letras, números e `-`/`_`, ou codifique os especiais (`@` vira `%40`, `#` vira `%23`). No Node, `encodeURIComponent('mi@nha#senha')` mostra o valor certo.

### 4.3 A variante MySQL gerenciado

Se o seu projeto continua em MySQL, muda o driver, não a ideia. O `mysql2/promise` com `createPool` é o mesmo da Aula 09 do Nível 3, agora com TLS e host remoto. Nesta variante o `src/config/index.js` mantém as variáveis separadas (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`) em vez de `DATABASE_URL`:

```js
// src/db/pool.js — variante para MySQL gerenciado (Aiven, Railway, RDS…)
import { readFileSync } from 'node:fs'
import mysql from 'mysql2/promise'
import { config } from '../config/index.js'

export const pool = mysql.createPool({
  host: config.DB_HOST,
  port: config.DB_PORT,
  user: config.DB_USER,
  password: config.DB_PASSWORD,
  database: config.DB_NAME,
  ssl: {
    ca: readFileSync(new URL('../../certs/banco-ca.pem', import.meta.url)),
    minVersion: 'TLSv1.2',
  },
  waitForConnections: true,
  connectionLimit: 10,       // equivale ao max do pg
  queueLimit: 0,             // fila ilimitada de quem espera conexão
  enableKeepAlive: true,     // evita que firewalls derrubem conexões ociosas
})

/** Executa uma consulta e devolve só as linhas. */
export async function consultar(sql, parametros = []) {
  const [linhas] = await pool.query(sql, parametros)
  return linhas
}
```

`mysql.createPool('mysql://usuario:senha@host:porta/banco')` também aceita a URL inteira como string; com certificado próprio, os campos separados ficam mais legíveis. Note a diferença de retorno que já apareceu na Aula 09: o `mysql2` devolve `[linhas, campos]`, o `pg` devolve um objeto com `.rows`. A função `consultar` esconde isso do resto da aplicação — é o mesmo Adapter da Aula 12.

## 5. Traduzindo o schema: MySQL → Postgres

Se você está saindo do MySQL, o schema precisa de ajustes. Nenhum deles é difícil; todos aparecem de uma vez na primeira migration.

| MySQL | Postgres | Atenção |
|---|---|---|
| `INT AUTO_INCREMENT PRIMARY KEY` | `INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY` | `SERIAL` funciona, mas é a forma antiga |
| `ENUM('a','b')` | `VARCHAR(20) CHECK (col IN ('a','b'))` | ou um `CREATE TYPE ... AS ENUM` |
| `DATETIME` | `TIMESTAMPTZ` | guarde sempre com fuso; converta na apresentação |
| `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` | `TIMESTAMPTZ NOT NULL DEFAULT now()` | `now()` respeita a transação |
| `ENGINE=InnoDB CHARSET=utf8mb4` | (nada) | Postgres é transacional e UTF-8 por padrão |
| `?` como placeholder | `$1`, `$2`, `$3` | numerados, podem repetir |
| `resultado.insertId` | `RETURNING *` na própria consulta | devolve a linha inteira, não só o id |
| `` `crase` `` para identificadores | `"aspas duplas"` | sem aspas, Postgres rebaixa tudo para minúsculas |

A migration `0001` do UniEventos, na versão Postgres:

```sql
-- migrations/0001_criar_tabela_eventos.sql
CREATE TABLE IF NOT EXISTS eventos (
  id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  titulo      VARCHAR(150) NOT NULL,
  descricao   TEXT,
  categoria   VARCHAR(20) NOT NULL
              CHECK (categoria IN ('palestra', 'minicurso', 'workshop')),
  data_hora   TIMESTAMPTZ NOT NULL,
  local       VARCHAR(150) NOT NULL,
  vagas       INTEGER NOT NULL DEFAULT 0 CHECK (vagas >= 0),
  imagem_url  VARCHAR(255),
  criado_em   TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT uk_eventos_titulo UNIQUE (titulo)
);
```

A restrição `uk_eventos_titulo` não é decoração: além de impedir dois eventos com o mesmo nome, ela é o que permite ao seed da §7 dizer "insira **se não existir**" com uma única instrução.

```sql
-- migrations/0002_criar_tabela_inscricoes.sql
CREATE TABLE IF NOT EXISTS inscricoes (
  id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  evento_id    INTEGER NOT NULL REFERENCES eventos(id) ON DELETE CASCADE,
  usuario_uid  VARCHAR(128) NOT NULL,
  criado_em    TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT uk_evento_usuario UNIQUE (evento_id, usuario_uid)
);

CREATE INDEX IF NOT EXISTS idx_inscricoes_usuario ON inscricoes (usuario_uid);
```

E o repositório, adaptado. É a mesma interface da Aula 13 — quem chama não percebe a troca:

```js
// src/repositories/eventos.repository.postgres.js
import { pool } from '../db/pool.js'

export function criarRepositorioDeEventosPostgres() {
  return {
    async listar({ categoria = null, limite = 20, deslocamento = 0 } = {}) {
      const { rows } = await pool.query(
        `SELECT * FROM eventos
          WHERE ($1::text IS NULL OR categoria = $1)
          ORDER BY data_hora
          LIMIT $2 OFFSET $3`,
        [categoria, limite, deslocamento],
      )
      return rows
    },

    async buscarPorId(id) {
      const { rows } = await pool.query('SELECT * FROM eventos WHERE id = $1', [id])
      return rows[0] ?? null
    },

    async criar(evento) {
      const { rows } = await pool.query(
        `INSERT INTO eventos (titulo, descricao, categoria, data_hora, local, vagas, imagem_url)
         VALUES ($1, $2, $3, $4, $5, $6, $7)
         RETURNING *`,
        [
          evento.titulo,
          evento.descricao ?? null,
          evento.categoria,
          evento.dataHora,
          evento.local,
          evento.vagas ?? 0,
          evento.imagemUrl ?? null,
        ],
      )
      return rows[0]
    },

    async remover(id) {
      const resultado = await pool.query('DELETE FROM eventos WHERE id = $1', [id])
      return resultado.rowCount > 0
    },
  }
}
```

Duas sutilezas que economizam meia hora de depuração:

- **`$1::text IS NULL OR categoria = $1`** — o Postgres precisa saber o tipo de cada parâmetro para planejar a consulta. Quando o mesmo `$1` aparece comparado com `NULL` e com uma coluna, o `::text` tira a ambiguidade; sem ele, o erro é `could not determine data type of parameter $1`.
- **`resultado.rowCount`** — o equivalente ao `affectedRows` do MySQL. É o que diz se o `DELETE` realmente apagou alguma coisa (para responder 404 em vez de 204).

> **🧠 Você sabia?**
> No Postgres, `CREATE TABLE`, `ALTER TABLE` e `DROP TABLE` são transacionais: dentro de `BEGIN … ROLLBACK`, uma tabela criada some como se nunca tivesse existido. No MySQL, não — qualquer comando de definição de dados confirma a transação em andamento silenciosamente. É por isso que um script de migration que falha no meio deixa o Postgres intacto e o MySQL em um estado híbrido, com metade das mudanças aplicadas. Essa única diferença já justifica o cuidado extra ao escrever migrations para MySQL.

## 6. RLS: o que muda quando você conecta por SQL

Na Aula 12 do Nível 3 você habilitou **Row Level Security** nas tabelas do Supabase e escreveu policies — sem elas, o `supabase-js` recebe `data: []` sem erro nenhum — um dos maiores consumidores de tempo de depuração nesta trilha.

Aqui está o detalhe que quase ninguém conta: quando a sua API conecta com a **string de conexão do banco**, ela entra como o papel `postgres`, que é dono das tabelas. E o dono da tabela **ignora RLS**. Ou seja:

- Pelo `supabase-js`, com a chave pública (`anon`), o RLS vale e as policies decidem o que cada pessoa vê.
- Pelo `pg`, com a senha do banco, o RLS não vale: a sua API vê tudo.

Isso não é um bug — é a divisão de responsabilidades. Quando o navegador fala **direto** com o banco, o banco precisa se defender sozinho (RLS). Quando quem fala com o banco é a **sua API**, é a API que autoriza, no middleware do Firebase da Aula 10 e nos services da Aula 13. As duas coisas convivem: mantenha as policies para o caminho do `supabase-js` e mantenha a autorização no back-end para o caminho SQL.

```sql
-- migrations/0003_habilitar_rls.sql
-- Vale para quem acessa pelo supabase-js (chaves anon/authenticated).
-- A API Express, que conecta como dono da tabela, não é afetada por estas regras.
ALTER TABLE eventos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "eventos visíveis para todos"
  ON eventos FOR SELECT
  USING (true);

CREATE POLICY "somente autenticados criam eventos"
  ON eventos FOR INSERT
  TO authenticated
  WITH CHECK (true);
```

> **⚠️ Atenção**
> A `service_role key` do Supabase também ignora RLS e nunca pode aparecer no front — vale a mesma regra da senha do banco. Se você precisa de acesso total, ele fica no servidor. Uma chave dessas em um repositório público é achada por robôs em minutos.

## 7. Migrations no banco na nuvem

O executor de migrations da Aula 13 continua valendo; só o dialeto muda. Esta é a versão Postgres, com um ganho real: cada migration roda **dentro de uma transação**, então uma migration que falha no meio não deixa lixo.

```js
// scripts/migrar.js — aplica migrations/*.sql em ordem, uma única vez cada
import { readdir, readFile } from 'node:fs/promises'
import { readFileSync } from 'node:fs'
import pg from 'pg'
import { config } from '../src/config/index.js'

const PASTA = new URL('../migrations/', import.meta.url)

const cliente = new pg.Client({
  connectionString: config.DATABASE_URL,
  ssl: {
    ca: readFileSync(new URL(`../${config.DATABASE_CA}`, import.meta.url)),
    rejectUnauthorized: true,
  },
})

async function migrar() {
  await cliente.connect()

  await cliente.query(`
    CREATE TABLE IF NOT EXISTS migrations_executadas (
      nome_arquivo TEXT PRIMARY KEY,
      executado_em TIMESTAMPTZ NOT NULL DEFAULT now()
    )
  `)

  const { rows } = await cliente.query('SELECT nome_arquivo FROM migrations_executadas')
  const jaExecutadas = new Set(rows.map((linha) => linha.nome_arquivo))

  const arquivos = (await readdir(PASTA)).filter((nome) => nome.endsWith('.sql')).sort()
  let aplicadas = 0

  for (const arquivo of arquivos) {
    if (jaExecutadas.has(arquivo)) {
      console.log(`pulando ${arquivo} (já aplicada)`)
      continue
    }

    const sql = await readFile(new URL(arquivo, PASTA), 'utf-8')
    console.log(`aplicando ${arquivo}...`)

    // DDL transacional: ou a migration inteira entra, ou nada entra.
    await cliente.query('BEGIN')
    try {
      await cliente.query(sql)
      await cliente.query('INSERT INTO migrations_executadas (nome_arquivo) VALUES ($1)', [arquivo])
      await cliente.query('COMMIT')
      aplicadas += 1
      console.log(`${arquivo} aplicada`)
    } catch (erro) {
      await cliente.query('ROLLBACK')
      throw new Error(`falha em ${arquivo}: ${erro.message}`)
    }
  }

  console.log(`concluído: ${aplicadas} migration(s) nova(s).`)
}

migrar()
  .catch((erro) => {
    console.error('falha ao migrar:', erro.message)
    process.exitCode = 1
  })
  .finally(() => cliente.end())
```

Três regras de convivência com migrations em um banco compartilhado:

1. **Migration aplicada nunca é editada.** O arquivo já rodou no banco de alguém. Para mudar, crie a migration seguinte (`0004_corrigir_tipo_da_coluna_vagas.sql`).
2. **Uma mudança por arquivo, com nome que descreve a mudança.** `0005_adicionar_indice_categoria.sql` conta a história no `git log`.
3. **Migration que apaga dado precisa de revisão de outra pessoa.** `DROP COLUMN` em produção não tem `Ctrl+Z`.

### Seed: dados de exemplo, sem duplicar

Um seed serve para que qualquer pessoa (ou o CI do Capítulo 09) tenha um banco com conteúdo em segundos. A regra de ouro é ser **idempotente**: rodar duas vezes não pode criar dois eventos iguais.

```js
// scripts/semear.js — popula o banco com dados de exemplo, sem duplicar
import { pool } from '../src/db/pool.js'
import { config } from '../src/config/index.js'

const EVENTOS = [
  {
    titulo: 'Semana Acadêmica de Sistemas de Informação',
    categoria: 'palestra',
    local: 'Auditório da FACET',
    vagas: 120,
    descricao: 'Abertura com egressos do curso contando o primeiro emprego.',
  },
  {
    titulo: 'Minicurso de Vue 3 e Vuetify',
    categoria: 'minicurso',
    local: 'Laboratório 2',
    vagas: 30,
    descricao: 'Componentes, rotas e estado em uma tarde.',
  },
  {
    titulo: 'Workshop de Deploy',
    categoria: 'workshop',
    local: 'Laboratório 1',
    vagas: 25,
    descricao: 'Do commit ao domínio com HTTPS.',
  },
]

async function semear() {
  if (config.NODE_ENV === 'production' && process.env.PERMITIR_SEED !== 'sim') {
    throw new Error('recusando semear em produção sem PERMITIR_SEED=sim')
  }

  // ON CONFLICT (titulo) só funciona porque a migration 0001 criou uk_eventos_titulo.
  // Schema é assunto de migration; o seed apenas insere dados.
  let inseridos = 0
  for (const [posicao, evento] of EVENTOS.entries()) {
    const { rowCount } = await pool.query(
      `INSERT INTO eventos (titulo, descricao, categoria, data_hora, local, vagas)
       VALUES ($1, $2, $3, now() + make_interval(days => $4), $5, $6)
       ON CONFLICT (titulo) DO NOTHING`,
      [evento.titulo, evento.descricao, evento.categoria, (posicao + 1) * 7, evento.local, evento.vagas],
    )
    inseridos += rowCount
  }

  console.log(`seed concluído: ${inseridos} evento(s) inserido(s), ${EVENTOS.length - inseridos} já existiam.`)
}

semear()
  .catch((erro) => {
    console.error('falha no seed:', erro.message)
    process.exitCode = 1
  })
  .finally(() => pool.end())
```

`make_interval(days => $4)` cria datas relativas ao momento da execução — assim o seed nunca fica com eventos no passado, e nenhuma data literal entra no código.

```json
{
  "scripts": {
    "migrar": "node scripts/migrar.js",
    "semear": "node scripts/semear.js"
  }
}
```

## 8. Backup e restauração

Provedor faz snapshot. Ótimo. Mas o snapshot está **dentro** da conta do provedor: não protege contra você apagar a tabela errada e só perceber uma semana depois (a retenção do plano gratuito costuma ser curta), nem contra a conta ser suspensa. Um backup próprio, num arquivo que você guarda em outro lugar, custa cinco minutos.

### Postgres: `pg_dump` e `psql`

```bash
# dump lógico completo (schema + dados) em formato texto, legível e versionável
pg_dump "$DATABASE_URL" --no-owner --no-privileges --file=backup-unieventos.sql

# formato comprimido, restaurado com pg_restore — melhor para bancos maiores
pg_dump "$DATABASE_URL" --no-owner --no-privileges --format=custom --file=backup-unieventos.dump

# só os dados de uma tabela (útil para levar dados de produção para o ambiente local)
pg_dump "$DATABASE_URL" --data-only --table=eventos --file=eventos.sql
```

- `--no-owner` e `--no-privileges` removem os comandos que atribuem dono e permissões — sem eles, restaurar em outro servidor falha porque o papel do Supabase não existe lá.
- Aspas duplas em `"$DATABASE_URL"` são obrigatórias: a URL tem `?`, `&` e `:` que o shell interpretaria.

Restaurando:

```bash
# formato texto
psql "$DATABASE_URL_DESTINO" --file=backup-unieventos.sql

# formato custom
pg_restore --dbname="$DATABASE_URL_DESTINO" --no-owner --clean --if-exists backup-unieventos.dump
```

### MySQL: `mysqldump` e `mysql`

O comando prometido no Capítulo 07, agora com as opções que importam:

```bash
mysqldump \
  --host=mysql-xxxx.exemplo.aivencloud.com --port=12345 \
  --user=avnadmin --password \
  --single-transaction --quick --routines --triggers \
  --ssl-mode=REQUIRED \
  unieventos > backup-unieventos.sql
```

- `--single-transaction` tira o dump dentro de uma transação: consistente e **sem travar** as tabelas InnoDB (sem ele, o site fica lento durante o backup).
- `--quick` transmite linha a linha em vez de carregar a tabela inteira na memória.
- `--routines --triggers` incluem procedures e triggers, que ficam de fora por padrão.
- `--ssl-mode=REQUIRED` recusa conexão sem TLS — em banco na nuvem, sempre.

Restaurando:

```bash
mysql \
  --host=mysql-xxxx.exemplo.aivencloud.com --port=12345 \
  --user=avnadmin --password --ssl-mode=REQUIRED \
  unieventos < backup-unieventos.sql
```

### Automatizando e, principalmente, testando

```bash
#!/usr/bin/env bash
# scripts/backup.sh — dump diário com retenção de 7 dias
set -euo pipefail

DESTINO="/srv/backups/unieventos"
CARIMBO="$(date +%Y%m%d-%H%M)"
ARQUIVO="$DESTINO/unieventos-$CARIMBO.dump"

mkdir -p "$DESTINO"

# DATABASE_URL vem do ambiente; nunca escreva a senha aqui dentro.
pg_dump "$DATABASE_URL" --no-owner --no-privileges --format=custom --file="$ARQUIVO"

# mantém só os 7 dumps mais recentes
find "$DESTINO" -name 'unieventos-*.dump' -mtime +7 -delete

echo "backup gerado: $ARQUIVO ($(du -h "$ARQUIVO" | cut -f1))"
```

```bash
chmod +x scripts/backup.sh
crontab -e
# uma linha, backup às 3h da manhã, com o log guardado:
# 0 3 * * * DATABASE_URL='postgresql://postgres.SEU_REF:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:5432/postgres' /srv/unieventos-api/scripts/backup.sh >> /var/log/backup-unieventos.log 2>&1
```

Agora a parte que quase todo mundo pula. **Backup não testado não é backup.** Restaure em um Postgres descartável, usando o Docker do Capítulo 07:

```bash
# 1. sobe um Postgres vazio só para o teste
docker run -d --rm --name pg-teste -e POSTGRES_PASSWORD=teste -p 5433:5432 postgres:17-alpine

# 2. espera aceitar conexão e restaura o dump
sleep 10
pg_restore --dbname='postgresql://postgres:teste@localhost:5433/postgres' --no-owner backup-unieventos.dump

# 3. confere: as contagens batem com as do banco de produção?
psql 'postgresql://postgres:teste@localhost:5433/postgres' -c 'SELECT count(*) FROM eventos;'
psql 'postgresql://postgres:teste@localhost:5433/postgres' -c 'SELECT count(*) FROM inscricoes;'

# 4. derruba
docker stop pg-teste
```

> **🔎 Por baixo do capô**
> `pg_dump` não é um "copiar arquivos": ele abre uma transação com um *snapshot* do banco e reconstrói tudo como comandos SQL — por isso o dump é consistente mesmo com o site recebendo escritas durante a cópia, e por isso ele pode ser restaurado em outra versão do Postgres. O preço: o dump é proporcional ao **conteúdo**, não ao disco, e demora mais em bancos grandes. Ele também exige que a versão do `pg_dump` seja igual ou maior que a do servidor — daí o erro `aborting because of server version mismatch` quando o seu Ubuntu tem `pg_dump` 14 e o Supabase roda uma versão bem mais nova.

## 🚀 Passo a passo — UniEventos com o banco no Supabase, com seed e backup

Ao final destes passos a `unieventos-api` (na sua máquina e no VPS do Capítulo 07) vai falar com um Postgres gerenciado em São Paulo, com o schema aplicado por migrations, dados de exemplo e um backup restaurado com sucesso em um banco descartável.

Está no **Nível 2**? Aplique o mesmo passo na `cafe-cerrado-api`: troque `unieventos` por `cafe_cerrado` nos nomes de banco e de tabela, e o seed de eventos pelo cardápio de produtos. A URL gerenciada, o TLS, as migrations e o teste de restauração são idênticos.

### Passo 1 — criar o projeto e guardar a URL

No painel do Supabase, crie o projeto `unieventos` na região São Paulo. Em **Settings → Database**, copie a string do **pooler de sessão** (porta 5432) e baixe o certificado.

```bash
cd unieventos-api
mkdir -p certs
# salve o certificado baixado como certs/banco-ca.crt
```

### Passo 2 — configurar a API

```bash
npm install pg
```

Ajuste `src/config/index.js` (§4.2), crie `src/db/pool.js` (§4) e preencha o `.env`:

```bash
# .env — local
DATABASE_URL=postgresql://postgres.SEU_REF:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:5432/postgres
DATABASE_CA=certs/banco-ca.crt
```

Teste a conexão antes de qualquer outra coisa:

```bash
node --input-type=module -e "import {pool} from './src/db/pool.js'; const r = await pool.query('select version()'); console.log(r.rows[0].version); await pool.end()"
```

A saída deve começar com `PostgreSQL`. Se der erro, vá direto para a tabela de 🐛 Erros comuns — os quatro primeiros casos cobrem 90% das falhas aqui.

### Passo 3 — migrations e seed

Traduza as migrations para Postgres (§5), atualize `scripts/migrar.js` (§7) e rode:

```bash
npm run migrar
npm run semear
```

Confira no **Table Editor** do Supabase: a tabela `eventos` com três linhas, `inscricoes` vazia e `migrations_executadas` com um registro por arquivo.

### Passo 4 — apontar os repositórios e subir a API

Troque o repositório MySQL pelo de Postgres (§5) na montagem do `src/app.js` e suba:

```bash
npm run dev
curl http://localhost:3000/health
curl http://localhost:3000/api/eventos
```

`/api/eventos` deve devolver os três eventos do seed, vindos da nuvem.

### Passo 5 — o VPS sem MySQL

No VPS do Capítulo 07, o serviço `db` do `compose.prod.yaml` deixa de existir. Antes de removê-lo, leve os dados que já estavam lá:

```bash
ssh meuvps
cd /srv/unieventos-api
# O compose lê o .env sozinho; o seu shell, não. Sem esta linha o -p fica
# sem valor, o mysqldump abre um prompt e o arquivo sai vazio.
set -a; . ./.env; set +a
docker compose -f compose.prod.yaml exec -T db \
  mysqldump -u root -p"$DB_ROOT_PASSWORD" --single-transaction unieventos > dados-antigos.sql
```

Edite `compose.prod.yaml`: apague o serviço `db`, a seção `volumes:` e o `depends_on` da API. Troque as variáveis do banco por `DATABASE_URL` no `.env` de produção (com `chmod 600`) e suba:

```bash
docker compose -f compose.prod.yaml up -d
docker compose -f compose.prod.yaml logs --tail 30 api
curl -s https://api.seudominio.dev/api/eventos | head -c 200
```

A API agora é **sem estado**: pode ser destruída e recriada sem perder nada. É exatamente o que o Capítulo 09 precisa para fazer deploy automático.

### Passo 6 — backup e restauração testada

```bash
export DATABASE_URL='postgresql://postgres.SEU_REF:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:5432/postgres'
./scripts/backup.sh
```

Restaure em um Postgres descartável e compare as contagens (§8). Anote os dois números no `README.md`, na seção **Banco de dados**.

### Como conferir

1. `curl https://api.seudominio.dev/api/eventos` devolve os eventos, e o painel do Supabase mostra a conexão ativa em **Settings → Database**.
2. `docker compose -f compose.prod.yaml ps` no VPS mostra **um** serviço só (`api`).
3. `npm run migrar` rodado duas vezes seguidas não aplica nada na segunda.
4. `npm run semear` rodado duas vezes não duplica eventos.
5. O `pg_restore` em um contêiner vazio devolve exatamente as mesmas contagens de `eventos` e `inscricoes`.

**Resultado esperado:** a API roda em qualquer lugar — seu notebook, o VPS, um contêiner novo — apontando para o mesmo banco, e você tem um arquivo `.dump` que já provou que restaura.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Explique com suas palavras a diferença entre o pooler de sessão (5432) e o de transação (6543) do Supabase. Qual dos dois a `unieventos-api`, que fica no ar o tempo todo, deve usar? E uma função serverless que sobe a cada requisição?

**A2.** A API roda em dois contêineres, cada um com `max: 10` no pool. Quantas conexões o banco vê? Se o plano permite 15, o que acontece com a décima sexta e qual mensagem aparece no log?

**A3.** Traduza para Postgres: `id INT AUTO_INCREMENT PRIMARY KEY`, `status ENUM('ativo','inativo')`, `criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP` e a consulta `SELECT * FROM eventos WHERE categoria = ? LIMIT ?`.

**A4.** Um colega conectou a API pelo `pg` com a senha do banco, testou e disse: "as policies de RLS não estão funcionando, minha API vê tudo". Explique por que isso é esperado e onde a autorização precisa acontecer nesse caminho.

**A5.** Qual é a diferença prática entre `ssl: { rejectUnauthorized: false }` e `ssl: { ca, rejectUnauthorized: true }`? Descreva um ataque que o segundo impede e o primeiro não.

**A6.** Você rodou `npm run semear` três vezes. Quantos eventos existem na tabela e por quê? Que cláusula do `INSERT` garante isso?

### Nível B — Aplicação

**B1.** Meça a diferença que a região faz. Escreva um script que abre a conexão, roda `SELECT 1` cem vezes em sequência e imprime o tempo total e a média por consulta. Rode contra o banco na nuvem e contra um Postgres local em Docker.

Resultado esperado: duas médias, a local na casa de 1 ms e a da nuvem em dezenas de milissegundos; um parágrafo no `README.md` explicando por que 100 consultas sequenciais são um problema de arquitetura.

<details><summary>Dica</summary>

Use `performance.now()` antes e depois do laço. Para o Postgres local, `docker run -d --rm -e POSTGRES_PASSWORD=teste -p 5433:5432 postgres:17-alpine` e uma `DATABASE_URL` apontando para `localhost:5433` (sem TLS: um `ssl: false` condicional resolve).
</details>

**B2.** Adicione a coluna `encerrado BOOLEAN NOT NULL DEFAULT false` à tabela `eventos` usando uma migration nova, sem editar nenhuma migration existente, e faça o repositório passar a filtrar eventos encerrados na listagem.

Resultado esperado: `npm run migrar` aplica só o arquivo novo; `GET /api/eventos` deixa de trazer os encerrados; rodar `npm run migrar` de novo não faz nada.

<details><summary>Dica</summary>

O arquivo é `0004_adicionar_coluna_encerrado.sql` com `ALTER TABLE eventos ADD COLUMN IF NOT EXISTS encerrado BOOLEAN NOT NULL DEFAULT false;`. No repositório, um `AND encerrado = false` no `WHERE` — ou um parâmetro `incluirEncerrados` com valor padrão.
</details>

**B3.** Provoque o esgotamento do pool. Baixe `max` para 2, crie uma rota que roda `SELECT pg_sleep(3)` e dispare 5 requisições simultâneas com `curl` em segundo plano. Observe os tempos de resposta.

Resultado esperado: as duas primeiras respondem em ~3 s, as demais em ~6 s e ~9 s — elas ficaram na fila esperando conexão. Com `connectionTimeoutMillis` baixo, aparece `Error: timeout exceeded when trying to connect`.

<details><summary>Dica</summary>

`for i in 1 2 3 4 5; do (time curl -s localhost:3000/api/lento) & done; wait`. É a demonstração prática de por que uma consulta lenta derruba o site inteiro: ela não segura só a própria requisição, segura o pool.
</details>

**B4.** Faça o backup completo, apague **uma** tabela no banco de teste (nunca no de produção) e restaure só ela a partir do dump.

Resultado esperado: `pg_restore --table=eventos` (ou um dump `--data-only --table=eventos`) devolve a tabela com a mesma contagem, sem tocar nas outras.

<details><summary>Dica</summary>

Faça tudo no contêiner descartável da §8: restaure o dump inteiro nele, `DROP TABLE eventos CASCADE`, e restaure de novo só a tabela. Repare no efeito do `CASCADE` sobre a chave estrangeira de `inscricoes` — esse é o aprendizado do exercício.
</details>

### Nível C — Desafio

**C1.** Faça a API funcionar com **dois** bancos sem mudar uma linha dos services: `DB_DIALETO=postgres` usa o repositório do Supabase, `DB_DIALETO=mysql` usa o do MySQL do Capítulo 07. Uma variável de ambiente escolhe a implementação na inicialização, e a suíte de testes passa nos dois modos.

<details><summary>Dica</summary>

É o Adapter da Aula 12 aplicado ao banco: dois arquivos `eventos.repository.postgres.js` e `eventos.repository.mysql.js` com a mesma interface, e uma fábrica em `src/repositories/index.js` que escolhe pelo `config.DB_DIALETO`. O que vai doer: `RETURNING *` não existe no MySQL (use `insertId` + um `SELECT`), e `$1` versus `?`. Se cada repositório resolver isso internamente, ninguém fora deles precisa saber qual banco está por baixo.
</details>

## 🏆 Desafios

### ⭐ O banco que responde em 20 ms — ou em 200
Tags: banco-de-dados, performance, investigacao

Sua tela de eventos parece rápida no `npm run dev`, com o banco em Docker na mesma máquina, e fica arrastada com o banco na nuvem. Nada no código mudou — mudou a distância. Descubra exatamente quanto da lentidão é rede e quanto é consulta mal escrita, e prove a diferença com números.

**Critérios de pronto**

- Uma tabela no `README.md` com o tempo médio de `GET /api/eventos` em três cenários: banco local, banco na nuvem na região mais próxima e banco na nuvem em outra região.
- O tempo de rede (ida e volta de um `SELECT 1`) medido separadamente do tempo da consulta real.
- Pelo menos uma consulta da API reescrita para fazer **uma** ida ao banco em vez de várias, com o antes e o depois medidos.
- Uma frase explicando por que `EXPLAIN ANALYZE` mostra um tempo menor do que o que a API observa.

<details><summary>Pistas</summary>

1. Crie um segundo projeto gratuito em outra região só para a medição; apague depois.
2. `EXPLAIN ANALYZE SELECT ...` no SQL Editor dá o tempo de execução **dentro** do servidor. A diferença entre esse número e o que o Node cronometra é a rede.
3. Um laço que busca as inscrições de cada evento é o clássico problema de N+1 consultas: 1 consulta da lista + N consultas dos detalhes. `JOIN` ou `WHERE evento_id = ANY($1)` resolvem.
4. Meça com `curl -o /dev/null -s -w "%{time_total}\n"` repetido 10 vezes e tire a média — uma medição só não vale nada.
</details>

### ⭐⭐ O backup que você provou que funciona
Tags: banco-de-dados, deploy, seguranca

Todo mundo tem backup até precisar restaurar. Monte a rotina completa do seu projeto autoral — gerar, guardar fora do servidor, restaurar em um banco descartável e comparar — e execute-a até o fim pelo menos uma vez, com evidência.

**Critérios de pronto**

- `scripts/backup.sh` gera um dump com carimbo de tempo no nome e apaga os mais antigos que 7 dias.
- O script roda por `cron` (ou por uma tarefa agendada) e o log guarda a saída de cada execução.
- Um `scripts/restaurar-teste.sh` sobe um banco em Docker, restaura o dump mais recente e imprime a contagem de linhas de cada tabela.
- O `README.md` traz a saída real dos dois scripts e responde: quanto tempo você levaria para voltar ao ar se o banco fosse apagado agora?
- Nenhuma senha aparece dentro dos scripts nem no `crontab` versionado.

<details><summary>Pistas</summary>

1. `set -euo pipefail` no topo faz o script parar no primeiro erro em vez de seguir e "terminar com sucesso" sem ter feito nada.
2. Para comparar contagens automaticamente, gere um arquivo com `SELECT count(*)` de cada tabela nos dois bancos e use `diff`.
3. Guardar o dump no mesmo servidor não protege contra a perda do servidor. `rclone`, `rsync` para outra máquina ou o upload para um bucket resolvem — o Capítulo 06 já ensinou o `rsync`.
4. Um dump com dados de pessoas é dado pessoal: pense onde ele fica e quem tem acesso.
</details>

### ⭐⭐⭐ Do MySQL para o Postgres sem perder um evento
Tags: banco-de-dados, mysql, supabase, refatoracao

O projeto nasceu em MySQL (Aula 09 do Nível 3) e agora vai para um Postgres gerenciado. O schema muda, os tipos mudam, as consultas mudam — e os dados que já existem precisam chegar do outro lado **inteiros**, com as chaves estrangeiras casando. Faça a migração de verdade, com verificação automática de que nada se perdeu.

**Critérios de pronto**

- Um script (`scripts/migrar-mysql-para-postgres.js`) lê do MySQL e grava no Postgres, em ordem de dependência, dentro de uma transação por tabela.
- Os ids são preservados, e as sequências de identidade do Postgres são ajustadas para não colidir com os ids existentes.
- Um relatório final compara, tabela a tabela, a contagem de origem e de destino, e falha se qualquer uma divergir.
- Datas chegam com o mesmo instante nos dois bancos (atenção ao fuso do `DATETIME` sem fuso do MySQL).
- A API sobe apontando para o Postgres e todos os testes da Aula 13 passam sem mudar um único service.

<details><summary>Pistas</summary>

1. Ordem importa: `eventos` antes de `inscricoes`, senão a chave estrangeira reclama. Ou desabilite as restrições durante a carga e reabilite no fim.
2. Para preservar ids em uma coluna `GENERATED ALWAYS AS IDENTITY`, o `INSERT` precisa de `OVERRIDING SYSTEM VALUE`. Depois, `SELECT setval(pg_get_serial_sequence('eventos','id'), max(id)) FROM eventos` acerta o contador.
3. Inserir 5.000 linhas com 5.000 `INSERT` custa 5.000 idas e voltas de rede. Procure inserção em lote (`UNNEST` ou `INSERT ... VALUES` com muitas tuplas) e compare o tempo.
4. `DATETIME` do MySQL não tem fuso; `TIMESTAMPTZ` tem. Decida explicitamente em qual fuso os valores antigos foram gravados antes de converter — e escreva essa decisão em um comentário.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `Error: connect ENETUNREACH 2600:1f1c:…:5432` | a conexão direta do Supabase só tem endereço IPv6 e a sua rede é IPv4 | use a string do **pooler de sessão** (`...pooler.supabase.com:5432`) |
| `error: password authentication failed for user "postgres"` | senha errada, ou usuário do pooler sem o sufixo do projeto | no pooler o usuário é `postgres.<ref>`; senha com caractere especial precisa ser codificada na URL |
| `error: no pg_hba.conf entry for host "…", SSL off` | conexão aberta sem TLS | passe `ssl: { ca, rejectUnauthorized: true }` no `Pool` |
| `Error: self-signed certificate in certificate chain` | TLS ativo, mas sem o certificado da autoridade do provedor | baixe o certificado no painel e aponte `ca` para ele (não desligue a verificação) |
| `error: sorry, too many clients already` | soma dos `max` de todas as instâncias acima do limite do plano | baixe o `max`, use o pooler e feche o pool no encerramento (`pool.end()`) |
| `error: prepared statement "s1" already exists` | pooler de **transação** (6543) com prepared statements | use a porta 5432 (sessão) para a API que fica no ar |
| `error: relation "eventos" does not exist` | migrations não aplicadas nesse banco, ou banco/schema errado na URL | `npm run migrar` apontando para a URL certa; confira o nome do banco no fim da URL |
| `error: syntax error at or near "AUTO_INCREMENT"` | SQL escrito para MySQL rodando no Postgres | traduza o schema pela tabela da §5 |
| `error: could not determine data type of parameter $1` | o mesmo parâmetro comparado com `NULL` e com uma coluna | escreva o tipo: `$1::text IS NULL OR categoria = $1` |
| `Error: ETIMEDOUT` ao conectar em MySQL gerenciado | IP não liberado na lista de permissões do provedor | libere o IP do VPS e do seu computador no painel do serviço |
| `pg_dump: error: aborting because of server version mismatch` | `pg_dump` mais antigo que o servidor | instale a versão do cliente igual ou maior (`postgresql-client-17`) ou rode dentro de um contêiner com a versão certa |
| Consulta pelo `supabase-js` devolve `data: []` sem erro | RLS habilitado sem policy para aquele papel | crie a policy (§6); pelo `pg` com a senha do banco esse caso não aparece, porque o dono ignora RLS |

## 🏠 Para praticar depois da aula (1 h)

No repositório da API do seu **projeto autoral**:

1. Crie o banco em um serviço gerenciado (Supabase, Neon ou MySQL na nuvem), na região mais próxima, e conecte a API por pool com TLS verificado.
2. Substitua as variáveis soltas do banco por `DATABASE_URL` (mais `DATABASE_CA`) no `src/config/index.js` e atualize o `.env.example`.
3. Garanta que `npm run migrar` cria o schema do zero em um banco vazio e que `npm run semear` popula sem duplicar quando rodado duas vezes.
4. Gere um backup, restaure-o em um banco descartável em Docker e registre no `README.md` a seção **Banco de dados**: qual serviço, qual região, como migrar, como semear, como fazer e como restaurar o backup — em no máximo 15 linhas.

**Critério de pronto:** um colega consegue, só com o `README.md` e um `.env` que você entregue por outro canal, subir a API contra o banco na nuvem e ver dados na rota de listagem. Nenhuma senha aparece no repositório (`git log -p` incluído).

**Guarde no seu repositório:** commit + push.

## ✅ Está no ar quando…

- [ ] O banco existe em um serviço gerenciado, na região mais próxima, e você guardou a senha no gerenciador de senhas.
- [ ] `src/db/pool.js` usa pool (`new pg.Pool` ou `mysql.createPool`) com TLS verificado por certificado, `max` compatível com o plano e tratador de `error`.
- [ ] `DATABASE_URL` está no `.env`, no `.env.example` (sem valor real) e em nenhum outro lugar do repositório.
- [ ] `npm run migrar` aplica o schema em um banco vazio e não faz nada na segunda execução.
- [ ] `npm run semear` popula o banco e é idempotente.
- [ ] `GET /api/eventos` responde com dados do banco na nuvem, local e no VPS.
- [ ] O `compose.prod.yaml` do VPS não tem mais serviço de banco nem volume de dados.
- [ ] Existe um `.sql`/`.dump` de backup guardado **fora** do servidor, e você já o restaurou uma vez conferindo as contagens.
- [ ] O `README.md` tem uma seção **Banco de dados** com serviço, região e os comandos de migrar, semear, backup e restauração.

## 📚 Para aprofundar

- [Supabase — Database](https://supabase.com/docs/guides/database/overview) — visão geral do Postgres gerenciado; leia também "Connecting to your database".
- [Supabase — Connection pooling](https://supabase.com/docs/guides/database/connecting-to-postgres) — as três strings, quando usar cada uma e os limites de conexão por plano.
- [Supabase — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) — policies, `USING` e `WITH CHECK`; releia com a Aula 12 do Nível 3 ao lado.
- [Neon — Branching](https://neon.com/docs/introduction/branching) — cópia instantânea do banco por branch; a base do desafio de banco efêmero do Capítulo 09.
- [node-postgres (`pg`)](https://node-postgres.com/) — em especial "Pooling" e "Queries" (parâmetros `$1`, `rows`, `rowCount`).
- [mysql2 — documentação](https://sidorares.github.io/node-mysql2/docs) — `createPool`, opções de `ssl` e diferenças em relação ao `mysql` original.
- [PostgreSQL — `pg_dump`](https://www.postgresql.org/docs/current/app-pgdump.html) e [`pg_restore`](https://www.postgresql.org/docs/current/app-pgrestore.html) — todas as opções, com exemplos no fim da página.
- [MySQL — `mysqldump`](https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html) — o significado exato de `--single-transaction` e por que ele não serve para MyISAM.
- [PostgreSQL — Data Types](https://www.postgresql.org/docs/current/datatype.html) — a referência para traduzir tipos do MySQL sem chutar.

No próximo capítulo o trabalho manual acaba: o GitHub Actions passa a rodar lint e testes a cada push, publicar o site estático sozinho, construir a imagem Docker da API e enviá-la ao VPS por SSH — e você vai proteger a branch principal para que só entre código que passou por tudo isso.
