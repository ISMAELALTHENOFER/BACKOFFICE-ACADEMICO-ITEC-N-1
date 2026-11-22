"""Contenido del documento de análisis y diseño del Backoffice Académico ITEC N°1.

Fuentes: backoffice_itec_enunciado.docx, Requerimientos.docx, Anexo Requerimientos.docx
y las decisiones de alcance registradas en PLAN_DE_IMPLEMENTACION.md.
"""

TITULO = "Backoffice Académico ITEC N°1"
AUTOR = "Ismael Althenofer"
FECHA = "Noviembre de 2026"

INTRODUCCION = [
    "El presente documento describe el análisis y el diseño del Backoffice Académico del "
    "Instituto Tecnológico N°1 (ITEC N°1), un sistema de gestión académica centralizado que "
    "permite administrar alumnos, docentes, materias, inscripciones, asistencias y calificaciones, "
    "aplicando automáticamente las reglas académicas de regularidad y correlatividad.",
    "El sistema se desarrolla en Java con una arquitectura en capas bajo el patrón "
    "Modelo-Vista-Controlador (MVC) y persistencia en una base de datos relacional MySQL ejecutada en "
    "un contenedor Docker. El análisis y el diseño son independientes de la plataforma de presentación: "
    "el mismo modelo, las mismas reglas y la misma base de datos sirven tanto para una aplicación de "
    "escritorio como para una aplicación web.",
    "El documento reúne el escenario, las reglas del negocio, los requisitos funcionales, los casos "
    "de uso con sus diagramas de secuencia y contratos de operación, los diagramas de clases, el "
    "diagrama de estados académicos, el modelo de datos y la arquitectura del sistema.",
]

ESCENARIO = {
    "parrafos": [
        "El ITEC N°1 gestiona gran parte de su información académica de forma manual o mediante "
        "herramientas dispersas (planillas y registros en papel). Esto genera duplicación de datos, "
        "errores en el cálculo de la regularidad, dificultades para verificar correlativas y "
        "demoras en la emisión de reportes y actas.",
        "El instituto dicta carreras organizadas en planes de estudio. Cada plan está compuesto por "
        "materias que pueden tener correlativas: para cursar o rendir una materia, el alumno debe "
        "tener aprobadas las materias correlativas. Cada materia se dicta en una o más comisiones "
        "por ciclo lectivo y cuatrimestre, con horarios semanales de lunes a viernes y uno o más "
        "docentes asignados (un responsable y, opcionalmente, auxiliares).",
        "El personal administrativo registra a los alumnos y docentes, define las materias y sus "
        "correlativas, arma la oferta de comisiones e inscribe a los alumnos en las cursadas. "
        "Los docentes registran la asistencia de cada clase, cargan las notas de parciales, "
        "recuperatorios, trabajos prácticos y exámenes finales, y cierran las actas. Los alumnos "
        "consultan su asistencia, sus notas y su condición académica.",
        "Un alumno es regular en una cursada cuando su asistencia es igual o superior al 70 % de las "
        "clases dictadas. Las calificaciones van de 0 a 10 y se aprueba con 6 o más. Según el "
        "promedio de la cursada, el alumno promociona la materia, queda regular para rendir el final "
        "o desaprueba la cursada.",
        "El sistema debe cubrir las siguientes áreas:",
    ],
    "alcance": [
        "Gestión de acceso: inicio de sesión con usuario y contraseña, roles diferenciados "
        "(Administrativo, Docente y Alumno) y control de permisos en cada operación.",
        "Gestión académica: alumnos, docentes, materias, correlativas, oferta de comisiones, "
        "horarios y clases.",
        "Inscripciones: inscripción de alumnos a cursadas con validación de correlativas.",
        "Asistencia: registro por clase, justificación de inasistencias, cálculo automático de "
        "regularidad y cierre de asistencia por comisión.",
        "Calificaciones: parciales, recuperatorios, trabajos prácticos, finales, cálculo de promedio "
        "y condición, corrección auditada de notas y cierre de actas.",
        "Reportes: asistencia por materia, rendimiento por alumno, alumnos en riesgo y libro de "
        "actas exportable en PDF, Excel y CSV.",
        "Auditoría: registro de quién cargó asistencias, quién modificó notas, cuándo y con qué "
        "valores anteriores y nuevos.",
    ],
    "cierre": [
        "Quedan fuera del alcance obligatorio y se consideran mejoras futuras: carga masiva de notas "
        "por Excel, registro de asistencia mediante código QR, firma digital de actas y "
        "notificaciones automáticas a los alumnos.",
    ],
}

PERSONAL = [
    [AUTOR, "Analista, diseñador y desarrollador",
     "Relevamiento y análisis de requisitos, diseño de la arquitectura y del modelo de datos, "
     "implementación, pruebas, documentación y despliegue."],
]

USUARIOS = [
    ["Administrativo", "ADM",
     "Personal administrativo del instituto. Agrupa los roles «Administrador» y «Administrativo» "
     "del enunciado. Gestiona usuarios, alumnos, docentes, materias, correlativas, oferta académica, "
     "asignaciones docentes e inscripciones; justifica inasistencias; reabre actas y asistencias "
     "cerradas (correcciones extraordinarias); consulta reportes y auditoría."],
    ["Docente", "DOC",
     "Docente asignado a una o más comisiones. Registra asistencia, justifica inasistencias, carga y "
     "corrige notas de sus comisiones, cierra la asistencia y las actas de finales, y consulta "
     "reportes de sus comisiones."],
    ["Alumno", "ALU",
     "Estudiante del instituto. Consulta únicamente su propia asistencia, sus calificaciones y su "
     "condición académica en cada cursada."],
]

