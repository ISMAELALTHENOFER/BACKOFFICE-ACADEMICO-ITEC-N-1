# Plan para completar el Backoffice Académico ITEC N.º 1

Este documento convierte el enunciado, el backlog, el anexo y el diagrama en un plan verificable. **No describe funcionalidades ya implementadas**: al momento de redactarlo solo existe un proyecto Maven Java 20 cuyo `main` imprime `Hello World!` (`BackOffice/pom.xml` y `BackOffice/src/main/java/itec/backoffice/BackOffice.java`). Las casillas se marcan únicamente al implementar y comprobar cada entrega.

## Fuentes y criterio de lectura

| Fuente | Qué aporta |
| --- | --- |
| [`backoffice_itec_enunciado.docx`](backoffice_itec_enunciado.docx) | Objetivo, requisitos técnicos, diagramas y entregables obligatorios. |
| [`Requerimientos.docx`](Requerimientos.docx) | Historias `US-AUTH-01` a `US-REP-02`, reglas, dependencias y casos de prueba `TC-*`. |
| [`Anexo Requerimientos.docx`](Anexo%20Requerimientos.docx) | Extensiones de asistencia y calificaciones, auditoría, reportes adicionales y funcionalidades opcionales. |
| [`backoffice-itec.jpeg`](backoffice-itec.jpeg) | Boceto visual del modelo académico; no sustituye las reglas escritas ni un modelo de datos validado. |

**Convención:** «obligatorio» significa indicado en el enunciado o una historia; «sugerido/opcional» conserva esa condición de la fuente. Las decisiones abiertas se acuerdan antes de programar su comportamiento. Los endpoints del backlog están marcados «opcionales si API»: no obligan a elegir una API ni a implementar esas rutas si se elige otra plataforma.

## Definiciones pendientes antes de implementar

- [ ] Elegir Web, Desktop o API + cliente; el enunciado permite las tres, pero exige Java y arquitectura en capas MVC. Definir cómo se usará la aplicación de punta a punta.
- [ ] Elegir base relacional o no relacional y su esquema; el enunciado exige **script SQL**, por lo que si se elige una base no relacional hay que aclarar qué cubrirá ese entregable antes de avanzar.
- [ ] Aclarar si «Administrador» y «Administrativo» son roles diferentes o el mismo; el enunciado enumera ambos, mientras el backlog usa `ADM`. Definir quién crea cuentas y cómo se asignan roles.
- [ ] Definir identidad y reglas de cada cursada: carrera, plan de estudios, materia, cuatrimestre/semestre, comisión y período. Precisar qué significa «no duplicar inscripción» y si un alumno puede recursar una materia en otra comisión o período.
- [ ] Fijar escala, redondeo y cálculo de calificaciones: el backlog propone `0..10` y aprobación con nota **mayor o igual a 6**; el anexo permite elegir si el recuperatorio reemplaza o promedia, y llama «configurable» al promedio. Definir promoción, parciales requeridos, cantidad de recuperatorios y relación entre regularidad y aprobación.
- [ ] Definir el denominador del 70 % de asistencia (clases registradas, justificadas y ausencia de clases), el efecto exacto de justificar una falta, y cuándo se recalcula o congela la regularidad.
- [ ] Definir el procedimiento de reapertura/corrección extraordinaria de actas y asistencia cerradas, con permisos y auditoría; el anexo prohíbe editar actas cerradas y reserva el desbloqueo a `ADM`.
- [ ] Definir integrantes, entorno de ejecución, estrategia de despliegue en Docker y datos de ejemplo para la entrega.

## Plan de trabajo, en orden de dependencias

### 1. Base técnica y modelo académico

