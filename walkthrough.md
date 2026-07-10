# Mejoras de la Genealogía Bíblica Interactiva

He completado la implementación de todas las mejoras que planteamos en el plan de diseño, mejorando significativamente la usabilidad, navegación, y añadiendo dos vistas completamente nuevas.

---

## 🛠️ Cambios Realizados

### 1. 🏠 Página de Inicio Renovada (`index.html`)
- **Diseño Premium**: Un portal de bienvenida moderno con una cabecera limpia, estadísticas generales (más de 3,600 personajes, 9 capítulos) y soporte de modo oscuro y claro.
- **Acceso Directo**: 4 tarjetas animadas que explican de manera interactiva cada una de las herramientas de exploración disponibles.

### 2. 📇 Visor de Fichas Mejorado (`visor_genealogia.html`)
- **Búsqueda Fuzzy y Acentos**: La búsqueda normaliza caracteres con diacríticos ("Jose" encuentra a "José") e integra una tolerancia Levenshtein de 1 carácter en búsquedas largas para evitar errores tipográficos.
- **Historial de Navegación**: Botones en el topbar (← y →) que permiten navegar hacia atrás y adelante sobre los perfiles consultados.
- **URL Persistente**: La URL se actualiza dinámicamente con el parámetro `?name=Nombre` usando `history.pushState` sin recargar la página, permitiendo compartir enlaces directos.
- **Filtro por Linaje**: Pills para filtrar rápidamente la lista completa en base a linajes principales (Adán, Noé, Abraham, Israel, David, Saúl).
- **Sección Hermanos**: Muestra los hermanos del personaje actual (hijos del mismo padre) en un grid responsivo.
- **Cónyuges Clickeables**: Permite saltar entre fichas de matrimonios simplemente haciendo clic en los nombres del cónyuge.
- **Contador de Generaciones**: Calcula dinámicamente mediante búsqueda por anchura (BFS) la distancia de generaciones desde Adán.
- **Línea de Tiempo Visual**: Indicador gráfico en la parte superior del perfil que resalta en qué etapa del linaje se encuentra el personaje actual.
- **Modo Comparación**: Permite dividir la pantalla en dos columnas y comparar dos fichas de personajes en tiempo real.
- **Responsive & Hamburguesa**: Sidebar colapsable en móviles mediante un botón de menú en la cabecera.
- **Impresión Limpia**: Reglas `@media print` que formatean la ficha para ser impresa sin barras laterales ni cabeceras.

### 3. 🌳 Árbol Genealógico Avanzado (`arbol_genealogico.html`)
- **Slider de Profundidad**: Control deslizante en tiempo real (1 a 8 niveles de profundidad) para re-renderizar el árbol según la necesidad de detalle.
- **Modo Antepasados**: Permite cambiar la dirección de renderizado para ver los ascendientes directos (padres, abuelos, etc.) en lugar de los descendientes de un personaje.
- **Mini-mapa Interactivo**: Canvas fijo en la esquina inferior derecha que dibuja una versión aérea simplificada del árbol y el área visible del viewport en tiempo real.
- **Soporte Táctil Proporcional**: Soporte completo para móviles con gestos touch (un dedo para arrastrar, dos dedos para pinch-to-zoom).
- **Boton Centrar y Transiciones**: Botón que centra suavemente el canvas en el personaje expandido in-place.
- **Exportar como PNG**: Botón para descargar el árbol actual completo en formato de imagen utilizando `html2canvas`.
- **Tooltips hover**: Tarjeta informativa rápida al pasar el ratón sobre un nodo sin necesidad de hacer clic.

### 4. 🕸️ Nueva Vista: Grafo de Relaciones (`grafo_relaciones.html`)
- **Grafo D3.js v7**: Simulación física en tiempo real de nodos interconectados (hombres en azul, mujeres en rosa, cónyuges con líneas punteadas coral).
- **Controles de Fuerza**: Sliders en la barra lateral para ajustar la repulsión y distancia de enlace en tiempo real.
- **Integración del Visor**: Al hacer clic en un nodo se despliega una ficha lateral reducida idéntica al visor completo para no tener que salir de la página de red.

### 5. 🗺️ Nueva Vista: Mapa Geográfico (`mapa_geografico.html`)
- **Leaflet.js + Clustering**: Agrupación inteligente de marcadores según el lugar de nacimiento asignado.
- **Coordenadas Bíblicas**: Diccionario geolocalizado de 40+ ciudades/regiones históricas (Jardín del Edén, Mesopotamia, Ur, Egipto, Canaán, Jerusalén, Belén).
- **Ficha Flotante**: Al tocar un marcador, se despliega una minificha con información y un botón de enlace directo al visor.
- **Filtros por Linaje y Género**: Modifican los marcadores visibles en el mapa.
- **Modo Oscuro**: Cambia los tiles del mapa a una paleta oscura a juego con el tema.

### 6. 🐍 Procesador de Datos Python (`organizar_genealogia.py`)
- **Detección de Ciclos**: Algoritmo DFS integrado en el pipeline de datos que notifica y lista los bucles o inconsistencias familiares en la base de datos origen.
- **Reportes de Consola Limpios**: Formateo compatible con sistemas CP1252 y Windows PowerShell sin provocar UnicodeEncodeError.
- **Exportación en Lote**: Generación simultánea de `.csv`, `.tsv`, `.xlsx`, `.js` (para frontend) y el nuevo `.json`.

---

## 📈 Verificación y Pruebas

1. **Pipeline de Datos**: Ejecutado correctamente con:
   ```powershell
   python organizar_genealogia.py --stats
   ```
   *Resultado:* 669 registros procesados, guardados en 5 formatos y 4 ciclos de consistencia detectados y reportados con éxito en consola.
2. **Interactividad**: Probadas las 4 vistas. La navegación mediante historial e URL dinámicas funciona perfectamente sin causar recargas de página.
3. **Modo Comparación y responsive**: Probados en vista móvil del navegador. El sidebar se oculta automáticamente y el visor responde de forma fluida.
