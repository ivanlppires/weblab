# Capítulo 01 — Caixa de ferramentas do dev web

> **Deploy & Ferramentas** · Unidade 1: Ferramentas e versionamento
> WebLab · UNEMAT — Campus Sinop
> **Tempo estimado:** 2 a 3 h · estudo autônomo, em paralelo à sua trilha

## 🎯 Objetivos de aprendizagem

Ao final deste capítulo você será capaz de:

- Navegar, criar pastas e ler arquivos pelo terminal (`pwd`, `ls`, `cd`, `mkdir`, `cat`, `code .`) em Linux, macOS e Windows, sabendo qual shell está usando.
- Configurar o VS Code com as extensões recomendadas nesta trilha e um `settings.json` que formata o código ao salvar.
- Usar as abas Elements, Console, Network e Lighthouse do DevTools, e o modo de dispositivo, para inspecionar qualquer página da Web.
- Instalar o Node.js LTS por um gerenciador de versões (nvm no Linux/macOS, nvm-windows no Windows) e explicar por que isso é melhor do que o instalador comum.
- Ler um `package.json` e usar `npm init`, `npm install`, `npm run` e `npx` com segurança.
- Conferir versões (`node -v`, `npm -v`, `git --version`, `npm ls`) e diagnosticar um ambiente quebrado.
- Padronizar indentação, codificação e fim de linha em qualquer editor com um `.editorconfig`.

## 📋 Pré-requisitos

- [ ] Um computador em que você possa instalar programas (Linux, macOS ou Windows 10/11).
- [ ] Cerca de 2 GB livres em disco e acesso à internet.
- [ ] Uma conta de e-mail que você acesse — vai servir para o GitHub no Capítulo 02.

> Este é o primeiro capítulo da trilha Deploy & Ferramentas; não há capítulo anterior para retomar. Se você está no **Nível 1**, faça-o antes ou junto com a Aula 02 — tudo aqui usa só HTML, CSS e o navegador. Se está no **Nível 2 ou 3**, use-o como revisão do ambiente: é comum descobrir que o `node -v` da máquina é de dois anos atrás. Hoje você monta a bancada de trabalho; no Capítulo 02, aprende a guardar o histórico dela com Git.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 40 min | Terminal (qual usar, comandos de navegação) e VS Code (extensões, `settings.json`, atalhos, `.editorconfig`) |
| 2 | 50 min | DevTools na prática; Node.js LTS via nvm; npm, `npx` e a anatomia do `package.json` |
| 3 | 60 min | Passo a passo: ambiente pronto e um projeto de teste rodando no Live Server; Laboratório |

## 1. Por que uma caixa de ferramentas

Um site é só um conjunto de arquivos de texto. Dá para escrever HTML no Bloco de Notas e abrir com dois cliques — e nas primeiras aulas do Nível 1 isso basta. O problema aparece na terceira semana: você tem cinco páginas, uma pasta de imagens, um CSS que não recarrega, um colega que quer ver o site na máquina dele e, no fim do semestre, precisa publicar tudo em um endereço público.

Cada ferramenta deste capítulo resolve uma dor específica:

| Ferramenta | Dor que resolve |
|---|---|
| Terminal | Criar, mover e inspecionar arquivos sem clicar; rodar programas (Git, npm, Vite) que não têm janela |
| VS Code + extensões | Escrever código com destaque de sintaxe, autocompletar, formatação automática e servidor local |
| DevTools | Enxergar o que o navegador fez com o seu HTML/CSS/JS — e por que não fez o que você esperava |
| Node.js + npm | Rodar JavaScript fora do navegador e instalar as ferramentas do ofício (Prettier, ESLint, Vite, Express) |
| `.editorconfig` | Garantir que o código fique igual no seu editor e no de qualquer outra pessoa que abrir o projeto |

Você não precisa dominar tudo hoje. Precisa **instalar tudo hoje**, entender para que serve cada peça e saber onde conferir se está funcionando. É o que a maioria dos "não roda na minha máquina" do semestre tem em comum: uma peça faltando na bancada.

> **🧠 Você sabia?**
> O `bash`, terminal padrão da maioria das distribuições Linux, é mais velho que a Web. Foi escrito por Brian Fox para o projeto GNU, e o nome é um trocadilho: *Bourne Again SHell*, em homenagem ao `sh` de Stephen Bourne, que ele substituiu. Os comandos `ls`, `cd` e `cat` que você vai usar hoje são os mesmos que um programador usava em um terminal de texto verde décadas antes de existir navegador.

## 2. O terminal

### 2.1 Qual terminal usar

O terminal é um programa que recebe comandos digitados e mostra o resultado em texto. O que interpreta os comandos se chama **shell**, e há vários. Para que os comandos deste material funcionem iguais em todas as máquinas, a recomendação é:

| Sistema | Terminal recomendado | Como abrir |
|---|---|---|
| Linux (Ubuntu, Mint, Fedora) | `bash` (já vem instalado) | <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>T</kbd> ou "Terminal" no menu |
| macOS | Terminal.app (shell `zsh`, compatível com tudo daqui) | <kbd>Cmd</kbd>+<kbd>Espaço</kbd>, digite "Terminal" |
| Windows | **Git Bash** (instalado junto com o Git for Windows) | Menu Iniciar → "Git Bash" |

No Windows existe também o **PowerShell**, que aceita `ls`, `cd`, `pwd`, `cat` e `mkdir` como apelidos de comandos próprios — mas sem as opções do Linux (`ls -la` dá erro lá) e sem `touch`. Para não ter dois conjuntos de comandos na cabeça, use o Git Bash ao longo de toda esta trilha. Você instala o Git for Windows no passo a passo deste capítulo e ganha os dois de uma vez: o `git` e um shell compatível com Linux.

> **💡 Dica**
> Quem usa Windows e quer um Linux "de verdade" dentro do Windows pode instalar o **WSL** (`wsl --install` em um PowerShell como administrador). Não é obrigatório para nada do WebLab; o Git Bash resolve tudo do que precisamos.

Para descobrir qual shell está rodando:

```bash
echo $SHELL
```

Saída típica: `/bin/bash` (Linux, Git Bash) ou `/bin/zsh` (macOS).

### 2.2 Onde estou, o que tem aqui, para onde vou

Todo terminal está sempre "dentro" de uma pasta, chamada **diretório de trabalho**. Três comandos resolvem 80 % da navegação:

```bash
pwd          # print working directory: mostra em que pasta você está
ls           # lista o conteúdo da pasta atual
cd Documentos  # change directory: entra na pasta Documentos
```

Variações de `ls` que você vai usar todo dia:

```bash
ls -l        # formato longo: permissões, dono, tamanho, data de cada item
ls -a        # inclui arquivos ocultos (os que começam com ponto, como .gitignore)
ls -la       # os dois juntos — o mais usado
ls css       # lista o conteúdo de uma subpasta sem entrar nela
```

Variações de `cd`:

