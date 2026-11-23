# Guía de referencias para el desarrollo

Relevamiento de los proyectos de referencia del curso, para usar durante la implementación.
Material de trabajo interno: eliminar junto con `document/guia/` antes de la entrega final.

## 1. Fuentes revisadas

| Fuente | Ruta | Uso |
|---|---|---|
| Proyecto del profesor | `D:\DESARROLLOS\ITEC\web-2026` | Convenciones Spring, enunciado, requerimientos, teoría |
| Proyectos POO de escritorio | `D:\DESARROLLOS\ITEC\GENERAL\Guias\POO`, `D:\DESARROLLOS\ITEC\GENERAL\Gym-FitPower-POO` | Variante escritorio |
| Apps Spring Boot | `D:\DESARROLLOS\ITEC\GENERAL\SPRING`, `D:\DESARROLLOS\ITEC\GENERAL\SUPERMERCADO-(spring-boot)`, `D:\DESARROLLOS\ITEC\GENERAL\Guias\SPRING BOOT` | Variante web |
| Guías resueltas y plantilla | `document/guia/*.pdf`, `Plantilla tp integrador.docx` | Formato del documento de análisis (ya aplicado) |
| Spring Initializr del curso | `D:\DESARROLLOS\ITEC\FINAL CARRERA\sprinboot-Guia-descarga.jpg` | Configuración inicial del proyecto web |

## 2. Prioridad entre fuentes

1. `Requerimientos.docx` y `Anexo Requerimientos.docx` (contrato y reglas de negocio).
2. Enunciado (`backoffice_itec_enunciado.docx`).
3. Convenciones del código del profesor (`web-2026`).
4. Resto de los proyectos de referencia.

Cuando el código base del profesor contradice los requerimientos, se siguen los requerimientos.

## 3. Entregables exigidos por el enunciado

- Java, MVC en capas, base de datos relacional.
- Script SQL obligatorio.
- Git + GitHub con Git Flow.
- Documentación en `/document` con diagramas: arquitectura, clases, secuencia, estados académicos del alumno y modelo de datos.
- README con descripción e integrantes.
- Proyecto ejecutable con instrucciones Docker.
- Defensa oral: MVC, POO, persistencia, Git y reglas de negocio.

## 4. Variante escritorio

### Proyecto modelo: `Gym-FitPower-POO`

- Maven, Java 20, Swing con formularios de NetBeans (`.form`).
- JPA con EclipseLink 2.7 (`jakarta.persistence`) y `XxxJpaController` generados por NetBeans.
- MySQL 8 en Docker (`DOCKER/docker-compose.yml`).
- Paquetes: `model`, `dao` (JpaControllers + `Conexion` + `dao/exceptions`), `controller`, `view` (+ `view/resource` para modelos de tabla).
- Flujo: `Main` abre la conexión, muestra el login y luego la pantalla según el rol.
- Patrones a reutilizar: `FieldValidator` (validación de campos), `InterfacePanel` (contrato de los paneles CRUD).

Mapeo al proyecto: `itec.backoffice.{model, dao, controller, view}`.

### Piezas a tomar de otros proyectos

- `.jar` ejecutable: `maven-assembly-plugin` con `jar-with-dependencies`, como en `Guias\POO\Proyectos POO\certificacion2019-master\pom.xml`, o `maven-shade-plugin` con `ManifestResourceTransformer` y `mainClass itec.backoffice.controller.Main`.
- Separación interfaz / implementación de DAO: `certificacion2019-master` (`dao/XxxDao` + `dao/impl`).
- Modelos y listeners de tabla para paneles CRUD grandes: `municipalidaddesktop` (`TablaXxxModelo`, `TablaXxxModelListener`).

### Errores de las referencias que no hay que copiar

