Os desafios das aulas treinam um músculo de cada vez; os projetos desta página pedem o corpo inteiro. Cada um parte de um problema que existe fora da sala e exige que você modele os dados, implemente as regras e explique as decisões. Estão em ordem crescente de complexidade: os dez primeiros cabem em três arquivos (`index.html`, `style.css` e `script.js`), sem framework e sem back-end; os dois últimos são o passo seguinte, com API, login, banco, testes e deploy. Entregue sempre a versão mínima funcionando mais uma evolução da sua escolha, acompanhadas de uma demonstração de três minutos e de um texto curto explicando a estrutura do HTML, a estratégia de CSS e a lógica do JavaScript. A trilha sugerida diz a partir de qual aula você já tem o que precisa para começar.

### ⭐ Página de perfil profissional
Tags: html, css, flexbox, responsivo, projeto

**Trilha sugerida:** Nível 1 (a partir da aula 08) · **Tempo estimado:** 4–6 h

Um recrutador abre o link do seu perfil antes de abrir o currículo e decide em trinta segundos se continua lendo. Uma página de uma tela só, feita por você, diz mais do que dez linhas de "conhecimentos em HTML" num PDF. Construa a sua: quem você é, o que estuda, o que sabe fazer, o que já construiu e como falar com você. É o cartão de visitas que cresce junto com o curso — cada projeto desta lista vira um item novo na sua seção de projetos.

**Funcionalidades mínimas**

- Cabeçalho com foto (ou avatar), nome, curso e uma frase de apresentação.
- Seções de formação, habilidades (lista) e projetos, com pelo menos um card com link real (pode ser o site do evento da trilha).
- Contatos com links funcionais: e-mail, GitHub e LinkedIn; links externos abrem em nova aba.
- Navegação interna por âncoras entre as seções.
- Layout em Flexbox que vira uma coluna no celular.

**Critérios de pronto**

- HTML válido no validador do W3C, usando `header`, `nav`, `main`, `section` e `footer` (nenhum `div` fazendo papel de seção).
- Toda imagem tem `alt` descritivo; a foto de perfil tem `width` e `height` declarados.
- Abre em 360 px de largura sem rolagem horizontal e sem texto cortado.
- Contraste entre texto e fundo de pelo menos 4.5:1 (verifique no DevTools).
- Lighthouse Acessibilidade ≥ 90 e Performance ≥ 90 no modo celular.
- Publicado em URL pública (GitHub Pages ou Netlify; a aula 15 do Nível 1 e o capítulo 03 de Deploy ensinam como).

**Evolução (escolha pelo menos uma)**

- Alternância entre tema claro e escuro com um botão, guardando a preferência no `localStorage` (a partir da aula 13 do Nível 1) e respeitando `prefers-color-scheme` na primeira visita.
- Seção de projetos gerada a partir de um array de objetos em JavaScript, em vez de HTML fixo.
- Versão para impressão (`@media print`) que vira um currículo de uma página em PDF.

<details><summary>Pistas</summary>

1. Desenhe no papel antes de abrir o editor: três caixas (cabeçalho, conteúdo, rodapé) e o que entra em cada uma. A aula 05 do Nível 1 explica por que a estrutura vem antes do estilo.
2. Use `flex-direction: column` como padrão e mude para `row` a partir de 720 px com uma `@media`; celular primeiro dá menos código do que o contrário (aula 08).
3. Variáveis CSS (`--cor-fundo`, `--cor-texto`) no `:root` deixam o tema escuro da evolução em cinco linhas: basta trocar os valores dentro de um seletor `[data-tema="escuro"]`.
4. Para a preferência salva, `localStorage.setItem` e `getItem` guardam uma string; leia-a no início do script, antes de pintar a página, para não piscar o tema errado.
</details>

### ⭐ Cardápio digital de restaurante
Tags: html, css, grid, responsivo, projeto

**Trilha sugerida:** Nível 1 (a partir da aula 08; evolução a partir da aula 13) · **Tempo estimado:** 5–8 h

O QR code na mesa do restaurante abre um PDF de 8 MB que não cabe na tela do celular — você já passou por isso. O dono da lanchonete perto do campus sofre com o mesmo problema e não sabe que a solução são três arquivos. Monte um cardápio que carrega rápido, organiza os produtos por categoria e funciona com uma mão só, enquanto a outra segura o celular na fila.

**Funcionalidades mínimas**

- Pelo menos três categorias (lanches, bebidas, sobremesas), cada uma com título e pelo menos quatro produtos.
- Cada produto em um card com imagem, nome, descrição curta e preço em reais.
- Menu fixo no topo com links para cada categoria.
- Grade de cards com CSS Grid: uma coluna no celular, duas no tablet, três ou mais no desktop.
- Destaque visual para itens "do dia" ou "mais pedidos".

**Critérios de pronto**