REGLAS = [
    ["RN-01", "Todo usuario accede con nombre de usuario y contraseña. Las contraseñas se almacenan "
     "con un algoritmo de hash seguro con sal, nunca en texto plano.", "Baja", "US-AUTH-01"],
    ["RN-02", "Los roles del sistema son ADM (Administrativo), DOC (Docente) y ALU (Alumno). Solo un "
     "ADM puede crear usuarios, activarlos o desactivarlos y asignarles un rol.", "Media", "Política del negocio"],
    ["RN-03", "Los permisos se verifican en cada operación y no solo al mostrar el menú. Un usuario "
     "inactivo o con credenciales incorrectas no puede ingresar; el mensaje de error no revela qué "
     "dato fue incorrecto.", "Baja", "US-AUTH-01"],
    ["RN-04", "Un alumno requiere DNI único, nombre, apellido y email con formato válido; el teléfono "
     "es opcional. Se crea en estado ACTIVO y se registra la fecha de última modificación.",
     "Baja", "US-ALU-01..03"],
    ["RN-05", "Un docente requiere DNI único, nombre, apellido y email con formato válido; el teléfono "
     "es opcional. Se crea en estado ACTIVO.", "Baja", "US-PROF-01..02"],
    ["RN-06", "Alumnos, docentes y materias no se eliminan físicamente: la baja es lógica (estado "
     "INACTIVO / INACTIVA) y se conserva su historial académico.", "Baja", "US-ALU-04, US-PROF-03, US-MAT-03"],
    ["RN-07", "Una materia requiere código único y nombre, pertenece a un plan de estudios y se crea "
     "en estado ACTIVA.", "Baja", "US-MAT-01..02"],
    ["RN-08", "Una materia puede tener varias correlativas. No se permite que una materia sea "
     "correlativa de sí misma ni que se formen ciclos de correlatividad de cualquier longitud.",
     "Baja", "US-MAT-04"],
    ["RN-09", "Solo se asignan docentes ACTIVO a comisiones de materias ACTIVA. Cada comisión tiene un "
     "docente RESPONSABLE y puede tener docentes AUXILIAR. Un docente inactivo no recibe nuevas "
     "asignaciones.", "Media", "US-PROF-04"],
    ["RN-10", "Una cursada se identifica por alumno, materia, comisión y ciclo lectivo. No se permite "
     "inscribir a un alumno en una materia en la que ya tenga una inscripción EN_CURSO, REGULAR, "
     "PROMOCIONADO o APROBADO. Puede recursar en otro ciclo si su inscripción anterior terminó "
     "NO_REGULAR, DESAPROBADO o BAJA.", "Media", "US-INS-01, decisión del proyecto"],
    ["RN-11", "Para inscribirse, el alumno debe estar ACTIVO, la materia ACTIVA y todas sus "
     "correlativas aprobadas (estado APROBADO o PROMOCIONADO). Si faltan correlativas, el sistema "
     "informa cuáles.", "Baja", "US-INS-01"],
    ["RN-12", "Solo el docente asignado a la comisión registra la asistencia de cada alumno inscripto "
     "por clase, con estado PRESENTE, AUSENTE o JUSTIFICADA.", "Baja", "US-ASIS-01, Anexo"],
    ["RN-13", "Porcentaje de asistencia = (presentes + justificadas) / clases dictadas registradas × 100, "
     "con dos decimales. El alumno es REGULAR con 70 % o más (umbral inclusivo) y NO_REGULAR con "
     "menos de 70 %. Sin clases registradas se informa «Sin registros».",
     "Media", "US-ASIS-02, US-ASIS-03, decisión del proyecto"],
    ["RN-14", "Para justificar una inasistencia el motivo es obligatorio y el certificado es opcional. "
     "Una inasistencia justificada se computa como presente.", "Media", "US-ASIS-04, decisión del proyecto"],
    ["RN-15", "Al cerrar la asistencia de una comisión se congela el porcentaje y se fija la condición "
     "de cursada (RN-18). Luego no se modifican asistencias salvo reapertura por un ADM (RN-22).",
     "Baja", "US-ASIS-05"],
    ["RN-16", "Las notas van de 0 a 10 con hasta un decimal. Una nota fuera de rango se rechaza. "
     "Una nota es aprobada si es mayor o igual a 6.", "Baja", "US-CAL-01, Anexo"],
    ["RN-17", "Evaluaciones de cursada: Parcial 1 y Parcial 2 (obligatorios) y Trabajo práctico "
     "(opcional). Cada parcial tiene un recuperatorio, habilitado solo si el parcial fue desaprobado "
     "(nota menor a 6). La nota del recuperatorio reemplaza a la del parcial.",
     "Media", "US-CAL-04, decisión del proyecto"],
    ["RN-18", "Promedio de cursada = suma de las notas efectivas (parciales luego del recuperatorio y "
     "trabajo práctico si existe) / cantidad de notas. Al cerrar la asistencia, con ambos parciales "
     "cargados: asistencia menor a 70 % → NO_REGULAR; asistencia de 70 % o más y promedio de 8 o más → "
     "PROMOCIONADO; asistencia de 70 % o más y promedio entre 6 y menos de 8 → REGULAR; asistencia de "
     "70 % o más y promedio menor a 6 → DESAPROBADO.", "Media", "US-CAL-05, decisión del proyecto"],
    ["RN-19", "Solo rinde final el alumno REGULAR con todas las correlativas aprobadas. Nota final "
     "mayor o igual a 6 → APROBADO; menor a 6 → DESAPROBADO. El alumno PROMOCIONADO no rinde final.",
     "Baja", "US-CAL-02"],
    ["RN-20", "Un docente solo modifica notas de sus comisiones, mientras la cursada o el acta estén "
     "abiertas. Cada modificación registra nota anterior, nota nueva, usuario y fecha.",
     "Baja", "US-CAL-03, Anexo"],
    ["RN-21", "Un acta final solo se cierra si todos los alumnos habilitados tienen nota final. "
     "Cerrada, el acta no es editable.", "Baja", "US-CAL-06"],
    ["RN-22", "Solo un ADM puede reabrir un acta o una asistencia cerrada (corrección extraordinaria), "
     "indicando un motivo obligatorio. La reapertura queda auditada.", "Baja", "Anexo, decisión del proyecto"],
    ["RN-23", "Se audita la carga y modificación de asistencias, la modificación de notas, los cierres "
     "y las reaperturas: acción, entidad, valor anterior, valor nuevo, usuario, fecha y motivo. "
     "Los registros de auditoría no se modifican ni se eliminan desde el sistema.", "Baja", "Anexo (EPIC-AUD)"],
    ["RN-24", "Un alumno solo puede consultar su propia información académica.", "Baja", "Decisión del proyecto"],
    ["RN-25", "Un alumno está en riesgo de pérdida de regularidad si su asistencia es menor a 70 % y en "
     "riesgo académico si su promedio es menor a 6.", "Media", "Anexo"],
]

