# Aula 09 — Integrando com SGBD MySQL

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 3 blocos de 50 min + 1 h de prática

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- explicar por que dados em memória não servem para uma aplicação real, e o que persistência significa;
- modelar as tabelas do UniEventos em MySQL, com chaves primárias, estrangeiras, tipos, restrições e índices;
- instalar e configurar um servidor MySQL (nativo ou via Docker) e conectar-se a ele com uma ferramenta gráfica;
- criar um pool de conexões com `mysql2/promise`, entendendo por que pool e não conexão única;
- escrever consultas parametrizadas, evitando SQL injection por concatenação de string;
- ler resultados de `INSERT`, `UPDATE`, `DELETE` e `SELECT` corretamente com a API baseada em Promise;
- usar transações para operações que precisam ser atômicas (inscrever em evento e decrementar vagas);
- organizar o back-end em camadas — repositório, serviço, controlador — migrando o CRUD da Aula 08 sem quebrar contrato nenhum com o front-end.

## 📋 Pré-requisitos desta aula

Na Aula 08 você chegou ao Marco 2 com um CRUD completo, middlewares próprios e validação com Zod — tudo isso guardando dados num array em memória. Hoje esse array desaparece. Toda a `unieventos-api` passa a persistir em um banco de dados relacional de verdade: **MySQL**.

Vale reforçar o que muda e o que não muda hoje. O que muda: de onde os dados vêm e para onde vão — de um array na RAM para tabelas em disco, com todas as garantias que isso traz. O que **não** muda: o formato de cada requisição, o formato de cada resposta, os status codes, as rotas, os middlewares de validação e de erro. Esse é o teste que valida se você fez a migração corretamente — se o `requests.http` da Aula 08 continuar passando sem editar uma linha sequer, a API está correta.

Guarde desde já uma decisão que vai valer para toda a Unidade 3: **as colunas do banco são `snake_case` (`data_hora`, `imagem_url`), mas o JSON que a API troca com o front continua `camelCase` (`dataHora`, `imagemUrl`)**, como desde a Aula 06. Quem faz a tradução entre os dois vocabulários é o repositório, e só ele — nem o service, nem o controller, nem o Vue precisam saber que existe um `data_hora` do outro lado.

- [ ] `unieventos-api` da Aula 08, com CRUD completo em memória, middlewares e validação Zod funcionando.
- [ ] `requests.http` cobrindo todos os endpoints (Aula 08).
- [ ] Marco 2 alcançado.
- [ ] Modelagem relacional revisada: entidade, atributo, chave primária e estrangeira (conteúdo de cursos anteriores de banco de dados ou estudo prévio equivalente — hoje é aplicação, não introdução).
- [ ] Máquina com privilégios de administrador para instalar o MySQL (ou Docker instalado, como alternativa).
- [ ] Ao menos uma ferramenta gráfica de banco escolhida (MySQL Workbench, DBeaver ou a extensão do VS Code) para inspecionar tabelas visualmente durante a aula.

> **⚠️ Atenção**
> Nunca commite senha de banco de dados no repositório. Toda credencial desta aula vive em `.env`, fora do controle de versão. Se você acidentalmente commitar uma senha, troque-a imediatamente — trocar a senha é mais rápido e mais seguro do que tentar "remover" o commit do histórico.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Modelagem relacional do UniEventos; instalação do MySQL; `schema.sql` completo |
| 2 | 50 min | `mysql2/promise`: pool, consultas parametrizadas, SQL injection, transações |
| 3 | 50 min | Camadas repositório/serviço/controlador; migração dos endpoints da Aula 08 para MySQL |

## 1. Por que dados em memória não servem

O array `eventos` das Aulas 07 e 08 vive na memória RAM do processo Node. Isso tem três problemas fatais para uso real:

**Não sobrevive a um reinício.** Toda vez que você reinicia o servidor (ou ele cai por qualquer motivo), o array volta ao estado inicial do código-fonte — qualquer evento criado, editado ou removido durante a execução se perde.

**Não escala para múltiplas instâncias.** Se você um dia rodar duas cópias da API (para atender mais tráfego), cada cópia tem seu próprio array, na sua própria memória — uma não sabe o que a outra gravou. Os dados ficam inconsistentes entre instâncias.

**Não sobrevive a um deploy.** Publicar uma nova versão do código normalmente significa derrubar o processo antigo e subir um novo — e o processo novo começa com o array do código, não com o estado anterior.

**Persistência** é a propriedade de dados sobreviverem além do tempo de vida do processo que os manipula. Um banco de dados é software especializado exatamente nisso: gravar em disco (ou em memória de forma replicada e durável) de um jeito que sobrevive a reinícios, crashes e múltiplas instâncias acessando ao mesmo tempo — com garantias de consistência que um array simples não oferece.

### Por que relacional, e por que MySQL

O UniEventos tem entidades com relações claras entre si: um evento tem várias inscrições; uma inscrição pertence a um evento e a um usuário. Esse tipo de relação — um-para-muitos, muitos-para-muitos — é exatamente o que um **banco de dados relacional** (SGBD — Sistema Gerenciador de Banco de Dados) modela bem, com chaves estrangeiras garantindo a integridade dessas relações no próprio banco, não só no código da aplicação.

**MySQL** é um dos SGBDs relacionais mais usados no mercado, de código aberto, com décadas de maturidade. Esta trilha usa a versão 8, com o driver `mysql2` (Node) na versão 3.x, sempre pelo submódulo `mysql2/promise` — a variante que devolve `Promise`s em vez de exigir callbacks, compatível com `async`/`await`, no mesmo estilo que você já usa desde a Aula 01.

> **🔎 Por baixo do capô**
> Você já viu o Firestore (Aula 07) como alternativa de persistência. A diferença central: o Firestore é um banco **NoSQL orientado a documentos** — cada documento é um JSON flexível, sem schema fixo entre documentos da mesma coleção, e relações entre coleções são geridas manualmente pela aplicação. Um SGBD relacional como o MySQL exige schema definido antes de inserir dados (as tabelas do script abaixo), mas em troca oferece integridade referencial garantida pelo próprio banco (`FOREIGN KEY`), consultas relacionais poderosas (`JOIN`) e transações ACID robustas. Nenhum dos dois é "melhor" em absoluto — a escolha depende do formato dos dados e das garantias que a aplicação precisa. O UniEventos usa MySQL a partir de hoje porque suas entidades são fortemente relacionadas (evento ↔ inscrição ↔ usuário), o caso de uso clássico para modelagem relacional.

> **🧠 Você sabia?**
> O nome "MySQL" não é uma sigla técnica: "My" é o nome da filha de um dos criadores originais, Michael Widenius, que trabalhava na empresa sueca MySQL AB nos anos 1990. O banco passou por várias mãos corporativas desde então — foi comprado pela Sun Microsystems em 2008, e a Sun foi comprada pela Oracle em 2010, dona atual do MySQL. Apesar das trocas de dono, o MySQL continua open source e é, até hoje, um dos bancos relacionais mais usados do mundo — inclusive por empresas que competem diretamente com produtos da própria Oracle.

## 2. Modelagem relacional aplicada ao UniEventos

Relembrando o modelo de dados do projeto (Aula 07, §3), as três entidades centrais do UniEventos:

- **`eventos`** — os eventos acadêmicos: palestras, minicursos, workshops.
- **`usuarios`** — quem se cadastra e se inscreve (autenticados via Firebase Auth a partir da Aula 10; aqui já preparamos a tabela).
- **`inscricoes`** — a relação muitos-para-muitos entre `usuarios` e `eventos`: um usuário pode se inscrever em vários eventos, um evento tem vários inscritos.

