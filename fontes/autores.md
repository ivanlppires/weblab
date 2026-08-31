## Como a autoria funciona aqui

O WebLab é publicado aberto e continua sendo escrito. Para que o crédito seja justo e verificável, cada contribuição é registrada com **o que a pessoa fez** e **em que parte do material** — nos moldes da taxonomia [CRediT](https://credit.niso.org/), usada por periódicos científicos para separar quem concebeu, quem escreveu, quem revisou e quem programou.

Os papéis usados aqui são:

| Papel | O que significa |
|---|---|
| Concepção | Desenhou a estrutura do material, a sequência das trilhas e o padrão editorial |
| Redação | Escreveu aulas ou capítulos completos |
| Revisão | Revisou tecnicamente um conjunto identificado de aulas, propondo correções e melhorias |
| Software | Escreveu ou manteve o gerador do site (Python, CSS e JavaScript) |
| Curadoria | Organizou desafios, links, exemplos e o banco de projetos |

## Quem pode entrar como coautor

O material é revisado por convite. O critério é objetivo, para que ninguém dependa de interpretação:

- **Coautoria** — quem revisa tecnicamente uma unidade inteira (quatro aulas ou mais), reescreve trechos, corrige erros de conteúdo ou acrescenta material novo. Entra na lista de autores desta página, no arquivo de citação do repositório e nos metadados do DOI, com o papel e o escopo descritos.
- **Crédito de revisão** — quem faz uma leitura pontual, aponta erros específicos ou sugere melhorias em aulas isoladas. Aparece no rodapé das aulas revisadas e nos agradecimentos, sem entrar como autor.

Em qualquer um dos casos, o escopo é registrado por escrito: "revisou o Nível 2, aulas 11 a 16" diz mais — e é mais honesto — do que um nome solto numa lista.

## Como contribuir

O material inteiro vive em [github.com/ivanlppires/weblab](https://github.com/ivanlppires/weblab), em Markdown. Há três caminhos, do mais leve ao mais envolvido:

1. **Apontar um erro:** abra uma *issue* descrevendo a aula, o trecho e o problema. Erros de código, comandos que não rodam e explicações confusas são os mais valiosos.
2. **Propor uma correção:** edite o arquivo em `fontes/<trilha>/` e abra um *pull request*. O padrão editorial está em `fontes/ESPECIFICACAO.md` e é verificado automaticamente (`python build/lint.py`) antes de qualquer publicação.
3. **Revisar uma unidade:** escreva para o professor combinando o escopo. Revisões dessa natureza entram como coautoria.

## Como citar

Ao usar o WebLab em aula, em um trabalho ou em outro material, cite a versão que você consultou. O arquivo `CITATION.cff` no repositório mantém os dados sempre atualizados, e o site tem endereço fixo:

> PIRES, Ivan Luiz Pedroso *et al.* **WebLab — Laboratório de Desenvolvimento Web**. UNEMAT — Campus Sinop, FACET. Disponível em: https://weblab.ivanpires.dev.

## Licença

O conteúdo (as aulas, os desafios e os textos) é publicado sob **Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)**: você pode copiar, adaptar e usar em qualquer contexto, inclusive em sala de aula de outra instituição, desde que credite a autoria e indique as mudanças feitas. O gerador do site (o código em `build/`) é publicado sob **licença MIT**.
