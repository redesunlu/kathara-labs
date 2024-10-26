# Ejemplo laboratorio con pérdida de paquetes y/o latencia

## Ambiente
 - PC1: 192.168.0.10 [Red A]
 - Router: 192.168.0.1 [Red A] | 192.168.1.1 [Red B]
 - PC2: 192.168.1.10 [Red B]

## Ejemplo captura:
 1. Iniciar laboratorio.
 Por defecto el router como script de inicio corre:
```
/sbin/ifconfig eth0 192.168.0.1 up
/sbin/ifconfig eth1 192.168.1.1 up

tc qdisc add dev eth0 root netem delay 100ms loss 50%
```
Por lo que simula un retardo de 100 milisegundos y una pérdida de paquetes del 50% sobre la interfaz eth0. Para más información, ver el archivo `router1.startup`.


 2. Para correr el servidor, ejecutar en PC2:
 ```
 root@pc2:/# dd if=/dev/urandom count=10 bs=1500 | nc -l -p 8080
10+0 records in
10+0 records out
15000 bytes (15 kB, 15 KiB) copied, 0.000130125 s, 115 MB/s
```
 3. Iniciar captura de ambas redes [A y B]
 4. Ejecutar en PC1: 
 ```
nc -v -w 3 192.168.1.10 8080 > un_archivo
Connection to 192.168.1.10 8080 port [tcp/http-alt] succeeded!
 ```
