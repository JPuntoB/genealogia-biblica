import re
import csv
import sys

# Paths
input_file = "Ase.txt"
csv_output = "genealogia_organizada.csv"
tsv_output = "genealogia_organizada.tsv"
xlsx_output = "genealogia_organizada.xlsx"

# Internal Knowledge Base for Biblical Patriarchs and Figures
patriarch_data = {
    "Adam": {
        "lugar": "Edén",
        "significado": "Hombre, hecho de tierra roja",
        "cruzada": "Génesis 1:26-27, 2:7, 5:1-5; Lucas 3:38; Romanos 5:12-21",
        "adicional": "Primer ser humano creado por Dios en el relato del Génesis. Representa el inicio de la humanidad."
    },
    "Eva": {
        "lugar": "Edén",
        "significado": "Madre de todos los vivientes / Dadora de vida",
        "cruzada": "Génesis 2:21-25, 3:1-20, 4:1-2; 2 Corintios 11:3; 1 Timoteo 2:13",
        "adicional": "Primera mujer, esposa de Adam. Creada de su costilla para ser su compañera."
    },
    "Set": {
        "lugar": "Fuera del Edén",
        "significado": "Sustituto, designado",
        "cruzada": "Génesis 4:25-26, 5:3-8; Lucas 3:38",
        "adicional": "Hijo de Adam y Eva, nacido después del asesinato de Abel por Caín. Heredero de la línea mesiánica."
    },
    "Enós": {
        "lugar": "Tierra de Nod / Canaán",
        "significado": "Mortal, débil, hombre",
        "cruzada": "Génesis 4:26, 5:6-11; Lucas 3:38",
        "adicional": "Hijo de Set; durante sus días se comenzó a invocar públicamente el nombre de YAHVÉ."
    },
    "Cainán": {
        "lugar": "Canaán",
        "significado": "Adquisición, posesión o nido",
        "cruzada": "Génesis 5:9-14; Lucas 3:37",
        "adicional": "Patriarca antediluviano, hijo de Enós y padre de Mahalaleel."
    },
    "Mahalaleel": {
        "lugar": "Canaán",
        "significado": "Alabanza de Dios / Resplandor de Dios",
        "cruzada": "Génesis 5:12-17; Lucas 3:37",
        "adicional": "Hijo de Cainán, ancestro antediluviano en la genealogía que conduce a Noé."
    },
    "Jared": {
        "lugar": "Canaán",
        "significado": "Descenso o el que desciende",
        "cruzada": "Génesis 5:15-20; Lucas 3:37",
        "adicional": "Hijo de Mahalaleel y padre de Enoc. Vivió 962 años."
    },
    "Enoc": {
        "lugar": "Canaán",
        "significado": "Consagrado, dedicado o iniciado",
        "cruzada": "Génesis 5:18-24; Hebreos 11:5; Judas 1:14-15; Lucas 3:37",
        "adicional": "Caminó con Dios íntimamente y no vio muerte, pues Dios se lo llevó al cielo directamente."
    },
    "Matusalén": {
        "lugar": "Canaán",
        "significado": "Hombre de la jabalina / Cuando él muera se enviará",
        "cruzada": "Génesis 5:21-27; Lucas 3:37",
        "adicional": "Hijo de Enoc y abuelo de Noé; es el ser humano más longevo registrado en la Biblia (969 años)."
    },
    "Lamec": {
        "lugar": "Canaán",
        "significado": "Poderoso, fuerte o el que rebaja",
        "cruzada": "Génesis 5:25-31; Lucas 3:36",
        "adicional": "Hijo de Matusalén y padre de Noé. Profetizó sobre el descanso que traería su hijo."
    },
    "Noé": {
        "lugar": "Mesopotamia",
        "significado": "Descanso, alivio o consuelo",
        "cruzada": "Génesis 5:28-32, Caps 6-9; Mateo 24:37-39; Hebreos 11:7; 1 Pedro 3:20; 2 Pedro 2:5; Lucas 3:36",
        "adicional": "Construyó el Arca para salvar a su familia y a la creación terrestre del Diluvio universal."
    },
    "Sem": {
        "lugar": "Mesopotamia",
        "significado": "Nombre, renombre o fama",
        "cruzada": "Génesis 5:32, 9:26-27, 10:21-31, 11:10-11; Lucas 3:36",
        "adicional": "Hijo de Noé; de su linaje provienen los pueblos semitas y la línea de la promesa."
    },
    "Cam": {
        "lugar": "Mesopotamia",
        "significado": "Caliente, cálido o quemado",
        "cruzada": "Génesis 5:32, 9:22-25, 10:6-20",
        "adicional": "Hijo de Noé; padre de Cus, Mizraim, Fut y Canaán, ancestro de pueblos africanos y cananeos."
    },
    "Jafet": {
        "lugar": "Mesopotamia",
        "significado": "Que él ensanche o bello",
        "cruzada": "Génesis 5:32, 9:27, 10:2-5",
        "adicional": "Hijo de Noé; ancestro de los pueblos europeos y de Asia Menor (indoeuropeos)."
    },
    "Arfaxad": {
        "lugar": "Mesopotamia",
        "significado": "Fortaleza o sanador",
        "cruzada": "Génesis 11:10-13, 10:22; Lucas 3:36",
        "adicional": "Hijo de Sem, nacido dos años después del Diluvio."
    },
    "Sala": {
        "lugar": "Mesopotamia",
        "significado": "Brote, retoño o enviado",
        "cruzada": "Génesis 11:12-15, 10:24; Lucas 3:35",
        "adicional": "Hijo de Arfaxad y padre de Heber."
    },
    "Heber": {
        "lugar": "Mesopotamia",
        "significado": "El que cruza / Del otro lado",
        "cruzada": "Génesis 11:14-17, 10:24-25; Lucas 3:35",
        "adicional": "Ancestro epónimo de los hebreos, hijo de Sala."
    },
    "Peleg": {
        "lugar": "Mesopotamia",
        "significado": "División o canal",
        "cruzada": "Génesis 11:16-19, 10:25; Lucas 3:35",
        "adicional": "Hijo de Heber; llamado así porque en sus días la población de la tierra fue dividida (Torre de Babel)."
    },
    "Reu": {
        "lugar": "Mesopotamia",
        "significado": "Amigo, compañero o pastor",
        "cruzada": "Génesis 11:18-21; Lucas 3:35",
        "adicional": "Hijo de Peleg y antepasado directo de Abraham."
    },
    "Serug": {
        "lugar": "Mesopotamia",
        "significado": "Rama, brote o entrelazado",
        "cruzada": "Génesis 11:20-23; Lucas 3:35",
        "adicional": "Hijo de Reu y bisabuelo de Abraham."
    },
    "Nacor": {
        "lugar": "Ur de los Caldeos",
        "significado": "Resoplador, jadeante",
        "cruzada": "Génesis 11:22-25; Lucas 3:34",
        "adicional": "Hijo de Serug y abuelo del patriarca Abraham."
    },
    "Taré": {
        "lugar": "Ur de los Caldeos",
        "significado": "Retraso o cabra montés",
        "cruzada": "Génesis 11:24-32; Josué 24:2; Lucas 3:34",
        "adicional": "Padre de Abraham, Nacor y Harán; salió de Ur con su familia rumbo a Canaán, muriendo en Harán."
    },
    "Abraham": {
        "lugar": "Ur de los Caldeos",
        "significado": "Padre de una multitud",
        "cruzada": "Génesis 11:26 a 25:10; Romanos 4; Gálatas 3; Lucas 3:34; Mateo 1:1-2",
        "adicional": "Padre de la fe y progenitor del pueblo de Israel y de los árabes; recibió la promesa divina del pacto."
    },
    "Isaac": {
        "lugar": "Beerseba",
        "significado": "Él reirá / Risa",
        "cruzada": "Génesis 21 a 35; Gálatas 4:21-31; Hebreos 11:20; Mateo 1:2",
        "adicional": "Hijo de la promesa nacido de Abraham y Sara en su vejez extrema; padre de Jacob y Esaú."
    },
    "Esaú": {
        "lugar": "Canaán",
        "significado": "Velludo o hecho",
        "cruzada": "Génesis 25:21-34, Cap 27, Cap 36; Romanos 9:13; Hebreos 12:16-17",
        "adicional": "Hijo primogénito de Isaac y Rebeca; vendió su primogenitura por comida y fundó la nación de Edom."
    },
    "Israel": {
        "lugar": "Canaán",
        "significado": "El que lucha con Dios / Príncipe de Dios",
        "cruzada": "Génesis 25:21 a 49:33; Oseas 12:3-4; Mateo 1:2",
        "adicional": "Nombre dado a Jacob tras su lucha con el ángel en Peniel; sus doce hijos fundaron las 12 tribus."
    },
    "Rubén": {
        "lugar": "Padan-aram",
        "significado": "¡He aquí un hijo!",
        "cruzada": "Génesis 29:32, 35:22, 49:3-4",
        "adicional": "Hijo primogénito de Jacob y Lea; perdió sus derechos de primogenitura por profanar el lecho de su padre."
    },
    "Simeón": {
        "lugar": "Padan-aram",
        "significado": "Dios ha oído",
        "cruzada": "Génesis 29:33, 34:25-30, 49:5-7",
        "adicional": "Segundo hijo de Jacob y Lea; lideró la venganza contra Siquem junto a Leví."
    },
    "Leví": {
        "lugar": "Padan-aram",
        "significado": "Unido, asociado o de mi mano",
        "cruzada": "Génesis 29:34, 49:5-7; Éxodo 2; Hebreos 7",
        "adicional": "Tercer hijo de Jacob y Lea; su descendencia fue apartada exclusivamente para el servicio del templo."
    },
    "Judá": {
        "lugar": "Padan-aram",
        "significado": "Alabado sea Dios / Celebrado",
        "cruzada": "Génesis 29:35, Cap 38, Cap 44, 49:8-12; Hebreos 7:14; Apocalipsis 5:5; Mateo 1:2-3",
        "adicional": "Cuarto hijo de Jacob y Lea; de su línea proviene el rey David y Jesucristo (el León de la tribu de Judá)."
    },
    "José": {
        "lugar": "Padan-aram",
        "significado": "Que él añada / YAHVÉ añadirá",
        "cruzada": "Génesis 30:22-24, Caps 37-50; Salmo 105:17-22; Hebreos 11:21-22",
        "adicional": "Hijo predilecto de Jacob y Raquel; vendido por sus hermanos, llegó a ser gobernante y salvador de Egipto."
    },
    "Benjamín": {
        "lugar": "Canaán (cerca de Belén)",
        "significado": "Hijo de mi mano derecha / Hijo de mi dolor",
        "cruzada": "Génesis 35:16-18, 49:27; Romanos 11:1; Filipenses 3:5",
        "adicional": "Hijo menor de Jacob y Raquel, quien falleció en el parto llamándolo Benoni."
    },
    "Caleb": {
        "lugar": "Egipto",
        "significado": "Perro, audaz, impetuoso o fiel",
        "cruzada": "Números 13:6, 14:24-38; Josué 14:6-15",
        "adicional": "Espía fiel de la tribu de Judá que confió en Dios; recibió Hebrón como herencia por su fe."
    },
    "David": {
        "lugar": "Belén",
        "significado": "Amado",
        "cruzada": "1 Samuel 16 a 1 Reyes 2; Mateo 1:6, 22:42-45; Lucas 1:32; Hechos 2:29-36",
        "adicional": "Segundo rey de Israel; pastor, músico, poeta, unificador nacional y escritor de la mayoría de los Salmos."
    },
    "Salomón": {
        "lugar": "Jerusalén",
        "significado": "Pacífico / Paz",
        "cruzada": "2 Samuel 12:24-25; 1 Reyes 1 a 11; 2 Crónicas 1 a 9; Mateo 6:29, 12:42",
        "adicional": "Hijo de David y Betsabé; tercer rey de Israel, constructor del Templo y famoso por su riqueza y sabiduría."
    },
    "Moisés": {
        "lugar": "Egipto (Gosén)",
        "significado": "Sacado de las aguas / Hijo",
        "cruzada": "Libros de Éxodo a Deuteronomio; Hebreos 11:23-29; Mateo 17:3; Juan 1:17",
        "adicional": "Profeta y libertador de Israel; condujo el Éxodo a través del Mar Rojo y recibió la Ley en el Sinaí."
    },
    "Aarón": {
        "lugar": "Egipto",
        "significado": "Montañés, excelso o ilustre",
        "cruzada": "Éxodo 4 a 40; Levítico 8; Números 20:22-29; Hebreos 5:4",
        "adicional": "Hermano mayor de Moisés y primer Sumo Sacerdote consagrado de Israel."
    },
    "Miriam": {
        "lugar": "Egipto",
        "significado": "Rebelión, amada o gota de mar",
        "cruzada": "Éxodo 2:4-10, 15:20-21; Números 12; Miqueas 6:4",
        "adicional": "Hermana mayor de Moisés y Aarón; profetisa que lideró el canto de victoria en el cruce del Mar Rojo."
    },
    "Josué": {
        "lugar": "Egipto",
        "significado": "YAHVÉ es salvación",
        "cruzada": "Éxodo 17:9, Números 27:18-23; Libro de Josué; Hebreos 4:8",
        "adicional": "Sucesor de Moisés; comandó militarmente la conquista de Canaán y el reparto de la tierra."
    }
}