```text
┌───────────────┐          ┌──────────────────┐          ┌───────────────┐
│   eventos      │          │   inscricoes       │          │   usuarios     │
├───────────────┤          ├──────────────────┤          ├───────────────┤
│ id (PK)        │◄─────────│ evento_id (FK)     │          │ id (PK)        │
│ titulo         │  1:N     │ usuario_id (FK)    │─────────►│ firebase_uid   │
│ descricao      │          │ id (PK)             │   N:1    │ nome           │
│ categoria      │          │ criado_em           │          │ email          │
│ data_hora      │          └──────────────────┘          │ criado_em      │
│ local          │                                          └───────────────┘
│ vagas          │
│ imagem_url     │
│ criado_em      │
└───────────────┘
```

### Tipos de dados, restrições e índices

| Coluna | Tipo | Por quê |
|---|---|---|
| `id` | `INT AUTO_INCREMENT` | número inteiro que o próprio banco incrementa a cada inserção |
| `titulo`, `nome`, `email` | `VARCHAR(n)` | texto de tamanho limitado e conhecido |
| `descricao` | `TEXT` | texto longo, sem limite prático relevante |
| `data_hora`, `criado_em` | `DATETIME` | data e hora, sem fuso embutido (cuidado explicado adiante) |
| `vagas` | `INT` | número inteiro não negativo |
| `NOT NULL` | restrição | impede gravar um registro sem aquele campo |
| `UNIQUE` | restrição | impede duplicar um valor (ex.: dois usuários com o mesmo e-mail) |
| índice em chave estrangeira | otimização | acelera buscas e junções (`JOIN`) que filtram por aquela coluna |

> **⚠️ Atenção**
> `DATETIME` no MySQL grava data e hora **sem informação de fuso** — é literalmente "19:00 no dia 15", sem dizer em qual fuso horário. Se a aplicação gravar horários locais (fuso de Sinop, UTC−4) e outra parte do sistema assumir UTC (o padrão do JavaScript com `new Date().toISOString()`), o horário exibido para o usuário fica deslocado. A prática mais segura: padronize um único fuso para toda a aplicação — o mais comum é gravar tudo em UTC no banco e converter para o fuso do usuário só na apresentação (no front-end). Esta trilha, por simplicidade didática, grava os horários já no fuso local do evento; em um sistema com usuários em fusos diferentes, prefira UTC no banco.

### Script `sql/schema.sql` completo

```sql
-- sql/schema.sql
-- Script de criação do banco de dados do UniEventos.
-- Execute com: mysql -u root -p < sql/schema.sql

CREATE DATABASE IF NOT EXISTS unieventos
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE unieventos;

-- tabela de usuários — uid do Firebase Auth vem na Aula 10, já deixamos o campo pronto
CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  firebase_uid VARCHAR(128) UNIQUE,
  nome VARCHAR(120) NOT NULL,
  email VARCHAR(160) NOT NULL UNIQUE,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- tabela de eventos
CREATE TABLE eventos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(160) NOT NULL,
  descricao TEXT,
  categoria ENUM('palestra', 'minicurso', 'workshop') NOT NULL,
  data_hora DATETIME NOT NULL,
  local VARCHAR(160) NOT NULL,
  vagas INT NOT NULL DEFAULT 0,
  imagem_url VARCHAR(400),
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  INDEX idx_eventos_categoria (categoria),
  INDEX idx_eventos_data_hora (data_hora)
);

-- tabela de inscrições — relação N:N entre usuarios e eventos
CREATE TABLE inscricoes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  evento_id INT NOT NULL,
  usuario_id INT NOT NULL,
  criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_inscricoes_evento
    FOREIGN KEY (evento_id) REFERENCES eventos(id)
    ON DELETE CASCADE,

  CONSTRAINT fk_inscricoes_usuario
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    ON DELETE CASCADE,

  -- um mesmo usuário não pode se inscrever duas vezes no mesmo evento
  UNIQUE KEY uk_inscricao_unica (evento_id, usuario_id)
);

-- dados de exemplo
INSERT INTO usuarios (firebase_uid, nome, email) VALUES
  ('uid-exemplo-001', 'Ana Souza', 'ana.souza@exemplo.com'),
  ('uid-exemplo-002', 'Bruno Lima', 'bruno.lima@exemplo.com');

INSERT INTO eventos (titulo, descricao, categoria, data_hora, local, vagas, imagem_url) VALUES
  ('Semana Acadêmica de Computação', 'Palestras e minicursos sobre o mercado de tecnologia.', 'palestra', '2030-10-15 19:00:00', 'Auditório Central', 80, 'https://picsum.photos/seed/semana-computacao/400/240'),
  ('Minicurso de Vue 3', 'Introdução prática ao framework Vue com Composition API.', 'minicurso', '2030-10-20 14:00:00', 'Laboratório 3', 30, 'https://picsum.photos/seed/minicurso-vue/400/240'),
  ('Workshop de Firebase e Express', 'Construindo uma API real do zero.', 'workshop', '2030-10-28 19:30:00', 'Laboratório 1', 25, 'https://picsum.photos/seed/workshop-firebase/400/240');

INSERT INTO inscricoes (evento_id, usuario_id) VALUES
  (1, 1),
  (1, 2),
  (2, 1);
```

`ON DELETE CASCADE` garante que, se um evento for removido, todas as inscrições associadas a ele são removidas automaticamente pelo próprio banco — sem precisar de código na aplicação para limpar registros órfãos. A restrição `UNIQUE KEY uk_inscricao_unica (evento_id, usuario_id)` impede, no nível do banco, que o mesmo usuário se inscreva duas vezes no mesmo evento — mesmo que a aplicação, por algum bug, tentasse permitir.

> **💡 Dica**
> `utf8mb4` (em vez do antigo `utf8` do MySQL, que na verdade só suporta um subconjunto do Unicode) é o padrão recomendado hoje — suporta acentos, emojis e qualquer caractere completo do Unicode sem surpresas.

## 3. Instalando o MySQL

Três caminhos chegam ao mesmo lugar: um servidor MySQL 8 escutando em `localhost:3306`. Escolha o que for mais conveniente para o seu sistema operacional e siga — não é preciso instalar mais de um.

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation   # define senha do root e remove configurações inseguras padrão
```

### Windows

Baixe o **MySQL Installer** em [dev.mysql.com/downloads/installer](https://dev.mysql.com/downloads/installer/), escolha "Server only" (ou "Full" se quiser o Workbench junto), e siga o assistente — ele já pede para definir a senha do usuário `root` durante a instalação.

### Alternativa: Docker (qualquer sistema operacional)

Se você já tem Docker instalado, essa é a forma mais rápida de ter um MySQL isolado, sem instalar nada permanentemente no sistema:

```bash
docker run --name mysql-unieventos \
  -e MYSQL_ROOT_PASSWORD=senhaDeDesenvolvimento123 \
  -e MYSQL_DATABASE=unieventos \
  -p 3306:3306 \
  -d mysql:8
