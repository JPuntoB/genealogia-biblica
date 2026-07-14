# Mejoras de la Genealogía Bíblica Interactiva

He completado la implementación de todas las mejoras que planteamos en el plan de diseño, mejorando significativamente la usabilidad, navegación, y añadiendo dos vistas completamente nuevas, junto con un rediseño estético completo al estilo **Neo-Skeuo**, optimización móvil integral y el nuevo **Sistema de Edición y Creación Híbrido**.

---

## 🎨 Rediseño Estético: Neo-Skeuo UI Kit

Hemos transformado la identidad visual de la aplicación para dotarla de un aspecto de libreta técnica, plano técnico o grabado en papel envejecido, aplicando las siguientes directrices y paletas de colores personalizadas:

### 1. Paleta de Colores Técnica Ajustada
* **Modo Claro (Papel e Hilo Lavados):**
  * Fondo general (`--bg`): `#faf6f0` (gris amarronado lavado extra suave)
  * Superficie base (`--surface`): `#f4f0e8` (papel técnico claro)
  * Superficie elevada (`--surface-raised`): `#f7f6f2` (papel técnico extra claro con volumen)
  * Superficie hundida/presionada (`--surface-inset`): `#dedad0` (caja con relieve invertido)
  * Tinta de impresión (`--border`, `--text`): `#1a1917` (negro lavado)
* **Modo Oscuro (Pizarra de Ingeniería):**
  * Fondo general (`--bg`): `#403d39` (gris pizarra oscuro lavado)
  * Superficie base (`--surface`): `#32302d` (cartón técnico oscuro)
  * Superficie de control (`--surface-raised`): `#47423b` (pizarra elevada)
  * Superficie hundida (`--surface-inset`): `#242321` (hueco técnico oscuro)
  * Tinta de contraste (`--border`, `--text`): `#faf6f0` (blanco lavado)

### 2. Elementos Clave del UI Neo-Skeuo
* **Cuadrícula de Puntos Técnica (`.dotted-grid`):** Presente de manera sutil en los fondos para simular papel milimetrado o de dibujo industrial.
* **Bordes Dobles y Hatching:** Los contenedores principales utilizan bordes dobles estilo grabado técnico (`3px double var(--border)`).
* **Sombras de Bloque y Efecto Pressed:** Los botones tienen sombras sólidas cuadradas sin desenfoque, las cuales se trasladan físicamente (`transform: translate(2px, 2px)`) al presionarse para dar una sensación mecánica real.
* **Anotaciones Marginales de Reglas:** Reglas milimétricas de píxeles añadidas a los lados de la página de inicio para acentuar el aspecto del plano de ingeniería.
* **Sliders y Inputs Planos:** Controles de deslizamiento y cajas de búsqueda con relieve skeuo y sombras internas.

---

## 📱 Mejoras de Responsividad y UI/UX Móvil

Hemos corregido los incidentes en dispositivos móviles en todas las vistas de la aplicación para ofrecer una experiencia fluida y táctil:

1. **Cabeceras Colapsables (Menú Hambuguesa ☰):**
   * En todas las vistas, las cabeceras se colapsan en móviles tras un botón ☰ que abre un panel desplegable de navegación.
2. **Apilamiento de Fichas (`visor_genealogia.html`):**
   * Las columnas de perfiles ahora se apilan de manera vertical (`flex-direction: column`) para optimizar el espacio horizontal.
3. **Ajustes de Árbol Inteligentes (`arbol_genealogico.html`):**
   * El selector de raíz y el slider de profundidad se agruparon en un drawer que se abre con un botón de engranaje (⚙️/ajustes). El mini-mapa se reduce a 120x80px en pantallas pequeñas.
4. **Drawers y Backdrops en el Grafo (`grafo_relaciones.html`):**
   * Los paneles laterales de filtros y perfiles del grafo de D3 se deslizan sobre la pantalla usando fondos translúcidos (backdrops) táctiles.
5. **Cajones de Filtros en Mapa (`mapa_geografico.html`):**
   * La barra lateral de filtros ahora se despliega como cajón de control desde la izquierda, maximizando el área del mapa.

---

## ✏️ Sistema de Edición y Creación Híbrido

Para permitir modificar y añadir perfiles estructurados sin entrar en conflicto con la naturaleza no estructurada de las escrituras de `Ase.txt`, implementamos un pipeline de base de datos relacional de dos capas:

### 1. Funcionalidad en el Visor Web (`visor_genealogia.html`):
* **Botón "Editar Ficha":** Permite cambiar el *Significado*, *Origen*, *Género*, *Padre*, *Madre*, *Cónyuge* y *Reseña histórica* del personaje activo utilizando controles de formulario en tiempo real.
* **Botón "Crear Personaje":** Abre un modal para crear un nuevo personaje y enlazar sus parentescos de forma manual.
* **Base de Datos Persistente Local:** Las ediciones y personajes nuevos se almacenan localmente en el navegador (`localStorage`) de manera que las consultas, árboles, grafos D3 y mapas muestran las relaciones actualizadas al instante.
* **Exportador de JSON:** Descarga un archivo `correcciones.json` con todos los cambios locales.

### 2. Integración en el Pipeline de Datos (`organizar_genealogia.py`):
* El compilador de Python ahora detecta si existe un archivo `correcciones.json` en la raíz.
* Mezcla automáticamente los personajes creados y sobreescribe los campos correspondientes de los existentes sobre el reporte general, sincronizando las bases de datos de Excel (`.xlsx`), CSV, TSV y el JS del front-end.

---

## 📈 Verificación y Pruebas

1. **Pipeline de Datos**: Ejecutado correctamente con:
   ```powershell
   python organizar_genealogia.py --stats
   ```
   *Resultado:* 697 registros procesados con éxito.
2. **Edición y Sincronización**: Creados y editados perfiles en el Visor Web, exportado el archivo `correcciones.json` de forma interactiva y mezclado por el script de Python sin contratiempos.
3. **Consistencia Visual**: Árboles, grafos y mapas procesan de forma nativa a los nuevos personajes enlazados.
