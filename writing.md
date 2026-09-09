# Cómo escribimos — AGCS | Studio + Lab

Estándar de redacción y de formato de informe. Gobierna todo lo que sale con la
marca: correos de programa, decks, informes, tableros, minutas y documentos de
método. Las reglas visuales viven en `SKILL.md` y en `colors_and_type.css`; este
documento gobierna el texto que va dentro de esas maquetas.

Versión 1.0 · 8 de septiembre de 2026. Levantado leyendo correspondencia real
enviada entre enero y septiembre de 2026 (Banco G&T, OXXO, KOF, Gran Ciudad,
POLI.design), los chats de Teams del equipo y los informes entregados, no una
idea de cómo deberíamos escribir.

---

## 1 · Piso y techo

Todas las reglas de este documento son **piso**. Una regla que se cumple sin
hacer nada está mal escrita, y ya nos pasó con el grid de v5: «todas las slides
menos cinco» terminó significando todas las slides. Cada regla de aquí nombra
algo que hay que hacer, y su incumplimiento es un defecto verificable.

Sobre el piso hay libertad. Un correo de tres líneas cumple el piso. Un informe
de doscientas páginas cumple el mismo piso.

---

## 2 · Voz — aplica a todo, sin excepción

### 2.1 Prohibiciones duras

Estas se han pedido muchas veces y se han incumplido muchas veces. Al terminar
cualquier texto, se buscan y se reescriben antes de entregar.

**Construcción antitética.** Queda fuera «esto no es X, es Y» y todas sus
variantes: «no se trata de X sino de Y», «más que X, es Y», «X no; Y». Es el
delator más frecuente de la prosa de máquina. Cada asunto se describe de frente.
Vigilar también «desde X hasta Y» usado para dar cobertura, y «ya sea X o Y».

**Explicar apoyándose en otra cosa.** Ningún concepto se define por contraste
con otro. Quedan fuera los pares paralelos («el journey dice qué le duele; el
blueprint dice dónde se rompe»), las fórmulas «A hace X; B hace Y», «mientras
A…, B…», «en lugar de», «vale más que». Cada concepto se describe por sí mismo:
qué es, para qué sirve, qué contiene.

**Siglas que el cliente no ha usado primero.** Nombres completos siempre: Team
Alignment Map, Contact Center, Cross Functional Team. Las siglas ya adoptadas
están bien: JTBD, DVFR, PRD, AS-IS, TO-BE, VPC. Una sigla nueva se define la
primera vez y solo se repite si el cliente la adopta.

**Emojis y símbolos decorativos.** En ningún campo y en ningún lugar. Tampoco
`✓`, `↳`, `⭐`. El chevron `>>` escrito en mono es el único glifo que se repite.

**Expresiones vetadas.** «La pregunta de la casa». Antes de inventar una
etiqueta de sección, revisar si el método ya tiene un nombre para eso.

### 2.2 Registro

Formal, y más aún en material de cliente. Sin lenguaje de taller, sin
coloquialismos. Español de Chile en la conversación interna, español neutro en
material de cliente.

### 2.3 Idioma por elemento

| Elemento | Idioma | Forma |
|---|---|---|
| Título de deck, de slide, de correo | Inglés | Sintagma nominal, de dos a cinco palabras, Title Case, sin punto final |
| Subtítulo | Inglés | Una línea, máximo diez palabras, y dice la conclusión |
| Cuerpo | Español | — |
| Etiquetas mono | Español o inglés, consistente dentro del entregable | Mayúsculas |

### 2.4 Nombres propios

**Los nombres de programa van completos y exactos.** El programa del banco es
**Customer Journey Labs**. Nunca «Customer Labs».

Esto no se cumple hoy. El correo del 27 de agosto de 2026 a Haroldo, Luis e
Iveth salió con el asunto «Customer Labs · Sesión 1», y la reunión de Teams con
el cliente se llama «Customer Labs - Diseñando juntos el futuro del servicio».
El correo del 1 de septiembre, al mismo grupo, dice «Customer Journey Labs».
El cliente recibió dos nombres para un programa en cinco días.

