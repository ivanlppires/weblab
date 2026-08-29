from build import lint


def aula_ok(tipo="aula"):
    secs = [
        "## 🎯 Objetivos de aprendizagem", "## 📋 Pré-requisitos", "## 🗺️ Roteiro", "## 1. Teoria",
        "## 🚀 Passo a passo — publicar" if tipo == "deploy" else "## 💻 Mão na massa — passo",
        "## 🧪 Laboratório", "## 🏆 Desafios", "## 🐛 Erros comuns",
        "## 🏠 Atividade assíncrona (1 h)",
        "## ✅ Está no ar quando…" if tipo == "deploy" else "## ✅ Checkpoint do projeto",
        "## 📚 Para aprofundar",
    ]
    lab = "\n".join(
        ["### Nível A — Fixação"] + [f"**A{i}.** pergunta" for i in range(1, 5)]
        + ["", "### Nível B — Aplicação"] + [f"**B{i}.** tarefa" for i in range(1, 4)]
        + ["", "### Nível C — Desafio em sala", "**C1.** difícil"]
    )
    des = "\n".join(
        f"### {'⭐' * n} T{n}\nTags: html, css\n\ntexto\n\n**Critérios de pronto**\n\n- a\n\n<details><summary>Pistas</summary>\n\n1. p\n</details>\n"
        for n in (1, 2, 3)
    )
    corpo = {"## 🧪 Laboratório": lab, "## 🏆 Desafios": des}
    linhas = ["# Aula 01 — X" if tipo == "aula" else "# Capítulo 01 — X", ""]
    for s in secs:
        linhas += [s, "", corpo.get(s, "texto"), ""]
    linhas += ["```js", "const x = 1;", "```", ""] + ["linha de texto"] * 600
    return "\n".join(linhas)


def test_aula_valida_sem_erros():
    assert lint.lint_texto(aula_ok(), "aula") == []


def test_capitulo_deploy_valido():
    assert lint.lint_texto(aula_ok("deploy"), "deploy") == []


def test_falta_secao():
    erros = lint.lint_texto(aula_ok().replace("## 🐛 Erros comuns", "## Erros"), "aula")
    assert any("🐛" in e for e in erros)


def test_secao_fora_de_ordem():
    t = aula_ok()
    t = t.replace("## 🐛 Erros comuns", "## TMP").replace("## 🏠 Atividade assíncrona (1 h)", "## 🐛 Erros comuns").replace("## TMP", "## 🏠 Atividade assíncrona (1 h)")
    erros = lint.lint_texto(t, "aula")
    assert any("ordem" in e for e in erros)


def test_fence_sem_linguagem():
    erros = lint.lint_texto(aula_ok().replace("```js", "```"), "aula")
    assert any("sem linguagem" in e for e in erros)


def test_fence_aninhado_com_4_crases_nao_confunde():
    t = aula_ok() + "\n````markdown\n```js\nx\n```\n````\n"
    assert not any("sem linguagem" in e for e in lint.lint_texto(t, "aula"))


def test_placeholder():
    erros = lint.lint_texto(aula_ok() + "\n// ...resto do código\n", "aula")
    assert any("placeholder" in e for e in erros)
    erros = lint.lint_texto(aula_ok() + "\nTODO: escrever\n", "aula")
    assert any("placeholder" in e for e in erros)


def test_poucos_desafios_e_lab():
    t = aula_ok().replace("### ⭐⭐⭐ T3", "### T3").replace("**B3.** tarefa", "")
    erros = lint.lint_texto(t, "aula")
    assert any("desafios" in e for e in erros) and any("Nível B" in e for e in erros)


def test_desafio_sem_tags_ou_criterios():
    t = aula_ok().replace("Tags: html, css\n\ntexto\n\n**Critérios de pronto**", "texto", 1)
    erros = lint.lint_texto(t, "aula")
    assert any("Tags" in e for e in erros) and any("Critérios de pronto" in e for e in erros)


def test_tabela_larga():
    t = aula_ok() + "\n| a | b | c | d | e |\n|---|---|---|---|---|\n| 1 | 2 | 3 | 4 | 5 |\n"
    assert any("colunas" in e for e in lint.lint_texto(t, "aula"))


def test_tamanho_minimo():
    t = "\n".join(aula_ok().splitlines()[:300])
    assert any("linhas" in e for e in lint.lint_texto(t, "aula"))


def test_titulo_esperado():
    erros = lint.lint_texto(aula_ok(), "aula", titulo_esperado="Aula 01 — Outro título")
    assert any("título" in e.lower() for e in erros)
    assert lint.lint_texto(aula_ok(), "aula", titulo_esperado="Aula 01 — X") == []


def test_livre_so_checa_fences_e_placeholders():
    assert lint.lint_texto("## Docs\n\n- [MDN](https://x) — y\n", "livre") == []
    assert lint.lint_texto("```\nx\n```\n", "livre") != []
