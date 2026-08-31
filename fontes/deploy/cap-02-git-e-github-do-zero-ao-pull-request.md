# Capítulo 02 — Git e GitHub do zero ao pull request

> **Deploy & Ferramentas** · Unidade 1: Ferramentas e versionamento
> WebLab · curso aberto de desenvolvimento web
> **Tempo estimado:** 2 a 3 h · estudo autônomo, em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Explicar o que é um commit, o que ele guarda e por que o Git é diferente de uma pasta com cópias numeradas.
- Descrever as três áreas do Git (diretório de trabalho, área de preparação e repositório) e dizer em qual delas cada arquivo está, lendo a saída de `git status`.
- Criar branches, mesclar com `git merge` e resolver um conflito lendo os marcadores no arquivo.
- Criar um repositório local, registrar mudanças (`git add`, `git commit`) e navegar pelo histórico (`git log`, `git diff`, `git show`).
- Escrever um `.gitignore`, um `README.md` e um `.gitattributes` que servem para qualquer projeto das trilhas.
- Desfazer trabalho com segurança escolhendo entre `git restore`, `git commit --amend`, `git reset` e `git revert`.
- Autenticar-se no GitHub pelo terminal (`gh auth login`), criar o repositório remoto (`gh repo create`), publicar (`git push`) e abrir, revisar e mesclar um pull request (`gh pr create`, `gh pr merge`).
- Usar `git stash`, tags anotadas e um fluxo de trabalho em dupla sem sobrescrever o código do colega.

## 📋 Pré-requisitos

- [ ] Ambiente do Capítulo 01 pronto: `git --version` responde `2.x.y`, `code .` abre o VS Code e você navega pelo terminal.
- [ ] A pasta `~/weblab/site-evento` com as cinco páginas do site do evento acadêmico (Nível 1) — ou a pasta do seu projeto autoral, se você está em outra trilha.
- [ ] Um e-mail que você acesse, para criar a conta no GitHub.
- [ ] O `gh` (GitHub CLI) instalado — o Passo 4 do passo a passo mostra como, em cada sistema.

> No Capítulo 01 você montou a bancada: terminal, VS Code, DevTools, Node e npm. A bancada funciona, mas não tem memória — apagou, apagou; quebrou, quebrou. Hoje você instala essa memória. O Git guarda cada versão do projeto na sua máquina; o GitHub guarda uma cópia na internet, permite trabalhar em dupla e é o endereço público do seu trabalho daqui em diante. No Capítulo 03, esse mesmo repositório vira um site publicado.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 45 min | Por que versionar; as três áreas do Git; configuração, primeiro repositório e histórico (§1 a §4) |
| 2 | 45 min | `.gitignore` e `README.md`; desfazer com segurança; branches, merge e conflitos (§5 a §7) |
| 3 | 60 min | GitHub, `gh`, pull request, stash e tags; passo a passo e Laboratório (§8 a §11) |

## 1. Por que versionar

Abra a pasta de projetos antigos de qualquer colega e você encontra alguma variação disto:

```text
site-final.zip   site-final-2.zip   site-final-agora-vai.zip
site-final-agora-vai-CORRIGIDO.zip   site-final-versao-do-joao.zip
```

Esse esquema falha em quatro pontos, e todos aparecem no semestre: **não dá para saber o que mudou** entre duas pastas sem abrir as duas e comparar arquivo por arquivo; **não dá para desfazer só uma parte** (se a versão nova quebrou o menu mas melhorou o rodapé, você perde as duas coisas ao voltar); **não dá para trabalhar em dupla** sem alguém sobrescrever o outro por WhatsApp; e **não dá para publicar**, porque nenhuma hospedagem moderna aceita `.zip` — todas leem um repositório Git.

Um **sistema de controle de versão** resolve os quatro. O Git registra o projeto inteiro em pontos no tempo (os **commits**), guarda quem fez cada mudança e por quê, permite voltar a qualquer ponto e permite que várias pessoas mexam nos mesmos arquivos e reconciliem o resultado.

E há um efeito colateral pedagógico que importa mais do que parece: **quem versiona experimenta mais.** Sem Git, você hesita antes de reescrever o CSS que está "quase bom". Com Git, você cria uma branch, destrói tudo, e volta ao estado anterior com um comando. A coragem para refatorar é uma consequência técnica do versionamento.

| Sem Git | Com Git |
|---|---|
| "Acho que a versão boa é a de terça" | `git log` mostra data, autor e mensagem de cada versão |
| Comparar arquivos abrindo os dois; copiar a pasta antes de mexer | `git diff` mostra linha a linha o que mudou; `git switch -c experimento` cria uma linha do tempo paralela |
| Mandar `.zip` no WhatsApp | `git push` e o link do repositório |

> **🧠 Você sabia?**
> Linus Torvalds escreveu a primeira versão do Git em pouco mais de duas semanas, depois que o projeto do kernel Linux perdeu o direito de usar a ferramenta proprietária que vinha usando. O objetivo declarado era ser rápido, distribuído e à prova de corrupção de dados — por isso todo commit é identificado por um **hash** do próprio conteúdo. Mudou um byte em qualquer arquivo de qualquer commit antigo? O hash muda, e o Git percebe. Não é um recurso de segurança adicionado depois: é o formato de armazenamento.

## 2. Como o Git pensa

### 2.1 Snapshots, não diferenças

A maioria dos sistemas antigos guardava, para cada arquivo, a **lista de diferenças** em relação à versão anterior. O Git guarda **fotografias do projeto inteiro** (snapshots). A cada commit ele salva o estado de todos os arquivos rastreados; os que não mudaram não são copiados de novo, apenas referenciados.

Cada commit é um objeto com o conteúdo de todos os arquivos naquele instante, o autor, o e-mail e o instante da gravação, a mensagem que você escreveu e o **hash do commit anterior** (o "pai").

É esse último campo que forma a corrente: cada commit aponta para o anterior, e o histórico é a corrente inteira. O identificador de um commit é um hash de 40 caracteres hexadecimais, mas na prática você usa os 7 primeiros (`a3f9c21`), que já são únicos em um projeto de porte comum.

### 2.2 As três áreas

Este é o conceito que mais confunde no começo, e o que mais economiza tempo depois. Um arquivo do seu projeto vive em uma de três áreas:

```text
  Diretório de trabalho          Área de preparação            Repositório
  (working tree)                 (staging area / index)        (.git)
  os arquivos que você           o que você escolheu para      o histórico
  edita no VS Code               entrar no próximo commit      permanente

        │ ─────── git add ──────────────► │ ──── git commit ───────► │
        │ ◄────── git restore ─────────── │                          │
        │ ◄──────────────── git restore --source=HEAD ─────────────  │
```

O **diretório de trabalho** é a pasta que você vê no gerenciador de arquivos; editar aqui não registra nada. A **área de preparação** é uma lista do que vai no próximo commit, e existe para você poder commitar **parte** do que fez — corrigir o menu em um commit e o rodapé em outro, mesmo tendo feito as duas coisas juntas. O **repositório** é a pasta oculta `.git` na raiz do projeto, onde os commits ficam: apagou a `.git`, apagou o histórico; copiou a `.git` junto, levou o histórico.

Um arquivo pode estar em quatro estados: **não rastreado** (o Git nunca o viu), **modificado** (mudou desde o último commit), **preparado** (está na área de preparação) e **inalterado**. O `git status` diz exatamente em qual estado está cada arquivo — leia-o sempre.

### 2.3 HEAD, branch e a linha do tempo

Uma **branch** é apenas um nome que aponta para um commit — não é uma cópia da pasta. **HEAD** é um ponteiro para a branch em que você está: `git switch outra` move o HEAD, e o Git troca o conteúdo da pasta para bater com aquele commit. Criar uma branch é instantâneo, porque só cria um nome; é por isso que o fluxo "uma branch por tarefa" é normal em qualquer time.