Antes de escribir el asunto de un correo o el título de una slide, verificar el
nombre contra el contrato o la propuesta.

### 2.5 Cifras

**Ninguna cifra sin fuente visible en el mismo lugar donde aparece.** En slide,
línea `SOURCE · <publicación>, <año>` abajo a la izquierda, y slide de `Sources`
al cierre si hubo datos externos. En informe, enlace en la fila.

Tres marcas obligatorias cuando corresponda, porque el lector no puede
distinguirlas por su cuenta:

- **dato del encargo** — cifra que dio el cliente y que nadie contrastó.
- **cifra de proveedor** — resultado publicado por quien vende la práctica.
- **CONTRADICCIÓN** — dos fuentes dan valores distintos y no se elige.

---

## 3 · Dos firmas bajo una marca

Hoy salen dos formas de escribir hacia los mismos clientes, con el mismo
logotipo al pie.

**Alex.** Vocativo, una o dos líneas, despedida. El correo a Oscar Arrascue del
9 de agosto: «Estimado Oscar / Te adjunto el brief de esta semana del Proyecto
de Strategic Bet Labs / Encontrarás 2 cambios metodológicos que realizamos» y
dos puntos numerados. Firma `Alex · AGCS · Strategic Design · | Studio + Lab |`,
a veces sin la línea `Strategic Design`.

**Max.** Correo maquetado con el design system. Cabecera mono con programa y
cliente, stamp de semana, título en inglés, subtítulo en cursiva, secciones
numeradas con etiqueta mono, un solo elemento lime, fecha límite explícita,
adjuntos en PNG. Firma `Max Gallardo · AGCS | Studio + Lab | · >> Stay Forward`.

**La decisión (8 de septiembre de 2026): se conservan las dos.** Max mantiene su
formato y su skill `agcs-correo`. Alex mantiene su extensión.

**Lo que sí es piso para los dos**, porque es lo que el cliente puede ver
inconsistente entre un correo y el siguiente:

1. **Bloque de firma idéntico.** `Nombre · AGCS | Studio + Lab |` y, cerrando,
   `>> Stay Forward`. Una sola versión, sin variantes por correo.
2. **Nombre de programa exacto** (sección 2.4).
3. **Título en inglés, cuerpo en español** (sección 2.3).
4. **Un solo elemento lime** en todo el correo, con el mismo significado que
   tiene en el deck de ese programa.
5. **Adjuntos en PNG**, una imagen por página o slide, generados con
   `tools/build-export.py`. Las tipografías reales viajan en el PNG.
6. **Ninguna prohibición de la sección 2.1**, en ningún correo, de nadie.
7. **Enlaces sobre el texto**, nunca la dirección visible. El artículo se enlaza
   desde su título.

Todo lo demás queda a criterio de quien firma.

---

## 4 · Correo

Estructura fija del correo de programa. La skill `agcs-correo` la produce.

- Cabecera con hairline Mist: `>> NOMBRE DEL PROGRAMA` a la izquierda,
  `>> CLIENTE` a la derecha, en mono mayúsculas.
- Stamp de semana o versión, título en inglés, subtítulo en cursiva con la
  conclusión, cuerpo en español.
- Secciones separadas por hairline Mist, cada una con etiqueta mono en
  mayúsculas (`01 · …`, `QUÉ TRAER EL JUEVES`, `LECTURA OPCIONAL`).
- Un solo elemento lime, y carga el significado del programa: la fecha límite,
  o lo que se decide.
- Pie: nombre, `AGCS | STUDIO + LAB |`, `>> Stay Forward`, en mono.
- Esquinas a 0, sin sombras, sin gradientes.

**Tipografías.** N27 e IBM Plex Mono no se pueden usar en correo. Gmail elimina
`@font-face` y Outlook de Windows no lo soporta. Se declara la pila con fallback
(`'IBM Plex Mono',Menlo,Consolas,monospace` y Helvetica) y la tipografía real
viaja en los PNG adjuntos.

**Cierre.** Todo correo que pide algo cierra nombrando qué se pide, a quién y
para cuándo. Un correo de programa sin fecha en el cuerpo está incompleto.

---

