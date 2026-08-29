# Aula 10 — Requisições autenticadas com Firebase

> **Nível 3 — Frameworks Modernos** · Unidade 3: Integração front-end/back-end
> WebLab · UNEMAT Sinop · Prof. Ivan Luiz Pedroso Pires

Na Aula 09 o UniEventos passou a persistir eventos no MySQL, com a API `unieventos-api` seguindo a arquitetura controller → service → repository. Qualquer pessoa com acesso à API conseguia criar, editar ou excluir um evento — não havia noção de "quem" fazia a requisição. Hoje isso muda: vamos exigir identidade.

## 🎯 Objetivos de aprendizagem

Ao final desta aula você será capaz de:

- Explicar a diferença entre autenticação e autorização, e por que senha em texto puro no banco é um erro grave.
- Descrever a estrutura de um JWT (header, payload, assinatura) e explicar por que ele é assinado, não criptografado.
- Implementar cadastro, login, logout e login com Google usando o SDK modular do Firebase Auth.
- Construir uma store Pinia de autenticação que resolve corretamente o problema do F5 (recarregar a página autenticado).
- Proteger rotas do Vue Router com `beforeEach` aguardando a inicialização da autenticação.
- Enviar o token do usuário em cada requisição Axios via interceptor e validá-lo no back-end com `firebase-admin`.
- Diferenciar dois níveis de proteção (rota no front = UX; middleware no back = segurança) e implementar autorização por papel com custom claims.

## 📋 Pré-requisitos desta aula

Checklist antes de começar:

- [ ] `unieventos-web` rodando com Vue Router e Pinia configurados (Aulas 04–06).
- [ ] `unieventos-api` rodando com Express 5, endpoints de eventos e persistência MySQL (Aulas 07–09).
- [ ] Projeto Firebase criado (Aula 07) — anote o `projectId`.
- [ ] Node.js 22.22.2 e npm 10.9.7 instalados (`node -v`, `npm -v`).
- [ ] Acesso ao [console do Firebase](https://console.firebase.google.com) com o projeto do UniEventos.

## 🗺️ Roteiro

| Bloco | Tempo | Atividade |
|---|---|---|
| 1 | 50 min | Autenticação × autorização; anatomia de um JWT; habilitar provedores no console; Firebase Auth no front (cadastro, login, logout) |
| 2 | 50 min | Store de autenticação em Pinia; guard de rota; interceptor Axios enviando o token |
| 3 | 50 min | Verificação do token no back-end com `firebase-admin`; middleware `autenticar`/`autorizar`; custom claims; testes com e sem token |

## 1. Autenticação não é autorização

São duas perguntas diferentes, e misturar as duas é a origem de muito bug de segurança:

- **Autenticação** responde "quem é você?". O sistema confirma sua identidade — normalmente com e-mail e senha, ou delegando a um provedor como Google.
- **Autorização** responde "o que você pode fazer?". Depois de saber quem você é, o sistema decide se você pode ler, criar, editar ou excluir um recurso.

Um usuário autenticado pode não estar autorizado a excluir um evento — só o administrador está. Um visitante não autenticado pode estar autorizado a *ler* a lista de eventos, que é pública. As duas coisas são independentes e o back-end precisa checar as duas, sempre, endpoint por endpoint.

### Por que não guardar senha no seu próprio banco (se puder evitar)

Até aqui o UniEventos não tinha usuários — só eventos. Se fôssemos implementar login "na mão", a tentação seria criar uma tabela `usuarios` com uma coluna `senha`. Isso é perigoso por dois motivos:

1. **Nunca se guarda a senha em texto puro.** Se o banco vazar, todas as senhas vazam — e como a maioria das pessoas reutiliza senha entre sites, o estrago vai muito além do seu sistema.
2. **Hash não é criptografia.** Criptografia é reversível (existe uma chave para desfazer). Hash é uma função de mão única: você transforma a senha em uma sequência de caracteres da qual, na prática, não dá para voltar. No login, você faz o hash da senha digitada e compara com o hash guardado — nunca descriptografa nada. Bibliotecas como `bcrypt` fazem isso com "salt" (um valor aleatório por usuário) para que duas pessoas com a mesma senha não gerem o mesmo hash, e com um custo computacional propositalmente alto, para dificultar ataques de força bruta.

Fazer isso corretamente — hash com salt, custo ajustável, fluxo de "esqueci minha senha", verificação de e-mail, proteção contra força bruta, login social — é trabalho considerável e cheio de detalhes fáceis de errar. Por isso, na disciplina (e em grande parte dos projetos reais de pequeno e médio porte) **delegamos a identidade a um provedor especializado**: o Firebase Authentication. Ele guarda a senha (com hash correto, num banco que não é o seu), emite um token assinado provando quem é o usuário, e você só precisa validar esse token.

> **⚠️ Atenção**
> Delegar autenticação não elimina a responsabilidade de proteger seus endpoints. O Firebase resolve "provar quem é o usuário". Decidir "o que esse usuário pode fazer no meu sistema" continua sendo trabalho do seu back-end.

## 2. Anatomia de um JWT

O Firebase (e a grande maioria dos sistemas de autenticação modernos) usa **JSON Web Token (JWT)** como formato do token de identidade. Um JWT é uma string com três partes separadas por ponto:

```text
eyJhbGciOiJSUzI1NiIsImtpZCI6ImFiYzEyMyJ9.eyJuYW1lIjoiTWFyaWEgU2lsdmEiLCJlbWFpbCI6Im1hcmlhQGV4ZW1wbG8uY29tIiwiYWRtaW4iOnRydWUsImlhdCI6MTc2MTQ4MDAwMCwiZXhwIjoxNzYxNDgzNjAwfQ.QqE8f3s1Zx7pR2nL9mK4vT6wY0aB1cD8eF3gH5iJ7kL
```

**header** . **payload** . **assinatura**

Cada parte é um objeto codificado em Base64URL. Decodificando as duas primeiras (a assinatura não se decodifica — ela não é Base64 de um JSON, é um bloco de bytes criptográfico):

**Header** — diz qual algoritmo assinou o token:

```json
{
  "alg": "RS256",
  "kid": "abc123"
}
```

**Payload** — as "claims" (afirmações) sobre o usuário. É aqui que vive a informação:

```json
{
  "name": "Maria Silva",
  "email": "maria@exemplo.com",
  "admin": true,
  "iat": 1761480000,
  "exp": 1761483600
}
```

`iat` (issued at) e `exp` (expiration) são timestamps Unix. `admin` é um exemplo de **custom claim** — vamos usar exatamente isso na seção 6 para autorização.

> **🔎 Por baixo do capô**
> Um JWT **é assinado, não é criptografado**. Qualquer pessoa pode pegar esse token e decodificar o header e o payload num site como jwt.io ou com `atob()` no console do navegador — não há segredo nenhum escondido ali, e por isso **nunca coloque dados sensíveis no payload** (senha, número de cartão, CPF). A assinatura (terceira parte) é o que garante que ninguém alterou o conteúdo sem ter a chave privada do emissor. Se você mudar um único caractere do payload — por exemplo, trocar `"admin": false` para `"admin": true` — a assinatura deixa de bater, e quem valida o token (no nosso caso, o `firebase-admin` no back-end) rejeita o token inteiro.

### Access token × refresh token

O Firebase trabalha com dois tokens:

- **ID token (access token):** de curta duração (1 hora), é o que você envia em cada requisição para provar identidade. É o JWT que acabamos de decodificar.
- **Refresh token:** de longa duração, fica guardado pelo SDK do Firebase e é usado *automaticamente*, nos bastidores, para pedir um novo ID token quando o atual expira — sem exigir que o usuário faça login de novo.

Essa separação existe porque um token de vida curta limita o estrago se ele vazar (ex.: em um log, em uma extensão maliciosa do navegador), enquanto o refresh token, mais sensível, fica protegido e raramente trafega.

> **📌 Na prova**
> JWT tem três partes (header.payload.assinatura), é codificado em Base64URL (não criptografado) e assinado (não pode ser alterado sem invalidar a assinatura). ID token expira em 1h; o SDK renova sozinho usando o refresh token.

## 3. Habilitando autenticação no console do Firebase

No [console do Firebase](https://console.firebase.google.com), projeto do UniEventos:

1. Menu lateral → **Build → Authentication → Get started**.
2. Aba **Sign-in method** → **Add new provider**.
3. Habilite **Email/Password** (o toggle simples, sem "passwordless").
4. Habilite também **Google** — escolha um e-mail de suporte do projeto e salve.

Isso é configuração de infraestrutura, feita uma vez. O código vem agora.

## 4. Firebase Auth no front — SDK modular

O pacote já está instalado desde a Aula 07 (`firebase@12.17.1`). Se o seu projeto ainda não tem, instale:

```bash
npm install firebase@12.17.1
```

```js
// src/services/firebase.js
import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

// Cole aqui o objeto de configuração exibido em
// Configurações do projeto → Geral → Seus apps → Config SDK.
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

const app = initializeApp(firebaseConfig)

export const auth = getAuth(app)
export const db = getFirestore(app)
```

```bash
# .env (na raiz de unieventos-web, sem aspas, sem espaço ao redor do =)
VITE_FIREBASE_API_KEY=AIzaSy...
VITE_FIREBASE_AUTH_DOMAIN=unieventos-xxxxx.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=unieventos-xxxxx
VITE_FIREBASE_STORAGE_BUCKET=unieventos-xxxxx.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abcdef
```

> **⚠️ Atenção**
> `firebase.auth()` com namespace **não existe mais**. A única forma correta no SDK 12 é a API modular: importar funções soltas (`getAuth`, `signInWithEmailAndPassword`, `onAuthStateChanged` etc.) de `'firebase/auth'` e passar a instância `auth` como primeiro argumento. Se você encontrar tutorial usando `firebase.auth().signInWithEmailAndPassword(...)`, está desatualizado — não copie.

Um serviço dedicado para as operações de autenticação, separado do `firebase.js` de inicialização:

```js
// src/services/authService.js
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  updateProfile,
  sendPasswordResetEmail,
  GoogleAuthProvider,
  signInWithPopup,
} from 'firebase/auth'
import { auth } from './firebase'

// Traduz os códigos de erro mais comuns do Firebase Auth para mensagens
// em português — o usuário final não precisa saber o que é "auth/weak-password".
const MENSAGENS_ERRO = {
  'auth/invalid-credential': 'E-mail ou senha incorretos.',
  'auth/invalid-email': 'E-mail em formato inválido.',
  'auth/email-already-in-use': 'Este e-mail já está cadastrado.',
  'auth/weak-password': 'A senha precisa ter pelo menos 6 caracteres.',
  'auth/network-request-failed': 'Falha de conexão. Verifique sua internet.',
  'auth/too-many-requests': 'Muitas tentativas seguidas. Aguarde um instante.',
  'auth/popup-closed-by-user': 'Janela de login fechada antes de concluir.',
}

function traduzirErro(erro) {
  const mensagem = MENSAGENS_ERRO[erro.code]
  return mensagem ?? 'Não foi possível concluir a operação. Tente novamente.'
}

export async function cadastrar(nome, email, senha) {
  try {
    const credencial = await createUserWithEmailAndPassword(auth, email, senha)
    // O Firebase não pede nome no cadastro por e-mail/senha — setamos depois.
    await updateProfile(credencial.user, { displayName: nome })
    return credencial.user
  } catch (erro) {
    throw new Error(traduzirErro(erro))
  }
}

export async function entrar(email, senha) {
  try {
    const credencial = await signInWithEmailAndPassword(auth, email, senha)
    return credencial.user
  } catch (erro) {
    throw new Error(traduzirErro(erro))
  }
}

export async function entrarComGoogle() {
  try {
    const provedor = new GoogleAuthProvider()
    const credencial = await signInWithPopup(auth, provedor)
    return credencial.user
  } catch (erro) {
    throw new Error(traduzirErro(erro))
  }
}

export async function sair() {
  await signOut(auth)
}

export async function solicitarRedefinicaoSenha(email) {
  try {
    await sendPasswordResetEmail(auth, email)
  } catch (erro) {
    throw new Error(traduzirErro(erro))
  }
}

// Registra um observador do estado de login. Retorna a função de
// cancelamento — quem chamar deve guardá-la e invocar ao desmontar.
export function observarAutenticacao(callback) {
  return onAuthStateChanged(auth, callback)
}
```

> **💡 Dica**
> `onAuthStateChanged` dispara sempre que o estado de login muda — login, logout, e também **na primeira carga da página**, depois que o SDK verifica o refresh token salvo no navegador. É esse terceiro caso que vamos explorar na store, a seguir.

## 5. Store de autenticação: resolvendo o problema do F5

Se você guardar o usuário logado só em uma variável reativa comum, ao apertar F5 ela reseta para `null` — mesmo que o usuário continue logado no Firebase. O SDK vai confirmar isso, mas **de forma assíncrona**, alguns milissegundos depois do primeiro render. Se o seu guard de rota checar `usuario` antes desse retorno, ele vai redirecionar um usuário legitimamente logado para a tela de login. É um bug clássico.

A solução: a store expõe uma Promise de inicialização, e o guard de rota **aguarda** essa Promise antes de decidir.

```js
// src/stores/authStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { observarAutenticacao } from '@/services/authService'

export const useAuthStore = defineStore('auth', () => {
  const usuario = ref(null)
  const carregando = ref(false)
  const inicializado = ref(false)

  // Promise única, compartilhada por todos que chamarem inicializar().
  // Evita registrar o observador do Firebase mais de uma vez.
  let promessaInicializacao = null

  function inicializar() {
    if (promessaInicializacao) return promessaInicializacao

    promessaInicializacao = new Promise((resolve) => {
      observarAutenticacao((usuarioFirebase) => {
        usuario.value = usuarioFirebase
        if (!inicializado.value) {
          inicializado.value = true
          resolve() // só resolve no PRIMEIRO disparo do observador
        }
      })
    })

    return promessaInicializacao
  }

  const estaLogado = computed(() => usuario.value !== null)

  // Custom claim "admin" só aparece depois de setCustomUserClaims (seção 7)
  // e de o usuário obter um novo ID token — ver observação na seção 7.
  const ehAdmin = computed(() => usuario.value?.customClaims?.admin === true)

  return { usuario, carregando, inicializado, inicializar, estaLogado, ehAdmin }
})
```

> **🔎 Por baixo do capô**
> `onAuthStateChanged` dispara de novo toda vez que o token é renovado, mas resolvemos a Promise só na **primeira** vez (`if (!inicializado.value)`). Depois disso, os componentes que precisam de reatividade (menu, header) simplesmente leem `usuario` e `estaLogado`, que são refs/computed normais e continuam atualizando sozinhos.

`ehAdmin` como escrito acima lê `customClaims` diretamente do objeto `User` do Firebase, que **não** expõe essa propriedade por padrão — claims custom exigem decodificar o ID token (`getIdTokenResult`). Ajustamos isso corretamente na seção 7, depois de explicar custom claims no back-end; por ora, mantenha o getter, ele será completado adiante.

## 6. Protegendo rotas no Vue Router

```js
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/cadastro',
      name: 'cadastro',
      component: () => import('@/views/CadastroView.vue'),
    },
    {
      path: '/minhas-inscricoes',
      name: 'minhas-inscricoes',
      component: () => import('@/views/MinhasInscricoesView.vue'),
      meta: { requerAuth: true },
    },
    {
      path: '/admin/eventos',
      name: 'admin-eventos',
      component: () => import('@/views/admin/EventosAdminView.vue'),
      meta: { requerAuth: true, requerAdmin: true },
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  // Aguarda o primeiro retorno do onAuthStateChanged antes de decidir
  // qualquer coisa — sem isso, um F5 numa rota protegida redireciona
  // para /login mesmo com o usuário já autenticado.
  await authStore.inicializar()

  if (to.meta.requerAuth && !authStore.estaLogado) {
    return {
      name: 'login',
      query: { redirect: to.fullPath },
    }
  }

  if (to.meta.requerAdmin && !authStore.ehAdmin) {
    return { name: 'home' }
  }

  return true
})

export default router
```

Depois do login, a tela de login redireciona de volta para onde o usuário queria ir:

```vue
<!-- src/views/LoginView.vue (trecho de script) -->
<script setup>
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

async function aoLogarComSucesso() {
  const destino = route.query.redirect || '/'
  router.push(destino)
}
</script>
```

Escondendo itens de menu conforme o estado de login:

```vue
<!-- src/components/BarraNavegacao.vue -->
<script setup>
import { useAuthStore } from '@/stores/authStore'
import { sair } from '@/services/authService'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

async function aoClicarSair() {
  await sair()
  router.push('/login')
}
</script>

<template>
  <v-app-bar>
    <v-app-bar-title>UniEventos</v-app-bar-title>

    <template v-if="!authStore.estaLogado">
      <v-btn to="/login">Entrar</v-btn>
      <v-btn to="/cadastro">Cadastrar</v-btn>
    </template>

    <template v-else>
      <v-btn v-if="authStore.ehAdmin" to="/admin/eventos">Administração</v-btn>
      <v-btn to="/minhas-inscricoes">Minhas inscrições</v-btn>

      <v-menu>
        <template #activator="{ props }">
          <v-avatar v-bind="props" class="mr-2" style="cursor: pointer">
            <v-img
              v-if="authStore.usuario?.photoURL"
              :src="authStore.usuario.photoURL"
              :alt="authStore.usuario.displayName ?? 'Avatar do usuário'"
            />
            <span v-else>{{ authStore.usuario?.email?.[0]?.toUpperCase() }}</span>
          </v-avatar>
        </template>
        <v-list>
          <v-list-item :title="authStore.usuario?.displayName ?? authStore.usuario?.email" />
          <v-list-item title="Sair" @click="aoClicarSair" />
        </v-list>
      </v-menu>
    </template>
  </v-app-bar>
</template>
```

> **⚠️ Atenção**
> Um `beforeEach` no Router impede que a *interface* mostre a tela protegida — mas qualquer pessoa pode desligar o JavaScript, chamar a API diretamente com `curl` ou editar o guard no DevTools. **Guard de rota é UX, não segurança.** A única barreira real está no back-end, validando o token em cada requisição — é o que vem na seção 7.

## 🧩 Padrão de projeto em uso: Proxy de proteção + Guard

O **Proxy de proteção** (variação estrutural do padrão Proxy) intercepta o acesso a um objeto real e decide se o acesso é permitido antes de repassar a chamada. É exatamente o papel do middleware `autenticar` que construímos na seção 7: ele fica *na frente* do controller real, verifica credenciais, e só deixa a chamada prosseguir se o token for válido — o controller nunca sabe que existe um "porteiro" antes dele.

O **Guard** (aqui usado no sentido do Vue Router — um "guarda de rota" comportamental, correlato ao Proxy de proteção do lado do front) cumpre o mesmo papel do lado da navegação: intercepta a transição de rota e decide, antes de renderizar, se ela deve prosseguir, ser bloqueada ou redirecionada. Repare que os dois padrões resolvem o mesmo problema — controlar acesso — em duas camadas diferentes da aplicação, e nenhum substitui o outro.

## 7. Enviando o token em cada requisição

O usuário logado no Firebase tem um método `getIdToken()` que devolve o JWT atual (renovando-o automaticamente se estiver perto de expirar). Plugamos isso no interceptor de requisição do Axios, criado na Aula 06:

```js
// src/services/api.js
import axios from 'axios'
import { auth } from './firebase'
import router from '@/router'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:3000/api',
})

api.interceptors.request.use(async (config) => {
  const usuarioAtual = auth.currentUser

  if (usuarioAtual) {
    // getIdToken() usa o cache do SDK; só bate na rede do Firebase
    // quando o token está perto de expirar (renovação automática).
    const token = await usuarioAtual.getIdToken()
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  (resposta) => resposta,
  (erro) => {
    if (erro.response?.status === 401) {
      // Token ausente, inválido ou expirado sem chance de renovação
      // automática (ex.: usuário revogado no console). Mandamos para
      // o login preservando a rota atual.
      router.push({ name: 'login', query: { redirect: router.currentRoute.value.fullPath } })
    }
    return Promise.reject(erro)
  },
)

export default api
```

> **💡 Dica**
> Não é preciso gerenciar expiração de token manualmente. O SDK do Firebase renova o ID token sozinho (usando o refresh token) sempre que `getIdToken()` é chamado e o token atual está a menos de 5 minutos de expirar. O interceptor de requisição, ao chamar `getIdToken()` antes de cada chamada, já se beneficia disso de graça.

## 8. Verificando o token no back-end com `firebase-admin`

Do lado do cliente, qualquer um pode *afirmar* ser quem quiser — inclusive forjar um cabeçalho `Authorization`. A prova de identidade real só existe quando o back-end valida a assinatura do token contra as chaves públicas do Firebase. É isso que o pacote `firebase-admin` faz.

### 8.1 Gerando a chave de conta de serviço

No console do Firebase: **Configurações do projeto → Contas de serviço → Gerar nova chave privada**. Isso baixa um `.json` com credenciais completas de administrador do projeto — trate como uma senha.

```bash
# unieventos-api/.gitignore
node_modules/
.env
serviceAccountKey.json
```

> **⚠️ Atenção**
> `serviceAccountKey.json` nunca vai para o Git. Se você já commitou por engano, o arquivo precisa ser considerado comprometido: revogue a chave no console (Contas de serviço → gerenciar chaves) e gere outra. Em produção (Render, Railway etc.) prefira uma variável de ambiente com o JSON inteiro codificado em base64, decodificada na inicialização — assim nenhum arquivo sensível precisa existir no disco do servidor.

```bash
# instalação, versão travada conforme especificação da disciplina
npm install firebase-admin@14.2.0
```

```js
// unieventos-api/src/config/firebaseAdmin.js
import { initializeApp, cert, getApps } from 'firebase-admin/app'
import { getAuth } from 'firebase-admin/auth'
import fs from 'node:fs'

function carregarCredencial() {
  // Em produção: variável de ambiente com o JSON em base64.
  if (process.env.FIREBASE_SERVICE_ACCOUNT_BASE64) {
    const json = Buffer.from(process.env.FIREBASE_SERVICE_ACCOUNT_BASE64, 'base64').toString('utf-8')
    return JSON.parse(json)
  }

  // Em desenvolvimento: arquivo local, fora do Git.
  const conteudo = fs.readFileSync(new URL('../../serviceAccountKey.json', import.meta.url), 'utf-8')
  return JSON.parse(conteudo)
}

// getApps() evita inicializar duas vezes se este módulo for importado
// em mais de um lugar (ex.: em testes).
if (getApps().length === 0) {
  initializeApp({ credential: cert(carregarCredencial()) })
}

export const authAdmin = getAuth()
```

### 8.2 Middleware `autenticar`

```js
// unieventos-api/src/middlewares/autenticar.js
import { authAdmin } from '../config/firebaseAdmin.js'

export async function autenticar(req, res, next) {
  const cabecalho = req.headers.authorization

  if (!cabecalho?.startsWith('Bearer ')) {
    return res.status(401).json({ erro: 'Token de autenticação ausente.' })
  }

  const token = cabecalho.replace('Bearer ', '')

  try {
    const tokenDecodificado = await authAdmin.verifyIdToken(token)

    // Popula req.usuario para os middlewares e controllers seguintes
    // usarem — igual fizemos com req.body validado na Aula 08.
    req.usuario = {
      uid: tokenDecodificado.uid,
      email: tokenDecodificado.email,
      admin: tokenDecodificado.admin === true, // custom claim, seção 8.4
    }

    next()
  } catch (erro) {
    // Cobre token expirado, assinatura inválida, token forjado etc.
    return res.status(401).json({ erro: 'Token inválido ou expirado.' })
  }
}
```

Express 5 captura erros de handlers `async` automaticamente (Aula 08), mas aqui usamos `try/catch` de propósito: um token inválido não é um erro inesperado do servidor (500), é uma resposta de negócio esperada (401). Deixar o `errorHandler` central tratar isso como 500 estaria errado.

### 8.3 Middleware `autorizar`

```js
// unieventos-api/src/middlewares/autorizar.js
export function autorizar(papeis = []) {
  return (req, res, next) => {
    if (!req.usuario) {
      // autenticar() deve sempre rodar antes de autorizar() na cadeia
      return res.status(401).json({ erro: 'Token de autenticação ausente.' })
    }

    const temPermissao = papeis.includes('admin') ? req.usuario.admin : true

    if (!temPermissao) {
      return res.status(403).json({ erro: 'Você não tem permissão para esta ação.' })
    }

    next()
  }
}
```

> **🔎 Por baixo do capô**
> 401 (*Unauthorized*) significa "eu não sei quem você é" — token ausente ou inválido. 403 (*Forbidden*) significa "eu sei quem você é, mas você não pode fazer isso" — token válido, mas sem a permissão necessária. Misturar os dois confunde quem está depurando o front.

### 8.4 Custom claims: marcando um usuário como admin

Custom claims são pares chave-valor extras que o Firebase embute no payload do JWT, definidos pelo back-end (nunca pelo próprio usuário). Um script único, rodado manualmente, promove um usuário a administrador:

```js
// unieventos-api/scripts/promoverAdmin.js
// Uso: node scripts/promoverAdmin.js email@exemplo.com
import '../src/config/firebaseAdmin.js'
import { getAuth } from 'firebase-admin/auth'

const email = process.argv[2]

if (!email) {
  console.error('Uso: node scripts/promoverAdmin.js <email>')
  process.exit(1)
}

const auth = getAuth()
const usuario = await auth.getUserByEmail(email)

await auth.setCustomUserClaims(usuario.uid, { admin: true })

console.log(`${email} agora é administrador.`)
```

```bash
node scripts/promoverAdmin.js professor@unemat.br
```

> **⚠️ Atenção**
> Custom claims só aparecem em um **novo** ID token. Se o usuário já estava logado quando você rodou o script, ele precisa deslogar e logar de novo (ou o front precisa forçar `getIdToken(true)`, com `true` pedindo renovação forçada) para o token trazer `admin: true`. É um erro comum: "rodei o script e continua sem permissão" — o token antigo, em cache no navegador, simplesmente ainda não tem a claim.

Com isso, completamos o `ehAdmin` da store (seção 5), que ficou pendente. A forma correta de ler a claim no front é via `getIdTokenResult()`, não pela propriedade `customClaims` (que não existe no objeto `User`):

```js
// src/stores/authStore.js — ajuste da action inicializar()
function inicializar() {
  if (promessaInicializacao) return promessaInicializacao

  promessaInicializacao = new Promise((resolve) => {
    observarAutenticacao(async (usuarioFirebase) => {
      if (usuarioFirebase) {
        const resultado = await usuarioFirebase.getIdTokenResult()
        usuario.value = usuarioFirebase
        ehAdminClaim.value = resultado.claims.admin === true
      } else {
        usuario.value = null
        ehAdminClaim.value = false
      }

      if (!inicializado.value) {
        inicializado.value = true
        resolve()
      }
    })
  })

  return promessaInicializacao
}
```

```js
// e trocar o computed ehAdmin por uma ref simples atualizada acima
const ehAdminClaim = ref(false)
const ehAdmin = computed(() => ehAdminClaim.value)
```

### 8.5 Aplicando nos endpoints de eventos

```js
// unieventos-api/src/routes/eventosRoutes.js
import { Router } from 'express'
import { autenticar } from '../middlewares/autenticar.js'
import { autorizar } from '../middlewares/autorizar.js'
import * as eventosController from '../controllers/eventosController.js'

const router = Router()

// Leitura pública — qualquer visitante, sem token, vê os eventos
router.get('/', eventosController.listar)
router.get('/:id', eventosController.buscarPorId)

// Escrita exige apenas estar autenticado
router.post('/', autenticar, eventosController.criar)
router.put('/:id', autenticar, eventosController.atualizar)

// Exclusão exige estar autenticado E ser admin
router.delete('/:id', autenticar, autorizar(['admin']), eventosController.remover)

export default router
```

## 💻 Mão na massa — telas de autenticação completas

### Passo 1 — Tela de cadastro

```vue
<!-- src/views/CadastroView.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { cadastrar } from '@/services/authService'

const router = useRouter()

const nome = ref('')
const email = ref('')
const senha = ref('')
const confirmarSenha = ref('')
const erro = ref('')
const carregando = ref(false)

const regraObrigatorio = (v) => !!v || 'Campo obrigatório'
const regraEmail = (v) => /.+@.+\..+/.test(v) || 'E-mail inválido'
const regraSenhaMinima = (v) => v.length >= 6 || 'Mínimo de 6 caracteres'
const regraSenhasIguais = (v) => v === senha.value || 'As senhas não coincidem'

async function aoSubmeter() {
  erro.value = ''
  carregando.value = true
  try {
    await cadastrar(nome.value, email.value, senha.value)
    router.push('/')
  } catch (e) {
    erro.value = e.message
  } finally {
    carregando.value = false
  }
}
</script>

<template>
  <v-container class="d-flex align-center justify-center" style="min-height: 80vh">
    <v-card max-width="420" width="100%" class="pa-4">
      <v-card-title>Criar conta</v-card-title>

      <v-form @submit.prevent="aoSubmeter">
        <v-card-text>
          <v-alert v-if="erro" type="error" class="mb-4" density="compact">
            {{ erro }}
          </v-alert>

          <v-text-field
            v-model="nome"
            label="Nome completo"
            :rules="[regraObrigatorio]"
          />
          <v-text-field
            v-model="email"
            label="E-mail"
            type="email"
            :rules="[regraObrigatorio, regraEmail]"
          />
          <v-text-field
            v-model="senha"
            label="Senha"
            type="password"
            :rules="[regraObrigatorio, regraSenhaMinima]"
          />
          <v-text-field
            v-model="confirmarSenha"
            label="Confirmar senha"
            type="password"
            :rules="[regraObrigatorio, regraSenhasIguais]"
          />
        </v-card-text>

        <v-card-actions>
          <v-btn type="submit" color="primary" block :loading="carregando">
            Cadastrar
          </v-btn>
        </v-card-actions>
      </v-form>

      <v-card-text class="text-center">
        Já tem conta? <router-link to="/login">Entrar</router-link>
      </v-card-text>
    </v-card>
  </v-container>
</template>
```

### Passo 2 — Tela de login, com Google e redirecionamento

```vue
<!-- src/views/LoginView.vue -->
<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { entrar, entrarComGoogle, solicitarRedefinicaoSenha } from '@/services/authService'

const route = useRoute()
const router = useRouter()

const email = ref('')
const senha = ref('')
const erro = ref('')
const mensagemSucesso = ref('')
const carregando = ref(false)

function irParaDestino() {
  const destino = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
  router.push(destino)
}

async function aoSubmeter() {
  erro.value = ''
  carregando.value = true
  try {
    await entrar(email.value, senha.value)
    irParaDestino()
  } catch (e) {
    erro.value = e.message
  } finally {
    carregando.value = false
  }
}

async function aoClicarGoogle() {
  erro.value = ''
  carregando.value = true
  try {
    await entrarComGoogle()
    irParaDestino()
  } catch (e) {
    erro.value = e.message
  } finally {
    carregando.value = false
  }
}

async function aoEsquecerSenha() {
  erro.value = ''
  mensagemSucesso.value = ''
  if (!email.value) {
    erro.value = 'Informe o e-mail para receber o link de redefinição.'
    return
  }
  try {
    await solicitarRedefinicaoSenha(email.value)
    mensagemSucesso.value = 'Enviamos um link de redefinição para o seu e-mail.'
  } catch (e) {
    erro.value = e.message
  }
}
</script>

<template>
  <v-container class="d-flex align-center justify-center" style="min-height: 80vh">
    <v-card max-width="420" width="100%" class="pa-4">
      <v-card-title>Entrar</v-card-title>

      <v-form @submit.prevent="aoSubmeter">
        <v-card-text>
          <v-alert v-if="erro" type="error" class="mb-4" density="compact">
            {{ erro }}
          </v-alert>
          <v-alert v-if="mensagemSucesso" type="success" class="mb-4" density="compact">
            {{ mensagemSucesso }}
          </v-alert>

          <v-text-field v-model="email" label="E-mail" type="email" />
          <v-text-field v-model="senha" label="Senha" type="password" />

          <v-btn variant="text" size="small" @click="aoEsquecerSenha">
            Esqueci minha senha
          </v-btn>
        </v-card-text>

        <v-card-actions class="flex-column">
          <v-btn type="submit" color="primary" block :loading="carregando">
            Entrar
          </v-btn>
          <v-btn
            variant="outlined"
            block
            class="mt-2"
            prepend-icon="mdi-google"
            :loading="carregando"
            @click="aoClicarGoogle"
          >
            Entrar com Google
          </v-btn>
        </v-card-actions>
      </v-form>

      <v-card-text class="text-center">
        Não tem conta? <router-link to="/cadastro">Cadastrar</router-link>
      </v-card-text>
    </v-card>
  </v-container>
</template>
```

### Passo 3 — Inicializando a store no `main.js`

```js
// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from '@/stores/authStore'

import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'

const vuetify = createVuetify({ theme: { defaultTheme: 'light' } })

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(vuetify)

// Dispara a inicialização o quanto antes; o router aguarda a mesma
// Promise no beforeEach, então não há corrida entre os dois.
useAuthStore().inicializar()

app.mount('#app')
```

### Passo 4 — Área administrativa protegida

```vue
<!-- src/views/admin/EventosAdminView.vue -->
<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()

onMounted(() => {
  // Se chegou até aqui, o guard de rota já garantiu requerAuth + requerAdmin.
  console.log('Admin logado:', authStore.usuario.email)
})
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-4">Administração de eventos</h1>
    <p>Bem-vindo(a), {{ authStore.usuario?.displayName ?? authStore.usuario?.email }}.</p>
    <!-- CRUD completo de eventos vem na Aula 11 -->
  </v-container>
</template>
```

### Passo 5 — Testando a API manualmente

Sem token — deve retornar 401:

```bash
curl -i http://localhost:3000/api/eventos -X POST \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Semana da Computação"}'
```

Com token inválido (qualquer string) — também 401:

```bash
curl -i http://localhost:3000/api/eventos -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token-forjado-qualquer" \
  -d '{"titulo":"Semana da Computação"}'
```

Com token válido — copie o token real do DevTools (aba Network, requisição feita pelo front logado, cabeçalho `Authorization`) e cole aqui:

```bash
curl -i http://localhost:3000/api/eventos -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer COLE_O_TOKEN_AQUI" \
  -d '{"titulo":"Semana da Computação","categoria":"palestra","data_hora":"2026-12-01T19:00:00","local":"Auditório","vagas":80}'
```

Tentando excluir sem ser admin (usuário autenticado comum) — deve retornar 403:

```bash
curl -i http://localhost:3000/api/eventos/1 -X DELETE \
  -H "Authorization: Bearer TOKEN_DE_USUARIO_COMUM"
```

## 🧪 Laboratório

**1. Cadastro e login funcionando.** Crie uma conta pelo formulário de cadastro do seu projeto autoral, faça logout e faça login de novo.
<details><summary>Dica</summary>Abra o DevTools → Application → verifique se há chaves salvas pelo Firebase no IndexedDB/LocalStorage após o login.</details>

**2. Login com Google.** Habilite o provedor Google no console e teste `entrarComGoogle()`.
<details><summary>Dica</summary>Se o popup fechar sozinho sem erro visível, confira o console — geralmente é domínio não autorizado em Authentication → Settings → Authorized domains.</details>

**3. Rota protegida.** Crie uma rota `meta: { requerAuth: true }` no seu projeto e confirme que, deslogado, você é redirecionado para `/login?redirect=...` e volta para a rota certa após logar.
<details><summary>Dica</summary>Teste apertando F5 na rota protegida já logado — não pode redirecionar para login.</details>

**4. Middleware `autenticar` na API.** Proteja um endpoint de escrita do seu projeto autoral e teste os três cenários de `curl` da seção anterior.
<details><summary>Dica</summary>Um token expira em 1h — se testar depois de muito tempo, gere outro logando de novo no front.</details>

**5. Custom claim de admin.** Rode o script `promoverAdmin.js` com seu próprio e-mail, deslogue e logue de novo, e confirme que `authStore.ehAdmin` fica `true` e que o menu de administração aparece.
<details><summary>Dica</summary>Se continuar `false`, o token em cache é o antigo — force `getIdTokenResult(true)` ou deslogue mesmo.</details>

## 🐛 Erros comuns e como resolver

| Sintoma | Causa | Solução |
|---|---|---|
| 401 mesmo logado no front | Interceptor não aguardou `getIdToken()` (esqueceu `await`) | Confirme que a função do interceptor é `async` e usa `await usuarioAtual.getIdToken()` |
| Guard redireciona para login mesmo autenticado, só no F5 | `beforeEach` não aguardou `inicializar()` | Adicione `await authStore.inicializar()` como primeira linha do guard |
| "auth/network-request-failed" | Sem internet, ou domínio bloqueado por extensão/firewall | Verificar conexão; testar em aba anônima sem extensões |
| Token válido no Postman mas 401 na API | Relógio do servidor fora de sincronia (token "ainda não válido" ou "expirado" por diferença de horário) | Sincronizar o relógio do servidor (NTP); em nuvem isso raramente acontece, mas em VM local pode |
| CORS bloqueia a requisição com `Authorization` | `cors()` no Express sem liberar o header customizado | Configurar `cors({ origin: 'http://localhost:5173', allowedHeaders: ['Content-Type', 'Authorization'] })` |
| `admin` sempre `false` mesmo após `setCustomUserClaims` | Token antigo em cache, claim não propagada | Deslogar e logar de novo, ou `getIdTokenResult(true)` para forçar renovação |
| `req.usuario` é `undefined` no controller | `autorizar` usado sem `autenticar` antes na cadeia de middlewares | Sempre montar a rota como `autenticar, autorizar([...])`, nessa ordem |

## 🏠 Atividade assíncrona (1 h)

No seu projeto autoral: implemente cadastro, login, logout e proteção de pelo menos uma rota do front (`requerAuth: true`) e um endpoint de escrita da API (`autenticar`). Grave um GIF ou vídeo curto (menos de 1 minuto) mostrando: (1) tentativa de acessar a rota protegida deslogado sendo redirecionada, (2) login, (3) acesso liberado, (4) `curl` sem token retornando 401. Suba o material (código + evidência) no repositório do projeto e envie o link pelo SIGAA.

**Critério de pronto:** os quatro passos do vídeo aparecem, e o commit com a implementação está no repositório.

## ✅ Checkpoint do projeto autoral

- [ ] `src/services/firebase.js` inicializado com variáveis de ambiente (nada de chave hardcoded no código).
- [ ] Cadastro, login, logout e login com Google funcionando na interface.
- [ ] `stores/authStore.js` com `inicializar()`, `estaLogado` e `ehAdmin` implementados corretamente.
- [ ] Pelo menos uma rota protegida com `meta: { requerAuth: true }` funcionando após F5.
- [ ] Interceptor Axios enviando `Authorization: Bearer <token>` em toda requisição autenticada.
- [ ] API com `firebase-admin` configurado e `serviceAccountKey.json` fora do Git.
- [ ] Pelo menos um endpoint de escrita protegido por `autenticar`, e um por `autorizar(['admin'])`.
- [ ] Testes manuais com `curl` (sem token, token inválido, token válido) documentados.

## 📚 Para aprofundar

- [Firebase Auth — Web (modular)](https://firebase.google.com/docs/auth/web/start)
- [Firebase Auth — gerenciar usuários com o Admin SDK](https://firebase.google.com/docs/auth/admin/manage-users)
- [Custom claims — documentação oficial](https://firebase.google.com/docs/auth/admin/custom-claims)
- [jwt.io — debugger de JWT](https://jwt.io)
- [RFC 7519 — JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- Plano de curso, Unidade 3: Firebase, autenticação e banco de dados.

Na Aula 11 fechamos o ciclo: CRUD completo de eventos, ponta a ponta, autenticado — Vue consumindo a API Express, que persiste no MySQL, tudo validado com o token do Firebase que construímos hoje.
