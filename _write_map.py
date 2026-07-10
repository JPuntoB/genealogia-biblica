html = r"""<!DOCTYPE html>
<html lang="es" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Genealog&#237;a B&#237;blica &middot; Mapa Geogr&#225;fico</title>
    <meta name="description" content="Mapa interactivo de los lugares de nacimiento de los personajes b&#237;blicos de 1 Cr&#243;nicas. Visualiza d&#243;nde vivieron los patriarcas y sus descendientes.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Leaflet -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <!-- MarkerCluster -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css">
    <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
    <style>
        /* == Design tokens ============================================ */
        :root {
            --bg:        #f5f4f2;
            --surface:   #ffffff;
            --border:    #e4e2dc;
            --text:      #1a1916;
            --muted:     #7a7870;
            --subtle:    #b0ada6;
            --accent:    #1a56db;
            --accent-bg: #eef3ff;
            --m-dot:     #3b82f6;
            --f-dot:     #e879a0;
            --radius-sm: 8px;
            --radius-md: 14px;
            --shadow-md: 0 4px 20px rgba(0,0,0,.12);
        }
        [data-theme="dark"] {
            --bg:        #111110;
            --surface:   #1c1b19;
            --border:    #2e2c28;
            --text:      #f0ede8;
            --muted:     #888580;
            --subtle:    #5a5753;
            --accent:    #5b8def;
            --accent-bg: #1a2340;
            --m-dot:     #60a5fa;
            --f-dot:     #f472b6;
            --shadow-md: 0 4px 20px rgba(0,0,0,.45);
        }

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { height: 100%; }
        body {
            font-family: 'Inter', system-ui, sans-serif;
            font-size: 14px; line-height: 1.5;
            background: var(--bg); color: var(--text);
            display: flex; flex-direction: column; overflow: hidden;
        }

        /* == Topbar =================================================== */
        .topbar {
            height: 52px; min-height: 52px;
            display: flex; align-items: center; gap: 12px;
            padding: 0 20px;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            flex-shrink: 0; z-index: 1000;
        }
        .topbar-brand { font-size: 13px; font-weight: 600; color: var(--text); display: flex; align-items: center; gap: 8px; }
        .topbar-brand-dot { width: 7px; height: 7px; background: var(--accent); border-radius: 50%; }
        .topbar-sub { font-size: 12px; color: var(--subtle); padding-left: 4px; }
        .topbar-sep { flex: 1; }
        .topbar-btn {
            display: flex; align-items: center; gap: 5px;
            padding: 5px 11px; font-size: 12px; font-weight: 500;
            color: var(--muted); background: transparent;
            border: 1px solid var(--border); border-radius: var(--radius-sm);
            cursor: pointer; text-decoration: none; font-family: inherit;
            transition: border-color .15s, color .15s, background .15s;
        }
        .topbar-btn:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-bg); }
        .topbar-btn svg { width: 13px; height: 13px; fill: currentColor; flex-shrink: 0; }

        /* == Main layout ============================================== */
        .workspace { flex: 1; display: flex; overflow: hidden; position: relative; }

        /* == Sidebar ================================================== */
        .sidebar {
            width: 240px; min-width: 240px;
            display: flex; flex-direction: column;
            background: var(--surface);
            border-right: 1px solid var(--border);
            z-index: 500; overflow-y: auto;
        }
        .sidebar::-webkit-scrollbar { width: 3px; }
        .sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
        .sb-section { padding: 14px 14px 10px; border-bottom: 1px solid var(--border); }
        .sb-section:last-child { border-bottom: none; }
        .sb-label {
            font-size: 10px; font-weight: 700; letter-spacing: .6px;
            text-transform: uppercase; color: var(--subtle); margin-bottom: 9px;
        }

        /* Pills */
        .filter-pills { display: flex; flex-wrap: wrap; gap: 5px; }
        .f-pill {
            padding: 4px 10px; font-size: 11px; font-weight: 500;
            color: var(--muted); background: var(--bg);
            border: 1px solid var(--border); border-radius: 20px;
            cursor: pointer; font-family: inherit; transition: all .15s;
        }
        .f-pill:hover { border-color: var(--accent); color: var(--accent); background: var(--accent-bg); }
        .f-pill.active { border-color: var(--accent); color: var(--accent); background: var(--accent-bg); font-weight: 600; }

        /* Gender toggle */
        .gender-toggle { display: flex; gap: 5px; }
        .g-btn {
            flex: 1; padding: 6px 4px; font-size: 11px; font-weight: 500;
            color: var(--muted); background: var(--bg);
            border: 1px solid var(--border); border-radius: var(--radius-sm);
            cursor: pointer; font-family: inherit; text-align: center; transition: all .15s;
        }
        .g-btn.active-all { border-color: var(--accent); color: var(--accent); background: var(--accent-bg); }
        .g-btn.active-m   { border-color: var(--m-dot); color: var(--m-dot); background: rgba(59,130,246,.1); }
        .g-btn.active-f   { border-color: var(--f-dot); color: var(--f-dot); background: rgba(232,121,160,.1); }

        /* Counter */
        .counter-box {
            background: var(--bg); border: 1px solid var(--border);
            border-radius: var(--radius-sm); padding: 10px 13px;
            display: flex; align-items: baseline; gap: 6px;
        }
        .counter-num { font-size: 22px; font-weight: 700; color: var(--text); line-height: 1; }
        .counter-lbl { font-size: 11px; color: var(--subtle); }

        /* Legend */
        .legend-row { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--muted); padding: 3px 0; }
        .leg-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
        .leg-dot.m { background: var(--m-dot); }
        .leg-dot.f { background: var(--f-dot); }
        .cluster-hint { display: flex; align-items: center; gap: 8px; font-size: 11px; color: var(--subtle); margin-top: 8px; }
        .cluster-sample {
            width: 24px; height: 24px; border-radius: 50%;
            background: rgba(59,130,246,.18); border: 2.5px solid rgba(59,130,246,.6);
            display: flex; align-items: center; justify-content: center;
            font-size: 9px; font-weight: 700; color: #1d4ed8; flex-shrink: 0;
        }

        /* == Map ====================================================== */
        .map-wrap { flex: 1; position: relative; overflow: hidden; }
        #map { width: 100%; height: 100%; z-index: 1; }
        .leaflet-container { font-family: 'Inter', system-ui, sans-serif; }

        /* == Spinner ================================================== */
        #spinner {
            position: absolute; inset: 0;
            background: var(--bg);
            display: flex; flex-direction: column;
            align-items: center; justify-content: center; gap: 14px;
            z-index: 800;
        }
        .spin-ring {
            width: 38px; height: 38px;
            border: 3px solid var(--border);
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin .7s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .spin-txt { font-size: 13px; color: var(--muted); }

        /* == Ficha panel ============================================== */
        #fichaPanel {
            position: absolute; bottom: 28px; right: 20px;
            width: 320px;
            background: var(--surface); border: 1px solid var(--border);
            border-radius: var(--radius-md); box-shadow: var(--shadow-md);
            z-index: 900; display: none; overflow: hidden;
            animation: slideUp .2s ease;
        }
        @keyframes slideUp {
            from { transform: translateY(12px); opacity: 0; }
            to   { transform: translateY(0);    opacity: 1; }
        }
        .fh { display: flex; align-items: flex-start; gap: 10px; padding: 14px 16px 10px; border-bottom: 1px solid var(--border); }
        .fh-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; margin-top: 4px; }
        .fh-name { font-size: 16px; font-weight: 700; flex: 1; line-height: 1.2; }
        .fh-close { background: none; border: none; cursor: pointer; color: var(--subtle); font-size: 16px; padding: 0; line-height: 1; transition: color .15s; }
        .fh-close:hover { color: var(--text); }
        .fb { padding: 10px 16px 14px; display: flex; flex-direction: column; gap: 6px; }
        .fb-row { display: flex; gap: 8px; align-items: baseline; }
        .fb-key { font-size: 10px; font-weight: 700; letter-spacing: .4px; text-transform: uppercase; color: var(--subtle); width: 52px; flex-shrink: 0; padding-top: 1px; }
        .fb-val { font-size: 12.5px; color: var(--text); flex: 1; }
        .fb-notes { font-size: 12px; color: var(--muted); line-height: 1.6; background: var(--bg); border-radius: var(--radius-sm); padding: 8px 10px; margin-top: 2px; }
        .fb-actions { display: flex; gap: 7px; margin-top: 6px; }
        .fb-btn {
            flex: 1; padding: 7px 10px; font-size: 11.5px; font-weight: 600;
            border-radius: var(--radius-sm); cursor: pointer; text-align: center;
            text-decoration: none; font-family: inherit; transition: all .15s;
            background: var(--accent); color: #fff; border: none;
        }
        .fb-btn:hover { filter: brightness(1.1); }

        /* Custom marker hover */
        .cmark { transition: transform .15s; cursor: pointer; }
        .cmark:hover { transform: scale(1.25); }
    </style>
</head>
<body>

<!-- == Topbar ========================================================= -->
<header class="topbar">
    <div class="topbar-brand">
        <div class="topbar-brand-dot"></div>
        Genealog&#237;a B&#237;blica
    </div>
    <span class="topbar-sub">1 Cr&#243;nicas 1&#8211;9</span>
    <div class="topbar-sep"></div>
    <a href="visor_genealogia.html" class="topbar-btn">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
        Visor fichas
    </a>
    <a href="arbol_genealogico.html" class="topbar-btn">
        <svg viewBox="0 0 24 24"><path d="M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z"/></svg>
        &#193;rbol gr&#225;fico
    </a>
    <button class="topbar-btn" id="themeToggle" title="Cambiar tema">
        <svg id="sunIcon" style="display:none" viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zm0 8c-1.65 0-3-1.35-3-3s1.35-3 3-3 3 1.35 3 3-1.35 3-3 3zm0-11c-.55 0-1-.45-1-1V2c0-.55.45-1 1-1s1 .45 1 1v1c0 .55-.45 1-1 1zm0 16c-.55 0-1 .45-1 1v1c0 .55.45 1 1 1s1-.45 1-1v-1c0-.55-.45-1-1-1zm8-8c0-.55-.45-1-1-1h-1c-.55 0-1 .45-1 1s.45 1 1 1h1c.55 0 1-.45 1-1zM6 12c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1s.45 1 1 1h1c.55 0 1-.45 1-1zm11.66-5.66-.71-.71c-.39-.39-1.02-.39-1.41 0s-.39 1.02 0 1.41l.71.71c.39.39 1.02.39 1.41 0s.39-1.02 0-1.41zm-11.31 11.3-.71.71c-.39.39-.39 1.02 0 1.41s1.02.39 1.41 0l.71-.71c.39-.39.39-1.02 0-1.41s-1.02-.39-1.41 0z"/></svg>
        <svg id="moonIcon" viewBox="0 0 24 24"><path d="M12.3 22h-.1c-5.5 0-10-4.5-10-10 0-4.8 3.5-8.9 8.3-9.7.6-.1 1.1.4 1 1-.4 2.4.4 4.9 2.1 6.6 1.7 1.7 4.2 2.5 6.6 2.1.6-.1 1.1.4 1 1-.8 4.8-4.9 8.3-9.7 8.3z"/></svg>
        Tema
    </button>
</header>

<!-- == Workspace ====================================================== -->
<div class="workspace">

    <!-- Sidebar -->
    <aside class="sidebar">
        <div class="sb-section">
            <div class="sb-label">Personajes en el mapa</div>
            <div class="counter-box">
                <span class="counter-num" id="markerCount">&#8212;</span>
                <span class="counter-lbl">personajes visibles</span>
            </div>
        </div>

        <div class="sb-section">
            <div class="sb-label">Filtrar por linaje</div>
            <div class="filter-pills">
                <button class="f-pill active" onclick="setLineage('all',this)">Todos</button>
                <button class="f-pill" onclick="setLineage('Adam',this)">Ad&#225;n</button>
                <button class="f-pill" onclick="setLineage('No\u00e9',this)">No&#233;</button>
                <button class="f-pill" onclick="setLineage('Abraham',this)">Abraham</button>
                <button class="f-pill" onclick="setLineage('Israel',this)">Israel</button>
                <button class="f-pill" onclick="setLineage('David',this)">David</button>
                <button class="f-pill" onclick="setLineage('Sa\u00FAl',this)">Sa&#250;l</button>
            </div>
        </div>

        <div class="sb-section">
            <div class="sb-label">Filtrar por g&#233;nero</div>
            <div class="gender-toggle">
                <button class="g-btn active-all" id="gAll" onclick="setGender('all')">Todos</button>
                <button class="g-btn" id="gM" onclick="setGender('M')">&#9794; Hombres</button>
                <button class="g-btn" id="gF" onclick="setGender('F')">&#9792; Mujeres</button>
            </div>
        </div>

        <div class="sb-section">
            <div class="sb-label">Leyenda</div>
            <div class="legend-row"><div class="leg-dot m"></div><span>Personaje masculino</span></div>
            <div class="legend-row"><div class="leg-dot f"></div><span>Personaje femenino</span></div>
            <div class="cluster-hint">
                <div class="cluster-sample">N</div>
                <span>Grupo de marcadores &#8212; clic para expandir</span>
            </div>
        </div>

        <div class="sb-section" style="flex:1;display:flex;align-items:flex-end;">
            <p style="font-size:11px;color:var(--subtle);line-height:1.6;">
                Haz clic en un marcador para ver la ficha del personaje.<br>
                Los grupos se expanden al hacer zoom.
            </p>
        </div>
    </aside>

    <!-- Map wrapper -->
    <div class="map-wrap">
        <div id="spinner">
            <div class="spin-ring"></div>
            <div class="spin-txt">Cargando personajes&#8230;</div>
        </div>

        <div id="map"></div>

        <!-- Floating ficha panel -->
        <div id="fichaPanel">
            <div class="fh">
                <div class="fh-dot" id="fichaDot"></div>
                <div class="fh-name" id="fichaName">&#8212;</div>
                <button class="fh-close" onclick="closeFicha()" title="Cerrar">&#10005;</button>
            </div>
            <div class="fb">
                <div class="fb-row">
                    <span class="fb-key">G&#233;nero</span>
                    <span class="fb-val" id="fichaGender">&#8212;</span>
                </div>
                <div class="fb-row">
                    <span class="fb-key">Origen</span>
                    <span class="fb-val" id="fichaPlace">&#8212;</span>
                </div>
                <div class="fb-row" id="fichaFatherRow" style="display:none">
                    <span class="fb-key">Padre</span>
                    <span class="fb-val" id="fichaFather">&#8212;</span>
                </div>
                <div class="fb-row" id="fichaMotherRow" style="display:none">
                    <span class="fb-key">Madre</span>
                    <span class="fb-val" id="fichaMother">&#8212;</span>
                </div>
                <div class="fb-notes" id="fichaNotes" style="display:none"></div>
                <div class="fb-actions">
                    <a class="fb-btn" id="fichaLink" href="#" target="_blank">Ver ficha completa &#8594;</a>
                </div>
            </div>
        </div>
    </div>

</div><!-- workspace -->

<script src="genealogia_data.js"></script>
<script>
/* ====================================================================
   DATA LAYER
   ==================================================================== */
const people = {};

const LOCAL_PATRIARCHS = {
    "Adam":    { lugar:"Jard\u00edn del Ed\u00e9n",              notas:"Primer ser humano creado por Dios. Colocado en el Ed\u00e9n, expulsado tras la ca\u00edda." },
    "Eva":     { lugar:"Jard\u00edn del Ed\u00e9n",              notas:"Primera mujer, madre de Ca\u00edn, Abel, Set y otros." },
    "Set":     { lugar:"Fuera del Ed\u00e9n",                    notas:"Tercer hijo de Ad\u00e1n y Eva. De su l\u00ednea desciende No\u00e9." },
    "No\u00e9":    { lugar:"Tierra pre-diluviana / Mesopotamia", notas:"Construy\u00f3 el arca para salvar a su familia del Diluvio universal." },
    "Abraham": { lugar:"Ur de los Caldeos",                      notas:"Patriarca hebreo. Dios le orden\u00f3 salir de Ur hacia Cana\u00e1n." },
    "Israel":  { lugar:"Padan-aram",                             notas:"Hijo de Isaac y Rebeca. Padre de las doce tribus de Israel." },
    "David":   { lugar:"Bel\u00e9n",                             notas:"Segundo rey de Israel. Venci\u00f3 a Goliat y recibi\u00f3 la promesa del trono eterno." },
    "Salom\u00f3n":{ lugar:"Jerusal\u00e9n",                     notas:"Hijo de David y Betsab\u00e9, famoso por su sabidur\u00eda y el Primer Templo." }
};

function buildRelationshipMap() {
    if (typeof GENEALOGIA_DATA === 'undefined') return;
    function gc(name) {
        if (!name) return null;
        const n = name.trim(); if (!n) return null;
        if (!people[n]) people[n] = { name:n, gender:"M", father:"", mother:"", birthPlace:"", spouses:new Set(), children:[], notes:"", reference:"", meaning:"" };
        return people[n];
    }
    GENEALOGIA_DATA.forEach(row => {
        const cn = row["Hijos"], fn = row["Padre"], mn = row["Madre"];
        const child = gc(cn), father = gc(fn), mother = gc(mn);
        if (child) {
            if (fn) child.father = fn;
            if (mn) child.mother = mn;
            child.gender = row["G\u00e9nero Hijos"] || "M";
            child.birthPlace = (row["Lugar de nacimiento"] || "").replace(/\s*\(padre\)\s*/i, "").trim();
            const fi = row["Informaci\u00f3n Adicional"] || row["Notas"] || "";
            const cm = fi.match(/Sobre (?:el hijo|la hija) \([^)]+\):\s*(.+?)(?:\s*\|\s*Sobre (?:el padre|la madre)|$)/i);
            child.notes = cm ? cm[1].trim() : fi;
            child.reference = row["Referencia"] || "";
        }
        const bp = (row["Lugar de nacimiento"] || "").replace(/\s*\(padre\)\s*/i, "").trim();
        if (father && cn) {
            father.children.push({ name:cn, gender:row["G\u00e9nero Hijos"]||"M", birthPlace:bp });
            if (mn) { father.spouses.add(mn); mother.spouses.add(fn); }
        }
        if (mother && cn) mother.children.push({ name:cn, gender:row["G\u00e9nero Hijos"]||"M", birthPlace:bp });
        if (fn && row["Significado del Nombre (Padre)"]) father.meaning = row["Significado del Nombre (Padre)"];
    });
    Object.keys(LOCAL_PATRIARCHS).forEach(name => {
        const loc = LOCAL_PATRIARCHS[name], p = gc(name); if (!p) return;
        if (loc.lugar) p.birthPlace = loc.lugar;
        if (loc.notas && !p.notes) p.notes = loc.notas;
    });
}

/* ====================================================================
   PLACE COORDS
   ==================================================================== */
const PLACE_COORDS = {
    "Ed\u00e9n":                              [37.5,  42.5],
    "Jard\u00edn del Ed\u00e9n":              [37.5,  42.5],
    "Jard\u00edn del ed\u00e9n":              [37.5,  42.5],
    "Mesopotamia":                             [33.5,  44.5],
    "Tierra pre-diluviana / Mesopotamia":      [33.5,  44.5],
    "Mesopotamia (aprox.)":                    [33.5,  44.5],
    "Cana\u00e1n":                             [31.5,  35.5],
    "Tierra de Cana\u00e1n":                   [31.5,  35.5],
    "Tierra de Nod / Cana\u00e1n":             [31.3,  35.0],
    "Ur de los Caldeos":                       [30.96, 46.1],
    "Ur":                                      [30.96, 46.1],
    "Har\u00e1n":                              [36.86, 39.03],
    "Padan-aram":                              [36.86, 39.03],
    "Egipto":                                  [27.0,  30.0],
    "Tierra de Gos\u00e9n":                    [30.8,  31.7],
    "Gos\u00e9n":                              [30.8,  31.7],
    "Bel\u00e9n":                              [31.70, 35.20],
    "Jerusal\u00e9n":                          [31.78, 35.23],
    "Hebr\u00f3n":                             [31.53, 35.10],
    "Siquem":                                  [32.21, 35.29],
    "Ram\u00e1":                               [31.92, 35.18],
    "Sil\u00f3":                               [32.05, 35.29],
    "Gib\u00e1 de Benjam\u00edn":              [31.85, 35.22],
    "Gib\u00e1":                               [31.85, 35.22],
    "Mamb\u00e9r":                             [31.53, 35.10],
    "Mambr\u00e9":                             [31.53, 35.10],
    "Beerseba":                                [31.25, 34.79],
    "Gaza":                                    [31.51, 34.47],
    "Jeric\u00f3":                             [31.86, 35.44],
    "Dot\u00e1n":                              [32.42, 35.20],
    "Peniel":                                  [32.20, 35.60],
    "Mizpa":                                   [31.87, 35.20],
    "Moab":                                    [31.2,  35.7],
    "Am\u00f3n":                               [31.95, 35.93],
    "Edom":                                    [30.5,  35.5],
    "Idumea":                                  [30.5,  35.5],
    "Desierto de Sina\u00ed":                  [29.5,  33.8],
    "Sina\u00ed":                              [29.5,  33.8],
    "Fuera del Ed\u00e9n":                     [36.0,  41.0],
    "Tierra de Nod":                           [36.0,  41.5],
    "Arabia":                                  [25.0,  45.0],
    "Damasco":                                 [33.51, 36.29],
    "Siria":                                   [34.8,  38.9],
    "N\u00ednive":                             [36.36, 43.15],
    "Asiria":                                  [36.0,  43.5],
    "Babilonia":                               [32.54, 44.42],
    "Babel":                                   [32.54, 44.42],
    "Persia":                                  [32.0,  53.0]
};

function resolveCoords(bp) {
    if (!bp) return null;
    const s = bp.trim();
    if (PLACE_COORDS[s]) return PLACE_COORDS[s];
    const sl = s.toLowerCase();
    for (const [k,v] of Object.entries(PLACE_COORDS)) {
        if (k.toLowerCase() === sl) return v;
    }
    for (const [k,v] of Object.entries(PLACE_COORDS)) {
        if (sl.includes(k.toLowerCase()) || k.toLowerCase().includes(sl)) return v;
    }
    return null;
}

/* ====================================================================
   LINEAGE BFS
   ==================================================================== */
function isDescendantOf(name, ancestor) {
    if (name === ancestor) return true;
    const visited = new Set(), queue = [name];
    while (queue.length) {
        const cur = queue.shift();
        if (visited.has(cur)) continue;
        visited.add(cur);
        const p = people[cur]; if (!p) continue;
        if (p.father === ancestor || p.mother === ancestor) return true;
        if (p.father) queue.push(p.father);
        if (p.mother) queue.push(p.mother);
    }
    return false;
}

/* ====================================================================
   MAP
   ==================================================================== */
let map, tileLight, tileDark, clusterGroup;
let allMarkers = [];
let activeLineage = "all", activeGender = "all";

function makeIcon(gender) {
    const isF = gender.toLowerCase() === "f";
    const fill   = isF ? "#e879a0" : "#3b82f6";
    const stroke = isF ? "#be185d" : "#1d4ed8";
    return L.divIcon({
        html: '<div class="cmark"><svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 22 22"><circle cx="11" cy="11" r="9" fill="' + fill + '" stroke="' + stroke + '" stroke-width="2" opacity="0.92"/></svg></div>',
        className: '',
        iconSize: [22,22], iconAnchor: [11,11]
    });
}

function buildMarkers() {
    clusterGroup.clearLayers();
    allMarkers = [];
    Object.values(people).forEach(p => {
        const coords = resolveCoords(p.birthPlace);
        if (!coords) return;
        const lat = coords[0] + (Math.random()-0.5)*0.05;
        const lng = coords[1] + (Math.random()-0.5)*0.05;
        const marker = L.marker([lat,lng], { icon: makeIcon(p.gender||"M") });
        marker.on("click", e => { L.DomEvent.stopPropagation(e); openFicha(p); });
        allMarkers.push({ marker, person: p });
    });
    updateFilters();
}

function updateFilters() {
    clusterGroup.clearLayers();
    let count = 0;
    allMarkers.forEach(({ marker, person: p }) => {
        const gOk = activeGender === "all"
            || (activeGender === "M" && (p.gender||"M").toLowerCase()==="m")
            || (activeGender === "F" && (p.gender||"M").toLowerCase()==="f");
        const lOk = activeLineage === "all" || isDescendantOf(p.name, activeLineage);
        if (gOk && lOk) { clusterGroup.addLayer(marker); count++; }
    });
    document.getElementById("markerCount").textContent = count;
}

function setLineage(lineage, btn) {
    activeLineage = lineage;
    document.querySelectorAll(".f-pill").forEach(el => el.classList.remove("active"));
    btn.classList.add("active");
    updateFilters();
}
function setGender(g) {
    activeGender = g;
    document.getElementById("gAll").className = "g-btn" + (g==="all"?" active-all":"");
    document.getElementById("gM").className   = "g-btn" + (g==="M"  ?" active-m"  :"");
    document.getElementById("gF").className   = "g-btn" + (g==="F"  ?" active-f"  :"");
    updateFilters();
}

/* ====================================================================
   FICHA PANEL
   ==================================================================== */
function openFicha(p) {
    const isF = (p.gender||"M").toLowerCase()==="f";
    document.getElementById("fichaDot").style.background   = isF ? "var(--f-dot)" : "var(--m-dot)";
    document.getElementById("fichaName").textContent       = p.name;
    document.getElementById("fichaGender").textContent     = isF ? "\u2640 Femenino" : "\u2642 Masculino";
    document.getElementById("fichaPlace").textContent      = p.birthPlace || "\u2014";
    document.getElementById("fichaFather").textContent     = p.father || "\u2014";
    document.getElementById("fichaMother").textContent     = p.mother || "\u2014";
    document.getElementById("fichaFatherRow").style.display = p.father ? "flex" : "none";
    document.getElementById("fichaMotherRow").style.display = p.mother ? "flex" : "none";
    const notes = (p.notes||"").trim();
    const ne = document.getElementById("fichaNotes");
    if (notes) { ne.textContent = notes.length > 200 ? notes.slice(0,200)+"..." : notes; ne.style.display="block"; }
    else { ne.style.display="none"; }
    document.getElementById("fichaLink").href = "visor_genealogia.html?name=" + encodeURIComponent(p.name);
    const panel = document.getElementById("fichaPanel");
    panel.style.display = "block";
    panel.style.animation = "none"; void panel.offsetHeight; panel.style.animation = "";
}
function closeFicha() { document.getElementById("fichaPanel").style.display="none"; }

/* ====================================================================
   THEME
   ==================================================================== */
let isDark = false;
function applyTheme(t) {
    isDark = t==="dark";
    document.documentElement.setAttribute("data-theme", t);
    document.getElementById("sunIcon").style.display  = isDark?"block":"none";
    document.getElementById("moonIcon").style.display = isDark?"none":"block";
    if (map) {
        if (isDark) { map.removeLayer(tileLight); map.addLayer(tileDark);  }
        else        { map.removeLayer(tileDark);  map.addLayer(tileLight); }
    }
}

/* ====================================================================
   INIT
   ==================================================================== */
window.addEventListener("DOMContentLoaded", () => {
    // Theme (before map so tile is correct from the start)
    const saved = localStorage.getItem("theme")||"light";
    isDark = saved==="dark";
    document.documentElement.setAttribute("data-theme", saved);
    document.getElementById("sunIcon").style.display  = isDark?"block":"none";
    document.getElementById("moonIcon").style.display = isDark?"none":"block";
    document.getElementById("themeToggle").addEventListener("click", () => {
        const next = isDark?"light":"dark";
        localStorage.setItem("theme", next); applyTheme(next);
    });

    // Map
    map = L.map("map", { center:[32,35], zoom:5 });

    tileLight = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '\u00a9 <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    });
    tileDark = L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
        attribution: '\u00a9 <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors \u00a9 <a href="https://carto.com/">CARTO</a>',
        maxZoom: 19
    });
    (isDark ? tileDark : tileLight).addTo(map);

    clusterGroup = L.markerClusterGroup({
        showCoverageOnHover: false,
        maxClusterRadius: 50,
        spiderfyOnMaxZoom: true,
        disableClusteringAtZoom: 10,
        iconCreateFunction(cluster) {
            const c = cluster.getChildCount();
            const sz = c<10?34:c<50?40:48;
            return L.divIcon({
                html: '<div style="width:'+sz+'px;height:'+sz+'px;border-radius:50%;background:rgba(59,130,246,.18);border:2.5px solid rgba(59,130,246,.6);display:flex;align-items:center;justify-content:center;font-size:'+(c<10?12:11)+'px;font-weight:700;color:#1d4ed8;font-family:Inter,sans-serif">'+c+'</div>',
                className:'', iconSize:[sz,sz], iconAnchor:[sz/2,sz/2]
            });
        }
    });
    map.addLayer(clusterGroup);
    map.on("click", () => closeFicha());

    // Build data after a brief timeout (genealogia_data.js may be large)
    setTimeout(() => {
        buildRelationshipMap();
        buildMarkers();
        document.getElementById("spinner").style.display = "none";
    }, 150);
});
</script>
</body>
</html>"""

with open('mapa_geografico.html', 'w', encoding='utf-8') as f:
    f.write(html)

lines = html.count('\n') + 1
print(f"WRITTEN: {lines} lines")