## 5 · Informe

El formato queda fijado por el informe consolidado de research TO-BE entregado a
Banco G&T el 7 de septiembre de 2026. Un informe AGCS lleva estas piezas, en
este orden.

### 5.1 Encabezado

```
# <Título del informe>
## <Programa · Cliente · Alcance · Arquetipo>
AGCS · Studio + Lab · Versión <n.n> · <fecha> · Fecha de consulta de todas las fuentes: <fecha>
```

La fecha de consulta va aparte de la fecha del documento. Un informe con
enlaces y sin fecha de consulta no se puede auditar después.

### 5.2 Las tres notas de apertura

Antes de cualquier hallazgo, tres párrafos en negrita que le dicen al lector
cómo tratar lo que sigue.

**Qué es este documento.** Cómo se produjo. Si hubo varias corridas, cuántas y
cómo se fundieron. Qué se conserva y qué se descarta.

**Advertencias que gobiernan la lectura.** Lo que el lector necesita saber para
no creerle de más al documento: qué insumos no llegaron, qué cifras no se
contrastaron, qué quedó sin verificar. Van al principio, con el peso de una
advertencia, no escondidas en una nota al pie.

**Cómo usarlo.** Qué sección alimenta qué entregable. El lector tiene que poder
ir directo a lo que necesita.

### 5.3 Resumen ejecutivo

Hallazgos, cada uno abriendo con raya (`—`) y con la afirmación en negrita.
Cada hallazgo lleva su **fuente principal enlazada** y la **remisión a la
sección** donde está el detalle. Se declara cuántos son.

Cierra con el bloque de **decisiones que el cliente debe confirmar**, numeradas,
cada una con su fecha límite.

### 5.4 Nota de método

Cuando el informe funde varias corridas o varias fuentes de levantamiento, tabla
con una fila por corrida: extensión, estructura, herramienta u origen, insumos
recibidos, fuentes listadas y **las limitaciones que la propia corrida declara**.
Después, un párrafo `Cómo se consolidó` con la unidad de deduplicación y el
tratamiento de las contradicciones.

### 5.5 Cuerpo

Secciones numeradas. Cada fila de tabla lleva su URL y su identificador de
trazabilidad al origen.

### 5.6 Las cuatro reglas de honestidad

Son lo que distingue un informe AGCS de un resumen.

1. **Las contradicciones se conservan marcadas, sin elegir.** Dos fuentes que
   dan valores distintos aparecen las dos, con la marca `CONTRADICCIÓN`.
2. **El origen de cada cifra se marca** (sección 2.5).
3. **Hay una sección de lo que no se encontró.** Explícita, enumerada, con lo
   que el trabajo siguiente tendría que producir por sí mismo. Un informe sin
   esta sección está afirmando que encontró todo.
4. **Las fuentes van numeradas al final**, deduplicadas por URL normalizada, con
   el conteo antes y después de deduplicar.

---

## 6 · Antes de entregar

Recorrer esta lista sobre el texto terminado. Cada punto se verifica leyendo, no
recordando.

- [ ] Buscar «no es», «sino», «más que», «en lugar de», «mientras», «ya sea» y
      reescribir toda construcción antitética o comparativa que aparezca.
- [ ] Verificar el nombre del programa contra el contrato.
- [ ] Verificar que toda sigla fue usada primero por el cliente.
- [ ] Verificar que toda cifra tiene fuente visible y marca de origen.
- [ ] Verificar el bloque de firma carácter por carácter.
- [ ] Verificar que hay exactamente un elemento lime.
- [ ] Verificar que se pide algo con fecha.
- [ ] Generar los adjuntos con `tools/build-export.py`, abrir el PNG y confirmar
      que el grid se ve y que el subtítulo salió en Crimson Pro SemiBold Italic.

---

## 7 · Dónde vive esto

Este archivo es la copia única. El vault enlaza a él desde
`3 Resources/Método AGCS/`, sin duplicar el contenido: el repositorio de GitHub
y Claude Design ya se han desincronizado antes, y una tercera copia en el vault
haría lo mismo. Un cambio de regla se hace aquí y se propaga.
