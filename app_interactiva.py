from datetime import datetime, timedelta

# Inventario inicial de portátiles disponibles en el centro
portatiles = {
    "PORT01": {"marca": "HP", "estado": "Disponible"},
    "PORT02": {"marca": "Lenovo", "estado": "Disponible"},
    "PORT03": {"marca": "Dell", "estado": "Disponible"},
    "PORT04": {"marca": "Asus", "estado": "Disponible"}
}

# Diccionario de usuarios y lista de préstamos inicialmente VACÍOS
usuarios = {}
prestamos = []

def registrar_usuario():
    print("\n--- REGISTRAR NUEVO USUARIO ---")
    usuario_id = input("Ingrese el documento de identidad (ID): ").strip()
    
    if not usuario_id:
        print("❌ Error: El documento no puede estar vacío.")
        return
        
    if usuario_id in usuarios:
        print(f"❌ Error: Ya existe un usuario registrado con el documento {usuario_id}.")
        return
        
    nombre = input("Ingrese el nombre completo: ").strip()
    if not nombre:
        print("❌ Error: El nombre no puede estar vacío.")
        return
        
    correo = input("Ingrese el correo electrónico: ").strip()
    
    print("Seleccione el rol del usuario:")
    print("1. Aprendiz (Préstamo por 1 día)")
    print("2. Instructor (Préstamo por 3 días)")
    print("3. Administrativo (Préstamo por 3 días)")
    opcion_rol = input("Elija una opción (1/2/3): ").strip()
    
    roles = {"1": "Aprendiz", "2": "Instructor", "3": "Administrativo"}
    if opcion_rol not in roles:
        print("❌ Error: Opción de rol inválida. Registro cancelado.")
        return
        
    rol = roles[opcion_rol]
    
    # Guardar el nuevo usuario en el diccionario
    usuarios[usuario_id] = {
        "nombre": nombre,
        "correo": correo,
        "rol": rol,
        "sancionado": False
    }
    
    print(f"\n✅ Usuario '{nombre}' ({rol}) registrado con éxito con el ID: {usuario_id}.")

def listar_usuarios():
    print("\n--- LISTA DE USUARIOS REGISTRADOS ---")
    if not usuarios:
        print("Aún no hay usuarios registrados en el sistema.")
        return
        
    for uid, datos in usuarios.items():
        estado_sancion = "🔴 Sancionado" if datos["sancionado"] else "🟢 Activo"
        print(f"ID: {uid} | Nombre: {datos['nombre']} | Rol: {datos['rol']} | Correo: {datos['correo']} | Estado: {estado_sancion}")

def registrar_prestamo():
    print("\n--- REGISTRAR NUEVO PRÉSTAMO ---")
    if not usuarios:
        print("⚠️ No hay usuarios registrados. Primero debe registrar al menos un usuario (Opción 1).")
        return
        
    usuario_id = input("Ingrese el documento del usuario: ").strip()
    
    if usuario_id not in usuarios:
        print("❌ Error: El usuario no está registrado. Regístrelo primero en la opción 1.")
        return
        
    usuario = usuarios[usuario_id]
    if usuario["sancionado"]:
        print(f"❌ Error: El usuario {usuario['nombre']} tiene una sanción activa y no puede solicitar equipos.")
        return
        
    # Verificar si ya tiene un préstamo activo
    prestamos_activos = [p for p in prestamos if p["usuario_id"] == usuario_id and p["estado"] == "Activo"]
    if prestamos_activos:
        print(f"❌ Error: {usuario['nombre']} ya tiene un portátil prestado ({prestamos_activos[0]['portatil_id']}).")
        return

    # Mostrar portátiles disponibles para facilitar la elección
    disponibles = [pid for pid, datos in portatiles.items() if datos["estado"] == "Disponible"]
    if not disponibles:
        print("❌ Error: No hay ningún portátil disponible en este momento.")
        return
    print(f"Equipos disponibles: {', '.join(disponibles)}")

    portatil_id = input("Ingrese el ID/Placa del portátil a prestar: ").strip().upper()
    if portatil_id not in portatiles:
        print("❌ Error: El portátil ingresado no existe en el inventario.")
        return
        
    if portatiles[portatil_id]["estado"] != "Disponible":
        print(f"❌ Error: El portátil {portatil_id} no está disponible (Estado: {portatiles[portatil_id]['estado']}).")
        return

    # Asignar días de préstamo según el rol
    dias_prestamo = 1 if usuario["rol"] == "Aprendiz" else 3
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
        
    ahora = datetime.now()
    retrasado = ahora > prestamo_activo["fecha_limite"]
    
    prestamo_activo["estado"] = "Devuelto"
    prestamo_activo["fecha_devolucion_real"] = ahora
    portatiles[portatil_id]["estado"] = "Disponible"
    
    usuario = usuarios[prestamo_activo["usuario_id"]]
    print(f"\n✅ Devolución registrada con éxito.")
    print(f"🧑 Usuario: {usuario['nombre']}")
    print(f"💻 Equipo: {portatil_id}")
    
    if retrasado:
        usuario["sancionado"] = True
        print("⚠️ ALERTA: La devolución se hizo fuera de tiempo. El usuario ha quedado SANCIONADO.")
    else:
        print("👍 Devolución entregada a tiempo. Sin novedades.")

def mostrar_prestamos():
    print("\n--- HISTORIAL Y ESTADO DE PRÉSTAMOS ---")
    if not prestamos:
        print("No hay préstamos registrados todavía.")
        return
    for idx, p in enumerate(prestamos, start=1):
        usuario = usuarios.get(p['usuario_id'], {}).get('nombre', 'Desconocido')
        estado_entrega = "⚠️ ATRASADO" if p["estado"] == "Activo" and datetime.now() > p["fecha_limite"] else p["estado"]
        print(f"{idx}. Usuario: {usuario} (ID: {p['usuario_id']}) | Equipo: {p['portatil_id']} | Límite: {p['fecha_limite'].strftime('%Y-%m-%d %H:%M')} | Estado: {estado_entrega}")

# Menú principal interactivo
while True:
    print("\n==========================================")
    print("  SISTEMA DE PRÉSTAMOS SENA   ")
    print("==========================================")
    print("1. Registrar Nuevo Usuario")
    print("2. Ver Usuarios Registrados")
    print("3. Registrar Préstamo de Portátil")
    print("4. Registrar Devolución de Portátil")
    print("5. Ver Historial/Estado de Préstamos")
    print("6. Salir")
    opcion = input("Elija una opción (1-6): ").strip()
    
    if opcion == "1":
        registrar_usuario()
    elif opcion == "2":
        listar_usuarios()
    elif opcion == "3":
        registrar_prestamo()
    elif opcion == "4":
        registrar_devolucion()
    elif opcion == "5":
        mostrar_prestamos()
    elif opcion == "6":
        print("Saliendo del sistema... ¡Hasta luego!")
        break
    else:
        print("❌ Opción inválida, por favor elija un número del 1 al 6.")