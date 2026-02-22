#!/usr/bin/env python3
"""
Script Host B - Recepción de Tramas Ethernet (Capa 2)
====================================================
Este script escucha tramas Ethernet en la interfaz de red y muestra
las que coincidan con el filtro especificado. Permite a los estudiantes
ver en tiempo real las tramas recibidas y sus campos de capa 2.

Los estudiantes pueden ejecutar este script mientras capturan con Wireshark
para ver tanto en el script como en Wireshark cómo llegan las tramas.

NOTA: Requiere privilegios de administrador (sudo) para capturar tramas.
"""

from scapy.all import Ether, sniff, conf
import sys

# Configuración
conf.verb = 1

def procesar_trama(paquete):
    """
    Función callback que se ejecuta cada vez que se captura una trama.
    Analiza y muestra los campos de la trama Ethernet.
    """
    
    # Verificar que sea una trama Ethernet
    if Ether in paquete:
        print("\n" + "=" * 60)
        print("TRAMA ETHERNET RECIBIDA (Capa 2)")
        print("=" * 60)
        
        # Extraer la capa Ethernet
        eth = paquete[Ether]
        
        # Mostrar campos principales de la trama
        print(f"\n[*] Campos de la Trama Ethernet:")
        print(f"    - MAC Destino:  {eth.dst}")
        print(f"    - MAC Origen:   {eth.src}")
        print(f"    - EtherType:    0x{eth.type:04x}")
        
        # Identificar el tipo de protocolo encapsulado
        if eth.type == 0x0800:
            tipo_proto = "IPv4"
        elif eth.type == 0x0806:
            tipo_proto = "ARP"
        elif eth.type == 0x86DD:
            tipo_proto = "IPv6"
        elif eth.type == 0x9000:
            tipo_proto = "Experimental/Personalizado"
        else:
            tipo_proto = f"Desconocido (0x{eth.type:04x})"
        
        print(f"    - Protocolo:    {tipo_proto}")
        
        # Mostrar el payload si existe
        if paquete.haslayer('Raw'):
            payload = bytes(paquete['Raw'])
            print(f"\n[*] Payload (datos):")
            print(f"    - Tamaño: {len(payload)} bytes")
            print(f"    - Contenido: {payload[:100]}")  # Primeros 100 bytes
            
            # Intentar decodificar como texto si es posible
            try:
                texto = payload.decode('utf-8')
                print(f"    - Texto: {texto}")
            except:
                print(f"    - Hex: {payload.hex()}")
        
        # Mostrar representación completa de la trama
        print(f"\n[*] Trama completa:")
        paquete.show()
        
        print("\n" + "=" * 60)

def escuchar_tramas():
    """
    Captura y procesa tramas Ethernet en la interfaz especificada.
    """
    
    print("=" * 60)
    print("HOST B - ESCUCHANDO TRAMAS ETHERNET (Capa 2)")
    print("=" * 60)
    
    # Especificar la interfaz de red a usar
    # Debe ser la misma interfaz donde Host A está enviando
    interfaz = "eth0"  # Modificar según tu sistema
    
    # Filtro BPF (Berkeley Packet Filter)
    # Captura solo tramas con un EtherType específico o dirección MAC
    # Modificar según las necesidades del laboratorio
    filtro = "ether proto 0x9000 or ether broadcast"
    # Opciones:
    # - "ether proto 0x9000" = captura solo EtherType 0x9000
    # - "ether dst ff:ff:ff:ff:ff:ff" = solo broadcast
    # - "ether src 00:11:22:33:44:55" = solo desde una MAC específica
    
    print(f"\n[*] Configuración:")
    print(f"    - Interfaz: {interfaz}")
    print(f"    - Filtro: {filtro}")
    print(f"\n[*] Esperando tramas...")
    print("[*] Presionar Ctrl+C para detener\n")
    
    try:
        # sniff() captura paquetes de la red
        # prn= función que se ejecuta por cada paquete capturado
        # filter= filtro BPF para capturar solo ciertos paquetes
        # iface= interfaz de red a escuchar
        # store=0 no almacena paquetes en memoria (eficiente para largo tiempo)
        sniff(
            prn=procesar_trama,
            filter=filtro,
            iface=interfaz,
            store=0
        )
        
    except PermissionError:
        print("\n[ERROR] Se requieren privilegios de administrador.")
        print("        Ejecutar con: sudo python3 ethernet_host_B.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error al capturar tramas: {e}")
        print(f"        Verificar que la interfaz '{interfaz}' existe y está activa.")
        sys.exit(1)

if __name__ == "__main__":
    print("\n[!] IMPORTANTE: Este script requiere privilegios de administrador")
    print("    Ejecutar con: sudo python3 ethernet_host_B.py\n")
    print("[INFO] Para laboratorio:")
    print("       1. Iniciar este script en Host B")
    print("       2. Iniciar captura en Wireshark")
    print("       3. Ejecutar ethernet_host_A.py en Host A")
    print("       4. Observar tramas tanto en este script como en Wireshark\n")
    
    try:
        escuchar_tramas()
    except KeyboardInterrupt:
        print("\n\n[*] Captura detenida por el usuario.")
        sys.exit(0)
