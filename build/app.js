/* WebLab — comportamento do site (inlinado pelo build). Sem dependências. */
(function () {
  'use strict';
  var raiz = document.documentElement;
  var RAIZ_REL = raiz.getAttribute('data-raiz') || './';

  // ---------- localStorage seguro ----------
  function ler(chave) { try { return window.localStorage.getItem(chave); } catch (e) { return null; } }
  function gravar(chave, valor) { try { if (valor === null) localStorage.removeItem(chave); else localStorage.setItem(chave, valor); } catch (e) { /* sem storage */ } }

  // ---------- tema ----------
  (function tema() {
    var salvo = ler('weblab:tema');
    if (salvo) raiz.setAttribute('data-tema', salvo);
    else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) raiz.setAttribute('data-tema', 'escuro');
    var bt = document.getElementById('tema');
    if (!bt) return;
    function rotulo() {
      var escuro = raiz.getAttribute('data-tema') === 'escuro';
      bt.innerHTML = '<span aria-hidden="true">' + (escuro ? '☼' : '☾') + '</span><span class="rotulo">' + (escuro ? 'Claro' : 'Escuro') + '</span>';
      bt.setAttribute('aria-label', escuro ? 'Mudar para o tema claro' : 'Mudar para o tema escuro');
    }
    bt.addEventListener('click', function () {
      var novo = raiz.getAttribute('data-tema') === 'escuro' ? 'claro' : 'escuro';
      raiz.setAttribute('data-tema', novo);
      gravar('weblab:tema', novo);
      rotulo();
    });
    rotulo();
  })();

  // ---------- menu lateral (mobile) ----------
  (function menu() {
    var bt = document.getElementById('menu-btn');
    var lateral = document.querySelector('.lateral');
    if (!bt || !lateral) return;
    function abrir(v) { lateral.classList.toggle('aberta', v); bt.setAttribute('aria-expanded', String(v)); }
    bt.addEventListener('click', function () { abrir(!lateral.classList.contains('aberta')); });
    var fechar = lateral.querySelector('.fechar');
    if (fechar) fechar.addEventListener('click', function () { abrir(false); });
    lateral.addEventListener('click', function (e) { if (e.target.closest('a')) abrir(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') abrir(false); });
  })();

  // ---------- copiar código ----------
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.copiar');
    if (!b) return;
    var pre = b.closest('.bloco').querySelector('pre');
    var txt = pre.innerText;
    var ok = function () {
      b.textContent = 'Copiado ✓'; b.classList.add('ok');
      setTimeout(function () { b.textContent = 'Copiar'; b.classList.remove('ok'); }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, ok);
    else { var t = document.createElement('textarea'); t.value = txt; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); } catch (x) { } t.remove(); ok(); }
  });

  // ---------- barra de progresso de leitura ----------
  (function progresso() {
    var pr = document.getElementById('progresso');
    if (!pr) return;
    var tick = false;
    window.addEventListener('scroll', function () {
      if (tick) return; tick = true;
      requestAnimationFrame(function () {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        pr.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
        tick = false;
      });
    }, { passive: true });
  })();

  // ---------- sumário ativo ----------
  var observador = null;
  function ligarSumario(container) {
    if (observador) observador.disconnect();
    var toc = document.getElementById('toc');
    if (!toc || !('IntersectionObserver' in window)) return;
    var links = {};
    toc.querySelectorAll('a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
    var alvos = (container || document).querySelectorAll('main h2[id], main h3[id]');
    observador = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) {
        var a = links[e.target.id];
        if (!a || !e.isIntersecting) return;
        Object.keys(links).forEach(function (k) { links[k].classList.remove('ativo'); });
        a.classList.add('ativo');
      });
    }, { rootMargin: '-80px 0px -70% 0px' });
    alvos.forEach(function (t) { observador.observe(t); });
  }
  ligarSumario();

  // ---------- progresso local: aulas concluídas e desafios feitos ----------
  function atualizarBarras() {
    document.querySelectorAll('.progresso-trilha[data-aulas]').forEach(function (el) {
      var ids = [];
      try { ids = JSON.parse(el.getAttribute('data-aulas')); } catch (e) { }
      if (!ids.length) return;
      var feitas = ids.filter(function (id) { return ler('weblab:aula:' + id) === '1'; }).length;
      var pct = Math.round(100 * feitas / ids.length);
      el.querySelector('.barra i').style.width = pct + '%';
      el.querySelector('b').textContent = feitas + '/' + ids.length;
      var rot = el.querySelector('.rot');
      if (rot) rot.textContent = pct === 100 ? 'Trilha concluída 🎉' : (feitas ? pct + '% concluído' : 'Comece pela aula 01');
    });
    document.querySelectorAll('[data-aula-id]').forEach(function (el) {
      el.classList.toggle('feita', ler('weblab:aula:' + el.getAttribute('data-aula-id')) === '1');
    });
    var cont = document.getElementById('desafios-feitos');
    if (cont) {
      var n = 0;
      document.querySelectorAll('article.ficha').forEach(function (f) { if (f.classList.contains('feito')) n++; });
      cont.textContent = n;
    }
  }

  (function progressoLocal() {
    // checkbox "Concluí esta aula"
    var c = document.getElementById('concluir');
    if (c) {
      var chave = c.getAttribute('data-chave');
      c.checked = ler(chave) === '1';
      c.closest('.concluir').classList.toggle('ok', c.checked);
      c.addEventListener('change', function () {
        gravar(chave, c.checked ? '1' : null);
        c.closest('.concluir').classList.toggle('ok', c.checked);
        atualizarBarras();
      });
    }
    // checkboxes "Feito" nos desafios (aula e banco)
    document.querySelectorAll('label.feito input[data-chave]').forEach(function (cb) {
      var chave = cb.getAttribute('data-chave');
      var art = cb.closest('article');
      cb.checked = ler(chave) === '1';
      if (art) art.classList.toggle('feito', cb.checked);
      cb.addEventListener('change', function () {
        gravar(chave, cb.checked ? '1' : null);
        if (art) art.classList.toggle('feito', cb.checked);
        atualizarBarras();
        if (typeof filtrarFichas === 'function') filtrarFichas();
      });
    });
    atualizarBarras();
  })();

  // ---------- busca global ----------
  (function busca() {
    var input = document.getElementById('busca');
    var res = document.getElementById('busca-res');
    if (!input || !res) return;
    var indice = null, carregando = false, sel = -1;
    function normal(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
    function carregar(cb) {
      if (indice) return cb();
      if (carregando) return;
      carregando = true;
      fetch(RAIZ_REL + 'busca.json').then(function (r) { return r.json(); }).then(function (j) { indice = j; carregando = false; cb(); })
        .catch(function () { carregando = false; res.innerHTML = '<div class="vazio">Não foi possível carregar o índice de busca.</div>'; });
    }
    function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
    function render(lista, q) {
      sel = -1;
      if (!q) { res.hidden = true; return; }
      if (!lista.length) { res.innerHTML = '<div class="vazio">Nada encontrado para “' + esc(q) + '”.</div>'; res.hidden = false; return; }
      res.innerHTML = lista.slice(0, 20).map(function (r) {
        return '<a href="' + esc(RAIZ_REL + r.u + (r.a ? '#' + r.a : '')) + '"><div class="t">' + esc(r.t) + '</div><div class="m">' + esc(r.tr) + (r.sub ? ' · ' + esc(r.sub) : '') + '</div></a>';
      }).join('');
      res.hidden = false;
    }
    function buscar() {
      var q = normal(input.value.trim());
      if (!q) { res.hidden = true; return; }
      var termos = q.split(/\s+/);
      var achados = [];
      indice.forEach(function (p) {
        var alvoT = normal(p.t), alvoH = normal((p.h || []).join(' | ')), alvoD = normal((p.d || []).join(' | '));
        var pontos = 0;
        var ok = termos.every(function (t) {
          if (alvoT.indexOf(t) >= 0) { pontos += 3; return true; }
          if (alvoH.indexOf(t) >= 0) { pontos += 2; return true; }
          if (alvoD.indexOf(t) >= 0) { pontos += 1; return true; }
          return false;
        });
        if (!ok) return;
        var sub = '';
        var hh = (p.h || []).filter(function (h) { return termos.some(function (t) { return normal(h).indexOf(t) >= 0; }); });
        if (hh.length) sub = hh.slice(0, 2).join(' · ');
        else { var dd = (p.d || []).filter(function (d) { return termos.some(function (t) { return normal(d).indexOf(t) >= 0; }); }); if (dd.length) sub = '🏆 ' + dd[0]; }
        achados.push({ u: p.u, t: p.t, tr: p.tr, sub: sub, pontos: pontos });
      });
      achados.sort(function (a, b) { return b.pontos - a.pontos; });
      render(achados, input.value.trim());
    }
    input.addEventListener('focus', function () { carregar(function () { if (input.value.trim()) buscar(); }); });
    input.addEventListener('input', function () { carregar(buscar); });
    input.addEventListener('keydown', function (e) {
      var itens = res.querySelectorAll('a');
      if (e.key === 'ArrowDown' && itens.length) { e.preventDefault(); sel = Math.min(sel + 1, itens.length - 1); }
      else if (e.key === 'ArrowUp' && itens.length) { e.preventDefault(); sel = Math.max(sel - 1, 0); }
      else if (e.key === 'Enter' && sel >= 0 && itens[sel]) { itens[sel].click(); return; }
      else if (e.key === 'Escape') { res.hidden = true; input.blur(); return; }
      else return;
      itens.forEach(function (a, i) { a.classList.toggle('sel', i === sel); });
      if (itens[sel]) itens[sel].scrollIntoView({ block: 'nearest' });
    });
    document.addEventListener('click', function (e) { if (!e.target.closest('.busca-wrap')) res.hidden = true; });
  })();

  // ---------- filtros do banco de desafios ----------
  var filtrarFichas = null;
  (function banco() {
    var fichas = document.querySelectorAll('article.ficha');
    if (!fichas.length) return;
    var selTrilha = document.getElementById('f-trilha');
    var botoes = document.querySelectorAll('.filtros .dific button');
    var soNaoFeitos = document.getElementById('f-nao-feitos');
    var texto = document.getElementById('f-texto');
    var tags = document.querySelectorAll('.tags-nuvem button');
    var contagem = document.getElementById('contagem');
    var dific = '', tag = '';
    function normal(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
    filtrarFichas = function () {
      var q = normal(texto ? texto.value.trim() : '');
      var tr = selTrilha ? selTrilha.value : '';
      var n = 0;
      fichas.forEach(function (f) {
        var ok = true;
        if (tr && f.getAttribute('data-trilha') !== tr) ok = false;
        if (dific && f.getAttribute('data-dificuldade') !== dific) ok = false;
        if (tag && (' ' + f.getAttribute('data-tags') + ' ').indexOf(' ' + tag + ' ') < 0) ok = false;
        if (soNaoFeitos && soNaoFeitos.checked && f.classList.contains('feito')) ok = false;
        if (q && normal(f.textContent).indexOf(q) < 0) ok = false;
        f.classList.toggle('oculto', !ok);
        if (ok) n++;
      });
      if (contagem) contagem.textContent = n + ' de ' + fichas.length + ' desafios';
    };
    if (selTrilha) selTrilha.addEventListener('change', filtrarFichas);
    if (soNaoFeitos) soNaoFeitos.addEventListener('change', filtrarFichas);
    if (texto) texto.addEventListener('input', filtrarFichas);
    botoes.forEach(function (b) {
      b.addEventListener('click', function () {
        dific = dific === b.getAttribute('data-d') ? '' : b.getAttribute('data-d');
        botoes.forEach(function (x) { x.classList.toggle('ativo', x.getAttribute('data-d') === dific); });
        filtrarFichas();
      });
    });
    tags.forEach(function (b) {
      b.addEventListener('click', function () {
        tag = tag === b.getAttribute('data-tag') ? '' : b.getAttribute('data-tag');
        tags.forEach(function (x) { x.classList.toggle('ativo', x.getAttribute('data-tag') === tag); });
        filtrarFichas();
      });
    });
    // ?tag=x ou ?trilha=nivel-1 na URL
    try {
      var u = new URL(location.href);
      if (u.searchParams.get('trilha') && selTrilha) selTrilha.value = u.searchParams.get('trilha');
      if (u.searchParams.get('tag')) { tag = u.searchParams.get('tag'); tags.forEach(function (x) { x.classList.toggle('ativo', x.getAttribute('data-tag') === tag); }); }
    } catch (e) { }
    filtrarFichas();
  })();

  // ---------- apostila única: uma aula por vez ----------
  (function apostila() {
    var secoes = [].slice.call(document.querySelectorAll('.aula-secao'));
    if (!secoes.length) return;
    var ids = secoes.map(function (s) { return s.getAttribute('data-aula'); });
    var toc = document.getElementById('toc');
    var atual = null;
    function abrir(num, semScroll) {
      if (ids.indexOf(num) < 0) num = ids[0];
      atual = num;
      secoes.forEach(function (s) { s.classList.toggle('oculto', s.getAttribute('data-aula') !== num); });
      document.querySelectorAll('.lateral a[data-ir]').forEach(function (a) { a.classList.toggle('ativo', a.getAttribute('data-ir') === num); });
      var sec = document.querySelector('.aula-secao[data-aula="' + num + '"]');
      var dados = sec.querySelector('.toc-dados');
      if (toc) toc.innerHTML = '<h4>Nesta aula</h4>' + (dados ? dados.innerHTML : '');
      if (!semScroll) window.scrollTo(0, 0);
      if (location.hash !== '#aula-' + num) history.replaceState(null, '', '#aula-' + num);
      ligarSumario(sec);
    }
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a[data-ir]');
      if (!a) return;
      e.preventDefault();
      abrir(a.getAttribute('data-ir'));
    });
    document.addEventListener('keydown', function (e) {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      var i = ids.indexOf(atual);
      if (e.key === 'j' && i < ids.length - 1) abrir(ids[i + 1]);
      if (e.key === 'k' && i > 0) abrir(ids[i - 1]);
    });
    var hash = (location.hash || '').replace('#aula-', '');
    abrir(hash && ids.indexOf(hash) >= 0 ? hash : ids[0], true);
    // âncora interna (#a03-secao) dentro de uma aula específica
    if (location.hash && ids.indexOf(hash) < 0) {
      var m = location.hash.match(/^#a(\d\d)-/);
      if (m) { abrir(m[1], true); var alvo = document.querySelector(location.hash); if (alvo) alvo.scrollIntoView(); }
    }
  })();

  // ---------- atalhos de teclado ----------
  document.addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.metaKey || e.ctrlKey || e.altKey) return;
    var ant = document.querySelector('[data-nav="anterior"]');
    var pro = document.querySelector('[data-nav="proxima"]');
    var busca = document.getElementById('busca');
    if (e.key === 'j' && pro) pro.click();
    if (e.key === 'k' && ant) ant.click();
    if (e.key === '/' && busca) { e.preventDefault(); busca.focus(); }
  });
})();