- A grade se reorganiza de uma a três ou mais colunas conforme a largura da tela, sem quebrar os cards.
- Todas as imagens têm `alt`, `loading="lazy"` e dimensões declaradas; nenhuma passa de 200 KB.
- A página inteira pesa menos de 1 MB (aba Rede do DevTools) e abre em menos de 2 s com "3G rápido" simulado.
- Todos os preços aparecem com `R$` e duas casas decimais.
- Abre em 360 px sem rolagem horizontal; o menu do topo continua utilizável.
- Lighthouse Acessibilidade ≥ 90.

**Evolução (escolha pelo menos uma)**

- Busca por nome que filtra os cards enquanto você digita (aula 14 do Nível 1).
- Botões de categoria que mostram só os produtos daquela categoria, com o botão ativo destacado.
- Favoritos marcados com um ícone de coração e persistidos no `localStorage`.
- Modo "cozinha": versão de alto contraste com fonte maior, ativada por um botão.

<details><summary>Pistas</summary>

1. Escreva cada produto como um `article` dentro de uma `section` por categoria; a estrutura semântica é o que vai facilitar os filtros depois (aula 05 do Nível 1).
2. `grid-template-columns: repeat(auto-fill, minmax(240px, 1fr))` resolve a responsividade da grade sem uma única media query — leia sobre `auto-fill` e `auto-fit` na MDN (aula 08).
3. Para a busca, dê a cada card um atributo `data-nome` e compare com `includes()` em minúsculas; esconder é adicionar uma classe, não remover o elemento (aula 14).
4. Favoritos são só uma lista de ids: guarde-a como JSON no `localStorage` e, ao carregar a página, aplique a classe `favorito` nos cards cujo id está na lista.
</details>

### ⭐⭐ Lista de tarefas
Tags: javascript, dom, eventos, formularios, projeto

**Trilha sugerida:** Nível 1 (a partir da aula 14) ou Nível 2 (a partir da aula 07) · **Tempo estimado:** 6–8 h

Todo desenvolvedor já fez uma lista de tarefas, e é exatamente por isso que ela é um bom projeto: você vai comparar a sua com centenas de outras e descobrir o que separa uma lista de brinquedo de uma que você usaria de verdade. Ela parece trivial até você precisar decidir o que acontece com uma tarefa vazia, com duas iguais, com a página recarregada, com o Enter pressionado no lugar do clique.

**Funcionalidades mínimas**

- Formulário para adicionar tarefa com título obrigatório, por Enter ou por botão.
- Lista renderizada a partir de um array de objetos em JavaScript — nunca editando o HTML na mão.
- Marcar como concluída (com estilo diferente), editar o título e excluir.
- Contador de pendentes e botão para limpar as concluídas.
- Filtro: todas, pendentes e concluídas.

**Critérios de pronto**

- Enviar o formulário vazio ou só com espaços não cria tarefa e mostra uma mensagem na tela — sem `alert()`.
- Recarregar a página mantém todas as tarefas e o estado de cada uma (persistência em `localStorage`).
- A lista inteira é operável só pelo teclado: Tab alcança cada botão, Enter ou Espaço aciona, e o foco fica visível.
- Nenhum `id` duplicado no DOM; cada tarefa tem um identificador único que não é a posição no array.
- Console do DevTools sem erros ao adicionar, editar, concluir, filtrar e excluir.

**Evolução (escolha pelo menos uma)**

- Data limite com destaque para tarefas atrasadas.
- Arrastar e soltar para reordenar, com a API nativa de drag and drop.
- Etiquetas coloridas com filtro combinado ao filtro de estado.
- Desfazer a última exclusão por cinco segundos, como o Gmail faz.

<details><summary>Pistas</summary>

1. Comece pelo modelo, não pela tela: `{ id, titulo, concluida, criadaEm }`. Uma função `renderizar()` que esvazia a lista e desenha o array inteiro é mais simples do que atualizar item por item (aula 14 do Nível 1 ou aula 07 do Nível 2).
2. Um único ouvinte de clique na `ul`, lendo `event.target.closest('button')` e um atributo `data-acao`, substitui um ouvinte por botão — pesquise "event delegation" na MDN.
3. `crypto.randomUUID()` gera ids únicos sem biblioteca; `Date.now()` também serve enquanto ninguém cria duas tarefas no mesmo milissegundo.
4. `localStorage` só guarda strings: `JSON.stringify` ao salvar, `JSON.parse` ao carregar, com um `try/catch` para o caso de o conteúdo estar corrompido.
</details>

### ⭐⭐ Calculadora de notas acadêmicas
Tags: javascript, formularios, dom, projeto

**Trilha sugerida:** Nível 1 (a partir da aula 14) · **Tempo estimado:** 6–8 h

Fim de semestre, três notas lançadas no SIGAA e a mesma pergunta em todo grupo da turma: "quanto eu preciso tirar na última pra passar?". Responda de uma vez por todas com uma calculadora que o colega consegue usar no celular, no corredor, antes da prova. A conta é fácil; o difícil é não deixar ninguém digitar 15, deixar um campo em branco ou ler "aprovado" em verde quando a média foi 4,9.

**Funcionalidades mínimas**