```

Isso sobe um contêiner MySQL 8, já criando o banco `unieventos`, expondo a porta padrão `3306` na sua máquina. Para parar e voltar a usar depois:

```bash
docker stop mysql-unieventos     # para o contêiner
docker start mysql-unieventos    # volta a rodar, com os dados preservados
```

> **⚠️ Atenção**
> A senha do exemplo (`senhaDeDesenvolvimento123`) é só para desenvolvimento local. Nunca reutilize senhas de exemplo de material didático em nada que vá para produção.

> **💡 Dica**
> Se você usa Docker no dia a dia, considere adicionar um `docker-compose.yml` ao repositório `unieventos-api`, versionando a configuração do banco de desenvolvimento junto do código — assim qualquer colega que clonar o projeto sobe o mesmo ambiente com um único `docker compose up -d`, sem precisar copiar o comando `docker run` manualmente.

### Ferramentas para explorar o banco visualmente

| Ferramenta | Característica |
|---|---|
| **MySQL Workbench** | oficial da Oracle/MySQL, completa, modelagem visual de schema |
| **DBeaver** | multiplataforma, suporta vários SGBDs além de MySQL, gratuita |
| **extensão MySQL do VS Code** | fica dentro do próprio editor, boa para consultas rápidas sem trocar de janela |
| **linha de comando (`mysql`)** | sempre disponível, sem instalação extra, ótima para scripts e automação |
| **phpMyAdmin** | interface web, comum em hospedagens compartilhadas; menos usada em desenvolvimento local |

Escolha uma, conecte em `localhost:3306` com o usuário `root` e a senha definida, e rode o `sql/schema.sql` — ou pela ferramenta gráfica, ou direto no terminal:

```bash
mysql -u root -p < sql/schema.sql
```

Depois de rodar o script, use a ferramenta escolhida para navegar visualmente pelas tabelas criadas, conferir os `INSERT`s de exemplo e, se quiser, gerar um diagrama entidade-relacionamento a partir do schema existente — a maioria dessas ferramentas faz engenharia reversa do banco para um diagrama automaticamente, útil para conferir se as relações ficaram como o desenhado na §2.

## 4. `mysql2/promise` na prática

```bash
npm install mysql2
```

### Pool de conexões: por que, e não conexão única

Uma conexão única a um banco de dados atende **uma consulta por vez** — se sua API recebe cinco requisições simultâneas, e cada uma precisa consultar o banco, quatro delas ficam esperando a primeira terminar. Um **pool de conexões** mantém várias conexões abertas simultaneamente, e o driver empresta uma livre para cada consulta, devolvendo ao pool quando ela termina.

```js
// src/bancoDeDados.js
import mysql from 'mysql2/promise'

export const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  waitForConnections: true,   // se todas as conexões estiverem ocupadas, espera na fila em vez de falhar
  connectionLimit: 10,        // no máximo 10 conexões simultâneas no pool
  namedPlaceholders: true,    // permite usar :nome em vez de só "?" nas queries
})
```

`waitForConnections: true` significa que, se as 10 conexões do `connectionLimit` estiverem todas ocupadas no momento de uma nova consulta, o driver enfileira a requisição e espera uma liberar, em vez de lançar erro imediatamente. `namedPlaceholders: true` habilita a sintaxe `:nomeDoParametro` nas consultas, além da tradicional `?` posicional — útil quando a query tem muitos parâmetros e a ordem fica difícil de acompanhar.

### `pool.query` vs `pool.execute`

```js
// pool.query: envia a consulta e os valores juntos, o driver monta e executa
const [linhas] = await pool.query('SELECT * FROM eventos WHERE categoria = ?', ['palestra'])

// pool.execute: usa prepared statements no protocolo do MySQL — o SQL é compilado
// uma vez pelo servidor e reutilizado, mais eficiente para consultas repetidas
const [linhas2] = await pool.execute('SELECT * FROM eventos WHERE categoria = ?', ['palestra'])
```

Para a maioria dos casos, o comportamento observável é o mesmo — a diferença é performance em consultas repetidas com muita frequência (prepared statements do `execute` compensam o custo extra de preparo quando a mesma consulta roda muitas vezes). Esta trilha usa `pool.execute` como padrão no repositório, por ser a prática mais recomendada em produção.

### Consultas parametrizadas — e o ataque que elas evitam

Nunca, em hipótese alguma, concatene valores vindos do usuário diretamente numa string SQL:

```js
// NUNCA FAÇA ISSO — vulnerável a SQL injection
const categoria = req.query.categoria
const sql = `SELECT * FROM eventos WHERE categoria = '${categoria}'`
const [linhas] = await pool.query(sql)
```

Se alguém enviar `categoria` como `' OR 1=1 --`, a string final montada fica:

```sql
SELECT * FROM eventos WHERE categoria = '' OR 1=1 --'
```

`OR 1=1` é sempre verdadeiro, e `--` comenta o resto da linha — a consulta passa a devolver **todos** os eventos da tabela, ignorando completamente o filtro pretendido. Em consultas de autenticação, o mesmo tipo de ataque pode permitir login sem senha correta; em `DELETE`/`UPDATE` malformados dessa forma, pode apagar ou alterar a tabela inteira.

A correção é sempre usar **placeholders** (`?` ou `:nome`), nunca concatenação:

```js
// CORRETO — consulta parametrizada
const categoria = req.query.categoria
const [linhas] = await pool.execute('SELECT * FROM eventos WHERE categoria = ?', [categoria])
```

Com placeholder, o driver envia a consulta e os valores **separadamente** para o servidor MySQL — o valor nunca é interpretado como parte da sintaxe SQL, não importa o que ele contenha. `' OR 1=1 --` viraria, nesse caso, literalmente o texto que está sendo procurado na coluna `categoria`, e não devolveria nada (porque nenhuma categoria se chama isso).

> **⚠️ Atenção**
> SQL injection é uma das vulnerabilidades mais antigas e mais exploradas da web, e ainda aparece em sistemas reais porque alguém, em algum momento, concatenou uma string "só dessa vez". A regra não tem exceção: todo valor vindo de fora (query string, corpo da requisição, cabeçalho) entra numa query como parâmetro, nunca como texto concatenado.

### Lendo o resultado de cada tipo de consulta

```js
// SELECT: o resultado é um array de linhas (mesmo com 0 ou 1 resultado)
const [linhas] = await pool.execute('SELECT * FROM eventos WHERE id = ?', [1])
const evento = linhas[0] // undefined se não encontrou

// INSERT: o resultado é um objeto com metadados da inserção
const [resultado] = await pool.execute(
  'INSERT INTO eventos (titulo, categoria, data_hora, local, vagas) VALUES (?, ?, ?, ?, ?)',
  ['Palestra de teste', 'palestra', '2030-11-05 19:00:00', 'Auditório Central', 60],
)
console.log(resultado.insertId)       // id gerado pelo AUTO_INCREMENT
console.log(resultado.affectedRows)   // quantas linhas foram afetadas (1, aqui)

// UPDATE / DELETE: também devolvem affectedRows
const [resultadoUpdate] = await pool.execute('UPDATE eventos SET vagas = ? WHERE id = ?', [50, 1])
console.log(resultadoUpdate.affectedRows) // 0 se o id não existia, 1 se atualizou
```

`pool.query`/`pool.execute` sempre devolvem um array de dois elementos — por isso o padrão `const [linhas] = await ...` (desestruturação, já vista desde a Aula 01). O primeiro elemento é o resultado propriamente dito; o segundo (normalmente descartado com `const [linhas]`, ignorando a segunda posição) traz metadados de campos, que raramente usamos diretamente.

### Consultas relacionais com `JOIN`

A vantagem de ter um banco relacional aparece quando você precisa combinar dados de mais de uma tabela numa única consulta — algo que, com dados em memória (Aulas 07–08), exigia laços manuais em JavaScript para "juntar" arrays.

```js
// buscar as inscrições de um evento, já trazendo o nome e e-mail de cada inscrito,
// numa única ida ao banco — sem precisar de uma segunda consulta por usuário
const [inscricoesDoEvento] = await pool.execute(
  `SELECT i.id, i.criado_em, u.nome, u.email
   FROM inscricoes i
   INNER JOIN usuarios u ON u.id = i.usuario_id
   WHERE i.evento_id = ?
   ORDER BY i.criado_em ASC`,
  [eventoId],
)
```

`INNER JOIN` combina linhas de `inscricoes` com as linhas correspondentes de `usuarios`, casando pela condição `u.id = i.usuario_id` — exatamente a relação de chave estrangeira definida no `schema.sql`. O resultado já vem com os dados prontos para a resposta da API, sem processamento adicional em JavaScript.