```bash
cd ..        # sobe um nível (para a pasta "pai")
cd ../..     # sobe dois níveis
cd ~         # vai para a sua pasta pessoal (home)
cd           # o mesmo que cd ~
cd -         # volta para a pasta em que você estava antes
cd /         # vai para a raiz do sistema de arquivos
```

> **🔬 Investigue**
> Abra o terminal e rode `pwd`, depois `ls -la`. Quantos itens começam com ponto? Eles não aparecem no gerenciador de arquivos comum — são configurações de programas (`.bashrc`, `.config`, `.ssh`). Agora rode `cd /` e `ls`: você está vendo a raiz do sistema. Volte com `cd -`. Em nenhum momento você "quebrou" nada: navegar é só olhar.

### 2.3 Criando e lendo arquivos

```bash
mkdir projetos               # cria a pasta projetos
mkdir -p projetos/site/css   # cria a cadeia inteira de pastas de uma vez (-p = parents)
touch index.html             # cria um arquivo vazio (ou atualiza a data de um existente)
cat index.html               # mostra o conteúdo de um arquivo de texto na tela
cp index.html contato.html   # copia
mv contato.html paginas/     # move (ou renomeia, se o destino for um nome de arquivo)
rm rascunho.html             # apaga um arquivo — sem lixeira, sem desfazer
rm -r pasta-velha            # apaga uma pasta e tudo dentro dela — cuidado dobrado
clear                        # limpa a tela (ou Ctrl+L)
```

E o comando que você mais vai digitar neste semestre:

```bash
code .
```

Abre o VS Code **com a pasta atual como projeto**. O ponto significa "aqui". Abrir a pasta (e não um arquivo solto) é o que faz o Live Server, o Git e as extensões entenderem onde o projeto começa.

> **⚠️ Atenção**
> `rm` não pergunta e não tem lixeira. `rm -rf` com o caminho errado apaga pastas inteiras em silêncio. Antes de qualquer `rm -r`, rode `ls` no alvo para ter certeza do que vai sumir. E nunca copie um comando com `rm -rf` da internet sem entender cada parte dele.

### 2.4 Caminhos absolutos e relativos

Um **caminho absoluto** começa na raiz e não depende de onde você está: `/home/ana/projetos/site/index.html` (Linux), `/Users/ana/projetos/site/index.html` (macOS), `C:\Users\ana\projetos\site\index.html` (Windows — no Git Bash aparece como `/c/Users/ana/…`).

Um **caminho relativo** parte do diretório de trabalho: se você está em `projetos/site`, então `css/estilo.css` é o arquivo dentro da subpasta `css`, e `../outro-site` é a pasta irmã.

Essa distinção volta com força no Capítulo 03: um `href="/css/estilo.css"` (absoluto, começa com barra) funciona no seu computador e **quebra** quando o site é publicado em um subcaminho como `usuario.github.io/site-evento/`. Guarde a ideia: barra no início = "a partir da raiz".

### 2.5 Truques que economizam horas

- <kbd>Tab</kbd> completa nomes de arquivos e pastas. Digite `cd Doc` e aperte <kbd>Tab</kbd>: vira `cd Documentos/`. Dois <kbd>Tab</kbd> mostram as opções quando há mais de uma.
- <kbd>↑</kbd> e <kbd>↓</kbd> percorrem o histórico de comandos. `history` lista tudo.
- <kbd>Ctrl</kbd>+<kbd>C</kbd> interrompe o programa em execução (é assim que você para um servidor de desenvolvimento).
- <kbd>Ctrl</kbd>+<kbd>R</kbd> busca no histórico: digite parte de um comando antigo e ele aparece.
- Arraste uma pasta do gerenciador de arquivos para a janela do terminal: o caminho absoluto dela é colado.
- Nomes com espaço precisam de aspas ou barra invertida: `cd "Meus Projetos"` ou `cd Meus\ Projetos`. Melhor ainda: **não use espaços nem acentos** em nomes de pastas de projeto. `site-evento`, não `Site do Evento`.

## 3. VS Code

### 3.1 Instalação e o comando `code`

Baixe em <https://code.visualstudio.com> e instale. Três detalhes por sistema:

- **Windows:** no instalador, marque "Add to PATH" e as opções "Open with Code" no menu de contexto. Sem o PATH, `code .` não funciona no terminal.
- **macOS:** abra o VS Code, aperte <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> e execute **Shell Command: Install 'code' command in PATH**. Só assim `code .` funciona no Terminal.
- **Linux:** o pacote `.deb`/`.rpm` já registra o comando. Em distribuições com Snap, `sudo snap install code --classic`.

Teste:

```bash
code --version
```

A saída tem três linhas: a versão, um hash do build e a arquitetura (`x64` ou `arm64`).

### 3.2 Extensões recomendadas

Extensões são instaladas pela aba **Extensions** (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd>) ou pelo terminal, o que é mais rápido e reproduzível. O identificador de cada uma é `editor.nome`:

| Extensão | Identificador | Para que serve |
|---|---|---|
| Live Server | `ritwickdey.LiveServer` | Servidor local que recarrega o navegador a cada salvamento — Nível 1 inteiro |
| Prettier | `esbenp.prettier-vscode` | Formata HTML, CSS, JS, JSON e Vue com um padrão único |
| ESLint | `dbaeumer.vscode-eslint` | Aponta erros e maus hábitos no JavaScript enquanto você digita |
| Vue - Official | `Vue.volar` | Suporte a arquivos `.vue` (destaque, autocompletar, erros) — Nível 3 |
| REST Client | `humao.rest-client` | Testa APIs a partir de arquivos `.http` sem sair do editor — Níveis 2 e 3 |
| GitLens | `eamodio.gitlens` | Mostra quem mudou cada linha e quando; histórico visual — Capítulo 02 em diante |
| EditorConfig | `EditorConfig.EditorConfig` | Faz o editor obedecer ao `.editorconfig` do projeto |

Instalação de todas de uma vez:

```bash
code --install-extension ritwickdey.LiveServer
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint
code --install-extension Vue.volar
code --install-extension humao.rest-client
code --install-extension eamodio.gitlens
code --install-extension EditorConfig.EditorConfig
```

Para conferir o que está instalado:

```bash
code --list-extensions
```

> **💡 Dica**
> Prefere o VS Code em português? Instale `MS-CEINTL.vscode-language-pack-pt-BR`. Este material usa os nomes em inglês dos menus e abas (Settings, Extensions, Elements) porque é assim que aparecem na documentação oficial e nas respostas do Stack Overflow — vale a pena se acostumar com eles.

### 3.3 `settings.json`

As configurações do VS Code vivem em um arquivo JSON. Abra-o com <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → **Preferences: Open User Settings (JSON)**. Cole (ou mescle) isto:

`settings.json` (configurações do usuário)

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.wordWrap": "on",
  "editor.linkedEditing": true,
  "editor.bracketPairColorization.enabled": true,
  "files.eol": "\n",
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true,
  "emmet.variables": { "lang": "pt-BR" },
  "liveServer.settings.donotShowInfoMsg": true,
  "terminal.integrated.defaultProfile.windows": "Git Bash",
  "[markdown]": { "files.trimTrailingWhitespace": false }
}
```

O que cada linha faz:

- `editor.formatOnSave` + `editor.defaultFormatter`: ao salvar, o Prettier reorganiza indentação, aspas e quebras de linha. Você para de gastar atenção com estética e passa a gastar com lógica.
- `editor.tabSize: 2` + `insertSpaces`: dois espaços por nível, o padrão do ecossistema JavaScript/Vue.
- `editor.linkedEditing`: renomear a tag de abertura de um elemento HTML renomeia a de fechamento junto.
- `files.eol: "\n"`: fim de linha no padrão Unix. Evita o aviso `LF will be replaced by CRLF` do Git no Windows.
- `emmet.variables.lang`: o atalho `!` do Emmet passa a gerar `<html lang="pt-BR">` em vez de `en`.
- `terminal.integrated.defaultProfile.windows`: o terminal integrado do VS Code no Windows abre o Git Bash, não o PowerShell.

Há também configurações **por projeto**, em `.vscode/settings.json` dentro da pasta do projeto. Elas valem só ali e podem ser versionadas — útil para uma equipe usar o mesmo formatador.

### 3.4 Prettier: `.prettierrc`

O Prettier tem opiniões fortes e poucas opções. As que mudamos no WebLab ficam em um arquivo na raiz do projeto, e o estilo bate com o código que você vê nas aulas (sem ponto e vírgula, aspas simples):

`.prettierrc`

```json
{
  "semi": false,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "es5"
}
```

Sem esse arquivo, o Prettier usa os padrões dele (com ponto e vírgula e aspas duplas). Nenhum dos dois estilos é "errado" — o que importa é o projeto inteiro seguir um só.

### 3.5 `.editorconfig`

O `.prettierrc` fala com o Prettier; o `.editorconfig` fala com **qualquer editor** (VS Code, Sublime, IntelliJ, Vim). Ele define o básico da forma do arquivo — indentação, codificação, fim de linha — e é lido pela extensão EditorConfig. Coloque na raiz de todo projeto:

`.editorconfig`

```ini
# Configuração lida por qualquer editor com suporte a EditorConfig
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

`root = true` diz "pare de procurar `.editorconfig` nas pastas acima". A seção `[*]` vale para todo arquivo; a `[*.md]` abre uma exceção para Markdown, em que dois espaços no fim da linha significam quebra de linha.

### 3.6 Atalhos essenciais

No macOS, troque <kbd>Ctrl</kbd> por <kbd>Cmd</kbd> e <kbd>Alt</kbd> por <kbd>Option</kbd>.

