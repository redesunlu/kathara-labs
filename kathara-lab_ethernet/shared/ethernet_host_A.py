#!/usr/bin/env python3
"""
Script Host A - Intercambio de Tramas Ethernet (Capa 2)
======================================================
Este script envía una trama Ethernet personalizada a otro host en la misma LAN.
Los estudiantes pueden capturar esta trama con Wireshark y analizar los campos
de la capa de enlace de datos (Capa 2 del modelo OSI).

Campos importantes de Ethernet para observar en Wireshark:
- Dirección MAC de destino (dst)
- Dirección MAC de origen (src)
- EtherType (tipo de protocolo encapsulado)
- Payload (datos transportados)

NOTA: Requiere privilegios de administrador (sudo) para enviar tramas raw.
"""

from scapy.all import Ether, sendp, conf
import sys

# Configuración para visualizar mejor los paquetes
conf.verb = 1  # Nivel de verbosidad (0=silencioso, 1=normal, 2=verbose)

def enviar_trama_ethernet():
    """
    Crea y envía una trama Ethernet personalizada.
    """
    
    print("=" * 60)
    print("HOST A - ENVIANDO TRAMA ETHERNET (Capa 2)")
    print("=" * 60)
    
    # Configuración de direcciones MAC
    # IMPORTANTE: Modificar estas direcciones según tu laboratorio
    mac_destino = "02:42:ac:11:00:02"  # Broadcast - llega a todos en la LAN
    mac_origen = "02:42:ac:11:00:01"   # MAC de ejemplo para Host A
    
    # Especificar la interfaz de red a usar
    # En Linux: eth0, wlan0, etc.
    # En macOS: en0, en1, etc.
    # En Windows: usar el nombre completo de la interfaz
    interfaz = "eth0"  # Modificar según tu sistema
    
    print(f"\n[*] Configuración:")
    print(f"    - Interfaz: {interfaz}")
    print(f"    - MAC Origen: {mac_origen}")
    print(f"    - MAC Destino: {mac_destino}")
    
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
    mensaje = b"Hola desde Host A - Trama Ethernet Capa 2"
    trama = trama / mensaje
    
    print(f"    - Payload: {mensaje.decode('utf-8')}")
    print(f"    - EtherType: 0x{trama.type:04x}")
    
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
        print("\n[INFO] Instrucciones para captura:")
        print(f"      1. Ejecutar Wireshark y capturar en interfaz '{interfaz}'")
        print(f"      2. Filtrar por: eth.addr == {mac_origen}")
        print(f"      3. Observar los campos de la trama Ethernet:")
        print("         - Destination MAC")
        print("         - Source MAC")
        print("         - EtherType")
        print("         - Payload (datos)")
        
    except PermissionError:
        print("\n[ERROR] Se requieren privilegios de administrador.")
        print("        Ejecutar con: sudo python3 ethernet_host_A.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error al enviar trama: {e}")
        print(f"        Verificar que la interfaz '{interfaz}' existe y está activa.")
        sys.exit(1)

if __name__ == "__main__":
    print("\n[!] IMPORTANTE: Este script requiere privilegios de administrador")
    print("    Ejecutar con: sudo python3 ethernet_host_A.py\n")
    
    try:
        enviar_trama_ethernet()
    except KeyboardInterrupt:
        print("\n\n[*] Proceso interrumpido por el usuario.")
        sys.exit(0)
