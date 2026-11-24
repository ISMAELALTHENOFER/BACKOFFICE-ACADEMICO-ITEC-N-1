"""Genera document/Documentacion_Backoffice_Academico_ITEC.docx.

Uso (desde la raíz del repositorio):
    python document/generador/generar_documento.py

Requisitos: python-docx y los PNG ya renderizados en document/diagramas
(java -jar plantuml.jar -charset UTF-8 -tpng document/diagramas/*.puml).
"""
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT  # noqa: F401  (disponible para secciones apaisadas)
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from contenido import (
    AUTOR, CASOS_DE_USO, CONTRATOS, ESCENARIO, INTRODUCCION, PAQUETES,
    PERSONAL, REGLAS, REQUISITOS, REQUISITOS_NO_FUNCIONALES, TITULO,
    TRAZABILIDAD, USUARIOS, FECHA, CAPAS, ENTORNO, NOTAS_MODELO_DATOS, EXTENSIONES_MODELO,
    DSS, OBJETIVOS, FRACASOS, HISTORIAS,
)

RAIZ = Path(__file__).resolve().parents[1]
DIAGRAMAS = RAIZ / "diagramas"
SALIDA = RAIZ / "Documentacion_Backoffice_Academico_ITEC.docx"
ANCHO_UTIL = Cm(16.5)


# ---------- utilidades de formato ----------

def sombrear(celda, color="D9E2F3"):
    tc_pr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tc_pr.append(shd)


def texto_celda(celda, texto, negrita=False):
    celda.text = ""
    lineas = texto if isinstance(texto, list) else [texto]
    for i, linea in enumerate(lineas):
        par = celda.paragraphs[0] if i == 0 else celda.add_paragraph()
        run = par.add_run(linea)
        run.bold = negrita
        run.font.size = Pt(9.5)


def tabla(doc, encabezados, filas, anchos=None):
    t = doc.add_table(rows=1, cols=len(encabezados))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for celda, enc in zip(t.rows[0].cells, encabezados):
        texto_celda(celda, enc, negrita=True)
        sombrear(celda)
    for fila in filas:
        celdas = t.add_row().cells
        for celda, valor in zip(celdas, fila):
            texto_celda(celda, valor)
    if anchos:
        for fila in t.rows:
            for celda, ancho in zip(fila.cells, anchos):
                celda.width = Cm(ancho)
    doc.add_paragraph()
    return t


def tabla_clave_valor(doc, pares):
    t = doc.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    for clave, valor in pares:
        c1, c2 = t.add_row().cells
        texto_celda(c1, clave, negrita=True)
        sombrear(c1)
        texto_celda(c2, valor)
        c1.width, c2.width = Cm(4.5), Cm(12)
    doc.add_paragraph()


def imagen(doc, nombre, epigrafe, ancho=ANCHO_UTIL):
    ruta = DIAGRAMAS / nombre
    if not ruta.exists():
        raise FileNotFoundError(f"Falta {ruta}; renderizar primero los .puml")
    doc.add_picture(str(ruta), width=ancho)
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph(epigrafe)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9)


def ancho_para(nombre, maximo=ANCHO_UTIL):
    """Evita ampliar diagramas chicos: limita el ancho al tamaño nativo a 110 ppp."""
    import struct
    with open(DIAGRAMAS / nombre, "rb") as f:
        ancho_px = struct.unpack(">I", f.read(24)[16:20])[0]
    return min(maximo, Cm(ancho_px / 110 * 2.54))


def parrafos(doc, textos):
    for texto in textos:
        doc.add_paragraph(texto)