- Contraseñas de usuario en texto plano: guardar hash (BCrypt).
- Credenciales de la base fijas en `persistence.xml`: pasarlas por variables de entorno a `Persistence.createEntityManagerFactory(nombre, props)`.
- Roles decididos comparando el texto de la descripción: usar enum o id.
- Ningún proyecto genera un `.jar` ejecutable con su `pom.xml` actual.
- Scripts SQL de semilla con errores de sintaxis: el esquema y la semilla van en `docker-entrypoint-initdb.d`.
- Sin tests: agregar tests de la lógica de negocio.

### Decisión pendiente

Swing (lo usan todas las guías del curso) o JavaFX (no hay ningún ejemplo en el curso).

## 5. Variante web (Spring Boot)

### Configuración inicial (Spring Initializr del curso)

- Maven, Java 17, Spring Boot 3.1.0, empaquetado Jar.
- Dependencias: Lombok, DevTools, Spring Web, Spring Data JPA, Spring Data JDBC, H2, MySQL Driver.
- Ajustes:
  - Group / paquete raíz: `itec.backoffice` (no `com.itec1`).
  - Spring Data JDBC es redundante con JPA; mantener solo si se exige.
  - Agregar `spring-boot-starter-validation`, `spring-boot-starter-security` y jjwt para la autenticación.

### Estructura de código (profesor + `GENERAL\SPRING`)

- Paquetes: `config`, `constants`, `controller`, `dto/<entidad>/` (`XxxRequestDto`, `XxxResponseDto`), `exception`, `model`, `repository`, `service` (interfaces) + `service/impl` (`XxxServiceImpl`), `security/{config, filter, service, util, dto}`.
- Inyección por constructor.
- Rutas definidas en constantes (`APIConstant`).
- Respuesta uniforme `ResponseEntity<ApiResponse<T>>`: `{meta{method, operation}, data: List<T>, errors: List<ErrorDto{code, description}>}` con `@JsonInclude(NON_NULL)`.
- Mapeo entidad ↔ DTO a mano en el servicio (Lombok `@Builder`), sin MapStruct.
- `@Transactional(readOnly = true)` en lecturas.
- Configuración YAML por perfiles: `dev` (H2), `prod` (MySQL con credenciales desde variables de entorno).

### Persistencia

- Entidades: `@Entity @Data @NoArgsConstructor @AllArgsConstructor @Builder`.
- Ids `Long` con `GenerationType.IDENTITY`.
- Enums con `@Enumerated(EnumType.STRING)`.
- Relaciones de referencia: `web-2026` core (`Alumno.java`, `Materia.java` correlativas con `@ManyToMany @JoinTable`, `HorarioClase.java`) y `Proyecto Final/finalprojectweb` (`ShippingOrder.java`).
- `@OneToOne @JoinColumn(name = "user_id")` entre Alumno/Profesor y `User`.
- Unicidad con `@Table(uniqueConstraints = ...)`.
- Repositorios `JpaRepository<X, Long>` con consultas derivadas; la teoría recomienda `@Query` con HQL.
- Relaciones del dominio del profesor: `web-2026\proyecto base\backoffice-itec-master\document\relaciones.md`.

### Seguridad (profesor)

- JWT sin estado (HS256), filtro `OncePerRequestFilter`, `BCryptPasswordEncoder`, `@EnableMethodSecurity`.
- Enum `Rol {ADMIN, ADMINISTRATIVO, PROFESOR, ALUMNO}` como `ROLE_<nombre>`; `User implements UserDetails`; roles en `@ElementCollection` (`user_roles`).
- Registro protegido: solo ADMIN crea ADMIN/ADMINISTRATIVO; ADMIN o ADMINISTRATIVO crean PROFESOR/ALUMNO.
- Usuario administrador inicial creado al arrancar (`AdminInitializer`) desde propiedades.

### Manejo de errores

`@ControllerAdvice` que devuelve `ApiResponse.errors`:

| Excepción | Código |
|---|---|
| BadCredentials | 401 |
| MethodArgumentNotValid | 400, un error por campo |
| ConstraintViolation | 400 |
| AccessDenied | 403 |
| No encontrado (agregar `NotFoundException`) | 404 |
| Dato existente | 409 |
| Cualquier otra | 500 |