- Campos numéricos para pelo menos três notas, com pesos configuráveis.
- Cálculo de média simples ou ponderada, conforme a escolha.
- Situação (aprovado, exame ou reprovado) com a regra e os limites visíveis na tela.
- "Quanto falta": a nota mínima necessária na próxima avaliação para atingir a média.
- Feedback por cor e por texto, nunca só por cor.

**Critérios de pronto**

- Notas fora do intervalo de 0 a 10, vazias ou não numéricas são rejeitadas com mensagem ao lado do campo, sem `alert()`.
- Pesos que não fecham 100 % (ou 10) geram aviso antes do cálculo.
- Resultado com uma casa decimal; 6,95 aparece como 7,0 e a situação corresponde ao valor mostrado (nada de arredondar para um lado e classificar pelo outro).
- Funciona com Tab e Enter; o resultado é anunciado pelo leitor de tela (região com `aria-live`).
- Lógica de cálculo em funções puras, testáveis no console: `media([7, 8, 9], [1, 1, 2])` devolve o valor sem tocar no DOM.

**Evolução (escolha pelo menos uma)**

- Várias disciplinas em uma tabela, com média por disciplina e resumo do semestre (quantas aprovadas, coeficiente médio).
- Disciplinas salvas no `localStorage` e resumo exportado em CSV.
- Gráfico de barras em CSS puro comparando as médias.
- Regras de aprovação selecionáveis (média 6,0 com exame, média 7,0 sem exame, outra combinação), definidas em um objeto de configuração.

<details><summary>Pistas</summary>

1. Separe em duas camadas desde o início: funções que calculam (recebem números, devolvem números) e funções que leem e escrevem na tela. É a aula 13 do Nível 1 aplicada.
2. `input.valueAsNumber` devolve `NaN` para campo vazio — use `Number.isNaN` na validação, e `min`, `max` e `step` no HTML como primeira linha de defesa (aula 03).
3. Para o "quanto falta", isole a incógnita na fórmula da média ponderada: nota necessária = (média alvo × soma dos pesos − pontos já obtidos) ÷ peso da próxima. Se der acima de 10, diga com todas as letras que não é mais possível.
4. Arredonde uma única vez, no fim, com `toFixed(1)`, e classifique usando o mesmo número arredondado que você mostra.
</details>

### ⭐⭐ Quiz de conhecimentos
Tags: javascript, dom, eventos, projeto

**Trilha sugerida:** Nível 2 (a partir da aula 08) · **Tempo estimado:** 8–10 h

Um quiz é um jogo de estado: qual pergunta está na tela, o que já foi respondido, quantos pontos, se acabou. Todo bug de quiz ("a pergunta 3 apareceu duas vezes", "o botão continuou clicável depois da resposta") é um estado que alguém esqueceu de controlar. Faça um quiz sobre o tema que quiser — a disciplina, o Pantanal, futebol — e aprenda a pensar a interface como uma função do estado.

**Funcionalidades mínimas**

- Pelo menos dez perguntas de múltipla escolha em um array de objetos (enunciado, alternativas, índice da correta, explicação).
- Uma pergunta por vez, com indicador de progresso ("3 de 10").
- Ao responder, marca certo ou errado, mostra a explicação e trava as alternativas até "Próxima".
- Tela final com pontuação, percentual e botão para recomeçar.
- Estado da aplicação em um único objeto `estado`, nunca espalhado em variáveis soltas.

**Critérios de pronto**

- Depois de responder, clicar em outra alternativa não muda nada (verificável na tela e no console).
- Recomeçar zera tudo, inclusive o progresso e as perguntas já vistas, sem recarregar a página.
- Cada pergunta aparece exatamente uma vez por rodada.
- As alternativas são `button` de verdade, focáveis e acionáveis por teclado; a resposta correta não é identificável no HTML antes de responder.
- As perguntas ficam em um arquivo separado (`perguntas.js`), sem lógica dentro dele.

**Evolução (escolha pelo menos uma)**

- Cronômetro por pergunta, com penalidade por tempo esgotado.
- Ordem aleatória de perguntas e de alternativas a cada rodada, sem repetição.
- Revisão final com todas as perguntas, a sua resposta e a correta.
- Ranking local com os cinco melhores resultados e o nome do jogador, salvo no `localStorage`.
- Perguntas carregadas de um JSON externo com `fetch` (a partir da aula 10).

<details><summary>Pistas</summary>

1. Escreva `renderizar(estado)` antes de qualquer evento: dado o estado, qual HTML aparece? Cada clique só altera o estado e chama `renderizar` de novo — é o padrão que o Vue automatiza no Nível 3.
2. Para não denunciar a resposta, nunca coloque `data-correta="true"` no botão; compare o índice clicado com `pergunta.correta` em JavaScript (aulas 07 e 08 do Nível 2).
3. Embaralhar é o algoritmo de Fisher–Yates: dez linhas com um `for` de trás para a frente e uma troca. `sort(() => Math.random() - 0.5)` parece funcionar, mas é enviesado.
4. Para o cronômetro, `setInterval` precisa ser encerrado com `clearInterval` sempre que a pergunta muda — guarde o id do intervalo no estado.
</details>

### ⭐⭐ Sistema de cadastro de eventos
Tags: javascript, formularios, crud, dom, projeto