### Transações: inscrever em evento e decrementar vagas

Considere a operação "inscrever um usuário num evento": ela precisa (1) verificar se há vaga, (2) inserir a inscrição, e (3) decrementar o contador de vagas. Se o passo 2 tiver sucesso mas o passo 3 falhar (por exemplo, o servidor cair no meio), o banco fica em um estado inconsistente — uma inscrição existe, mas a vaga não foi descontada. Uma **transação** garante que um grupo de operações aconteça **tudo ou nada**.

```js
// src/repositories/inscricoesRepository.js
import { pool } from '../bancoDeDados.js'
import { erroNaoEncontrado, erroValidacao } from '../erros/ErroHttp.js'

export async function inscreverUsuarioNoEvento(eventoId, usuarioId) {
  // pool.getConnection() empresta UMA conexão específica do pool, exclusiva para esta transação
  const conexao = await pool.getConnection()

  try {
    await conexao.beginTransaction()

    // trava a linha do evento para leitura, evitando que duas inscrições simultâneas
    // leiam "vagas: 1" ao mesmo tempo e ambas decidam que podem inscrever
    const [eventos] = await conexao.execute(
      'SELECT vagas FROM eventos WHERE id = ? FOR UPDATE',
      [eventoId],
    )

    if (eventos.length === 0) {
      throw erroNaoEncontrado('Evento não encontrado')
    }

    if (eventos[0].vagas <= 0) {
      throw erroValidacao('Não há vagas disponíveis para este evento')
    }

    await conexao.execute(
      'INSERT INTO inscricoes (evento_id, usuario_id) VALUES (?, ?)',
      [eventoId, usuarioId],
    )

    await conexao.execute(
      'UPDATE eventos SET vagas = vagas - 1 WHERE id = ?',
      [eventoId],
    )

    // só grava tudo em definitivo se as três operações acima passaram sem erro
    await conexao.commit()
  } catch (erro) {
    // desfaz TUDO que essa transação tentou fazer — o banco volta ao estado anterior
    await conexao.rollback()
    throw erro
  } finally {
    // devolve a conexão ao pool, sempre — sucesso ou falha
    conexao.release()
  }
}
```

`FOR UPDATE` no `SELECT` trava a linha lida até o fim da transação, impedindo que outra transação concorrente leia o mesmo valor de `vagas` antes do commit — evitando o cenário de duas inscrições simultâneas "roubarem" a última vaga ao mesmo tempo.

> **⚠️ Atenção**
> `conexao.release()` no `finally` é obrigatório. Se você esquecer de liberar uma conexão emprestada do pool, ela fica presa — e depois de `connectionLimit` conexões presas, o pool se esgota e toda nova consulta trava esperando uma conexão livre que nunca aparece. Isso é a causa mais comum de uma API que "funciona bem no início e trava depois de um tempo".

O caminho de sucesso e o caminho de falha, lado a lado:

```text
  beginTransaction()
        │
        ▼
  SELECT ... FOR UPDATE  (lê e trava a linha do evento)
        │
        ▼
  vagas > 0? ──── não ────► throw erroValidacao()  → 422
        │ sim                      │
        ▼                          ▼
  INSERT em inscricoes        catch: rollback()
        │                     (nada gravado)
        ▼                          │
  UPDATE vagas = vagas - 1         │
        │                          │
        ▼                          │
  commit()                         │
  (tudo gravado)                   │
        │                          │
        └──────────┬───────────────┘
                    ▼
             finally: release()
             (conexão sempre volta ao pool)
```

Note que `release()` roda em **ambos** os caminhos — é justamente o papel do `finally`: executar independentemente de a `try` ter chegado ao `commit()` ou de o `catch` ter chegado ao `rollback()`.

> **🔬 Investigue**
> Abra duas conexões simultâneas ao MySQL (duas abas do MySQL Workbench/DBeaver, ou dois terminais com `mysql -u root -p`). Na primeira, rode `START TRANSACTION;` seguido de `SELECT vagas FROM eventos WHERE id = 1 FOR UPDATE;`, e **não** dê `COMMIT` ainda. Na segunda aba, tente rodar a mesma consulta (`SELECT ... FOR UPDATE`) para o mesmo `id`. O que acontece? Volte à primeira aba e rode `COMMIT;` — o que muda imediatamente na segunda?

## 5. Configuração por ambiente

```bash
# .env (nunca commitar)
PORTA=3000
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=senhaDeDesenvolvimento123
DB_NAME=unieventos
```

```bash
# .env.example (versionado, sem valores sigilosos)
PORTA=3000
DB_HOST=localhost
DB_USER=
DB_PASSWORD=
DB_NAME=unieventos
```

```bash
node --watch --env-file=.env src/servidor.js
```

Cada ambiente (sua máquina, a de um colega, um servidor de produção futuro) tem seu próprio `.env`, com valores possivelmente diferentes — mas o mesmo código-fonte funciona em todos, porque nada de configuração está fixado (*hardcoded*) no JavaScript.

## 🧩 Padrão de projeto em uso — Factory / Object Pool e Repository

`mysql2.createPool(...)` é uma aplicação combinada de dois padrões criacionais. **Factory Method**: você não instancia uma conexão diretamente com `new Conexao()` — chama uma função de fábrica (`createPool`) que encapsula a lógica de criação e devolve o objeto pronto para uso, escondendo os detalhes de configuração interna. **Object Pool**: em vez de criar uma conexão nova para cada requisição (caro: negociar protocolo, autenticar, alocar recursos no servidor de banco), o pool mantém um conjunto de conexões já abertas, prontas, emprestando uma a cada consulta e devolvendo-a ao pool quando termina — reduzindo drasticamente o custo de abrir/fechar conexão repetidamente.

A camada de **Repository**, que construímos a seguir, é um padrão estrutural de organização: isola todo o SQL da aplicação dentro de funções com nomes de domínio (`buscarEventoPorId`, `inserirEvento`), para que o resto do código nunca precise saber que existe SQL por trás — só chama métodos. Trocar de MySQL para outro banco (Aula 12, com Supabase) significa reescrever o repositório, sem tocar em serviço, controlador ou rotas.

## 💻 Mão na massa — camadas repositório, serviço e controlador

A partir de agora a `unieventos-api` ganha três camadas com responsabilidades separadas:

```text
requisição HTTP
      │
      ▼
  controller   — lê req, chama o service, monta a resposta HTTP (não sabe SQL)
      │
      ▼
  service      — regra de negócio (ex.: "vagas não pode ficar negativo")
      │
      ▼
  repository   — só SQL: monta e executa queries, devolve dados "crus"
      │
      ▼
  MySQL
```

O **controller** não sabe que existe SQL — ele lida só com `req`/`res` e delega tudo ao service. O **service** não sabe que existe `req`/`res` — ele recebe parâmetros simples e devolve dados ou lança erros de negócio. O **repository** não sabe nada sobre HTTP — só executa SQL e devolve linhas. Essa separação permite testar a regra de negócio sem precisar simular uma requisição HTTP, e trocar o banco de dados (Aula 12, Supabase) sem tocar em controller nem service.

### Passo 1 — repositório de eventos