### Diferencias del código del profesor que hay que corregir

| Código del profesor | Lo que exigen los requerimientos |
|---|---|
| Rutas `/auth/...` | Rutas `/api/v1/...` |
| Siempre 200 | 201 al crear, 204 al borrar |
| Sin 404 | 404 cuando no existe |
| Sin baja lógica | Estado INACTIVO |
| Sin auditoría | Entidad `AuditLog` (acción, usuario, entidad, valor anterior, valor nuevo, fecha) y fecha de última modificación |
| Sin control de usuario INACTIVO | Login rechazado (TC-AUTH-06) |
| Sin control de profesor asignado | Asistencia solo por el profesor asignado (403) |
| Carpetas `service` / `impl` invertidas en el módulo security | Interfaces en `service`, implementaciones en `service/impl` |

### Docker

Ninguna referencia tiene un `docker-compose` de app + MySQL funcional. Escribir uno nuevo con:

- Servicio `mysql` (`mysql:8.0`), volumen nombrado montado, healthcheck, scripts en `docker-entrypoint-initdb.d`.
- Servicio `app` con `depends_on` (condición healthy) y `SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/<base>`.
- `Dockerfile` cuyo nombre de `.jar` coincida con el `artifactId`.
- Credenciales por variables de entorno (archivo `.env` fuera del repositorio).

## 6. Contrato de la API (requerimientos)

- `POST /api/v1/auth/login` (200 / 401 / 403).
- Alumnos: `POST` (201 / 400 / 409), `GET|PUT|DELETE /{dni}` (DELETE = baja lógica, 204).
- Profesores: `POST`, `PUT|DELETE /{id}`, `POST /materias/{idMateria}/profesores/{idProfesor}`.
- Materias: CRUD + `POST /{id}/correlativas/{idCorrelativa}` (sin autorreferencia ni ciclos).
- `POST /api/v1/inscripciones`: alumno y materia ACTIVOS, sin duplicados, correlativas aprobadas.
- `POST /api/v1/asistencias`: solo el profesor asignado (si no, 403).
- `GET /api/v1/asistencias/alumnos/{id}`; estados PRESENTE / AUSENTE / JUSTIFICADA; cierre de asistencia.
- `PUT /api/v1/calificaciones/{id}` con auditoría; recuperatorio; promedio → PROMOCIONADO / REGULAR / DESAPROBADO.
- `POST /api/v1/actas/cerrar`.
- Reportes por materia, por alumno y de alumnos en riesgo; exportación PDF / Excel / CSV.

## 7. Testing (teoría del curso)

- JUnit 5 + Mockito: `@ExtendWith(MockitoExtension.class)`, `@Mock` del repositorio, `@InjectMocks` del servicio.
- Principios F.I.R.S.T. y estructura Given / When / Then.
- Nombres de test descriptivos; casos borde (nulo, vacío, inválido).
- Carpetas `src/test/.../unit` y `src/test/.../integration`.
- Repositorios sin mocks; servicios con repositorios mockeados; controladores con servicio mockeado.
- Ninguna referencia tiene tests reales para copiar.

## 8. Errores conocidos en las referencias

- `examplejpa`: no compila (`PersonController.java:22`, import inexistente en `IFlightService.java:3`).
- `SUPERMERCADO`: `ProductRepository` usa `Integer` como id con entidad `Long`; versión SNAPSHOT.
- `GENERAL\SPRING`: Dockerfile con nombre de `.jar` incorrecto; volumen de MySQL no montado; sin handler de validación.
- `project-course`: `StudentServiceImpl.java:40` asigna el nombre en el apellido; `spring-boot-starter-validation` en versión 4.0.6 con Boot 3.5.5.
- springfox y jjwt antiguos no funcionan con Boot 3.
- Varias configuraciones tienen contraseñas en texto plano: no copiarlas.