def clean_name(name):
    if not name:
        return ""
    
    # Specific known fixes
    name_clean = name.strip()
    name_lower = name_clean.lower()
    if name_lower.startswith("david que le"):
        return "David"
    if name_lower.startswith("aarón son estos") or name_lower.startswith("aaron son estos"):
        return "Aarón"
        
    # Remove leading articles or prepositions
    name_clean = re.sub(r'^(y|el|la|los|las|de|ben|hijo de|hijos de|hija de|a|al|del)\s+', '', name_clean, flags=re.IGNORECASE)
    # Remove trailing descriptors
    name_clean = re.sub(r'\s+(ben|hijo|hijos|padre|madre|su\s+hermana|hermana|primogénito|segundo|tercero|cuarto|quinto|sexto|séptimo|octavo|noveno|décimo|su\s+mujer|mujer|concubina|su\s+nuera|nuera)\b.*', '', name_clean, flags=re.IGNORECASE)
    
    # Remove descriptive clauses
    name_clean = re.sub(r'\s+que\s+le\s+nacieron.*', '', name_clean, flags=re.IGNORECASE)
    name_clean = re.sub(r'\s+son\s+estos.*', '', name_clean, flags=re.IGNORECASE)
    
    # Clean whitespace and symbols (including stray semicolons)
    name_clean = name_clean.strip(",.; \t\n()\"'")
    return name_clean

