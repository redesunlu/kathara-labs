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

 2. Iniciar captura de ambas redes [A y B]. En el caso de capturar en el host, se recomienda filtrar el tráfico ipv6, por ejemplo usando tshark, para capturar en todas las interfaces que comiencen con `kt-` filtrando ipv6:
 ```
 $ sudo tshark -w tcp_retransmission.pcap $(brctl show | grep "^kt-" | cut -f1 | sed 's/^/-i /' | tr '\n' ' ') -f 'not ip6'
 Running as user "root" and group "root". This could be dangerous.
Capturing on 'kt-0faddb491144' and 'kt-32b3756214ac'
_
```

 3. Para correr el servidor, ejecutar en PC2:
 ```
root@pc2:/#  dd if=/dev/urandom count=5 bs=1400 | nc -l -p 8080
5+0 records in
5+0 records out
7000 bytes (7.0 kB, 6.8 KiB) copied, 0.000143594 s, 48.7 MB/s
```
 4. Ejecutar en PC1: 
 ```
root@pc1:/# nc -v -w 3 192.168.1.10 8080 > un_archivo
Connection to 192.168.1.10 8080 port [tcp/http-alt] succeeded!
 ```