REQUISITOS = [
    ("Seguridad y acceso", [
        ["RF-01", "Permitir iniciar sesión con usuario y contraseña y habilitar las funciones según el rol.", "US-AUTH-01"],
        ["RF-02", "Permitir cerrar sesión.", "US-AUTH-01"],
        ["RF-03", "Gestionar usuarios: crear, activar, desactivar, asignar rol y restablecer contraseña.", "Enunciado 3.1"],
        ["RF-04", "Verificar los permisos del rol en cada operación del sistema.", "US-AUTH-01, Anexo"],
    ]),
    ("Gestión de alumnos", [
        ["RF-05", "Registrar alumnos con validación de datos y DNI único.", "US-ALU-01"],
        ["RF-06", "Consultar un alumno por DNI.", "US-ALU-02"],
        ["RF-07", "Modificar los datos de un alumno.", "US-ALU-03"],
        ["RF-08", "Dar de baja lógica a un alumno conservando su historial.", "US-ALU-04"],
    ]),
    ("Gestión de docentes", [
        ["RF-09", "Registrar docentes con validación de datos y DNI único.", "US-PROF-01"],
        ["RF-10", "Modificar los datos de un docente.", "US-PROF-02"],
        ["RF-11", "Dar de baja lógica a un docente conservando su historial.", "US-PROF-03"],
        ["RF-12", "Asignar docentes a comisiones y consultar las asignaciones.", "US-PROF-04"],
    ]),
    ("Gestión de materias", [
        ["RF-13", "Registrar materias con código único.", "US-MAT-01"],
        ["RF-14", "Modificar los datos de una materia.", "US-MAT-02"],
        ["RF-15", "Dar de baja lógica a una materia conservando su historial.", "US-MAT-03"],
        ["RF-16", "Definir correlativas de una materia, rechazando autorreferencias y ciclos.", "US-MAT-04"],
    ]),
    ("Oferta académica", [
        ["RF-17", "Gestionar carreras y planes de estudio.", "Enunciado 3.2"],
        ["RF-18", "Gestionar comisiones por materia, ciclo lectivo y cuatrimestre, con sus horarios.", "Enunciado 3.2"],
        ["RF-19", "Registrar las clases dictadas de cada comisión.", "US-ASIS-01"],
    ]),
    ("Inscripciones", [
        ["RF-20", "Inscribir alumnos a una cursada validando estado, duplicados y correlativas.", "US-INS-01"],
    ]),
    ("Asistencia", [
        ["RF-21", "Registrar la asistencia por clase y alumno inscripto.", "US-ASIS-01"],
        ["RF-22", "Recalcular automáticamente el porcentaje y la condición de regularidad.", "US-ASIS-02"],
        ["RF-23", "Consultar la asistencia de un alumno con presentes, ausentes, justificadas, porcentaje y condición.", "US-ASIS-03"],
        ["RF-24", "Justificar inasistencias con motivo y certificado opcional.", "US-ASIS-04"],
        ["RF-25", "Cerrar la asistencia de una comisión y fijar la condición de cursada.", "US-ASIS-05"],
    ]),
    ("Calificaciones y actas", [
        ["RF-26", "Registrar notas de parciales y trabajos prácticos.", "US-CAL-01"],
        ["RF-27", "Registrar recuperatorios de parciales desaprobados.", "US-CAL-04"],
        ["RF-28", "Calcular automáticamente el promedio y la condición de cursada.", "US-CAL-05"],
        ["RF-29", "Registrar notas de examen final para alumnos habilitados.", "US-CAL-02"],
        ["RF-30", "Modificar calificaciones registrando la auditoría del cambio.", "US-CAL-03"],
        ["RF-31", "Cerrar el acta de examen final.", "US-CAL-06"],
        ["RF-32", "Reabrir actas o asistencias cerradas (solo ADM, con motivo).", "Anexo"],
    ]),
    ("Reportes y consultas", [
        ["RF-33", "Generar el reporte de asistencia y regularidad por materia/comisión.", "US-REP-01"],
        ["RF-34", "Generar el reporte de rendimiento por alumno.", "US-REP-02"],
        ["RF-35", "Generar el reporte de alumnos en riesgo.", "Anexo"],
        ["RF-36", "Generar el libro de actas y exportarlo en PDF, Excel y CSV.", "Anexo"],
        ["RF-37", "Permitir al alumno consultar su situación académica.", "US-AUTH-01, decisión del proyecto"],
        ["RF-38", "Consultar los registros de auditoría (solo ADM).", "Anexo (EPIC-AUD)"],
    ]),
]