| Atalho | O que faz | Quando usar |
|---|---|---|
| <kbd>Ctrl</kbd>+<kbd>P</kbd> | Abre um arquivo pelo nome | Projeto com muitas páginas |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> | Paleta de comandos | Qualquer ação do editor sem procurar no menu |
| <kbd>Ctrl</kbd>+<kbd>`</kbd> | Mostra/esconde o terminal integrado | O tempo todo |
| <kbd>Ctrl</kbd>+<kbd>B</kbd> | Mostra/esconde a barra lateral | Mais espaço para o código |
| <kbd>Ctrl</kbd>+<kbd>/</kbd> | Comenta/descomenta a linha ou seleção | Testar sem apagar |
| <kbd>Alt</kbd>+<kbd>↑</kbd> / <kbd>↓</kbd> | Move a linha atual | Reordenar regras CSS |
| <kbd>Shift</kbd>+<kbd>Alt</kbd>+<kbd>↓</kbd> | Duplica a linha | Repetir um `<li>` |
| <kbd>Ctrl</kbd>+<kbd>D</kbd> | Seleciona a próxima ocorrência da palavra | Renomear várias de uma vez |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>L</kbd> | Seleciona todas as ocorrências | O mesmo, tudo de uma vez |
| <kbd>F2</kbd> | Renomeia o símbolo (variável, função) | Refatorar JavaScript |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>F</kbd> | Busca em todos os arquivos | Achar onde uma classe é usada |
| <kbd>Shift</kbd>+<kbd>Alt</kbd>+<kbd>F</kbd> | Formata o documento | Quando o formatOnSave não está ligado |
| <kbd>Ctrl</kbd>+<kbd>,</kbd> | Abre as configurações | Ajustar o editor |
| <kbd>Ctrl</kbd>+<kbd>K</kbd> <kbd>Ctrl</kbd>+<kbd>S</kbd> | Lista todos os atalhos | Aprender mais um por semana |

### 3.7 Emmet: HTML em uma linha

O VS Code traz o **Emmet** embutido: você digita uma abreviação e aperta <kbd>Tab</kbd>. Em um arquivo `.html`:

- `!` → esqueleto completo (`<!DOCTYPE html>`, `<html lang="pt-BR">`, `<meta viewport>`, `<title>`).
- `ul>li*3` → uma lista com três itens.
- `.card>h2+p` → uma `div.card` com um `h2` e um `p` dentro.
- `a[href="contato.html"]{Contato}` → um link com atributo e texto.
- `table>tr*3>td*2` → uma tabela 3×2.

Vale a pena passar dez minutos no *cheat sheet* oficial (<https://docs.emmet.io/cheat-sheet/>); as páginas do site do evento saem em metade do tempo.

## 4. DevTools: o raio-X do navegador

Todo navegador moderno traz ferramentas de desenvolvedor. Abra com <kbd>F12</kbd>, <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>I</kbd> ou botão direito → **Inspecionar** (no macOS, <kbd>Cmd</kbd>+<kbd>Option</kbd>+<kbd>I</kbd>). Os exemplos aqui são do Chrome; o Firefox tem as mesmas abas com nomes quase iguais.

### 4.1 Elements — o HTML como o navegador entendeu

A aba **Elements** mostra a **árvore DOM**: não o seu arquivo, mas o que o navegador construiu a partir dele (com tags que ele fechou por você, com o que o JavaScript inseriu). Ao clicar em um elemento:

- O painel **Styles** lista cada regra CSS que atinge o elemento, em ordem de prioridade, com as sobrescritas riscadas. É onde você descobre por que "meu CSS não aplica": outra regra mais específica venceu, ou o seletor não bate.
- Você pode **editar valores ao vivo** (clique em `16px` e digite `24px`) para experimentar sem tocar no arquivo. Nada disso é salvo — é rascunho.
- O painel **Computed** mostra o valor final de cada propriedade e o **diagrama de caixa** (margin, border, padding, conteúdo).
- A lupa no canto superior esquerdo (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>C</kbd>) seleciona um elemento clicando na página.

### 4.2 Console — o que o JavaScript tem a dizer

A aba **Console** mostra mensagens de `console.log`, avisos e **erros em vermelho** com o arquivo e a linha (`script.js:12`). Também é um interpretador: digite `document.title` e aperte <kbd>Enter</kbd>; digite `2 + 2`; digite `document.querySelectorAll('a').length` para contar os links da página. Nas aulas de JavaScript do Nível 1 você vai passar mais tempo aqui do que no editor.

### 4.3 Network — cada arquivo que a página pediu

A aba **Network** grava tudo o que o navegador baixou: HTML, CSS, imagens, fontes, scripts, chamadas a APIs. Para cada requisição: **Status** (200 ok, 404 não encontrado, 304 não mudou), **Type**, **Size** e **Time**. A linha do tempo à direita (o *waterfall*) mostra o que esperou por quem.

Três hábitos:

1. Abra o DevTools **antes** de recarregar (<kbd>F5</kbd>), senão a aba fica vazia.
2. Marque **Disable cache** enquanto desenvolve, para sempre ver a versão nova do CSS.
3. Use o seletor de velocidade (**No throttling** → **Slow 4G**) para sentir o site como quem está no 4G ruim do interior.

Na barra de baixo, o resumo: número de requisições, total transferido, tempo até `DOMContentLoaded` e até `Load`.

### 4.4 Device toolbar — o site no celular

<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> liga o **modo de dispositivo**: a página é renderizada nas dimensões de um celular ou tablet, com toque simulado. Escolha um aparelho na lista ou digite largura e altura. É a ferramenta central da aula de telas responsivas do Nível 1 — mas lembre que é uma simulação: fontes, desempenho e o teclado virtual só se veem em um celular de verdade.

### 4.5 Lighthouse — a nota do seu site

A aba **Lighthouse** roda uma auditoria automática e dá notas de 0 a 100 em quatro categorias: **Performance**, **Accessibility**, **Best Practices** e **SEO**. Escolha *Mobile*, clique em **Analyze page load** e espere um minuto. Cada item reprovado vem com explicação e link. É o critério objetivo de "site bom" usado nos checkpoints das trilhas: ≥ 90 em Performance e Accessibility.

### 4.6 Sources e Application — para depois

**Sources** permite colocar pontos de parada (*breakpoints*) no JavaScript e executar linha a linha — você vai usar nas aulas de funções e eventos. **Application** mostra `localStorage`, cookies e *service workers* — aparece no Nível 3, quando o UniEventos guarda inscrições no navegador.

> **🔬 Investigue**
> Abra <https://weblab.ivanpires.dev> com a aba Network aberta e **Disable cache** marcado. Recarregue. Anote: quantas requisições? Qual o maior arquivo (clique no cabeçalho **Size** para ordenar)? Quanto tempo até `DOMContentLoaded`? Agora mude para **Slow 4G** e recarregue de novo. O que mais demorou? Esse é o tipo de medição que você vai repetir no seu próprio site publicado, no Capítulo 03.

## 5. Node.js e npm

### 5.1 Por que um dev front-end precisa de Node

O **Node.js** roda JavaScript fora do navegador. Você só vai escrever servidores com ele no Nível 2 — mas precisa dele desde já porque **as ferramentas do ofício são escritas em JavaScript**: o Prettier que formata seu CSS, o ESLint que aponta erros, o Vite que empacota o Vue, o `serve` que sobe um servidor local. Todas são instaladas e executadas pelo **npm**, o gerenciador de pacotes que vem junto com o Node.

Pense no npm como uma loja de aplicativos para código: qualquer pessoa publica um pacote (uma pasta com JavaScript e um `package.json`), e qualquer projeto instala esse pacote com um comando. O registro público tem milhões de pacotes, do minúsculo ao gigantesco.

> **🧠 Você sabia?**
> Um pacote chamado `left-pad`, com 11 linhas que só adicionavam espaços à esquerda de um texto, era dependência indireta de milhares de projetos. Quando o autor o removeu do npm em uma disputa, builds do mundo inteiro quebraram na mesma tarde — e o npm mudou as regras para impedir a remoção de pacotes publicados. É a lição de que todo `npm install` é um ato de confiança em desconhecidos; o `package-lock.json`, que você vai ver adiante, existe para tornar essa confiança pelo menos reproduzível.

### 5.2 LTS e o gerenciador de versões

O Node tem duas linhas: **Current** (versões ímpares, novidades primeiro, suporte curto) e **LTS** (*Long Term Support* — versões pares, recebem correções por anos). Use sempre a **LTS**: hoje, a linha 22 (a 24 também é LTS e funciona). O `create-vue` do Nível 3 exige `^22.18.0 || >=24.12.0`, o que é mais um motivo para não ficar com um Node velho.

Há dois jeitos de instalar. O instalador de <https://nodejs.org> funciona, mas deixa uma versão única e fixa, e no Linux/macOS costuma exigir `sudo` para instalar pacotes globais. O jeito recomendado é um **gerenciador de versões**, que instala o Node na sua pasta pessoal (sem `sudo`) e permite ter várias versões lado a lado — o projeto antigo de um freela em Node 18, o projeto novo em Node 22.

**Linux e macOS — nvm.** Copie o comando de instalação da página oficial (<https://github.com/nvm-sh/nvm#installing-and-updating>); ele tem este formato, com a versão atual do nvm no meio da URL:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

Feche e abra o terminal (o instalador acrescenta linhas ao `~/.bashrc` ou `~/.zshrc`, que só são lidas em um terminal novo). Depois:

```bash
nvm install --lts          # baixa e instala a LTS mais recente
nvm use --lts              # ativa nesta sessão
nvm alias default 'lts/*'  # torna a LTS o padrão de todo terminal novo
nvm ls                     # lista as versões instaladas (a ativa tem ->)
node -v                    # v22.x.x (ou v24.x.x)
npm -v                     # 10.x.x ou 11.x.x
```

Para uma versão específica: `nvm install 22`, `nvm use 22`.

**Windows — nvm-windows.** É um projeto diferente, com comandos parecidos. Baixe o `nvm-setup.exe` em <https://github.com/coreybutler/nvm-windows/releases>, instale e abra um Git Bash **novo**:

```bash
nvm install lts    # instala a LTS mais recente
nvm list           # mostra o número exato da versão instalada
nvm use lts        # ativa (pode pedir um terminal como administrador)
node -v
npm -v
```

Se preferir não usar gerenciador no Windows, o instalador oficial também serve: `winget install OpenJS.NodeJS.LTS` em um PowerShell, ou o `.msi` do site. Você perde a troca de versões, mas ganha simplicidade.

### 5.3 npm: os quatro comandos

Entre em uma pasta de projeto e:

```bash
npm init -y
```

Cria um `package.json` com valores padrão (o `-y` aceita todas as perguntas). Em seguida:

```bash
npm install prettier --save-dev   # instala um pacote como dependência de desenvolvimento
npm install                       # instala tudo que o package.json lista (ao clonar um projeto)
npm run formatar                  # executa o script "formatar" definido em package.json
npx prettier --check .            # executa um pacote sem instalar globalmente
```

- `npm install <pacote>` (ou `npm i`) baixa o pacote para `node_modules/` e o registra em `dependencies`. Com `-D` (ou `--save-dev`), registra em `devDependencies` — coisas que só existem enquanto você desenvolve (formatador, empacotador, ferramentas de teste), e não no site final.
- `npm install` sem argumentos lê `package.json` e `package-lock.json` e recria `node_modules/` inteira. É o primeiro comando que você roda ao baixar qualquer projeto Node.
- `npm run <nome>` executa um comando definido em `scripts`. `npm run` sem nome lista os scripts disponíveis.
- `npx <comando>` procura o executável em `node_modules/.bin` do projeto; se não existir, baixa uma cópia temporária e pergunta se pode executar. É assim que você usa `npx create-vue@latest` sem instalar nada antes.

### 5.4 `package.json` explicado

Depois de `npm init -y`, `npm install -D prettier serve` e a edição dos scripts, o arquivo de um projeto de teste fica assim (a ordem dos campos e um ou outro campo extra variam com a versão do npm):

`package.json`

```json
{
  "name": "ola-weblab",
  "version": "1.0.0",
  "description": "Projeto de teste do ambiente WebLab",
  "scripts": {
    "dev": "serve . -l 3000",
    "formatar": "prettier --write .",
    "verificar": "prettier --check ."
  },
  "keywords": [],
  "author": "Seu Nome",
  "license": "MIT",
  "devDependencies": {
    "prettier": "^3.6.2",
    "serve": "^14.2.4"
  }
}
```

Campo a campo:

| Campo | Significado |
|---|---|
| `name`, `version` | Identidade do projeto. Só importam de verdade se você publicar um pacote no npm |
| `scripts` | Comandos com apelido. `npm run dev` executa `serve . -l 3000` |
| `dependencies` | Pacotes que o código final precisa para rodar (ex.: `express`, `vue`, `axios`) |
| `devDependencies` | Pacotes usados só durante o desenvolvimento (ex.: `prettier`, `vite`, `nodemon`) |
| `license` | Sob que termos outras pessoas podem usar seu código — voltamos a isso no Capítulo 02 |

O `^` antes da versão é **semver** (versionamento semântico): `^3.6.2` aceita qualquer `3.x.y` a partir de `3.6.2`, mas não `4.0.0`. O primeiro número muda quando há quebra de compatibilidade; o segundo, quando há funcionalidade nova; o terceiro, quando há correção.

> **🔎 Por baixo do capô**
> Ao rodar `npm install`, o npm lê `package.json`, resolve a árvore de dependências (cada pacote depende de outros, que dependem de outros), baixa tudo do registro para `node_modules/` e grava em `package-lock.json` a versão **exata** de cada pacote instalado. Os executáveis dos pacotes ganham um atalho em `node_modules/.bin/` — é por isso que `serve` funciona dentro de `scripts` sem caminho: o npm coloca essa pasta no `PATH` enquanto roda um script. E é por isso que `npx serve` acha o `serve` do projeto antes de pensar em baixar qualquer coisa.

### 5.5 `node_modules` e `package-lock.json`

Duas regras que evitam metade dos problemas de Git do semestre:

1. **`node_modules/` nunca vai para o Git nem para o `.zip`.** É regenerável com `npm install`, pesa dezenas ou centenas de megabytes e tem milhares de arquivos.
2. **`package-lock.json` sempre vai para o Git.** Ele garante que qualquer pessoa — um colega ou o servidor — instale exatamente as mesmas versões que você testou.

## 6. Gerenciando versões

Quando algo "não funciona", a primeira pergunta é: **qual versão?** Comandos de diagnóstico:

```bash
node -v              # versão do Node ativa
npm -v               # versão do npm
git --version        # versão do Git
nvm current          # qual Node o nvm ativou nesta sessão (Linux/macOS)
which node           # de onde o executável node está vindo
npm ls --depth=0     # pacotes instalados no projeto, sem as dependências das dependências
npm outdated         # o que tem versão nova disponível
npm view vite version  # última versão publicada de um pacote
```

Para fixar a versão do Node **por projeto**, crie um `.nvmrc` na raiz com o número da linha:

`.nvmrc`

```text
22
```

Quem entrar na pasta e rodar `nvm use` recebe a versão certa sem pensar. Muitos projetos também declaram o mesmo em `package.json`, no campo `engines`:

```json
{
  "engines": {
    "node": ">=22.18.0"
  }
}
```

> **⚠️ Atenção**
> Se `node -v` mostra uma versão diferente da que você acabou de instalar com o nvm, há dois Nodes na máquina: um do instalador antigo, outro do nvm. `which -a node` lista todos. Desinstale o antigo (ou deixe `nvm alias default` decidir) para não passar o semestre com um ambiente que muda a cada terminal.

## 🚀 Passo a passo — Ambiente pronto e um projeto de teste no Live Server

Ao fim destes passos, sua máquina responde a `node -v`, `npm -v` e `git --version`, o VS Code tem as extensões recomendadas, e um projeto mínimo abre no navegador pelo Live Server e recarrega sozinho ao salvar. Faça na ordem; cada passo tem um jeito de conferir.

### Passo 1 — Git (e o Git Bash, no Windows)

- **Windows:** baixe e instale o Git for Windows em <https://git-scm.com/download/win> (ou `winget install --id Git.Git -e --source winget` no PowerShell). Aceite os padrões; ele instala o **Git Bash**.
- **macOS:** no Terminal, `git --version`. Se não estiver instalado, o sistema oferece as *Command Line Tools*; aceite. Alternativa: `brew install git`.
- **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install git`.

