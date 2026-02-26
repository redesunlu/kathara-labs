#!/usr/bin/env python3
"""
ethernet_sender_host.py - Emisor de tramas Ethernet (Capa 2)
============================================================
Este script envía una trama Ethernet personalizada a una MAC de otro host en la misma LAN.
Los estudiantes pueden capturar esta trama con Wireshark y analizar los campos de la capa 
de enlace de datos (Capa 2 del modelo OSI).

Campos importantes de Ethernet para observar en Wireshark:
- Dirección MAC de destino (dst)
- Dirección MAC de origen (src)
- EtherType (tipo de protocolo encapsulado)
- Payload (datos transportados)

NOTA: Requiere privilegios de administrador (sudo) para enviar tramas raw.
"""

from scapy.all import Ether, sendp, conf, get_if_hwaddr, Padding
import sys

MIN_ETHERNET_FRAME = 64  # Mínimo de bytes para el payload de Ethernet (46 bytes de datos + 18 bytes de cabecera = 64 bytes)

# Configuración para visualizar mejor los paquetes
conf.verb = 1  # Nivel de verbosidad (0=silencioso, 1=normal, 2=verbose)

def enviar_trama_ethernet(dst_mac, mensaje):
	"""
	Crea y envía una trama Ethernet personalizada.
	"""
	# Especificar la interfaz de red a usar
	# En Linux: eth0, wlan0, etc.
	# En macOS: en0, en1, etc.
	# En Windows: usar el nombre completo de la interfaz
	interfaz = "eth0"  # Modificar según tu sistema

	# Configuración de direcciones MAC
	mac_destino = dst_mac 
	mac_origen  = get_if_hwaddr("eth0")
	print("=" * 60)
	print("Enviando desde ", mac_origen, "a", mac_destino, " : ", mensaje)
	print("=" * 60)

	# Construcción de la trama Ethernet
	# Ether() crea una trama de capa 2
	trama = Ether(
		dst=mac_destino,     # Dirección MAC de destino (6 bytes)
		src=mac_origen,      # Dirección MAC de origen (6 bytes)
		type=0x9000          # EtherType personalizado (experimental)
							 # 0x0800 = IPv4, 0x0806 = ARP, 0x86DD = IPv6
	)
    
    # Agregar datos (payload) a la trama
    # En este caso, un mensaje simple en texto
	trama = trama / str(mensaje)
    
	#print(f" - Payload: {mensaje.decode('utf-8')}")
	#print(f" - EtherType: 0x{trama.type:04x}")

	# Chequeo si el padding es necesario y lo agrego en tal caso
	# Comentado porque no es necesario para el ejercicio, pero lo dejo como referencia
	# if len(trama) < MIN_ETHERNET_FRAME:
	# 	pad_len = MIN_ETHERNET_FRAME - len(trama)
	# 	# Crear un objecto Padding con la longitud requerida de ceros
	# 	# Puedes usar cualquier valor de byte para la carga de padding, aquí uso ceros
	# 	pad = Padding(load=b'\x00' * pad_len)
	# 	# Apilar el padding a la trama original
	# 	trama = trama / pad
	# 	print(f" - Padding agregado: {pad_len} bytes para alcanzar el mínimo de {MIN_ETHERNET_FRAME} bytes")
	# 	print(f" - Longitud de la trama con padding: {len(trama)} bytes")

	# Mostrar resumen de la trama construida
	print(f"\n[*] Trama construida:")
	trama.show()

	# Enviar la trama en la red
	print(f"\n[*] Enviando trama por interfaz {interfaz}...")
	try:
		# sendp() envía paquetes en capa 2 (con cabecera Ethernet)
		# iface= especifica la interfaz de red a usar
		sendp(trama, iface=interfaz, verbose=True)
		print("\n[✓] Trama enviada exitosamente!")        
	except PermissionError:
		print("\n[ERROR] Se requieren privilegios de administrador.")
		print("        Ejecutar con: sudo python3 ethernet_sender_host.py")
		sys.exit(1)
	except Exception as e:
		print(f"\n[ERROR] Error al enviar trama: {e}")
		print(f"        Verificar que la interfaz '{interfaz}' existe y está activa.")
	sys.exit(1)

if __name__ == "__main__":
	print("\n[!] IMPORTANTE: Este script requiere privilegios de administrador")
	print("    Ejecutar con: sudo python3 ethernet_sender_host.py\n")

	if len(sys.argv) != 3:
		print("Uso: sudo python3 ethernet_sender_host.py <mac_destino> <mensaje>")
		print()
		print("Parámetros:")
		print("  mac_destino  Dirección MAC destino (ej: aa:bb:cc:dd:ee:ff)")
		print("  mensaje      Mensaje a enviar como payload de la trama")
		print()
		print("Ejemplo:")
		print("  sudo python3 ethernet_sender_host.py aa:bb:cc:dd:ee:ff 'Hola mundo'")
		sys.exit(1)

	dst_mac = sys.argv[1]
	mensaje = sys.argv[2]

	try:
		enviar_trama_ethernet(dst_mac, mensaje)
	except KeyboardInterrupt:
		print("\n\n[*] Proceso interrumpido por el usuario.")
	sys.exit(0)
