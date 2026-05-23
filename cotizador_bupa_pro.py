"""
╔══════════════════════════════════════════════════════════════╗
║     COTIZADOR PRO — BUPA SEGUROS CHILE  v4                  ║
║     Filtros reales · Selección por checkbox · WA dinámico   ║
╚══════════════════════════════════════════════════════════════╝
    pip install streamlit pandas
    streamlit run cotizador_bupa_pro.py
"""
import streamlit as st
import pandas as pd
import os
import io
import zipfile
from datetime import date
from urllib.parse import quote

st.markdown("""
<style>

/* ===== APP ===== */
.stApp{
    background-color:#F4F8FC;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#4EA5F5,#74B9FF);
    border-right:1px solid #d9e6f2;
}

[data-testid="stSidebar"] *{
    color:#083B66 !important;
}

/* ===== TITULOS ===== */
h1{
    color:#003A70 !important;
    font-weight:800 !important;
}

h2{
    color:#005EB8 !important;
    font-weight:700 !important;
}

h3{
    color:#0066C2 !important;
    font-weight:600 !important;
}

/* ===== TEXTO ===== */
p, label, span, div{
    color:#1f2d3d;
}

/* ===== INPUTS ===== */
.stTextInput input,
.stNumberInput input,
textarea{
    background:white !important;
    color:#222 !important;
    border:1px solid #c9d7e6 !important;
    border-radius:12px !important;
}

.stTextInput input::placeholder{
    color:#9aa9b8 !important;
}

/* ===== SELECTBOX ===== */
.stSelectbox div[data-baseweb="select"]{
    background:white !important;
    color:#222 !important;
    border-radius:12px !important;
}

/* ===== TARJETAS ===== */
div[data-testid="stMetric"]{
    background:white;
    border-radius:16px;
    padding:18px;
    box-shadow:0 4px 14px rgba(0,0,0,.06);
    border-left:5px solid #00AEEF;
}

/* ===== BOTONES ===== */
.stButton > button,
.stDownloadButton > button{
    background:#009FE3 !important;
    color:white !important;
    border:none !important;
    border-radius:12px !important;
    font-weight:600 !important;
    padding:0.6rem 1rem !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover{
    background:#0088c6 !important;
}

/* ===== WHATSAPP ===== */
a[data-testid="stLinkButton"]{
    background:#25D366 !important;
    color:white !important;
    border-radius:12px !important;
    padding:12px 18px !important;
    text-decoration:none !important;
    font-weight:700 !important;
}

a[data-testid="stLinkButton"]:hover{
    background:#1fb958 !important;
}

/* ===== ALERTAS ===== */
[data-testid="stAlert"]{
    border-radius:14px !important;
}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════
# LOGIN SIMPLE
# ═══════════════════════════════════════

USUARIOS = {
    "romulo": "seguros2026",
    "demo": "demo123",
    "ale": "mochada1997"
}

if "login_ok" not in st.session_state:
    st.session_state.login_ok = False

if not st.session_state.login_ok:

    st.title("🔒 Acceso Cotizador PRO")

    usuario = st.text_input("Usuario")
    clave = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        if usuario in USUARIOS and USUARIOS[usuario] == clave:
            st.session_state.login_ok = True
            st.rerun()

        else:
            st.error("Usuario o contraseña incorrecta")

    st.stop()

import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Cotizador PRO · Bupa Seguros",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)



# ✅ Corrección aplicada:
# Los planes BCT60/BCT70/BCT80 tenían mal configuradas las cargas 0-17 años.
# El portal Bupa usa tarifa infantil distinta a la de 18-25.

# ⚠️ Tarifas actualizadas manualmente según portal oficial Bupa Sales / productos.bupa.cl
# Validado con capturas mayo 2026 proporcionadas por Rómulo.

# ══════════════════════════════════════════════════════════════════
# BASE DE DATOS COMPLETA DE PLANES
# flags: cat, libre, maternidad, salud_mental, quirurgico, sin_dps
# prevision: ["FONASA"], ["ISAPRE"], ["FONASA","ISAPRE"]
# ══════════════════════════════════════════════════════════════════

PDFS_PLANES = {
    "Bupa + Protección 70/25": "pdfs/Seguro BMP Bupa + Proteccion 70-25.pdf",
    "Bupa + Protección 70/70": "pdfs/Seguro BMP Bupa + Proteccion 70-70.pdf",
    "Bupa + Protección 80/70": "pdfs/Seguro BMP Bupa + Proteccion 80-70.pdf",

    "Bupa Ambulatorio 70": "pdfs/Seguro BMPA70 Bupa Ambulatorio + Protección.pdf",

    "Bupa Cuidado Total 60": "pdfs/Seguro BCT Bupa Cuidado Total 60.pdf",
    "Bupa Cuidado Total 70": "pdfs/Seguro BCT Bupa Cuidado Total 70.pdf",
    "Bupa Cuidado Total 80": "pdfs/Seguro BCT Bupa Cuidado Total 80.pdf",

    "Bupa MultiSalud": "pdfs/Seguro BMS Bupa MultiSalud.pdf",
    "Bupa MultiSalud Pro": "pdfs/Seguro BMS Bupa MultiSalud Pro.pdf",

    "Dental IntegraMédica": "pdfs/Plan Dental IntegraMédica 68%.pdf",
    "IntegraMédica 100%": "pdfs/Plan IntegraMédica 100%.pdf",

    "Plan Adulto Mayor 70%": "pdfs/Plan IntegraMédica Adulto Mayor 70.pdf",

    "Bupa Complementa": "pdfs/Seguro BCO Bupa Complementa.pdf",

    "PYME Digital": "pdfs/PYME Digital.pdf",
}

PLANES = {
    "70/25": {
        "nombre":    "Bupa + Protección 70/25",
        "emoji":     "🔵",
        "prevision": ["FONASA"],
        "f_cat":True, "f_libre":False, "f_maternidad":True,
        "f_salud_mental":False, "f_quirurgico":True, "f_sin_dps":False,
        "contratante": {"0-2":None,"3-17":None,"18-25":0.75,"26-35":0.96,"36-45":1.10,"46-55":1.24,"56-59":1.41,"60-64":1.52,"65-70":2.05,"71-75":2.88},
        "dependiente": {"0-2":0.49,"3-17":0.49,"18-25":0.70,"26-35":0.92,"36-45":1.06,"46-55":1.20,"56-59":1.37,"60-64":1.48,"65-70":2.01,"71-75":2.84},
        "hosp":"70%","amb":"25%","cat":"✅ 100% hasta UF 9.500","tope_base":"UF 500/año",
        "tope_cat":"UF 9.500/año","muerte":"✅ UF 500","red":"Clínica Bupa Santiago + IntegraMédica",
        "maternidad":"70%","oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)",
        "ded_amb":"UF 0,5/año","ded_hosp":"UF 5/año","dps":True,"salud_mental":False,
        "para_quien":"Presupuesto limitado. Prioriza hospitalización. Uso ambulatorio bajo.",
        "no_para":"Quienes van mucho al médico ambulatorio (cubre solo 25%).",
        "carencias":"Bariátrica, ocular láser, rinolaringológica: 1 año.",
        "tag":"Precio mínimo con catastrófico · FONASA",
    },
    "70/70": {
        "nombre":    "Bupa + Protección 70/70",
        "emoji":     "🟣",
        "prevision": ["FONASA"],
        "f_cat":True, "f_libre":False, "f_maternidad":True,
        "f_salud_mental":False, "f_quirurgico":True, "f_sin_dps":False,
        "contratante": {"0-2":None,"3-17":None,"18-25":1.02,"26-35":1.31,"36-45":1.49,"46-55":1.69,"56-59":1.90,"60-64":2.05,"65-70":2.75,"71-75":3.85},
        "dependiente": {"0-2":0.64,"3-17":0.64,"18-25":0.97,"26-35":1.26,"36-45":1.45,"46-55":1.65,"56-59":1.85,"60-64":2.00,"65-70":2.71,"71-75":3.81},
        "hosp":"70%","amb":"70%","cat":"✅ 100% hasta UF 9.500","tope_base":"UF 500/año",
        "tope_cat":"UF 9.500/año","muerte":"✅ UF 500","red":"Clínica Bupa Santiago + IntegraMédica",
        "maternidad":"70%","oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)",
        "ded_amb":"UF 0,5/año","ded_hosp":"UF 5/año","dps":True,"salud_mental":False,
        "para_quien":"Familias con uso ambulatorio frecuente. Cobertura equilibrada.",
        "no_para":"Quien busca el máximo porcentaje hospitalario.",
        "carencias":"Bariátrica, ocular láser, rinolaringológica: 1 año.",
        "tag":"⭐ El más equilibrado · FONASA",
    },
    "80/70": {
        "nombre":    "Bupa + Protección 80/70",
        "emoji":     "🔴",
        "prevision": ["FONASA"],
        "f_cat":True, "f_libre":False, "f_maternidad":True,
        "f_salud_mental":False, "f_quirurgico":True, "f_sin_dps":False,
        "contratante": {"0-2":None,"3-17":None,"18-25":1.21,"26-35":1.55,"36-45":1.77,"46-55":2.01,"56-59":2.25,"60-64":2.43,"65-70":3.27,"71-75":4.57},
        "dependiente": {"0-2":0.76,"3-17":0.76,"18-25":1.16,"26-35":1.50,"36-45":1.73,"46-55":1.96,"56-59":2.21,"60-64":2.39,"65-70":3.22,"71-75":4.53},
        "hosp":"80%","amb":"70%","cat":"✅ 100% hasta UF 9.500","tope_base":"UF 500/año",
        "tope_cat":"UF 9.500/año","muerte":"✅ UF 500","red":"Clínica Bupa Santiago + IntegraMédica",
        "maternidad":"80%","oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)",
        "ded_amb":"UF 0,5/año","ded_hosp":"UF 5/año","dps":True,"salud_mental":False,
        "para_quien":"Máxima cobertura en red Bupa. Historial de cirugías o enfermedades crónicas.",
        "no_para":"Quien busca red más amplia que Bupa/IntegraMédica.",
        "carencias":"Bariátrica, ocular láser, rinolaringológica: 1 año.",
        "tag":"⭐ Mayor cobertura hospitalaria · FONASA",
    },
    "AMB70": {
        "nombre":    "Bupa Ambulatorio 70",
        "emoji":     "🟢",
        "prevision": ["FONASA"],
        "f_cat":False, "f_libre":False, "f_maternidad":False,
        "f_salud_mental":False, "f_quirurgico":False, "f_sin_dps":False,
        "contratante": {"0-2":0.86,"3-17":0.41,"18-25":0.57,"26-35":0.60,"36-45":0.68,"46-55":0.77,"56-59":0.86,"60-64":0.91,"65-70":0.96,"71-75":1.26},
        "dependiente": {"0-2":0.86,"3-17":0.41,"18-25":0.57,"26-35":0.60,"36-45":0.68,"46-55":0.77,"56-59":0.86,"60-64":0.91,"65-70":0.96,"71-75":1.26},
        "hosp":"❌ No cubre","amb":"70%","cat":"❌ No incluye","tope_base":"UF 250/año",
        "tope_cat":"— No aplica","muerte":"❌ No incluye","red":"Clínica Bupa Santiago + IntegraMédica",
        "maternidad":"❌ No cubre","oncologia":"❌ No cubre","dental":"62% dcto IntegraMédica",
        "medicamentos":"No incluye","ded_amb":"UF 0,5/año","ded_hosp":"— No aplica",
        "dps":True,"salud_mental":False,
        "para_quien":"Jóvenes sanos. Complemento básico. Presupuesto muy ajustado.",
        "no_para":"Personas con riesgo de hospitalización, embarazo o cirugías.",
        "carencias":"No aplica (no cubre hospitalización).",
        "tag":"Solo ambulatorio · Precio mínimo · FONASA",
    },
    "MULTI": {
        "nombre":    "Bupa MultiSalud",
        "emoji":     "🟡",
        "prevision": ["FONASA"],
        "f_cat":True, "f_libre":False, "f_maternidad":True,
        "f_salud_mental":True, "f_quirurgico":True, "f_sin_dps":False,
        "contratante": {"0-2":None,"3-17":None,"18-25":1.40,"26-35":1.80,"36-45":2.07,"46-55":2.76,"56-59":3.28,"60-64":3.62,"65-70":3.96,"71-75":5.29},
        "dependiente": {"0-2":1.35,"3-17":0.94,"18-25":1.40,"26-35":1.80,"36-45":2.07,"46-55":2.76,"56-59":3.28,"60-64":3.62,"65-70":3.96,"71-75":5.29},
        "hosp":"90%/80%/50% (según red)","amb":"70%/60%/50% (según red)",
        "cat":"✅ Extensión catastrófica en 2 capas hasta UF 7.500","tope_base":"UF 1.500/año",
        "tope_cat":"UF 7.500 total (Capa 1 UF 2.500 + Capa 2 UF 5.000)","muerte":"❌ No incluye",
        "red":"Red Pref: Bupa+Reñaca+IntegraMédica | Red 1: Dávila+Interclinica | Red 2: Sta.María+otros",
        "maternidad":"90%/80%/50%","oncologia":"90%/80%/50%","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)",
        "ded_amb":"UF 1/año","ded_hosp":"UF 5/año","dps":True,"salud_mental":True,
        "para_quien":"FONASA B,C,D con acceso a Dávila, Santa María. Red ampliada + salud mental.",
        "no_para":"Quien busca máxima cobertura en red única.",
        "carencias":"Bariátrica, ocular láser, rinolaringológica, reasignación sexo: 1 año.",
        "tag":"Red ampliada + Salud mental · FONASA",
    },
    "MULTIPRO": {
        "nombre":    "Bupa MultiSalud Pro",
        "emoji":     "🟠",
        "prevision": ["FONASA"],
        "f_cat":True, "f_libre":False, "f_maternidad":True,
        "f_salud_mental":True, "f_quirurgico":True, "f_sin_dps":False,
        "contratante": {"0-2":None,"3-17":None,"18-25":1.71,"26-35":2.07,"36-45":2.44,"46-55":3.24,"56-59":3.93,"60-64":4.30,"65-70":4.50,"71-75":6.22},
        "dependiente": {"0-2":1.58,"3-17":1.05,"18-25":1.71,"26-35":2.07,"36-45":2.44,"46-55":3.24,"56-59":3.93,"60-64":4.30,"65-70":4.50,"71-75":6.22},
        "hosp":"90%/80%/70% (según red)","amb":"90%/70%/60% (según red)",
        "cat":"✅ Extensión catastrófica en 2 capas hasta UF 7.500","tope_base":"UF 1.500/año",
        "tope_cat":"UF 7.500 total (Capa 1 UF 2.500 + Capa 2 UF 5.000)","muerte":"❌ No incluye",
        "red":"Red Pref: Bupa+Reñaca+IntegraMédica | Red 1: Dávila+Interclinica | Red 2: Sta.María+otros",
        "maternidad":"90%/80%/70%","oncologia":"90%/80%/70%","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)",
        "ded_amb":"UF 1/año","ded_hosp":"UF 5/año","dps":True,"salud_mental":True,
        "para_quien":"FONASA B,C,D con la mejor cobertura posible + red ampliada + salud mental.",
        "no_para":"Presupuesto ajustado.",
        "carencias":"Bariátrica, ocular láser, rinolaringológica, reasignación sexo: 1 año.",
        "tag":"⭐ Mayor cobertura Pro · FONASA",
    },
    "BCT60": {
        "nombre":    "Bupa Cuidado Total 60",
        "emoji":     "🔷",
        "prevision": ["FONASA","ISAPRE"],
        "f_cat":False, "f_libre":True, "f_maternidad":True,
        "f_salud_mental":True, "f_quirurgico":True, "f_sin_dps":False,
        "contratante": {"0-2":None,"3-17":None,"18-25":0.86,"26-35":1.04,"36-45":1.04,"46-55":1.16,"56-59":1.22,"60-64":1.32,"65-70":1.75,"71-75":2.44},
        "dependiente": {"0-2":0.75,"3-17":0.75,"18-25":0.86,"26-35":1.04,"36-45":1.04,"46-55":1.16,"56-59":1.22,"60-64":1.32,"65-70":1.75,"71-75":2.44},
        "hosp":"60%","amb":"60%","cat":"❌ No incluye","tope_base":"UF 250/año",
        "tope_cat":"— No aplica","muerte":"❌ No incluye","red":"Libre elección + cobertura extra Red Bupa",
        "maternidad":"60%","oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 30% marca con receta (tope $25.000/mes)",
        "ded_amb":"UF 1/año (gratis en Red Bupa)","ded_hosp":"UF 1/año (gratis en Red Bupa)",
        "dps":True,"salud_mental":True,
        "para_quien":"ISAPRE o FONASA que quieren libre elección. Salud mental incluida.",
        "no_para":"Quien necesita extensión catastrófica o tiene preexistencias.",
        "carencias":"Bariátrica, Septoplastía, Disforia de Género: 1 año.",
        "tag":"Libre elección · Salud mental · ISAPRE y FONASA",
    },
    "BCT70": {
        "nombre":    "Bupa Cuidado Total 70",
        "emoji":     "💙",
        "prevision": ["FONASA","ISAPRE"],
        "f_cat":False, "f_libre":True, "f_maternidad":True,
        "f_salud_mental":True, "f_quirurgico":True, "f_sin_dps":False,
        "contratante": {"0-2":None,"3-17":None,"18-25":1.09,"26-35":1.31,"36-45":1.31,"46-55":1.46,"56-59":1.56,"60-64":1.68,"65-70":2.24,"71-75":3.12},
        "dependiente": {"0-2":0.92,"3-17":0.92,"18-25":1.09,"26-35":1.31,"36-45":1.31,"46-55":1.46,"56-59":1.56,"60-64":1.68,"65-70":2.24,"71-75":3.12},
        "hosp":"70%","amb":"70%","cat":"❌ No incluye","tope_base":"UF 400/año",
        "tope_cat":"— No aplica","muerte":"❌ No incluye","red":"Libre elección + cobertura extra Red Bupa",
        "maternidad":"70%","oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 30% marca con receta (tope $25.000/mes)",
        "ded_amb":"UF 1/año (gratis en Red Bupa)","ded_hosp":"UF 1/año (gratis en Red Bupa)",
        "dps":True,"salud_mental":True,
        "para_quien":"ISAPRE o FONASA que quieren libre elección equilibrada. Tope UF 400.",
        "no_para":"Quien necesita extensión catastrófica o tiene preexistencias.",
        "carencias":"Bariátrica, Septoplastía, Disforia de Género: 1 año.",
        "tag":"⭐ Libre elección equilibrada · ISAPRE y FONASA",
    },
    "BCT80": {
        "nombre":    "Bupa Cuidado Total 80",
        "emoji":     "💜",
        "prevision": ["FONASA","ISAPRE"],
        "f_cat":False, "f_libre":True, "f_maternidad":True,
        "f_salud_mental":True, "f_quirurgico":True, "f_sin_dps":False,
        "contratante": {"0-2":None,"3-17":None,"18-25":1.35,"26-35":1.61,"36-45":1.61,"46-55":1.79,"56-59":1.93,"60-64":2.08,"65-70":2.78,"71-75":3.87},
        "dependiente": {"0-2":1.10,"3-17":1.10,"18-25":1.35,"26-35":1.61,"36-45":1.61,"46-55":1.79,"56-59":1.93,"60-64":2.08,"65-70":2.78,"71-75":3.87},
        "hosp":"80%","amb":"80%","cat":"❌ No incluye","tope_base":"UF 600/año",
        "tope_cat":"— No aplica","muerte":"❌ No incluye","red":"Libre elección + cobertura extra Red Bupa",
        "maternidad":"80%","oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 30% marca con receta (tope $25.000/mes)",
        "ded_amb":"UF 1/año (gratis en Red Bupa)","ded_hosp":"UF 1/año (gratis en Red Bupa)",
        "dps":True,"salud_mental":True,
        "para_quien":"ISAPRE o FONASA que quieren máxima cobertura con libre elección. Tope UF 600.",
        "no_para":"Quien necesita extensión catastrófica o tiene preexistencias.",
        "carencias":"Bariátrica, Septoplastía, Disforia de Género: 1 año.",
        "tag":"⭐ Máxima cobertura libre elección · ISAPRE y FONASA",
    },
    "COMPLEMENTA": {
        "nombre":    "Bupa Complementa",
        "emoji":     "🧩",
        "prevision": ["ISAPRE"],
        "f_cat":False, "f_libre":True, "f_maternidad":True,
        "f_salud_mental":True, "f_quirurgico":True, "f_sin_dps":False,
        # Tarifas del tarifario mayo 2026 (misma tabla que BCT pero exclusivo ISAPRE)
        "contratante": {"0-2":0.45,"3-17":0.45,"18-25":0.51,"26-35":0.63,"36-45":0.63,"46-55":0.70,"56-59":0.83,"60-64":0.89,"65-70":1.19,"71-75":None},
        "dependiente": {"0-2":0.45,"3-17":0.45,"18-25":0.51,"26-35":0.63,"36-45":0.63,"46-55":0.70,"56-59":0.83,"60-64":0.89,"65-70":1.19,"71-75":None},
        "hosp":"Mismo % que tu plan ISAPRE","amb":"Mismo % que tu plan ISAPRE (solo red Bupa)",
        "cat":"❌ No incluye","tope_base":"UF 500/año",
        "tope_cat":"— No aplica","muerte":"❌ No incluye",
        "red":"Hosp: Libre elección (excl. Clínica U. Andes, Las Condes, Alemana) | Amb: solo Bupa Stgo, Reñaca e IntegraMédica",
        "maternidad":"Mismo % que tu plan ISAPRE","oncologia":"Mismo % que tu plan ISAPRE",
        "dental":"No incluye","medicamentos":"No incluye",
        "ded_amb":"Sin deducible","ded_hosp":"Sin deducible (sin BMI)",
        "dps":True,"salud_mental":True,
        "para_quien":"ISAPRE que quiere cubrir el copago que su plan no paga. Sin deducible ni BMI.",
        "no_para":"FONASA. Quien quiere libre elección ambulatoria amplia (solo en red Bupa).",
        "carencias":"Bariátrica, rinolaringológica, reasignación sexo, vasectomía, reducción mamaria: 1 año.",
        "tag":"⭐ Exclusivo ISAPRE · Cubre tu copago · Sin deducible ni BMI",
    },
}

# ── Convenios (tarifa por tramo, no por edad) ─────────────────────
AM_TARIFAS = {
    "Solo Titular":             0.84,
    "Titular + 1 beneficiario": 1.55,
    "Titular + 2 beneficiarios":2.23,
    "Titular + 3 beneficiarios":2.92,
    "Titular + 4 beneficiarios":3.62,
}
IM100_TARIFAS = {
    "Solo Titular":             0.84,
    "Titular + 1 beneficiario": 1.32,
    "Titular + 2 beneficiarios":1.90,
    "Titular + 3 beneficiarios":2.49,
    "Titular + 4 beneficiarios":3.09,
    "Titular + 5 beneficiarios":3.69,
}
# Mi Dental: primer pago distinto al mensual
DENTAL_TARIFAS_INICIO = {
    "Solo Titular":             0.50,
    "Titular + 1 beneficiario": 0.99,
    "Titular + 2 beneficiarios":1.47,
    "Titular + 3 beneficiarios":1.96,
    "Titular + 4 beneficiarios":2.44,
}
DENTAL_TARIFAS_MENSUAL = {
    "Solo Titular":             0.08,
    "Titular + 1 beneficiario": 0.15,
    "Titular + 2 beneficiarios":0.22,
    "Titular + 3 beneficiarios":0.28,
    "Titular + 4 beneficiarios":0.35,
}

# ─── FUNCIONES ────────────────────────────────────────────────────

def rango(edad):
    if edad < 3:     return "0-2"
    elif edad <= 17: return "3-17"
    elif edad <= 25: return "18-25"
    elif edad <= 35: return "26-35"
    elif edad <= 45: return "36-45"
    elif edad <= 55: return "46-55"
    elif edad <= 59: return "56-59"
    elif edad <= 64: return "60-64"
    elif edad <= 70: return "65-70"
    else:            return "71-75"

def get_precio(pk, edad, es_contratante):
    col = "contratante" if es_contratante else "dependiente"
    return PLANES[pk][col].get(rango(edad))

def clp(uf, val_uf):
    return f"${uf * val_uf:,.0f}".replace(",", ".")

def ok(b): return "✅" if b else "❌"

def resumen_plan_whatsapp(p):
    cubre=[]
    no_cubre=[]

    if "❌" not in p["hosp"]:
        cubre.append("Hospitalizaciones y cirugías")
    if "❌" not in p["amb"]:
        cubre.append("Consultas médicas y exámenes")
    if p["f_salud_mental"]:
        cubre.append("Salud mental")
    if p["f_libre"]:
        cubre.append("Libre elección según póliza")
    if p["f_cat"]:
        cubre.append("Extensión catastrófica")
    if "❌" not in p["maternidad"]:
        cubre.append("Maternidad")

    if "❌" in p["hosp"]:
        no_cubre.append("Hospitalización y cirugías")
    if not p["f_cat"]:
        no_cubre.append("Extensión catastrófica")
    if "❌" in p["maternidad"]:
        no_cubre.append("Maternidad")

    exclusiones=[
        "Enfermedades preexistentes declaradas" if p["dps"] else "Prestaciones fuera de convenio",
        "Procedimientos estéticos",
        "Prestaciones excluidas en póliza",
    ]

    if p["dps"]:
        exclusiones.append("Prestaciones sujetas a evaluación médica (DPS)")

    return cubre, no_cubre, exclusiones


def cupon_para_plan(pk):
    """Retorna (codigo_cupon, pct_descuento) según el plan."""
    if not usar_cupon: return ("", 0)
    if pk in ["BCT60","BCT70","BCT80"]:           return CUPONES["BCT"]
    if pk in ["70/25","70/70","80/70"]:            return CUPONES["BP"]
    if pk == "MULTI":                              return CUPONES["BMS"]
    if pk == "AMB70":                              return CUPONES["AMBU"]
    if pk == "MULTIPRO":                           return CUPONES["BPRO"]
    return ("", 0)

def calcular(pk, edad_c, cargas, val_uf):
    pc = get_precio(pk, edad_c, True)
    if pc is None: return None
    cupon_cod, pct = cupon_para_plan(pk)
    pc_d = pc * (1 - pct/100)
    total = pc_d
    det = [{"quien":"Contratante","edad":edad_c,"orig":pc,"final":pc_d,
            "cupon":cupon_cod,"pct":pct}]
    for c in cargas:
        pcc = get_precio(pk, c["edad"], False)
        if pcc:
            pcc_d = pcc * (1 - pct/100)
            total += pcc_d
            det.append({"quien":c["nombre"],"edad":c["edad"],"orig":pcc,
                        "final":pcc_d,"cupon":cupon_cod,"pct":pct})
        else:
            det.append({"quien":c["nombre"],"edad":c["edad"],"orig":None,
                        "final":None,"cupon":"","pct":0})
    return {"total":total,"det":det,"cupon":cupon_cod,"pct":pct}

def calcular_convenio(pk):
    """Calcula precio de convenio según tramo seleccionado."""
    if pk == "AM70":
        uf = AM_TARIFAS[tramo_am]
        return {"total":uf,"tramo":tramo_am,"cupon":"","pct":0,
                "det":[{"quien":tramo_am,"edad":None,"orig":uf,"final":uf}],
                "es_convenio":True}
    if pk == "IM100":
        uf = IM100_TARIFAS[tramo_im]
        return {"total":uf,"tramo":tramo_im,"cupon":"","pct":0,
                "det":[{"quien":tramo_im,"edad":None,"orig":uf,"final":uf}],
                "es_convenio":True}
    if pk == "DENTAL":
        uf_mensual = DENTAL_TARIFAS_MENSUAL[tramo_dental]
        uf_inicio  = DENTAL_TARIFAS_INICIO[tramo_dental]
        return {"total":uf_mensual,"tramo":tramo_dental,"cupon":"","pct":0,
                "det":[{"quien":tramo_dental,"edad":None,"orig":uf_mensual,"final":uf_mensual}],
                "es_convenio":True,"uf_inicio":uf_inicio}
    return None

# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 👤 Datos del Cliente")
    nombre    = st.text_input("Nombre completo", placeholder="Ej: Franco Lupi")
    edad_c    = st.number_input("Edad contratante", 18, 84, 35)
    prevision = st.selectbox("Previsión", ["FONASA B,C,D","ISAPRE"])
    prevision_base = "ISAPRE" if prevision == "ISAPRE" else "FONASA"

    st.markdown("---")
    st.markdown("### 👨‍👩‍👧‍👦 Cargas")
    n_cargas = st.number_input("Número de cargas", 0, 6, 0)
    cargas = []
    for i in range(n_cargas):
        a, b = st.columns([2,1])
        nc = a.text_input(f"Carga {i+1}", key=f"nc{i}", placeholder="Parentesco")
        ec = b.number_input("Edad", 0, 75, 5, key=f"ec{i}")
        cargas.append({"nombre": nc or f"Carga {i+1}", "edad": ec})

    st.markdown("---")
    st.markdown("### ⚙️ Config")
    val_uf   = st.number_input("Valor UF ($)", 30000, 50000, 40180, 10)

    # Tramo para convenios (se usa si AM70 o IM100 están seleccionados)
    st.markdown("**Tramo convenios (si aplica):**")
    tramo_am   = st.selectbox("👴 Tramo Adulto Mayor",   list(AM_TARIFAS.keys()),   key="tramo_am")
    tramo_im   = st.selectbox("💊 Tramo IntegraMédica 100%", list(IM100_TARIFAS.keys()), key="tramo_im")
    tramo_dental = st.selectbox("🦷 Tramo Mi Dental", list(DENTAL_TARIFAS_MENSUAL.keys()), key="tramo_dental")

    st.markdown("---")
    st.markdown("### 🎁 Cupones de descuento")
    st.caption("Se aplican automáticamente según el plan")
    CUPONES = {
        "BCT":   ("BCTALL20NEW",    20),
        "BP":    ("BMPHYA20NEW",    20),
        "BMS":   ("BMSBASE20JUL",   20),
        "AMBU":  ("BMPAMB10ENERO",  10),
        "BPRO":  ("BMSPRO10JUL",    10),
    }
    usar_cupon = st.checkbox("Aplicar cupón de descuento", value=False)
    if usar_cupon:
        st.info("""**Cupones disponibles:**
- BCT 60/70/80: BCTALL20NEW (20%)
- B+P 70/25, 70/70, 80/70: BMPHYA20NEW (20%)
- MultiSalud: BMSBASE20JUL (20%)
- Ambulatorio 70: BMPAMB10ENERO (10%)
- MultiSalud Pro: BMSPRO10JUL (10%)""")

    st.markdown("---")
    st.markdown("### 🎯 Filtros del cliente")
    st.caption("Marca lo que el cliente necesita — filtra por edad y cobertura automáticamente")

    f_preex        = st.checkbox("⚠️ Tiene Preexistencias (sin DPS)")
    f_cat          = st.checkbox("⚡ Extensión Catastrófica")
    f_libre        = st.checkbox("🏥 Libre Elección de médico/clínica")
    f_maternidad   = st.checkbox("🍼 Cobertura de Maternidad")
    f_salud_mental = st.checkbox("🧠 Salud Mental (psicología/psiquiatría)")
    f_quirurgico   = st.checkbox("🔪 Hospitalización y Cirugías")

    if f_preex:
        st.warning("⚠️ Solo planes sin DPS. Activa los Convenios abajo.")

    st.markdown("---")
    st.markdown("### 🤝 Convenios especiales")
    st.caption("Sin DPS · Cubren preexistencias · Filtran por edad automáticamente")
    f_adulto_mayor = st.checkbox("👴 Adulto Mayor (60–84 años)")
    f_im100        = st.checkbox("💊 IntegraMédica 100% ambulatorio")
    f_dental       = st.checkbox("🦷 Mi Dental IntegraMédica 68%")
    f_pyme         = st.checkbox("🏢 Empresa / PYME")

# Variable alias para compatibilidad interna
f_sin_dps = f_preex

# ══════════════════════════════════════════════════════════════════
# CATÁLOGO UNIFICADO — planes regulares + convenios
# ══════════════════════════════════════════════════════════════════

EDAD_INGRESO = {
    "70/25":(18,75),"70/70":(18,75),"80/70":(18,75),
    "AMB70":(18,75),"MULTI":(18,75),"MULTIPRO":(18,75),
    "BCT60":(18,75),"BCT70":(18,75),"BCT80":(18,75),
    "COMPLEMENTA":(18,89),
    "AM70" :(60,84),"IM100":(18,64),"DENTAL":(18,89),
}

CONVENIOS = {
    "AM70": {
        "nombre":"Plan Adulto Mayor 70%","emoji":"👴",
        "prevision":["FONASA","ISAPRE"],
        "f_cat":False,"f_libre":False,"f_maternidad":False,
        "f_salud_mental":False,"f_quirurgico":False,"f_sin_dps":True,
        "dps":False,"tag":"Solo ambulatorio · Sin DPS · 60–84 años",
        "hosp":"❌ No cubre","amb":"70%","cat":"❌ No incluye",
        "tope_base":"UF 25/beneficiario/año","tope_cat":"— No aplica",
        "muerte":"❌ No incluye","maternidad":"❌ No cubre","oncologia":"❌ No cubre",
        "salud_mental":False,"red":"Solo IntegraMédica nacional",
        "dental":"No incluye",
        "medicamentos":"60% genérico / 40% marca con receta (tope $20.000/mes)",
        "ded_amb":"Sin deducible","ded_hosp":"— No aplica",
        "rescate_vital":"🚑 Unidad Coronaria Móvil (UCM) · Activación ilimitada riesgo vital inminente · 2 activaciones/año riesgo vital · Fono: 223914444",
        "para_quien":"60–84 años con preexistencias. Sin DPS. Ingreso inmediato.",
        "no_para":"Quien necesita hospitalización o cirugías.",
        "carencias":"Sin carencias — vigencia desde contratación.",
        "es_convenio":True,"tarifas":AM_TARIFAS,
    },
    "IM100": {
        "nombre":"IntegraMédica 100%","emoji":"💊",
        "prevision":["FONASA","ISAPRE"],
        "f_cat":False,"f_libre":False,"f_maternidad":False,
        "f_salud_mental":False,"f_quirurgico":False,"f_sin_dps":True,
        "dps":False,"tag":"100% ambulatorio · Sin DPS · Cubre preexistencias",
        "hosp":"❌ No cubre","amb":"100%","cat":"❌ No incluye",
        "tope_base":"UF 60/año","tope_cat":"— No aplica",
        "muerte":"❌ No incluye","maternidad":"❌ No cubre","oncologia":"❌ No cubre",
        "salud_mental":False,"red":"Solo IntegraMédica nacional",
        "dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)",
        "ded_amb":"Sin deducible","ded_hosp":"— No aplica",
        "para_quien":"Cualquier edad con preexistencias. 100% copago ambulatorio.",
        "no_para":"Quien necesita hospitalización, cirugías o maternidad.",
        "carencias":"Sin carencias — vigencia inmediata.",
        "es_convenio":True,"tarifas":IM100_TARIFAS,
    },
    "DENTAL": {
        "nombre":"Mi Dental IntegraMédica 68%","emoji":"🦷",
        "prevision":["FONASA","ISAPRE"],
        "f_cat":False,"f_libre":False,"f_maternidad":False,
        "f_salud_mental":False,"f_quirurgico":False,"f_sin_dps":True,
        "dps":False,"tag":"68% dcto todos los tratamientos dentales · Sin DPS · 18–89 años",
        "hosp":"❌ No cubre","amb":"❌ Solo dental",
        "cat":"❌ No incluye","tope_base":"Sin tope (68% dcto en todos los tratamientos)",
        "tope_cat":"— No aplica","muerte":"❌ No incluye",
        "maternidad":"❌ No cubre","oncologia":"❌ No cubre",
        "salud_mental":False,
        "red":"Red Dental IntegraMédica (Stgo, Copiapó, La Serena, Viña, Rancagua, Talca, Concepción)",
        "dental":"68% dcto TODOS los tratamientos dentales + 1 limpieza anual GRATIS",
        "medicamentos":"50% genérico / 20% marca con receta (tope $20.000/mes) SalcoBrand",
        "ded_amb":"Sin deducible","ded_hosp":"— No aplica",
        "para_quien":"Cualquier persona. Todas las edades. Sin previsión requerida. Ideal para tratamientos dentales.",
        "no_para":"Quien necesita cobertura médica, hospitalización o ambulatorio.",
        "carencias":"Vigencia dental desde el 2° mes. Sin carencias para descuentos.",
        "es_convenio":True,"tarifas":DENTAL_TARIFAS_MENSUAL,
        "tarifas_inicio":DENTAL_TARIFAS_INICIO,
    },
}

CATALOGO = {**PLANES, **CONVENIOS}

# ── Funciones de compatibilidad ───────────────────────────────────

def edad_valida(pk, edad):
    e_min, e_max = EDAD_INGRESO.get(pk, (18,75))
    if edad < e_min or edad > e_max: return False
    if pk in PLANES:
        return PLANES[pk]["contratante"].get(rango(edad)) is not None
    return True  # convenios usan tramos

def es_compatible(pk):
    p = CATALOGO[pk]
    if not edad_valida(pk, edad_c):                return False
    if prevision_base not in p["prevision"]:        return False
    if (f_sin_dps or f_preex) and p["dps"]:        return False
    if f_cat          and not p["f_cat"]:           return False
    if f_libre        and not p["f_libre"]:         return False
    if f_maternidad   and not p["f_maternidad"]:    return False
    if f_salud_mental and not p["f_salud_mental"]:  return False
    if f_quirurgico   and not p["f_quirurgico"]:    return False
    # Convenios: solo aparecen si su checkbox está activo o hay filtro que los activa
    if pk == "AM70"   and not (f_adulto_mayor or f_preex or f_sin_dps): return False
    if pk == "IM100"  and not (f_im100 or f_preex or f_sin_dps):        return False
    if pk == "DENTAL" and not (f_dental or f_sin_dps):                  return False
    return True

# ── Calcular planes compatibles ───────────────────────────────────

ningun_filtro = not any([f_cat,f_libre,f_maternidad,f_salud_mental,f_quirurgico,
                          f_sin_dps,f_preex,f_adulto_mayor,f_im100,f_dental,f_pyme])

if ningun_filtro:
    # Sin filtros: mostrar todos los planes regulares válidos para esta edad
    planes_compatibles = [pk for pk in PLANES
                          if edad_valida(pk, edad_c)
                          and prevision_base in PLANES[pk]["prevision"]]
else:
    planes_compatibles = [pk for pk in CATALOGO if es_compatible(pk)]

# Calcular precios
precios = {}
for pk in planes_compatibles:
    if pk in PLANES:
        r = calcular(pk, edad_c, cargas, val_uf)
        if r: precios[pk] = r
    else:
        r = calcular_convenio(pk)
        if r: precios[pk] = r

planes_compatibles = [pk for pk in planes_compatibles if pk in precios]

# Avisos en sidebar por edad
if edad_c > 75:
    st.sidebar.error(f"🔴 {edad_c} años: sin planes regulares. Activa 👴 o 💊 en Convenios.")
elif edad_c >= 60:
    st.sidebar.info(f"💡 {edad_c} años: también aplica el Plan Adulto Mayor (60–84 años).")

# Recomendado (planes regulares con precio)
orden_rec = ["BCT80","BCT70","80/70","MULTIPRO","BCT60","70/70","MULTI","70/25","AMB70"]
rec = next((p for p in orden_rec if p in precios and precios[p].get("total")), "")

# ══════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════

st.markdown("""
<div style="
background:linear-gradient(90deg,#005EB8,#00AEEF);
padding:22px;
border-radius:18px;
margin-bottom:20px;
box-shadow:0 6px 20px rgba(0,0,0,.10);
">

<h1 style="
margin:0;
color:white !important;
font-size:34px;
">
🏥 Cotizador PRO — Bupa Seguros Chile
</h1>

<p style="
margin-top:8px;
margin-bottom:0;
color:#E
h1, h2, h3, h4 = st.columns(4)
h1.info(f"**Cliente:** {nombre or '(sin nombre)'} · {edad_c} años")
h2.info(f"**Previsión:** {prevision}")
h3.info(f"**Cargas:** {n_cargas} | **UF:** ${val_uf:,}".replace(",","."))
h4.info(f"**Opciones disponibles:** {len(planes_compatibles)}")

# Avisos importantes
if edad_c > 75:
    # Solo Adulto Mayor aplica (IM100 solo hasta 64)
    st.error(f"🔴 Con {edad_c} años no hay planes regulares (máx. ingreso 75 años). "
             f"Activa **👴 Adulto Mayor** en Convenios Especiales del panel izquierdo.")
elif edad_c > 64:
    # Entre 65 y 75: IM100 ya no aplica, solo Adulto Mayor
    if not f_adulto_mayor:
        st.info(f"💡 Con {edad_c} años también aplica el **Plan Adulto Mayor** (60–84 años). "
                f"Actívalo en Convenios Especiales en el panel izquierdo.")
elif edad_c >= 60 and not f_adulto_mayor:
    # Entre 60 y 64: aplican ambos
    st.info(f"💡 Con {edad_c} años también aplican el **Plan Adulto Mayor** (60–84 años) "
            f"y la **IntegraMédica 100%** (hasta 64 años). Actívalos en Convenios Especiales.")
if f_preex:
    st.warning("⚠️ Preexistencias activas — solo planes sin DPS y convenios.")

# ══════════════════════════════════════════════════════════════════
# SELECCIÓN POR CHECKBOX — regulares + convenios en vista unificada
# ══════════════════════════════════════════════════════════════════

st.markdown("---")
planes_seleccionados = []

if planes_compatibles:
    st.markdown("### ✅ Selecciona los planes a presentar al cliente")
    st.caption("Solo los planes marcados aparecerán en el detalle y en el mensaje WhatsApp")

    regulares_disp = [pk for pk in planes_compatibles if pk in PLANES and precios[pk].get("total")]
    convenios_disp = [pk for pk in planes_compatibles if pk in CONVENIOS]

    if regulares_disp:
        st.markdown("**📋 Planes regulares:**")
        cols_r = st.columns(min(len(regulares_disp), 4))
        for i, pk in enumerate(regulares_disp):
            p = PLANES[pk]
            r = precios[pk]
            with cols_r[i % 4]:
                etiqueta = f"{p['emoji']} {p['nombre']}\nUF {r['total']:.2f}"
                if st.checkbox(etiqueta, value=(pk == rec), key=f"sel_{pk}"):
                    planes_seleccionados.append(pk)

    if convenios_disp:
        st.markdown("**🤝 Convenios (sin DPS · cubren preexistencias):**")
        cols_c = st.columns(min(len(convenios_disp), 4))
        for i, pk in enumerate(convenios_disp):
            p = CONVENIOS[pk]
            r = precios.get(pk)
            with cols_c[i % 4]:
                precio_str = f"UF {r['total']:.2f} ({r['tramo']})" if r else "por tramo"
                etiqueta = f"{p['emoji']} {p['nombre']}\n{precio_str}"
                if st.checkbox(etiqueta, value=True, key=f"sel_{pk}"):
                    planes_seleccionados.append(pk)

    if not planes_seleccionados:
        st.warning("☝️ Marca al menos un plan para ver el detalle y generar el WhatsApp.")

else:
    if edad_c > 75:
        st.error(f"⛔ No hay planes disponibles para {edad_c} años.")
Activa en el panel izquierdo:
- 👴 **Plan Adulto Mayor** (acepta 60–84 años)""")
    elif edad_c > 64:
        st.error(f"""⛔ **No hay planes regulares para {edad_c} años** (máx. 75 años).
Activa en el panel izquierdo:
- 👴 **Plan Adulto Mayor** (acepta 60–84 años)
_(IntegraMédica 100% solo acepta hasta 64 años)_""")
    elif f_preex or f_sin_dps:
        st.warning("⚠️ No hay opciones sin DPS con esos filtros. Activa 👴 Adulto Mayor o 💊 IntegraMédica 100%.")
    else:
        st.warning("💡 Ningún plan cumple los filtros. Revisa la combinación.")

t1, t2, t3, t4 = st.tabs(["📋 Detalle de Planes","📊 Comparativa","🔍 Coberturas","📱 WhatsApp"])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — DETALLE
# ══════════════════════════════════════════════════════════════════
with t1:
    if not planes_seleccionados:
        st.info("Selecciona al menos un plan arriba para ver el detalle.")
    else:
        # Métricas rápidas — todos juntos
        cols_met = st.columns(min(len(planes_seleccionados), 4))
        for i, pk in enumerate(planes_seleccionados):
            p = CATALOGO[pk]
            r = precios[pk]
            with cols_met[i % 4]:
                es_conv = pk in CONVENIOS
                lbl = f"{'⭐ ' if pk==rec else ''}{p['emoji']} {p['nombre']}"
                sub = f"({r.get('tramo','')}) " if es_conv else ""
                cupon_badge = f" 🎁{r.get('pct',0)}%" if r.get('pct',0) > 0 else ""
                st.metric(lbl, f"UF {r['total']:.2f}{cupon_badge}",
                          sub + clp(r['total'],val_uf)+"/mes")

        st.markdown("---")

        for pk in planes_seleccionados:
            p = CATALOGO[pk]
            r = precios[pk]
            es_conv = pk in CONVENIOS
            es_rec  = pk == rec
            cupon_str = f" 🎁 {r.get('cupon','')} ({r.get('pct',0)}% dcto)" if r.get('pct',0) > 0 else ""
            tramo_str = f" · {r.get('tramo','')}" if es_conv else ""
            titulo = (f"{'⭐ RECOMENDADO · ' if es_rec else ''}{p['emoji']} {p['nombre']}"
                      f"{tramo_str} — UF {r['total']:.2f}/mes{cupon_str} · {clp(r['total'],val_uf)}")

            with st.expander(titulo, expanded=es_rec):
                badges_line = []
                if es_conv: badges_line.append("🤝 Convenio · Sin DPS · Cubre preexistencias")
                if p["f_cat"]:            badges_line.append("⚡ Catastrófico")
                if p["f_libre"]:          badges_line.append("🏥 Libre Elección")
                if p["f_maternidad"]:     badges_line.append("🍼 Maternidad")
                if p["f_salud_mental"]:   badges_line.append("🧠 Salud Mental")
                if p["f_quirurgico"]:     badges_line.append("🔪 Hospitalización")
                if not p["f_quirurgico"]: badges_line.append("⚠️ Solo Ambulatorio")
                if r.get("pct",0) > 0:    badges_line.append(f"🎁 Cupón {r['cupon']} ({r['pct']}% dcto)")
                st.markdown(f"**{p['tag']}** · {'  ·  '.join(badges_line)}")
                st.markdown(f"Previsión: {' / '.join(p['prevision'])}")
                st.markdown("---")

                col_izq, col_der = st.columns(2)
                with col_izq:
                    st.markdown("##### 📊 Coberturas")
                    for k, v in [
                        ("🏥 Hospitalaria",     p["hosp"]),
                        ("🩺 Ambulatoria",       p["amb"]),
                        ("⚡ Catastrófica",      p["cat"]),
                        ("🍼 Maternidad",        p["maternidad"]),
                        ("💀 Muerte accidental", p["muerte"]),
                        ("🧠 Salud mental",      ok(p["salud_mental"])),
                        ("🦷 Dental",            p["dental"]),
                        ("💊 Medicamentos",      p["medicamentos"]),
                        ("🔝 Tope base",         p["tope_base"]),
                        ("🔝 Tope catastrófico", p["tope_cat"]),
                        ("➖ Deducible amb.",    p["ded_amb"]),
                        ("➖ Deducible hosp.",   p["ded_hosp"]),
                        ("📋 DPS",               "No requerida" if not p["dps"] else "Requerida"),
                        ("🏥 Red",               p["red"]),
                    ]:
                        ca, cb = st.columns([2,3])
                        ca.markdown(f"**{k}**")
                        cb.write(v)
                    # UCM solo para AM70
                    if pk == "AM70" and p.get("rescate_vital"):
                        ca, cb = st.columns([2,3])
                        ca.markdown("**🚑 Rescate Vital**")
                        cb.write(p["rescate_vital"])

                with col_der:
                    st.markdown("##### 👥 Asegurados y precios")
                    if es_conv:
                        st.write(f"• **{r.get('tramo','')}**: UF {r['total']:.2f} · {clp(r['total'],val_uf)}")
                        st.caption("Precio fijo por tramo familiar — no varía por edad individual")
                        # Tabla de tramos del convenio
                        tarifas = p.get("tarifas", {})
                        df_t = pd.DataFrame({
                            "Tramo": list(tarifas.keys()),
                            "UF/mes": [f"UF {v:.2f}" for v in tarifas.values()],
                            "$/mes": [clp(v, val_uf) for v in tarifas.values()],
                        })
                        st.dataframe(df_t, hide_index=True, use_container_width=True)
                    else:
                        for d in r["det"]:
                            if d["final"]:
                                if d.get("pct",0) > 0 and d["orig"]:
                                    st.write(f"• **{d['quien']}** ({d['edad']} años): "
                                             f"~~UF {d['orig']:.2f}~~ → **UF {d['final']:.2f}** · {clp(d['final'],val_uf)}")
                                else:
                                    st.write(f"• **{d['quien']}** ({d['edad']} años): "
                                             f"UF {d['final']:.2f} · {clp(d['final'],val_uf)}")
                            else:
                                st.write(f"• {d['quien']} ({d['edad']} años): *no disponible*")
                        if r.get("pct",0) > 0:
                            st.info(f"🎁 Descuento {r['pct']}% con cupón **{r['cupon']}**")

                st.markdown("---")
                cb1, cb2 = st.columns(2)
                cb1.success(f"✅ **Le conviene a:** {p['para_quien']}")
                cb2.warning(f"⚠️ **No ideal para:** {p['no_para']}")
                st.caption(f"⏳ Carencias: {p['carencias']}")
                st.markdown("---")

                col_izq, col_der = st.columns(2)
                with col_izq:
                    st.markdown("##### 📊 Coberturas")
                    for k, v in [
                        ("🏥 Hospitalaria",     p["hosp"]),
                        ("🩺 Ambulatoria",       p["amb"]),
                        ("⚡ Catastrófica",      p["cat"]),
                        ("🍼 Maternidad",        p["maternidad"]),
                        ("💀 Muerte accidental", p["muerte"]),
                        ("🧠 Salud mental",      ok(p["salud_mental"])),
                        ("🦷 Dental",            p["dental"]),
                        ("💊 Medicamentos",      p["medicamentos"]),
                        ("🔝 Tope base",         p["tope_base"]),
                        ("🔝 Tope catastrófico", p["tope_cat"]),
                        ("➖ Deducible amb.",    p["ded_amb"]),
                        ("➖ Deducible hosp.",   p["ded_hosp"]),
                        ("📋 DPS",               "Requerida" if p["dps"] else "No requerida"),
                        ("🏥 Red",               p["red"]),
                    ]:
                        ca, cb = st.columns([2,3])
                        ca.markdown(f"**{k}**")
                        cb.write(v)

                with col_der:
                    st.markdown("##### 👥 Asegurados y precios")
                    for d in r["det"]:
                        if d["final"]:
                            if d.get("pct",0) > 0 and d["orig"]:
                                st.write(f"• **{d['quien']}** ({d['edad']} años): ~~UF {d['orig']:.2f}~~ → **UF {d['final']:.2f}** · {clp(d['final'],val_uf)}")
                            else:
                                st.write(f"• **{d['quien']}** ({d['edad']} años): UF {d['final']:.2f} · {clp(d['final'],val_uf)}")
                        else:
                            st.write(f"• {d['quien']} ({d['edad']} años): *no disponible para esta edad*")

                    if r.get("pct",0) > 0:
                        st.info(f"🎁 Descuento {r['pct']}% con cupón **{r['cupon']}**")

                st.markdown("---")
                cb1, cb2 = st.columns(2)
                cb1.success(f"✅ **Le conviene a:** {p['para_quien']}")
                cb2.warning(f"⚠️ **No ideal para:** {p['no_para']}")
                st.caption(f"⏳ Carencias: {p['carencias']}")

# ══════════════════════════════════════════════════════════════════
# TAB 2 — COMPARATIVA
# ══════════════════════════════════════════════════════════════════
with t2:
    if len(planes_seleccionados) < 2:
        st.info("Selecciona al menos 2 planes para comparar.")
    else:
        filas = {"Característica": [
            "💰 Prima UF/mes","💵 Prima $/mes","📆 Prima $/año",
            "🏥 Cobertura hosp.","🩺 Cobertura amb.",
            "⚡ Catastrófica","🔝 Tope base","🔝 Tope cat.",
            "🍼 Maternidad","💀 Muerte accidental",
            "🧠 Salud mental","🦷 Dental",
            "➖ Deducible amb.","➖ Deducible hosp.",
            "🏥 Red","📋 DPS","🎯 Previsión","🎁 Cupón",
        ]}
        for pk in planes_seleccionados:
            p = CATALOGO[pk]
            r = precios[pk]
            es_conv = pk in CONVENIOS
            lbl = f"{'⭐ ' if pk==rec else ''}{p['emoji']} {p['nombre']}"
            if es_conv: lbl += f"\n({r.get('tramo','')})"
            cupon_info = f"{r.get('cupon','')} ({r.get('pct',0)}%)" if r.get('pct',0) > 0 else "—"
            filas[lbl] = [
                f"UF {r['total']:.2f}",
                clp(r['total'],val_uf),
                clp(r['total']*12,val_uf),
                p["hosp"], p["amb"],
                "✅" if p["f_cat"] else "❌",
                p["tope_base"], p["tope_cat"],
                p["maternidad"],
                "✅" if "500" in p["muerte"] else "❌",
                ok(p["salud_mental"]), p["dental"][:20] if len(p["dental"])>20 else p["dental"],
                p["ded_amb"], p["ded_hosp"],
                p["red"][:30]+"..." if len(p["red"])>30 else p["red"],
                "No" if not p["dps"] else "Sí",
                " / ".join(p["prevision"]),
                cupon_info,
            ]
        df = pd.DataFrame(filas).set_index("Característica")
        st.dataframe(df, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# TAB 3 — COBERTURAS DETALLADAS
# ══════════════════════════════════════════════════════════════════
with t3:
    if not planes_seleccionados:
        st.info("Selecciona planes arriba.")
    else:
        plan_det = st.selectbox("Ver detalle de:",
            options=planes_seleccionados,
            format_func=lambda x: f"{CATALOGO[x]['emoji']} {CATALOGO[x]['nombre']}")

        p = CATALOGO[plan_det]
        r = precios[plan_det]
        st.markdown(f"## {p['emoji']} {p['nombre']}")
        if r:
            st.markdown(f"**Prima:** UF {r['total']:.2f}/mes · {clp(r['total'],val_uf)}/mes · {clp(r['total']*12,val_uf)}/año")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🩺 Ambulatorio")
            for item in ["Consultas medicina general (ilimitadas, presencial)",
                         "Videoconsultas medicina general y especialidades (ilimitadas)",
                         "Consultas especialidad presencial (ilimitadas)",
                         "Consulta de urgencia","Nutricionista (con prescripción)",
                         "Exámenes laboratorio e imagenología","Exámenes preventivos",
                         "Procedimientos diagnósticos y terapéuticos"]:
                if "❌" not in p["amb"]:
                    st.write(f"✅ **{p['amb']}** — {item}")
                else:
                    st.write(f"❌ {item}")
            if p["salud_mental"]:
                st.write("✅ **Psicología y Psiquiatría** ambulatoria")
            if p["f_libre"]:
                st.write("✅ **Kinesiología y Fonoaudiología** (con prescripción)")

            if p["f_quirurgico"]:
                st.markdown("#### 🏥 Hospitalización")
                for item in ["Día cama","Día cama UTI/UCI/Incubadora",
                             "Honorarios médico quirúrgicos","Derecho a pabellón",
                             "Insumos y medicamentos hospitalarios",
                             "Procedimientos diagnósticos","Cirugía ambulatoria"]:
                    st.write(f"✅ **{p['hosp']}** — {item}")
            else:
                st.error("❌ Este plan NO cubre hospitalización ni cirugías")

        with c2:
            if p["f_maternidad"]:
                st.markdown("#### 🍼 Maternidad")
                for item in ["Parto normal","Cesárea","Aborto no voluntario","Complicaciones del embarazo"]:
                    st.write(f"✅ **{p['maternidad']}** — {item}")

            st.markdown("#### ⚡ Extensión Catastrófica")
            if p["f_cat"]:
                st.success(p["cat"])
                st.write(f"Tope: {p['tope_cat']}")
            else:
                st.error("❌ No incluye extensión catastrófica")

            st.markdown("#### 📌 Topes y Deducibles")
            df_t = pd.DataFrame({
                "Concepto":["Tope base","Tope catastrófico","Deducible amb.","Deducible hosp.","Muerte accidental"],
                "Valor":[p["tope_base"],p["tope_cat"],p["ded_amb"],p["ded_hosp"],p["muerte"]],
            })
            st.dataframe(df_t, hide_index=True, use_container_width=True)

            st.markdown("#### 🏥 Red de Prestadores")
            st.info(p["red"])
            if p["f_libre"]:
                st.markdown("""
| Red | Lab. | Imag. | Día cama | Pabellón |
|-----|------|-------|----------|----------|
| IntegraMédica | +12% | +12% | — | — |
| Clínica Bupa Stgo | +10% | +10% | +10% | +10% |
| Clínica Bupa Reñaca | +10% | +10% | +10% | +10% |
""")

        st.markdown("---")
        ca, cb = st.columns(2)
        ca.success(f"✅ Le conviene a: {p['para_quien']}")
        cb.warning(f"⚠️ No ideal para: {p['no_para']}")
        st.caption(f"⏳ Carencias: {p['carencias']}")

# ══════════════════════════════════════════════════════════════════
# TAB 4 — WHATSAPP (usa exactamente los planes seleccionados)
# ══════════════════════════════════════════════════════════════════
with t4:
    st.subheader("📱 Mensaje WhatsApp")

    if not planes_seleccionados:
        st.info("Selecciona planes arriba para generar el mensaje.")
    else:
        wa1, wa2 = st.columns(2)
        with wa1:
            asesor   = st.text_input("Tu nombre", "Romulo Lupi")
            telefono = st.text_input("Tu teléfono", "+569 90790892")
            telefono_cliente = st.text_input(
                "WhatsApp cliente (solo 9 dígitos)",
                placeholder="912345678"
            )
        with wa2:
            modo = st.radio("Modo", ["Un solo plan","Comparativa (todos los seleccionados)"])

        hoy = date.today().strftime("%d/%m/%Y")
        nc  = nombre or "Estimado/a"

        def build_puntos(pk):
            p = CATALOGO[pk]
            r = precios[pk]
            es_conv = pk in CONVENIOS
            pts = []
            # ── Lo que SÍ cubre ──────────────────────────────────
            if "❌" not in p["hosp"]:        pts.append(f"🏥 Hospitalización: {p['hosp']}")
            pts.append(                                  f"🩺 Ambulatorio: {p['amb']}")
            if p["f_cat"]:                   pts.append(f"⚡ Catastrófico: 100% hasta {p['tope_cat']}")
            if "❌" not in p["maternidad"]:   pts.append(f"🍼 Maternidad: {p['maternidad']}")
            if "500" in p["muerte"]:          pts.append("💀 Muerte accidental: UF 500")
            if p["salud_mental"]:             pts.append("🧠 Salud mental (psicología y psiquiatría)")
            if p["f_libre"]:                  pts.append("🏥 Libre elección de médico y clínica")
            if es_conv and pk == "AM70":      pts.append("🚑 Rescate Riesgo Vital — Unidad Coronaria Móvil (fono: 223914444)")
            if es_conv:                       pts.append("✅ CUBRE PREEXISTENCIAS — sin DPS")
            if p["dental"] and "No" not in p["dental"]: pts.append(f"🦷 Dental: {p['dental']}")
            pts.append(                                  f"💊 Medicamentos: {p['medicamentos']}")
            # ── Lo que NO cubre ───────────────────────────────────
            no_cubre = []
            if "❌" in p["hosp"]:             no_cubre.append("Hospitalización ni cirugías")
            if not p["f_cat"]:                no_cubre.append("Extensión catastrófica")
            if "❌" in p["maternidad"]:        no_cubre.append("Maternidad")
            if "❌" in p["oncologia"]:         no_cubre.append("Oncología")
            if not p["salud_mental"]:          no_cubre.append("Psicología ni psiquiatría")
            if "500" not in p["muerte"]:       no_cubre.append("Muerte accidental")
            if not p["f_libre"]:               no_cubre.append("Libre elección (red cerrada)")
            if no_cubre:
                pts.append("⛔ *No cubre:* " + " · ".join(no_cubre))
            return pts

        def precio_str_wa(pk):
            r = precios[pk]
            pct = r.get("pct", 0)
            if pct > 0:
                orig = sum(d["orig"] for d in r["det"] if d.get("orig"))
                return f"~~UF {orig:.2f}~~ → *UF {r['total']:.2f}* (~{clp(r['total'],val_uf)}/mes)"
            return f"*UF {r['total']:.2f}* (~{clp(r['total'],val_uf)}/mes)"

        def asegurados_str(pk):
            r = precios[pk]
            es_conv = pk in CONVENIOS
            if es_conv:
                return f"\n   • {r.get('tramo','')}: UF {r['total']:.2f} ({clp(r['total'],val_uf)})"
            s = ""
            for d in r["det"]:
                if d.get("final"):
                    if d.get("pct",0) > 0 and d.get("orig"):
                        s += f"\n   • {d['quien']} ({d['edad']} años): ~~UF {d['orig']:.2f}~~ → UF {d['final']:.2f} ({clp(d['final'],val_uf)})"
                    else:
                        s += f"\n   • {d['quien']} ({d['edad']} años): UF {d['final']:.2f} ({clp(d['final'],val_uf)})"
            return s

        def cupon_str_plan(pk):
            r = precios[pk]
            if r.get("pct",0) > 0:
                return f"\n🎁 *Cupón:* {r['cupon']} ({r['pct']}% dcto)"
            return ""

        if modo == "Un solo plan":
            plan_wa = st.selectbox("Plan a enviar:",
                options=planes_seleccionados,
                format_func=lambda x: f"{CATALOGO[x]['emoji']} {CATALOGO[x]['nombre']}")

            p = CATALOGO[plan_wa]
            r = precios[plan_wa]
            pts = build_puntos(plan_wa)
            es_conv = plan_wa in CONVENIOS

            msg = f"""Hola {nc} 👋

Te comparto tu cotización personalizada de *Bupa Seguros* 🏥
📅 Fecha: {hoy}

━━━━━━━━━━━━━━━━━━━━━
🏥 *COTIZACIÓN BUPA SEGUROS*
━━━━━━━━━━━━━━━━━━━━━
👤 *Cliente:* {nombre or nc} · {edad_c} años
📋 *Previsión:* {prevision}
🔹 *Plan:* {p['nombre']}{cupon_str_plan(plan_wa)}

👥 *Asegurados:*{asegurados_str(plan_wa)}

💰 *Prima mensual:*
   → {precio_str_wa(plan_wa)}
   → Anual aprox.: {clp(r['total']*12, val_uf)}

━━━━━━━━━━━━━━━━━━━━━
✅ *Coberturas:*
{chr(10).join("   " + pt for pt in pts)}

📌 *Topes:*
   • Base: {p['tope_base']}
   • Catastrófico: {p['tope_cat']}
   • Deducible amb.: {p['ded_amb']}
   • Deducible hosp.: {p['ded_hosp']}

🏥 *Red:* {p['red']}
📋 *DPS:* {'No requerida — cubre preexistencias' if not p['dps'] else 'Requerida'}
⏳ *Carencias:* {p['carencias']}

━━━━━━━━━━━━━━━━━━━━━
🤝 ¿Te interesa avanzar?
📱 {asesor}
📞 {telefono}

_Cotización tarifario Bupa Seguros mayo 2026. UF ${val_uf:,}. El riesgo es cubierto por Bupa Compañía de Seguros de Vida S.A._""".replace(",",".")

        else:  # Comparativa multi-plan — todos los seleccionados en un solo mensaje
            bloques = ""
            for i, pk in enumerate(planes_seleccionados, 1):
                p = CATALOGO[pk]
                r = precios[pk]
                es_conv = pk in CONVENIOS
                es_rec_str = "\n⭐ *RECOMENDADO*" if pk == rec else ""
                conv_str = "\n🤝 _Convenio: sin DPS · cubre preexistencias_" if es_conv else ""
                pts = build_puntos(pk)
                cupon_bloque = f"\n🎁 Cupón: {r['cupon']} ({r['pct']}% dcto)" if r.get("pct",0) > 0 else ""
                tramo_bloque = f" · {r.get('tramo','')}" if es_conv else ""
                bloques += f"""
🔹 *OPCIÓN {i} — {p['nombre']}*{tramo_bloque}{es_rec_str}{conv_str}

💰 {precio_str_wa(pk)}{cupon_bloque}
{chr(10).join("✅ " + pt for pt in pts[:7])}
📌 Tope: {p['tope_base']} · Ded.: {p['ded_amb']}
📋 DPS: {'No requerida' if not p['dps'] else 'Requerida'}
⏳ Carencias: {p['carencias']}
⛔ Exclusiones: Preexistencias declaradas · estéticos · exclusiones póliza

━━━━━━━━━━━━━━━━━━━━━"""

            if rec in planes_seleccionados:
                p_rec = CATALOGO[rec]
                recom_txt = f"\n💡 *Recomendación:* El plan *{p_rec['nombre']}* ofrece el mejor equilibrio para tu perfil.\n"
            else:
                recom_txt = ""

            msg = f"""Hola {nc} 👋

Te comparto tus opciones de *Bupa Seguros* 🏥
📅 Fecha: {hoy}

━━━━━━━━━━━━━━━━━━━━━
👤 *Cliente:* {nombre or nc} · {edad_c} años
📋 *Previsión:* {prevision}
━━━━━━━━━━━━━━━━━━━━━
{bloques}
{recom_txt}
🤝 Conversemos y te ayudo a elegir la mejor opción.
📱 {asesor}
📞 {telefono}

_Cotización tarifario Bupa Seguros mayo 2026. UF ${val_uf:,}. El riesgo es cubierto por Bupa Compañía de Seguros de Vida S.A._""".replace(",",".")

        st.code(msg, language=None)

        # ==========================================
        # BOTÓN WHATSAPP
        # ==========================================
        
        if telefono_cliente:
        
            telefono_destino = f"56{telefono_cliente}"
        
            mensaje_url = quote(msg, safe="")
        
            wa_link = (
                f"https://web.whatsapp.com/send?"
                f"phone={telefono_destino}&text={mensaje_url}"
            )
        
            st.link_button(
                "📲 Abrir WhatsApp",
                wa_link
            )
        
        else:
        
            st.warning("⚠️ Ingresa el número del cliente.")
        
        # ==========================================
        # PDFs OFICIALES
        # ==========================================

        st.markdown("## 📄 PDFs Oficiales")
        
        for plan_key in planes_seleccionados:

            if plan_key in PLANES:
                nombre_plan = PLANES[plan_key]["nombre"]

            elif plan_key in CONVENIOS:
                nombre_plan = CONVENIOS[plan_key]["nombre"]

            else:
                continue

            if nombre_plan in PDFS_PLANES:

                ruta_pdf = PDFS_PLANES[nombre_plan]

                if os.path.exists(ruta_pdf):

                    with open(ruta_pdf, "rb") as pdf_file:

                        st.download_button(
                            label=f"📄 Descargar {nombre_plan}",
                            data=pdf_file,
                            file_name=os.path.basename(ruta_pdf),
                            mime="application/pdf",
                            key=f"pdf_{plan_key}"
                        )
        # ==========================================
        # PACK CLIENTE ZIP
        # ==========================================
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        
            for plan_key in planes_seleccionados:
        
                if plan_key in PLANES:
                    nombre_plan = PLANES[plan_key]["nombre"]
        
                else:
                    nombre_plan = plan_key
        
                if nombre_plan in PDFS_PLANES:
        
                    ruta_pdf = PDFS_PLANES[nombre_plan]
        
                    if os.path.exists(ruta_pdf):
        
                        zip_file.write(
                            ruta_pdf,
                            arcname=os.path.basename(ruta_pdf)
                        )
        
        zip_buffer.seek(0)
        
        st.download_button(
            label="📦 Descargar Pack Cliente",
            data=zip_buffer,
            file_name=f"{nombre.replace(' ', '_')}_Cotizacion_Bupa.zip",
            mime="application/zip"
        )
        
        st.success(f"✅ Mensaje listo con {len(planes_seleccionados)} plan(es) seleccionado(s).")


# ── PYME (solo informativo) ───────────────────────────────────────
if f_pyme:
    st.markdown("---")
    st.markdown("## 🏢 Plan PYME Bupa")
    st.info("Sin DPS colectivo · Cubre preexistencias · Mínimo 2 trabajadores")
    st.markdown("""
- ✅ No requieren DPS individual — cubre a todos los trabajadores
- ✅ Cubre preexistencias desde el primer día
- ✅ Precio especial por volumen según número de trabajadores
- ✅ Deducible $0 en red Bupa/IntegraMédica

**Para cotizar necesitas:** RUT empresa · N° trabajadores · Rango de edades · Previsión predominante

💡 Contacta a tu ejecutivo Bupa o ingresa a BupaSales para cotizar.
""")

# ─── FOOTER ──────────────────────────────────────────────────────
st.markdown("---")
st.caption("🔒 Uso interno · Información actualizada según PDFs oficiales Bupa Seguros · El riesgo es cubierto por Bupa Compañía de Seguros de Vida S.A.")