Conferir (em um terminal novo):

```bash
git --version
```

Esperado: `git version 2.x.y`.

### Passo 2 — VS Code e o comando `code`

Instale conforme a §3.1 e, em um terminal novo:

```bash
code --version
```

Esperado: três linhas, começando pela versão. No Windows, use o Git Bash; no macOS, só funciona depois do **Shell Command: Install 'code' command in PATH**.

### Passo 3 — extensões

```bash
code --install-extension ritwickdey.LiveServer
code --install-extension esbenp.prettier-vscode
code --install-extension dbaeumer.vscode-eslint
code --install-extension Vue.volar
code --install-extension humao.rest-client
code --install-extension eamodio.gitlens
code --install-extension EditorConfig.EditorConfig
code --list-extensions
```

Esperado: a última linha lista as sete extensões.

### Passo 4 — `settings.json`

No VS Code, <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> → **Preferences: Open User Settings (JSON)** → cole o conteúdo da §3.3 → salve. Se o arquivo já tinha conteúdo, mescle dentro das mesmas chaves `{ }`.

### Passo 5 — Node.js LTS

Siga a §5.2 para o seu sistema. Conferir, em um terminal novo:

```bash
node -v
npm -v
npx -v
```

Esperado: `v22.x.x` (ou `v24.x.x`), `10.x.x` (ou `11.x.x`) e o mesmo número do npm.

### Passo 6 — a pasta de projetos e o projeto de teste

Crie uma pasta para todos os projetos do WebLab e, dentro dela, o projeto de teste:

```bash
mkdir -p ~/weblab/ola-weblab
cd ~/weblab/ola-weblab
mkdir css js
touch index.html css/estilo.css js/script.js
ls -R
```

Esperado:

```text
.:
css  index.html  js

./css:
estilo.css

./js:
script.js
```

Abra no VS Code:

```bash
code .
```

### Passo 7 — os três arquivos

