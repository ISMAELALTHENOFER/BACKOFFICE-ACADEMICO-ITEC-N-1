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

## Decisión técnica confirmada

- El sistema se implementa en **Java** con **MySQL** en dos variantes que comparten análisis, reglas, arquitectura MVC y modelo de datos: primero una **aplicación de escritorio con JavaFX** y luego una **aplicación web con Spring Boot**.
- La documentación de análisis y diseño (`Documentacion_Backoffice_Academico_ITEC.docx`) es agnóstica a la tecnología de presentación y vale para ambas variantes.
- Mantener la arquitectura en capas **MVC**, como exige el enunciado; el diagrama de arquitectura debe mostrar cómo se separan la presentación (pantallas o páginas), las reglas de aplicación/negocio y el acceso a MySQL.
- La decisión elimina las alternativas Web, API como producto principal y base no relacional. Los endpoints del backlog siguen siendo opcionales y no forman parte del alcance salvo que se acuerde una API adicional.

## Cómo usar el proyecto guía

El repositorio de referencia `web-2026 (guia)` contiene un backoffice principalmente **web**, no una aplicación de escritorio JavaFX. Su backend más completo usa Maven/Java 17 y separa módulos `api`, `commons`, `core` y `security` (`proyecto base/backoffice-itec-master/pom.xml:17-27`). El README de ese backend describe React, PostgreSQL, JWT/Spring Security y MVC (`proyecto base/backoffice-itec-master/README.md:91-99`).

| Tomar como referencia | Adaptar al objetivo de este proyecto | No copiar sin validar |
| --- | --- | --- |
| Separación de responsabilidades y flujo servicio → repositorio → modelo; por ejemplo `AlumnoServiceImpl` usa `AlumnoRepository` (`proyecto base/backoffice-itec-master/backoffice-itec-core/src/main/java/ar/edu/itec1misiones/service/impl/AlumnoServiceImpl.java:9-29`). | Usar JavaFX para la interfaz y sus controladores; mantener reglas académicas en servicios y persistencia detrás de repositorios, conectados a MySQL. | No trasladar React, REST ni los controladores Spring: no corresponden al producto de escritorio elegido. |
| Vocabulario y entidades académicas existentes: `Alumno`, `Profesor`, `Materia`, `Asistencia`, `Nota` y `AlumnoInscripto`; asistencia se relaciona con inscripción y horario (`proyecto base/backoffice-itec-master/backoffice-itec-core/src/main/java/ar/edu/itec1misiones/model/Asistencia.java:7-26`). | Comparar esas entidades con las historias y el diagrama fuente; conservar solo las que representen reglas acordadas y completar relaciones/campos faltantes. | No considerar una clase/modelo o una lista del README como prueba de que el flujo funcional está implementado. |
| Perfiles de configuración y pruebas del proyecto guía como ejemplos para estudiar. | Definir configuración propia para MySQL y pruebas de comportamiento de cada regla y criterio `TC-*`. | El README menciona PostgreSQL, pero el perfil de desarrollo observado configura H2 (`proyecto base/backoffice-itec-master/backoffice-itec-api/src/main/resources/application-dev.yml:1-15`); las pruebas observadas son limitadas. No reutilizar esa configuración como verdad para este sistema. |

**Conclusión:** el proyecto guía sirve para orientar el vocabulario del dominio y la separación por capas, no para copiar su plataforma ni asumir que ya resuelve las reglas. La arquitectura objetivo es MVC + MySQL en ambas variantes (JavaFX y Spring Boot); el alcance se verifica contra los documentos del ITEC y pruebas propias.

## Inventario de documentación y entregables pendientes

Este inventario refleja el estado observado del repositorio al revisar los requisitos. Los archivos DOCX y el JPEG son **fuentes**; no cuentan como reemplazo de los entregables finales.