> **🔎 Por baixo do capô**
> Entre em um repositório e rode `ls .git`. Você vai ver `HEAD` (um arquivo de uma linha, com o texto `ref: refs/heads/main`), `objects/` (todo o conteúdo, comprimido e endereçado por hash), `refs/heads/` (um arquivo por branch, contendo o hash do commit) e `config` (as configurações locais). Rode `cat .git/HEAD` e `cat .git/refs/heads/main`. O segundo arquivo tem exatamente 41 bytes: o hash do último commit e uma quebra de linha. Uma branch é isso — um arquivo com um hash dentro.

## 3. Configurando o Git

Antes do primeiro commit, diga ao Git quem você é. Essa informação vai junto de **cada commit** e não pode ser corrigida depois sem reescrever o histórico:

```bash
git config --global user.name "Ana Souza"
git config --global user.email "ana.souza@gmail.com"
```

Use o **mesmo e-mail** da sua conta do GitHub; é assim que o site liga os commits ao seu perfil e conta as contribuições.

Mais quatro ajustes que evitam problemas conhecidos (no **Windows**, a chave `core.autocrlf` recebe `true` em vez de `input`):

```bash
git config --global init.defaultBranch main       # nome da branch inicial
git config --global core.editor "code --wait"     # VS Code como editor de mensagens
git config --global pull.rebase false             # git pull faz merge (padrão explícito)
git config --global core.autocrlf input           # Linux e macOS
git config --list --show-origin                   # confere tudo
```

O que é o `autocrlf`? Windows termina linhas com dois caracteres (CR + LF); Linux e macOS, com um só (LF). Sem configuração, um arquivo salvo no Windows aparece como "todas as linhas mudaram" para quem está no Linux. Com `autocrlf`, o Git converte na entrada e na saída, e o aviso `warning: LF will be replaced by CRLF` que você viu no Capítulo 01 passa a ser inofensivo — ele está apenas anunciando a conversão.

O `--show-origin` mostra cada chave, o valor e **de qual arquivo** ela veio (`~/.gitconfig` para o global, `.git/config` para o do projeto). Configurações do projeto vencem as globais — útil quando um repositório precisa de outro e-mail.

> **💡 Dica**
> Apelidos economizam digitação: `git config --global alias.s "status -s"` e `git config --global alias.lg "log --oneline --graph --decorate --all"` fazem `git s` e `git lg` funcionarem.

## 4. O primeiro repositório

### 4.1 `git init` e o primeiro commit

Entre na pasta do projeto e transforme-a em repositório:

```bash
cd ~/weblab/site-evento
git init
git status
```

O `git init` responde `Initialized empty Git repository in /home/ana/weblab/site-evento/.git/`. Nada mais mudou — os arquivos continuam iguais, apenas ganharam uma pasta `.git` ao lado. O `git status` mostra:

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	contato.html
	css/
	img/
	index.html
	inscricao.html
	js/
	palestrantes.html
	programacao.html