`index.html` (digite `!` e <kbd>Tab</kbd> para o esqueleto, depois complete)

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Olá, WebLab</title>
    <link rel="stylesheet" href="css/estilo.css" />
  </head>
  <body>
    <main>
      <h1>Ambiente pronto</h1>
      <p>Se esta página recarregou sozinha quando você salvou, o Live Server está funcionando.</p>
      <p id="relogio">Carregando o relógio pelo JavaScript…</p>
    </main>
    <script src="js/script.js"></script>
  </body>
</html>
```

`css/estilo.css`

```css
/* Estilo mínimo só para provar que o CSS foi carregado */
body {
  font-family: system-ui, sans-serif;
  max-width: 40rem;
  margin: 2rem auto;
  padding: 0 1rem;
  background: #f5f5f0;
  color: #222;
}

h1 {
  color: #1b6b4a;
}
```

`js/script.js`

```js
// Mostra a hora atual e prova que o JavaScript foi carregado
const relogio = document.querySelector('#relogio')

function atualizarRelogio() {
  const agora = new Date()
  relogio.textContent = `Agora são ${agora.toLocaleTimeString('pt-BR')}`
}

atualizarRelogio()
setInterval(atualizarRelogio, 1000)

console.log('Ambiente WebLab: JavaScript carregado com sucesso')
```

### Passo 8 — Live Server

Com `index.html` aberto, clique em **Go Live** no canto inferior direito da janela (ou botão direito no arquivo → **Open with Live Server**). O navegador abre `http://127.0.0.1:5500/index.html`.

Mude o texto do `<h1>` e salve: a página recarrega sozinha. Abra o DevTools (<kbd>F12</kbd>) → **Console**: a mensagem `Ambiente WebLab: JavaScript carregado com sucesso` está lá. Aba **Network**, recarregue: quatro requisições (`index.html`, `estilo.css`, `script.js` e um `favicon.ico` com 404 — normal, ainda não há favicon; o Capítulo 03 resolve).

### Passo 9 — `npm init` e os arquivos de padronização

