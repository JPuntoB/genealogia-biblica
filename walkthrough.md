# Mejoras de la Genealogía Bíblica Interactiva

He completado la implementación de todas las mejoras que planteamos en el plan de diseño, mejorando significativamente la usabilidad, navegación, y añadiendo dos vistas completamente nuevas, junto con un rediseño estético completo al estilo **Neo-Skeuo**, optimización móvil integral, el sistema de edición y creación híbrido, y la última ronda de mejoras funcionales.

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

* **Botón "Editar Ficha":** Permite cambiar el *Significado*, *Origen*, *Género*, *Padre*, *Madre*, *Cónyuge* y *Reseña histórica* del personaje activo utilizando controles de formulario en tiempo real.
* **Botón "Crear Personaje":** Abre un modal para crear un nuevo personaje y enlazar sus parentescos de forma manual.
* **Base de Datos Persistente Local:** Las ediciones y personajes nuevos se almacenan localmente en el navegador (`localStorage`) de manera que las consultas, árboles, grafos D3 y mapas muestran las relaciones actualizadas al instante.
* **Exportador de JSON:** Descarga un archivo `correcciones.json` con todos los cambios locales.
* **Integración en el Pipeline de Datos (`organizar_genealogia.py`):** El compilador de Python ahora detecta si existe un archivo `correcciones.json` en la raíz, mezclando los nuevos personajes y sobreescribiendo los campos correspondientes.

---

## 🚀 Ronda Final de Mejoras Implementadas

### Lote 1 — Mejoras al Editor (`visor_genealogia.html`)
1. **Autocompletado Relacional:** Campos de Padre, Madre y Cónyuge cuentan con autocompletado en tiempo real basado en la lista de nombres existentes, evitando errores tipográficos.
2. **Validación relacional al crear:** Al añadir un personaje con parientes inexistentes en la base de datos, el sistema ofrece crearlos automáticamente con una ficha inicial mínima.
3. **Exportar Linaje como PDF:** Un botón descarga en PDF la genealogía completa (de Adán al personaje actual) estructurada en una tabla limpia de ancestros generada mediante `jsPDF`.
4. **Atajos de teclado:** Soporte nativo para:
   * `Ctrl + K` (foco de búsqueda).
   * `E` (activar/desactivar edición).
   * `Escape` (cerrar modales/drawer).
   * `Alt + ←/→` (navegación por el historial).
5. **Accesibilidad (a11y):** Roles ARIA implementados en toda la app, foco de teclado interactivo para todos los chips y controles, y compatibilidad con lectores de pantalla.

### Lote 2 — Nuevas Vistas
6. **Línea de Tiempo Cronológica (`linea_temporal.html`):** Eje horizontal interactivo con zoom que sitúa a los personajes en su época bíblica (con fechas directas o calculadas por parentesco). Incluye un cajón de ficha rápida lateral y filtro de linaje raíz.
7. **Dashboard de Estadísticas (`estadisticas.html`):** Gráficos interactivos (`Chart.js`) que muestran la proporción de géneros, el top de personajes con más descendientes, la distribución generacional y el reparto por linajes.

### Lote 3 — Infraestructura
8. **Búsqueda Global (`index.html`):** El buscador del panel central analiza instantáneamente la base de datos completa y ofrece accesos directos rápidos para abrir al personaje en Fichas, Árbol, Grafo o Mapa.
9. **Modo Offline PWA (`manifest.json` y `sw.js`):** Soporte completo para instalar la aplicación en móviles o tablets y ejecutarla sin necesidad de conexión a internet (los assets principales y las bases de datos de genealogía se cachean automáticamente).
10. **Menú de navegación actualizado:** Todas las cabeceras y menús móviles se han actualizado para integrar fluidamente las 7 vistas de la app.

---

## 📈 Verificación y Pruebas

1. **Pipeline de Datos**: Ejecutado correctamente con:
   ```powershell
   python organizar_genealogia.py --stats
   ```
   *Resultado:* 697 registros procesados con éxito.
2. **Offline PWA**: Verificada la descarga en segundo plano de todos los assets mediante el Service Worker y el correcto renderizado offline.
3. **Generación de PDF**: jsPDF compila correctamente los ancestros sin romper fuentes.