```

Tudo está **não rastreado**: o Git enxerga os arquivos, mas não cuida deles ainda. Prepare e commite:

```bash
git add .
git status -s
git commit -m "Estrutura inicial do site do evento com as cinco páginas"
```

O `git status -s` (short) é a versão compacta, de duas colunas: a primeira mostra o estado na área de preparação, a segunda no diretório de trabalho. Aqui ele imprime uma linha `A  <arquivo>` por página. `A` = adicionado; as outras letras que você vai ver são `M` (modificado), `D` (apagado), `R` (renomeado) e `??` (não rastreado).

### 4.2 Mensagens de commit que servem para alguma coisa

A mensagem é lida por você mesmo daqui a três semanas, procurando quando o menu quebrou. Duas regras bastam:

- **Imperativo, presente, em português:** "Adiciona menu responsivo", não "adicionei" nem "adicionando".
- **Diga o *quê* e, se não for óbvio, o *porquê*.** O *como* já está no diff.

| Mensagem ruim | Mensagem boa |
|---|---|
| `alteracoes` | `Corrige alinhamento do menu no celular` |
| `update` | `Adiciona página de palestrantes com 6 fichas` |
| `arrumei o css` | `Troca cores fixas por variáveis CSS no tema` |

Para uma mensagem com corpo (título curto, linha em branco, explicação), rode `git commit` sem `-m`: o VS Code abre (por causa do `core.editor`), você escreve, salva e fecha a aba. O Git usa o texto.

Muitos times adotam **Conventional Commits**, um formato com prefixo: `feat:` para funcionalidade nova, `fix:` para correção, `docs:` para documentação, `style:` para formatação, `refactor:` para reorganização sem mudar comportamento e `chore:` para tarefas de infraestrutura — por exemplo, `fix: corrige link quebrado para programacao.html`. Não é obrigatório no WebLab, mas adote: o histórico fica legível e você já chega no mercado falando a língua.

### 4.3 Lendo o histórico

```bash
git log --oneline                              # uma linha por commit
git log --oneline --graph --decorate --all     # com o desenho das branches
git log --stat                                 # quantas linhas mudaram em cada arquivo
git log -3                                     # só os três últimos
git log --author="Ana"                         # filtra por autor
git log -- css/estilo.css                      # só os commits que tocaram nesse arquivo
```

Saída de `git log --oneline --graph --decorate --all` em um projeto com duas branches:

```text
*   9c1d2e4 (HEAD -> main) Mescla menu-responsivo em main
|\
| * 4b7a0f1 (menu-responsivo) Fecha o menu ao clicar em um link
| * e21c8ad Adiciona botão hambúrguer e media query
|/
* a3f9c21 Estrutura inicial do site do evento com as cinco páginas
```

Para ver o conteúdo de um commit específico, `git show a3f9c21` (mensagem e diff completo), `git show a3f9c21 --stat` (só a lista de arquivos) ou `git show a3f9c21:index.html` (o arquivo como estava naquele commit).

### 4.4 `git diff`: o que exatamente mudou

```bash
git diff              # diretório de trabalho × área de preparação
git diff --staged     # área de preparação × último commit
git diff HEAD         # diretório de trabalho × último commit (os dois juntos)
git diff main menu-responsivo   # diferença entre duas branches
```

Um diff se lê assim:

```text
--- a/css/estilo.css
+++ b/css/estilo.css
@@ -12,7 +12,7 @@ header {
   display: flex;
-  background: #1b6b4a;
+  background: var(--cor-primaria);
   padding: 1rem;
```

`-` é a linha removida, `+` a adicionada, e as linhas sem sinal são contexto. O `@@ -12,7 +12,7 @@` diz que o trecho começa na linha 12 e tem 7 linhas nos dois lados.

> **🔬 Investigue**
> Dentro do `site-evento`, abra o `index.html` e troque o texto do `<h1>`. **Não salve ainda.** Rode `git status`: nada mudou para o Git (ele lê o arquivo em disco). Agora salve e rode `git status` de novo — o arquivo aparece como `modified`. Rode `git diff` e leia as linhas `-`/`+`. Agora `git add index.html`, e rode `git diff` outra vez: sai vazio, porque a mudança saiu do diretório de trabalho e foi para a área de preparação. Rode `git diff --staged` e ela reaparece. Essas duas telas explicam as três áreas melhor do que qualquer diagrama.

## 5. `.gitignore`, `README.md` e `.gitattributes`

### 5.1 O que nunca entra no repositório

Três categorias de arquivo ficam de fora. O **regenerável** (`node_modules/`, `dist/`, `build/`, `.vite/`), que qualquer pessoa recria com `npm install` e `npm run build`. O **secreto** (`.env`, chaves de API, credenciais de banco): um segredo commitado está **público para sempre**, mesmo que você apague depois, porque continua no histórico. E o que é **do seu computador**: `.DS_Store` (macOS), `Thumbs.db` (Windows), `*.log` e pastas de configuração pessoal do editor.

O arquivo `.gitignore`, na raiz, lista o que o Git deve ignorar:

`.gitignore`

```text
# Dependências e artefatos de build
node_modules/
dist/
build/
.vite/

# Variáveis de ambiente e segredos
.env
.env.*.local
*.pem
*.key

# Logs e arquivos do sistema operacional
*.log
.DS_Store
Thumbs.db

# Editores (mantemos as configurações compartilhadas do projeto)
.idea/
.vscode/*
!.vscode/settings.json
```

A sintaxe é simples: uma linha por padrão e `#` para comentário; barra no fim (`dist/`) significa "só pastas com esse nome"; `*` casa qualquer coisa dentro de um nível e `**/` casa qualquer profundidade; barra no começo (`/temp`) ancora na raiz do repositório; e `!` **reverte** a regra anterior — é o que faz `.vscode/settings.json` ser versionado mesmo com `.vscode/*` ignorado.

> **⚠️ Atenção**
> O `.gitignore` só vale para arquivos **não rastreados**. Se você já commitou `node_modules/`, acrescentar a linha não resolve: o Git continua cuidando dele. Remova do rastreamento sem apagar do disco com `git rm -r --cached node_modules` e commite. E se o que vazou foi um `.env` com senha, trocar a senha é obrigatório — apagar o arquivo não apaga o histórico.

### 5.2 `README.md`: a capa do projeto

O GitHub renderiza o `README.md` na página inicial do repositório. É a primeira coisa que quem avalia o projeto, um colega ou um recrutador vai ler. Cinco seções bastam: **o que é**, **como rodar**, **estrutura**, **estado atual** e **autoria**.

`README.md`

```markdown
# Site do Evento — Semana Acadêmica de Sistemas de Informação

Site institucional de cinco páginas para a Semana Acadêmica, construído na
trilha Nível 1 do WebLab. HTML5 semântico, CSS3 responsivo e
JavaScript sem framework.

Como rodar: clone, abra a pasta no VS Code e clique em **Go Live** (extensão
Live Server) com o `index.html` aberto. O site sobe em `http://127.0.0.1:5500`.

    git clone https://github.com/ana-souza/site-evento.git
    cd site-evento && code .

Estrutura: `index.html`, `programacao.html`, `palestrantes.html`,
`inscricao.html` e `contato.html` na raiz; estilos em `css/estilo.css`,
scripts em `js/script.js`, imagens em `img/`.

Estado atual: as cinco páginas em HTML semântico e o menu de navegação estão
prontos; faltam o layout responsivo e a validação do formulário de inscrição.

Ana Souza — Introdução ao Desenvolvimento Web,
seu nome. Código sob licença MIT.
```

Repare que o bloco de comandos dentro do README está indentado com quatro espaços em vez de cercado por crases — é a outra forma de marcar código em Markdown, e ela evita confusão quando o arquivo é mostrado dentro de outro documento. No seu projeto, use títulos `##` para separar as cinco seções e uma lista de tarefas (`- [x]` e `- [ ]`) no estado atual: o GitHub a renderiza com caixas de seleção.

### 5.3 `.gitattributes`: o fim da guerra CRLF

O `core.autocrlf` da §3 é uma configuração da **sua máquina**. O `.gitattributes` é do **projeto**, e vale para todo mundo que clonar:

`.gitattributes`

```text
# Normaliza o fim de linha de todo arquivo de texto para LF no repositório
* text=auto eol=lf

# Arquivos binários: nunca converter
*.png binary
*.jpg binary
*.webp binary
*.pdf binary
*.woff2 binary
```

Com isso, o repositório guarda tudo com LF, independentemente de quem commitou, e cada máquina recebe o que precisa ao clonar. É uma linha que evita diffs de mil linhas quando a dupla usa sistemas diferentes.

## 6. Desfazendo com segurança

Quatro situações, quatro comandos. Escolher errado aqui é a principal causa de trabalho perdido no semestre.

**"Editei e quero voltar ao último commit."** O `git restore` descarta o que está só no diretório de trabalho — e **apaga** de vez o que você escreveu e não commitou:

```bash
git restore index.html            # descarta as mudanças de um arquivo (. = todos)
git restore --staged index.html   # tira da área de preparação, mantendo as edições
```

**"O último commit está errado."** Se você errou a mensagem ou esqueceu um arquivo e **ainda não deu push**, `git add arquivo-esquecido.html` seguido de `git commit --amend -m "nova mensagem"` substitui o último commit por um novo, com outro hash. Nunca use em commit que já foi para o GitHub e que outra pessoa possa ter baixado.

**"Quero desfazer o commit, mas manter o trabalho."**

```bash
git reset --soft HEAD~1     # desfaz o commit; tudo volta para a área de preparação
git reset HEAD~1            # desfaz o commit; tudo volta para o diretório de trabalho
git reset --hard HEAD~1     # desfaz o commit E apaga as mudanças — o perigoso
```

**"Preciso desfazer um commit que já está no GitHub."** Use `git revert a3f9c21`. O `revert` **não apaga** nada: cria um commit novo que desfaz o que aquele commit fez. É o único método seguro quando o histórico já é público, porque não reescreve nada que alguém já baixou — e `--amend` e `reset` reescrevem.

> **⚠️ Atenção**
> `git reset --hard` e `git restore` sem nada preparado são as duas únicas formas comuns de perder trabalho de verdade com Git. Antes de qualquer um dos dois, rode `git status` e leia a lista do que vai sumir. Se estiver em dúvida, `git stash` (§10.1) guarda tudo sem apagar.

## 7. Branches, merge e conflitos

### 7.1 Criar e trocar

```bash
git switch -c menu-responsivo    # cria a branch e já muda para ela
git switch main                  # volta para main
git branch -a                    # lista as branches locais (* na atual) e as remotas
git branch -d menu-responsivo    # apaga (só se já foi mesclada; -D força)
```

O comando antigo para isso era `git checkout -b`; ele continua funcionando, mas `git switch` existe justamente porque `checkout` fazia coisas demais e confundia. Use `switch` para branches e `restore` para arquivos.

Regra de ouro do WebLab: **`main` sempre funciona**. Toda mudança nasce em uma branch com nome descritivo (`menu-responsivo`, `validacao-inscricao`, `corrige-contraste`) e só volta para `main` quando está pronta.

### 7.2 Mesclar

Estando em `main`:

```bash
git switch main
git merge menu-responsivo
git merge --no-ff menu-responsivo   # força sempre um commit de mesclagem
```

Dois desfechos possíveis. No **fast-forward**, se `main` não recebeu nenhum commit desde que a branch nasceu, o Git apenas move o ponteiro de `main` para frente, sem criar commit novo. No **commit de mesclagem**, quando as duas branches evoluíram, o Git cria um commit com **dois pais** — é o `9c1d2e4` do grafo da §4.3. O `--no-ff` força o segundo caso mesmo quando o primeiro seria possível, e o histórico fica mais legível: cada funcionalidade vira um "nó" visível no grafo.

### 7.3 Conflitos

Um conflito acontece quando as duas branches mudaram **as mesmas linhas** do mesmo arquivo. O Git não adivinha qual está certa e para:

```text
Auto-merging index.html
CONFLICT (content): Merge conflict in index.html
Automatic merge failed; fix conflicts and then commit the result.
```

Abra o arquivo. O Git escreveu marcadores nele:

```html
<h1>
<<<<<<< HEAD
  Semana Acadêmica de Sistemas de Informação
=======
  Semana Acadêmica de Sistemas de Informação — 12ª edição
>>>>>>> menu-responsivo
</h1>
```

Leia assim: entre `<<<<<<< HEAD` e `=======` está a versão da branch em que você está; entre `=======` e `>>>>>>>` está a versão da branch que você está trazendo.

Resolver é editar o trecho à mão até ficar como deve ficar — pode ser uma das duas, ou uma terceira redação — e **apagar as três linhas de marcador**. Depois:

```bash
git diff --name-only --diff-filter=U   # lista só os arquivos ainda em conflito
git add index.html
git commit              # sem -m: o Git já sugere a mensagem de mesclagem
git merge --abort       # alternativa: desiste e volta ao estado anterior
```

Quando um arquivo inteiro deve vir de um lado só, `git checkout --ours index.html` aceita a versão da branch atual e `--theirs` a que está chegando. O VS Code também mostra os conflitos com botões (**Accept Current Change**, **Accept Incoming Change**, **Accept Both Changes**); use-os, mas leia o resultado: aceitar "both" com frequência gera HTML duplicado.

> **🧠 Você sabia?**
> Conflito não é erro, e não é sinal de que alguém fez algo errado. É o Git avisando que uma decisão humana é necessária. Times grandes tratam a **frequência** de conflitos como métrica de organização: muitos conflitos indicam branches que vivem tempo demais separadas. A receita é a mesma em qualquer time: branches curtas, mescladas em dias e não em semanas, e `git pull` no começo de cada sessão de trabalho.

## 8. GitHub e o `gh`

### 8.1 Git não é GitHub

**Git** é o programa que roda na sua máquina e guarda o histórico. **GitHub** é um site que hospeda repositórios Git e acrescenta o que o Git não tem: interface web, controle de acesso, issues, pull requests, ações automatizadas e páginas publicadas. Existem concorrentes (GitLab, Bitbucket, Codeberg) com as mesmas ideias. Você pode usar Git sem GitHub a vida toda, mas não pode publicar um site, colaborar ou entregar um link sem um servidor remoto.

Crie sua conta em <https://github.com> usando o **mesmo e-mail** do `git config user.email`. Escolha um nome de usuário que você mostraria a um empregador: ele vai virar parte da URL de todos os seus projetos e, no Capítulo 03, do endereço do seu site (`ana-souza.github.io`).

Enquanto estiver lá, ative a **autenticação em duas etapas** — o GitHub a exige de quem contribui com código.

### 8.2 O GitHub CLI

O `gh` é o cliente oficial de linha de comando. Ele resolve a autenticação e permite criar repositórios, abrir pull requests e revisar código sem sair do terminal.

Instalação:

```bash
sudo apt install gh                  # Ubuntu/Debian
brew install gh                      # macOS, com Homebrew
winget install --id GitHub.cli       # Windows, em um PowerShell
```

Se o `apt` da sua distribuição trouxer uma versão antiga, use o repositório oficial descrito em <https://github.com/cli/cli/blob/trunk/docs/install_linux.md>.

Conferir e autenticar com `gh --version` e `gh auth login`. O login faz quatro perguntas no terminal:

1. **What account do you want to log into?** → `GitHub.com`
2. **What is your preferred protocol for Git operations?** → `HTTPS` (mais simples; a §8.3 mostra a alternativa)
3. **Authenticate Git with your GitHub credentials?** → `Yes` (o `gh` passa a responder pelo `git push`, sem pedir senha)
4. **How would you like to authenticate?** → `Login with a web browser` — o terminal mostra um código de oito caracteres, você o cola na página que abrir e autoriza.

Confira com `gh auth status`. Saída esperada: `✓ Logged in to github.com account ana-souza (keyring)` e a lista de escopos.

> **💡 Dica**
> Em uma máquina de laboratório, **nunca** deixe sua sessão do `gh` aberta. Faça `gh auth logout` ao terminar, ou use `gh auth login` com o navegador em janela anônima. O token guardado dá acesso de escrita a todos os seus repositórios.

### 8.3 SSH, se você preferir

Com HTTPS + `gh`, o push já funciona sem senha. Se quiser chaves SSH (útil quando você também acessa um servidor, como no Capítulo 06), gere a chave aceitando o caminho padrão `~/.ssh/id_ed25519`, envie a pública e teste:

```bash
ssh-keygen -t ed25519 -C "ana.souza@gmail.com"
gh ssh-key add ~/.ssh/id_ed25519.pub --title "Notebook da Ana"
ssh -T git@github.com
```

Resposta esperada: `Hi ana-souza! You've successfully authenticated, but GitHub does not provide shell access.` Isso não é erro — o GitHub só aceita Git, não sessão de terminal.

### 8.4 Criar o repositório remoto e publicar

Dentro da pasta que já é um repositório local:

```bash
gh repo create site-evento --public --source=. --remote=origin --push
```

O `--public` deixa o repositório visível para qualquer pessoa (`--private` faz o contrário), `--source=.` usa o repositório Git da pasta atual em vez de criar um vazio, `--remote=origin` cadastra a URL remota com o apelido `origin` e `--push` já envia a branch atual.

Sem o `gh`, você cria o repositório vazio pela interface web e liga os dois no terminal:

```bash
git remote add origin https://github.com/ana-souza/site-evento.git
git remote -v
git push -u origin main
```

O `-u` (de *upstream*) liga a branch local `main` à remota `origin/main`. Depois disso, `git push` e `git pull` sem argumentos já sabem para onde ir. Para abrir o repositório no navegador, `gh repo view --web`; em outra máquina, `gh repo clone ana-souza/site-evento` (ou `git clone <url>`) traz o histórico inteiro, e não só os arquivos — por isso `git log` funciona imediatamente na máquina nova, sem internet.

## 9. Pull request: a conversa sobre o código

### 9.1 O que é

Um **pull request** (PR) é um pedido: "revisem estas mudanças e, se estiverem boas, coloquem na `main`". Ele mostra o diff, permite comentários linha a linha, roda verificações automáticas (Capítulo 09) e registra a decisão.

Em um projeto de uma pessoa, o PR parece burocracia — mas é justamente aí que ele ensina: você se obriga a reler o próprio diff antes de mesclar, e o número de bugs bobos cai. Em dupla, ele é o único jeito civilizado de trabalhar. O ciclo completo:

```text
main ──●──────────────────────────────●── (merge do PR)
        \ ●───────●───────●──────────/     branch da tarefa
       commit  commit  push      revisão
```

### 9.2 Abrindo o PR

```bash
git switch -c menu-responsivo
git add css/estilo.css js/script.js index.html
git commit -m "Adiciona menu hamburguer responsivo abaixo de 768px"
git push -u origin menu-responsivo
gh pr create --base main --head menu-responsivo \
  --title "Menu responsivo com botão hambúrguer" \
  --body "Abaixo de 768px o menu vira um botão. Fecha ao clicar em um link e ao apertar Esc. Testado no modo dispositivo do DevTools em 375px e 768px."
```

Três opções que valem conhecer: `--fill` usa a mensagem do commit como título e corpo, `--draft` abre como rascunho (ninguém revisa ainda) e `--web` abre o formulário no navegador. O `gh` imprime a URL do PR — guarde-a: é o link que você compartilha quando a entrega envolve revisão.

### 9.3 Revisando

```bash
gh pr list                          # PRs abertos no repositório
gh pr view 1                        # descrição, autor, estado
gh pr diff 1                        # o diff completo, no terminal
gh pr checkout 1                    # baixa a branch do PR para testar na sua máquina
gh pr checks 1                      # resultado das verificações automáticas
gh pr review 1 --comment --body "O botão precisa de aria-expanded."
gh pr review 1 --approve
gh pr review 1 --request-changes --body "O menu não fecha com Esc."
```

Uma revisão útil olha quatro coisas, nesta ordem: **funciona?** (baixe a branch e teste), **está claro?** (nomes, indentação), **quebra algo?** (links, outras páginas), **falta alguma coisa?** (acessibilidade, tratamento de erro, `alt` nas imagens).

> **⚠️ Atenção**
> O GitHub **não deixa você aprovar o seu próprio pull request**. Se tentar, o `gh` responde `Can not approve your own pull request`. Isso não impede o merge em um repositório pessoal — apenas o carimbo de aprovação. Nos trabalhos em dupla, cada um aprova o PR do outro.

### 9.4 Mesclando

```bash
gh pr merge 1 --squash --delete-branch
```

Três estratégias, e quando usar cada uma:

| Estratégia | O que faz | Quando usar |
|---|---|---|
| `--merge` | Cria um commit de mesclagem, preserva todos os commits da branch | Quando o histórico da branch conta uma história útil |
| `--squash` | Junta todos os commits da branch em **um só** na `main` | O padrão do WebLab: `main` fica com um commit por funcionalidade |
| `--rebase` | Reaplica os commits da branch por cima da `main`, sem commit de mesclagem | Histórico linear, em times que exigem isso |

Depois do merge, atualize sua máquina com `git switch main` e `git pull`. O `--delete-branch` do `gh` apaga as **duas** cópias da branch — a do GitHub e a da sua máquina —, então não sobra nada para um `git branch -d` apagar depois. Se você mesclar pelo site, sem o `--delete-branch`, aí sim: `git push origin --delete menu-responsivo` remove a remota e `git branch -d menu-responsivo` remove a local.

### 9.5 Proteção de branch

No repositório do GitHub, em **Settings → Branches → Add branch ruleset**, você exige que a `main` só receba código por PR e só depois de uma aprovação — é o que impede o `git push` direto no dia do prazo. No Capítulo 09, essa mesma tela passa a exigir que os testes automáticos passem antes do merge.

## 10. Stash, tags e o que mais você vai usar

### 10.1 `git stash`: guardar sem commitar

Você está no meio de uma alteração e precisa trocar de branch agora (o colega achou um bug em produção). Commitar pela metade polui o histórico; perder o trabalho, nem pensar:

```bash
git stash push -u -m "menu pela metade"   # -u inclui arquivos não rastreados
git switch main
git switch menu-responsivo      # depois de resolver o urgente e commitar
git stash list                  # stash@{0}: On menu-responsivo: menu pela metade
git stash pop                   # devolve as mudanças e remove da pilha
```

Na pilha também valem `git stash apply stash@{0}` (devolve mantendo o item), `git stash show -p stash@{0}` (mostra o diff guardado), `git stash drop` (descarta um) e `git stash clear` (esvazia tudo).

### 10.2 Tags: marcar versões

Uma tag é um nome fixo para um commit. Serve para marcar entregas:

```bash
git tag -a v1.0.0 -m "Marco 1: cinco páginas em HTML"
git push origin v1.0.0   # tags não sobem no push comum; --tags envia todas
```

O `git tag -l` lista as existentes. O `-a` cria uma **tag anotada**, que guarda autor, data e mensagem — é a que se usa em entregas. Sem `-a`, a tag é apenas um apelido do hash. No GitHub, uma tag pode virar uma **release**, com notas e arquivos anexados:

```bash
gh release create v1.0.0 --title "Marco 1 — site do evento" \
  --notes "Cinco páginas em HTML semântico, menu de navegação e formulário de inscrição."
```

### 10.3 Comandos de resgate

```bash
git reflog                      # todo movimento do HEAD, inclusive o que "sumiu"
git blame css/estilo.css        # quem escreveu cada linha e em qual commit
git bisect start                # busca binária pelo commit que introduziu um bug
git clean -n                    # lista arquivos não rastreados que seriam apagados (-fd apaga)
```

O `git reflog` é a rede de segurança: mesmo depois de um `git reset --hard` infeliz, o commit antigo continua listado lá por semanas, e `git switch -c recuperado <hash>` traz tudo de volta.

## 11. Trabalhando em dupla

O trabalho em dupla (nesta trilha ou em qualquer projeto real) segue sempre o mesmo ciclo:

1. **Antes de começar a trabalhar**, atualize: `git switch main && git pull`.
2. **Crie uma branch por tarefa** (`git switch -c inscricao-validacao`) e faça **commits pequenos e frequentes**, um assunto por commit.
3. **Publique cedo**: `git push -u origin inscricao-validacao` já no primeiro commit, mesmo inacabado (`gh pr create --draft`). O colega vê que você está mexendo ali.
4. **Abra o PR**, peça revisão e responda aos comentários com novos commits — o PR se atualiza sozinho a cada push.
5. **Merge com squash**, apague a branch, volte para a `main` e dê `git pull`.

Duas situações inevitáveis:

**A `main` andou enquanto você trabalhava.** Traga as novidades para a sua branch antes de pedir o merge, resolvendo os conflitos ali e não na `main`:

```bash
git switch main && git pull
git switch inscricao-validacao
git merge main
```

**O push foi recusado.**

```text
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/ana-souza/site-evento.git'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

Significa que o remoto tem commits que você não tem. A resposta certa é `git pull` (que mescla) e depois `git push`. A resposta errada é `git push --force`, que **apaga o trabalho do colega** no servidor.

Combine com a dupla, no primeiro dia: quem mexe em qual arquivo (um no HTML das páginas, outro no CSS, por exemplo), que a `main` é intocável e só recebe merge de PR, e que ninguém dá `--force` em branch compartilhada.

> **🔬 Investigue**
> Simule uma dupla sozinho, em duas pastas. Clone o mesmo repositório duas vezes: `git clone <url> copia-a` e `git clone <url> copia-b`. Em `copia-a`, mude o `<h1>` do `index.html`, commite e dê push. Em `copia-b`, **sem dar pull**, mude a **mesma linha**, commite e tente o push. Leia a mensagem de rejeição inteira. Agora rode `git pull` em `copia-b`: o conflito aparece. Resolva, commite e dê push. Volte em `copia-a` e rode `git pull` para ver o resultado final. Você acabou de viver, em dez minutos, o ciclo que trava a maioria dos trabalhos em grupo.

## 🚀 Passo a passo — O site do evento versionado, no GitHub e com um PR mesclado

Ao fim destes passos, `site-evento` é um repositório Git com histórico legível, existe em `https://github.com/<seu-usuario>/site-evento`, tem `README.md`, `.gitignore` e `.gitattributes`, e uma funcionalidade nova entrou na `main` por um pull request revisado e mesclado. Faça na ordem.

### Passo 1 — Configurar o Git e iniciar o repositório

Rode os seis `git config --global` da §3 (no Windows, `core.autocrlf true`) e confira com `git config --list --show-origin`. Depois:

```bash
cd ~/weblab/site-evento
git init
git add .
git status -s
git commit -m "Estrutura inicial do site do evento com as cinco páginas"
git log --oneline
```

Esperado: uma linha, com o hash curto e a mensagem.

### Passo 2 — `.gitignore`, `.gitattributes` e `README.md`

Crie os três arquivos na raiz com o conteúdo das §5.1, §5.3 e §5.2 (adaptando o README ao seu projeto e ao seu nome). Depois commite e teste se o `.gitignore` está valendo:

```bash
git add .gitignore .gitattributes README.md
git commit -m "Adiciona README, .gitignore e .gitattributes"
mkdir -p node_modules && touch node_modules/teste.js .env
git status -s
rm -rf node_modules .env
```

Esperado: o `git status -s` **não** menciona `node_modules` nem `.env`.

### Passo 3 — Autenticar o `gh` e publicar

Instale o GitHub CLI conforme a §8.2 e autentique-se, respondendo `GitHub.com`, `HTTPS`, `Yes` e `Login with a web browser`:

```bash
gh --version
gh auth login
gh auth status
gh repo create site-evento --public --source=. --remote=origin --push
git remote -v
gh repo view --web
```

Esperado: o navegador abre o repositório com os arquivos e o README renderizado.

### Passo 4 — Branch com a funcionalidade nova

Crie a branch com `git switch -c menu-responsivo` e acrescente o botão ao menu de `index.html`, dentro do `<header>`, antes da lista de links:

`index.html`

```html
<header class="cabecalho">
  <a class="logo" href="index.html">Semana Acadêmica</a>
  <button class="botao-menu" id="botaoMenu" aria-expanded="false"
          aria-controls="menuPrincipal" aria-label="Abrir menu de navegação">☰</button>
  <nav>
    <ul class="menu" id="menuPrincipal">
      <li><a href="index.html">Início</a></li>
      <li><a href="programacao.html">Programação</a></li>
      <li><a href="palestrantes.html">Palestrantes</a></li>
      <li><a href="inscricao.html">Inscrição</a></li>
      <li><a href="contato.html">Contato</a></li>
    </ul>
  </nav>
</header>
```

`css/estilo.css` (acrescente ao fim do arquivo)

```css
/* Menu responsivo: o botão só aparece em telas estreitas */
.botao-menu {
  display: none;
  font-size: 1.5rem;
  background: none;
  border: 0;
  color: inherit;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
}

@media (max-width: 768px) {
  .botao-menu { display: block; }
  .menu {
    display: none;
    flex-direction: column;
    width: 100%;
    gap: 0.5rem;
    padding: 1rem 0;
  }
  .menu.aberto { display: flex; }
}
```

`js/script.js` (acrescente ao fim do arquivo)

```js
// Menu responsivo: abre e fecha a lista de links em telas estreitas
const botaoMenu = document.querySelector('#botaoMenu')
const menuPrincipal = document.querySelector('#menuPrincipal')

function definirEstado(aberto) {
  menuPrincipal.classList.toggle('aberto', aberto)
  botaoMenu.setAttribute('aria-expanded', String(aberto))
  botaoMenu.setAttribute('aria-label', aberto ? 'Fechar menu de navegação' : 'Abrir menu de navegação')
}

botaoMenu.addEventListener('click', () => definirEstado(!menuPrincipal.classList.contains('aberto')))
menuPrincipal.addEventListener('click', (evento) => {
  if (evento.target.tagName === 'A') definirEstado(false)
})
document.addEventListener('keydown', (evento) => {
  if (evento.key === 'Escape') definirEstado(false)
})
```

Teste no navegador (Live Server + modo dispositivo em 375 px) e commite:

```bash
git add index.html css/estilo.css js/script.js
git commit -m "Adiciona menu hamburguer responsivo abaixo de 768px"
git push -u origin menu-responsivo
```

### Passo 5 — Abrir e revisar o pull request

```bash
gh pr create --base main --head menu-responsivo \
  --title "Menu responsivo com botão hambúrguer" \
  --body "Abaixo de 768px o menu vira um botão com aria-expanded. Fecha ao clicar em um link e com Esc. Testado no modo dispositivo em 375px e 768px."
gh pr list
gh pr diff
gh pr review --comment --body "Diff conferido: aria-expanded muda junto com a classe, e o Esc fecha. Aprovado para merge."
```

Se você estiver em dupla, quem **não** abriu o PR roda `gh pr checkout <numero>`, testa no navegador e depois `gh pr review <numero> --approve`.

### Passo 6 — Mesclar, limpar e marcar a entrega

```bash
gh pr merge --squash --delete-branch
git switch main
git pull
git log --oneline --graph --decorate --all
git tag -a v1.0.0 -m "Site do evento com as cinco páginas e menu responsivo"
git push origin v1.0.0
gh release create v1.0.0 --title "v1.0.0 — site do evento" \
  --notes "Cinco páginas em HTML semântico, CSS com menu responsivo e navegação por teclado."
gh repo view --web
```

Esperado: o histórico da `main` mostra três commits, o último com a mensagem do PR, e a release aparece na lateral da página do repositório.

### Como conferir

| Comando ou ação | Resultado esperado |
|---|---|
| `git log --oneline` | Pelo menos três commits com mensagens no imperativo |
| `git status` | `nothing to commit, working tree clean` |
| `git status -s` após criar `.env` | Nenhuma linha para `.env` (está ignorado) |
| `git remote -v` | `origin` com a URL do seu repositório, em `fetch` e `push` |
| `gh pr list --state merged` | O PR do menu, com estado `MERGED` |
| `git branch -a` | Só `main` local e `remotes/origin/main` |
| `git show v1.0.0 --stat` e a página do repositório | O commit marcado com a lista de arquivos; README renderizado e a release na lateral |

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Um arquivo aparece em `git status` sob **Changes not staged for commit**. Em qual das três áreas ele está? E se aparecer sob **Changes to be committed**? E sob **Untracked files**?

**A2.** Preveja a saída. Você editou `index.html` e `css/estilo.css`, rodou `git add index.html` e em seguida `git diff` e `git diff --staged`. Qual arquivo aparece em cada um dos dois comandos, e por quê?

**A3.** Para cada situação, diga qual comando usar: (a) descartar uma edição não commitada; (b) tirar um arquivo da área de preparação; (c) corrigir a mensagem do último commit local; (d) desfazer um commit que já está no GitHub; (e) guardar o trabalho pela metade para trocar de branch.

**A4.** Você acrescentou `node_modules/` ao `.gitignore`, mas a pasta continua aparecendo em `git status`. Explique por quê e escreva a sequência de comandos que resolve sem apagar a pasta do disco.

**A5.** Um `index.html` em conflito tem `<<<<<<< HEAD`, `<h1>Semana Acadêmica</h1>`, `=======`, `<h1>Semana Acadêmica de Sistemas de Informação</h1>` e `>>>>>>> titulo-longo`, nesta ordem. Diga qual versão pertence a qual branch, e o que precisa ser feito no arquivo antes do `git add`.

**A6.** Qual a diferença entre `git fetch` e `git pull`? E entre `gh pr merge --squash` e `gh pr merge --merge`, do ponto de vista do que aparece em `git log --oneline` da `main`?

### Nível B — Aplicação

**B1.** Histórico limpo em três commits. Comece de uma pasta nova (`git init`), com um `index.html` de esqueleto. Faça exatamente três commits, nesta ordem: um só com o esqueleto HTML, um só com o CSS ligado por `<link>`, e um só com o `<script>` e o `script.js`. As três mensagens devem estar no imperativo e ter menos de 60 caracteres.

Resultado esperado: `git log --oneline` mostra três linhas; `git show --stat` de cada commit lista apenas os arquivos daquele assunto (nenhum commit toca em arquivo de outro assunto).

<details><summary>Dica</summary>

Faça a edição, `git add` **só do arquivo daquele assunto** e `git commit`. Se você editar tudo antes, ainda dá certo: use `git add <arquivo>` seletivamente, ou `git add -p` para escolher trecho por trecho dentro do mesmo arquivo.
</details>

**B2.** Conflito provocado e resolvido. No `site-evento`, crie duas branches a partir da `main`: `titulo-curto` e `titulo-longo`. Em cada uma, altere **a mesma linha** do `<h1>` do `index.html` e commite. Volte para a `main`, mescle a primeira (vai passar), e mescle a segunda (vai dar conflito). Resolva escolhendo uma terceira redação, diferente das duas.

Resultado esperado: `git log --oneline --graph --all` mostra o desenho com as duas branches e o commit de mesclagem; o `index.html` final tem a terceira redação e nenhum marcador `<<<<<<<`.

<details><summary>Dica</summary>

`git diff --name-only --diff-filter=U` lista os arquivos que ainda estão em conflito. Depois de editar, `git add` marca como resolvido, e `git commit` sem `-m` aceita a mensagem que o Git já preparou. Se quiser desistir no meio, `git merge --abort`.
</details>

**B3.** Arqueologia do repositório. Escolha um repositório público conhecido (por exemplo <https://github.com/vuejs/core>), clone-o e responda, **só pelo terminal**: quantos commits ele tem; quem são os cinco maiores autores por número de commits; qual foi o primeiro commit (hash, data e mensagem); qual arquivo tem mais commits no histórico.

Resultado esperado: um `arqueologia.md` com as quatro respostas e o comando exato usado em cada uma.

<details><summary>Dica</summary>

`git rev-list --count HEAD` conta commits. `git shortlog -sn | head -5` ranqueia autores. `git log --reverse --oneline | head -1` acha o primeiro. Para o arquivo mais commitado, combine `git log --name-only --pretty=format:` com `sort | uniq -c | sort -rn | head`.
</details>

**B4.** Fluxo completo em dupla. Com um colega (ou com duas cópias clonadas, como na §11): a pessoa A adiciona o repositório à conta dela e convida a B em **Settings → Collaborators**. Cada uma cria uma branch, faz uma alteração em página diferente, abre um PR e **revisa e aprova o PR da outra**. Ao final, as duas alterações estão na `main`.

Resultado esperado: dois PRs mesclados, cada um com uma revisão de aprovação de outra pessoa; `git log --oneline` na `main` mostra as duas funcionalidades.

<details><summary>Dica</summary>

`gh pr checkout <numero>` baixa a branch do PR para testar antes de aprovar. Lembre que ninguém aprova o próprio PR — se aparecer `Can not approve your own pull request`, você está tentando revisar o seu.
</details>

### Nível C — Desafio

**C1.** Resgate depois do desastre. Prepare o cenário: em um repositório de teste com cinco commits, rode `git reset --hard HEAD~3`. Os três últimos commits sumiram do `git log`. Recupere-os sem clonar de novo e sem usar o GitHub, deixando a `main` exatamente como estava antes. Depois, repita o desastre de outra forma: crie uma branch `experimento`, commite algo nela, volte para a `main` e apague a branch com `git branch -D experimento`. Recupere o commit perdido.

<details><summary>Dica</summary>

`git reflog` lista todo movimento do `HEAD`, incluindo os commits que nenhuma branch aponta mais. A partir de um hash de lá, `git reset --hard <hash>` devolve a `main` ao ponto certo, e `git switch -c recuperado <hash>` cria uma branch nova sobre um commit órfão. Objetos órfãos são apagados de verdade só quando o `git gc` roda, semanas depois.
</details>

## 🏆 Desafios

### ⭐ O que o `.git` guarda
Tags: git, terminal, investigacao

O `git status` diz que a pasta está limpa, mas a `.git` tem centenas de arquivos. O que exatamente está lá dentro, e por que um repositório com 20 commits de um site de 200 KB pode ocupar menos espaço do que os próprios arquivos? Hoje você abre a caixa preta.

**Critérios de pronto**

- Um `relatorio-git.md` com o tamanho de `.git` (`du -sh .git`) e o número de arquivos, medidos depois de 3, 10 e 20 commits no `site-evento`.
- A saída de `cat .git/HEAD` e de `cat .git/refs/heads/main`, com uma frase explicando o que cada uma significa, e o conteúdo do último commit lido diretamente do banco de objetos, com o comando usado.
- Três linhas explicando por que copiar a pasta do projeto **sem** a `.git` entrega os arquivos mas destrói o histórico.

<details><summary>Pistas</summary>

1. `git cat-file -t <hash>` diz o tipo de um objeto (`commit`, `tree`, `blob`); `git cat-file -p <hash>` mostra o conteúdo.
2. O hash do último commit está em `.git/refs/heads/main`. Passe-o para o `cat-file -p` e siga o campo `tree`.
3. `git count-objects -vH` resume quantos objetos existem e quanto ocupam, soltos e empacotados.
4. Rode `git gc` e meça de novo: o Git compacta os objetos soltos em um *packfile* e guarda apenas as diferenças entre versões parecidas.
</details>

### ⭐⭐ Um histórico que conta a história
Tags: git, github, refatoracao

Pegue o repositório mais bagunçado que você tem (aquele com commits chamados "alteracoes", "update2" e "agora vai") e transforme-o em um repositório que você mostraria numa entrevista. O objetivo não é maquiar: é aprender a escrever o histórico enquanto trabalha, praticando em um caso ruim.

**Critérios de pronto**

- Um repositório novo no GitHub, público, com o mesmo conteúdo final e um histórico de **pelo menos 8 commits**, cada um com um assunto único e mensagem no formato Conventional Commits.
- `README.md` completo: o que é, como rodar, estrutura de pastas, estado atual em checklist e autoria.
- `.gitignore` e `.gitattributes` adequados ao tipo de projeto.
- Pelo menos uma branch mesclada por pull request, com descrição de três linhas explicando a mudança.
- Uma tag anotada `v1.0.0`, uma release com notas e um parágrafo no README dizendo o que você faria diferente desde o começo.

<details><summary>Pistas</summary>

1. Não tente reescrever o histórico antigo. Comece um repositório limpo e reconstrua o projeto em etapas, commitando cada etapa — é mais rápido e ensina mais.
2. `git add -p` permite preparar só parte de um arquivo, o que é o que torna possível separar assuntos que você fez juntos.
3. Para o PR, escolha uma melhoria real que ainda falta (acessibilidade, responsividade, tratamento de erro) em vez de inventar uma mudança cosmética.
4. `gh repo view --web` e leia a sua própria página como se fosse outra pessoa: dá para rodar o projeto só com o que está escrito ali?
</details>

### ⭐⭐⭐ Caçada ao commit culpado
Tags: git, bug, investigacao

Um site que funcionava parou de funcionar, e ninguém sabe quando. Em vez de ler cinquenta commits, o Git faz uma busca binária: você diz um ponto bom e um ruim, e ele te leva ao commit exato em oito passos. Hoje você planta o bug, esquece onde ele está e usa o `git bisect` para achá-lo.

**Critérios de pronto**

- Um repositório com **no mínimo 20 commits** no `site-evento` (ou no seu projeto autoral), com mudanças reais e pequenas.
- Um bug plantado em algum commit do meio, que quebre algo verificável por um comando (por exemplo, um seletor de CSS renomeado que faz o menu sumir, ou uma chamada a uma função que não existe).
- Um script `verificar.sh` que sai com código 0 quando o site está bom e diferente de 0 quando está quebrado.
- A sessão completa de `git bisect run ./verificar.sh` colada em um `caca.md`, mostrando quantos passos foram necessários e qual commit foi apontado.
- Uma comparação escrita: quantos commits você teria conferido na mão (busca linear) e quantos o `bisect` conferiu; a explicação do porquê da diferença.
- O bug corrigido por um `git revert` do commit culpado, e não por uma edição manual.
- Este tipo de investigação é o que separa quem entende Git de quem só decora comandos — vale a pena incluir no seu projeto autoral.

<details><summary>Pistas</summary>

1. `git bisect start`, `git bisect bad` (no commit atual) e `git bisect good <hash-antigo>` iniciam a busca; o Git faz o checkout do meio e espera o seu veredicto.
2. `git bisect run <comando>` automatiza tudo: o Git roda o comando em cada passo e usa o código de saída como resposta.
3. Um `verificar.sh` simples pode ser um `grep -q '\.menu' css/estilo.css` — sai 0 se achar, 1 se não. Verificações mais sérias entram no Capítulo 10, com testes de verdade.
4. Com 20 commits, a busca linear conferiria até 20; a binária confere no máximo 5 (o log na base 2 de 20, arredondado para cima). Registre os dois números.
5. `git bisect reset` devolve você à branch de onde saiu — não esqueça, ou vai continuar em estado destacado.
</details>

### 🔥 Boss — A bancada inteira, versionada e publicada
Tags: git, github, terminal, projeto

Este é o Boss da Unidade 1: ele junta tudo o que os Capítulos 01 e 02 ensinaram. A ideia é simples de enunciar e trabalhosa de executar bem: **uma máquina nova deve ficar pronta para trabalhar rodando um comando do seu repositório.** Ambiente, configurações, projeto e histórico, tudo versionado e reproduzível.

**Critérios de pronto**

- Um repositório público `bancada` no GitHub contendo: `extensoes.txt` do VS Code, `settings.json`, `.prettierrc`, `.editorconfig`, `.gitconfig` de exemplo (sem o seu e-mail real) e um `instalar.sh`.
- `bash instalar.sh` em uma máquina limpa (ou em um usuário novo do seu sistema) instala as extensões, copia as configurações para o caminho certo do sistema detectado e aplica os `git config --global` da §3. Rodar duas vezes não dá erro nem duplica nada.
- Um `novo-projeto.sh` que cria um projeto do zero (pastas, `index.html` com `lang="pt-BR"` e viewport, `css/`, `js/`, `.gitignore`, `.editorconfig`, `README.md`), roda `git init`, faz o primeiro commit e cria o repositório remoto com `gh repo create`, tudo em um comando.
- O histórico do `bancada` tem no mínimo 6 commits com mensagens no imperativo, uma branch mesclada por pull request e uma tag anotada `v1.0.0`.
- O `README.md` documenta cada script, mostra a saída esperada, traz uma seção "Testado em" com pelo menos dois sistemas (ou dois usuários da mesma máquina) e três capturas mostrando a máquina limpa antes e depois.
- Um colega clona o seu `bancada`, roda os scripts e confirma no `README.md` (por pull request) que funcionou na máquina dele.

<details><summary>Pistas</summary>

1. `case "$(uname -s)" in Linux*) … ;; Darwin*) … ;; MINGW*|MSYS*) … ;; esac` detecta o sistema; os caminhos do `settings.json` estão no desafio de dotfiles do Capítulo 01.
2. Idempotência vem de `mkdir -p`, `cp -f` e de checar antes de agir: `git config --global --get user.name` devolve vazio quando a chave não existe.
3. `gh repo create "$1" --public --source=. --remote=origin --push` fecha o `novo-projeto.sh` — mas confira antes se `gh auth status` está autenticado, e avise com uma mensagem clara se não estiver.
4. Para o teste "máquina limpa" sem formatar nada, crie um usuário novo no sistema (`sudo adduser teste`) e rode os scripts lá dentro.
5. O pull request do colega é a prova de que o processo funciona fora da sua cabeça — é exatamente para isso que a revisão existe.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `fatal: not a git repository (or any of the parent directories): .git` | Você está fora da pasta do projeto, ou nunca rodou `git init` | `pwd` para conferir, `cd` para a pasta certa; se for projeto novo, `git init` |
| `Author identity unknown *** Please tell me who you are.` | `user.name`/`user.email` não configurados | Rode os dois `git config --global` da §3 e repita o commit |
| `error: failed to push some refs to '…' hint: Updates were rejected because the remote contains work that you do not have locally` | O remoto tem commits que você não baixou | `git pull` (resolva conflitos se houver) e depois `git push`; nunca `--force` em branch compartilhada |
| `fatal: refusing to merge unrelated histories` | Repositório local e remoto começaram separados (você criou o repo no site com README e também deu `git init` local) | `git pull origin main --allow-unrelated-histories`, resolva os conflitos e commite |
| `CONFLICT (content): Merge conflict in index.html` | As duas branches mudaram as mesmas linhas | Edite o arquivo, apague os marcadores, `git add` e `git commit`; para desistir, `git merge --abort` |
| `error: Your local changes to the following files would be overwritten by checkout` | Você tenta trocar de branch com edições não commitadas em arquivos que mudam entre as branches | `git stash push -m "wip"`, troque de branch, `git stash pop`; ou commite antes |
| `Can not approve your own pull request` | Você tentou `gh pr review --approve` no seu próprio PR | Peça a revisão ao colega; em repositório pessoal, mescle sem aprovação |
| `warning: LF will be replaced by CRLF in index.html` | Fim de linha diferente entre o sistema e o repositório | Não é erro; configure `core.autocrlf` (§3) e adicione o `.gitattributes` da §5.3 |
| `fatal: The current branch menu-responsivo has no upstream branch` | Primeiro push de uma branch nova, sem `-u` | `git push -u origin menu-responsivo` |
| `node_modules` aparece em `git status` mesmo com a linha no `.gitignore` | A pasta já estava rastreada antes da regra | `git rm -r --cached node_modules` e commite; o `.gitignore` passa a valer |

## 🏠 Para praticar depois da aula (1 h)

Leve o seu **projeto autoral** (o site com o tema que você escolheu na sua trilha) para o GitHub, com histórico decente:

1. Rode `git init` na pasta do projeto autoral e crie `.gitignore`, `.gitattributes` e `README.md` (com as seções: o que é, como rodar, estrutura, estado atual em checklist e autoria).
2. Faça **no mínimo quatro commits** separados por assunto, com mensagens no imperativo e menos de 60 caracteres cada.
3. Publique com `gh repo create <nome> --public --source=. --remote=origin --push`.
4. Crie a branch `melhoria-<algo>`, faça uma melhoria real (acessibilidade, responsividade, um texto que estava faltando), commite, dê push e abra um pull request com descrição de três linhas explicando **o que** mudou e **por quê**.
5. Mescle o PR com `--squash --delete-branch`, volte para a `main`, dê `git pull` e crie a tag anotada `v0.1.0`.

**Critério de pronto:** `git log --oneline` na `main` mostra cinco ou mais commits com mensagens legíveis; o repositório é público; o README aparece renderizado na página; existe um PR com estado `MERGED`; a tag `v0.1.0` está no GitHub; `git status` diz `working tree clean`.

**Guarde no seu repositório:** o link do repositório público e o link do pull request mesclado. Nada de `.zip` daqui em diante.

## ✅ Está no ar quando…

- [ ] `git log --oneline --graph --decorate --all` no `site-evento` mostra um histórico com pelo menos três commits e o traço da branch mesclada.
- [ ] `git status` responde `nothing to commit, working tree clean`.
- [ ] `https://github.com/<seu-usuario>/site-evento` abre, é público e mostra o `README.md` renderizado.
- [ ] Criar um arquivo `.env` na pasta **não** faz nada aparecer em `git status`.
- [ ] `gh pr list --state merged` lista o pull request do menu responsivo.
- [ ] `git branch -a` mostra só `main` e `remotes/origin/main` — as branches de tarefa foram apagadas depois do merge.
- [ ] A tag `v1.0.0` existe local (`git tag -l`) e no GitHub (na lateral da página do repositório).
- [ ] Você explica, sem consultar, a diferença entre `git restore`, `git reset` e `git revert`, e sabe o que fazer quando aparece `CONFLICT (content): Merge conflict in …`.

