# Servidor — weblab.aprendabit.com

Como o WebLab é publicado e onde cada coisa vive no VPS.

## Resumo

| Item | Valor |
|---|---|
| URL | <https://weblab.aprendabit.com> (HTTP → 301 → HTTPS) |
| URL anterior | <https://weblab.ivanpires.dev> — continua servindo o mesmo diretório; as páginas declaram `canonical` para o domínio novo |
| Host | `ivanpires.dev` (VPS Ubuntu 22.04, nginx 1.18) |
| Usuário de publicação | `webmaster@ivanpires.dev` (chave SSH já instalada) |
| Raiz do site | `/home/webmaster/apps/weblab/site/` |
| Vhost nginx | `/etc/nginx/sites-available/weblab.aprendabit.com` e `.../weblab.ivanpires.dev` (ambos com link em `sites-enabled/` e apontando para a mesma raiz) |
| Certificado | Let's Encrypt, `/etc/letsencrypt/live/weblab.aprendabit.com/` (renovação automática pelo `certbot.timer`) |
| Logs | `/var/log/nginx/weblab.access.log`, `/var/log/nginx/weblab.error.log` |

## Republicar

```bash
./deploy.sh            # lint + build completo + rsync
./deploy.sh --parcial  # só as aulas que existem (durante a escrita)
./deploy.sh --forcar   # ignora erros de lint (pré-visualização)
```

O script roda `build/build.py` e depois:

```bash
rsync -az --delete --chmod=D755,F644 site/ webmaster@ivanpires.dev:/home/webmaster/apps/weblab/site/
```

Não há passo no servidor: nginx serve os arquivos estáticos direto da pasta. Conferir depois: `curl -sI https://weblab.aprendabit.com/ | head -1` (200) e `curl -s -o /dev/null -w "%{http_code}\n" https://weblab.aprendabit.com/nao-existe` (404).

## Vhost

```nginx
server {
    server_name weblab.aprendabit.com;
    root /home/webmaster/apps/weblab/site;
    index index.html;
    charset utf-8;

    gzip on;
    gzip_types text/html text/css application/javascript application/json image/svg+xml text/plain application/xml;
    gzip_min_length 1024;

    location / {
        try_files $uri $uri/ $uri.html =404;
    }

    location = /busca.json {
        add_header Cache-Control "public, max-age=3600";
    }

    error_page 404 /404.html;
    access_log /var/log/nginx/weblab.access.log;
    error_log  /var/log/nginx/weblab.error.log;

    listen 443 ssl;                     # blocos "managed by Certbot"
    ssl_certificate     /etc/letsencrypt/live/weblab.aprendabit.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/weblab.aprendabit.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = weblab.aprendabit.com) { return 301 https://$host$request_uri; }
    listen 80;
    server_name weblab.aprendabit.com;
    return 404;
}
```

## Acesso root (para mexer no nginx/certbot)

O usuário `webmaster` não tem sudo. Root só via contêiner privilegiado:

```bash
ssh webmaster@ivanpires.dev
docker run --rm -it --privileged --pid=host --net=host -v /:/host redis:7-alpine chroot /host /bin/bash
# dentro: nginx -t && systemctl reload nginx ; certbot certificates ; certbot renew --dry-run
```

## Como foi criado

1. `ssh webmaster@ivanpires.dev 'mkdir -p /home/webmaster/apps/weblab/site'` e primeiro `./deploy.sh --parcial`.
2. Registro DNS `A` de `weblab.aprendabit.com` apontando para o IP do VPS (mesmo IP de `ivanpires.dev`).
3. Vhost acima em `sites-available/`, link em `sites-enabled/`, `nginx -t && systemctl reload nginx`.
4. `certbot --nginx -d weblab.aprendabit.com` (adicionou os blocos SSL e o redirect 80 → 443).

## Trocar o domínio ou o servidor

Só três lugares sabem o endereço: `build/config.py` (`URL_BASE`, usado no `sitemap.xml`), `deploy.sh` (`DESTINO`) e o vhost. Nada no conteúdo das aulas depende do domínio.

## Migração de domínio (agosto de 2026)

O site passou a ser publicado em **weblab.aprendabit.com**; `weblab.ivanpires.dev` continua no ar, servindo o mesmo diretório, para não quebrar links já divulgados. As páginas trazem `<link rel="canonical">` apontando para o domínio novo, e `sitemap.xml` e `CITATION.cff` usam apenas ele — então buscadores e citações convergem para `aprendabit.com` sem que ninguém receba 404.

Quando quiser aposentar o endereço antigo de vez, troque o corpo do vhost `weblab.ivanpires.dev` por um redirecionamento permanente:

```nginx
server {
    listen 443 ssl;
    server_name weblab.ivanpires.dev;
    # ... blocos de certificado gerados pelo certbot ...
    return 301 https://weblab.aprendabit.com$request_uri;
}
```

Três lugares sabem o endereço: `URL_BASE` em `build/config.py`, `DESTINO` em `deploy.sh` e os vhosts. Nada no conteúdo das aulas depende do domínio.