No terminal integrado do VS Code (<kbd>Ctrl</kbd>+<kbd>`</kbd>), dentro de `ola-weblab`:

```bash
npm init -y
npm install -D prettier serve
```

Crie `.prettierrc` e `.editorconfig` com o conteúdo das §3.4 e §3.5, e acrescente os scripts ao `package.json` até ele ficar como na §5.4. Depois:

```bash
npm run formatar
npm run dev
```

Esperado: o Prettier lista os arquivos formatados; o `serve` sobe em `http://localhost:3000` (é um segundo servidor local, sem recarga automática — serve para conferir que `npm run` funciona). Pare com <kbd>Ctrl</kbd>+<kbd>C</kbd>.

### Como conferir

| Comando ou ação | Resultado esperado |
|---|---|
| `node -v` · `npm -v` · `git --version` | `v22.x` (ou `v24.x`) · `10.x` (ou `11.x`) · `2.x` |
| `code --list-extensions` | As sete extensões da §3.2 |
| Salvar um arquivo mal indentado | O Prettier reorganiza na hora |
| **Go Live** | Página em `127.0.0.1:5500`, recarrega ao salvar |
| DevTools → Console | A mensagem do `console.log` |
| DevTools → Network | `estilo.css` e `script.js` com status 200 |
| `npm run` (sem nome) | Lista `dev`, `formatar` e `verificar` |
| `ls -a` | Mostra `.editorconfig`, `.prettierrc`, `node_modules`, `package.json`, `package-lock.json` |

## 🧪 Laboratório

### Nível A — Fixação

**A1.** Você está em `~/weblab/site-evento/css` e roda `cd ..` e depois `pwd`. O que aparece? E se em seguida rodar `cd ~` e `pwd`?

**A2.** Qual a diferença entre `npm install prettier` e `npm install -D prettier`? Em que campo do `package.json` cada um registra o pacote, e qual dos dois é o certo para um formatador?

**A3.** Preveja o que acontece ao rodar `npx serve .` em uma pasta que **não** tem o `serve` instalado nem localmente nem globalmente. O comando falha?

**A4.** Em uma pasta vazia, `mkdir -p projetos/site/css` cria quantas pastas? O que muda se `projetos` já existir? E o que acontece com `mkdir projetos/site/css` (sem `-p`) na pasta vazia?

**A5.** Para cada situação, diga qual aba do DevTools responde: (a) "por que o `color: red` não aplicou neste parágrafo?"; (b) "qual arquivo voltou com 404?"; (c) "o que meu `console.log` imprimiu?"; (d) "como o site fica em uma tela de 375 px?"; (e) "qual a nota de acessibilidade da página?".

**A6.** `node -v` e `nvm current` podem mostrar valores diferentes? Descreva uma situação em que isso acontece e como corrigir.

### Nível B — Aplicação

**B1.** Estrutura em um comando. Crie, com **um único** `mkdir` e **um único** `touch`, a estrutura do site do evento: `site-evento/index.html`, `programacao.html`, `inscricao.html`, `palestrantes.html`, `contato.html`, `css/estilo.css`, `js/script.js` e a pasta `img/` vazia. Mostre o resultado com `ls -R`.

Resultado esperado:

```text
site-evento:
contato.html  css  img  index.html  inscricao.html  js  palestrantes.html  programacao.html

site-evento/css:
estilo.css

site-evento/img:

site-evento/js:
script.js
```

<details><summary>Dica</summary>

O bash expande chaves: `mkdir -p site-evento/{css,js,img}` cria as três subpastas de uma vez, e `touch site-evento/{index,programacao,inscricao,palestrantes,contato}.html` cria os cinco HTML. Combine com os caminhos de `css/` e `js/` no mesmo `touch`.
</details>

**B2.** Formatação automática. Crie `js/bagunca.js` com exatamente este conteúdo, salve e observe o que o Prettier faz:

```js
const   produtos=[{nome:"Café",preco:5},{nome:"Pão de queijo",
preco:4}]
function total( lista ){let soma=0;for(const p of lista){soma+=p.preco};return soma}
console.log( total(produtos) );
```

Resultado esperado: ao salvar, o arquivo fica com dois espaços de indentação, aspas simples, sem ponto e vírgula, um item por linha no array e o `for` em várias linhas — sem você tocar em nada.

<details><summary>Dica</summary>

Se nada acontecer ao salvar, abra a paleta de comandos e execute **Format Document With…** → **Prettier**; se o Prettier não aparecer na lista, a extensão não está instalada. Se aparecer mas o resultado tiver ponto e vírgula, o `.prettierrc` não está na raiz da pasta aberta no VS Code.
</details>

**B3.** Caçador de requisições. Com a aba Network aberta e **Disable cache** marcado, carregue a página inicial de três sites: <https://weblab.ivanpires.dev>, o portal da UNEMAT e um site de notícias à sua escolha. Para cada um, registre: número de requisições, total transferido, maior arquivo (nome e tamanho) e tempo até `DOMContentLoaded`. Repita com **Slow 4G**.

Resultado esperado: uma tabela com três linhas e as medições nas duas velocidades, mais uma frase por site dizendo qual recurso mais atrasou o carregamento no 4G lento.

<details><summary>Dica</summary>

Os totais ficam na barra de status na parte de baixo da aba Network. Clique no cabeçalho **Size** para ordenar por tamanho e no **Waterfall** para ver quem esperou por quem. O seletor de velocidade fica ao lado de **Disable cache**.
</details>

**B4.** Scripts próprios. No projeto `ola-weblab`, acrescente ao `package.json` um script `abrir` que executa `code .`, e um script `limpar` que apaga `node_modules` (`rm -rf node_modules`). Rode `npm run limpar`, confira com `ls -a` que a pasta sumiu, e depois `npm install` para recriá-la.

Resultado esperado: `npm run` lista cinco scripts; depois de `npm install`, `npm ls --depth=0` volta a mostrar `prettier` e `serve` com as mesmas versões de antes (é o `package-lock.json` garantindo isso).

<details><summary>Dica</summary>

Scripts são strings de shell comuns. Compare a saída de `npm ls --depth=0` antes e depois: as versões batem porque o lock foi respeitado, não porque você teve sorte.
</details>

### Nível C — Desafio

**C1.** Gerador de projeto. Escreva um script `novo-projeto.sh` que receba um nome (`bash novo-projeto.sh cardapio`) e: recuse se a pasta já existir; crie a pasta com `index.html` (esqueleto completo com `lang="pt-BR"`, viewport e título igual ao nome), `css/estilo.css`, `js/script.js`, `.editorconfig` e `.prettierrc`; e termine abrindo o VS Code na pasta. Torne-o executável e use-o para criar a pasta do seu projeto autoral.

<details><summary>Dica</summary>

O primeiro argumento é `$1`. `if [ -d "$1" ]; then echo "já existe"; exit 1; fi` faz a recusa. Para gravar arquivos com várias linhas dentro do script, use um *heredoc*: `cat > "$1/index.html" <<'EOF'` seguido das linhas e de `EOF` sozinho em uma linha. `chmod +x novo-projeto.sh` dá permissão de execução.
</details>

## 🏆 Desafios

### ⭐ Quanto pesa uma dependência?
Tags: terminal, node, investigacao

Você instalou **um** pacote — `prettier` — e a pasta `node_modules` apareceu. Quantos arquivos ela tem? E se instalar `vite`? A resposta explica, melhor do que qualquer regra, por que `node_modules` nunca entra em um `.zip`, em um e-mail ou no Git.

**Critérios de pronto**

- Um arquivo `relatorio.md` com uma tabela: pacote instalado, número de arquivos em `node_modules`, tamanho em disco, número de pacotes em `package-lock.json`.
- Medições para três cenários: só `prettier`; `prettier` + `serve`; `prettier` + `serve` + `vite`.
- Os comandos exatos usados para contar e medir, colados no relatório.
- Três linhas explicando por que `package.json` + `package-lock.json` (alguns KB) substituem `node_modules` (dezenas de MB) na hora de compartilhar o projeto.

<details><summary>Pistas</summary>

1. `find node_modules -type f | wc -l` conta arquivos; `du -sh node_modules` mede o tamanho.
2. Para contar pacotes no lock, `grep -c '"node_modules/' package-lock.json` é uma aproximação boa.
3. `npm ls --depth=0` mostra só o que você pediu; `npm ls --all` mostra a árvore inteira — compare os dois tamanhos.
4. Apague e recrie com `rm -rf node_modules && npm install` para ver quanto tempo o npm leva; é o preço que o colega paga ao clonar seu projeto, e é baixo.
</details>

### ⭐⭐ Dotfiles: seu VS Code em um comando
Tags: terminal, projeto

Formatou o computador? Vai usar a máquina do laboratório? Profissionais guardam suas configurações em um repositório de **dotfiles** e reinstalam tudo com um script. Monte o seu: uma pasta `bancada` com um `instalar.sh` que, em uma máquina limpa, deixa o VS Code exatamente como o seu — extensões, `settings.json`, `.prettierrc` e `.editorconfig` padrão.

**Critérios de pronto**

- `extensoes.txt` gerado a partir do seu VS Code, um identificador por linha.
- `bash instalar.sh` instala todas as extensões da lista e copia o `settings.json` para o lugar certo **no sistema em que está rodando** (Linux, macOS ou Windows/Git Bash), sem perguntar nada.
- Rodar o script duas vezes seguidas não dá erro nem duplica nada.
- Testado na máquina de um colega (ou em um usuário novo do seu sistema), com o resultado de `code --list-extensions` colado no `README.md` da pasta.
- No Capítulo 02 você vai publicar essa pasta como o repositório `bancada` — é exatamente o material que o Boss daquele capítulo pede.

<details><summary>Pistas</summary>

1. `code --list-extensions > extensoes.txt` gera a lista; `xargs -L1 code --install-extension < extensoes.txt` instala linha a linha.
2. O `settings.json` do usuário fica em `~/.config/Code/User/` (Linux), `~/Library/Application Support/Code/User/` (macOS) e `$APPDATA/Code/User/` (Windows, no Git Bash). `uname -s` diz em qual sistema o script está.
3. Um `case "$(uname -s)" in Linux*) … ;; Darwin*) … ;; MINGW*|MSYS*) … ;; esac` escolhe o caminho.
4. `mkdir -p` antes de copiar e `cp -f` para sobrescrever tornam o script idempotente. Considere `ln -s` em vez de `cp`, para que editar o arquivo no VS Code atualize o repositório.
</details>

### ⭐⭐⭐ Detetive de performance
Tags: devtools, performance, investigacao

Por que um site de notícias demora oito segundos no 4G e o WebLab demora um? Hoje você deixa de adivinhar. Escolha três sites reais (um portal de notícias, uma loja online e um site de universidade), audite cada um no DevTools e escreva um laudo com a causa raiz da lentidão de cada um — e uma correção que você mesmo consegue demonstrar.

**Critérios de pronto**

- Para cada site: nota de Performance do Lighthouse (modo *Mobile*), total transferido, número de requisições e o recurso que mais bloqueou a renderização (com evidência da aba Network ou Performance).
- Percentual de JavaScript e CSS **não usados** na carga inicial, medido com a aba Coverage.
- Um laudo de uma página por site: o gargalo, por que ele acontece e uma correção concreta (formato de imagem, carregamento adiado, fonte, script de terceiros).
- Uma das correções demonstrada: salve a página (**Save as… → Webpage, Complete**), aplique a correção localmente (ex.: converta as imagens para WebP com <https://squoosh.app>) e mostre o antes e o depois com Network e Lighthouse.
- Este é o tipo de investigação que compõe bem o seu Marco de responsividade/performance, se você quiser incluí-la no projeto autoral.

<details><summary>Pistas</summary>

1. A aba Coverage abre pela paleta do DevTools (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> dentro do DevTools → "Show Coverage"); grave a carga e ordene por bytes não usados.
2. Na aba Network, filtre por **Img** e ordene por **Size**; imagens acima de 300 KB em uma página de notícias quase sempre são o primeiro gargalo.
3. A aba Performance grava um perfil: procure o marcador **LCP** (*Largest Contentful Paint*) e veja o que estava carregando antes dele.
4. O relatório do Lighthouse já lista "Eliminate render-blocking resources" e "Serve images in next-gen formats" com estimativa de ganho em segundos — use-a para priorizar a correção que vai demonstrar.
</details>

## 🐛 Erros comuns

| Sintoma | Causa | Solução |
|---|---|---|
| `bash: code: command not found` (ou `'code' não é reconhecido`) | O VS Code não está no PATH | macOS: paleta → **Shell Command: Install 'code' command in PATH**; Windows: reinstale marcando "Add to PATH"; sempre abra um terminal novo depois |
| `npm.ps1 cannot be loaded because running scripts is disabled on this system` | Política de execução do PowerShell bloqueia scripts | Use o Git Bash; ou, no PowerShell como administrador, `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `nvm: command not found` logo após instalar | O terminal atual não releu o `~/.bashrc`/`~/.zshrc` | Feche e abra o terminal (ou `source ~/.bashrc`); no macOS com zsh, confira se as linhas do nvm foram para `~/.zshrc` |
| `node -v` mostra uma versão antiga depois de `nvm install --lts` | Outro Node no PATH (instalador antigo) ou o alias `default` aponta para a versão velha | `which -a node` para achar o intruso; `nvm alias default 'lts/*'`; desinstale o Node antigo |
| `npm ERR! code EACCES` ao instalar pacote global | Node instalado com privilégios de administrador; `sudo npm` piora | Instale o Node pelo nvm (fica na sua pasta pessoal, sem `sudo`) |
| `npm ERR! enoent ENOENT: no such file or directory, open '…/package.json'` | Você rodou `npm install` ou `npm run` fora da pasta do projeto | `pwd` para conferir, `cd` para a pasta certa; se for um projeto novo, `npm init -y` primeiro |
| Live Server abre uma lista de arquivos ou `Cannot GET /` | Não há `index.html` na raiz da pasta aberta, ou você abriu um arquivo solto em vez da pasta | Feche tudo e abra a **pasta** com `code .`; garanta que `index.html` está na raiz |
| A página não recarrega ao salvar | Arquivo não salvo (bolinha na aba), ou a página foi aberta por dois cliques (`file://`) em vez do Go Live | Salve com <kbd>Ctrl</kbd>+<kbd>S</kbd>; confira que a URL começa com `http://127.0.0.1:5500` |
| `Get-ChildItem : A parameter cannot be found that matches parameter name 'la'` | `ls -la` no PowerShell, que só imita o `ls` do Linux | Use o Git Bash (ou `Get-ChildItem -Force` no PowerShell) |
| Prettier não formata ao salvar | `editor.defaultFormatter` não definido, ou outra extensão formata aquela linguagem | Paleta → **Format Document With…** → **Configure Default Formatter** → Prettier |
| `warning: LF will be replaced by CRLF` em todo `git add` (Windows) | Fim de linha do Windows (CRLF) em conflito com o do projeto (LF) | `files.eol: "\n"` no VS Code e `git config --global core.autocrlf true`; o Capítulo 02 explica |

## 🏠 Para praticar depois da aula (1 h)

Monte o ambiente completo e crie a pasta do seu **projeto autoral** (o site com o tema que você escolheu na sua trilha):

1. Siga o passo a passo até o fim; corrija qualquer item da tabela "Como conferir" que não bata.
2. Crie a pasta do projeto autoral em `~/weblab/<nome-do-projeto>` (sem espaços nem acentos) com `index.html`, `css/estilo.css`, `js/script.js`, `.editorconfig` e `.prettierrc`. O `index.html` deve ter `lang="pt-BR"`, viewport, um `<title>` com o nome do projeto e um `<h1>`.
3. Abra com o Live Server e deixe um `console.log` com o nome do projeto no `script.js`.
4. Tire três capturas de tela: (a) o terminal com a saída de `node -v`, `npm -v` e `git --version`; (b) o terminal com `code --list-extensions`; (c) o navegador com o site no Live Server e o DevTools aberto na aba Console mostrando a sua mensagem.

**Critério de pronto:** as três capturas mostram versões LTS do Node, as sete extensões e a mensagem no Console; a pasta do projeto tem os cinco arquivos e **não** contém `node_modules`.

**Guarde:** um `.zip` da pasta do projeto (sem `node_modules`) e as três capturas em um único PDF, num lugar seguro. A partir do Capítulo 02, isso vira o link do repositório no GitHub.

## ✅ Está no ar quando…

Nada vai ao ar neste capítulo — a bancada é que fica pronta. Confira:

- [ ] `node -v` imprime `v22.x.x` ou `v24.x.x`; `npm -v` imprime `10.x.x` ou superior; `git --version` imprime `2.x.y`.
- [ ] `code .` abre o VS Code na pasta atual, a partir do terminal recomendado para o seu sistema.
- [ ] `code --list-extensions` lista Live Server, Prettier, ESLint, Vue - Official, REST Client, GitLens e EditorConfig.
- [ ] Salvar um arquivo mal indentado o reformata (Prettier + `formatOnSave`).
- [ ] O Live Server serve o `index.html` em `127.0.0.1:5500` e recarrega ao salvar.
- [ ] Você encontra um `console.log` na aba Console e um 404 na aba Network sem ajuda.
- [ ] A pasta do projeto autoral existe, com `.editorconfig` e `.prettierrc` na raiz e sem `node_modules` no que será entregue.
- [ ] Você sabe explicar, em uma frase, a diferença entre `npm install`, `npm run` e `npx`.

## 📚 Para aprofundar

- VS Code — documentação oficial (introdução, terminal integrado, atalhos): <https://code.visualstudio.com/docs>
- VS Code — referência de atalhos em PDF (Linux, macOS, Windows): <https://code.visualstudio.com/docs/configure/keybindings>
- Emmet — cheat sheet oficial: <https://docs.emmet.io/cheat-sheet/>
- Chrome DevTools — guia oficial em português (Elements, Console, Network, Lighthouse): <https://developer.chrome.com/docs/devtools?hl=pt-br>
- Node.js — trilha "Aprenda" em português (o que é Node, como instalar, npm): <https://nodejs.org/pt/learn>
- nvm — instalação e uso: <https://github.com/nvm-sh/nvm#installing-and-updating>
- nvm-windows — releases e instruções: <https://github.com/coreybutler/nvm-windows>
- npm — documentação de `package.json` e dos comandos: <https://docs.npmjs.com/cli/v10/configuring-npm/package-json>
- Prettier — opções de configuração: <https://prettier.io/docs/options>
- EditorConfig — especificação e exemplos: <https://editorconfig.org>
- Pro Git (capítulo 1, "Começando", para chegar preparado ao Capítulo 02): <https://git-scm.com/book/pt-br/v2>

No próximo capítulo, a bancada ganha memória: Git para guardar cada versão do projeto e GitHub para publicá-lo, colaborar e abrir o seu primeiro pull request.