```js
// src/repositories/eventosRepository.js
import { pool } from '../bancoDeDados.js'

// As colunas do MySQL são snake_case (data_hora, imagem_url); o contrato HTTP da
// unieventos-api é camelCase desde a Aula 06 (dataHora, imagemUrl). O repositório é
// o único lugar da aplicação que conhece os dois vocabulários — é ele que traduz.
function linhaParaEvento(linha) {
  return {
    id: linha.id,
    titulo: linha.titulo,
    descricao: linha.descricao,
    categoria: linha.categoria,
    dataHora: linha.data_hora,
    local: linha.local,
    vagas: linha.vagas,
    imagemUrl: linha.imagem_url,
  }
}

export async function listarEventos({ categoria, ordenarPor, direcao, porPagina, offset }) {
  const colunasPermitidas = ['id', 'titulo', 'data_hora', 'vagas']
  const coluna = colunasPermitidas.includes(ordenarPor) ? ordenarPor : 'id'
  const sentidoOrdenacao = direcao === 'desc' ? 'DESC' : 'ASC'

  // nomes de coluna/direção não podem ser parametrizados com "?" (só valores podem);
  // por isso validamos contra uma lista fixa (colunasPermitidas) antes de montar a string
  let sql = 'SELECT * FROM eventos'
  const parametros = []

  if (categoria) {
    sql += ' WHERE categoria = ?'
    parametros.push(categoria)
  }

  sql += ` ORDER BY ${coluna} ${sentidoOrdenacao} LIMIT ? OFFSET ?`
  parametros.push(porPagina, offset)

  // ATENÇÃO: aqui é pool.query, não pool.execute. O mysql2 envia os parâmetros de um
  // statement preparado como string, e o MySQL recusa `LIMIT '10'` com
  // "Incorrect arguments to mysqld_stmt_execute". Como porPagina e offset já foram
  // validados como inteiros no service, pool.query resolve sem abrir brecha de injeção.
  const [linhas] = await pool.query(sql, parametros)
  return linhas.map(linhaParaEvento)
}

export async function contarEventos(categoria) {
  let sql = 'SELECT COUNT(*) AS total FROM eventos'
  const parametros = []

  if (categoria) {
    sql += ' WHERE categoria = ?'
    parametros.push(categoria)
  }

  const [linhas] = await pool.execute(sql, parametros)
  return linhas[0].total
}

export async function buscarEventoPorId(id) {
  const [linhas] = await pool.execute('SELECT * FROM eventos WHERE id = ?', [id])
  return linhas[0] ? linhaParaEvento(linhas[0]) : null
}

export async function inserirEvento(evento) {
  const [resultado] = await pool.execute(
    `INSERT INTO eventos (titulo, descricao, categoria, data_hora, local, vagas, imagem_url)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [
      evento.titulo,
      evento.descricao || null,
      evento.categoria,
      evento.dataHora,
      evento.local,
      evento.vagas,
      evento.imagemUrl || null,
    ],
  )
  return buscarEventoPorId(resultado.insertId)
}

export async function substituirEvento(id, evento) {
  const [resultado] = await pool.execute(
    `UPDATE eventos
     SET titulo = ?, descricao = ?, categoria = ?, data_hora = ?, local = ?, vagas = ?, imagem_url = ?
     WHERE id = ?`,
    [
      evento.titulo,
      evento.descricao || null,
      evento.categoria,
      evento.dataHora,
      evento.local,
      evento.vagas,
      evento.imagemUrl || null,
      id,
    ],
  )
  if (resultado.affectedRows === 0) return null
  return buscarEventoPorId(id)
}

export async function atualizarEventoParcial(id, campos) {
  const colunasPermitidas = {
    titulo: 'titulo',
    descricao: 'descricao',
    categoria: 'categoria',
    dataHora: 'data_hora',
    local: 'local',
    vagas: 'vagas',
    imagemUrl: 'imagem_url',
  }

  const atribuicoes = []
  const parametros = []

  for (const [chave, valor] of Object.entries(campos)) {
    if (colunasPermitidas[chave]) {
      atribuicoes.push(`${colunasPermitidas[chave]} = ?`)
      parametros.push(valor)
    }
  }

  if (atribuicoes.length === 0) return buscarEventoPorId(id)

  parametros.push(id)
  const [resultado] = await pool.execute(
    `UPDATE eventos SET ${atribuicoes.join(', ')} WHERE id = ?`,
    parametros,
  )
  if (resultado.affectedRows === 0) return null
  return buscarEventoPorId(id)
}

export async function removerEvento(id) {
  const [resultado] = await pool.execute('DELETE FROM eventos WHERE id = ?', [id])
  return resultado.affectedRows > 0
}
```

> **⚠️ Atenção**
> Note que nomes de **coluna** e **direção de ordenação** (`ORDER BY coluna ASC/DESC`) não podem vir de placeholder `?` — o protocolo de prepared statements do MySQL só parametriza **valores**, não identificadores de coluna nem palavras-chave SQL. É por isso que `listarEventos` valida `ordenarPor` contra uma lista fixa (`colunasPermitidas`) antes de montar a string com esse nome — validar contra uma lista fechada de valores aceitos é seguro; aceitar qualquer string do usuário nessa posição reabriria a porta para injection.

### Passo 2 — serviço de eventos

```js
// src/services/eventosService.js
import * as eventosRepository from '../repositories/eventosRepository.js'
import { erroNaoEncontrado, erroValidacao } from '../erros/ErroHttp.js'

export async function obterListaDeEventos({ categoria, ordenarPor, direcao, pagina, porPagina }) {
  const paginaSegura = Math.max(1, Number(pagina) || 1)
  const porPaginaSegura = Math.min(100, Math.max(1, Number(porPagina) || 10))
  const offset = (paginaSegura - 1) * porPaginaSegura

  const [eventos, total] = await Promise.all([
    eventosRepository.listarEventos({ categoria, ordenarPor, direcao, porPagina: porPaginaSegura, offset }),
    eventosRepository.contarEventos(categoria),
  ])

  return {
    eventos,
    paginacao: { pagina: paginaSegura, porPagina: porPaginaSegura, total },
  }
}

export async function obterEventoPorId(id) {
  const evento = await eventosRepository.buscarEventoPorId(id)
  if (!evento) {
    throw erroNaoEncontrado('Evento não encontrado')
  }
  return evento
}

export async function criarEvento(dadosEvento) {
  if (dadosEvento.vagas < 0) {
    throw erroValidacao('Vagas não pode ser negativo')
  }
  return eventosRepository.inserirEvento(dadosEvento)
}

export async function atualizarEventoCompleto(id, dadosEvento) {
  const eventoAtualizado = await eventosRepository.substituirEvento(id, dadosEvento)
  if (!eventoAtualizado) {
    throw erroNaoEncontrado('Evento não encontrado')
  }
  return eventoAtualizado
}

export async function atualizarEventoParcial(id, campos) {
  const eventoAtualizado = await eventosRepository.atualizarEventoParcial(id, campos)
  if (!eventoAtualizado) {
    throw erroNaoEncontrado('Evento não encontrado')
  }
  return eventoAtualizado
}

export async function excluirEvento(id) {
  const removeu = await eventosRepository.removerEvento(id)
  if (!removeu) {
    throw erroNaoEncontrado('Evento não encontrado')
  }
}
```

O service centraliza regras que o repository não deveria conhecer (como "vagas não pode ser negativo") e traduz "não encontrado no banco" (`null`) em um erro de domínio (`erroNaoEncontrado`) — o controller nunca precisa checar `if (!evento)` porque o service já garante isso via exceção.

### Passo 3 — controlador de eventos

```js
// src/controllers/eventosController.js
import * as eventosService from '../services/eventosService.js'

export async function listar(req, res) {
  const { categoria, ordenarPor, direcao, pagina, porPagina } = req.query
  const { eventos, paginacao } = await eventosService.obterListaDeEventos({
    categoria,
    ordenarPor,
    direcao,
    pagina,
    porPagina,
  })
  res.json({ dados: eventos, paginacao })
}

export async function buscarPorId(req, res) {
  const evento = await eventosService.obterEventoPorId(Number(req.params.id))
  res.json({ dados: evento })
}

export async function criar(req, res) {
  const novoEvento = await eventosService.criarEvento(req.body)
  res.status(201).location(`/api/eventos/${novoEvento.id}`).json({ dados: novoEvento })
}

