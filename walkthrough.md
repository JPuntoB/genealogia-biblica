# Mejoras de la Genealogía Bíblica Interactiva

He completado la implementación de todas las mejoras que planteamos en el plan de diseño, mejorando significativamente la usabilidad, navegación, y añadiendo dos vistas completamente nuevas, junto con un rediseño estético completo al estilo **Neo-Skeuo**.

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

## 🛠️ Cambios Realizados por Archivo

### 1. 🏠 Página de Inicio Renovada (`index.html`)
- **Estilo Libreta**: Rediseñada con tarjetas técnicas con doble línea, iconos monocromáticos skeuo y reglas de píxeles marginales estéticas.
- **Acceso Directo**: 4 tarjetas que reaccionan mecánicamente al pasar el ratón por encima (efecto de traslación).

### 2. 📇 Visor de Fichas Mejorado (`visor_genealogia.html`)
- **Fichas e Inset Inputs**: Cajas de búsqueda estilo relieve invertido y fichas de detalle enmarcadas en bordes grabados.
- **Historial e Interfaz**: Botones mecánicos elevados para navegar por el historial, y panel de comparación con estilo de ficha duplicada.
- **Línea de Tiempo del Linaje**: Ajustada visualmente como una regla de medición técnica sobre los patriarcas clave.

### 3. 🌳 Árbol Genealógico Avanzado (`arbol_genealogico.html`)
- **Fondo de Ingeniería**: Fondo de cuadrícula punteada interactiva que se mueve con el árbol.
- **Nodos Técnicos**: Cajas planas monocromas para los nodos de hombres y mujeres, con rebordes sólidos de tinta.
- **Minimap Blueprint**: Renderizado con bordes dobles simulando un plano de control técnico.

### 4. 🕸️ Nueva Vista: Grafo de Relaciones (`grafo_relaciones.html`)
- **Red Bosquejada**: Líneas de conexión y enlaces en tinta lavada; nodos de baja saturación con borde negro de 2px.
- **Tablero de Mandos**: Panel izquierdo con sliders skeuomorphic y pills de control técnico.

### 5. 🗺️ Nueva Vista: Mapa Geográfico (`mapa_geografico.html`)
- **Fichas Flotantes**: Ventana de detalles con doble reborde y botones skeuo.
- **Controles de Mapa**: Los botones clásicos de zoom de Leaflet se integraron a la paleta de papel envejecido y bordes del UI kit.

### 6. 🐍 Procesador de Datos Python (`organizar_genealogia.py`)
- **Salida Limpia**: Eliminados los emojis problemáticos y reemplazados por delimitadores ASCII seguros para evitar excepciones en la codificación de consolas locales.

---

## 📈 Verificación y Pruebas

1. **Pipeline de Datos**: Ejecutado correctamente con:
   ```powershell
   python organizar_genealogia.py --stats
   ```
   *Resultado:* 669 registros procesados, guardados en 5 formatos y 4 ciclos de consistencia detectados y reportados con éxito en consola.
2. **Coherencia del Tema**: Comprobado el correcto comportamiento de la paleta en modo claro (`#faf6f0`) y oscuro (`#403d39`) a través de las 5 vistas de la aplicación.