## 📚 Para aprofundar

- Pro Git, de Scott Chacon e Ben Straub — <https://git-scm.com/book/pt-br/v2> — livro oficial, gratuito e em português. Leia os capítulos 2 (Fundamentos) e 3 (Ramificação), que cobrem tudo deste capítulo com mais profundidade.
- Documentação de referência do Git — <https://git-scm.com/docs> — a página de cada comando; comece por `git-status`, `git-switch` e `git-restore`. GitHub Docs em português — <https://docs.github.com/pt> — contas, repositórios, colaboração e a seção "Sobre pull requests".
- GitHub Skills — <https://skills.github.com> — cursos interativos curtos, feitos dentro de repositórios reais; o "Introduction to GitHub" leva menos de uma hora.
- Manual do GitHub CLI — <https://cli.github.com/manual/> — todos os comandos do `gh`, com exemplos por subcomando.
- Learn Git Branching — <https://learngitbranching.js.org/?locale=pt_BR> — visualizador interativo de branches, merge e rebase; o melhor lugar para "ver" o grafo se formando.
- Conventional Commits — <https://www.conventionalcommits.org/pt-br/> — a especificação do formato de mensagens usado na §4.2.
- Documentação do `.gitignore` — <https://git-scm.com/docs/gitignore> — e a coleção de modelos por linguagem em <https://github.com/github/gitignore>.
- MILETTO, Evandro M.; BERTAGNOLLI, Silvia C. *Desenvolvimento de software II*. Bookman — capítulo sobre gerência de configuração e controle de versão.

No próximo capítulo, esse repositório deixa de ser só um backup: o GitHub Pages e a Netlify passam a servir o `site-evento` e o Café Cerrado em endereços públicos, e você descobre por que um `href="/css/estilo.css"` que funciona na sua máquina quebra no ar.