- [ ] Sustituir el ejemplo `Hello World!` por un proyecto ejecutable con capas claras de presentación, aplicación/negocio y persistencia (MVC), sin atar reglas de negocio a la interfaz. Mantener Java y Maven.
- [ ] Diseñar y crear el esquema persistente, relaciones, claves, restricciones y migración/creación reproducible; entregar el **script SQL obligatorio** y datos mínimos de demostración. Proteger historial en bajas lógicas.
- [ ] Modelar alumnos, docentes, materias, correlativas, carreras, planes, semestres, comisiones, horarios, clases, inscripciones, asistencias, evaluaciones, calificaciones, actas y auditoría según las funciones acordadas. Validar cardinalidades y nombres antes de copiar la imagen al código.
- [ ] Habilitar configuración externa del entorno (conexión a datos y secretos), manejo de errores y ejecución local reproducible. No guardar contraseñas ni credenciales en el repositorio.

### 2. Acceso y catálogos académicos

- [ ] `US-AUTH-01`: iniciar sesión con usuario/contraseña; hash seguro, usuarios activos, rechazo de credenciales incorrectas y autorización por rol en **cada operación**, no solo en el menú. Probar `TC-AUTH-01` a `TC-AUTH-06` para `ADM`, `DOC` y `ALU`.
- [ ] `US-ALU-01..04`: alta, consulta por DNI, modificación y baja lógica de alumnos. Validar nombre, apellido, DNI único, email y teléfono; alta `ACTIVO`; última modificación; preservar historial y bloquear nuevas inscripciones de inactivos. Probar `TC-ALU-01..12`.
- [ ] `US-PROF-01..03`: alta, modificación y baja lógica de docentes; DNI único, email válido, estado `ACTIVO`, historial conservado y prohibición de nuevas asignaciones de inactivos. Probar `TC-PROF-01..07`.
- [ ] `US-MAT-01..03`: alta, modificación y baja lógica de materias; código/nombre obligatorio, código único cuando se use, estado `ACTIVA`, historial conservado y bloqueo de inscripciones nuevas a materias inactivas. Probar `TC-MAT-01..06`.
- [ ] `US-MAT-04`: definir correlativas múltiples, rechazando autorreferencias y ciclos de cualquier longitud. Probar `TC-MAT-07..09`.
- [ ] `US-PROF-04`: asignar docentes activos a materias activas y mostrar la asignación. Acordar si hay docente responsable y co-docentes. Probar `TC-PROF-08..10`.
- [ ] Crear/consultar la oferta de cursadas y clases por comisión, período y horario para que inscripciones, asistencia y exámenes se vinculen a una instancia concreta; el diagrama incluye estos conceptos, pero las operaciones exactas aún requieren definición.

### 3. Inscripciones, asistencia y regularidad

- [ ] `US-INS-01`: inscribir alumno activo en materia activa sin duplicar la cursada; exigir correlativas aprobadas e informar cuáles faltan. Probar `TC-INS-01..04` y bloqueo de materia inactiva (`TC-MAT-06`).
- [ ] `US-ASIS-01`: docente autenticado y asignado registra presente/ausente por alumno inscripto y fecha/clase; impedir modificaciones de otro docente. Probar `TC-ASIS-01..02`.
- [ ] `US-ASIS-02`: recalcular regularidad automáticamente con umbral inclusivo de **70 %**, usando la base de clases definida. Probar 70 % exacto y 69,9 % (`TC-ASIS-03..04`).
- [ ] `US-ASIS-03`: consulta del historial por alumno con presentes, ausentes, justificadas, porcentaje y condición; resolver «sin asistencias». Probar `TC-ASIS-05..07`.
- [ ] `US-ASIS-04`: justificar inasistencia con motivo obligatorio, certificado opcional y estado `JUSTIFICADA`; aplicar al porcentaje la regla acordada, sin penalizar al alumno.
- [ ] `US-ASIS-05`: cerrar asistencia por comisión, fijar regularidad final y denegar modificaciones posteriores salvo la excepción administrativa definida y auditada.

### 4. Evaluaciones, notas y actas

