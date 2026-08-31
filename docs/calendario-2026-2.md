# Calendário 2026.2 (primeira oferta)

O material do WebLab é **atemporal**: nenhuma aula traz datas, nome de semestre ou turma.
O calendário de um semestre é opcional e vive só em `build/config.py`, aparecendo apenas
no índice de cada trilha.

## Como publicar o calendário de um semestre

Em `build/config.py`:

1. `SEMESTRE = "2027.1"` (o rótulo aparece ao lado do título "Cronograma").
2. Preencha `CRONOGRAMA` no formato abaixo (a chave é o id da trilha; `prazo: True` marca ⏰ no dia de entrega).
3. Opcionalmente, acrescente `"prazo": "24/04/2027, 23h59"` a cada item de `AVALIACOES` — sem isso, o site diz que os prazos saem no SIGAA.
4. `./deploy.sh`.

Para voltar ao material atemporal: `SEMESTRE = ""` e `CRONOGRAMA = {}`, e remova os `"prazo"` das avaliações.

## Registro: o calendário usado em 2026.2

Datas conforme os Planos de Curso em `docs/planos/`; no Nível 3, com a correção de +2 dias
feita pelo professor (encontros às quartas-feiras).

```python
CRONOGRAMA = {
    "nivel-1": [
        {"data": "11/08/2026", "num": "01", "descricao": "Apresentação da disciplina; tecnologias e arquitetura da Web"},
        {"data": "18/08/2026", "num": "02", "descricao": "Introdução ao HTML: estrutura, textos, links, tabelas"},
        {"data": "25/08/2026", "num": "03", "descricao": "Introdução ao formulário"},
        {"data": "01/09/2026", "num": "04", "descricao": "Formulário, mídias e listas"},
        {"data": "08/09/2026", "num": "05", "descricao": "Elementos HTML para layout e introdução ao CSS"},
        {"data": "15/09/2026", "num": "06", "descricao": "CSS: sintaxe, seletores, classes, atributos e valores — envio da Avaliação 1", "prazo": True},
        {"data": "22/09/2026", "num": "07", "descricao": "Formatando o layout de um website e o menu"},
        {"data": "29/09/2026", "num": "08", "descricao": "Criando telas responsivas"},
        {"data": "06/10/2026", "num": "09", "descricao": "Animações e efeitos em CSS"},
        {"data": "13/10/2026", "num": "10", "descricao": "Introdução ao JavaScript — envio da Avaliação 2", "prazo": True},
        {"data": "20/10/2026", "num": "11", "descricao": "Variáveis, operações aritméticas e estruturas de controle"},
        {"data": "27/10/2026", "num": "12", "descricao": "Estruturas sequenciais, condicionais e de repetição"},
        {"data": "03/11/2026", "num": "13", "descricao": "Funções e eventos"},
        {"data": "10/11/2026", "num": "14", "descricao": "JavaScript para validação de formulários e consultas dinâmicas"},
        {"data": "17/11/2026", "num": "15", "descricao": "Publicando seu website na internet — envio da Avaliação 3", "prazo": True},
    ],
    "nivel-2": [
        {"data": "11/08/2026", "num": "01", "descricao": "Apresentação; arquitetura web; ambiente de desenvolvimento e Git"},
        {"data": "18/08/2026", "num": "02", "descricao": "Introdução ao desenvolvimento web"},
        {"data": "25/08/2026", "num": "03", "descricao": "Revisão de HTML: layout, links e formulários"},
        {"data": "01/09/2026", "num": "04", "descricao": "Frameworks CSS"},
        {"data": "08/09/2026", "num": "05", "descricao": "Animação e SVG"},
        {"data": "15/09/2026", "num": "06", "descricao": "Acessibilidade e ARIA"},
        {"data": "22/09/2026", "num": "07", "descricao": "Revisão de JavaScript: objetos, funções, eventos e DOM"},
        {"data": "29/09/2026", "num": "08", "descricao": "Funções, arrow functions, callbacks e vetores — prazo da Avaliação 1 (23h59)", "prazo": True},
        {"data": "06/10/2026", "num": "09", "descricao": "Promises e async/await"},
        {"data": "13/10/2026", "num": "10", "descricao": "AJAX, JSON e Single Page Application"},
        {"data": "20/10/2026", "num": "11", "descricao": "Introdução ao Express"},
        {"data": "27/10/2026", "num": "12", "descricao": "Express estruturado e middlewares — prazo da Avaliação 2 (23h59)", "prazo": True},
        {"data": "03/11/2026", "num": "13", "descricao": "Rotas e controladores"},
        {"data": "10/11/2026", "num": "14", "descricao": "Autenticação com Google (front e back)"},
        {"data": "17/11/2026", "num": "15", "descricao": "CRUD com front-end assíncrono (AJAX/SPA)"},
        {"data": "24/11/2026", "num": "16", "descricao": "CRUD completo com autenticação Google — prazo da Avaliação 3 (23h59)", "prazo": True},
    ],
    "nivel-3": [
        {"data": "12/08/2026", "num": "01", "descricao": "Apresentação da disciplina e revisão de JavaScript"},
        {"data": "19/08/2026", "num": "02", "descricao": "Introdução ao Vue: instância, ciclo de vida e diretivas"},
        {"data": "26/08/2026", "num": "03", "descricao": "Vue: listas, computed e ciclo de vida"},
        {"data": "02/09/2026", "num": "04", "descricao": "Introdução a Vuetify e Vue Router — prazo da Avaliação 1", "prazo": True},
        {"data": "16/09/2026", "num": "05", "descricao": "Componentes, Vue Router e Vuetify avançado"},
        {"data": "23/09/2026", "num": "06", "descricao": "Axios e Pinia"},
        {"data": "30/09/2026", "num": "07", "descricao": "Introdução ao Firebase, Node.js e Express"},
        {"data": "07/10/2026", "num": "08", "descricao": "Endpoints e middlewares — prazo da Avaliação 2", "prazo": True},
        {"data": "21/10/2026", "num": "09", "descricao": "Integrando com SGBD MySQL"},
        {"data": "28/10/2026", "num": "10", "descricao": "Requisições autenticadas com Firebase"},
        {"data": "11/11/2026", "num": "11", "descricao": "Integrando front-end com back-end: CRUD"},
        {"data": "18/11/2026", "num": "12", "descricao": "CRUD com banco em nuvem (Supabase)"},
        {"data": "25/11/2026", "num": "13", "descricao": "Desenvolvimento do back-end"},
        {"data": "09/12/2026", "num": "14", "descricao": "Documentação com Swagger"},
        {"data": "16/12/2026", "num": "15", "descricao": "Apresentação dos resultados — prazo da Avaliação 3", "prazo": True},
    ],
}

AVALIACOES = {
    "nivel-1": [
        {"n": 1, "prazo": "15/09/2026", "escopo": "Site em HTML com os elementos da Unidade 1 (estrutura, textos, links, tabelas, formulários, mídias, listas)."},
        {"n": 2, "prazo": "13/10/2026", "escopo": "O mesmo site estilizado com CSS: layout, menu, responsividade e animações."},
        {"n": 3, "prazo": "17/11/2026", "escopo": "O site dinâmico e interativo com JavaScript: eventos, validação de formulários e consultas dinâmicas."},
    ],
    "nivel-2": [
        {"n": 1, "prazo": "29/09/2026, 23h59", "escopo": "Website client-side em HTML e CSS: HTML semântico, layout responsivo, framework CSS, animação/SVG, acessibilidade."},
        {"n": 2, "prazo": "27/10/2026, 23h59", "escopo": "Evolução do site com JavaScript: validação de formulários, DOM e eventos, programação assíncrona, SPA com AJAX/JSON."},
        {"n": 3, "prazo": "24/11/2026, 23h59", "escopo": "Aplicação full-stack com Node.js e Express: rotas e controladores, autenticação Google, CRUD com persistência, front-end assíncrono."},
    ],
    "nivel-3": [
        {"n": 1, "prazo": "02/09/2026, 23h59", "escopo": "Vue 3 com CLI: estrutura, componentes, diretivas, Vuetify e Vue Router básico."},
        {"n": 2, "prazo": "07/10/2026, 23h59", "escopo": "Vue avançado: Vuetify + Axios + Vue Router + Pinia."},
        {"n": 3, "prazo": "16/12/2026, 23h59", "escopo": "Back-end com Express, banco de dados (MySQL/Supabase), autenticação Firebase, documentação e deploy."},
    ],
}
```