export async function substituir(req, res) {
  const eventoAtualizado = await eventosService.atualizarEventoCompleto(Number(req.params.id), req.body)
  res.json({ dados: eventoAtualizado })
}

export async function atualizarParcial(req, res) {
  const eventoAtualizado = await eventosService.atualizarEventoParcial(Number(req.params.id), req.body)
  res.json({ dados: eventoAtualizado })
}

export async function excluir(req, res) {
  await eventosService.excluirEvento(Number(req.params.id))
  res.status(204).send()
}
```

Repare que nenhum controller trata erro manualmente — todo `throw` (vindo do service, vindo do repository, vindo de qualquer lugar da cadeia de `await`) é capturado automaticamente pelo Express 5 e cai no `tratadorDeErros` da Aula 08, sem nenhuma mudança nele.

### Passo 4 — rotas usando o controller

```js
// src/routes/eventos.routes.js
import { Router } from 'express'
import * as eventosController from '../controllers/eventosController.js'
import { validar } from '../middlewares/validador.js'
import { schemaEvento, schemaEventoParcial } from '../schemas/evento.schema.js'

const router = Router()

router.get('/', eventosController.listar)
router.get('/:id', eventosController.buscarPorId)
router.post('/', validar(schemaEvento), eventosController.criar)
router.put('/:id', validar(schemaEvento), eventosController.substituir)
router.patch('/:id', validar(schemaEventoParcial), eventosController.atualizarParcial)
router.delete('/:id', eventosController.excluir)

export default router
```

Compare com o `eventos.routes.js` da Aula 08: a **assinatura de cada rota é idêntica** (mesmo método, mesmo caminho, mesmo middleware de validação). Só o corpo mudou de "manipula um array" para "chama um controller que fala com MySQL por baixo". Esse é o ponto central da aula: **o contrato HTTP não mudou, então o front-end não precisa de nenhuma alteração.**

### Passo 5 — atualizando o `servidor.js`

```js
// src/servidor.js
import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import compression from 'compression'
import morgan from 'morgan'
import rateLimit from 'express-rate-limit'
import eventosRoutes from './routes/eventos.routes.js'
import { middlewareNaoEncontrado, tratadorDeErros } from './middlewares/erros.js'
import { logger } from './middlewares/logger.js'
import { medidorDeTempo } from './middlewares/medidorDeTempo.js'
import './bancoDeDados.js' // garante que o pool é criado na subida do servidor

const app = express()

app.use(cors())
app.use(helmet())
app.use(compression())
app.use(express.json())
app.use(morgan('dev'))
app.use(logger)
app.use(medidorDeTempo)

const limitador = rateLimit({ windowMs: 15 * 60 * 1000, limit: 100 })
app.use('/api/', limitador)

app.use('/api/eventos', eventosRoutes)

app.use(middlewareNaoEncontrado)
app.use(tratadorDeErros)

const porta = process.env.PORTA || 3000