- [ ] `US-CAL-01`: docente asignado carga parciales de alumnos inscriptos; validar escala acordada y rechazar fuera de rango. Probar `TC-CAL-01..02`.
- [ ] `US-CAL-02`: cargar final solo para alumno regular y con correlativas aprobadas; con nota **>= 6** marcar `APROBADO`, con nota **< 6**, `DESAPROBADO`; impedir final de `NO_REGULAR`. Probar `TC-CAL-03..05`.
- [ ] `US-CAL-03`: permitir corrección de nota a docente autorizado con auditoría de valor anterior/nuevo, usuario y fecha; rechazar cambios no autorizados o en acta cerrada.
- [ ] `US-CAL-04`: permitir recuperatorio solo de parcial desaprobado; aplicar reemplazo o promedio según decisión previa y comprobar ambos resultados de recuperación.
- [ ] `US-CAL-05`: calcular automáticamente promedio y condición; acordar antes el efecto de recuperatorios y los estados `PROMOCIONADO`, `REGULAR`, `DESAPROBADO`.
- [ ] `US-CAL-06`: cerrar acta final solo si están todas las notas finales exigibles; bloquear edición posterior y permitir excepciones administrativas auditadas. Firma digital: **opcional**.

### 5. Consultas, reportes y entrega

- [ ] `US-REP-01`: reporte por materia con porcentaje y regularidad por alumno; sin registros, informar `Sin registros`. Probar `TC-REP-01..02`.
- [ ] `US-REP-02`: rendimiento por alumno con parciales, final, estado y promedio si aplica; sin notas, informar `Sin calificaciones registradas`. Probar `TC-REP-03..04`.
- [ ] Reporte adicional del anexo: alumnos en riesgo por asistencia <70 % o promedio <6, distinguiendo riesgo académico y riesgo de perder regularidad.
- [ ] Libro de actas con alumno, parciales, recuperatorios, final y condición; exportación PDF, Excel y CSV según el anexo. Confirmar formato y contenido de cada exportación antes de implementarla.
- [ ] Registrar quién cargó asistencia y quién modificó notas, cuándo y valores anteriores/nuevos; proteger los eventos de auditoría y verificar accesos de `DOC` asignado y `ADM` para excepciones.
- [ ] Escribir pruebas automatizadas por cada regla de negocio y por cada `TC-*` citado; incluir controles de autorización, persistencia, cierres, duplicados y límites 70 %/6. Validar flujos completos para administrativo, docente y alumno.
- [ ] Entregar en `document/` los diagramas **de arquitectura, clases, secuencia, estados académicos del alumno y modelo de datos**. Revisar que coincidan con el sistema final y actualizar el boceto si cambia el modelo.
- [ ] Completar README con descripción, integrantes, requisitos, configuración, arranque, pruebas y acceso de demostración; añadir Docker e instrucciones para ejecutar aplicación y base de datos desde cero; comprobarlo en un entorno limpio.
- [ ] Mantener Git/GitHub y ramas Git Flow; dejar el repositorio entregable y preparar la defensa de MVC, POO, persistencia, Git y reglas de negocio por integrante.

## Lectura de la imagen y límites del boceto

`backoffice-itec.jpeg` muestra `Career` → `StudyPlan` → `Topic` (materia), `Semester` y `Commission`; `Schedule`, `ModuleSchedule` y días de lunes a viernes; `Teacher`, `Student`, `StudentRegistered` y `Registration`; `Assistance`, `Exam` y `Qualification`. Incluye tipos `PRACTICAL ASSIGNMENT`, `MIDTERM`, `MAKEUP`, `FINAL` y estados `REGULAR`, `APPROVED`, `DISAPPROVED`. Es una **referencia conceptual**, no un esquema listo para implementar: faltan cardinalidades, identificadores, varias propiedades (marcadas `--`) y aparece `method(type): type` como marcador provisional. El anexo agrega `JUSTIFICADA`, `NO_REGULAR`, `PROMOCIONADO`, actas y auditoría que el dibujo no representa. El modelo definitivo debe resolver esas diferencias antes de crear el script SQL.

## Fuera de alcance obligatorio

El anexo señala como **futuro/opcional**: carga masiva de notas por Excel, QR de asistencia, firma digital de actas y notificaciones automáticas a alumnos. No son condiciones para considerar completo el alcance obligatorio; tampoco lo son los endpoints de ejemplo si no se elige API. No implementar estas extensiones antes de terminar y comprobar el flujo académico principal.