REQUISITOS_NO_FUNCIONALES = [
    ["RNF-01", "Lenguaje Java con gestión de dependencias y construcción automatizada. La solución puede implementarse como aplicación de escritorio o como aplicación web sin cambiar el análisis ni el modelo."],
    ["RNF-02", "Arquitectura en capas MVC: la interfaz no contiene reglas de negocio ni acceso a datos."],
    ["RNF-03", "Persistencia en MySQL 8 con script SQL reproducible para crear el esquema y datos de ejemplo."],
    ["RNF-04", "Ejecución con Docker (docker compose): la base de datos MySQL corre en contenedor en ambas variantes; la variante web se ejecuta completa (aplicación y base) con Docker. La variante de escritorio se distribuye como un archivo .jar ejecutable listo para usar."],
    ["RNF-05", "Credenciales de conexión fuera del código fuente (variables de entorno o archivo local excluido de Git)."],
    ["RNF-06", "Contraseñas con hash seguro con sal; consultas SQL parametrizadas para evitar inyección."],
    ["RNF-07", "Operaciones de cierre y reapertura ejecutadas en una transacción: se aplican completas o no se aplican."],
    ["RNF-08", "Pruebas automatizadas para cada regla de negocio y cada caso de prueba TC-* del backlog."],
    ["RNF-09", "Control de versiones con Git y GitHub siguiendo Git Flow; documentación en la carpeta /document."],
]

# ---------- casos de uso ----------

def _uc(id_, nombre, actor, rf, paquete, prioridad, complejidad, arquitectura, traza, pre, post,
        flujo, alternativos, nivel="Usuario", categoria="Primario", tipo="Real, primario", secundario="—"):
    return dict(id=id_, nombre=nombre, actor=actor, rf=rf, paquete=paquete, prioridad=prioridad,
                complejidad=complejidad, arquitectura=arquitectura, traza=traza, pre=pre, post=post,
                flujo=flujo, alternativos=alternativos, nivel=nivel, categoria=categoria, tipo=tipo,
                secundario=secundario)


