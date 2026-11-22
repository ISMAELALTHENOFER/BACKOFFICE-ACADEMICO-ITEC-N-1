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
    "permite administrar alumnos, profesores, carreras, planes de estudio, materias, comisiones, "
    "inscripciones, asistencias y notas, aplicando automáticamente las reglas académicas de "
    "regularidad y correlatividad.",
    "El sistema se desarrolla en Java con una arquitectura en capas bajo el patrón "
    "Modelo-Vista-Controlador (MVC) y persistencia en una base de datos relacional MySQL ejecutada en "
    "un contenedor Docker. El análisis y el diseño son independientes de la plataforma de presentación: "
    "el mismo modelo, las mismas reglas y la misma base de datos sirven tanto para una aplicación de "
    "escritorio como para una aplicación web.",
    "El documento reúne el escenario, las reglas del negocio, los requisitos funcionales, los casos "
    "de uso con sus diagramas de secuencia y contratos de operación, los diagramas de clases, el "
    "diagrama de estados de la cursada, el modelo de datos y la arquitectura del sistema.",
]

ESCENARIO = {
    "parrafos": [
        "El ITEC N°1 gestiona gran parte de su información académica de forma manual o mediante "
        "herramientas dispersas (planillas y registros en papel). Esto genera duplicación de datos, "
        "errores en el cálculo de la regularidad, dificultades para verificar correlativas y "
        "demoras en la emisión de reportes y actas.",
        "El instituto dicta carreras organizadas en planes de estudio con fecha de inicio y de fin. "
        "Cada plan está compuesto por materias ubicadas en un año y un cuatrimestre, que pueden tener "
        "correlativas: para cursar o rendir una materia, el alumno debe tener aprobadas sus "
        "correlativas. Los alumnos se inscriben en una o más carreras, bajo un plan de estudios y con "
        "un año de ingreso.",
        "En cada cuatrimestre lectivo se abren comisiones de las materias. Cada comisión tiene un "
        "profesor asignado y horarios de clase de lunes a viernes, compuestos por módulos horarios "
        "con hora de inicio y de fin. En cada comisión se toman exámenes: trabajos prácticos, "
        "parciales, recuperatorios y finales.",
        "El personal administrativo registra a los alumnos y profesores, define carreras, planes, "
        "materias y correlativas, arma la oferta de comisiones e inscribe a los alumnos. Un "
        "administrador, además, gestiona las cuentas del personal administrativo. Los profesores "
        "registran la asistencia de cada clase, cargan las notas y cierran las actas. Los alumnos "
        "consultan su asistencia, sus notas y el estado de sus cursadas.",
        "Un alumno es regular en una cursada cuando su asistencia es igual o superior al 70 % de las "
        "clases dictadas. Las notas van de 0 a 10 y se aprueba con 6 o más. Según el promedio de la "
        "cursada, el alumno promociona la materia, queda regular para rendir el final o debe "
        "recursarla.",
        "El sistema debe cubrir las siguientes áreas:",
    ],
    "alcance": [
        "Gestión de acceso: inicio de sesión con usuario y contraseña, roles diferenciados "
        "(Administrador, Administrativo, Profesor y Alumno) y control de permisos en cada operación.",
        "Gestión académica: alumnos y su inscripción a carreras, profesores, carreras, planes de "
        "estudio, materias, correlativas, cuatrimestres, comisiones y horarios.",
        "Inscripciones: inscripción de alumnos a comisiones con validación de plan y correlativas.",
        "Asistencia: registro por horario de clase y fecha, justificación de inasistencias, cálculo "
        "automático de regularidad y cierre de asistencia por comisión.",
        "Notas: trabajos prácticos, parciales, recuperatorios y finales, cálculo de promedio y estado "
        "de cursada, corrección auditada de notas y cierre de actas.",
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
    ["Administrador", "ADMIN",
     "Tiene todos los permisos del Administrativo y, además, crea y administra las cuentas con rol "
     "ADMIN y ADMINISTRATIVO."],
    ["Administrativo", "ADMINISTRATIVO",
     "Personal administrativo del instituto. Crea cuentas de profesores y alumnos; gestiona alumnos, "
     "profesores, carreras, planes, materias, correlativas, cuatrimestres, comisiones y horarios; "
     "inscribe alumnos a carreras y comisiones; justifica inasistencias; reabre actas y asistencias "
     "cerradas (correcciones extraordinarias); consulta reportes y auditoría."],
    ["Profesor", "PROFESOR",
     "Profesor asignado a una o más comisiones. Registra asistencia, justifica inasistencias, carga y "
     "corrige notas de sus comisiones, cierra la asistencia y las actas de finales, y consulta "
     "reportes de sus comisiones."],
    ["Alumno", "ALUMNO",
     "Estudiante del instituto. Consulta únicamente su propia asistencia, sus notas y el estado de "
     "cada cursada."],
]

REGLAS = [
    ["RN-01", "Todo usuario accede con nombre de usuario y contraseña. Las contraseñas se almacenan "
     "con un algoritmo de hash seguro con sal, nunca en texto plano.", "Baja", "US-AUTH-01"],
    ["RN-02", "Los roles del sistema son ADMIN, ADMINISTRATIVO, PROFESOR y ALUMNO; un usuario puede "
     "tener más de un rol. Solo un ADMIN crea usuarios ADMIN o ADMINISTRATIVO; un ADMIN o un "
     "ADMINISTRATIVO crean usuarios PROFESOR o ALUMNO.", "Media", "Enunciado 3.1, US-AUTH-01"],
    ["RN-03", "Los permisos se verifican en cada operación y no solo al mostrar el menú. Un usuario "
     "inactivo o con credenciales incorrectas no puede ingresar; el mensaje de error no revela qué "
     "dato fue incorrecto.", "Baja", "US-AUTH-01"],
    ["RN-04", "Todo usuario requiere nombre de usuario único, nombre, apellido, DNI único de 7 u 8 "
     "dígitos y email único con formato válido; el teléfono es opcional y tiene de 6 a 15 dígitos. "
     "Los datos personales de alumnos y profesores se guardan en su usuario. Se registra la fecha de "
     "última modificación.", "Baja", "US-ALU-01..03, US-PROF-01..02"],
    ["RN-05", "Al crear un usuario con rol ALUMNO o PROFESOR se crea el alumno o el profesor asociado "
     "(relación uno a uno), en estado ACTIVO.", "Baja", "US-ALU-01, US-PROF-01"],
    ["RN-06", "Alumnos, profesores y materias no se eliminan físicamente: la baja es lógica (estado "
     "INACTIVO / INACTIVA) y se conserva su historial académico.", "Baja", "US-ALU-04, US-PROF-03, US-MAT-03"],
    ["RN-07", "Una materia pertenece a un plan de estudios, se ubica en un año y un cuatrimestre del "
     "plan, requiere código único y nombre, y se crea en estado ACTIVA.", "Baja", "US-MAT-01..02"],
    ["RN-08", "Una materia puede tener varias correlativas. No se permite que una materia sea "
     "correlativa de sí misma ni que se formen ciclos de correlatividad de cualquier longitud.",
     "Baja", "US-MAT-04"],
    ["RN-09", "Un cuatrimestre se identifica por año y número (1 o 2) y tiene fecha de inicio y de fin; "
     "no puede repetirse la combinación de año y número.", "Baja", "Modelo de dominio"],
    ["RN-10", "Un horario de clase corresponde a un día de lunes a viernes y se compone de uno o más "
     "módulos horarios; cada módulo tiene un número, una hora de inicio y una hora de fin posterior.",
     "Baja", "Modelo de dominio"],
    ["RN-11", "Cada comisión corresponde a una materia ACTIVA y a un cuatrimestre, y tiene un único "
     "profesor asignado, que debe estar ACTIVO. Un profesor inactivo no recibe nuevas asignaciones.",
     "Media", "US-PROF-04"],
    ["RN-12", "Un alumno puede inscribirse en una o más carreras, cada una bajo un plan de estudios de "
     "esa carrera y con un año de ingreso. No puede inscribirse dos veces en la misma carrera.",
     "Media", "Modelo de dominio"],
    ["RN-13", "Una cursada es la inscripción de un alumno (en el marco de su carrera) a una comisión. "
     "No se permite inscribir a un alumno en una materia en la que ya tenga una cursada EN_CURSO, "
     "REGULAR, PROMOCIONADO o APROBADO. Puede volver a inscribirse en otro cuatrimestre si su "
     "cursada anterior terminó RECURSA, DESAPROBADO o BAJA.", "Media", "US-INS-01, decisión del proyecto"],
    ["RN-14", "Para inscribirse a una comisión, el alumno debe estar ACTIVO, la materia ACTIVA y "
     "pertenecer al plan de estudios de su carrera, y todas sus correlativas deben estar aprobadas "
     "(estado APROBADO o PROMOCIONADO). Si faltan correlativas, el sistema informa cuáles.",
     "Baja", "US-INS-01"],
    ["RN-15", "Solo el profesor de la comisión registra la asistencia de cada alumno inscripto, por "
     "horario de clase y fecha (la fecha debe coincidir con el día del horario), con estado PRESENTE, "
     "AUSENTE o JUSTIFICADA.", "Baja", "US-ASIS-01, Anexo"],
    ["RN-16", "Clases dictadas = combinaciones distintas de horario y fecha con asistencia registrada en "
     "la comisión. Porcentaje de asistencia = (presentes + justificadas) / clases dictadas × 100, con "
     "dos decimales. La condición de asistencia es REGULAR con 70 % o más (umbral inclusivo) y "
     "NO_REGULAR con menos de 70 %. Sin clases registradas se informa «Sin registros».",
     "Media", "US-ASIS-02, US-ASIS-03, decisión del proyecto"],
    ["RN-17", "Para justificar una inasistencia el motivo es obligatorio y el certificado es opcional. "
     "Una inasistencia justificada se computa como presente.", "Media", "US-ASIS-04, decisión del proyecto"],
    ["RN-18", "Al cerrar la asistencia de una comisión se congela el porcentaje y se fija el estado de "
     "cada cursada (RN-21). Luego no se modifican asistencias salvo reapertura (RN-25).",
     "Baja", "US-ASIS-05"],
    ["RN-19", "Las notas van de 0 a 10 con hasta un decimal. Una nota fuera de rango se rechaza. "
     "Una nota es aprobada si es mayor o igual a 6.", "Baja", "US-CAL-01, Anexo"],
    ["RN-20", "Cada comisión tiene dos exámenes de tipo PARCIAL (obligatorios) y puede tener exámenes "
     "de tipo TP. Cada parcial tiene un examen de tipo RECUPERATORIO vinculado, habilitado solo para "
     "los alumnos que desaprobaron ese parcial (nota menor a 6). La nota del recuperatorio reemplaza "
     "a la del parcial.", "Media", "US-CAL-04, decisión del proyecto"],
    ["RN-21", "Promedio de cursada = suma de las notas efectivas (parciales luego del recuperatorio y "
     "trabajos prácticos) / cantidad de notas. Al cerrar la asistencia, con ambos parciales cargados: "
     "asistencia menor a 70 % o promedio menor a 6 → RECURSA; asistencia de 70 % o más y promedio "
     "de 8 o más → PROMOCIONADO; asistencia de 70 % o más y promedio entre 6 y menos de 8 → REGULAR.",
     "Media", "US-CAL-05, decisión del proyecto"],
    ["RN-22", "Solo rinde final el alumno con cursada REGULAR y todas las correlativas aprobadas. Nota "
     "final mayor o igual a 6 → APROBADO; menor a 6 → DESAPROBADO. La nota se guarda como nota final "
     "de la cursada. El alumno PROMOCIONADO no rinde final.", "Baja", "US-CAL-02"],
    ["RN-23", "Un profesor solo modifica notas de sus comisiones, mientras la cursada o el acta estén "
     "abiertas. Cada modificación registra nota anterior, nota nueva, usuario y fecha.",
     "Baja", "US-CAL-03, Anexo"],
    ["RN-24", "Un acta final corresponde a un examen de tipo FINAL y solo se cierra si todos los "
     "alumnos habilitados tienen nota. Cerrada, el acta no es editable.", "Baja", "US-CAL-06"],
    ["RN-25", "Solo un ADMINISTRATIVO o un ADMIN pueden reabrir un acta o una asistencia cerrada "
     "(corrección extraordinaria), indicando un motivo obligatorio. La reapertura queda auditada.",
     "Baja", "Anexo, decisión del proyecto"],
    ["RN-26", "Se audita la carga y modificación de asistencias, la modificación de notas, los cierres "
     "y las reaperturas: acción, entidad, valor anterior, valor nuevo, usuario, fecha y motivo. "
     "Los registros de auditoría no se modifican ni se eliminan desde el sistema.", "Baja", "Anexo (EPIC-AUD)"],
    ["RN-27", "Un alumno solo puede consultar su propia información académica.", "Baja", "Decisión del proyecto"],
    ["RN-28", "Un alumno está en riesgo de pérdida de regularidad si su asistencia es menor a 70 % y en "
     "riesgo académico si su promedio es menor a 6.", "Media", "Anexo"],
]

REQUISITOS = [
    ("Seguridad y acceso", [
        ["RF-01", "Permitir iniciar sesión con usuario y contraseña y habilitar las funciones según los roles.", "US-AUTH-01"],
        ["RF-02", "Permitir cerrar sesión.", "US-AUTH-01"],
        ["RF-03", "Gestionar usuarios: crear con uno o más roles, activar, desactivar y restablecer contraseña, respetando quién puede crear cada rol.", "Enunciado 3.1"],
        ["RF-04", "Verificar los permisos de los roles en cada operación del sistema.", "US-AUTH-01, Anexo"],
    ]),
    ("Gestión de alumnos", [
        ["RF-05", "Registrar alumnos creando su usuario con rol ALUMNO, con validación de datos y DNI único.", "US-ALU-01"],
        ["RF-06", "Consultar un alumno por DNI.", "US-ALU-02"],
        ["RF-07", "Modificar los datos de un alumno.", "US-ALU-03"],
        ["RF-08", "Dar de baja lógica a un alumno conservando su historial.", "US-ALU-04"],
        ["RF-09", "Inscribir a un alumno en una carrera, bajo un plan de estudios y con año de ingreso.", "Modelo de dominio"],
    ]),
    ("Gestión de profesores", [
        ["RF-10", "Registrar profesores creando su usuario con rol PROFESOR, con validación de datos y DNI único.", "US-PROF-01"],
        ["RF-11", "Modificar los datos de un profesor.", "US-PROF-02"],
        ["RF-12", "Dar de baja lógica a un profesor conservando su historial.", "US-PROF-03"],
        ["RF-13", "Asignar el profesor de cada comisión y consultar las asignaciones.", "US-PROF-04"],
    ]),
    ("Gestión de materias", [
        ["RF-14", "Registrar materias de un plan de estudios con código único.", "US-MAT-01"],
        ["RF-15", "Modificar los datos de una materia.", "US-MAT-02"],
        ["RF-16", "Dar de baja lógica a una materia conservando su historial.", "US-MAT-03"],
        ["RF-17", "Definir correlativas de una materia, rechazando autorreferencias y ciclos.", "US-MAT-04"],
    ]),
    ("Oferta académica", [
        ["RF-18", "Gestionar carreras y planes de estudio.", "Enunciado 3.2"],
        ["RF-19", "Gestionar cuatrimestres lectivos.", "Modelo de dominio"],
        ["RF-20", "Gestionar comisiones por materia y cuatrimestre, con sus horarios de clase y módulos horarios.", "Enunciado 3.2"],
    ]),
    ("Inscripciones", [
        ["RF-21", "Inscribir alumnos a una comisión validando estado, plan, duplicados y correlativas.", "US-INS-01"],
    ]),
    ("Asistencia", [
        ["RF-22", "Registrar la asistencia por horario de clase, fecha y alumno inscripto.", "US-ASIS-01"],
        ["RF-23", "Recalcular automáticamente el porcentaje y la condición de asistencia.", "US-ASIS-02"],
        ["RF-24", "Consultar la asistencia de un alumno con presentes, ausentes, justificadas, porcentaje y condición.", "US-ASIS-03"],
        ["RF-25", "Justificar inasistencias con motivo y certificado opcional.", "US-ASIS-04"],
        ["RF-26", "Cerrar la asistencia de una comisión y fijar el estado de cada cursada.", "US-ASIS-05"],
    ]),
    ("Notas y actas", [
        ["RF-27", "Registrar exámenes de la comisión y las notas de parciales y trabajos prácticos.", "US-CAL-01"],
        ["RF-28", "Registrar recuperatorios de parciales desaprobados.", "US-CAL-04"],
        ["RF-29", "Calcular automáticamente el promedio y el estado de cursada.", "US-CAL-05"],
        ["RF-30", "Registrar notas de examen final para alumnos habilitados.", "US-CAL-02"],
        ["RF-31", "Modificar notas registrando la auditoría del cambio.", "US-CAL-03"],
        ["RF-32", "Cerrar el acta de examen final.", "US-CAL-06"],
        ["RF-33", "Reabrir actas o asistencias cerradas (ADMINISTRATIVO o ADMIN, con motivo).", "Anexo"],
    ]),
    ("Reportes y consultas", [
        ["RF-34", "Generar el reporte de asistencia y regularidad por materia y comisión.", "US-REP-01"],
        ["RF-35", "Generar el reporte de rendimiento por alumno.", "US-REP-02"],
        ["RF-36", "Generar el reporte de alumnos en riesgo.", "Anexo"],
        ["RF-37", "Generar el libro de actas y exportarlo en PDF, Excel y CSV.", "Anexo"],
        ["RF-38", "Permitir al alumno consultar su situación académica.", "US-AUTH-01, decisión del proyecto"],
        ["RF-39", "Consultar los registros de auditoría (ADMINISTRATIVO o ADMIN).", "Anexo (EPIC-AUD)"],
    ]),
]

REQUISITOS_NO_FUNCIONALES = [
    ["RNF-01", "Lenguaje Java con gestión de dependencias y construcción automatizada. La solución puede implementarse como aplicación de escritorio o como aplicación web sin cambiar el análisis ni el modelo."],
    ["RNF-02", "Arquitectura en capas MVC: la vista no contiene reglas de negocio ni acceso a datos."],
    ["RNF-03", "Persistencia en MySQL 8 con script SQL reproducible para crear el esquema y datos de ejemplo."],
    ["RNF-04", "Ejecución con Docker (docker compose): la base de datos MySQL corre en contenedor en ambas variantes; la variante web se ejecuta completa (aplicación y base) con Docker. La variante de escritorio se distribuye como un archivo .jar ejecutable listo para usar."],
    ["RNF-05", "Credenciales de conexión fuera del código fuente (variables de entorno o archivo local excluido de Git)."],
    ["RNF-06", "Contraseñas con hash seguro con sal; consultas SQL parametrizadas para evitar inyección."],
    ["RNF-07", "Operaciones de cierre y reapertura ejecutadas en una transacción: se aplican completas o no se aplican."],
    ["RNF-08", "Pruebas automatizadas que cubran cada escenario de los casos de uso, cada regla de negocio y cada caso de prueba TC-* del backlog."],
    ["RNF-09", "Control de versiones con Git y GitHub siguiendo Git Flow; documentación en la carpeta /document."],
]

EXTENSIONES_MODELO = [
    "Estado ACTIVO / INACTIVO en alumno y profesor, y ACTIVA / INACTIVA en materia, para la baja lógica.",
    "Código único de materia, exigido por la gestión de materias.",
    "Indicador de usuario activo y fechas de alta y modificación en el usuario.",
    "Estado de asistencia PRESENTE / AUSENTE / JUSTIFICADA, con motivo, certificado y usuario que la registró, en lugar de un valor presente sí/no.",
    "Vínculo del examen de recuperatorio con el parcial que recupera.",
    "Estados de cursada EN_CURSO, REGULAR, PROMOCIONADO, APROBADO, DESAPROBADO, RECURSA y BAJA, con porcentaje de asistencia y promedio.",
    "Cierre de asistencia en la comisión, acta final y registro de auditoría.",
]

# ---------- casos de uso ----------

def _uc(id_, nombre, actor, rf, paquete, prioridad, complejidad, arquitectura, traza, pre, post,
        flujo, alternativos, nivel="Usuario", categoria="Primario", tipo="Real, primario", secundario="—"):
    return dict(id=id_, nombre=nombre, actor=actor, rf=rf, paquete=paquete, prioridad=prioridad,
                complejidad=complejidad, arquitectura=arquitectura, traza=traza, pre=pre, post=post,
                flujo=flujo, alternativos=alternativos, nivel=nivel, categoria=categoria, tipo=tipo,
                secundario=secundario)


ADMINS = "ADMINISTRATIVO, ADMIN"

CASOS_DE_USO = [
    _uc("UC-01", "Iniciar sesión", "ADMIN, ADMINISTRATIVO, PROFESOR, ALUMNO", "RF-01, RF-02, RF-04", "Seguridad",
        "Alta", "Media", "Sí", "US-AUTH-01 / TC-AUTH-01..06",
        "El usuario está registrado en el sistema.",
        "Existe una sesión activa asociada al usuario y sus roles; se muestra el menú correspondiente.",
        ["El usuario inicia la aplicación.",
         "El sistema muestra la pantalla de inicio de sesión.",
         "El usuario ingresa nombre de usuario y contraseña y confirma.",
         "El sistema verifica que el usuario exista, esté activo y que la contraseña coincida con el hash almacenado.",
         "El sistema inicia la sesión y muestra el menú habilitado para sus roles."],
        ["3a. Campos vacíos: el sistema solicita completarlos y vuelve al paso 3.",
         "4a. Usuario inexistente o contraseña incorrecta: el sistema muestra «Usuario o contraseña incorrectos» y vuelve al paso 3.",
         "4b. Usuario inactivo: el sistema deniega el acceso con el mismo mensaje genérico.",
         "*a. En cualquier momento el usuario cierra sesión: el sistema finaliza la sesión y vuelve al paso 2."]),
    _uc("UC-02", "Gestionar usuarios", ADMINS, "RF-03", "Seguridad", "Alta", "Media", "No",
        "Enunciado 3.1",
        "Sesión iniciada con rol ADMINISTRATIVO o ADMIN.",
        "El usuario queda creado o actualizado con sus roles y estado.",
        ["El usuario selecciona «Usuarios».",
         "El sistema lista los usuarios con sus roles y estado.",
         "El usuario elige crear una cuenta e ingresa nombre de usuario, contraseña inicial, datos personales y roles.",
         "El sistema verifica que quien opera pueda asignar esos roles, valida los datos y la unicidad de nombre de usuario, DNI y email, guarda la contraseña con hash y registra el usuario activo.",
         "Si algún rol es ALUMNO o PROFESOR, el sistema crea el alumno o profesor asociado.",
         "El sistema confirma la operación."],
        ["3a. El usuario modifica roles, activa o desactiva una cuenta o restablece su contraseña: el sistema valida y guarda el cambio.",
         "4a. Un ADMINISTRATIVO intenta crear o modificar una cuenta ADMIN o ADMINISTRATIVO: el sistema deniega la operación.",
         "4b. Nombre de usuario, DNI o email duplicado: el sistema informa el error y vuelve al paso 3."]),
    _uc("UC-03", "Gestionar alumnos e inscripción a carrera", ADMINS, "RF-05..RF-09", "Gestión académica",
        "Alta", "Media", "No", "US-ALU-01..04 / TC-ALU-01..12",
        "Sesión iniciada con rol ADMINISTRATIVO o ADMIN.",
        "El alumno queda registrado, actualizado, dado de baja lógica o inscripto en una carrera.",
        ["El usuario selecciona «Alumnos».",
         "El sistema muestra el buscador por DNI y el listado de alumnos.",
         "El usuario elige «Nuevo» e ingresa nombre de usuario, contraseña inicial, nombre, apellido, DNI, email y teléfono.",
         "El sistema valida los campos obligatorios, el formato de DNI, email y teléfono, y que no existan el DNI, el email ni el nombre de usuario.",
         "El sistema crea el usuario con rol ALUMNO y el alumno en estado ACTIVO, y confirma.",
         "El usuario elige «Inscribir en carrera», selecciona carrera, plan de estudios y año de ingreso.",
         "El sistema verifica que el plan pertenezca a la carrera y que el alumno no esté ya inscripto en ella, y registra la inscripción."],
        ["2a. Consultar: el usuario ingresa un DNI; el sistema muestra los datos y carreras o «Alumno no encontrado».",
         "2b. Modificar: el usuario edita los datos de un alumno; el sistema valida, guarda y actualiza la fecha de modificación.",
         "2c. Dar de baja: el usuario confirma la baja; el sistema cambia el estado a INACTIVO y conserva el historial.",
         "4a. DNI, email o nombre de usuario duplicado: el sistema informa el error y no crea el registro.",
         "4b. Formato inválido o campo obligatorio vacío: el sistema indica el campo con error.",
         "7a. El alumno ya está inscripto en esa carrera: el sistema informa el error."]),
    _uc("UC-04", "Gestionar profesores", ADMINS, "RF-10..RF-12", "Gestión académica", "Alta", "Baja", "No",
        "US-PROF-01..03 / TC-PROF-01..07",
        "Sesión iniciada con rol ADMINISTRATIVO o ADMIN.",
        "El profesor queda registrado, actualizado o dado de baja lógica.",
        ["El usuario selecciona «Profesores».",
         "El sistema muestra el listado de profesores.",
         "El usuario elige «Nuevo» e ingresa nombre de usuario, contraseña inicial, nombre, apellido, DNI, email y teléfono.",
         "El sistema valida los campos y la unicidad de DNI, email y nombre de usuario.",
         "El sistema crea el usuario con rol PROFESOR y el profesor en estado ACTIVO, y confirma."],
        ["2a. Modificar: el sistema valida y guarda los cambios; si el profesor no existe informa «no encontrado».",
         "2b. Dar de baja: el sistema cambia el estado a INACTIVO; el profesor no recibe nuevas asignaciones.",
         "4a. DNI duplicado o email inválido: el sistema informa el error y no guarda."]),
    _uc("UC-05", "Gestionar materias y correlativas", ADMINS, "RF-14..RF-17", "Gestión académica", "Alta", "Media", "Sí",
        "US-MAT-01..04 / TC-MAT-01..09",
        "Sesión iniciada con rol ADMINISTRATIVO o ADMIN; existe al menos un plan de estudios.",
        "La materia queda registrada, actualizada, dada de baja o con sus correlativas definidas.",
        ["El usuario selecciona «Materias».",
         "El sistema muestra las materias por plan de estudios.",
         "El usuario elige «Nueva» e ingresa código, nombre, plan, año y cuatrimestre.",
         "El sistema valida que el código sea único y registra la materia en estado ACTIVA.",
         "El usuario selecciona «Correlativas» y elige las materias requeridas.",
         "El sistema verifica que no haya autorreferencia ni ciclos y guarda las correlativas."],
        ["2a. Modificar o dar de baja una materia: el sistema guarda el cambio; una materia INACTIVA no acepta nuevas inscripciones.",
         "4a. Código duplicado: el sistema informa el error.",
         "6a. La materia se elige como correlativa de sí misma: el sistema rechaza la operación.",
         "6b. Se detecta un ciclo (por ejemplo A → B → C → A): el sistema rechaza la operación e indica el ciclo."]),
    _uc("UC-06", "Gestionar oferta académica", ADMINS, "RF-18..RF-20", "Gestión académica", "Alta", "Media", "Sí",
        "Enunciado 3.2, modelo de dominio",
        "Sesión iniciada con rol ADMINISTRATIVO o ADMIN.",
        "Quedan definidas carreras, planes, cuatrimestres, módulos horarios, comisiones y sus horarios.",
        ["El usuario selecciona «Oferta académica».",
         "El usuario registra o selecciona la carrera y sus planes de estudio (nombre, fecha de inicio y de fin).",
         "El usuario registra el cuatrimestre lectivo (año, número, fecha de inicio y de fin).",
         "El usuario crea una comisión indicando materia, cuatrimestre y profesor.",
         "El usuario agrega los horarios de la comisión: día de lunes a viernes y módulos horarios.",
         "El sistema valida las reglas (cuatrimestre no repetido, materia activa, módulos válidos) y guarda."],
        ["3a. Cuatrimestre repetido para el año y número: el sistema informa el error.",
         "5a. No existen módulos horarios: el usuario registra módulos (número, hora de inicio y de fin); el sistema valida que la hora de fin sea posterior."]),
    _uc("UC-07", "Asignar profesor a comisión", ADMINS, "RF-13", "Gestión académica", "Alta", "Baja", "No",
        "US-PROF-04 / TC-PROF-08..10",
        "Sesión iniciada con rol ADMINISTRATIVO o ADMIN; existen el profesor y la comisión.",
        "La comisión queda con el profesor asignado.",
        ["El usuario selecciona una comisión.",
         "El sistema muestra el profesor asignado, si existe.",
         "El usuario elige un profesor.",
         "El sistema verifica que el profesor esté ACTIVO y la materia ACTIVA, y registra la asignación.",
         "El sistema muestra la asignación actualizada."],
        ["4a. Profesor INACTIVO: el sistema rechaza la asignación.",
         "4b. Materia INACTIVA: el sistema rechaza la asignación.",
         "4c. La comisión ya tiene profesor: el sistema solicita confirmar el reemplazo."]),
    _uc("UC-08", "Inscribir alumno a comisión", ADMINS, "RF-21", "Inscripciones", "Alta", "Alta", "Sí",
        "US-INS-01 / TC-INS-01..04, TC-ALU-12, TC-MAT-06",
        "Sesión iniciada con rol ADMINISTRATIVO o ADMIN; el alumno está inscripto en una carrera; existe la comisión.",
        "Existe una cursada (alumno inscripto) en estado EN_CURSO.",
        ["El usuario selecciona «Inscripciones» e ingresa el DNI del alumno.",
         "El sistema muestra los datos, el estado y las carreras del alumno.",
         "El usuario selecciona la carrera del alumno y la comisión.",
         "El sistema muestra la materia, el cuatrimestre, el profesor y los horarios.",
         "El usuario confirma la inscripción.",
         "El sistema valida alumno ACTIVO, materia ACTIVA y del plan del alumno, ausencia de cursada vigente y correlativas aprobadas.",
         "El sistema registra la cursada en estado EN_CURSO y confirma."],
        ["2a. Alumno inexistente: el sistema informa «Alumno no encontrado».",
         "6a. Alumno INACTIVO o materia INACTIVA: el sistema bloquea la inscripción.",
         "6b. La materia no pertenece al plan de la carrera del alumno: el sistema rechaza la inscripción.",
         "6c. Inscripción duplicada: el sistema informa que el alumno ya cursa o aprobó la materia.",
         "6d. Correlativas faltantes: el sistema informa la lista de materias que faltan aprobar."]),
    _uc("UC-09", "Registrar asistencia", "PROFESOR", "RF-22, RF-23", "Asistencia", "Alta", "Alta", "Sí",
        "US-ASIS-01..02 / TC-ASIS-01..04",
        "Sesión iniciada con rol PROFESOR; es el profesor de la comisión; la asistencia de la comisión está abierta.",
        "La asistencia queda registrada, auditada y el porcentaje de cada alumno recalculado.",
        ["El profesor selecciona una de sus comisiones, un horario de clase y la fecha.",
         "El sistema muestra los alumnos inscriptos con la asistencia previa de esa fecha, si existe.",
         "El profesor marca PRESENTE o AUSENTE para cada alumno.",
         "El profesor confirma.",
         "El sistema guarda las asistencias, registra la auditoría y recalcula el porcentaje y la condición de asistencia.",
         "El sistema muestra el resultado con la condición de cada alumno."],
        ["1a. El usuario no es el profesor de la comisión: el sistema deniega la operación.",
         "1b. La fecha no coincide con el día del horario: el sistema rechaza la fecha.",
         "5a. La asistencia de la comisión está cerrada: el sistema rechaza la modificación."]),
    _uc("UC-10", "Justificar inasistencia", "PROFESOR, " + ADMINS, "RF-25, RF-23", "Asistencia", "Media", "Baja", "No",
        "US-ASIS-04",
        "Existe una asistencia AUSENTE; la asistencia de la comisión está abierta (o fue reabierta).",
        "La asistencia queda JUSTIFICADA y el porcentaje recalculado.",
        ["El usuario busca al alumno y selecciona la inasistencia.",
         "El sistema muestra la fecha y el horario.",
         "El usuario ingresa el motivo y, opcionalmente, adjunta el certificado.",
         "El sistema valida el motivo, cambia el estado a JUSTIFICADA, registra la auditoría y recalcula el porcentaje."],
        ["4a. Motivo vacío: el sistema solicita completarlo.",
         "4b. Un PROFESOR que no es el de la comisión: el sistema deniega la operación."]),
    _uc("UC-11", "Cerrar asistencia de comisión", "PROFESOR", "RF-26, RF-29", "Asistencia", "Alta", "Media", "Sí",
        "US-ASIS-05, US-CAL-05",
        "Profesor de la comisión; la asistencia está abierta; los parciales están cargados.",
        "La asistencia queda cerrada y cada cursada con su estado RECURSA, REGULAR o PROMOCIONADO.",
        ["El profesor selecciona la comisión y elige «Cerrar asistencia».",
         "El sistema muestra, por alumno, el porcentaje, el promedio y el estado resultante.",
         "El profesor confirma el cierre.",
         "El sistema, en una transacción, congela porcentajes, asigna el estado de cada cursada, marca la comisión como cerrada y audita."],
        ["2a. Hay alumnos sin ambos parciales: el sistema lista los pendientes y no permite cerrar.",
         "2b. No hay clases registradas: el sistema informa «Sin registros» y no permite cerrar."]),
    _uc("UC-12", "Registrar nota de cursada", "PROFESOR", "RF-27, RF-28, RF-29", "Notas", "Alta", "Media", "Sí",
        "US-CAL-01, US-CAL-04, US-CAL-05 / TC-CAL-01..02",
        "Profesor de la comisión; la cursada está abierta.",
        "La nota queda registrada y el promedio recalculado.",
        ["El profesor selecciona la comisión y el examen (PARCIAL, RECUPERATORIO o TP), o crea uno con fecha, tipo y descripción.",
         "El sistema lista los alumnos inscriptos.",
         "El profesor ingresa la nota de cada alumno.",
         "El sistema valida el rango 0 a 10, registra las notas y recalcula el promedio."],
        ["1a. Recuperatorio: el profesor indica el parcial que recupera; el sistema solo habilita a los alumnos con ese parcial menor a 6 y la nota reemplaza a la del parcial.",
         "4a. Nota fuera de rango: el sistema rechaza el valor.",
         "4b. Ya existe una nota para ese alumno y examen: el sistema deriva a «Modificar nota» (UC-14)."]),
    _uc("UC-13", "Registrar nota final", "PROFESOR", "RF-30", "Notas", "Alta", "Media", "Sí",
        "US-CAL-02 / TC-CAL-03..05",
        "Profesor de la comisión; existe un acta final ABIERTA para un examen FINAL de la comisión.",
        "La nota final queda registrada en el acta.",
        ["El profesor selecciona el acta final.",
         "El sistema lista los alumnos con cursada REGULAR habilitados.",
         "El profesor ingresa la nota final de un alumno.",
         "El sistema valida rango, estado REGULAR y correlativas aprobadas, y registra la nota."],
        ["4a. Cursada no REGULAR (TC-CAL-05): el sistema rechaza la carga.",
         "4b. Correlativas pendientes: el sistema rechaza e informa cuáles faltan.",
         "4c. Acta cerrada: el sistema rechaza la carga."]),
    _uc("UC-14", "Modificar nota", "PROFESOR", "RF-31", "Notas", "Media", "Media", "Sí",
        "US-CAL-03",
        "Profesor de la comisión; la cursada o el acta están abiertas.",
        "La nota queda corregida y el cambio auditado.",
        ["El profesor busca la nota a corregir.",
         "El sistema muestra la nota actual.",
         "El profesor ingresa la nota nueva.",
         "El sistema valida, guarda, recalcula el promedio y registra la auditoría (nota anterior, nota nueva, usuario y fecha)."],
        ["4a. Acta o asistencia cerrada: el sistema rechaza el cambio (solo un ADMINISTRATIVO o ADMIN puede reabrir).",
         "4b. No es el profesor de la comisión: el sistema deniega la operación."]),
    _uc("UC-15", "Cerrar acta final", "PROFESOR", "RF-32", "Notas", "Alta", "Media", "Sí",
        "US-CAL-06",
        "Profesor de la comisión; el acta está ABIERTA.",
        "El acta queda CERRADA y cada cursada con estado APROBADO o DESAPROBADO y su nota final.",
        ["El profesor selecciona el acta y elige «Cerrar acta».",
         "El sistema verifica que todos los alumnos habilitados tengan nota final.",
         "El sistema, en una transacción, aplica APROBADO (nota >= 6) o DESAPROBADO (nota < 6), guarda la nota final de cada cursada, marca el acta como CERRADA y audita el cierre.",
         "El sistema confirma el cierre."],
        ["2a. Faltan notas: el sistema lista los alumnos sin nota final y no cierra."]),
    _uc("UC-16", "Reabrir acta o asistencia", ADMINS, "RF-33", "Notas", "Media", "Media", "Sí",
        "Anexo - Reglas de seguridad",
        "Sesión iniciada con rol ADMINISTRATIVO o ADMIN; el acta o la asistencia están cerradas.",
        "El acta o la asistencia quedan abiertas y la reapertura auditada.",
        ["El usuario selecciona el acta o la comisión cerrada.",
         "El usuario elige «Reabrir» e ingresa el motivo.",
         "El sistema valida el motivo, reabre el registro, devuelve las cursadas afectadas al estado previo correspondiente y registra la auditoría."],
        ["3a. Motivo vacío: el sistema solicita completarlo."]),
    _uc("UC-17", "Generar reportes académicos", "PROFESOR, " + ADMINS, "RF-34..RF-37, RF-39", "Reportes", "Alta", "Media", "No",
        "US-REP-01..02, Anexo / TC-REP-01..04",
        "Sesión iniciada; un PROFESOR solo accede a sus comisiones.",
        "Se muestra o exporta el reporte solicitado.",
        ["El usuario selecciona el reporte: asistencia por materia, rendimiento por alumno, alumnos en riesgo o libro de actas.",
         "El usuario indica los filtros (materia, comisión, cuatrimestre o alumno).",
         "El sistema calcula y muestra el reporte.",
         "Opcionalmente, el usuario exporta el libro de actas en PDF, Excel o CSV."],
        ["3a. Sin asistencias registradas: el sistema informa «Sin registros».",
         "3b. Alumno sin notas: el sistema informa «Sin calificaciones registradas».",
         "1a. Consultar auditoría (ADMINISTRATIVO o ADMIN): el sistema lista los eventos filtrados por fecha, usuario o entidad."]),
    _uc("UC-18", "Consultar situación académica", "ALUMNO", "RF-38, RF-24", "Reportes", "Media", "Baja", "No",
        "US-AUTH-01 (menú alumno), US-ASIS-03",
        "Sesión iniciada con rol ALUMNO.",
        "Se muestra la información académica del propio alumno.",
        ["El alumno selecciona «Mi situación académica».",
         "El sistema muestra sus carreras y cursadas con asistencia (presentes, ausentes, justificadas y porcentaje), notas, promedio y estado."],
        ["2a. Sin inscripciones: el sistema informa que no posee cursadas registradas."]),
]

CONTRATOS = [
    dict(uc="UC-01", titulo="Iniciar sesión", dss="dss-iniciar-sesion.png", ds="ds-iniciar-sesion.png",
         operacion="iniciarSesion(username: String, contraseña: char[])",
         responsabilidades="Autenticar al usuario, verificar su estado y abrir una sesión con sus roles.",
         controlador="AuthController / AuthService",
         pre="Existe un usuario con ese nombre de usuario.",
         post="Se creó una instancia de Sesion asociada al User; la contraseña no se conserva en memoria."),
    dict(uc="UC-03", titulo="Crear alumno", dss="dss-crear-alumno.png", ds="ds-crear-alumno.png",
         operacion="crearAlumno(username, contraseña, nombre, apellido, dni, email, teléfono)",
         responsabilidades="Validar los datos y registrar el usuario con rol ALUMNO y el alumno asociado.",
         controlador="AlumnoController / AlumnoService",
         pre="Sesión activa con rol ADMINISTRATIVO o ADMIN. No existe un usuario con el DNI, email o nombre de usuario indicados.",
         post="Se creó una instancia u de User con roles = {ALUMNO} y activo = verdadero; se creó una instancia a de Alumno "
              "asociada a u con estado ACTIVO."),
    dict(uc="UC-08", titulo="Inscribir alumno a comisión", dss="dss-inscribir-alumno.png", ds="ds-inscribir-alumno.png",
         operacion="confirmarInscripcion()",
         responsabilidades="Validar las reglas de inscripción y registrar la cursada.",
         controlador="InscripcionController / InscripcionService",
         pre="Sesión activa con rol ADMINISTRATIVO o ADMIN. Se seleccionaron un AlumnoCarrera y una ComisionMateria existentes.",
         post="Se creó una instancia i de AlumnoInscripto; i se asoció al AlumnoCarrera y a la ComisionMateria; i.estado = EN_CURSO."),
    dict(uc="UC-09", titulo="Registrar asistencia", dss="dss-registrar-asistencia.png", ds="ds-registrar-asistencia.png",
         operacion="confirmarAsistencia()",
         responsabilidades="Guardar la asistencia del horario y fecha, auditarla y recalcular la regularidad.",
         controlador="AsistenciaController / AsistenciaService",
         pre="Sesión activa con rol PROFESOR, profesor de la comisión. El horario existe y la fecha coincide con su día. La asistencia de la comisión está abierta.",
         post="Se creó o modificó una instancia de Asistencia por alumno inscripto; se creó un RegistroAuditoria por cada cambio; "
              "se actualizó AlumnoInscripto.porcentajeAsistencia."),
    dict(uc="UC-13", titulo="Registrar nota final", dss="dss-registrar-nota-final.png", ds="ds-registrar-nota-final.png",
         operacion="registrarNotaFinal(inscriptoId, valor)",
         responsabilidades="Validar la habilitación del alumno y registrar su nota final en el acta.",
         controlador="ActaController / NotaService",
         pre="Sesión activa con rol PROFESOR, profesor de la comisión. El acta está ABIERTA. La cursada está en estado REGULAR.",
         post="Se creó una instancia n de Nota; n se asoció al AlumnoInscripto y al Examen FINAL; n.valor = valor."),
    dict(uc="UC-15", titulo="Cerrar acta final", dss="dss-cerrar-acta.png", ds="ds-cerrar-acta.png",
         operacion="cerrarActa(actaId)",
         responsabilidades="Verificar que el acta esté completa, fijar el resultado de cada alumno y bloquear el acta.",
         controlador="ActaController / ActaService",
         pre="Sesión activa con rol PROFESOR, profesor de la comisión. El acta está ABIERTA y todos los alumnos habilitados tienen nota final.",
         post="Cada AlumnoInscripto pasó a APROBADO o DESAPROBADO y se registró su notaFinal; ActaFinal.estado = CERRADA; "
              "se registraron fechaCierre y cerradaPor; se creó un RegistroAuditoria del cierre."),
]

NOTAS_MODELO_DATOS = [
    "Todas las tablas usan motor InnoDB, codificación utf8mb4 y claves primarias BIGINT autoincrementales.",
    "Los roles de cada usuario se guardan en la tabla user_roles (un usuario puede tener varios roles).",
    "Las bajas lógicas se representan con las columnas estado/activo; no se eliminan filas con historial.",
    "Las correlativas son una relación muchos a muchos reflexiva sobre materia (tabla correlativas); la ausencia de ciclos se valida en la capa de negocio.",
    "La composición de horarios por módulos es una relación muchos a muchos (tabla horario_modulos).",
    "La unicidad (alumno_carrera_id, comision_id) evita inscripciones repetidas en la misma comisión; la regla de no tener dos "
    "cursadas vigentes en la misma materia (RN-13) se valida en la capa de negocio.",
    "La nota usa DECIMAL(3,1) con restricción CHECK entre 0 y 10.",
    "registro_auditoria solo admite inserciones desde la aplicación; el usuario de base de datos de la aplicación no tiene permisos UPDATE ni DELETE sobre esa tabla.",
]

PAQUETES = [
    ["view", "Vistas (pantallas o páginas): muestran datos y capturan las acciones del usuario (Vista de MVC)."],
    ["controller", "Controladores: reciben las acciones, invocan servicios y devuelven resultados a la vista (Controlador de MVC)."],
    ["dto", "Objetos de transferencia de datos de entrada y salida (XRequest / XResponse)."],
    ["service", "Interfaces de los casos de uso de la aplicación (XService)."],
    ["service.impl", "Implementaciones de los servicios (XServiceImpl): coordinan validaciones, reglas, transacciones y auditoría."],
    ["rule", "Reglas puras de dominio: regularidad, promedio y estado de cursada, validación de correlativas."],
    ["security", "Sesión del usuario, hash de contraseñas y autorización por rol y por profesor de la comisión."],
    ["model", "Entidades y enumeraciones del dominio académico (Modelo de MVC)."],
    ["exception", "Excepciones de negocio, de datos existentes y de acceso denegado."],
    ["repository", "Interfaces de acceso a datos (XRepository); su implementación depende de la variante."],
    ["configuration", "Configuración externa: conexión a MySQL y parámetros de la aplicación."],
]

CAPAS = {
    "parrafos": [
        "El sistema aplica el patrón de capas (Layers) combinado con MVC. Cada capa solo depende de la "
        "capa inferior: la vista delega en los controladores, los controladores invocan servicios, los "
        "servicios aplican reglas de dominio y usan repositorios, y los repositorios acceden a MySQL.",
        "La capa de negocio depende de las interfaces de repositorio y no de su implementación; esto "
        "permite probar las reglas académicas de forma aislada y cambiar la tecnología de persistencia "
        "o de presentación sin modificar la lógica. Por eso el mismo diseño admite una variante de "
        "escritorio y una variante web.",
    ],
    "tabla": [
        ["Presentación", "Vista y Controlador", "Paquetes view y controller (y dto). Sin reglas de negocio ni SQL."],
        ["Aplicación / Negocio", "Modelo", "Paquetes service, service.impl, rule, model, security y exception. Verifica permisos en cada operación."],
        ["Persistencia", "Modelo (acceso a datos)", "Paquete repository: interfaces e implementaciones sobre MySQL con consultas parametrizadas."],
        ["Datos", "—", "Base MySQL 8 en contenedor Docker, creada con el script SQL del proyecto."],
    ],
}

TRAZABILIDAD = [
    ["US-AUTH-01", "RF-01..RF-04", "UC-01, UC-02", "TC-AUTH-01..06"],
    ["US-ALU-01..04", "RF-05..RF-08", "UC-03", "TC-ALU-01..12"],
    ["Modelo de dominio", "RF-09", "UC-03", "Inscripción a carrera válida y duplicada"],
    ["US-PROF-01..03", "RF-10..RF-12", "UC-04", "TC-PROF-01..07"],
    ["US-PROF-04", "RF-13", "UC-07", "TC-PROF-08..10"],
    ["US-MAT-01..03", "RF-14..RF-16", "UC-05", "TC-MAT-01..06"],
    ["US-MAT-04", "RF-17", "UC-05", "TC-MAT-07..09"],
    ["Modelo de dominio", "RF-18..RF-20", "UC-06", "Cuatrimestre repetido; horarios y módulos válidos"],
    ["US-INS-01", "RF-21", "UC-08", "TC-INS-01..04; materia fuera del plan"],
    ["US-ASIS-01..02", "RF-22, RF-23", "UC-09", "TC-ASIS-01..04"],
    ["US-ASIS-03", "RF-24", "UC-17, UC-18", "TC-ASIS-05..07"],
    ["US-ASIS-04", "RF-25", "UC-10", "Justificación con y sin motivo; efecto en el porcentaje"],
    ["US-ASIS-05", "RF-26", "UC-11", "Cierre y bloqueo de modificaciones"],
    ["US-CAL-01", "RF-27", "UC-12", "TC-CAL-01..02"],
    ["US-CAL-02", "RF-30", "UC-13", "TC-CAL-03..05"],
    ["US-CAL-03", "RF-31", "UC-14", "Modificación con auditoría; rechazo en acta cerrada"],
    ["US-CAL-04", "RF-28", "UC-12", "Recuperatorio aprobado y desaprobado"],
    ["US-CAL-05", "RF-29", "UC-11, UC-12", "Promedio y estado: PROMOCIONADO, REGULAR, RECURSA"],
    ["US-CAL-06", "RF-32, RF-33", "UC-15, UC-16", "Cierre con y sin notas completas; reapertura"],
    ["US-REP-01", "RF-34", "UC-17", "TC-REP-01..02"],
    ["US-REP-02", "RF-35", "UC-17", "TC-REP-03..04"],
    ["Anexo - reportes", "RF-36, RF-37", "UC-17", "Alumnos en riesgo; exportación PDF, Excel y CSV"],
    ["Anexo - auditoría", "RF-39", "UC-17", "Registro de eventos de asistencia, notas, cierres y reaperturas"],
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