**Trilha sugerida:** Nível 2 (a partir da aula 08) · **Tempo estimado:** 8–12 h

O centro acadêmico anuncia palestras num grupo de WhatsApp, e ninguém acha a da semana passada nem sabe se a de amanhã é às 19h ou às 19h30. Uma agenda no navegador — sem servidor, sem login — já resolve a maior parte do problema, e usa o mesmo modelo de dados que você vai levar para uma API no fim do Nível 2 e para o UniEventos no Nível 3. A parte traiçoeira aqui é a data: formato, fuso, comparação e ordenação.

**Funcionalidades mínimas**

- Formulário com título, data, horário, local e descrição; edição e exclusão de eventos existentes.
- Lista em ordem cronológica, agrupada por dia, com os eventos passados separados dos futuros.
- Filtro por texto (título ou local) e por período (hoje, esta semana, todos).
- Persistência em `localStorage`.
- Confirmação antes de excluir.

**Critérios de pronto**

- Data e hora aparecem em português (dia da semana, dia e mês por extenso, hora com "h") e nunca no formato ISO cru.
- Não é possível salvar evento sem título, com data no passado ou com horário inválido; a mensagem aparece junto do campo, sem `alert()`.
- A ordem da lista está correta mesmo para eventos em meses e anos diferentes (teste com três datas de anos distintos).
- Editar um evento reaproveita o mesmo formulário e preserva o `id`; não cria duplicata.
- A lista se atualiza sem recarregar a página em toda operação; console sem erros.

**Evolução (escolha pelo menos uma)**

- Destaque para os próximos sete dias e contagem regressiva ("em 3 dias").
- Visão de calendário mensal em grade de sete colunas.
- Exportar e importar a agenda em JSON; gerar um arquivo `.ics` para o Google Agenda.
- Categorias com cor e filtro combinado.

<details><summary>Pistas</summary>

1. Guarde a data como a string que `input type="datetime-local"` devolve (`AAAA-MM-DDTHH:mm`) e converta com `new Date()` só para comparar e formatar; strings nesse formato ordenam corretamente até com `sort()` simples.
2. `Intl.DateTimeFormat('pt-BR', { dateStyle: 'medium', timeStyle: 'short' })` formata sem biblioteca — leia as opções `weekday` e `month` na MDN.
3. "Editar" e "criar" são a mesma função de salvar: se o objeto tem `id`, substitua no array (`findIndex`); senão, gere um id e faça `push` (aula 08 do Nível 2).
4. Para agrupar por dia, use `reduce` sobre a lista ordenada criando um objeto cuja chave é `data.slice(0, 10)`.
</details>

### ⭐⭐ Catálogo de produtos com carrinho
Tags: javascript, grid, dom, eventos, projeto

**Trilha sugerida:** Nível 2 (a partir da aula 08) · **Tempo estimado:** 8–12 h

Por que o total do carrinho nunca está escrito no HTML? Porque o carrinho é dado, e a tela é só um reflexo dele. Construa a vitrine de uma loja fictícia — o brechó, a livraria, a Café Cerrado — e um carrinho que sobrevive ao recarregar da página. Você vai reproduzir o raciocínio das lojas reais: uma lista de produtos, uma lista de itens escolhidos e funções que juntam as duas.

**Funcionalidades mínimas**

- Vitrine em grade responsiva gerada a partir de um array de produtos (nome, preço, imagem, categoria, estoque).
- Botão "adicionar" em cada card e ícone de carrinho no cabeçalho com contador de itens.
- Painel do carrinho (lateral ou modal) listando itens, quantidade, subtotal por item e total.
- Alterar quantidade (mais e menos) e remover item; carrinho persistido no `localStorage`.
- Filtro por categoria e ordenação por preço.

**Critérios de pronto**

- Adicionar o mesmo produto duas vezes aumenta a quantidade em vez de criar duas linhas.
- A quantidade nunca excede o estoque nem fica abaixo de 1: o botão desabilita **e** a lógica bloqueia.
- Total e contador do cabeçalho batem com a soma dos itens depois de qualquer operação; valores em `R$` com duas casas.
- O carrinho guarda apenas `{ id, quantidade }`; preço e nome vêm sempre do catálogo (mudar o preço de um produto altera o total na próxima renderização).
- O painel do carrinho fecha com Esc e devolve o foco ao botão que o abriu.

**Evolução (escolha pelo menos uma)**

- Cupom de desconto com regras (percentual, valor fixo, compra mínima, validade) e mensagem para cupom inválido.
- Cálculo de frete por faixa de CEP ou por peso.
- Tela de finalização com formulário validado e resumo do pedido.
- Catálogo carregado de um JSON via `fetch`, com estados de carregamento e de erro (aula 10).

<details><summary>Pistas</summary>