CASOS_DE_USO = [
    _uc("UC-01", "Iniciar sesión", "ADM, DOC, ALU", "RF-01, RF-02, RF-04", "Seguridad", "Alta", "Media", "Sí",
        "US-AUTH-01 / TC-AUTH-01..06",
        "El usuario está registrado en el sistema.",
        "Existe una sesión activa asociada al usuario y su rol; se muestra el menú correspondiente.",
        ["El usuario inicia la aplicación.",
         "El sistema muestra la pantalla de inicio de sesión.",
         "El usuario ingresa nombre de usuario y contraseña y confirma.",
         "El sistema verifica que el usuario exista, esté activo y que la contraseña coincida con el hash almacenado.",
         "El sistema inicia la sesión y muestra el menú habilitado para el rol (administrativo, docente o alumno)."],
        ["3a. Campos vacíos: el sistema solicita completarlos y vuelve al paso 3.",
         "4a. Usuario inexistente o contraseña incorrecta: el sistema muestra «Usuario o contraseña incorrectos» y vuelve al paso 3.",
         "4b. Usuario inactivo: el sistema deniega el acceso con el mismo mensaje genérico.",
         "*a. En cualquier momento el usuario cierra sesión: el sistema finaliza la sesión y vuelve al paso 2."]),
    _uc("UC-02", "Gestionar usuarios", "ADM", "RF-03", "Seguridad", "Alta", "Media", "No",
        "Enunciado 3.1",
        "Sesión iniciada con rol ADM.",
        "El usuario queda creado o actualizado con su rol y estado.",
        ["El ADM selecciona «Usuarios».",
         "El sistema lista los usuarios con su rol y estado.",
         "El ADM elige crear un usuario e ingresa nombre de usuario, contraseña inicial, rol y, si corresponde, el alumno o docente asociado.",
         "El sistema valida que el nombre de usuario sea único, guarda la contraseña con hash y registra el usuario activo.",
         "El sistema confirma la operación."],
        ["3a. El ADM modifica el rol, activa o desactiva un usuario o restablece su contraseña: el sistema valida y guarda el cambio.",
         "4a. Nombre de usuario duplicado: el sistema informa el error y vuelve al paso 3.",
         "4b. El alumno o docente asociado ya tiene usuario: el sistema informa el error."]),
    _uc("UC-03", "Gestionar alumnos", "ADM", "RF-05..RF-08", "Gestión académica", "Alta", "Baja", "No",
        "US-ALU-01..04 / TC-ALU-01..12",
        "Sesión iniciada con rol ADM.",
        "El alumno queda registrado, actualizado o dado de baja lógica.",
        ["El ADM selecciona «Alumnos».",
         "El sistema muestra el buscador por DNI y el listado de alumnos.",
         "El ADM elige «Nuevo» e ingresa DNI, nombre, apellido, email y teléfono.",
         "El sistema valida los campos obligatorios, el formato del email y que el DNI no exista.",
         "El sistema registra el alumno en estado ACTIVO y confirma."],
        ["2a. Consultar: el ADM ingresa un DNI; el sistema muestra los datos o «Alumno no encontrado».",
         "2b. Modificar: el ADM edita los datos de un alumno; el sistema valida, guarda y actualiza la fecha de modificación.",
         "2c. Dar de baja: el ADM confirma la baja; el sistema cambia el estado a INACTIVO y conserva el historial.",
         "4a. DNI duplicado: el sistema informa «Ya existe un alumno con ese DNI» y no crea el registro.",
         "4b. Email inválido o campo obligatorio vacío: el sistema indica el campo con error."]),
    _uc("UC-04", "Gestionar docentes", "ADM", "RF-09..RF-11", "Gestión académica", "Alta", "Baja", "No",
        "US-PROF-01..03 / TC-PROF-01..07",
        "Sesión iniciada con rol ADM.",
        "El docente queda registrado, actualizado o dado de baja lógica.",
        ["El ADM selecciona «Docentes».",
         "El sistema muestra el listado de docentes.",
         "El ADM elige «Nuevo» e ingresa DNI, nombre, apellido, email y teléfono.",
         "El sistema valida los campos, el email y que el DNI no exista.",
         "El sistema registra el docente en estado ACTIVO y confirma."],
        ["2a. Modificar: el sistema valida y guarda los cambios; si el docente no existe informa «no encontrado».",
         "2b. Dar de baja: el sistema cambia el estado a INACTIVO; el docente no recibe nuevas asignaciones.",
         "4a. DNI duplicado o email inválido: el sistema informa el error y no guarda."]),
    _uc("UC-05", "Gestionar materias y correlativas", "ADM", "RF-13..RF-16", "Gestión académica", "Alta", "Media", "Sí",
        "US-MAT-01..04 / TC-MAT-01..09",
        "Sesión iniciada con rol ADM; existe al menos un plan de estudios.",
        "La materia queda registrada, actualizada, dada de baja o con sus correlativas definidas.",
        ["El ADM selecciona «Materias».",
         "El sistema muestra las materias por plan de estudios.",
         "El ADM elige «Nueva» e ingresa código, nombre, plan, año y cuatrimestre.",
         "El sistema valida que el código sea único y registra la materia en estado ACTIVA.",
         "El ADM selecciona «Correlativas» y elige las materias requeridas.",
         "El sistema verifica que no haya autorreferencia ni ciclos y guarda las correlativas."],
        ["2a. Modificar o dar de baja una materia: el sistema guarda el cambio; una materia INACTIVA no acepta nuevas inscripciones.",
         "4a. Código duplicado: el sistema informa el error.",
         "6a. La materia se elige como correlativa de sí misma: el sistema rechaza la operación.",
         "6b. Se detecta un ciclo (por ejemplo A → B → C → A): el sistema rechaza la operación e indica el ciclo."]),
    _uc("UC-06", "Gestionar oferta académica", "ADM", "RF-17..RF-19", "Gestión académica", "Alta", "Media", "Sí",
        "Enunciado 3.2, modelo conceptual",
        "Sesión iniciada con rol ADM; existen materias activas.",
        "Quedan definidas carreras, planes, comisiones con horarios y clases.",
        ["El ADM selecciona «Oferta académica».",
         "El ADM registra o selecciona la carrera y el plan de estudios.",
         "El ADM crea una comisión para una materia indicando código, ciclo lectivo y cuatrimestre.",
         "El ADM agrega los horarios de la comisión (día de lunes a viernes, hora de inicio, hora de fin y aula).",
         "El sistema valida que la hora de fin sea posterior a la de inicio y que la comisión no exista para ese ciclo, y guarda.",
         "El ADM o el docente asignado registran las clases dictadas (fecha y tema)."],
        ["5a. Comisión duplicada para la materia y el ciclo: el sistema informa el error.",
         "6a. Ya existe una clase en esa fecha para la comisión: el sistema informa el error."]),
    _uc("UC-07", "Asignar docente a comisión", "ADM", "RF-12", "Gestión académica", "Alta", "Baja", "No",
        "US-PROF-04 / TC-PROF-08..10",
        "Sesión iniciada con rol ADM; existen el docente y la comisión.",
        "El docente queda asignado a la comisión con su rol docente.",
        ["El ADM selecciona una comisión.",
         "El sistema muestra los docentes asignados.",
         "El ADM elige un docente y su rol (RESPONSABLE o AUXILIAR).",
         "El sistema verifica que el docente esté ACTIVO, la materia ACTIVA y que no exista la asignación, y la registra.",
         "El sistema muestra la asignación actualizada."],
        ["4a. Docente INACTIVO: el sistema rechaza la asignación.",
         "4b. Materia INACTIVA: el sistema rechaza la asignación.",
         "4c. La comisión ya tiene un RESPONSABLE: el sistema solicita confirmar el reemplazo."]),
    _uc("UC-08", "Inscribir alumno a cursada", "ADM", "RF-20", "Inscripciones", "Alta", "Alta", "Sí",
        "US-INS-01 / TC-INS-01..04, TC-ALU-12, TC-MAT-06",
        "Sesión iniciada con rol ADM; existe la comisión.",
        "Existe una inscripción EN_CURSO del alumno en la comisión.",
        ["El ADM selecciona «Inscripciones» e ingresa el DNI del alumno.",
         "El sistema muestra los datos y el estado del alumno.",
         "El ADM selecciona la comisión.",
         "El sistema muestra la materia, el ciclo lectivo y los horarios.",
         "El ADM confirma la inscripción.",
         "El sistema valida alumno ACTIVO, materia ACTIVA, ausencia de inscripción vigente y correlativas aprobadas.",
         "El sistema registra la inscripción en estado EN_CURSO y confirma."],
        ["2a. Alumno inexistente: el sistema informa «Alumno no encontrado».",
         "6a. Alumno INACTIVO o materia INACTIVA: el sistema bloquea la inscripción.",
         "6b. Inscripción duplicada: el sistema informa que el alumno ya está inscripto o aprobó la materia.",
         "6c. Correlativas faltantes: el sistema informa la lista de materias que faltan aprobar."]),
    _uc("UC-09", "Registrar asistencia", "DOC", "RF-21, RF-22", "Asistencia", "Alta", "Alta", "Sí",
        "US-ASIS-01..02 / TC-ASIS-01..04",
        "Sesión iniciada con rol DOC; el docente está asignado a la comisión; la clase existe y la asistencia está abierta.",
        "La asistencia queda registrada, auditada y el porcentaje de cada alumno recalculado.",
        ["El docente selecciona una de sus comisiones y una clase.",
         "El sistema muestra los alumnos inscriptos con la asistencia previa, si existe.",
         "El docente marca PRESENTE o AUSENTE para cada alumno.",
         "El docente confirma.",
         "El sistema guarda las asistencias, registra la auditoría y recalcula el porcentaje y la condición provisoria.",
         "El sistema muestra el resultado con la condición de cada alumno."],
        ["1a. El docente no está asignado a la comisión: el sistema deniega la operación.",
         "5a. La asistencia de la comisión está cerrada: el sistema rechaza la modificación."]),
    _uc("UC-10", "Justificar inasistencia", "DOC, ADM", "RF-24, RF-22", "Asistencia", "Media", "Baja", "No",
        "US-ASIS-04",
        "Existe una asistencia AUSENTE; la asistencia de la comisión está abierta (o el ADM la reabrió).",
        "La asistencia queda JUSTIFICADA y el porcentaje recalculado.",
        ["El usuario busca al alumno y selecciona la inasistencia.",
         "El sistema muestra la fecha y la clase.",
         "El usuario ingresa el motivo y, opcionalmente, adjunta el certificado.",
         "El sistema valida el motivo, cambia el estado a JUSTIFICADA, registra la auditoría y recalcula el porcentaje."],
        ["4a. Motivo vacío: el sistema solicita completarlo.",
         "4b. DOC no asignado a la comisión: el sistema deniega la operación."]),
    _uc("UC-11", "Cerrar asistencia de comisión", "DOC", "RF-25, RF-28", "Asistencia", "Alta", "Media", "Sí",
        "US-ASIS-05, US-CAL-05",
        "Docente asignado; la asistencia de la comisión está abierta; los parciales están cargados.",
        "La asistencia queda cerrada y cada inscripción con su condición de cursada final.",
        ["El docente selecciona la comisión y elige «Cerrar asistencia».",
         "El sistema muestra, por alumno, el porcentaje, el promedio y la condición resultante.",
         "El docente confirma el cierre.",
         "El sistema, en una transacción, congela porcentajes, asigna NO_REGULAR, REGULAR, PROMOCIONADO o DESAPROBADO, marca la comisión como cerrada y audita."],
        ["2a. Hay alumnos sin ambos parciales: el sistema lista los pendientes y no permite cerrar.",
         "2b. No hay clases registradas: el sistema informa «Sin registros» y no permite cerrar."]),
    _uc("UC-12", "Registrar calificación de cursada", "DOC", "RF-26, RF-27, RF-28", "Calificaciones", "Alta", "Media", "Sí",
        "US-CAL-01, US-CAL-04, US-CAL-05 / TC-CAL-01..02",
        "Docente asignado a la comisión; la evaluación existe; la cursada está abierta.",
        "La nota queda registrada y el promedio recalculado.",
        ["El docente selecciona la comisión y la evaluación (Parcial 1, Parcial 2, Recuperatorio o Trabajo práctico).",
         "El sistema lista los alumnos inscriptos.",
         "El docente ingresa la nota de cada alumno.",
         "El sistema valida el rango 0 a 10, registra las notas y recalcula el promedio."],
        ["3a. Recuperatorio: el sistema solo habilita a los alumnos con el parcial correspondiente menor a 6; la nota reemplaza a la del parcial.",
         "4a. Nota fuera de rango: el sistema rechaza el valor.",
         "4b. Ya existe una nota para ese alumno y evaluación: el sistema deriva a «Modificar calificación» (UC-14)."]),
    _uc("UC-13", "Registrar nota final", "DOC", "RF-29", "Calificaciones", "Alta", "Media", "Sí",
        "US-CAL-02 / TC-CAL-03..05",
        "Docente asignado; existe un acta final ABIERTA para la comisión.",
        "La nota final queda registrada en el acta.",
        ["El docente selecciona el acta final.",
         "El sistema lista los alumnos REGULAR habilitados.",
         "El docente ingresa la nota final de un alumno.",
         "El sistema valida rango, estado REGULAR y correlativas aprobadas, y registra la nota."],
        ["4a. Alumno NO_REGULAR: el sistema rechaza la carga.",
         "4b. Correlativas pendientes: el sistema rechaza e informa cuáles faltan.",
         "4c. Acta cerrada: el sistema rechaza la carga."]),
    _uc("UC-14", "Modificar calificación", "DOC", "RF-30", "Calificaciones", "Media", "Media", "Sí",
        "US-CAL-03",
        "Docente asignado a la comisión; la cursada o el acta están abiertas.",
        "La nota queda corregida y el cambio auditado.",
        ["El docente busca la calificación a corregir.",
         "El sistema muestra la nota actual.",
         "El docente ingresa la nota nueva y una observación.",
         "El sistema valida, guarda, recalcula el promedio y registra la auditoría (nota anterior, nota nueva, usuario y fecha)."],
        ["4a. Acta o asistencia cerrada: el sistema rechaza el cambio (solo un ADM puede reabrir).",
         "4b. Docente no asignado: el sistema deniega la operación."]),
    _uc("UC-15", "Cerrar acta final", "DOC", "RF-31", "Calificaciones", "Alta", "Media", "Sí",
        "US-CAL-06",
        "Docente asignado; el acta está ABIERTA.",
        "El acta queda CERRADA y cada alumno con estado APROBADO o DESAPROBADO.",
        ["El docente selecciona el acta y elige «Cerrar acta».",
         "El sistema verifica que todos los alumnos habilitados tengan nota final.",
         "El sistema, en una transacción, aplica APROBADO (nota >= 6) o DESAPROBADO (nota < 6), marca el acta como CERRADA y audita el cierre.",
         "El sistema confirma el cierre."],
        ["2a. Faltan notas: el sistema lista los alumnos sin nota final y no cierra."]),
    _uc("UC-16", "Reabrir acta o asistencia", "ADM", "RF-32", "Calificaciones", "Media", "Media", "Sí",
        "Anexo - Reglas de seguridad",
        "Sesión iniciada con rol ADM; el acta o la asistencia están cerradas.",
        "El acta o la asistencia quedan abiertas y la reapertura auditada.",
        ["El ADM selecciona el acta o la comisión cerrada.",
         "El ADM elige «Reabrir» e ingresa el motivo.",
         "El sistema valida el motivo, reabre el registro, devuelve las inscripciones afectadas al estado previo correspondiente y registra la auditoría."],
        ["3a. Motivo vacío: el sistema solicita completarlo."]),
    _uc("UC-17", "Generar reportes académicos", "ADM, DOC", "RF-33..RF-36, RF-38", "Reportes", "Alta", "Media", "No",
        "US-REP-01..02, Anexo / TC-REP-01..04",
        "Sesión iniciada; un DOC solo accede a sus comisiones.",
        "Se muestra o exporta el reporte solicitado.",
        ["El usuario selecciona el reporte: asistencia por materia, rendimiento por alumno, alumnos en riesgo o libro de actas.",
         "El usuario indica los filtros (materia, comisión, ciclo o alumno).",
         "El sistema calcula y muestra el reporte.",
         "Opcionalmente, el usuario exporta el libro de actas en PDF, Excel o CSV."],
        ["3a. Sin asistencias registradas: el sistema informa «Sin registros».",
         "3b. Alumno sin notas: el sistema informa «Sin calificaciones registradas».",
         "1a. Consultar auditoría (solo ADM): el sistema lista los eventos filtrados por fecha, usuario o entidad."]),
    _uc("UC-18", "Consultar situación académica", "ALU", "RF-37, RF-23", "Reportes", "Media", "Baja", "No",
        "US-AUTH-01 (menú alumno), US-ASIS-03",
        "Sesión iniciada con rol ALU.",
        "Se muestra la información académica del propio alumno.",
        ["El alumno selecciona «Mi situación académica».",
         "El sistema muestra sus cursadas con asistencia (presentes, ausentes, justificadas y porcentaje), notas, promedio y condición."],
        ["2a. Sin inscripciones: el sistema informa que no posee cursadas registradas."]),
]

