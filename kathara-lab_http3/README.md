# HTTP/1.1, HTTP/2, HTTP/3 Server examples

1. Start the lab: `kathara lstart`
1. Start capturing in the host machine: `wireshark xxxx`
1. In the client terminal window:
 - Run the HTTP/1.1 example request:
```console
root@client:/# curl -v http://192.168.1.1/index.html
*   Trying 192.168.1.1:80...
* Connected to 192.168.1.1 (192.168.1.1) port 80 (#0)
> GET /index.html HTTP/1.1
> Host: 192.168.1.1
> User-Agent: curl/7.88.1
> Accept: */*
>
< HTTP/1.1 200 OK
< Date: Wed, 27 Mar 2024 21:11:50 GMT
< Server: Apache/2.4.57 (Debian)
< Last-Modified: Wed, 27 Mar 2024 21:08:53 GMT
< ETag: "f1-614aad05cc340"
< Accept-Ranges: bytes
< Content-Length: 241
< Vary: Accept-Encoding
< Content-Type: text/html
<
<html>
    <body><h1>Bienvenido!</h1>
    <p>Esta es la pagina que usted deberia estar viendo via HTTP/1.1.</p>
    <p>Valide que pudo acceder a ella a traves del protocolo HTTP 1.1, analizando la captura del dialogo.</p>
    </body>
* Connection #0 to host 192.168.1.1 left intact
```
 - Run the HTTP/2 example request:
```console
>root@client:/# curl -v http://192.168.1.2/index.html --http2
*   Trying 192.168.1.2:80...
* Connected to 192.168.1.2 (192.168.1.2) port 80 (#0)
> GET /index.html HTTP/1.1
> Host: 192.168.1.2
> User-Agent: curl/7.88.1
> Accept: */*
> Connection: Upgrade, HTTP2-Settings
> Upgrade: h2c
> HTTP2-Settings: AAMAAABkAAQCAAAAAAIAAAAA
>
< HTTP/1.1 101 Switching Protocols
< Upgrade: h2c
< Connection: Upgrade
* Received 101, Switching to HTTP/2
< HTTP/2 200
< last-modified: Wed, 27 Mar 2024 21:08:53 GMT
< etag: W/"ed-614aad05cc340"
< accept-ranges: bytes
< content-length: 237
< vary: Accept-Encoding
< content-type: text/html
< date: Sun, 00 Jan 1900 00:00:00 GMT
< server: Apache/2.4.57 (Debian)
<
<html>
    <body><h1>Bienvenido!</h1>
    <p>Esta es la pagina que usted deberia estar viendo via HTTP/2.</p>
    <p>Valide que pudo acceder a ella a traves del protocolo HTTP 2, analizando la captura del dialogo.</p>
    </body>
* Connection #0 to host 192.168.1.2 left intact
```
 - Run the HTTP/3 example request: # TODO - WIP