1. Duas listas, duas responsabilidades: `produtos` (imutável, vem do catálogo) e `carrinho` (muda com os cliques). Toda função do carrinho recebe as duas e devolve um número ou uma nova lista (aula 08 do Nível 2).
2. `reduce` calcula o total em uma linha; `find` acha o produto pelo id; `map` e `filter` renderizam. Se você está escrevendo um `for` com índice, pare e pense.
3. Para o `R$`, crie `new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' })` uma vez e reutilize o formatador.
4. Um painel acessível é um `dialog` nativo: `showModal()` já cuida do Esc e do foco; pesquise "HTMLDialogElement" na MDN.
</details>

### ⭐⭐⭐ Controle de despesas pessoais
Tags: javascript, formularios, dom, responsivo, projeto

**Trilha sugerida:** Nível 2 (a partir da aula 08) · **Tempo estimado:** 12–16 h

Some 0,1 com 0,2 no console do navegador. O resultado não é 0,3 — e é por isso que todo sistema financeiro sério guarda dinheiro em centavos inteiros. Neste projeto você vai controlar receitas e despesas de verdade (as suas ou as de um personagem), com categorias, saldo e filtros por mês, e descobrir na prática por que dinheiro e datas são os dois assuntos que mais geram bugs em produção.

**Funcionalidades mínimas**

- Lançamentos com descrição, valor, tipo (receita ou despesa), categoria e data; editar e excluir.
- Saldo, total de receitas e total de despesas do período selecionado.
- Filtros por mês e ano, por categoria e por tipo, combináveis entre si.
- Tabela ordenável por data e por valor; persistência em `localStorage`.
- Categorias gerenciáveis (criar, renomear), cada uma com cor.

**Critérios de pronto**

- Valores guardados como inteiros em centavos: `0,10 + 0,20` mostra `R$ 0,30`, e a soma de cem lançamentos de `R$ 0,10` dá exatamente `R$ 10,00`.
- A entrada aceita `1.234,56` e `1234.56` e rejeita letras, valores negativos ou zero, com mensagem no campo.
- Trocar o mês recalcula saldo e totais na hora; despesa aparece em vermelho **e** com sinal, não só por cor.
- Excluir uma categoria com lançamentos é impedido ou pede para onde movê-los — nunca deixa lançamento órfão.
- A tabela é legível em 360 px (as linhas viram cards ou as colunas secundárias se escondem) sem rolagem horizontal.
- Console sem erros; recarregar a página preserva tudo.

**Evolução (escolha pelo menos uma)**

- Resumo mensal com comparação ao mês anterior (subiu ou desceu quanto por cento).
- Limite por categoria com barra de progresso e alerta ao ultrapassar.
- Gráfico de pizza ou de barras da distribuição por categoria, em SVG feito por você (aula 05 do Nível 2) ou com Chart.js.
- Lançamentos recorrentes (aluguel todo dia 5) gerados automaticamente.
- Exportar CSV compatível com o Excel em português (ponto e vírgula como separador, vírgula decimal).

<details><summary>Pistas</summary>

1. Modelo: `{ id, descricao, valorCentavos, tipo, categoriaId, data }`. Converta na entrada (`Math.round(valor * 100)`) e formate na saída (`Intl.NumberFormat` com `currency: 'BRL'`); no meio, só inteiros.
2. Para aceitar `1.234,56`, remova os pontos de milhar e troque a vírgula por ponto antes do `Number()` — uma expressão regular de duas linhas; escreva a sua e teste com os dois formatos.
3. Filtros combináveis são `filter` encadeados sobre o array original; nunca filtre em cima do resultado anterior, ou o usuário não consegue voltar.
4. Para a tabela responsiva, `display: block` nas linhas com `td::before { content: attr(data-rotulo) }` transforma cada linha em um card no celular — pesquise "responsive tables" no CSS-Tricks.
</details>

### ⭐⭐⭐ Sistema de reservas de equipamentos
Tags: javascript, crud, formularios, dom, projeto

**Trilha sugerida:** Nível 2 (a partir da aula 08) · **Tempo estimado:** 12–16 h

O laboratório tem três projetores e cinco kits de Arduino, e a "reserva" é um caderno na secretaria. Duas turmas chegam com o mesmo projetor reservado, e o caderno não diz quem está com o kit que não voltou. Este é o projeto recomendado como fechamento dos dez: junta formulários, regras de negócio, estados, datas e persistência, e é a base direta do Boss "Sistema de reservas com API e login".

**Funcionalidades mínimas**

- Cadastro de equipamentos (nome, patrimônio, categoria, quantidade, estado: disponível, reservado, em uso, manutenção).
- Reserva com solicitante, equipamento, data e hora de início e de fim; retirada e devolução mudam o estado.
- Lista de reservas por equipamento e por dia, com filtro por estado.
- Persistência em `localStorage` e máquina de estados explícita (quais transições são permitidas).
- Painel resumo: quantos disponíveis, quantos em uso, quantas devoluções atrasadas.

**Critérios de pronto**