CONTRATOS = [
    dict(uc="UC-01", titulo="Iniciar sesión", dss="dss-iniciar-sesion.png", ds="ds-iniciar-sesion.png",
         operacion="iniciarSesion(nombreUsuario: String, contraseña: char[])",
         responsabilidades="Autenticar al usuario, verificar su estado y abrir una sesión con su rol.",
         controlador="LoginController / AuthService",
         pre="Existe un usuario con ese nombre de usuario.",
         post="Se creó una instancia de Sesion asociada al Usuario; la contraseña no se conserva en memoria."),
    dict(uc="UC-03", titulo="Crear alumno", dss="dss-crear-alumno.png", ds="ds-crear-alumno.png",
         operacion="crearAlumno(dni, nombre, apellido, email, teléfono)",
         responsabilidades="Validar los datos y registrar un alumno nuevo.",
         controlador="AlumnoController / AlumnoService",
         pre="Sesión activa con rol ADM. No existe un alumno con el DNI indicado.",
         post="Se creó una instancia a de Alumno; a.estado = ACTIVO; a.fechaAlta y a.fechaModificacion = fecha actual."),
    dict(uc="UC-08", titulo="Inscribir alumno", dss="dss-inscribir-alumno.png", ds="ds-inscribir-alumno.png",
         operacion="confirmarInscripcion()",
         responsabilidades="Validar las reglas de inscripción y registrar la cursada.",
         controlador="InscripcionController / InscripcionService",
         pre="Sesión activa con rol ADM. Se seleccionaron un alumno y una comisión existentes.",
         post="Se creó una instancia i de Inscripcion; i se asoció al Alumno y a la Comision; i.estadoAcademico = EN_CURSO."),
    dict(uc="UC-09", titulo="Registrar asistencia", dss="dss-registrar-asistencia.png", ds="ds-registrar-asistencia.png",
         operacion="confirmarAsistencia()",
         responsabilidades="Guardar la asistencia de la clase, auditarla y recalcular la regularidad.",
         controlador="AsistenciaController / AsistenciaService",
         pre="Sesión activa con rol DOC asignado a la comisión. La clase existe. La asistencia de la comisión está abierta.",
         post="Se creó o modificó una instancia de Asistencia por alumno inscripto; se creó un RegistroAuditoria por cada cambio; "
              "se actualizó Inscripcion.porcentajeAsistencia."),
    dict(uc="UC-13", titulo="Registrar nota final", dss="dss-registrar-nota-final.png", ds="ds-registrar-nota-final.png",
         operacion="registrarNotaFinal(inscripcionId, nota)",
         responsabilidades="Validar la habilitación del alumno y registrar su nota final en el acta.",
         controlador="ActaController / CalificacionService",
         pre="Sesión activa con rol DOC asignado. El acta está ABIERTA. La inscripción está en estado REGULAR.",
         post="Se creó una instancia c de Calificacion; c se asoció a la Inscripcion y a la Evaluacion FINAL; c.nota = nota."),
    dict(uc="UC-15", titulo="Cerrar acta final", dss="dss-cerrar-acta.png", ds="ds-cerrar-acta.png",
         operacion="cerrarActa(actaId)",
         responsabilidades="Verificar que el acta esté completa, fijar el resultado de cada alumno y bloquear el acta.",
         controlador="ActaController / ActaService",
         pre="Sesión activa con rol DOC asignado. El acta está ABIERTA y todos los alumnos habilitados tienen nota final.",
         post="Cada Inscripcion pasó a APROBADO o DESAPROBADO; ActaFinal.estado = CERRADA; se registraron fechaCierre y cerradaPor; "
              "se creó un RegistroAuditoria del cierre."),
]

