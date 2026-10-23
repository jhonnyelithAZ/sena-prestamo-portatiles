# Sistema de Gestión de Préstamos de Computadores Portátiles - SENA

Este repositorio contiene la solución propuesta para digitalizar y optimizar el proceso de préstamo de computadores portátiles en el centro de formación. La solución incluye análisis de requerimientos, diseño de flujo, un prototipo funcional en Python y casos de prueba.

---

## 📌 1. Descripción del problema
Actualmente, el centro de formación realiza el préstamo de computadores portátiles de manera manual (probablemente en hojas de papel o cuadernos). Este método genera descontrol y falta de visibilidad en tiempo real sobre:
* Quién tiene cada equipo (estudiantes, instructores o personal).
* Cuándo debe devolverse (vencimiento de plazos).
* Qué préstamos se encuentran pendientes, atrasados o por entregar.

Además, la falta de reglas de proceso claras y de un conjunto estandarizado de datos impide una gestión eficiente, aumentando el riesgo de pérdida de equipos, retrasos no penalizados y desorganización en el inventario.

---

## 📋 2. Requerimientos de Datos 

Para sistematizar el proceso, dividimos los datos necesarios en dos categorías:

### Datos Imprescindibles (Obligatorios para la operación básica)
* **Del Usuario:**
  * Documento de Identidad (ID / Cédula / Tarjeta de Identidad) - *Clave única*.
  * Nombre Completo.
  * Correo electrónico institucional y de contacto.
  * Rol (Aprendiz, Instructor, Administrativo).
* **Del Computador (Portátil):**
  * Placa de inventario o Serial único (ID del equipo).
  * Marca y Modelo.
  * Estado físico actual (Bueno, Regular).
  * Disponibilidad (Disponible, Prestado, En mantenimiento).
* **Del Préstamo:**
  * ID único de la transacción.
  * Fecha y hora de salida.
  * Fecha y hora límite de devolución.
  * ID del usuario que lo recibe y ID del equipo prestado.

### Datos a Confirmar (Sujetos a validación o extensión)
* Programa de formación o área del usuario (para saber a qué ficha o departamento pertenece).
* Jornada (Diurna, Nocturna, Mixta).
* Accesorios entregados (Cargador, mouse, maletín).
* Firma digital o física de aceptación de términos.
* Observaciones iniciales y finales del estado del hardware.

---

## 🤔 3. Preguntas al Responsable del Proceso 
1. **¿Cuál es el tiempo máximo permitido para un préstamo?** (¿Horas, el mismo día, o se pueden llevar a casa por varios días?).
2. **¿Existe un límite de equipos que un mismo usuario puede tener prestados a la vez?** (Por ejemplo, máximo 1 portátil por aprendiz).
3. **¿Cuáles son las consecuencias o sanciones si un usuario no devuelve el equipo a tiempo?** (¿Bloqueo en el sistema, reporte a coordinación?).
4. **¿Cómo se maneja el horario de atención?** (¿Qué pasa si un equipo se debe devolver un fin de semana o fuera de jornada?).
5. **¿Quiénes están autorizados para registrar los préstamos?** (¿Solo personal de biblioteca, instructores, o cualquier funcionario?).
6. **¿Se requiere de una verificación previa de antecedentes?** (Por ejemplo, si el aprendiz tiene sanciones previas o multas pendientes).

---

## 📐 4. Diagrama de Flujo y Pseudocódigo 

### Diagrama de Flujo
A continuación se presenta el flujo lógico del sistema para registrar préstamos y devoluciones de forma organizada:
![Diagrama de Flujo](img\diagrama.jpeg)

### Secuencia de Pasos (Pseudocódigo)
```text
Algoritmo Gestion_Prestamos_Portatiles
    // Definir estructuras de datos o listas de portátiles y usuarios
    Escribir "--- SISTEMA DE PRÉSTAMOS SENA ---"
    Escribir "1. Prestar Equipo  | 2. Devolver Equipo  | 3. Consultar Préstamos | 4. Salir"
    Leer opcion
    
    Mientras opcion != 4 Hacer
        Si opcion == 1 Entonces
            Escribir "Ingrese Documento del Usuario:"
            Leer id_usuario
            Escribir "Ingrese ID o Placa del Portátil:"
            Leer id_portatil
            
            Si PortatilEstaDisponible(id_portatil) Y UsuarioEstaActivo(id_usuario) Entonces
                MarcarPortatilComoPrestado(id_portatil)
                RegistrarTransaccion(id_usuario, id_portatil, FechaActual(), FechaLimite())
                Escribir "Préstamo registrado con éxito."
            Sino
                Escribir "Error: El portátil no está disponible o el usuario tiene restricciones."
            FinSi
            
        Si opcion == 2 Entonces
            Escribir "Ingrese ID o Placa del Portátil a devolver:"
            Leer id_portatil
            
            Si PortatilEstaPrestado(id_portatil) Entonces
                CalcularSiHayRetraso(id_portatil)
                MarcarPortatilComoDisponible(id_portatil)
                RegistrarDevolucion(id_portatil)
                Escribir "Devolución registrada correctamente."
            Sino
                Escribir "El equipo no se encuentra en estado de préstamo."
            FinSi
            
        Si opcion == 3 Entonces
            MostrarPrestamosActivos()
        FinSi
        
        Escribir "Seleccione una opción: "
        Leer opcion
    FinMientras
FinAlgoritmo
```


## 🧪 5. Pruebas y Resultados Esperados 

### Caso de Prueba 1: Préstamo Exitoso
* **Datos de entrada:** Usuario `1001` (Juan Pérez - Activo) solicita el equipo `PORT01` (Disponible).
* **Resultado esperado:** El sistema valida que el usuario no tiene sanciones y que el equipo está libre. Registra el préstamo, calcula la fecha límite de devolución (1 día) y cambia el estado de `PORT01` a "Prestado".

![Evidencia Prueba 1](img\caso1.png)

### Caso de Prueba 2: Rechazo por Usuario Sancionado
* **Datos de entrada:** Usuario `1003` (Luis Díaz - Sancionado) solicita el equipo `PORT02` (Disponible).
* **Resultado esperado:** El sistema detecta que el usuario tiene una sanción activa (`sancionado: True`), bloquea el préstamo mostrando un mensaje de error y mantiene el equipo `PORT02` como "Disponible".

![Evidencia Prueba 2](img\caso2.png)

---

## ⚠️ 6. Supuestos y Limitaciones de la Solución 

### Supuesto anotado
* Se asume que todos los portátiles y usuarios ya están previamente registrados en el sistema con códigos únicos antes de solicitar un préstamo, y que hay un encargado operando el programa en el momento de entregar o recibir el equipo.

### Situación que la solución todavía NO resuelve
* **Persistencia de datos y daños físicos:** Al cerrar la consola de Python, los préstamos registrados se borran porque aún no está conectado a una base de datos real (como MySQL o SQLite). Además, el programa todavía no permite registrar si un aprendiz devuelve el computador con la pantalla rota o sin el cargador.