- É impossível criar reserva que se sobreponha a outra do mesmo equipamento; teste os quatro casos (começa antes e termina dentro, começa dentro e termina depois, engloba, está contida) e a mensagem diz com qual reserva há conflito.
- Fim antes do início, reserva no passado e duração acima do limite configurado são rejeitados no formulário.
- Transições inválidas (devolver o que não foi retirado, reservar equipamento em manutenção) não existem na interface **e** são bloqueadas na lógica.
- Devolução com atraso é marcada e aparece no painel.
- As regras de negócio estão em funções puras separadas do DOM (`haConflito(reservas, nova)`, `podeTransitar(de, para)`), testáveis no console.
- Um `README.md` descreve as regras com uma tabela de estados e transições.

**Evolução (escolha pelo menos uma)**

- Histórico de movimentações por equipamento (quem, quando, o quê), que nunca é apagado.
- Linha do tempo por dia (grade de horas por equipamento) mostrando as reservas como blocos.
- Reserva de quantidade (três dos cinco kits) em vez de unidade única.
- Lista de espera quando não há disponibilidade, com promoção automática ao cancelar.
- Regras adaptadas a um usuário real, seguindo a dica no fim desta página.

<details><summary>Pistas</summary>

1. Duas reservas conflitam quando `inicioA < fimB && inicioB < fimA`. Só isso. Desenhe os quatro casos numa linha do tempo antes de acreditar.
2. Represente as transições como um objeto, `{ disponivel: ['reservado', 'manutencao'], reservado: ['em_uso', 'disponivel'] }`, e uma função `podeTransitar(de, para)` que o consulta — é o padrão State disfarçado, que o Nível 3 apresenta.
3. Reserva e equipamento são coleções separadas ligadas por `equipamentoId`; o estado atual do equipamento pode ser calculado a partir das reservas em vez de guardado — pense em qual escolha gera menos inconsistência.
4. Datas: guarde no formato ISO, compare com `getTime()` e formate só na hora de mostrar (as pistas do projeto de eventos valem aqui).
</details>

### ⭐⭐⭐ Painel com dados de uma API pública
Tags: fetch, async, json, api, projeto

**Trilha sugerida:** Nível 2 (a partir da aula 10) · **Tempo estimado:** 10–14 h

Até aqui todos os dados estavam no seu arquivo. Agora eles estão em outro computador, chegam quando querem, às vezes não chegam e às vezes chegam num formato diferente do que a documentação prometia. Escolha uma API pública sem chave — ViaCEP, BrasilAPI, REST Countries, Open-Meteo, PokéAPI — e construa um painel que consulta, apresenta e compara resultados. O que se avalia aqui não é o dado bonito na tela: é o que acontece nos 300 ms antes de ele chegar e no dia em que a API cai.

**Funcionalidades mínimas**

- Campo de busca (CEP, país, cidade, nome) que dispara a consulta com `fetch` e `async/await`.
- Resultado em cards ou tabela, com os campos relevantes formatados, e não o JSON cru.
- Estados visíveis: carregando (esqueleto ou spinner), vazio, erro de rede e "não encontrado".
- Histórico das últimas consultas da sessão, clicável.
- Componentes visuais reutilizáveis: uma função `cardResultado(dado)` usada em toda a página.

**Critérios de pronto**

- Desligue a rede no DevTools e faça uma busca: a página mostra mensagem amigável e um botão "tentar de novo"; nada quebra no console.
- Buscar algo inexistente (CEP `00000-000`, país "Nárnia") mostra "não encontrado", diferente do erro de rede.
- Duas buscas rápidas em sequência não mostram o resultado da primeira por cima da segunda (verifique com "3G lento" no DevTools).
- O botão fica desabilitado enquanto a requisição está em andamento; Enter no campo também busca.
- Só `async/await` com `try/catch`; resposta com `response.ok === false` é tratada como erro.
- Os dados exibidos correspondem ao JSON da API (mostre a aba Rede na demonstração).

**Evolução (escolha pelo menos uma)**

- Favoritos persistentes no `localStorage`, com página própria.
- Cache local: a mesma consulta em menos de dez minutos não vai à rede, e a tela avisa "resultado em cache".
- Paginação ou rolagem infinita para APIs que devolvem listas.
- Comparação lado a lado de dois resultados (dois países, dois Pokémon, duas cidades).
- Gráfico com Chart.js (temperatura por hora, população por país).

<details><summary>Pistas</summary>

1. Abra a documentação da API e faça a primeira chamada colando a URL na barra de endereços antes de escrever uma linha de JavaScript; anote o formato exato da resposta, inclusive quando não acha nada (o ViaCEP devolve um JSON com a chave `erro` e status 200).
2. `fetch` só rejeita em falha de rede; `404` e `500` resolvem normalmente — teste `response.ok` e lance um `Error` com o status (aulas 09 e 10 do Nível 2).
3. Para a corrida entre buscas, guarde um contador de requisições e ignore respostas cujo número não é o mais recente — ou pesquise `AbortController` e cancele a anterior.
4. Cache é um objeto `{ chave: { dados, em } }`: a chave é o termo normalizado e `em` é `Date.now()`; antes de chamar `fetch`, veja se existe e se ainda é recente.
</details>

### 🔥 Boss — Sistema de reservas com API e login
Tags: express, autenticacao, banco-de-dados, deploy, projeto