| Entregable | Estado actual | Mínimo para darlo por terminado |
| --- | --- | --- |
| `README.md` | Existe, pero solo tiene el título del repositorio. | Describir objetivo y alcance, integrantes, Java/MySQL y la tecnología de cada variante (JavaFX o Spring Boot), requisitos previos, configuración sin secretos, instalación/compilación, pruebas, ejecución de la app de escritorio y de MySQL con Docker; enlazar el script SQL y los diagramas finales. |
| Diagrama de arquitectura | Borrador en `diagramas/05-arquitectura.puml`. | Mostrar MVC y los componentes y conexiones con MySQL, válidos para la variante de escritorio y la web. |
| Diagrama de clases | Borrador de análisis y diseño en `diagramas/02`, `07` y `08`. | Representar clases, responsabilidades y relaciones implementadas, no solo entidades del boceto. |
| Diagrama de secuencia | DSS y DS de 6 operaciones en `diagramas/10` a `21`. | Mostrar al menos el flujo principal elegido, participantes y llamadas en orden; elegir el caso luego de definir la interfaz y los flujos. |
| Diagrama de estados académicos | Borrador en `diagramas/03-estados-academicos.puml`. | Mostrar estados, transiciones y condiciones de cambio del alumno/cursada según las reglas académicas acordadas. |
| Diagrama del modelo de datos | Borrador en `diagramas/04-modelo-de-datos.puml`. | Mostrar entidades/tablas, identificadores, relaciones y cardinalidades coherentes con la persistencia final. |
| Script SQL | No encontrado. | Crear el esquema reproducible de MySQL que exige el enunciado y verificarlo desde una base vacía. |
| Ejecución con Docker | No se encontraron `Dockerfile` ni archivo Compose. | Documentar y verificar MySQL en Docker y cómo se conecta cada variante. Acordar si el requisito de Docker exige contenerizar también la interfaz gráfica o si alcanza con la base en contenedor y la app ejecutada en el escritorio anfitrión. |
| Boceto `backoffice-itec.jpeg` | Existe; es conceptual e incompleto. | Conservarlo como fuente y actualizarlo o reemplazarlo por diagramas finales coherentes. No usarlo como modelo de datos definitivo. |
| Documento de análisis y diseño | `Documentacion_Backoffice_Academico_ITEC.docx`, generado con `generador/generar_documento.py` según la plantilla del TP integrador. | Mantenerlo sincronizado con el código: regenerar al cambiar reglas o diagramas. |
| DOCX de enunciado, backlog y anexo | Existen en `document/`; son fuentes del proyecto. | Mantenerlos como referencias originales; no hace falta duplicar su contenido en nuevos documentos. |

Los diagramas deben quedar en `document/`, como pide el enunciado. Los diagramas se escriben en PlantUML (`diagramas/*.puml`) con su imagen PNG; deben poder revisarse desde el repositorio y coincidir entre sí y con el sistema. La distinción entre roles, las reglas de negocio y el alcance de Docker ya están acordados (ver «Definiciones acordadas»). La documentación de API no está en el alcance confirmado; las rutas del backlog son ejemplos opcionales.

## Definiciones acordadas

Decisiones tomadas el 22/11/2026. Se detallan como reglas `RN-XX` en [`Documentacion_Backoffice_Academico_ITEC.docx`](Documentacion_Backoffice_Academico_ITEC.docx).

- [x] Roles: «Administrador» y «Administrativo» son el mismo rol `ADM`. Solo `ADM` crea usuarios y asigna roles. Roles del sistema: `ADM`, `DOC`, `ALU`.
- [x] Cursada: alumno + materia + comisión + ciclo lectivo. No se permite una inscripción vigente duplicada en la misma materia; se puede recursar en otro ciclo.
- [x] Calificaciones: escala 0 a 10 con un decimal; 2 parciales y 1 recuperatorio por parcial, que **reemplaza** la nota. Regular y promedio >= 8: `PROMOCIONADO`; regular y promedio >= 6: `REGULAR` (habilita final); si no, `DESAPROBADO`. Final >= 6: `APROBADO`.
- [x] Asistencia: el 70 % se calcula sobre las clases dictadas; una falta `JUSTIFICADA` cuenta como presente.
- [x] Cierres: actas y asistencias cerradas solo las reabre `ADM`, con motivo obligatorio y auditoría.
- [x] Ejecución: MySQL en Docker para ambas variantes. La variante JavaFX se compila como `.jar` ejecutable listo para usar y se conecta a MySQL en Docker. La variante Spring Boot se ejecuta completa con Docker (aplicación + MySQL con docker compose).
- [x] Integrantes: Ismael Althenofer. El alumno (`ALU`) solo consulta su asistencia, notas y condición.

## Plan de trabajo, en orden de dependencias

### 1. Base técnica y modelo académico

- [ ] Sustituir el ejemplo `Hello World!` por la variante de escritorio JavaFX (y luego la variante Spring Boot), con capas claras MVC de presentación, aplicación/negocio y persistencia; mantener Java y Maven y no atar reglas de negocio a la interfaz.
- [ ] Diseñar y crear el esquema MySQL persistente, relaciones, claves, restricciones y creación reproducible; entregar el **script SQL obligatorio** y proteger historial en bajas lógicas.
- [ ] Modelar alumnos, docentes, materias, correlativas, carreras, planes, semestres, comisiones, horarios, clases, inscripciones, asistencias, evaluaciones, calificaciones, actas y auditoría según las funciones acordadas. Validar cardinalidades y nombres antes de copiar la imagen al código.
- [ ] Habilitar configuración externa del entorno (conexión a MySQL y secretos), manejo de errores y ejecución local reproducible. No guardar contraseñas ni credenciales en el repositorio.

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