app.listen(porta, () => {
  console.log(`unieventos-api rodando em http://localhost:${porta}`)
})
```

### Como testar

Com o MySQL rodando e o `schema.sql` aplicado, suba a API (`node --watch --env-file=.env src/servidor.js`) e reabra o **mesmo** `requests.http` da Aula 08 — nenhuma linha dele precisa mudar.

```bash
curl -s http://localhost:3000/api/eventos?pagina=1&porPagina=2 | jq
```

Resultado esperado:

```json
{
  "dados": [
    { "id": 1, "titulo": "Semana Acadêmica de Computação", "categoria": "palestra", "dataHora": "2030-09-10T19:00:00.000Z", "local": "Auditório Central", "vagas": 120, "imagemUrl": null }
  ],
  "paginacao": { "pagina": 1, "porPagina": 2, "total": 3 }
}
```

Confira, item por item: (1) as chaves do objeto vêm em **camelCase** (`dataHora`, `imagemUrl`), e não com o nome das colunas (`data_hora`, `imagem_url`) — é o `linhaParaEvento` do repositório fazendo a tradução; (2) o envelope continua `{ dados, paginacao }`; (3) `POST` inválido devolve `422` com o mesmo `{ erro: { mensagem, codigo } }` de antes; (4) `GET /api/eventos/999` devolve `404`. Se algum teste que passava na Aula 08 agora falha, o problema está na camada MySQL nova, não no contrato da API — que permaneceu idêntico.

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Preveja, sem rodar, o valor de `linhas` e de `evento` no trecho abaixo, considerando que a tabela `eventos` desta aula só tem os ids 1, 2 e 3:

```js
const [linhas] = await pool.execute('SELECT * FROM eventos WHERE id = ?', [999])
const evento = linhas[0]
```

Resultado esperado: `linhas` é um array vazio (`[]`) — nenhuma linha bate com `id = 999` — e `evento` é `undefined`, porque acessar a posição `0` de um array vazio devolve `undefined`.

**A2.** Complete a linha que falta para este `INSERT` inserir corretamente os três valores esperados pela query:

```js
const [resultado] = await pool.execute(
  'INSERT INTO usuarios (firebase_uid, nome, email) VALUES (?, ?, ?)',
  // linha que falta aqui
)
```

Resultado esperado: `[uid, nome, email]` — um array com exatamente três valores, na mesma ordem das três `?` do SQL; a ordem importa tanto quanto a quantidade.

**A3.** Em uma frase: por que `pool.execute` é preferível a `pool.query` para uma consulta que roda com muita frequência (ex.: `buscarEventoPorId`, chamada em quase todo endpoint)?

Resultado esperado: porque `execute` usa prepared statements — o SQL é compilado uma vez pelo servidor MySQL e reaproveitado nas chamadas seguintes, evitando recompilar a mesma consulta repetidamente.

**A4.** Ache o erro nas linhas abaixo (a conexão emprestada do pool não é devolvida em caso de erro) e diga a correção:

```js
export async function contarInscricoes(eventoId) {
  const conexao = await pool.getConnection()
  const [linhas] = await conexao.execute('SELECT COUNT(*) AS total FROM inscricoes WHERE evento_id = ?', [eventoId])
  conexao.release()
  return linhas[0].total
}
```

Resultado esperado: se `conexao.execute` lançar uma exceção, o `conexao.release()` da linha seguinte nunca roda, e a conexão fica presa no pool para sempre. A correção é envolver o `execute` num `try/finally`, com `conexao.release()` dentro do `finally`.

**A5.** Verdadeiro ou falso, com justificativa de uma linha: "`DELETE FROM eventos WHERE id = ?` com um `id` que não existe na tabela lança uma exceção no `mysql2`."

Resultado esperado: falso — o `DELETE` roda normalmente e devolve `affectedRows: 0`; é responsabilidade do código verificar esse valor e decidir se isso significa "não encontrado" (como faz `removerEvento` desta aula).

### Nível B — Aplicação

**B1.** Repositório de usuários. Escreva `src/repositories/usuariosRepository.js` com `listarUsuarios()`, `buscarUsuarioPorId(id)` e `inserirUsuario({ nome, email })`. Use consultas parametrizadas em todas.

Resultado esperado: `listarUsuarios()` devolve um array com os usuários de exemplo (Ana Souza, Bruno Lima); `buscarUsuarioPorId(1)` devolve só o registro de Ana; `inserirUsuario({ nome: 'Carla Dias', email: 'carla@exemplo.com' })` grava um novo registro, e uma consulta seguinte confirma três usuários na tabela.

<details markdown="1">
<summary>Dica</summary>

Siga exatamente o padrão de `eventosRepository.js`: `pool.execute(sql, parametros)`, desestruturando `[linhas]` do retorno.
</details>

**B2.** Endpoint de inscrição. Crie `POST /api/eventos/:id/inscricoes` que recebe `{ "usuarioId": N }` no corpo e chama `inscreverUsuarioNoEvento` (já escrita nesta aula). Teste o caso de sucesso e o caso de vagas esgotadas (zere as vagas de um evento no banco antes de testar).

Resultado esperado: com vagas disponíveis, a resposta é `201` com a inscrição criada; depois de zerar as vagas do evento no banco, a mesma chamada responde `422` com a mensagem "Não há vagas disponíveis para este evento".

<details markdown="1">
<summary>Dica</summary>

O erro de vagas esgotadas já vem como `erroValidacao(...)` (um `ErroHttp` de status 422 e código `VALIDACAO`) de dentro da transação — seu controller só precisa dar `await` e deixar o Express capturar automaticamente.
</details>

**B3.** Ataque de SQL injection controlado. Na sua máquina de desenvolvimento, temporariamente reescreva `buscarEventoPorId` para concatenar a string (sem placeholder), e tente buscar com um `id` malicioso do tipo `1 OR 1=1`. Observe o resultado. Depois reverta para a versão parametrizada e repita o teste, confirmando que o ataque não funciona mais.

Resultado esperado: com a versão concatenada, a query maliciosa (`1 OR 1=1`) devolve **todos** os eventos da tabela em vez de nenhum; com a versão parametrizada, a mesma entrada é tratada como valor literal e não devolve nenhum evento (porque nenhum id se chama isso).

<details markdown="1">
<summary>Dica</summary>

Como `id` nessa rota já passa por `Number(req.params.id)` no controller, o ataque de string não chega inteiro ao repository nesse caso específico — para realmente ver o ataque funcionar, teste diretamente no `eventosRepository`, chamando a função com uma string maliciosa manualmente, sem o `Number()` do meio do caminho. Isso mostra por que **duas camadas de proteção** (validação de tipo + parametrização) são melhores que uma só.
</details>

**B4.** Índice e `EXPLAIN`. Rode `EXPLAIN SELECT * FROM eventos WHERE categoria = 'palestra'` no MySQL Workbench ou DBeaver, antes e depois de remover o índice `idx_eventos_categoria` (`DROP INDEX idx_eventos_categoria ON eventos`). Compare o campo `rows` do resultado (recrie o índice depois do teste).

Resultado esperado: com o índice, `EXPLAIN` mostra `type: ref` e um valor baixo em `rows`; sem o índice, `type: ALL` (varredura completa da tabela) e `rows` igual ao total de linhas da tabela `eventos`.

<details markdown="1">
<summary>Dica</summary>

Com o índice, o MySQL deve mostrar `type: ref` e um número baixo em `rows`. Sem o índice, `type: ALL` (varredura completa da tabela) e `rows` igual ao total de linhas da tabela.
</details>

**B5.** Transação com falha proposital. No meio de `inscreverUsuarioNoEvento`, adicione temporariamente um `throw new Error('falha proposital')` logo depois do `INSERT` na tabela `inscricoes`, antes do `UPDATE` de vagas. Rode a função, confirme que a inscrição **não** aparece na tabela (porque o `rollback` desfez tudo), e remova o `throw` de teste depois.

Resultado esperado: depois do `throw` proposital, a tabela `inscricoes` não ganha nenhuma linha nova — o `rollback` desfez o `INSERT` que já tinha rodado, confirmando que a transação é tudo-ou-nada.

<details markdown="1">
<summary>Dica</summary>

Consulte a tabela `inscricoes` direto pelo Workbench/DBeaver antes e depois de rodar o teste, para confirmar visualmente que nada foi persistido.
</details>

### Nível C — Desafio

**C1.** Endpoint de listagem com `JOIN`. Crie `GET /api/eventos/:id/inscricoes` que devolve a lista de inscritos de um evento, usando a consulta `JOIN` desta aula, no formato de envelope `{ "dados": [...] }`. Trate o caso de evento inexistente com `404`.

Resultado esperado: `GET /api/eventos/:id/inscricoes` devolve `{ "dados": [...] }` com nome e e-mail de cada inscrito, em ordem de inscrição; para um evento inexistente, a resposta é `404`, sem que o controller precise checar isso manualmente (o service já lança o erro).

<details markdown="1">
<summary>Dica</summary>

Siga a mesma separação em camadas: uma função no repository (`listarInscricoesDoEvento`), verificação de existência do evento no service (reaproveite `obterEventoPorId`), e um controller enxuto.
</details>

## 🏆 Desafios

### ⭐ O índice que ninguém usa
Tags: mysql, performance, investigacao, banco-de-dados

Toda tabela do `schema.sql` desta aula tem pelo menos um índice — mas nem toda consulta que você vai escrever no seu projeto autoral necessariamente usa esses índices do jeito que você espera. Rode `EXPLAIN` numa consulta do seu próprio domínio e descubra se ela realmente está usando o índice que você criou, ou se está fazendo uma varredura completa da tabela sem que ninguém tenha percebido.

**Critérios de pronto**

- O `EXPLAIN` de pelo menos uma consulta do seu repositório autoral está colado no README, com os campos `type` e `rows` destacados.
- Uma frase explica se o resultado é bom (usa índice) ou ruim (varredura completa) e por quê.
- Se for ruim, uma segunda versão do `EXPLAIN`, depois de criar o índice que faltava, mostra a melhora.

<details markdown="1">
<summary>Pistas</summary>

1. `EXPLAIN SELECT ...` na frente de qualquer consulta mostra como o MySQL planeja executá-la, sem rodar de verdade.
2. `type: ALL` sempre é suspeito numa tabela grande; `type: ref` ou `type: const` geralmente indicam uso de índice.
3. Um índice só ajuda se a cláusula `WHERE` (ou o `JOIN`) filtrar exatamente pela coluna indexada — um índice em `titulo` não ajuda um `WHERE categoria = ?`.
</details>

### ⭐⭐ Duas inscrições, uma vaga
Tags: mysql, banco-de-dados, bug, investigacao

A transação desta aula usa `FOR UPDATE` para travar a linha do evento — mas o que acontece se você **remover** essa trava de propósito e disparar duas inscrições simultâneas para um evento com exatamente 1 vaga? Reproduza a condição de corrida (*race condition*) que o `FOR UPDATE` existe para evitar, meça o dano, e depois prove que a versão correta resolve.

**Critérios de pronto**

- Uma cópia temporária de `inscreverUsuarioNoEvento` sem o `FOR UPDATE` (troque por um `SELECT vagas FROM eventos WHERE id = ?` simples).
- Um script que dispara duas chamadas quase simultâneas (`Promise.all` com duas chamadas da função) contra um evento com `vagas = 1`.
- Uma consulta ao banco depois do teste mostrando quantas inscrições foram criadas (o bug aparece quando o número é 2, não 1).
- A mesma bateria de testes rodada contra a versão com `FOR UPDATE`, confirmando que só 1 inscrição é criada.

<details markdown="1">
<summary>Pistas</summary>

1. Sem `FOR UPDATE`, as duas transações conseguem ler `vagas: 1` ao mesmo tempo, antes de qualquer uma delas fazer o `UPDATE` — as duas "acham" que podem inscrever.
2. `Promise.all([inscreverUsuarioNoEvento(id, 1), inscreverUsuarioNoEvento(id, 2)])` dispara as duas chamadas de forma concorrente o suficiente para expor a corrida na maioria das vezes (não é garantido a cada execução — rode algumas vezes).
3. `SELECT COUNT(*) FROM inscricoes WHERE evento_id = ?` depois do teste revela o número real de inscrições criadas.
</details>

### ⭐⭐⭐ Migrando sem quebrar nada
Tags: mysql, api, refatoracao, projeto

A promessa central desta aula é que migrar de memória para MySQL não deveria quebrar nenhum contrato de API. Prove isso formalmente no seu projeto autoral: grave as respostas de **todo** o `requests.http` rodando contra a versão em memória (Aula 08), migre para MySQL, rode de novo, e compare as duas rodadas (ignorando só os campos que legitimamente mudam, como datas de criação).

**Critérios de pronto**

- Um script (bash, Node, o que preferir) que roda cada requisição do `requests.http` duas vezes — antes e depois da migração — salvando as respostas em arquivos JSON separados (`respostas-memoria/` e `respostas-mysql/`).
- Uma comparação (`diff`, ou script próprio) apontando quais campos mudaram entre as duas rodadas.
- Uma lista, no README, dos campos que mudaram legitimamente (ex.: `id` pode mudar se o `AUTO_INCREMENT` começar de outro número) e uma confirmação de que o formato (as chaves do JSON, os status codes) é idêntico.
- Se algum contrato realmente quebrou (chave que sumiu, status diferente), uma correção no service ou controller até a comparação bater.

<details markdown="1">
<summary>Pistas</summary>

1. `curl -s <url> | python3 -m json.tool` (ou `jq`) formata a resposta para comparação legível.
2. `diff <(cat respostas-memoria/get-eventos.json) <(cat respostas-mysql/get-eventos.json)` mostra exatamente o que mudou entre os dois arquivos.
3. Ignore `id` e qualquer campo de data/hora automática ao comparar — eles mudam legitimamente entre execuções; o que importa é a estrutura e as regras de negócio (status codes, mensagens de erro, formato do envelope).
</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| `ER_ACCESS_DENIED_ERROR` | usuário ou senha incorretos no `.env` | confira `DB_USER`/`DB_PASSWORD`; teste login manual com `mysql -u usuario -p` |
| `ECONNREFUSED` | MySQL não está rodando, ou porta/host errados | confirme `systemctl status mysql` (Linux) ou o contêiner Docker rodando (`docker ps`) |
| `ER_NO_SUCH_TABLE` | `schema.sql` não foi executado, ou executado no banco errado | rode `mysql -u root -p < sql/schema.sql`; confira `USE unieventos;` no início do script |
| `ER_BAD_DB_ERROR` | `DB_NAME` no `.env` não corresponde ao banco criado | confira o nome exato do banco criado pelo `CREATE DATABASE` |
| Datas retornam com horário deslocado | fuso horário do servidor MySQL diferente do esperado pela aplicação | padronize o fuso do servidor e/ou converta explicitamente no código, sem assumir local implícito |
| `ER_DUP_ENTRY` | tentou inserir um valor que viola `UNIQUE` (e-mail repetido, inscrição duplicada) | trate esse erro específico no service, devolvendo `409 Conflict` com mensagem clara |
| Pool trava depois de um tempo de uso | conexão emprestada com `getConnection()` nunca foi liberada com `.release()` | sempre libere no `finally`, mesmo em caminhos de erro |
| `Too many connections` no lado do servidor MySQL | `connectionLimit` do pool maior que o limite configurado no servidor MySQL | ajuste `connectionLimit` para um valor compatível com a capacidade do servidor |
| `req.body` chega vazio no `POST` de inscrição | testou direto no banco sem passar pela API, ou esqueceu `Content-Type: application/json` no `requests.http` | confirme o cabeçalho e o corpo no arquivo `.http` |
| `resultado.insertId` vem `0` ou `undefined` | a tabela não tem coluna `AUTO_INCREMENT`, ou a query não era um `INSERT` | confira o `CREATE TABLE`; `insertId` só é preenchido em `INSERT` sobre coluna `AUTO_INCREMENT` |
| Erro de sintaxe SQL só em produção, funcionava local | diferença de versão do MySQL entre ambientes, ou script `schema.sql` não aplicado no novo ambiente | garanta que `schema.sql` seja executado em todo ambiente novo antes de subir a API |
| `Incorrect arguments to mysqld_stmt_execute` na listagem paginada | `pool.execute` envia os parâmetros de `LIMIT ? OFFSET ?` como string, e o MySQL só aceita inteiro ali | troque por `pool.query` nessa consulta (com `porPagina`/`offset` já validados como inteiro no service), como no repositório desta aula |
| `PROTOCOL_CONNECTION_LOST` durante uso prolongado | conexão do pool expirou por inatividade (timeout do servidor MySQL) | normal em pools ociosos; o `mysql2` reabre conexões automaticamente na próxima consulta — se persistir, revise `connectionLimit` e tempo de vida da conexão |

## 🏠 Para praticar depois da aula (1 h)

No seu **projeto autoral**:

1. Modele as tabelas do seu domínio em `sql/schema.sql`, com ao menos duas tabelas relacionadas por chave estrangeira (equivalente a `eventos`/`inscricoes`, adaptado ao seu tema).
2. Crie o banco (nativo ou Docker) e execute o script.
3. Migre seu repositório, serviço e controlador da Aula 08 (em memória) para MySQL, seguindo exatamente a separação em camadas desta aula.
4. Rode novamente o seu `requests.http` da Aula 08 sem alterar nenhuma linha — confirme que todos os testes continuam passando, agora contra o MySQL.
5. Implemente pelo menos uma operação transacional própria do seu domínio (qualquer ação que precise de "tudo ou nada" entre duas tabelas).

**Critério de pronto:** sua API autoral persiste em MySQL, os testes do `requests.http` da Aula 08 passam sem modificação, e o front-end autoral continua funcionando sem alterações — prova de que a migração foi transparente para quem consome a API.

## ✅ Checkpoint do projeto autoral

- [ ] `sql/schema.sql` versionado, com `CREATE DATABASE`, `CREATE TABLE`, chaves e `INSERT`s de exemplo.
- [ ] MySQL rodando localmente (nativo ou Docker), banco criado a partir do script.
- [ ] `.env`/`.env.example` com as quatro variáveis de conexão (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`), `.env` nunca commitado.
- [ ] Pool de conexões criado com `createPool`, usado em toda consulta — nenhuma conexão avulsa.
- [ ] Todas as consultas parametrizadas — nenhuma concatenação de valor de usuário em string SQL.
- [ ] Camadas repository/service/controller separadas, cada uma com responsabilidade única.
- [ ] Ao menos uma operação usando transação (`beginTransaction`/`commit`/`rollback`).
- [ ] `requests.http` da Aula 08 passando sem alterações contra a API já em MySQL.

