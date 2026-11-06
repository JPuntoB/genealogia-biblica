# 📜 Genealogía Bíblica Interactiva — 1 Crónicas

Aplicación web interactiva, moderna y accesible para la exploración técnica y visual de las genealogías bíblicas (especialmente centrada en los primeros capítulos de **1 Crónicas** y sus conexiones con **Génesis** y los Evangelios).

Cuenta con un sistema de diseño estético **Neo-Skeuo** (estilo libreta técnica, plano de ingeniería y papel milimetrado), arquitectura offline (PWA) y 6 esquemas interactivos de exploración.

---

## 🧭 Vistas y Herramientas

1. **Visor de Fichas (`visor_genealogia.html`)**:
   - Perfil biográfico completo con significado etimológico, origen geográfico, referencias cruzadas y notas.
   - Cálculo automático de linaje directo de generaciones (desde Adán).
   - Comparador dual de personajes en pantalla dividida.
   - Sistema de edición en vivo y creación de personajes locales (`localStorage`).
   - Exportación de linaje en formato PDF estructurado (`jsPDF`).
   - Exportación e importación de cambios mediante `correcciones.json`.
   - Atajos de teclado: `Ctrl + K` (búsqueda), `E` (modo edición), `Escape` (cerrar modales/paneles), `Alt + ←/→` (historial).

2. **Árbol Jerárquico (`arbol_genealogico.html`)**:
   - Diagrama de árbol interactivo con pan (arrastre), zoom y minimapa de navegación.
   - Selector de raíz y regulador de niveles de profundidad (1 a 8).
   - Modo antepasados (ascendencia) y descendencia directa.
   - Exportación de la vista actual a imagen PNG (`html2canvas`).

3. **Grafo de Relaciones (`grafo_relaciones.html`)**:
   - Red de simulación física en tiempo real basada en **D3.js v7**.
   - Conexiones parentales (padre/madre/hijo), conyugales y fraternales.
   - Filtros dinámicos por linaje patriarcal y género.
   - Drawer lateral con detalles biográficos instantáneos al hacer clic en cualquier nodo.

4. **Mapa Cartográfico (`mapa_geografico.html`)**:
   - Georreferenciación histórica de lugares de nacimiento y asentamientos bíblicos (Edén, Ur de los Caldeos, Harán, Belén, Jerusalén, Hebrón, etc.).
   - Motor de mapas **Leaflet** con agrupación inteligente por clusters de marcadores (**MarkerCluster**).
   - Búsqueda directa y filtrado por región y género.

5. **Línea Temporal (`linea_temporal.html`)**:
   - Eje cronológico estimado desde la Creación (~4000 a.C.) hasta el Exilio en Babilonia y Zorobabel (~520 a.C.).
   - Visualización de grandes eras bíblicas (Creación, Diluvio, Patriarcas, Éxodo, Monarquía, Exilio).
   - Algoritmo de interpolación temporal generacional para personajes sin fecha bíblica explícita.

6. **Dashboard de Estadísticas (`estadisticas.html`)**:
   - Gráficos analíticos mediante **Chart.js** (distribución por género, ranking de personajes con mayor descendencia, densidad por linajes y volumen por generación).
   - Métricas clave (KPIs) en tiempo real sincronizadas con las ediciones locales.

7. **Portal Principal y Búsqueda Global (`index.html`)**:
   - Buscador universal instantáneo que indexa toda la base de datos y ofrece accesos directos a cualquiera de las 6 vistas.
   - Indicador dinámico de personajes registrados y acceso rápido conmutador de tema Claro / Oscuro.

---

## 📱 Modo Offline y PWA (Progressive Web App)

La aplicación implementa un Service Worker (`sw.js`) y manifiesto (`manifest.json`) con icono vectorial (`favicon.svg`):
- Se puede instalar en teléfonos móviles (Android / iOS) o en el escritorio (Chrome / Edge / Firefox) como una app independiente.
- Funciona al 100% sin conexión a internet una vez cargada por primera vez.
- Sincronización transparente de ediciones locales entre todas las vistas a través de `localStorage`.

---

## ⚙️ Pipeline de Datos y Actualización

La base de datos original se procesa desde `Ase.txt` o `genealogia_organizada.xlsx`:

- **Generar archivos desde Excel:**
  ```bash
  python excel_to_js.py
  ```
  *(Lee `genealogia_organizada.xlsx` y compila `genealogia_data.js`).*

- **Reprocesar texto original y detectar ciclos o validar datos:**
  ```bash
  python organizar_genealogia.py --stats
  ```

---

## 🌐 Despliegue en Internet y Dominios Gratuitos

Al tratarse de una aplicación web estática (HTML, JS, CSS, SVG, JSON), **no requiere ningún servidor backend de pago**.

### 1. La Mejor Opción: Alojamiento en la nube con subdominio gratuito y SSL incluido
Existen plataformas de prestigio mundial que ofrecen alojamiento gratuito para siempre, con certificado HTTPS automático (imprescindible para el Service Worker y PWA), CDN global y disponibilidad del 99.99%:

| Proveedor | Dominio gratuito | Ventajas principales |
| :--- | :--- | :--- |
| **Netlify** *(Recomendado)* | `tunombre.netlify.app` | Ya incluye archivo `netlify.toml` preconfigurado. Solo arrastrar la carpeta o vincular repositorio. 100 GB/mes de tráfico gratuito. |
| **Cloudflare Pages** | `tunombre.pages.dev` | **Ancho de banda 100% ilimitado**, la red DNS más rápida del mundo y máxima protección DDoS. |
| **GitHub Pages** | `usuario.github.io/hijos` | Integrado directamente con control de versiones Git. |
| **Vercel** | `tunombre.vercel.app` | Despliegue ultra rápido y excelente latencia. |

### 2. Nombres de dominio sugeridos para este proyecto
Para ofrecer la mejor experiencia al usuario (profesional, memorable y fácil de escribir):
- `genealogia-biblica.netlify.app`
- `cronicas-genealogia.netlify.app`
- `arbol-genealogia.pages.dev`
- `genealogia-cronicas.pages.dev`

### 3. ¿Qué ocurre con los antiguos dominios gratuitos `.tk`, `.ml`, `.ga`, `.cf`?
> [!WARNING]
> Antiguamente existían servicios como Freenom que registraban dominios gratuitos de nivel superior (`.tk`, `.ml`, etc.). **Hoy en día no son recomendables y están prácticamente descontinuados**:
> - En 2023–2024 las autoridades internacionales de Internet (ICANN) y demandas judiciales frenaron sus operaciones por abusos y phishing.
> - Los buscadores como Google y los antivirus bloquean o marcan con advertencias de seguridad la mayoría de esos dominios.
> - Si un sitio alcanzaba visitas, el registrador podía revocar el dominio de forma arbitraria.
>
> Por ello, **la opción más sólida, profesional, segura y 100% gratuita para el usuario es un subdominio HTTPS oficial en Netlify (`.netlify.app`) o Cloudflare Pages (`.pages.dev`)**.