NOTAS_MODELO_DATOS = [
    "Todas las tablas usan motor InnoDB, codificación utf8mb4 y claves primarias BIGINT autoincrementales.",
    "Las bajas lógicas se representan con las columnas estado/activo; no se eliminan filas con historial.",
    "La correlatividad es una relación muchos a muchos reflexiva sobre materia; la ausencia de ciclos se valida en la capa de negocio.",
    "La unicidad (alumno_id, comision_id) evita inscripciones repetidas en la misma comisión; la regla de no tener dos "
    "inscripciones vigentes en la misma materia (RN-10) se valida en la capa de negocio.",
    "La nota usa DECIMAL(3,1) con restricción CHECK entre 0 y 10.",
    "registro_auditoria solo admite inserciones desde la aplicación; el usuario de base de datos de la aplicación no tiene permisos UPDATE ni DELETE sobre esa tabla.",
]

PAQUETES = [
    ["app", "Punto de entrada de la aplicación, arranque y armado de dependencias."],
    ["config", "Lectura de la configuración externa (URL, usuario y contraseña de MySQL)."],
    ["presentation.view + presentation.controller", "Vistas (pantallas o páginas) y controladores: reciben las acciones del usuario, invocan servicios y muestran resultados (Vista y Controlador de MVC)."],
    ["service", "Casos de uso de la aplicación: coordinan validaciones, reglas, transacciones y auditoría."],
    ["security", "Sesión del usuario, hash de contraseñas y autorización por rol y asignación docente."],
    ["domain.model", "Entidades y enumeraciones del dominio académico (Modelo de MVC)."],
    ["domain.rule", "Reglas puras de dominio: regularidad, promedio y condición, validación de correlativas."],
    ["domain.exception", "Excepciones de negocio y de acceso denegado."],
    ["repository", "Interfaces de acceso a datos que usa la capa de negocio."],
    ["persistence", "Implementaciones de los repositorios sobre MySQL y configuración de la conexión."],
]