## 📚 Para aprofundar

- Documentação oficial do MySQL 8 — [dev.mysql.com/doc/refman/8.0](https://dev.mysql.com/doc/refman/8.0/en/) (seções de tipos de dados, `FOREIGN KEY`, transações).
- Documentação do driver `mysql2` — [github.com/sidorares/node-mysql2](https://github.com/sidorares/node-mysql2) (README cobre pool, prepared statements e Promise API).
- OWASP — *SQL Injection Prevention Cheat Sheet* — referência de mercado sobre o assunto.
- Documentação do Docker Hub para a imagem oficial `mysql` — [hub.docker.com/_/mysql](https://hub.docker.com/_/mysql).
- MySQL 8 Reference Manual — capítulo *The InnoDB Storage Engine* — para entender transações, `FOR UPDATE` e isolamento em profundidade.
- Documentação do MySQL Workbench — [dev.mysql.com/doc/workbench/en](https://dev.mysql.com/doc/workbench/en/) — modelagem visual (ER Diagram) a partir de um schema existente.
- Plano da disciplina em que esta trilha nasceu — bibliografia básica, capítulos sobre bancos de dados relacionais e persistência.

Na Aula 10, a API que você acabou de migrar para MySQL ganha **autenticação de verdade**: o Firebase Authentication entra em cena para identificar quem faz cada requisição, e você vai proteger rotas — como criar, editar e remover eventos — para que só usuários autenticados (e autorizados) possam executá-las.