**Trilha sugerida:** Nível 2 (a partir da aula 16) ou Nível 3 (a partir da aula 12), com Deploy (capítulos 04, 05 e 08) · **Tempo estimado:** 24–32 h

O sistema de reservas em `localStorage` funciona só no navegador de quem cadastrou; no dia em que duas pessoas precisam ver a mesma agenda, ele vira um caderno digital. Este Boss leva o projeto anterior para onde ele pede para ir: um front SPA que fala com uma API Express 5, usuários que entram com a conta Google (ou Firebase), dados em MySQL ou Supabase, regra de conflito verificada no servidor — porque o cliente pode ser burlado — e tudo no ar, com HTTPS, numa URL que você manda para o coordenador do laboratório.

**Funcionalidades mínimas**

- API REST com Express 5: equipamentos e reservas (listar, criar, mudar estado, cancelar), respostas JSON e códigos HTTP corretos (`201`, `400`, `401`, `403`, `404`, `409`).
- Autenticação com Google Identity Services e verificação do ID token no back com `google-auth-library`, **ou** Firebase Auth com `firebase-admin`; rotas de escrita exigem token.
- Perfis: usuário comum reserva e cancela as próprias reservas; administrador cadastra equipamentos e vê todas.
- Banco relacional (MySQL com `mysql2/promise` ou Supabase com RLS) com tabelas `usuarios`, `equipamentos` e `reservas`.
- Front SPA: JavaScript puro com `fetch` no Nível 2; Vue 3 + Vuetify + Pinia + Axios no Nível 3. Estados de carregamento e de erro em toda chamada.
- Regra de conflito de horário verificada **no servidor** antes de gravar, respondendo `409` com a reserva conflitante.
- Deploy: front em hospedagem estática, API em Render, Railway ou VPS, banco na nuvem, HTTPS válido nos dois.

**Critérios de pronto**

- Via `curl` ou Insomnia: `POST /api/reservas` sem token devolve `401`; usuário comum tentando cancelar reserva de outro recebe `403`.
- Duas requisições de reserva do mesmo equipamento no mesmo horário, disparadas em paralelo (script com dois `fetch` simultâneos), resultam em uma `201` e uma `409` — nunca duas `201`.
- Nenhum segredo no repositório: `.env` no `.gitignore`, chaves lidas de `process.env`; a chave `service_role` do Supabase nunca chega ao front.
- A SPA funciona ao recarregar em qualquer rota (o servidor devolve o `index.html`), e a sessão sobrevive ao recarregar.
- `https://` em front e API, cadeado válido, sem aviso de conteúdo misto; CORS restrito à origem do front.
- `README.md` com diagrama da arquitetura, instruções de instalação, variáveis de ambiente documentadas e a URL pública.
- Lighthouse Acessibilidade ≥ 90 na tela de reservas; console sem erros.

**Evolução (escolha pelo menos uma)**

- Documentação da API com `swagger-jsdoc` e `swagger-ui-express`, publicada em `/docs` (aula 14 do Nível 3).
- E-mail de confirmação da reserva e lembrete de devolução.
- Histórico de movimentações imutável, com quem fez o quê (auditoria).
- Testes automatizados das regras de conflito e das permissões, rodando no GitHub Actions (capítulo 09 de Deploy).
- Contêiner Docker para a API e `docker compose` com banco local (capítulo 07 de Deploy).

<details><summary>Pistas</summary>

1. Comece pela API, sem front: modele as tabelas, escreva as rotas e teste tudo com Insomnia ou `curl`. Só depois monte a tela — o front do projeto anterior é reaproveitável trocando `localStorage` por chamadas HTTP (aulas 11 a 13 do Nível 2 ou 08 e 09 do Nível 3).
2. A verificação de conflito precisa ser atômica: uma transação (`BEGIN`, `SELECT` das reservas sobrepostas, `INSERT`, `COMMIT`) ou uma restrição no banco. Um `if` em JavaScript antes do `INSERT` deixa a janela aberta para a corrida.
3. Middleware de autenticação: lê `Authorization: Bearer`, verifica o token, coloca `req.usuario` e chama `next()`; um segundo middleware `exigirAdmin` compara o perfil (aula 14 do Nível 2 ou aula 10 do Nível 3). Em Express 5, erros em handlers `async` caem sozinhos no tratador de erros.
4. Para o deploy, siga os capítulos 04 e 05 de Deploy na ordem: primeiro a API no ar com HTTPS e variáveis de ambiente configuradas na plataforma, depois o front apontando para a URL da API. A maior parte dos problemas é CORS e URL errada.
</details>

### 🔥 Boss — Painel de dados com cache, gráficos e CI
Tags: api, testes, ci-cd, performance, projeto

**Trilha sugerida:** Nível 3 (a partir da aula 08), com Deploy (capítulos 09 e 10) · **Tempo estimado:** 24–32 h

O painel do projeto de API pública chama a fonte direto do navegador; com duzentos usuários abrindo a página, a fonte bloqueia o IP e o painel morre. Este Boss coloca um servidor seu no meio: uma API Express que consulta a fonte, guarda em cache, expõe endpoints limpos e é testada, publicada e monitorada por um pipeline que roda sozinho a cada `git push`. É o ciclo completo do trabalho profissional: código, teste, integração contínua, deploy e observação.