def vinetas(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def indice(doc):
    par = doc.add_paragraph()
    run = par.add_run()
    for tipo, texto in (("begin", None), (None, 'TOC \\o "1-3" \\h \\z \\u'), ("separate", None)):
        if tipo:
            fld = OxmlElement("w:fldChar")
            fld.set(qn("w:fldCharType"), tipo)
            run._r.append(fld)
        else:
            instr = OxmlElement("w:instrText")
            instr.set(qn("xml:space"), "preserve")
            instr.text = texto
            run._r.append(instr)
    par.add_run("Hacer clic derecho y elegir «Actualizar campos» para generar el índice.").italic = True
    fin = OxmlElement("w:fldChar")
    fin.set(qn("w:fldCharType"), "end")
    par.add_run()._r.append(fin)
    # Pide a Word actualizar los campos al abrir el documento.
    ajustes = doc.settings.element
    upd = OxmlElement("w:updateFields")
    upd.set(qn("w:val"), "true")
    ajustes.append(upd)


def salto(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# ---------- secciones ----------

def caratula(doc):
    for _ in range(6):
        doc.add_paragraph()
    for texto, tam, neg in (
        ("Instituto Tecnológico N°1 (ITEC N°1)", 16, False),
        ("Proyecto Final", 14, False),
        ("", 12, False),
        (TITULO, 26, True),
        ("Documentación de análisis y diseño", 16, False),
        ("", 12, False),
        ("", 12, False),
        (f"Alumno: {AUTOR}", 13, False),
        (FECHA, 12, False),
    ):
        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = par.add_run(texto)
        run.font.size = Pt(tam)
        run.bold = neg
        if neg:
            run.font.color.rgb = RGBColor(0x1F, 0x3A, 0x68)
    salto(doc)


def caso_de_uso(doc, uc):
    doc.add_heading(f"Caso de uso: {uc['nombre']} ({uc['id']})", level=2)
    t = doc.add_table(rows=0, cols=4)
    t.style = "Table Grid"

    def fila4(a, b, c, d):
        celdas = t.add_row().cells
        for i, (txt, neg) in enumerate(((a, True), (b, False), (c, True), (d, False))):
            texto_celda(celdas[i], txt, negrita=neg)
            if neg:
                sombrear(celdas[i])

    def fila_unida(etiqueta, contenido):
        celdas = t.add_row().cells
        texto_celda(celdas[0], etiqueta, negrita=True)
        sombrear(celdas[0])
        unida = celdas[1].merge(celdas[2]).merge(celdas[3])
        texto_celda(unida, contenido)

    def fila_actor_sistema(actor, sistema, negrita=False):
        celdas = t.add_row().cells
        izquierda = celdas[0].merge(celdas[1])
        derecha = celdas[2].merge(celdas[3])
        texto_celda(izquierda, actor, negrita=negrita)
        texto_celda(derecha, sistema, negrita=negrita)
        if negrita:
            sombrear(izquierda)
            sombrear(derecha)

    fila4("Nivel de caso de uso:", uc["nivel"], "Paquete:", uc["paquete"])
    fila_unida("Nombre del caso de uso:", f"{uc['nombre']} ({uc['id']})")
    fila4("Prioridad:", uc["prioridad"], "Categoría:", uc["categoria"])
    fila4("Complejidad:", uc["complejidad"], "Significativo para la arquitectura:", uc["arquitectura"])
    fila4("Actor principal:", uc["actor"], "Actor secundario:", uc.get("secundario", "—"))
    fila4("Tipo de caso de uso:", uc["tipo"], "Trazabilidad:", uc["traza"])
    fila_unida("Objetivos:", OBJETIVOS[uc["id"]])
    fila_unida("Precondiciones:", uc["pre"])
    fila_unida("Postcondiciones:", [f"Éxito (flujo normal): {uc['post']}"] + FRACASOS[uc["id"]])
    fila_flujo = t.add_row()
    encabezado = fila_flujo.cells[0].merge(fila_flujo.cells[3])
    texto_celda(encabezado, "Flujo normal", negrita=True)
    sombrear(encabezado)
    fila_actor_sistema("Actor", "Sistema", negrita=True)
    for i, paso in enumerate(uc["flujo"], 1):
        # El paso pertenece al sistema cuando su sujeto es «El sistema».
        if paso.startswith("El sistema") or paso.startswith("Si "):
            fila_actor_sistema("", f"{i}. {paso}")
        else:
            fila_actor_sistema(f"{i}. {paso}", "")
    fila_unida("Cursos alternativos:", uc["alternativos"] or ["No aplica."])
    for fila in t.rows:
        for celda, ancho in zip(fila.cells, (3.5, 4.75, 3.5, 4.75)):
            celda.width = Cm(ancho)
    doc.add_paragraph()

    if uc["id"] in DSS:
        doc.add_heading(f"DSS: {uc['nombre']} ({uc['id']})", level=3)
        imagen(doc, DSS[uc["id"]], f"Diagrama de secuencia del sistema - {uc['nombre']}",
               ancho_para(DSS[uc["id"]]))
    for c in [c for c in CONTRATOS if c["uc"] == uc["id"]]:
        doc.add_heading(f"CCO: {c['titulo']}", level=3)
        tabla_clave_valor(doc, [
            ("Operación", c["operacion"]),
            ("Responsabilidades", c["responsabilidades"]),
            ("Caso de uso", f"{uc['nombre']} ({uc['id']})"),
            ("Controlador", c["controlador"]),
            ("Precondiciones", c["pre"]),
            ("Postcondiciones", c["post"]),
        ])
        doc.add_heading(f"DS: {c['titulo']}", level=3)
        imagen(doc, c["ds"], f"Diagrama de secuencia - {c['titulo']}", ancho_para(c["ds"]))


def generar():
    doc = Document()
    estilo = doc.styles["Normal"]
    estilo.font.name = "Calibri"
    estilo.font.size = Pt(11)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.25)
        s.top_margin = s.bottom_margin = Cm(2)
        pie = s.footer.paragraphs[0]
        pie.text = f"{AUTOR} - {TITULO}"
        pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pie.runs[0].font.size = Pt(8)

    props = doc.core_properties
    props.author = AUTOR
    props.last_modified_by = AUTOR
    props.title = TITULO
    props.subject = "Documentación de análisis y diseño"
    props.comments = ""
    props.keywords = "ITEC, backoffice académico, Java, MVC, MySQL"

    caratula(doc)
    doc.add_heading("Índice", level=1)
    indice(doc)
    salto(doc)

    doc.add_heading("1. Introducción", level=1)
    parrafos(doc, INTRODUCCION)

    doc.add_heading("2. Escenario", level=1)
    parrafos(doc, ESCENARIO["parrafos"])
    vinetas(doc, ESCENARIO["alcance"])
    parrafos(doc, ESCENARIO["cierre"])

    doc.add_heading("3. Descripción del personal involucrado", level=1)
    doc.add_heading("3.1 Resumen del personal involucrado en el desarrollo", level=2)
    tabla(doc, ["Nombre", "Rol", "Responsabilidades"], PERSONAL, [4, 4, 8.5])
    doc.add_heading("3.2 Resumen de usuarios", level=2)
    tabla(doc, ["Rol", "Código", "Descripción y permisos"], USUARIOS, [3.5, 2, 11])

    doc.add_heading("4. Reglas del negocio (RN-XX)", level=1)
    tabla(doc, ["ID", "Descripción", "Grado de variación", "Fuente"], REGLAS, [1.6, 10, 2.2, 2.7])

    doc.add_heading("5. Requisitos funcionales (RF-XX)", level=1)
    for grupo, filas in REQUISITOS:
        doc.add_heading(f"Función de grupo: {grupo}", level=3)
        tabla(doc, ["Número", "Requerimiento", "Origen"], filas, [1.8, 11.7, 3])
    doc.add_heading("5.1 Requisitos no funcionales (RNF-XX)", level=2)
    tabla(doc, ["Número", "Requerimiento"], REQUISITOS_NO_FUNCIONALES, [2, 14.5])

    doc.add_heading("6. Historias de usuario", level=1)
    parrafos(doc, ["Las historias de usuario provienen del backlog del proyecto (Requerimientos y su "
                   "Anexo). Cada una indica el rol, la necesidad y el beneficio, sus criterios de "
                   "aceptación y los casos de prueba que la verifican. Los casos de prueba marcados "
                   "como «propuesto» completan las historias que en el backlog no tenían casos de "
                   "prueba definidos."])
    tabla(doc, ["ID", "Historia de usuario", "Caso de uso"],
          [[h["id"], h["titulo"], h["uc"]] for h in HISTORIAS], [3, 9.5, 4])
    for h in HISTORIAS:
        doc.add_heading(f"{h['id']}: {h['titulo']}", level=3)
        tabla_clave_valor(doc, [
            ("Descripción", f"Como {h['como']}, quiero {h['quiero']}, para {h['para']}."),
            ("Criterios de aceptación", h["criterios"]),
            ("Casos de prueba", h["pruebas"]),
        ])

    doc.add_heading("7. Diagrama de casos de uso", level=1)
    imagen(doc, "casos-de-uso.png", "Diagrama de casos de uso del sistema", Cm(13))
    tabla(doc, ["ID", "Caso de uso", "Actor", "Requisitos"],
          [[u["id"], u["nombre"], u["actor"], u["rf"]] for u in CASOS_DE_USO], [1.8, 6.5, 4, 4.2])

    doc.add_heading("8. Diagrama de clases de análisis", level=1)
    parrafos(doc, ["Representa los conceptos del dominio académico y sus asociaciones, "
                   "sin decisiones de implementación."])
    imagen(doc, "clases-analisis.png", "Diagrama de clases de análisis", ancho_para("clases-analisis.png"))
    parrafos(doc, ["Además de los conceptos del dominio académico base (usuarios, alumnos, profesores, "
                   "carreras, planes, materias, cuatrimestres, comisiones, horarios, exámenes, notas e "
                   "inscripciones), el modelo incorpora los siguientes elementos para cubrir los "
                   "requerimientos funcionales:"])
    vinetas(doc, EXTENSIONES_MODELO)

    doc.add_heading("9. Casos de uso", level=1)
    parrafos(doc, ["Se especifica cada caso de uso. Para las operaciones más significativas se "
                   "incluyen el diagrama de secuencia del sistema (DSS), el contrato de la operación "
                   "(CCO) y el diagrama de secuencia de diseño (DS)."])
    for uc in CASOS_DE_USO:
        caso_de_uso(doc, uc)

    doc.add_heading("10. Diagrama de estados (estado académico del alumno)", level=1)
    parrafos(doc, ["El estado académico pertenece a cada cursada del alumno (AlumnoInscripto). "
                   "Mientras la cursada está EN_CURSO, la condición de asistencia (REGULAR o NO_REGULAR) "
                   "se recalcula automáticamente con cada registro de asistencia; al cerrar la asistencia "
                   "se congela y se fija el estado de la cursada."])
    imagen(doc, "estados-academicos.png", "Diagrama de estados del alumno en una cursada")

    doc.add_heading("11. Diagrama de clases de diseño", level=1)
    imagen(doc, "clases-diseno.png", "Clases de diseño: controladores y servicios",
           ancho_para("clases-diseno.png", Cm(15)))
    imagen(doc, "clases-diseno-servicios.png",
           "Clases de diseño: implementación de servicios, seguridad, reglas, reportes y persistencia",
           ancho_para("clases-diseno-servicios.png", Cm(13)))
    imagen(doc, "clases-diseno-dominio.png", "Clases de diseño: modelo de dominio",
           ancho_para("clases-diseno-dominio.png"))

    doc.add_heading("12. Modelo de datos", level=1)
    imagen(doc, "modelo-de-datos.png", "Modelo de datos relacional (MySQL)")
    vinetas(doc, NOTAS_MODELO_DATOS)

    doc.add_heading("13. Paquetes del modelo del dominio", level=1)
    imagen(doc, "paquetes.png", "Paquetes del sistema y sus dependencias", ancho_para("paquetes.png"))
    tabla(doc, ["Paquete", "Responsabilidad"], PAQUETES, [5, 11.5])

    doc.add_heading("14. Patrón de arquitectura de capas (Layers)", level=1)
    parrafos(doc, CAPAS["parrafos"])
    tabla(doc, ["Capa", "Componente MVC", "Contenido"], CAPAS["tabla"], [4, 3.5, 9])
    imagen(doc, "arquitectura.png", "Diagrama de arquitectura", ancho_para("arquitectura.png"))

    doc.add_heading("15. Trazabilidad de requisitos y casos de prueba", level=1)
    tabla(doc, ["Historia", "Requisitos", "Caso de uso", "Casos de prueba"], TRAZABILIDAD, [3, 3.5, 3, 7])

    doc.add_heading("16. Entorno de ejecución", level=1)
    parrafos(doc, ENTORNO["parrafos"])
    tabla(doc, ["Componente", "Detalle"], ENTORNO["tabla"], [4.5, 12])

    doc.save(SALIDA)
    print(f"Documento generado: {SALIDA}")


if __name__ == "__main__":
    generar()