CAPAS = {
    "parrafos": [
        "El sistema aplica el patrón de capas (Layers) combinado con MVC. Cada capa solo depende de la "
        "capa inferior: la presentación invoca servicios, los servicios aplican reglas de dominio y usan "
        "repositorios, y los repositorios acceden a MySQL.",
        "La capa de negocio depende de las interfaces de repositorio y no de su implementación; esto "
        "permite probar las reglas académicas con repositorios en memoria y cambiar la tecnología de "
        "persistencia o de presentación sin modificar la lógica. Por eso el mismo diseño admite "
        "una variante de escritorio y una variante web.",
    ],
    "tabla": [
        ["Presentación", "Vista y Controlador", "Vistas (pantallas o páginas) y controladores. Sin reglas de negocio ni SQL."],
        ["Aplicación / Negocio", "Modelo", "Servicios, reglas de dominio, entidades y seguridad. Verifica permisos en cada operación."],
        ["Persistencia", "Modelo (acceso a datos)", "Interfaces de repositorio e implementaciones sobre MySQL con consultas parametrizadas."],
        ["Datos", "—", "Base MySQL 8 en contenedor Docker, creada con el script SQL del proyecto."],
    ],
}

TRAZABILIDAD = [
    ["US-AUTH-01", "RF-01..RF-04", "UC-01, UC-02", "TC-AUTH-01..06"],
    ["US-ALU-01..04", "RF-05..RF-08", "UC-03", "TC-ALU-01..12"],
    ["US-PROF-01..03", "RF-09..RF-11", "UC-04", "TC-PROF-01..07"],
    ["US-PROF-04", "RF-12", "UC-07", "TC-PROF-08..10"],
    ["US-MAT-01..03", "RF-13..RF-15", "UC-05", "TC-MAT-01..06"],
    ["US-MAT-04", "RF-16", "UC-05", "TC-MAT-07..09"],
    ["US-INS-01", "RF-20", "UC-08", "TC-INS-01..04"],
    ["US-ASIS-01..02", "RF-19, RF-21, RF-22", "UC-06, UC-09", "TC-ASIS-01..04"],
    ["US-ASIS-03", "RF-23", "UC-17, UC-18", "TC-ASIS-05..07"],
    ["US-ASIS-04", "RF-24", "UC-10", "Justificación con y sin motivo; efecto en el porcentaje"],
    ["US-ASIS-05", "RF-25", "UC-11", "Cierre y bloqueo de modificaciones"],
    ["US-CAL-01", "RF-26", "UC-12", "TC-CAL-01..02"],
    ["US-CAL-02", "RF-29", "UC-13", "TC-CAL-03..05"],
    ["US-CAL-03", "RF-30", "UC-14", "Modificación con auditoría; rechazo en acta cerrada"],
    ["US-CAL-04", "RF-27", "UC-12", "Recuperatorio aprobado y desaprobado"],
    ["US-CAL-05", "RF-28", "UC-11, UC-12", "Promedio y condición: PROMOCIONADO, REGULAR, DESAPROBADO"],
    ["US-CAL-06", "RF-31, RF-32", "UC-15, UC-16", "Cierre con y sin notas completas; reapertura ADM"],
    ["US-REP-01", "RF-33", "UC-17", "TC-REP-01..02"],
    ["US-REP-02", "RF-34", "UC-17", "TC-REP-03..04"],
    ["Anexo - reportes", "RF-35, RF-36", "UC-17", "Alumnos en riesgo; exportación PDF, Excel y CSV"],
    ["Anexo - auditoría", "RF-38", "UC-17", "Registro de eventos de asistencia, notas, cierres y reaperturas"],
]

ENTORNO = {
    "parrafos": [
        "La base de datos MySQL se ejecuta en un contenedor Docker definido con docker compose, que "
        "aplica el script SQL del proyecto al crear el contenedor. La variante de escritorio se compila "
        "como un archivo .jar ejecutable que se conecta a esa base; la variante web se ejecuta completa "
        "con Docker (contenedor de la aplicación y contenedor de MySQL). Las dos variantes del sistema "
        "comparten el mismo análisis, las mismas reglas de negocio, la misma arquitectura en capas MVC "
        "y el mismo modelo de datos; solo cambia la capa de presentación. Las instrucciones de "
        "instalación y ejecución se incluyen en el README del repositorio.",
    ],
    "tabla": [
        ["Lenguaje", "Java."],
        ["Arquitectura", "Capas MVC: presentación, aplicación/negocio y persistencia."],
        ["Base de datos", "MySQL 8 en Docker (docker compose), puerto 3306, volumen persistente."],
        ["Variante de escritorio", "Aplicación de escritorio compilada como archivo .jar ejecutable listo para usar; se conecta a MySQL en Docker."],
        ["Variante web", "Aplicación web del lado del servidor; aplicación y MySQL se ejecutan con Docker (docker compose)."],
        ["Configuración", "Parámetros de conexión (URL, usuario y contraseña) fuera del código fuente."],
        ["Pruebas", "Pruebas automatizadas de reglas de negocio y servicios."],
        ["Control de versiones", "Git y GitHub con Git Flow (ramas main, developer y feature/*)."],
    ],
}