**Funcionalidades mínimas**

- API Express 5 que consome uma fonte pública (Open-Meteo, BrasilAPI, IBGE, dados.gov.br) e expõe endpoints próprios (`/api/clima/:cidade`, `/api/indicadores`) com resposta normalizada.
- Cache no servidor (memória com tempo de vida, ou tabela no banco) e cache no cliente (`localStorage` ou Cache API), com indicação na resposta (cabeçalho `X-Cache: HIT` ou `MISS`).
- Front em Vue 3 + Vuetify + Pinia + Axios com pelo menos três gráficos em Chart.js (linha, barras e um terceiro), filtros por período ou região e estados de carregamento, vazio e erro.
- Testes automatizados: unitários das funções de transformação e de integração dos endpoints (`node --test` ou Vitest, com Supertest).
- GitHub Actions: a cada push, instala, roda lint e testes; na `main`, publica front e API.
- Monitoramento: endpoint `/health`, verificação externa (UptimeRobot ou similar) e log estruturado de erros.

**Critérios de pronto**

- Duas chamadas seguidas ao mesmo endpoint: a primeira responde `X-Cache: MISS`; a segunda responde `HIT` em menos de 50 ms (mostre no Insomnia ou com `curl -w '%{time_total}'`).
- Fonte pública indisponível (simule trocando a URL): a API devolve o último dado em cache com aviso, ou `503` com mensagem clara — nunca `500` genérico nem travamento.
- Cobertura de testes ≥ 70 % nas funções de transformação; pelo menos um teste falha de propósito quando você quebra uma regra (mostre na demonstração).
- Badge do GitHub Actions verde no `README.md`; um pull request com teste quebrado fica vermelho e não é publicado.
- Gráficos com título, eixos rotulados, unidade e alternativa textual (tabela ou resumo) para leitor de tela; `prefers-reduced-motion` desativa a animação do Chart.js.
- Lighthouse Performance ≥ 90 e Acessibilidade ≥ 90 na página principal; `vite build` sem aviso de tamanho de bundle.
- `/health` público e monitorado, com alerta configurado; URL pública com HTTPS.

**Evolução (escolha pelo menos uma)**

- Documentação com Swagger e limite de requisições por IP.
- Cache com invalidação seletiva e atualização em segundo plano (stale-while-revalidate).
- Exportar os dados filtrados em CSV e o gráfico em PNG.
- Docker para a API e deploy em VPS com nginx como proxy reverso (capítulos 06 e 07 de Deploy).
- Comparação entre duas regiões ou períodos no mesmo gráfico, com URL compartilhável (estado nos parâmetros da rota).

<details><summary>Pistas</summary>

1. Separe o back em três camadas: `fontes/` (fala com a API externa), `servicos/` (normaliza e cacheia) e `rotas/` (HTTP). Os testes unitários cobrem `servicos/` sem rede; os de integração usam Supertest com uma fonte falsa (aula 13 do Nível 3).
2. Cache em memória é um `Map` de chave para `{ dados, expiraEm }`; antes de ir à fonte, verifique `Date.now() < expiraEm`. Comece assim e só troque por algo externo se precisar de mais de uma instância.
3. Chart.js: um componente Vue por gráfico, recebendo `labels` e `datasets` por props e destruindo a instância em `onUnmounted` — senão o gráfico duplica ao trocar de filtro (aulas 05 e 06 do Nível 3).
4. O workflow do GitHub Actions começa com três passos (`checkout`, `setup-node` com cache do npm, `npm ci && npm test`); faça-o ficar verde antes de adicionar o deploy (capítulo 09 de Deploy). Segredos entram em Settings → Secrets do repositório, nunca no YAML.
</details>

> **💡 Dica**
> Desafio final, válido para qualquer projeto desta página: escolha um contexto real — o laboratório da sua faculdade, a biblioteca do bairro, uma escola, o comércio da família — e entreviste ao menos uma pessoa que usaria o sistema. Pergunte o que ela faz hoje, onde dói, o que é proibido e o que acontece quando dá errado. Depois adapte as regras do projeto ao que ouviu: talvez a reserva precise de aprovação, talvez o cardápio mude por turno, talvez a nota mínima seja outra. Nesse momento você deixa de reproduzir uma interface e passa a resolver um problema, que é o que se paga a um desenvolvedor.

> **📌 Vale gravar**
> Qualquer projeto desta página pode ser o **seu projeto autoral** — aquele que você constrói em paralelo às aulas e leva para o portfólio —, desde que siga a mesma arquitetura do projeto fio-condutor da trilha (Nível 1: site estático de várias páginas; Nível 2: SPA com API Express e login; Nível 3: Vue, Pinia, Express, banco e Firebase). Se você cursa a disciplina, combine a escolha com o professor antes de começar a unidade. Para saber se o projeto está no ponto, use o **marco da unidade**, na aula que a fecha: ele lista os requisitos e o checklist de qualidade.