def get_gender(name, context_text=""):
    context_text = context_text.lower()
    name_lower = name.lower()
    if "hermana" in context_text or "hija" in context_text:
        return "F"
    
    female_names = {
        "eva", "tamar", "sarvia", "abigail", "azuba", "efrata", "atara", 
        "abihail", "maaca", "acsa", "betsabé", "selomit", "haze-lelponi", 
        "hela", "naara", "bitia", "jehudaía", "seera", "sera", "hodes", 
        "husim", "baara", "abías"
    }
    if name_lower in female_names:
        if name_lower == "abías" and "mujer" not in context_text:
            return "M"
        return "F"
    return "M"

def preprocess_text(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        
    joined_lines = []
    current_line = ""
    
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        
        # Remove line numbers if they exist
        stripped = re.sub(r'^\d+:\s*', '', stripped)
        
        if current_line:
            if (current_line.endswith(",") or 
                current_line.endswith(";") or 
                current_line.endswith(":") or
                current_line.endswith(" y") or 
                current_line.endswith(" e") or
                stripped[0].islower() or
                re.match(r'^(el segundo|el tercero|el cuarto|el quinto|el sexto|el séptimo|el octavo|el noveno|el décimo|primogénito|segundo|tercero|cuarto|quinto|sexto|séptimo)\b', stripped, re.IGNORECASE)):
                current_line += " " + stripped
            else:
                joined_lines.append(current_line)
                current_line = stripped
        else:
            current_line = stripped
            
    if current_line:
        joined_lines.append(current_line)
        
    sentences = []
    for line in joined_lines:
        parts = re.split(r'\.(?=\s+[A-ZÁÉÍÓÚ]|$)', line)
        for part in parts:
            part = part.strip()
            if part:
                sentences.append(part)
                
    return sentences

def get_bible_reference(line_num, parent_name=None, child_name=None):
    # Determine the base chapter based on Ase.txt lines
    if line_num <= 42:
        chap = "1 Crónicas 1"
    elif line_num <= 97:
        chap = "1 Crónicas 2"
    elif line_num <= 121:
        chap = "1 Crónicas 3"
    elif line_num <= 164:
        chap = "1 Crónicas 4"
    elif line_num <= 190:
        chap = "1 Crónicas 5"
    elif line_num <= 271:
        chap = "1 Crónicas 6"
    elif line_num <= 311:
        chap = "1 Crónicas 7"
    elif line_num <= 351:
        chap = "1 Crónicas 8"
    else:
        chap = "1 Crónicas 9"
        
    # Append cross references if available
    cross_refs = []
    if parent_name and parent_name in patriarch_data and patriarch_data[parent_name].get("cruzada"):
        cross_refs.append(f"{parent_name}: {patriarch_data[parent_name]['cruzada']}")
    if child_name and child_name in patriarch_data and patriarch_data[child_name].get("cruzada"):
        if child_name != parent_name:
            cross_refs.append(f"{child_name}: {patriarch_data[child_name]['cruzada']}")
            
    if cross_refs:
        ref_str = f"{chap} [Cruces: {'; '.join(cross_refs)}]"
    else:
        ref_str = chap
        
    return ref_str

def enrich_record(record, orig_line_num):
    father = record["Padre"]
    mother = record["Madre"]
    child = record["Hijos"]
    
    # 1. Lugar de nacimiento: check child first, then father
    lugar = ""
    if child in patriarch_data and patriarch_data[child].get("lugar"):
        lugar = patriarch_data[child]["lugar"]
    elif father in patriarch_data and patriarch_data[father].get("lugar"):
        lugar = f"{patriarch_data[father]['lugar']} (padre)"
        
    # 2. Significado del nombre (Padre)
    significado_padre = ""
    if father in patriarch_data and patriarch_data[father].get("significado"):
        significado_padre = patriarch_data[father]["significado"]
        
    # 3. Referencias y referencias cruzadas
    referencia = get_bible_reference(orig_line_num, father, child)
    
    # 4. Información adicional
    adicional_list = []
    if father in patriarch_data and patriarch_data[father].get("adicional"):
        adicional_list.append(f"Sobre el padre ({father}): {patriarch_data[father]['adicional']}")
    if child in patriarch_data and patriarch_data[child].get("adicional"):
        adicional_list.append(f"Sobre el hijo ({child}): {patriarch_data[child]['adicional']}")
    
    info_adicional = " | ".join(adicional_list)
    
    # Add new fields to the record
    record["Lugar de nacimiento"] = lugar
    record["Significado del Nombre (Padre)"] = significado_padre
    record["Referencia"] = referencia
    record["Información Adicional"] = info_adicional
    
    return record

def parse_genealogy(sentences):
    records = []
    last_father = ""
    last_mother = ""
    
    ordinals = {
        "primogénito": 1, "primero": 1, "segundo": 2, "tercero": 3,
        "cuarto": 4, "quinto": 5, "sexto": 6, "séptimo": 7,
        "octavo": 8, "noveno": 9, "décimo": 10
    }

    for idx, text in enumerate(sentences):
        line_num = idx + 1
        
        # We need to approximate the original line number in Ase.txt for reference mapping
        # Since Ase.txt has 373 lines and sentences has 300, we map line_num to original index roughly
        # Or even better: we can keep track of line numbers in the preprocessor.
        # But a simple mapping based on sentence index works well enough, or we can use the notes number!
        # The notes in previous parse had "Sentencia X" or "Línea Y".
        # Let's write a simple regex on the text to find which chapter it is, or pass the index of the sentence
        # Actually, let's map sentence index linearly to line number:
        orig_line_num = int(line_num * (373 / 300))
        
        # 1. Pattern: "Hijos de X:" or "Los hijos de X:" or "Las familias de X:"
        hijos_de_match = re.search(r'(?:Hijos|Los hijos|Las familias|La heredad y habitación) de ([A-ZÁÉÍÓÚ][a-zA-ZñáéíóúüÁÉÍÓÚ\s]+?):\s*(.*)', text, re.IGNORECASE)
        if hijos_de_match:
            parent = clean_name(hijos_de_match.group(1))
            children_text = hijos_de_match.group(2)
            children_text = children_text.split(".")[0]
            
            children_raw = re.split(r',| y | e ', children_text)
            child_order = 1
            for child_raw in children_raw:
                child_clean = clean_name(child_raw)
                if not child_clean:
                    continue
                
                order = ""
                for ord_word, ord_num in ordinals.items():
                    if ord_word in child_raw.lower():
                        order = ord_num
                        break
                if not order:
                    order = child_order
                    child_order += 1
                
                gender = get_gender(child_clean, child_raw)
                
                mother = ""
                if "el de" in child_raw.lower() or "hijo de" in child_raw.lower():
                    m_match = re.search(r'(?:el de|de|hijo de)\s+([A-ZÁÉÍÓÚ][a-zñáéíóú]+)', child_raw, re.IGNORECASE)
                    if m_match:
                        potential_mother = clean_name(m_match.group(1))
                        if get_gender(potential_mother) == "F":
                            mother = potential_mother
                
                rec = {
                    "Padre": parent if get_gender(parent) == "M" else last_father,
                    "Madre": parent if get_gender(parent) == "F" else mother,
                    "Hijos": child_clean,
                    "Orden de Nacimiento": order,
                    "Género Hijos": gender,
                    "Notas": f"Sentencia {line_num}: {text[:100]}"
                }
                records.append(enrich_record(rec, orig_line_num))
            
            if get_gender(parent) == "M":
                last_father = parent
            else:
                last_mother = parent
            continue

        # 2. Pattern: "X engendró a Y"
        if "engendró" in text.lower():
            matches = list(re.finditer(r'([A-ZÁÉÍÓÚ][a-zñáéíóú\s]+?)\s+engendró\s+a\s+([A-ZÁÉÍÓÚ][a-zñáéíóú\s]+?)(?:\s+de\s+su\s+mujer\s+([A-ZÁÉÍÓÚ][a-zñáéíóú]+))?(?=\s+y|\s+e|,\s*[A-ZÁÉÍÓÚ]|\.|$)', text, re.IGNORECASE))
            if len(matches) > 1:
                for match in matches:
                    father = clean_name(match.group(1))
                    child = clean_name(match.group(2))
                    mother = clean_name(match.group(3)) if match.group(3) else ""
                    rec = {
                        "Padre": father,
                        "Madre": mother,
                        "Hijos": child,
                        "Orden de Nacimiento": "",
                        "Género Hijos": get_gender(child, text),
                        "Notas": f"Sentencia {line_num}: {text[:100]}"
                    }
                    records.append(enrich_record(rec, orig_line_num))
                continue
            elif len(matches) == 1:
                match = matches[0]
                father = clean_name(match.group(1))
                first_child = clean_name(match.group(2))
                mother = clean_name(match.group(3)) if match.group(3) else ""
                
                rec = {
                    "Padre": father,
                    "Madre": mother,
                    "Hijos": first_child,
                    "Orden de Nacimiento": 1 if "primogénito" in text.lower() else "",
                    "Género Hijos": get_gender(first_child, text),
                    "Notas": f"Sentencia {line_num}: {text[:100]}"
                }
                records.append(enrich_record(rec, orig_line_num))
                
                additional_children = re.findall(r'(?:el|la)?\s*(segundo|tercero|cuarto|quinto|sexto|séptimo|octavo|noveno|décimo)\s+([A-ZÁÉÍÓÚ][a-zñáéíóú]+)', text, re.IGNORECASE)
                for ord_word, child_name in additional_children:
                    child_clean = clean_name(child_name)
                    order = ordinals.get(ord_word.lower(), "")
                    rec = {
                        "Padre": father,
                        "Madre": mother,
                        "Hijos": child_clean,
                        "Orden de Nacimiento": order,
                        "Género Hijos": get_gender(child_clean, ord_word),
                        "Notas": f"Sentencia {line_num}: {text[:100]}"
                    }
                    records.append(enrich_record(rec, orig_line_num))
                
                sisters_match = re.search(r'fueron\s+hermanas\s+de\s+ellos|de\s+los\s+cuales\s+([A-ZÁÉÍÓÚ][a-zñáéíóú\s,ye]+)\s+fueron\s+hermanas', text, re.IGNORECASE)
                if sisters_match:
                    sisters_names_text = sisters_match.group(1) if sisters_match.group(1) else ""
                    if sisters_names_text:
                        sisters_raw = re.split(r',| y | e ', sisters_names_text)
                        for sis_raw in sisters_raw:
                            sis_clean = clean_name(sis_raw)
                            if sis_clean:
                                rec = {
                                    "Padre": father,
                                    "Madre": mother,
                                    "Hijos": sis_clean,
                                    "Orden de Nacimiento": "",
                                    "Género Hijos": "F",
                                    "Notas": f"Sentencia {line_num}: Hermana de los hijos de {father}"
                                }
                                records.append(enrich_record(rec, orig_line_num))
                last_father = father
                if mother:
                    last_mother = mother
                continue

        # 3. Pattern: "X dio a luz a Y" or "dio a luz a Y... cuyo padre fue Z"
        dio_luz_match = re.search(r'([A-ZÁÉÍÓÚ][a-zñáéíóúü]+(?:\s+(?:su\s+)?(?:nuera|concubina|mujer|hermana))?)\s*,?\s*(?:[dD]io\s+a\s+luz\s+a|[fF]ue\s+madre\s+de)\s+([A-ZÁÉÍÓÚa-zA-ZñáéíóúüÁÉÍÓÚ\s,ye]+?)(?=\s+cuyo|\s+padre|\.|$)', text)
        if dio_luz_match:
            mother = clean_name(dio_luz_match.group(1))
            children_text = dio_luz_match.group(2)
            
            father = last_father
            father_match = re.search(r'padre\s+de\s+[^,.]+?\s+fue\s+([A-ZÁÉÍÓÚ][a-zñáéíóú]+)|cuyo\s+padre\s+fue\s+([A-ZÁÉÍÓÚ][a-zñáéíóú]+)|concubina\s+de\s+([A-ZÁÉÍÓÚ][a-zñáéíóú]+)|mujer\s+de\s+([A-ZÁÉÍÓÚ][a-zñáéíóú]+)', text, re.IGNORECASE)
            if father_match:
                father = clean_name(next(item for item in father_match.groups() if item is not None))
                
            children_raw = re.split(r',| y | e ', children_text)
            for i, child_raw in enumerate(children_raw):
                child_clean = clean_name(child_raw)
                if not child_clean:
                    continue
                gender = get_gender(child_clean, child_raw)
                rec = {
                    "Padre": father,
                    "Madre": mother,
                    "Hijos": child_clean,
                    "Orden de Nacimiento": i + 1,
                    "Género Hijos": gender,
                    "Notas": f"Sentencia {line_num}: {text[:100]}"
                }
                records.append(enrich_record(rec, orig_line_num))
            last_mother = mother
            if father:
                last_father = father
            continue

        # 4. Pattern: "A, hijo de B" or "A fue hijo de B"
        hijo_de_match = re.search(r'([A-ZÁÉÍÓÚ][a-zñáéíóúü]+(?:\s+ben\s+[A-ZÁÉÍÓÚ][a-zñáéíóúü]+)?)\s+(?:fue\s+)?hijo\s+de\s+([A-ZÁÉÍÓÚ][a-zñáéíóú]+)', text, re.IGNORECASE)
        if hijo_de_match:
            child = clean_name(hijo_de_match.group(1))
            parent = clean_name(hijo_de_match.group(2))
            gender = get_gender(child, text)
            rec = {
                "Padre": parent if get_gender(parent) == "M" else last_father,
                "Madre": parent if get_gender(parent) == "F" else last_mother,
                "Hijos": child,
                "Orden de Nacimiento": "",
                "Género Hijos": gender,
                "Notas": f"Sentencia {line_num}: {text[:100]}"
            }
            records.append(enrich_record(rec, orig_line_num))
            continue

        # 5. Pattern: "A, padre de B"
        padre_de_match = re.search(r'([A-ZÁÉÍÓÚ][a-zñáéíóúü]+)\s*,\s*padre\s+de\s+([A-ZÁÉÍÓÚ][a-zñáéíóúü]+)', text, re.IGNORECASE)
        if padre_de_match:
            father = clean_name(padre_de_match.group(1))
            child = clean_name(padre_de_match.group(2))
            gender = get_gender(child, text)
            rec = {
                "Padre": father,
                "Madre": "",
                "Hijos": child,
                "Orden de Nacimiento": "",
                "Género Hijos": gender,
                "Notas": f"Sentencia {line_num}: {text[:100]}"
            }
            records.append(enrich_record(rec, orig_line_num))
            last_father = father
            continue

        # 6. Pattern: Simple list of names with no verbs
        if not re.search(r'\b(engendró|reinó|fue|fueron|hijos|hijo|padre|madre|mujer|concubina|nació|nacieron|luz|muerto|muerta)\b', text, re.IGNORECASE):
            names_raw = re.split(r',| y | e ', text)
            names = [clean_name(n) for n in names_raw if clean_name(n)]
            sibling_match = re.search(r'\b(?:y|e)\s+([A-ZÁÉÍÓÚ][a-zñáéíóú]+)', text, re.IGNORECASE)
            
            if len(names) >= 2:
                if sibling_match:
                    if "Noé" in names:
                        father_idx = names.index("Noé")
                        father = names[father_idx]
                        siblings = names[father_idx+1:]
                        for i in range(father_idx):
                            rec = {
                                "Padre": names[i],
                                "Madre": "",
                                "Hijos": names[i+1],
                                "Orden de Nacimiento": "",
                                "Género Hijos": "M",
                                "Notas": f"Sentencia {line_num}: Linaje de {names[i]}"
                            }
                            records.append(enrich_record(rec, orig_line_num))
                        for idx_sib, sib in enumerate(siblings):
                            rec = {
                                "Padre": father,
                                "Madre": "",
                                "Hijos": sib,
                                "Orden de Nacimiento": idx_sib + 1,
                                "Género Hijos": "M",
                                "Notas": f"Sentencia {line_num}: Hijo de {father}"
                            }
                            records.append(enrich_record(rec, orig_line_num))
                    else:
                        if len(names) >= 3:
                            father = names[-3]
                            siblings = names[-2:]
                            father_idx = names.index(father)
                            for i in range(father_idx):
                                rec = {
                                    "Padre": names[i],
                                    "Madre": "",
                                    "Hijos": names[i+1],
                                    "Orden de Nacimiento": "",
                                    "Género Hijos": "M",
                                    "Notas": f"Sentencia {line_num}: Linaje de {names[i]}"
                                }
                                records.append(enrich_record(rec, orig_line_num))
                            for idx_sib, sib in enumerate(siblings):
                                rec = {
                                    "Padre": father,
                                    "Madre": "",
                                    "Hijos": sib,
                                    "Orden de Nacimiento": idx_sib + 1,
                                    "Género Hijos": "M",
                                    "Notas": f"Sentencia {line_num}: Hijo de {father}"
                                }
                                records.append(enrich_record(rec, orig_line_num))
                        else:
                            rec = {
                                "Padre": names[0],
                                "Madre": "",
                                "Hijos": names[1],
                                "Orden de Nacimiento": 1,
                                "Género Hijos": "M",
                                "Notas": f"Sentencia {line_num}: Hijo de {names[0]}"
                            }
                            records.append(enrich_record(rec, orig_line_num))
                else:
                    for i in range(len(names) - 1):
                        rec = {
                            "Padre": names[i],
                            "Madre": "",
                            "Hijos": names[i+1],
                            "Orden de Nacimiento": "",
                            "Género Hijos": "M",
                            "Notas": f"Sentencia {line_num}: {names[i]} es padre de {names[i+1]}"
                        }
                        records.append(enrich_record(rec, orig_line_num))
                continue
                
    return records

# ─────────────────────────────────────────────────────────────────────────────
# Manual correction data — rows that the parser cannot reliably derive
# ─────────────────────────────────────────────────────────────────────────────

# Hijos de Ismael (Ase.txt líneas 17-19)
Ismael_hijos = [
    "Nebaiot", "Cedar", "Adbeel", "Mibsam",
    "Misma", "Duma", "Massa", "Hadad",
    "Tema", "Jetur", "Nafis", "Cedema"
]

# Hijos de Abraham con Cetura que el parser omite (solo registra Jocsán y Madián)
Cetura_hijos_faltantes = ["Zimram", "Medán", "Isbac", "Súa"]

# Nombres que el parser genera mal y deben eliminarse
BAD_CHILD_NAMES = {"de Timna", "Timna fue", "fue hermana", "hermana de"}

def is_bad_record(rec):
    """Returns True if the record is known-bad and should be dropped."""
    child = rec.get("Hijos", "").strip()
    # Drop stray parser artefacts
    if child in BAD_CHILD_NAMES:
        return True
    # Drop duplicate Abraham→Isaac rows (keep only the first)
    return False

def deduplicate(records):
    """Remove exact duplicate (Padre, Hijos) pairs, keeping first occurrence."""
    seen = set()
    out = []
    for rec in records:
        key = (rec["Padre"].strip(), rec["Hijos"].strip())
        if key in seen:
            continue
        seen.add(key)
        out.append(rec)
    return out

def fix_cainan_ambiguity(records):
    """
    There are TWO distinct people named Cainán:
      1. Antediluvian Cainán — son of Enós (Genesis 5:9)
      2. Post-diluvian Cainán — son of Arfaxad (Luke 3:36, Ase.txt line 12)
    Tag the post-diluvian one so the UI can distinguish them.
    """
    for rec in records:
        if rec["Hijos"].strip() == "Cainán" and rec["Padre"].strip() == "Arfaxad":
            rec["Hijos"] = "Cainán (hijo de Arfaxad)"
            rec["Notas"] = "[Distinción: Cainán post-diluviano, hijo de Arfaxad — Lucas 3:36] " + rec.get("Notas", "")
        if rec["Padre"].strip() == "Cainán" and rec["Hijos"].strip() == "Sala":
            rec["Padre"] = "Cainán (hijo de Arfaxad)"
    return records

def build_manual_records(fieldnames):
    """Build the manually-curated rows that the parser cannot generate correctly."""
    manual = []

    def make_row(padre, madre, hijo, orden, genero, lugar, ref, adicional, notas):
        r = {f: "" for f in fieldnames}
        r["Padre"] = padre
        r["Madre"] = madre
        r["Hijos"] = hijo
        r["Orden de Nacimiento"] = str(orden)
        r["Género Hijos"] = genero
        r["Lugar de nacimiento"] = lugar
        r["Referencia"] = ref
        r["Información Adicional"] = adicional
        r["Notas"] = notas
        return r

    # ── Hijos de Ismael (Ase.txt líneas 17-19) ──────────────────────────────
    ismael_info = "Sobre el padre (Ismael): Hijo de Abraham y Agar la egipcia; progenitor de doce príncipes y de los pueblos árabes."
    for i, nombre in enumerate(Ismael_hijos, start=1):
        manual.append(make_row(
            "Ismael", "", nombre, i, "M",
            "Arabia (padre)",
            "1 Crónicas 1",
            ismael_info,
            f"Hijos de Ismael — Ase.txt líneas 17-19 (corrección manual)"
        ))

    # ── Hijos de Abraham con Cetura (faltantes) ─────────────────────────────
    cetura_info = "Sobre el padre (Abraham): Padre de la fe y progenitor del pueblo de Israel y de los árabes; recibió la promesa divina del pacto."
    # Ase.txt línea 20 ordena: Zimram, Jocsán, Medán, Madián, Isbac y Súa
    orden_cetura = {"Zimram": 1, "Jocsán": 2, "Medán": 3, "Madián": 4, "Isbac": 5, "Súa": 6}
    for nombre in Cetura_hijos_faltantes:
        manual.append(make_row(
            "Abraham", "Cetura", nombre, orden_cetura[nombre], "M",
            "Ur de los Caldeos (padre)",
            "1 Crónicas 1",
            cetura_info,
            f"Hijo de Abraham y Cetura — Ase.txt línea 20 (corrección manual)"
        ))

    # ── Corrección: Amalec es hijo de Elifaz con Timna (concubina) ──────────
    manual.append(make_row(
        "Elifaz", "Timna", "Amalec", 7, "M",
        "Edom (padre)",
        "1 Crónicas 1",
        "Sobre el padre (Elifaz): Hijo primogénito de Esaú y fundador del clan edomita de Temán. | Sobre la madre (Timna): Concubina de Elifaz, hermana de Lotán horita.",
        "Hijo de Elifaz con su concubina Timna — Ase.txt línea 24 (corrección: sustituye fila 'de Timna')"
    ))

    return manual


# ── Mejoras: Detección de ciclos, estadísticas, JSON export, watch mode ──────

def detect_cycles(records):
    """
    Detecta ciclos en el grafo padre→hijo usando DFS.
    Retorna lista de ciclos encontrados (cada uno como lista de nombres).
    """
    # Construir grafo de adyacencia
    children_map = {}  # padre -> [hijos]
    for rec in records:
        padre = rec.get("Padre", "").strip()
        hijo  = rec.get("Hijos",  "").strip()
        if padre and hijo:
            children_map.setdefault(padre, []).append(hijo)

    cycles = []
    visited = set()
    rec_stack = set()
    path = []

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        for child in children_map.get(node, []):
            if child not in visited:
                if dfs(child):
                    return True
            elif child in rec_stack:
                # Encontramos un ciclo
                cycle_start = path.index(child)
                cycles.append(list(path[cycle_start:]) + [child])
        path.pop()
        rec_stack.discard(node)
        return False

    for node in list(children_map.keys()):
        if node not in visited:
            dfs(node)

    return cycles


def print_statistics(records):
    """
    Imprime un reporte de estadísticas de los datos genealógicos.
    """
    print("\n" + "=" * 60)
    print("  ESTADISTICAS DE LA GENEALOGIA BIBLICA")
    print("=" * 60)

    # Recopilar personas únicas
    people = {}
    for rec in records:
        for role, col in [("padre", "Padre"), ("madre", "Madre"), ("hijo", "Hijos")]:
            name = rec.get(col, "").strip()
            if name:
                if name not in people:
                    people[name] = {
                        "hijos": set(), "tiene_imagen": False,
                        "tiene_ref": False, "tiene_notas": False,
                        "genero": "M"
                    }
                if role == "hijo":
                    people[name]["genero"] = rec.get("Género Hijos", "M")
                    if rec.get("Referencia", "").strip():
                        people[name]["tiene_ref"] = True
                    if rec.get("Información Adicional", "").strip() or rec.get("Notas", "").strip():
                        people[name]["tiene_notas"] = True
                    if rec.get("Imagen_URL", "").strip():
                        people[name]["tiene_imagen"] = True
        padre = rec.get("Padre", "").strip()
        hijo  = rec.get("Hijos",  "").strip()
        if padre and hijo:
            people.setdefault(padre, {"hijos": set(), "tiene_imagen": False, "tiene_ref": False, "tiene_notas": False, "genero": "M"})
            people[padre]["hijos"].add(hijo)

    total = len(people)
    masculinos  = sum(1 for p in people.values() if p["genero"] != "F")
    femeninos   = total - masculinos
    con_imagen  = sum(1 for p in people.values() if p["tiene_imagen"])
    con_ref     = sum(1 for p in people.values() if p["tiene_ref"])
    con_notas   = sum(1 for p in people.values() if p["tiene_notas"])
    con_hijos   = sum(1 for p in people.values() if len(p["hijos"]) > 0)

    print(f"  Total de personas unicas : {total:>6}")
    print(f"  Masculinos               : {masculinos:>6}  ({masculinos/total*100:.1f}%)")
    print(f"  Femeninos                : {femeninos:>6}  ({femeninos/total*100:.1f}%)")
    print(f"  Con imagen asignada      : {con_imagen:>6}  ({con_imagen/total*100:.1f}%)")
    print(f"  Con referencia biblica   : {con_ref:>6}  ({con_ref/total*100:.1f}%)")
    print(f"  Con notas biograficas    : {con_notas:>6}  ({con_notas/total*100:.1f}%)")
    print(f"  Con descendientes reg.   : {con_hijos:>6}  ({con_hijos/total*100:.1f}%)")
    print(f"  Total relaciones padre-h : {len(records):>6}")

    # Top 10 con más hijos
    top10 = sorted(people.items(), key=lambda x: len(x[1]["hijos"]), reverse=True)[:10]
    print("\n  Top 10 personajes con mas hijos registrados:")
    for i, (name, data) in enumerate(top10, 1):
        bar = "#" * min(len(data["hijos"]), 30)
        print(f"   {i:>2}. {name:<30} {len(data['hijos']):>3} hijos  {bar}")

    # Detección de ciclos
    print("\n  Verificando ciclos en el grafo genealogico...")
    cycles = detect_cycles(records)
    if cycles:
        print(f"  [ALERTA] Se encontraron {len(cycles)} ciclo(s):")
        for cyc in cycles:
            print(f"     {' -> '.join(cyc)}")
    else:
        print("  OK: Sin ciclos detectados - el grafo es aciclico.")

    print("=" * 60 + "\n")


def validate_urls(records):
    """
    Verifica que las URLs en la columna 'Referencias_URLs' respondan HTTP 200.
    Requiere urllib (stdlib).
    """
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError

    url_set = set()
    for rec in records:
        for u in rec.get("Referencias_URLs", "").split("|"):
            u = u.strip()
            if u and u.startswith("http"):
                url_set.add(u)

    if not url_set:
        print("No se encontraron URLs para validar.")
        return

    print(f"Validando {len(url_set)} URLs únicas...")
    ok = bad = 0
    for url in sorted(url_set):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            code = urlopen(req, timeout=8).getcode()
            if code == 200:
                print(f"  ✅ {url}")
                ok += 1
            else:
                print(f"  ⚠️  HTTP {code}  {url}")
                bad += 1
        except (HTTPError, URLError, Exception) as e:
            print(f"  ❌ ERROR: {url}  ({e})")
            bad += 1
    print(f"\nResultado: {ok} OK, {bad} con error.")


def run_pipeline(show_stats=False, validate=False):
    """Ejecuta el pipeline completo y retorna los registros procesados."""
    import json

    print("Iniciando procesamiento mejorado de Ase.txt...")
    sentences = preprocess_text(input_file)
    print(f"Preprocesado completo: {len(sentences)} sentencias lógicas identificadas.")

    records = parse_genealogy(sentences)
    print(f"Se extrajeron {len(records)} registros genealógicos (sin filtrar).")

    # 1. Eliminar artefactos
    before = len(records)
    records = [r for r in records if not is_bad_record(r)]
    print(f"Eliminados {before - len(records)} registros con nombres incorrectos (artefactos del parser).")

    # 2. Eliminar duplicados
    before = len(records)
    records = deduplicate(records)
    print(f"Eliminados {before - len(records)} registros duplicados.")

    # 3. Resolver ambigüedad de Cainán
    records = fix_cainan_ambiguity(records)
    print("Ambigüedad de Cainán resuelta.")

    # Orden de columnas
    fieldnames = [
        "Padre", "Madre", "Hijos", "Orden de Nacimiento", "Género Hijos",
        "Lugar de nacimiento", "Significado del Nombre (Padre)",
        "Referencia", "Información Adicional", "Notas",
        "Imagen_URL", "Referencias_URLs", "Enlace_Externo"
    ]

    # 4. Añadir registros manuales
    manual_records = build_manual_records(fieldnames)
    records.extend(manual_records)
    print(f"Añadidos {len(manual_records)} registros manuales.")
    print(f"Total final: {len(records)} registros genealógicos.")

    # 5. Inyectar correcciones web si existe correcciones.json
    import os
    correcciones_file = "correcciones.json"
    if os.path.exists(correcciones_file):
        try:
            with open(correcciones_file, "r", encoding="utf-8") as jf:
                corr_data = json.load(jf)
                
            nuevos_count = 0
            if "nuevos" in corr_data and isinstance(corr_data["nuevos"], list):
                for new_rec in corr_data["nuevos"]:
                    full_rec = {f: "" for f in fieldnames}
                    full_rec.update(new_rec)
                    records.append(full_rec)
                    nuevos_count += 1
                    
            mods_count = 0
            if "modificaciones" in corr_data and isinstance(corr_data["modificaciones"], dict):
                for record in records:
                    child = record.get("Hijos", "").strip()
                    if child in corr_data["modificaciones"]:
                        mods = corr_data["modificaciones"][child]
                        
                        key_mapping = {
                            "meaning": "Significado del Nombre (Padre)",
                            "birthPlace": "Lugar de nacimiento",
                            "notes": "Notas",
                            "gender": "Género Hijos",
                            "father": "Padre",
                            "mother": "Madre"
                        }
                        
                        for js_key, py_key in key_mapping.items():
                            if js_key in mods and mods[js_key] is not None:
                                record[py_key] = mods[js_key]
                                
                        if "notes" in mods and mods["notes"] is not None:
                            record["Notas"] = mods["notes"]
                            record["Información Adicional"] = f"Sobre el hijo ({child}): {mods['notes']}"
                            
                        mods_count += 1
                        
            print(f"Inyectadas correcciones desde '{correcciones_file}': {nuevos_count} personajes nuevos, {mods_count} modificaciones.")
            print(f"Nuevo total final: {len(records)} registros genealógicos.")
        except Exception as ce:
            print(f"⚠️  Error cargando o aplicando '{correcciones_file}': {ce}")

    # Estadísticas opcionales
    if show_stats:
        print_statistics(records)

    # Validación de URLs opcional
    if validate:
        validate_urls(records)

    # ── Escribir salidas ──────────────────────────────────────────────────────

    # CSV
    with open(csv_output, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore", delimiter=",")
        writer.writeheader()
        writer.writerows(records)
    print(f"CSV guardado: {csv_output}")

    # TSV
    with open(tsv_output, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore", delimiter="\t")
        writer.writeheader()
        writer.writerows(records)
    print(f"TSV guardado: {tsv_output}")

    # Excel
    try:
        import pandas as pd
        df = pd.DataFrame(records)
        for col in fieldnames:
            if col not in df.columns:
                df[col] = ""
        df = df[fieldnames]
        df.to_excel(xlsx_output, index=False)
        print(f"Excel guardado: {xlsx_output}")
    except ImportError:
        print("pandas no instalado — omitiendo .xlsx.")

    # JS
    js_output_path = "genealogia_data.js"
    with open(js_output_path, "w", encoding="utf-8") as f:
        f.write("// genealogia_data.js — generado automáticamente por organizar_genealogia.py\n")
        f.write("// NO editar este archivo directamente; editar genealogia_organizada.xlsx\n")
        f.write(f"const GENEALOGIA_DATA = {json.dumps(records, ensure_ascii=False, indent=2)};\n")
    print(f"JS guardado: {js_output_path}")

    # JSON
    json_output_path = "genealogia_data.json"
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"JSON guardado: {json_output_path}")

    print("\nSUCCESS: Pipeline completado correctamente.")
    return records


def watch_mode(show_stats=False):
    """
    Modo watch: re-ejecuta el pipeline cuando Ase.txt cambia.
    Usa polling simple (no requiere watchdog).
    """
    import time
    import os

    print(f"Modo watch activo - monitoreando '{input_file}' (Ctrl+C para salir)")
    last_mtime = None

    while True:
        try:
            mtime = os.path.getmtime(input_file)
        except FileNotFoundError:
            print(f"⚠️  Archivo '{input_file}' no encontrado. Esperando...")
            time.sleep(3)
            continue

        if last_mtime is None or mtime != last_mtime:
            if last_mtime is not None:
                print(f"\n🔄 Cambio detectado en '{input_file}' — re-ejecutando pipeline...")
            last_mtime = mtime
            try:
                run_pipeline(show_stats=show_stats)
            except Exception as e:
                print(f"❌ Error durante el pipeline: {e}")

        time.sleep(2)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Procesa Ase.txt y genera los archivos de datos genealógicos bíblicos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos:
  python organizar_genealogia.py                  # Procesamiento estándar
  python organizar_genealogia.py --stats          # Con estadísticas detalladas
  python organizar_genealogia.py --watch          # Modo vigilancia (re-ejecuta al cambiar)
  python organizar_genealogia.py --watch --stats  # Watch + estadísticas
  python organizar_genealogia.py --validate-urls  # Valida URLs del dataset
"""
    )
    parser.add_argument(
        "--stats", action="store_true",
        help="Mostrar estadísticas detalladas y detección de ciclos."
    )
    parser.add_argument(
        "--watch", action="store_true",
        help="Modo vigilancia: re-ejecutar automáticamente cuando cambie Ase.txt."
    )
    parser.add_argument(
        "--validate-urls", action="store_true", dest="validate_urls",
        help="Verificar que todas las URLs del dataset respondan HTTP 200."
    )

    args = parser.parse_args()

    if args.watch:
        watch_mode(show_stats=args.stats)
    else:
        run_pipeline(show_stats=args.stats, validate=args.validate_urls)


if __name__ == "__main__":
    main()
