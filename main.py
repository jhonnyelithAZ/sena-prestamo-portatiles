from datetime import datetime, timedelta

# Bases de datos temporales (Simulación de DB)
portatiles = {
    "PORT01": {"marca": "HP", "estado": "Disponible"},
    "PORT02": {"marca": "Lenovo", "estado": "Disponible"},
    "PORT03": {"marca": "Dell", "estado": "Prestado"} # Uno ya ocupado para pruebas
}

usuarios = {
    "1001": {"nombre": "Juan Pérez", "rol": "Aprendiz", "sancionado": False},
    "1002": {"nombre": "Ana Gómez", "rol": "Instructor", "sancionado": False},
    "1003": {"nombre": "Luis Díaz", "rol": "Aprendiz", "sancionado": True} # Usuario con sanción
}

prestamos = [
    {
        "usuario_id": "1003",
        "portatil_id": "PORT03",
        "fecha_salida": datetime.now() - timedelta(days=2),
        "fecha_limite": datetime.now() - timedelta(days=1), # Retrasado
        "estado": "Activo"
    }
]

def registrar_prestamo():
    print("\n--- REGISTRAR NUEVO PRÉSTAMO ---")
    usuario_id = input("Ingrese el documento del usuario: ").strip()
    
    if usuario_id not in usuarios:
        print("❌ Error: El usuario no está registrado en la base de datos.")
        return
        
    usuario = usuarios[usuario_id]
    if usuario["sancionado"]:
        print(f"❌ Error: El usuario {usuario['nombre']} tiene una sanción activa y no puede pedir prestado.")
        return
        
    # Verificar si ya tiene un préstamo activo
    prestamos_activos = [p for p in prestamos if p["usuario_id"] == usuario_id and p["estado"] == "Activo"]
    if prestamos_activos:
        print(f"❌ Error: {usuario['nombre']} ya cuenta con un préstamo activo. Debe devolverlo primero.")
        return

    portatil_id = input("Ingrese el ID/Placa del portátil: ").strip().upper()
    if portatil_id not in portatiles:
        print("❌ Error: El portátil no existe en el inventario.")
        return
        
    if portatiles[portatil_id]["estado"] != "Disponible":
        print(f"❌ Error: El portátil {portatil_id} no está disponible (Estado: {portatiles[portatil_id]['estado']}).")
        return

    # Proceso de préstamo exitoso
    dias_prestamo = 1 if usuario["rol"] == "Aprendiz" else 3 # Las reglas del negocio
    fecha_salida = datetime.now()
    fecha_limite = fecha_salida + timedelta(days=dias_prestamo)
    
    portatiles[portatil_id]["estado"] = "Prestado"
    nuevo_prestamo = {
        "usuario_id": usuario_id,
        "portatil_id": portatil_id,
        "fecha_salida": fecha_salida,
        "fecha_limite": fecha_limite,
        "estado": "Activo"
    }
    prestamos.append(nuevo_prestamo)
    
    print(f"\n✅ Préstamo registrado con éxito para {usuario['nombre']}.")
    print(f"💻 Equipo: {portatil_id} ({portatiles[portatil_id]['marca']})")
    print(f"📅 Fecha límite de entrega: {fecha_limite.strftime('%Y-%m-%d %H:%M')}")

def registrar_devolucion():
    print("\n--- REGISTRAR DEVOLUCIÓN ---")
    portatil_id = input("Ingrese el ID/Placa del portátil a devolver: ").strip().upper()
    
    prestamo_activo = None
    for p in prestamos:
        if p["portatil_id"] == portatil_id and p["estado"] == "Activo":
            prestamo_activo = p
            break
            
    if not prestamo_activo:
        print("❌ Error: No se encontró ningún préstamo activo para este portátil.")
        return
        
    # Comprobar retraso
    ahora = datetime.now()
    retrasado = ahora > prestamo_activo["fecha_limite"]
    
    # Cerrar el préstamo y actualizar inventario
    prestamo_activo["estado"] = "Devuelto"
    prestamo_activo["fecha_devolucion_real"] = ahora
    portatiles[portatil_id]["estado"] = "Disponible"
    
    usuario = usuarios[prestamo_activo["usuario_id"]]
    print(f"\n✅ Devolución registrada con éxito.")
    print(f"🧑 Usuario: {usuario['nombre']}")
    print(f"💻 Equipo: {portatil_id}")
    
    if retrasado:
        usuario["sancionado"] = True
        print("⚠️ ALERTA: La devolución se hizo fuera de tiempo. El usuario ha sido SANCIONADO.")
    else:
        print("👍 Devolución a tiempo. Sin novedades.")

def mostrar_prestamos():
    print("\n--- ESTADO DE PRÉSTAMOS ---")
    if not prestamos:
        print("No hay registros históricos.")
        return
    for idx, p in enumerate(prestamos, start=1):
        usuario = usuarios.get(p['usuario_id'], {}).get('nombre', 'Desconocido')
        estado_entrega = "⚠️ ATRASADO" if p["estado"] == "Activo" and datetime.now() > p["fecha_limite"] else p["estado"]
        print(f"{idx}. Usuario: {usuario} | Equipo: {p['portatil_id']} | Límite: {p['fecha_limite'].strftime('%Y-%m-%d')} | Estado: {estado_entrega}")

# Menú interactivo
while True:
    print("\n==============================")
    print("  MENÚ GESTIÓN DE PORTÁTILES  ")
    print("==============================")
    print("1. Registrar Préstamo")
    print("2. Registrar Devolución")
    print("3. Ver Historial/Préstamos")
    print("4. Salir")
    opcion = input("Elija una opción: ").strip()
    
    if opcion == "1":
        registrar_prestamo()
    elif opcion == "2":
        registrar_devolucion()
    elif opcion == "3":
        mostrar_prestamos()
    elif opcion == "4":
        print("Gracias por usar el sistema. ¡Hasta luego!")
        break
    else:
        print("Opción inválida, intente de nuevo.")