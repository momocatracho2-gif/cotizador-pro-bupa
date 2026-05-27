"""
╔══════════════════════════════════════════════════════════════╗
║     COTIZADOR PRO — BUPA SEGUROS CHILE  v5                  ║
║     Multi-asesor · Panel Admin · Branding Premium           ║
╚══════════════════════════════════════════════════════════════╝
    pip install streamlit pandas
    streamlit run cotizador_bupa_pro.py
"""
import streamlit as st
import pandas as pd
import os, io, zipfile, json, hashlib
from datetime import date
from urllib.parse import quote
try:
    import requests as _requests
    _REQUESTS_OK = True
except ImportError:
    _REQUESTS_OK = False

st.set_page_config(
    page_title="Cotizador PRO · Bupa Seguros",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
# UF AUTOMÁTICA — mindicador.cl (cachea 1 hora)
# ══════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def get_uf_hoy():
    """Obtiene UF del día desde mindicador.cl con fallback a valor manual."""
    if not _REQUESTS_OK:
        return None, None
    try:
        r = _requests.get("https://mindicador.cl/api/uf", timeout=5)
        data = r.json()
        valor = float(data["serie"][0]["valor"])
        fecha = data["serie"][0]["fecha"][:10]
        return valor, fecha
    except Exception:
        return None, None

# ══════════════════════════════════════════════════════════════════
# LOGO BUPA — embebido base64
# ══════════════════════════════════════════════════════════════════
BUPA_LOGO_B64 = "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"
LOGO_HTML = (
    '<img src="data:image/png;base64,' + BUPA_LOGO_B64 + '" '
    'style="height:44px;object-fit:contain;" alt="Bupa Seguros">'
)
LOGO_HTML_SM = (
    '<img src="data:image/png;base64,' + BUPA_LOGO_B64 + '" '
    'style="height:28px;object-fit:contain;" alt="Bupa Seguros">'
)

# ══════════════════════════════════════════════════════════════════
# CSS GLOBAL
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
.stApp{background-color:#F4F8FC;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#4EA5F5,#74B9FF);border-right:1px solid #d9e6f2;}
[data-testid="stSidebar"] *{color:#083B66 !important;}
h1{color:#003A70 !important;font-weight:800 !important;}
h2{color:#005EB8 !important;font-weight:700 !important;}
h3{color:#0066C2 !important;font-weight:600 !important;}
p,label,span,div{color:#1f2d3d;}
.stTextInput input,.stNumberInput input,textarea{background:white !important;color:#222 !important;border:1px solid #c9d7e6 !important;border-radius:12px !important;}
.stSelectbox div[data-baseweb="select"]{background:white !important;color:#222 !important;border-radius:12px !important;}
div[data-testid="stMetric"]{background:white;border-radius:16px;padding:18px;box-shadow:0 4px 14px rgba(0,0,0,.06);border-left:5px solid #00AEEF;}
.stButton>button,.stDownloadButton>button{background:#009FE3 !important;color:white !important;border:none !important;border-radius:12px !important;font-weight:600 !important;padding:0.6rem 1rem !important;}
.stButton>button:hover,.stDownloadButton>button:hover{background:#0088c6 !important;}
a[data-testid="stLinkButton"]{background:#25D366 !important;color:white !important;border-radius:12px !important;padding:12px 18px !important;text-decoration:none !important;font-weight:700 !important;}
[data-testid="stAlert"]{border-radius:14px !important;}
/* ── Forzar tema claro en toda la app (evita modo oscuro del SO) ── */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color:#F4F8FC !important; color-scheme: light !important;
}
.stSelectbox div[data-baseweb="select"] > div {background:white !important;color:#222 !important;}
.stSelectbox div[data-baseweb="select"] span {color:#222 !important;}
.stSelectbox svg {fill:#555 !important;}
[data-baseweb="popover"], [data-baseweb="menu"] {background:white !important;}
[data-baseweb="menu"] li, [data-baseweb="menu"] [role="option"] {background:white !important;color:#222 !important;}
[data-baseweb="menu"] li:hover {background:#EBF4FF !important;}
textarea {background:white !important;color:#222 !important;}
[data-testid="stRadio"] label, [data-testid="stCheckbox"] label {color:#1f2d3d !important;}
[data-testid="stExpander"] {background:white !important;border:1px solid #d9e6f2 !important;border-radius:12px !important;}
[data-testid="stExpander"] summary {color:#003A70 !important;font-weight:700 !important;}
/* ── Desktop: ocultar hamburguesa y header nativo ── */
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header[data-testid="stHeader"] {background: transparent !important;}
[data-testid="stToolbar"] {display: none !important;}
[data-testid="stDecoration"] {display: none !important;}
[data-testid="stStatusWidget"] {display: none !important;}
/* ── Móvil: mostrar hamburguesa para abrir sidebar con filtros ── */
@media (max-width: 768px) {
    #MainMenu {visibility: visible !important; display: block !important;}
    header[data-testid="stHeader"] {
        background: #003A70 !important;
        visibility: visible !important;
    }
    [data-testid="stToolbar"] {display: flex !important;}
    [data-testid="stSidebar"] {
        width: 100vw !important;
        min-width: 100vw !important;
    }
    .stTextInput input,
    .stNumberInput input,
    textarea,
    .stSelectbox div[data-baseweb="select"] {
        font-size: 16px !important;
    }
    [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
    }
    [data-testid="stHorizontalBlock"] > div {
        width: 100% !important;
        min-width: 100% !important;
    }
    div[data-testid="stMetric"] {
        min-width: 45% !important;
        padding: 12px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# BASE DE ASESORES — Streamlit Secrets (compatible Cloud y local)
# ══════════════════════════════════════════════════════════════════
# En Streamlit Cloud: configura en Settings > Secrets
# En local: crea el archivo .streamlit/secrets.toml
#
# Formato secrets.toml:
# ADMIN_KEY = "bupapro2026"
#
# [asesores.romulo]
# password = "seguros2026"
# nombre = "Rómulo Lupi"
# telefono = "+569 90790892"
# ciudad = "Santiago"
# email = "romulo.lupi@bupa.cl"
# activo = true
#
# [asesores.demo]
# password = "demo123"
# nombre = "Asesor Demo"
# telefono = "+569 00000000"
# ciudad = "Santiago"
# email = "demo@bupa.cl"
# activo = true
# ══════════════════════════════════════════════════════════════════

ADMIN_KEY = st.secrets.get("ADMIN_KEY", "bupapro2026")

ASESORES_FILE = os.path.join(os.path.dirname(__file__), "asesores.json")

def load_asesores():
    """Carga asesores desde asesores.json (Railway) o st.secrets (Streamlit Cloud) como fallback."""
    # 1. Intentar desde asesores.json (Railway)
    if os.path.exists(ASESORES_FILE):
        try:
            with open(ASESORES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data:
                return {u: {
                    "password": d.get("password",""),
                    "nombre":   d.get("nombre", u),
                    "telefono": d.get("telefono",""),
                    "ciudad":   d.get("ciudad","Santiago"),
                    "email":    d.get("email",""),
                    "activo":   d.get("activo", True),
                } for u, d in data.items()}
        except Exception:
            pass
    # 2. Fallback: Streamlit Secrets (Streamlit Cloud)
    try:
        raw = st.secrets.get("asesores", {})
        asesores = {}
        for usuario, datos in raw.items():
            asesores[usuario] = {
                "password":  datos.get("password", ""),
                "nombre":    datos.get("nombre", usuario),
                "telefono":  datos.get("telefono", ""),
                "ciudad":    datos.get("ciudad", "Santiago"),
                "email":     datos.get("email", ""),
                "activo":    datos.get("activo", True),
            }
        if asesores:
            return asesores
    except Exception:
        pass
    # 3. Fallback hardcodeado
    return {
        "romulo": {
            "password": "seguros2026",
            "nombre":   "Rómulo Lupi",
            "telefono": "+569 90790892",
            "ciudad":   "Santiago",
            "email":    "romulo.lupi@bupa.cl",
            "activo":   True,
        },
        "demo": {
            "password": "demo123",
            "nombre":   "Asesor Demo Bupa",
            "telefono": "+569 00000000",
            "ciudad":   "Santiago",
            "email":    "demo@bupa.cl",
            "activo":   True,
        },
    }

def save_asesores(data):
    """Guarda en asesores.json si existe el archivo (Railway), si no genera TOML para Streamlit."""
    if os.path.exists(ASESORES_FILE):
        try:
            with open(ASESORES_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            st.session_state["secrets_pendientes"] = "__json_ok__"
            return
        except Exception as e:
            st.error(f"Error guardando asesores.json: {e}")
    # Fallback: generar TOML para Streamlit Cloud
    lines = ['ADMIN_KEY = "' + ADMIN_KEY + '"', "", "[asesores]"]
    for usuario, d in data.items():
        lines.append("")
        lines.append("[asesores." + usuario + "]")
        lines.append('password = "' + d.get("password","") + '"')
        lines.append('nombre = "' + d.get("nombre","") + '"')
        lines.append('telefono = "' + d.get("telefono","") + '"')
        lines.append('ciudad = "' + d.get("ciudad","Santiago") + '"')
        lines.append('email = "' + d.get("email","") + '"')
        lines.append("activo = " + ("true" if d.get("activo",True) else "false"))
    st.session_state["secrets_pendientes"] = "\n".join(lines)

# ══════════════════════════════════════════════════════════════════
# LOGIN / ADMIN
# ══════════════════════════════════════════════════════════════════
if "login_ok"  not in st.session_state: st.session_state.login_ok  = False
if "usuario"   not in st.session_state: st.session_state.usuario   = ""
if "es_admin"  not in st.session_state: st.session_state.es_admin  = False

asesores = load_asesores()

if not st.session_state.login_ok:
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown(
            '<div style="text-align:center;margin-bottom:24px;">' +
            '<div style="background:white;border-radius:16px;padding:16px 24px;display:inline-block;'
            'box-shadow:0 4px 20px rgba(0,94,184,0.15);margin-bottom:12px;">' +
            LOGO_HTML +
            '</div><br>'
            '<div style="color:#005EB8;font-size:22px;font-weight:800;">Cotizador PRO</div>'
            '<div style="color:#6b8caa;font-size:13px;">Plataforma de Asesoría Comercial</div>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown("---")
        usuario = st.text_input("Usuario", placeholder="tu_usuario")
        clave   = st.text_input("Contraseña", type="password")

        if st.button("Ingresar", use_container_width=True):
            # Admin master
            if usuario == "admin" and clave == ADMIN_KEY:
                st.session_state.login_ok = True
                st.session_state.usuario  = "admin"
                st.session_state.es_admin = True
                st.rerun()
            # Asesor normal
            elif usuario in asesores:
                a = asesores[usuario]
                if a["password"] == clave and a.get("activo", True):
                    st.session_state.login_ok = True
                    st.session_state.usuario  = usuario
                    st.session_state.es_admin = False
                    st.rerun()
                elif not a.get("activo", True):
                    st.error("Cuenta inactiva. Contacta al administrador.")
                else:
                    st.error("Usuario o contraseña incorrecta")
            else:
                st.error("Usuario o contraseña incorrecta")
    st.stop()

# ══════════════════════════════════════════════════════════════════
# PANEL ADMIN
# ══════════════════════════════════════════════════════════════════
if st.session_state.es_admin:
    asesores = load_asesores()

    st.markdown(
        '<div style="background:linear-gradient(135deg,#003A70,#005EB8);padding:18px 24px;'
        'border-radius:16px;margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;">'
        '<div style="display:flex;align-items:center;gap:16px;">'
        '<div style="background:white;border-radius:10px;padding:8px 14px;">' + LOGO_HTML + '</div>'
        '<div>'
        '<div style="color:white;font-size:20px;font-weight:800;">Panel de Administración</div>'
        '<div style="color:#7eb8e8;font-size:13px;">Gestión de asesores · Cotizador PRO</div>'
        '</div></div>'
        '<div style="color:#FFE566;font-size:14px;font-weight:700;">ADMIN MASTER</div>'
        '</div>',
        unsafe_allow_html=True
    )

    tab_ver, tab_nuevo, tab_editar = st.tabs(["👥 Asesores activos", "➕ Nuevo asesor", "✏️ Editar / Desactivar"])

    with tab_ver:
        st.markdown("### Asesores registrados")
        filas = []
        for u, d in asesores.items():
            filas.append({
                "Usuario":   u,
                "Nombre":    d["nombre"],
                "Teléfono":  d["telefono"],
                "Ciudad":    d["ciudad"],
                "Email":     d.get("email","—"),
                "Estado":    "Activo" if d.get("activo", True) else "Inactivo",
            })
        df_a = pd.DataFrame(filas)
        st.dataframe(df_a, use_container_width=True, hide_index=True)
        st.info(f"Total: {len(asesores)} asesores registrados")

    with tab_nuevo:
        st.markdown("### Agregar nuevo asesor")
        c1, c2 = st.columns(2)
        nu_user  = c1.text_input("Usuario (login)", placeholder="ana.perez")
        nu_pass  = c2.text_input("Contraseña", placeholder="minimo 6 caracteres")
        nu_nom   = c1.text_input("Nombre completo", placeholder="Ana Pérez González")
        nu_tel   = c2.text_input("Teléfono", placeholder="+569 9XXXXXXX")
        nu_ciu   = c1.text_input("Ciudad", placeholder="Santiago")
        nu_mail  = c2.text_input("Email Bupa", placeholder="ana.perez@bupa.cl")

        if st.button("Crear asesor", type="primary"):
            if not all([nu_user, nu_pass, nu_nom, nu_tel]):
                st.error("Completa usuario, contraseña, nombre y teléfono.")
            elif nu_user in asesores:
                st.error(f"El usuario '{nu_user}' ya existe.")
            elif len(nu_pass) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                asesores[nu_user] = {
                    "password":  nu_pass,
                    "nombre":    nu_nom,
                    "telefono":  nu_tel,
                    "ciudad":    nu_ciu or "Santiago",
                    "email":     nu_mail,
                    "activo":    True,
                }
                save_asesores(asesores)
                st.success("Asesor preparado. Copia el bloque de abajo en Streamlit Secrets.")

    with tab_editar:
        st.markdown("### Editar o desactivar asesor")
        usuario_sel = st.selectbox("Selecciona asesor", list(asesores.keys()))
        if usuario_sel:
            d = asesores[usuario_sel]
            c1, c2 = st.columns(2)
            # key incluye usuario_sel para que Streamlit resetee los campos al cambiar de asesor
            ed_nom  = c1.text_input("Nombre",    value=d["nombre"],           key="ed_nom_"  + usuario_sel)
            ed_tel  = c2.text_input("Teléfono",  value=d["telefono"],         key="ed_tel_"  + usuario_sel)
            ed_ciu  = c1.text_input("Ciudad",    value=d.get("ciudad",""),    key="ed_ciu_"  + usuario_sel)
            ed_mail = c2.text_input("Email",     value=d.get("email",""),     key="ed_mail_" + usuario_sel)
            ed_pass = c1.text_input("Nueva contraseña (dejar vacío = no cambiar)", key="ed_pass_" + usuario_sel)
            ed_act  = c2.checkbox("Cuenta activa", value=d.get("activo",True), key="ed_act_"  + usuario_sel)

            col_g, col_e = st.columns(2)
            if col_g.button("Guardar cambios", type="primary"):
                asesores[usuario_sel]["nombre"]   = ed_nom
                asesores[usuario_sel]["telefono"] = ed_tel
                asesores[usuario_sel]["ciudad"]   = ed_ciu
                asesores[usuario_sel]["email"]    = ed_mail
                asesores[usuario_sel]["activo"]   = ed_act
                if ed_pass:
                    asesores[usuario_sel]["password"] = ed_pass
                save_asesores(asesores)
                st.success("Cambios listos. Copia el bloque TOML de abajo en Streamlit Secrets y haz Reboot.")

            if col_e.button("Eliminar asesor", type="secondary"):
                if usuario_sel == "romulo":
                    st.error("No puedes eliminar al asesor principal.")
                else:
                    del asesores[usuario_sel]
                    save_asesores(asesores)
                    st.warning("Asesor eliminado. Copia el bloque TOML de abajo en Streamlit Secrets y haz Reboot.")

            # Mostrar resultado según entorno
            if st.session_state.get("secrets_pendientes"):
                if st.session_state["secrets_pendientes"] == "__json_ok__":
                    st.success("✅ Cambios guardados en asesores.json — activos de inmediato.")
                    st.session_state.pop("secrets_pendientes", None)
                else:
                    st.markdown("---")
                    st.markdown("#### Paso 1 — Copia este bloque:")
                    st.code(st.session_state["secrets_pendientes"], language="toml")
                    st.markdown("#### Paso 2 — Pégalo aquí:")
                    st.link_button(
                        "Ir a Streamlit Cloud → Settings → Secrets",
                        "https://share.streamlit.io"
                    )
                    st.info("Después de pegar, haz clic en Save → luego Reboot app para aplicar los cambios.")

    # ── Visualizador resultado guardado ───────────────────────────
    if st.session_state.get("secrets_pendientes"):
        if st.session_state["secrets_pendientes"] == "__json_ok__":
            st.success("✅ Cambios guardados en asesores.json — activos de inmediato.")
            st.session_state.pop("secrets_pendientes", None)
        else:
            st.markdown("---")
            st.markdown("### 📋 Copia esto en Streamlit Cloud → Settings → Secrets")
            st.info("Ve a tu app en share.streamlit.io → Settings → Secrets y reemplaza todo con este bloque:")
            st.code(st.session_state["secrets_pendientes"], language="toml")
            st.warning("Después de pegar los secrets, haz Reboot de la app en Streamlit Cloud para aplicar los cambios.")

    st.markdown("---")
    if st.button("Cerrar sesión admin"):
        st.session_state.login_ok = False
        st.session_state.es_admin = False
        st.session_state.pop("secrets_pendientes", None)
        st.rerun()
    st.stop()

# ══════════════════════════════════════════════════════════════════
# PERFIL DEL ASESOR LOGUEADO
# ══════════════════════════════════════════════════════════════════
asesores  = load_asesores()
asesor_d  = asesores.get(st.session_state.usuario, {})
ASESOR_NOMBRE   = asesor_d.get("nombre",   "Asesor Bupa")
ASESOR_TELEFONO = asesor_d.get("telefono", "+569 00000000")
ASESOR_CIUDAD   = asesor_d.get("ciudad",   "Santiago")
ASESOR_EMAIL    = asesor_d.get("email",    "")

# ══════════════════════════════════════════════════════════════════
# PDFs
# ══════════════════════════════════════════════════════════════════
PDFS_PLANES = {
    "Bupa + Protección 70/25":     "https://tinyurl.com/bupa-bp7025",
    "Bupa + Protección 70/70":     "https://tinyurl.com/bupa-bp7070",
    "Bupa + Protección 80/70":     "https://tinyurl.com/bupa-bp8070",
    "Bupa Ambulatorio 70":         "https://tinyurl.com/bupa-amb70",
    "Bupa Cuidado Total 60":       "https://tinyurl.com/bupa-bct60",
    "Bupa Cuidado Total 70":       "https://tinyurl.com/bupa-bct70",
    "Bupa Cuidado Total 80":       "https://tinyurl.com/bupa-bct80",
    "Bupa MultiSalud":             "https://tinyurl.com/bupa-multi",
    "Bupa MultiSalud Pro":         "https://tinyurl.com/bupa-multipro",
    "Mi Dental IntegraMédica 68%": "https://tinyurl.com/bupa-dental",
    "IntegraMédica 100%":          "https://tinyurl.com/bupa-im100",
    "Plan Adulto Mayor 70%":       "https://tinyurl.com/bupa-am70",
    "Bupa Complementa":            "https://tinyurl.com/bupa-complementa",
    "PYME Digital":                "https://tinyurl.com/bupa-pyme",
}

# ══════════════════════════════════════════════════════════════════
# BASE DE DATOS DE PLANES
# ══════════════════════════════════════════════════════════════════
PLANES = {
    "70/25": {
        "nombre":"Bupa + Protección 70/25","emoji":"🔵","prevision":["FONASA"],
        "f_cat":True,"f_libre":False,"f_maternidad":True,"f_salud_mental":False,"f_quirurgico":True,"f_sin_dps":False,
        "contratante":{"0-2":None,"3-17":None,"18-25":0.75,"26-35":0.96,"36-45":1.10,"46-55":1.24,"56-59":1.41,"60-64":1.52,"65-70":2.05,"71-75":2.88},
        "dependiente":{"0-2":0.49,"3-17":0.49,"18-25":0.70,"26-35":0.92,"36-45":1.06,"46-55":1.20,"56-59":1.37,"60-64":1.48,"65-70":2.01,"71-75":2.84},
        "hosp":"70%","amb":"25%","cat":"✅ 100% hasta UF 9.500","tope_base":"UF 500/año","tope_cat":"UF 9.500/año",
        "muerte":"✅ UF 500","red":"Clínica Bupa Santiago + IntegraMédica","maternidad":"70%",
        "oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)","ded_amb":"UF 0,5/año","ded_hosp":"UF 5/año",
        "dps":True,"salud_mental":False,
        "para_quien":"Presupuesto limitado. Prioriza hospitalización. Uso ambulatorio bajo.",
        "no_para":"Quienes van mucho al médico ambulatorio (cubre solo 25%).","carencias":"Bariátrica, ocular láser, rinolaringológica: 1 año.",
        "tag":"Precio mínimo con catastrófico · FONASA",
    },
    "70/70": {
        "nombre":"Bupa + Protección 70/70","emoji":"🟣","prevision":["FONASA"],
        "f_cat":True,"f_libre":False,"f_maternidad":True,"f_salud_mental":False,"f_quirurgico":True,"f_sin_dps":False,
        "contratante":{"0-2":None,"3-17":None,"18-25":1.02,"26-35":1.31,"36-45":1.49,"46-55":1.69,"56-59":1.90,"60-64":2.05,"65-70":2.75,"71-75":3.85},
        "dependiente":{"0-2":0.64,"3-17":0.64,"18-25":0.97,"26-35":1.26,"36-45":1.45,"46-55":1.65,"56-59":1.85,"60-64":2.00,"65-70":2.71,"71-75":3.81},
        "hosp":"70%","amb":"70%","cat":"✅ 100% hasta UF 9.500","tope_base":"UF 500/año","tope_cat":"UF 9.500/año",
        "muerte":"✅ UF 500","red":"Clínica Bupa Santiago + IntegraMédica","maternidad":"70%",
        "oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)","ded_amb":"UF 0,5/año","ded_hosp":"UF 5/año",
        "dps":True,"salud_mental":False,
        "para_quien":"Familias con uso ambulatorio frecuente. Cobertura equilibrada.",
        "no_para":"Quien busca el máximo porcentaje hospitalario.","carencias":"Bariátrica, ocular láser, rinolaringológica: 1 año.",
        "tag":"⭐ El más equilibrado · FONASA",
    },
    "80/70": {
        "nombre":"Bupa + Protección 80/70","emoji":"🔴","prevision":["FONASA"],
        "f_cat":True,"f_libre":False,"f_maternidad":True,"f_salud_mental":False,"f_quirurgico":True,"f_sin_dps":False,
        "contratante":{"0-2":None,"3-17":None,"18-25":1.21,"26-35":1.55,"36-45":1.77,"46-55":2.01,"56-59":2.25,"60-64":2.43,"65-70":3.27,"71-75":4.57},
        "dependiente":{"0-2":0.76,"3-17":0.76,"18-25":1.16,"26-35":1.50,"36-45":1.73,"46-55":1.96,"56-59":2.21,"60-64":2.39,"65-70":3.22,"71-75":4.53},
        "hosp":"80%","amb":"70%","cat":"✅ 100% hasta UF 9.500","tope_base":"UF 500/año","tope_cat":"UF 9.500/año",
        "muerte":"✅ UF 500","red":"Clínica Bupa Santiago + IntegraMédica","maternidad":"80%",
        "oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)","ded_amb":"UF 0,5/año","ded_hosp":"UF 5/año",
        "dps":True,"salud_mental":False,
        "para_quien":"Máxima cobertura en red Bupa. Historial de cirugías o enfermedades crónicas.",
        "no_para":"Quien busca red más amplia que Bupa/IntegraMédica.","carencias":"Bariátrica, ocular láser, rinolaringológica: 1 año.",
        "tag":"⭐ Mayor cobertura hospitalaria · FONASA",
    },
    "AMB70": {
        "nombre":"Bupa Ambulatorio 70","emoji":"🟢","prevision":["FONASA"],
        "f_cat":False,"f_libre":False,"f_maternidad":False,"f_salud_mental":False,"f_quirurgico":False,"f_sin_dps":False,
        "contratante":{"0-2":0.86,"3-17":0.41,"18-25":0.57,"26-35":0.60,"36-45":0.68,"46-55":0.77,"56-59":0.86,"60-64":0.91,"65-70":0.96,"71-75":1.26},
        "dependiente":{"0-2":0.86,"3-17":0.41,"18-25":0.57,"26-35":0.60,"36-45":0.68,"46-55":0.77,"56-59":0.86,"60-64":0.91,"65-70":0.96,"71-75":1.26},
        "hosp":"❌ No cubre","amb":"70%","cat":"❌ No incluye","tope_base":"UF 250/año","tope_cat":"— No aplica",
        "muerte":"❌ No incluye","red":"Clínica Bupa Santiago + IntegraMédica","maternidad":"❌ No cubre",
        "oncologia":"❌ No cubre","dental":"62% dcto IntegraMédica","medicamentos":"No incluye",
        "ded_amb":"UF 0,5/año","ded_hosp":"— No aplica","dps":True,"salud_mental":False,
        "para_quien":"Jóvenes sanos. Complemento básico. Presupuesto muy ajustado.",
        "no_para":"Personas con riesgo de hospitalización, embarazo o cirugías.","carencias":"No aplica (no cubre hospitalización).",
        "tag":"Solo ambulatorio · Precio mínimo · FONASA",
    },
    "MULTI": {
        "nombre":"Bupa MultiSalud","emoji":"🟡","prevision":["FONASA"],
        "f_cat":True,"f_libre":False,"f_maternidad":True,"f_salud_mental":True,"f_quirurgico":True,"f_sin_dps":False,
        "contratante":{"0-2":None,"3-17":None,"18-25":1.40,"26-35":1.80,"36-45":2.07,"46-55":2.76,"56-59":3.28,"60-64":3.62,"65-70":3.96,"71-75":5.29},
        "dependiente":{"0-2":1.35,"3-17":0.94,"18-25":1.40,"26-35":1.80,"36-45":2.07,"46-55":2.76,"56-59":3.28,"60-64":3.62,"65-70":3.96,"71-75":5.29},
        "hosp":"90%/80%/50% (según red)","amb":"70%/60%/50% (según red)",
        "cat":"✅ Extensión catastrófica en 2 capas hasta UF 7.500","tope_base":"UF 1.500/año",
        "tope_cat":"UF 7.500 total (Capa 1 UF 2.500 + Capa 2 UF 5.000)","muerte":"❌ No incluye",
        "red":"Red Pref: Bupa+Reñaca+IntegraMédica | Red 1: Dávila+Interclinica | Red 2: Sta.María+otros",
        "maternidad":"90%/80%/50%","oncologia":"90%/80%/50%","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)","ded_amb":"UF 1/año","ded_hosp":"UF 5/año",
        "dps":True,"salud_mental":True,
        "para_quien":"FONASA B,C,D con acceso a Dávila, Santa María. Red ampliada + salud mental.",
        "no_para":"Quien busca máxima cobertura en red única.","carencias":"Bariátrica, ocular láser, rinolaringológica, reasignación sexo: 1 año.",
        "tag":"Red ampliada + Salud mental · FONASA",
    },
    "MULTIPRO": {
        "nombre":"Bupa MultiSalud Pro","emoji":"🟠","prevision":["FONASA"],
        "f_cat":True,"f_libre":False,"f_maternidad":True,"f_salud_mental":True,"f_quirurgico":True,"f_sin_dps":False,
        "contratante":{"0-2":None,"3-17":None,"18-25":1.71,"26-35":2.07,"36-45":2.44,"46-55":3.24,"56-59":3.93,"60-64":4.30,"65-70":4.50,"71-75":6.22},
        "dependiente":{"0-2":1.58,"3-17":1.05,"18-25":1.71,"26-35":2.07,"36-45":2.44,"46-55":3.24,"56-59":3.93,"60-64":4.30,"65-70":4.50,"71-75":6.22},
        "hosp":"90%/80%/70% (según red)","amb":"90%/70%/60% (según red)",
        "cat":"✅ Extensión catastrófica en 2 capas hasta UF 7.500","tope_base":"UF 1.500/año",
        "tope_cat":"UF 7.500 total (Capa 1 UF 2.500 + Capa 2 UF 5.000)","muerte":"❌ No incluye",
        "red":"Red Pref: Bupa+Reñaca+IntegraMédica | Red 1: Dávila+Interclinica | Red 2: Sta.María+otros",
        "maternidad":"90%/80%/70%","oncologia":"90%/80%/70%","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)","ded_amb":"UF 1/año","ded_hosp":"UF 5/año",
        "dps":True,"salud_mental":True,
        "para_quien":"FONASA B,C,D con la mejor cobertura posible + red ampliada + salud mental.",
        "no_para":"Presupuesto ajustado.","carencias":"Bariátrica, ocular láser, rinolaringológica, reasignación sexo: 1 año.",
        "tag":"⭐ Mayor cobertura Pro · FONASA",
    },
    "BCT60": {
        "nombre":"Bupa Cuidado Total 60","emoji":"🔷","prevision":["FONASA","ISAPRE"],
        "f_cat":False,"f_libre":True,"f_maternidad":True,"f_salud_mental":True,"f_quirurgico":True,"f_sin_dps":False,
        "contratante":{"0-2":None,"3-17":0.75,"18-25":0.86,"26-35":1.04,"36-45":1.04,"46-55":1.16,"56-59":1.22,"60-64":1.32,"65-70":1.75,"71-75":2.44},
        "dependiente":{"0-2":0.75,"3-17":0.75,"18-25":0.86,"26-35":1.04,"36-45":1.04,"46-55":1.16,"56-59":1.22,"60-64":1.32,"65-70":1.75,"71-75":2.44},
        "hosp":"60%","amb":"60%","cat":"❌ No incluye","tope_base":"UF 250/año","tope_cat":"— No aplica",
        "muerte":"❌ No incluye","red":"Libre elección + cobertura extra Red Bupa","maternidad":"60%",
        "oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 30% marca con receta (tope $25.000/mes)",
        "ded_amb":"UF 1/año (gratis en Red Bupa)","ded_hosp":"UF 1/año (gratis en Red Bupa)",
        "dps":True,"salud_mental":True,
        "para_quien":"ISAPRE o FONASA que quieren libre elección. Salud mental incluida.",
        "no_para":"Quien necesita extensión catastrófica o tiene preexistencias.","carencias":"Bariátrica, Septoplastía, Disforia de Género: 1 año.",
        "tag":"Libre elección · Salud mental · ISAPRE y FONASA",
    },
    "BCT70": {
        "nombre":"Bupa Cuidado Total 70","emoji":"💙","prevision":["FONASA","ISAPRE"],
        "f_cat":False,"f_libre":True,"f_maternidad":True,"f_salud_mental":True,"f_quirurgico":True,"f_sin_dps":False,
        "contratante":{"0-2":None,"3-17":0.92,"18-25":1.09,"26-35":1.31,"36-45":1.31,"46-55":1.46,"56-59":1.56,"60-64":1.68,"65-70":2.24,"71-75":3.12},
        "dependiente":{"0-2":0.92,"3-17":0.92,"18-25":1.09,"26-35":1.31,"36-45":1.31,"46-55":1.46,"56-59":1.56,"60-64":1.68,"65-70":2.24,"71-75":3.12},
        "hosp":"70%","amb":"70%","cat":"❌ No incluye","tope_base":"UF 400/año","tope_cat":"— No aplica",
        "muerte":"❌ No incluye","red":"Libre elección + cobertura extra Red Bupa","maternidad":"70%",
        "oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 30% marca con receta (tope $25.000/mes)",
        "ded_amb":"UF 1/año (gratis en Red Bupa)","ded_hosp":"UF 1/año (gratis en Red Bupa)",
        "dps":True,"salud_mental":True,
        "para_quien":"ISAPRE o FONASA que quieren libre elección equilibrada. Tope UF 400.",
        "no_para":"Quien necesita extensión catastrófica o tiene preexistencias.","carencias":"Bariátrica, Septoplastía, Disforia de Género: 1 año.",
        "tag":"⭐ Libre elección equilibrada · ISAPRE y FONASA",
    },
    "BCT80": {
        "nombre":"Bupa Cuidado Total 80","emoji":"💜","prevision":["FONASA","ISAPRE"],
        "f_cat":False,"f_libre":True,"f_maternidad":True,"f_salud_mental":True,"f_quirurgico":True,"f_sin_dps":False,
        "contratante":{"0-2":None,"3-17":1.10,"18-25":1.35,"26-35":1.61,"36-45":1.61,"46-55":1.79,"56-59":1.93,"60-64":2.08,"65-70":2.78,"71-75":3.87},
        "dependiente":{"0-2":1.10,"3-17":1.10,"18-25":1.35,"26-35":1.61,"36-45":1.61,"46-55":1.79,"56-59":1.93,"60-64":2.08,"65-70":2.78,"71-75":3.87},
        "hosp":"80%","amb":"80%","cat":"❌ No incluye","tope_base":"UF 600/año","tope_cat":"— No aplica",
        "muerte":"❌ No incluye","red":"Libre elección + cobertura extra Red Bupa","maternidad":"80%",
        "oncologia":"Según prestaciones médicas cubiertas del plan","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 30% marca con receta (tope $25.000/mes)",
        "ded_amb":"UF 1/año (gratis en Red Bupa)","ded_hosp":"UF 1/año (gratis en Red Bupa)",
        "dps":True,"salud_mental":True,
        "para_quien":"ISAPRE o FONASA que quieren máxima cobertura con libre elección. Tope UF 600.",
        "no_para":"Quien necesita extensión catastrófica o tiene preexistencias.","carencias":"Bariátrica, Septoplastía, Disforia de Género: 1 año.",
        "tag":"⭐ Máxima cobertura libre elección · ISAPRE y FONASA",
    },
    "COMPLEMENTA": {
        "nombre":"Bupa Complementa","emoji":"🧩","prevision":["ISAPRE"],
        "f_cat":False,"f_libre":True,"f_maternidad":True,"f_salud_mental":True,"f_quirurgico":True,"f_sin_dps":False,
        "contratante":{"0-2":0.45,"3-17":0.45,"18-25":0.51,"26-35":0.63,"36-45":0.63,"46-55":0.70,"56-59":0.83,"60-64":0.89,"65-70":1.19,"71-75":None},
        "dependiente":{"0-2":0.45,"3-17":0.45,"18-25":0.51,"26-35":0.63,"36-45":0.63,"46-55":0.70,"56-59":0.83,"60-64":0.89,"65-70":1.19,"71-75":None},
        "hosp":"Mismo % que tu plan ISAPRE","amb":"Mismo % que tu plan ISAPRE (solo red Bupa)",
        "cat":"❌ No incluye","tope_base":"UF 500/año","tope_cat":"— No aplica","muerte":"❌ No incluye",
        "red":"Hosp: Libre elección (excl. Clínica U. Andes, Las Condes, Alemana) | Amb: solo Bupa Stgo, Reñaca e IntegraMédica",
        "maternidad":"Mismo % que tu plan ISAPRE","oncologia":"Mismo % que tu plan ISAPRE",
        "dental":"No incluye","medicamentos":"No incluye","ded_amb":"Sin deducible","ded_hosp":"Sin deducible (sin BMI)",
        "dps":True,"salud_mental":True,
        "para_quien":"ISAPRE que quiere cubrir el copago que su plan no paga. Sin deducible ni BMI.",
        "no_para":"FONASA. Quien quiere libre elección ambulatoria amplia (solo en red Bupa).",
        "carencias":"Bariátrica, rinolaringológica, reasignación sexo, vasectomía, reducción mamaria: 1 año.",
        "tag":"⭐ Exclusivo ISAPRE · Cubre tu copago · Sin deducible ni BMI",
    },
}

AM_TARIFAS   = {"Solo Titular":0.84,"Titular + 1 beneficiario":1.55,"Titular + 2 beneficiarios":2.23,"Titular + 3 beneficiarios":2.92,"Titular + 4 beneficiarios":3.62}
IM100_TARIFAS= {"Solo Titular":0.84,"Titular + 1 beneficiario":1.32,"Titular + 2 beneficiarios":1.90,"Titular + 3 beneficiarios":2.49,"Titular + 4 beneficiarios":3.09,"Titular + 5 beneficiarios":3.69}
DENTAL_TARIFAS_INICIO  = {"Solo Titular":0.50,"Titular + 1 beneficiario":0.99,"Titular + 2 beneficiarios":1.47,"Titular + 3 beneficiarios":1.96,"Titular + 4 beneficiarios":2.44}
DENTAL_TARIFAS_MENSUAL = {"Solo Titular":0.08,"Titular + 1 beneficiario":0.15,"Titular + 2 beneficiarios":0.22,"Titular + 3 beneficiarios":0.28,"Titular + 4 beneficiarios":0.35}

CONVENIOS = {
    "AM70":{"nombre":"Plan Adulto Mayor 70%","emoji":"👴","prevision":["FONASA","ISAPRE"],
        "f_cat":False,"f_libre":False,"f_maternidad":False,"f_salud_mental":False,"f_quirurgico":False,"f_sin_dps":True,
        "dps":False,"tag":"Solo ambulatorio · Sin DPS · 60-84 años",
        "hosp":"❌ No cubre","amb":"70%","cat":"❌ No incluye","tope_base":"UF 25/beneficiario/año","tope_cat":"— No aplica",
        "muerte":"❌ No incluye","maternidad":"❌ No cubre","oncologia":"❌ No cubre","salud_mental":False,
        "red":"Solo IntegraMédica nacional","dental":"No incluye",
        "medicamentos":"60% genérico / 40% marca con receta (tope $20.000/mes)",
        "ded_amb":"Sin deducible","ded_hosp":"— No aplica",
        "rescate_vital":"🚑 Unidad Coronaria Móvil (UCM) · Fono: 223914444",
        "para_quien":"60-84 años con preexistencias. Sin DPS.","no_para":"Quien necesita hospitalización o cirugías.",
        "carencias":"Sin carencias — vigencia desde contratación.","es_convenio":True,"tarifas":AM_TARIFAS},
    "IM100":{"nombre":"IntegraMédica 100%","emoji":"💊","prevision":["FONASA","ISAPRE"],
        "f_cat":False,"f_libre":False,"f_maternidad":False,"f_salud_mental":False,"f_quirurgico":False,"f_sin_dps":True,
        "dps":False,"tag":"100% ambulatorio · Sin DPS · Cubre preexistencias",
        "hosp":"❌ No cubre","amb":"100%","cat":"❌ No incluye","tope_base":"UF 60/año","tope_cat":"— No aplica",
        "muerte":"❌ No incluye","maternidad":"❌ No cubre","oncologia":"❌ No cubre","salud_mental":False,
        "red":"Solo IntegraMédica nacional","dental":"62% dcto IntegraMédica",
        "medicamentos":"50% genérico / 20% marca (tope $15.000/mes)",
        "ded_amb":"Sin deducible","ded_hosp":"— No aplica",
        "para_quien":"Cualquier edad con preexistencias. 100% copago ambulatorio.","no_para":"Quien necesita hospitalización, cirugías o maternidad.",
        "carencias":"Sin carencias — vigencia inmediata.","es_convenio":True,"tarifas":IM100_TARIFAS},
    "DENTAL":{"nombre":"Mi Dental IntegraMédica 68%","emoji":"🦷","prevision":["FONASA","ISAPRE"],
        "f_cat":False,"f_libre":False,"f_maternidad":False,"f_salud_mental":False,"f_quirurgico":False,"f_sin_dps":True,
        "dps":False,"tag":"68% dcto todos los tratamientos dentales · Sin DPS · 18-89 años",
        "hosp":"❌ No cubre","amb":"❌ Solo dental","cat":"❌ No incluye",
        "tope_base":"Sin tope (68% dcto todos los tratamientos)","tope_cat":"— No aplica",
        "muerte":"❌ No incluye","maternidad":"❌ No cubre","oncologia":"❌ No cubre","salud_mental":False,
        "red":"Red Dental IntegraMédica (Stgo, Copiapó, La Serena, Viña, Rancagua, Talca, Concepción)",
        "dental":"68% dcto TODOS los tratamientos dentales + 1 limpieza anual GRATIS",
        "medicamentos":"50% genérico / 20% marca con receta (tope $20.000/mes) SalcoBrand",
        "ded_amb":"Sin deducible","ded_hosp":"— No aplica",
        "para_quien":"Cualquier persona. Todas las edades.","no_para":"Quien necesita cobertura médica o ambulatoria.",
        "carencias":"Vigencia dental desde el 2° mes.","es_convenio":True,
        "tarifas":DENTAL_TARIFAS_MENSUAL,"tarifas_inicio":DENTAL_TARIFAS_INICIO},
}

CATALOGO = {**PLANES, **CONVENIOS}
EDAD_INGRESO = {"70/25":(18,75),"70/70":(18,75),"80/70":(18,75),"AMB70":(18,75),"MULTI":(18,75),
    "MULTIPRO":(18,75),"BCT60":(18,75),"BCT70":(18,75),"BCT80":(18,75),"COMPLEMENTA":(18,89),
    "AM70":(60,84),"IM100":(18,64),"DENTAL":(18,89)}
CUPONES = {"BCT":("BCTALL20NEW",20),"BP":("BMPHYA20NEW",20),"BMS":("BMSBASE20JUL",20),
           "AMBU":("BMPAMB10ENERO",10),"BPRO":("BMSPRO10JUL",10)}

# ══════════════════════════════════════════════════════════════════
# FUNCIONES
# ══════════════════════════════════════════════════════════════════
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

def get_precio(pk, edad, es_cont):
    col = "contratante" if es_cont else "dependiente"
    return PLANES[pk][col].get(rango(edad))

def clp(uf, val_uf):
    return "$" + f"{uf*val_uf:,.0f}".replace(",",".")

def ok(b): return "✅" if b else "❌"

def cupon_para_plan(pk, usar_cupon):
    if not usar_cupon: return ("", 0)
    if pk in ["BCT60","BCT70","BCT80"]: return CUPONES["BCT"]
    if pk in ["70/25","70/70","80/70"]: return CUPONES["BP"]
    if pk == "MULTI":                   return CUPONES["BMS"]
    if pk == "AMB70":                   return CUPONES["AMBU"]
    if pk == "MULTIPRO":                return CUPONES["BPRO"]
    return ("", 0)

def calcular(pk, edad_c, cargas, val_uf, usar_cupon):
    pc = get_precio(pk, edad_c, True)
    if pc is None: return None
    cod, pct = cupon_para_plan(pk, usar_cupon)
    pc_d = pc*(1-pct/100); total = pc_d
    det = [{"quien":"Contratante","edad":edad_c,"orig":pc,"final":pc_d,"cupon":cod,"pct":pct}]
    for c in cargas:
        pcc = get_precio(pk, c["edad"], False)
        if pcc:
            pcc_d = pcc*(1-pct/100); total += pcc_d
            det.append({"quien":c["nombre"],"edad":c["edad"],"orig":pcc,"final":pcc_d,"cupon":cod,"pct":pct})
        else:
            det.append({"quien":c["nombre"],"edad":c["edad"],"orig":None,"final":None,"cupon":"","pct":0})
    return {"total":total,"det":det,"cupon":cod,"pct":pct}

def calcular_convenio(pk, tramo_am, tramo_im, tramo_dental):
    if pk=="AM70":   uf=AM_TARIFAS[tramo_am];   return {"total":uf,"tramo":tramo_am,"cupon":"","pct":0,"det":[{"quien":tramo_am,"edad":None,"orig":uf,"final":uf}],"es_convenio":True}
    if pk=="IM100":  uf=IM100_TARIFAS[tramo_im]; return {"total":uf,"tramo":tramo_im,"cupon":"","pct":0,"det":[{"quien":tramo_im,"edad":None,"orig":uf,"final":uf}],"es_convenio":True}
    if pk=="DENTAL":
        uf_m=DENTAL_TARIFAS_MENSUAL[tramo_dental]; uf_i=DENTAL_TARIFAS_INICIO[tramo_dental]
        return {"total":uf_m,"tramo":tramo_dental,"cupon":"","pct":0,"det":[{"quien":tramo_dental,"edad":None,"orig":uf_m,"final":uf_m}],"es_convenio":True,"uf_inicio":uf_i}
    return None

def edad_valida(pk, edad):
    mn,mx = EDAD_INGRESO.get(pk,(18,75))
    if edad<mn or edad>mx: return False
    if pk in PLANES: return PLANES[pk]["contratante"].get(rango(edad)) is not None
    return True

def es_compatible(pk, edad_c, prevision_base, f_sin_dps, f_preex, f_cat, f_libre,
                  f_maternidad, f_salud_mental, f_quirurgico, f_adulto_mayor, f_im100, f_dental):
    p = CATALOGO[pk]
    if not edad_valida(pk,edad_c):               return False
    if prevision_base not in p["prevision"]:      return False
    if (f_sin_dps or f_preex) and p["dps"]:       return False
    if f_cat          and not p["f_cat"]:          return False
    if f_libre        and not p["f_libre"]:        return False
    if f_maternidad   and not p["f_maternidad"]:   return False
    if f_salud_mental and not p["f_salud_mental"]: return False
    if f_quirurgico   and not p["f_quirurgico"]:   return False
    if pk=="AM70"   and not (f_adulto_mayor or f_preex or f_sin_dps): return False
    if pk=="IM100"  and not (f_im100 or f_preex or f_sin_dps):        return False
    if pk=="DENTAL" and not (f_dental or f_sin_dps):                  return False
    return True

# ══════════════════════════════════════════════════════════════════
# DETECCIÓN MÓVIL vía query param + JS
# ══════════════════════════════════════════════════════════════════
st.components.v1.html("""
<script>
(function(){
    var w = window.innerWidth || screen.width;
    var url = new URL(window.parent.location.href);
    var actual = url.searchParams.get('_mv');
    var val = w <= 768 ? '1' : '0';
    if (actual !== val) {
        url.searchParams.set('_mv', val);
        window.parent.history.replaceState({}, '', url);
        window.parent.location.reload();
    }
})();
</script>
""", height=0)

try:
    es_movil = st.query_params.get("_mv", "0") == "1"
except Exception:
    es_movil = False

# ══════════════════════════════════════════════════════════════════
# SIDEBAR (desktop) o EXPANDER (móvil)
# ══════════════════════════════════════════════════════════════════
_ctx = st.sidebar if not es_movil else st.expander("⚙️ Filtros y datos del cliente", expanded=True)

with _ctx:
    st.markdown("## 👤 Datos del Cliente")
    nombre    = st.text_input("Nombre completo", placeholder="Ej: Franco Lupi")
    edad_c    = st.number_input("Edad contratante", 18, 84, 35)
    prevision = st.selectbox("Previsión", ["FONASA B,C,D","ISAPRE"])
    prevision_base = "ISAPRE" if prevision=="ISAPRE" else "FONASA"

    st.markdown("---")
    st.markdown("### 👨‍👩‍👧‍👦 Cargas")
    n_cargas = st.number_input("Número de cargas", 0, 6, 0)
    cargas = []
    for i in range(int(n_cargas)):
        a,b = st.columns([2,1])
        nc = a.text_input(f"Carga {i+1}", key=f"nc{i}", placeholder="Parentesco")
        ec = b.number_input("Edad", 0, 75, 5, key=f"ec{i}")
        cargas.append({"nombre": nc or f"Carga {i+1}", "edad": ec})

    st.markdown("---")
    st.markdown("### ⚙️ Config")
    uf_api, uf_fecha = get_uf_hoy()
    if uf_api:
        st.success("💱 UF " + uf_fecha + ": $" + f"{uf_api:,.0f}".replace(",",".") + " (actualizada automáticamente)")
        uf_default = int(round(uf_api))
    else:
        st.warning("⚠️ No se pudo obtener la UF automática. Ingresa el valor manual.")
        uf_default = 40180
    val_uf = st.number_input("Valor UF ($)", 30000, 50000, uf_default, 10,
        help="Se actualiza automáticamente cada hora desde mindicador.cl")
    st.markdown("**Tramo convenios:**")
    tramo_am     = st.selectbox("👴 Adulto Mayor",       list(AM_TARIFAS.keys()),            key="tramo_am")
    tramo_im     = st.selectbox("💊 IntegraMédica 100%", list(IM100_TARIFAS.keys()),          key="tramo_im")
    tramo_dental = st.selectbox("🦷 Mi Dental",          list(DENTAL_TARIFAS_MENSUAL.keys()), key="tramo_dental")

    st.markdown("---")
    st.markdown("### 🎁 Cupones")
    usar_cupon = st.checkbox("Aplicar cupón de descuento", value=False)
    if usar_cupon:
        st.info("BCT 60/70/80: BCTALL20NEW (20%)\nB+P: BMPHYA20NEW (20%)\nMultiSalud: BMSBASE20JUL (20%)\nAmb70: BMPAMB10ENERO (10%)\nMultiSalud Pro: BMSPRO10JUL (10%)")

    st.markdown("---")
    st.markdown("### 🎯 Filtros")
    f_preex        = st.checkbox("⚠️ Preexistencias (sin DPS)")
    f_cat          = st.checkbox("⚡ Extensión Catastrófica")
    f_libre        = st.checkbox("🏥 Libre Elección")
    f_maternidad   = st.checkbox("🍼 Maternidad")
    f_salud_mental = st.checkbox("🧠 Salud Mental")
    f_quirurgico   = st.checkbox("🔪 Hospitalización y Cirugías")

    st.markdown("---")
    st.markdown("### 🤝 Convenios especiales")
    f_adulto_mayor = st.checkbox("👴 Adulto Mayor (60-84 años)")
    f_im100        = st.checkbox("💊 IntegraMédica 100%")
    f_dental       = st.checkbox("🦷 Mi Dental 68%")
    f_pyme         = st.checkbox("🏢 Empresa / PYME")

    st.markdown("---")
    if st.button("Cerrar sesión"):
        st.session_state.login_ok = False
        st.session_state.usuario  = ""
        st.rerun()
    st.caption("Sesión: " + st.session_state.usuario)
f_sin_dps = f_preex

# ══════════════════════════════════════════════════════════════════
# CÁLCULO DE PLANES
# ══════════════════════════════════════════════════════════════════
ningun_filtro = not any([f_cat,f_libre,f_maternidad,f_salud_mental,f_quirurgico,
                          f_sin_dps,f_preex,f_adulto_mayor,f_im100,f_dental,f_pyme])
if ningun_filtro:
    planes_compatibles = [pk for pk in PLANES if edad_valida(pk,edad_c) and prevision_base in PLANES[pk]["prevision"]]
else:
    planes_compatibles = [pk for pk in CATALOGO if es_compatible(pk,edad_c,prevision_base,f_sin_dps,f_preex,
        f_cat,f_libre,f_maternidad,f_salud_mental,f_quirurgico,f_adulto_mayor,f_im100,f_dental)]

precios = {}
for pk in planes_compatibles:
    if pk in PLANES:
        r = calcular(pk, edad_c, cargas, val_uf, usar_cupon)
        if r: precios[pk] = r
    else:
        r = calcular_convenio(pk, tramo_am, tramo_im, tramo_dental)
        if r: precios[pk] = r
planes_compatibles = [pk for pk in planes_compatibles if pk in precios]

if edad_c > 75:
    (st.error if es_movil else st.sidebar.error)(f"🔴 {edad_c} años: sin planes regulares. Activa 👴 Adulto Mayor.")
elif edad_c >= 60:
    (st.info if es_movil else st.sidebar.info)(f"💡 {edad_c} años: también aplica Plan Adulto Mayor (60-84 años).")

orden_rec = ["BCT80","BCT70","80/70","MULTIPRO","BCT60","70/70","MULTI","70/25","AMB70"]
rec = next((p for p in orden_rec if p in precios and precios[p].get("total")), "")

# ══════════════════════════════════════════════════════════════════
# HEADER PREMIUM CON LOGO REAL
# ══════════════════════════════════════════════════════════════════
uf_fmt = "$" + f"{val_uf:,}".replace(",",".")
st.markdown(
    '<div style="background:linear-gradient(135deg,#005EB8 0%,#0082D4 60%,#00AEEF 100%);'
    'padding:18px 24px;border-radius:18px;margin-bottom:16px;'
    'box-shadow:0 8px 28px rgba(0,94,184,0.22);'
    'display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">'
    '<div style="display:flex;align-items:center;gap:18px;">'
    '<div style="background:white;border-radius:12px;padding:8px 16px;box-shadow:0 2px 8px rgba(0,0,0,0.12);">'
    + LOGO_HTML +
    '</div>'
    '<div>'
    '<div style="color:white;font-size:22px;font-weight:800;letter-spacing:-0.3px;">Cotizador PRO</div>'
    '<div style="color:#B8DEFF;font-size:12px;font-weight:500;margin-top:2px;">Seguros Complementarios · Herramienta de Asesoría Comercial</div>'
    '</div></div>'
    '<div style="text-align:right;">'
    '<div style="color:#B8DEFF;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">Asesor Comercial</div>'
    '<div style="color:#FFE566;font-size:17px;font-weight:800;margin-top:2px;">' + ASESOR_NOMBRE + '</div>'
    '<div style="color:#B8DEFF;font-size:12px;margin-top:3px;">' + ASESOR_TELEFONO + ' · ' + ASESOR_CIUDAD + '</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── KPI Cards Premium ─────────────────────────────────────────────
kpi_items = [
    ("#005EB8", "👤", "Cliente", (nombre or "(sin nombre)") + " · " + str(edad_c) + " años"),
    ("#0082D4", "📋", "Previsión", prevision),
    ("#00AEEF", "💱", "Valor UF", uf_fmt),
    ("#00C4A1", "🔍", "Opciones", str(len(planes_compatibles)) + " planes disponibles"),
]
kpi_html = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px;">'
for color, icon, label, value in kpi_items:
    kpi_html += (
        '<div style="background:white;border-radius:12px;padding:14px 16px;'
        'box-shadow:0 3px 12px rgba(0,0,0,0.06);border-left:4px solid ' + color + ';">'
        '<div style="font-size:10px;color:#7a8fa6;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">'
        + icon + ' ' + label + '</div>'
        '<div style="font-size:14px;color:#0d2137;font-weight:700;margin-top:5px;line-height:1.3;">' + value + '</div>'
        '</div>'
    )
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)

if edad_c > 75:
    st.error(f"🔴 Con {edad_c} años no hay planes regulares. Activa **👴 Adulto Mayor** en Convenios.")
elif edad_c >= 60 and not f_adulto_mayor:
    st.info(f"💡 Con {edad_c} años también aplican convenios. Actívalos en el panel izquierdo.")
if f_preex:
    st.warning("⚠️ Preexistencias activas — solo planes sin DPS y convenios.")

# ══════════════════════════════════════════════════════════════════
# SELECCIÓN POR CHECKBOX
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
        cols_r = st.columns(min(len(regulares_disp),4))
        for i,pk in enumerate(regulares_disp):
            p=PLANES[pk]; r=precios[pk]
            with cols_r[i%4]:
                if st.checkbox(p["emoji"]+" "+p["nombre"]+"\nUF "+f"{r['total']:.2f}", value=(pk==rec), key="sel_"+pk):
                    planes_seleccionados.append(pk)

    if convenios_disp:
        st.markdown("**🤝 Convenios (sin DPS · cubren preexistencias):**")
        cols_c = st.columns(min(len(convenios_disp),4))
        for i,pk in enumerate(convenios_disp):
            p=CONVENIOS[pk]; r=precios.get(pk)
            with cols_c[i%4]:
                ps = "UF "+f"{r['total']:.2f}"+" ("+r["tramo"]+")" if r else "por tramo"
                if st.checkbox(p["emoji"]+" "+p["nombre"]+"\n"+ps, value=True, key="sel_"+pk):
                    planes_seleccionados.append(pk)

    if not planes_seleccionados:
        st.warning("☝️ Marca al menos un plan para ver el detalle y generar el WhatsApp.")
else:
    if edad_c > 75:
        st.error("⛔ No hay planes para "+str(edad_c)+" años. Activa 👴 Plan Adulto Mayor.")
    elif f_preex or f_sin_dps:
        st.warning("⚠️ No hay opciones sin DPS. Activa 👴 Adulto Mayor o 💊 IntegraMédica 100%.")
    else:
        st.warning("💡 Ningún plan cumple los filtros. Revisa la combinación.")

# ══════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════
t1,t2,t3,t4 = st.tabs(["📋 Detalle de Planes","📊 Comparativa","🔍 Coberturas","📱 WhatsApp"])

# ── TAB 1 ─────────────────────────────────────────────────────────
with t1:
    if not planes_seleccionados:
        st.info("Selecciona al menos un plan arriba.")
    else:
        cols_met = st.columns(min(len(planes_seleccionados),4))
        for i,pk in enumerate(planes_seleccionados):
            p=CATALOGO[pk]; r=precios[pk]
            with cols_met[i%4]:
                es_conv = pk in CONVENIOS
                lbl  = ("⭐ " if pk==rec else "")+p["emoji"]+" "+p["nombre"]
                sub  = ("("+r.get("tramo","")+")" if es_conv else "")
                bdg  = (" 🎁"+str(r.get("pct",0))+"%") if r.get("pct",0)>0 else ""
                st.metric(lbl,"UF "+f"{r['total']:.2f}"+bdg, sub+clp(r["total"],val_uf)+"/mes")
        st.markdown("---")
        for pk in planes_seleccionados:
            p=CATALOGO[pk]; r=precios[pk]; es_conv=pk in CONVENIOS; es_rec=pk==rec
            cs = (" | 🎁 "+r.get("cupon","")+" ("+str(r.get("pct",0))+"% dcto)") if r.get("pct",0)>0 else ""
            ts = (" · "+r.get("tramo","")) if es_conv else ""
            titulo = ("⭐ RECOMENDADO · " if es_rec else "")+p["emoji"]+" "+p["nombre"]+ts+" — UF "+f"{r['total']:.2f}"+"/mes"+cs+" · "+clp(r["total"],val_uf)
            with st.expander(titulo, expanded=es_rec):
                badges=[]
                if es_conv:             badges.append("🤝 Convenio · Sin DPS · Cubre preexistencias")
                if p["f_cat"]:          badges.append("⚡ Catastrófico")
                if p["f_libre"]:        badges.append("🏥 Libre Elección")
                if p["f_maternidad"]:   badges.append("🍼 Maternidad")
                if p["f_salud_mental"]: badges.append("🧠 Salud Mental")
                if p["f_quirurgico"]:   badges.append("🔪 Hospitalización")
                if not p["f_quirurgico"]: badges.append("⚠️ Solo Ambulatorio")
                if r.get("pct",0)>0:    badges.append("🎁 Cupón "+r["cupon"]+" ("+str(r["pct"])+"% dcto)")
                st.markdown("**"+p["tag"]+"** · "+"  ·  ".join(badges))
                st.markdown("Previsión: "+" / ".join(p["prevision"]))
                st.markdown("---")
                col_izq,col_der = st.columns(2)
                with col_izq:
                    st.markdown("##### 📊 Coberturas")
                    for k,v in [("🏥 Hospitalaria",p["hosp"]),("🩺 Ambulatoria",p["amb"]),("⚡ Catastrófica",p["cat"]),
                        ("🍼 Maternidad",p["maternidad"]),("💀 Muerte accidental",p["muerte"]),("🧠 Salud mental",ok(p["salud_mental"])),
                        ("🦷 Dental",p["dental"]),("💊 Medicamentos",p["medicamentos"]),("🔝 Tope base",p["tope_base"]),
                        ("🔝 Tope catastrófico",p["tope_cat"]),("➖ Deducible amb.",p["ded_amb"]),("➖ Deducible hosp.",p["ded_hosp"]),
                        ("📋 DPS","No requerida" if not p["dps"] else "Requerida"),("🏥 Red",p["red"])]:
                        ca,cb=st.columns([2,3]); ca.markdown("**"+k+"**"); cb.write(v)
                    if pk=="AM70" and p.get("rescate_vital"):
                        ca,cb=st.columns([2,3]); ca.markdown("**🚑 Rescate Vital**"); cb.write(p["rescate_vital"])
                with col_der:
                    st.markdown("##### 👥 Asegurados y precios")
                    if es_conv:
                        st.write("• **"+r.get("tramo","")+"**: UF "+f"{r['total']:.2f}"+" · "+clp(r["total"],val_uf))
                        tarifas=p.get("tarifas",{})
                        st.dataframe(pd.DataFrame({"Tramo":list(tarifas.keys()),"UF/mes":["UF "+f"{v:.2f}" for v in tarifas.values()],"$/mes":[clp(v,val_uf) for v in tarifas.values()]}),hide_index=True,use_container_width=True)
                    else:
                        for d in r["det"]:
                            if d["final"]:
                                if d.get("pct",0)>0 and d["orig"]:
                                    st.write("• **"+d["quien"]+"** ("+str(d["edad"])+" años): ~~UF "+f"{d['orig']:.2f}"+"~~ → **UF "+f"{d['final']:.2f}"+"** · "+clp(d["final"],val_uf))
                                else:
                                    st.write("• **"+d["quien"]+"** ("+str(d["edad"])+" años): UF "+f"{d['final']:.2f}"+" · "+clp(d["final"],val_uf))
                            else:
                                st.write("• "+d["quien"]+" ("+str(d["edad"])+" años): *no disponible*")
                        if r.get("pct",0)>0: st.info("🎁 Descuento "+str(r["pct"])+"% con cupón **"+r["cupon"]+"**")
                st.markdown("---")
                cb1,cb2=st.columns(2)
                cb1.success("✅ **Le conviene a:** "+p["para_quien"])
                cb2.warning("⚠️ **No ideal para:** "+p["no_para"])
                st.caption("⏳ Carencias: "+p["carencias"])

# ── TAB 2 ─────────────────────────────────────────────────────────
with t2:
    if len(planes_seleccionados)<2:
        st.info("Selecciona al menos 2 planes para comparar.")
    else:
        filas={"Característica":["💰 Prima UF/mes","💵 Prima $/mes","📆 Prima $/año","🏥 Cobertura hosp.","🩺 Cobertura amb.",
            "⚡ Catastrófica","🔝 Tope base","🔝 Tope cat.","🍼 Maternidad","💀 Muerte accidental",
            "🧠 Salud mental","🦷 Dental","➖ Deducible amb.","➖ Deducible hosp.","🏥 Red","📋 DPS","🎯 Previsión","🎁 Cupón"]}
        for pk in planes_seleccionados:
            p=CATALOGO[pk]; r=precios[pk]; es_conv=pk in CONVENIOS
            lbl=("⭐ " if pk==rec else "")+p["emoji"]+" "+p["nombre"]+(("\n("+r.get("tramo","")+")" )if es_conv else "")
            ci=(r.get("cupon","")+" ("+str(r.get("pct",0))+"%)") if r.get("pct",0)>0 else "—"
            filas[lbl]=["UF "+f"{r['total']:.2f}",clp(r["total"],val_uf),clp(r["total"]*12,val_uf),p["hosp"],p["amb"],
                "✅" if p["f_cat"] else "❌",p["tope_base"],p["tope_cat"],p["maternidad"],
                "✅" if "500" in p["muerte"] else "❌",ok(p["salud_mental"]),
                p["dental"][:20]+"..." if len(p["dental"])>20 else p["dental"],
                p["ded_amb"],p["ded_hosp"],p["red"][:30]+"..." if len(p["red"])>30 else p["red"],
                "No" if not p["dps"] else "Sí"," / ".join(p["prevision"]),ci]
        st.dataframe(pd.DataFrame(filas).set_index("Característica"),use_container_width=True)

# ── TAB 3 ─────────────────────────────────────────────────────────
with t3:
    if not planes_seleccionados:
        st.info("Selecciona planes arriba.")
    else:
        plan_det=st.selectbox("Ver detalle de:",options=planes_seleccionados,format_func=lambda x:CATALOGO[x]["emoji"]+" "+CATALOGO[x]["nombre"])
        p=CATALOGO[plan_det]; r=precios[plan_det]
        st.markdown("## "+p["emoji"]+" "+p["nombre"])
        if r: st.markdown("**Prima:** UF "+f"{r['total']:.2f}"+"/mes · "+clp(r["total"],val_uf)+"/mes · "+clp(r["total"]*12,val_uf)+"/año")
        c1,c2=st.columns(2)
        with c1:
            st.markdown("#### 🩺 Ambulatorio")
            items_amb = ["Consultas medicina general (ilimitadas)","Videoconsultas (ilimitadas)","Consultas especialidad","Exámenes laboratorio e imagenología","Procedimientos diagnósticos y terapéuticos"]
            if plan_det != "AM70":
                items_amb.insert(3, "Urgencias")
            for item in items_amb:
                if "❌" not in p["amb"]: st.write("✅ **"+p["amb"]+"** — "+item)
                else: st.write("❌ "+item)
            if p["salud_mental"]: st.write("✅ **Psicología y Psiquiatría** ambulatoria")
            if p["f_libre"]:      st.write("✅ **Kinesiología y Fonoaudiología** (con prescripción)")
            if p["f_quirurgico"]:
                st.markdown("#### 🏥 Hospitalización")
                for item in ["Día cama","Día cama UTI/UCI/Incubadora","Honorarios médico quirúrgicos","Derecho a pabellón","Insumos y medicamentos hospitalarios","Cirugía ambulatoria"]:
                    st.write("✅ **"+p["hosp"]+"** — "+item)
            else: st.error("❌ Este plan NO cubre hospitalización ni cirugías")
        with c2:
            if p["f_maternidad"]:
                st.markdown("#### 🍼 Maternidad")
                for item in ["Parto normal","Cesárea","Aborto no voluntario","Complicaciones del embarazo"]:
                    st.write("✅ **"+p["maternidad"]+"** — "+item)
            st.markdown("#### ⚡ Extensión Catastrófica")
            if p["f_cat"]: st.success(p["cat"]); st.write("Tope: "+p["tope_cat"])
            else: st.error("❌ No incluye extensión catastrófica")
            st.markdown("#### 📌 Topes y Deducibles")
            st.dataframe(pd.DataFrame({"Concepto":["Tope base","Tope catastrófico","Deducible amb.","Deducible hosp.","Muerte accidental"],
                "Valor":[p["tope_base"],p["tope_cat"],p["ded_amb"],p["ded_hosp"],p["muerte"]]}),hide_index=True,use_container_width=True)
            st.markdown("#### 🏥 Red de Prestadores"); st.info(p["red"])
            if p["f_libre"]:
                st.markdown("| Red | Lab. | Imag. | Día cama | Pabellón |\n|-----|------|-------|----------|----------| \n| IntegraMédica | +12% | +12% | - | - |\n| Clínica Bupa Stgo | +10% | +10% | +10% | +10% |\n| Clínica Bupa Reñaca | +10% | +10% | +10% | +10% |")
        st.markdown("---")
        ca,cb=st.columns(2); ca.success("✅ Le conviene a: "+p["para_quien"]); cb.warning("⚠️ No ideal para: "+p["no_para"])
        st.caption("⏳ Carencias: "+p["carencias"])

# ── TAB 4 — WHATSAPP ──────────────────────────────────────────────
with t4:
    st.subheader("📱 Mensaje WhatsApp")
    if not planes_seleccionados:
        st.info("Selecciona planes arriba para generar el mensaje.")
    else:
        wa1,wa2=st.columns(2)
        with wa1:
            telefono_cliente=st.text_input("WhatsApp cliente (solo 9 dígitos)",placeholder="912345678")
        with wa2:
            modo=st.radio("Modo",["Un solo plan","Comparativa (todos los seleccionados)"])

        hoy=date.today().strftime("%d/%m/%Y"); nc=nombre or "Estimado/a"

        def build_puntos(pk):
            p=CATALOGO[pk]; es_conv=pk in CONVENIOS; pts=[]
            if "❌" not in p["hosp"]:          pts.append("🏥 Hospitalización: "+p["hosp"])
            pts.append("🩺 Ambulatorio: "+p["amb"])
            if p["f_cat"]:                      pts.append("⚡ Catastrófico: 100% hasta "+p["tope_cat"])
            if "❌" not in p["maternidad"]:     pts.append("🍼 Maternidad: "+p["maternidad"])
            if "500" in p["muerte"]:             pts.append("💀 Muerte accidental: UF 500")
            if p["salud_mental"]:               pts.append("🧠 Salud mental (psicología y psiquiatría)")
            if p["f_libre"]:                    pts.append("🏥 Libre elección de médico y clínica")
            if es_conv and pk=="AM70":           pts.append("🚑 Rescate Riesgo Vital — UCM (fono: 223914444)")
            if es_conv:                          pts.append("✅ CUBRE PREEXISTENCIAS — sin DPS")
            if p["dental"] and "No" not in p["dental"]: pts.append("🦷 Dental: "+p["dental"])
            pts.append("💊 Medicamentos: "+p["medicamentos"])
            no_c=[]
            if "❌" in p["hosp"]:               no_c.append("Hospitalización ni cirugías")
            if not p["f_cat"]:                  no_c.append("Extensión catastrófica")
            if "❌" in p["maternidad"]:         no_c.append("Maternidad")
            if not p["salud_mental"]:           no_c.append("Psicología ni psiquiatría")
            if "500" not in p["muerte"]:        no_c.append("Muerte accidental")
            if not p["f_libre"]:               no_c.append("Libre elección (red cerrada)")
            if no_c: pts.append("⛔ *No cubre:* "+" · ".join(no_c))
            return pts

        def precio_wa(pk):
            r=precios[pk]; pct=r.get("pct",0)
            if pct>0:
                orig=sum(d["orig"] for d in r["det"] if d.get("orig"))
                return "~~UF "+f"{orig:.2f}"+"~~ → *UF "+f"{r['total']:.2f}"+"* (~"+clp(r["total"],val_uf)+"/mes)"
            return "*UF "+f"{r['total']:.2f}"+"* (~"+clp(r["total"],val_uf)+"/mes)"

        def aseg_str(pk):
            r=precios[pk]; es_conv=pk in CONVENIOS
            if es_conv: return "\n   • "+r.get("tramo","")+" : UF "+f"{r['total']:.2f}"+" ("+clp(r["total"],val_uf)+")"
            s=""
            for d in r["det"]:
                if d.get("final"):
                    if d.get("pct",0)>0 and d.get("orig"):
                        s+="\n   • "+d["quien"]+" ("+str(d["edad"])+" años): ~~UF "+f"{d['orig']:.2f}"+"~~ → UF "+f"{d['final']:.2f}"+" ("+clp(d["final"],val_uf)+")"
                    else:
                        s+="\n   • "+d["quien"]+" ("+str(d["edad"])+" años): UF "+f"{d['final']:.2f}"+" ("+clp(d["final"],val_uf)+")"
            return s

        def cup_str(pk):
            r=precios[pk]
            if r.get("pct",0)>0: return "\n🎁 *Cupón:* "+r["cupon"]+" ("+str(r["pct"])+"% dcto)"
            return ""

        if modo=="Un solo plan":
            plan_wa=st.selectbox("Plan a enviar:",options=planes_seleccionados,format_func=lambda x:CATALOGO[x]["emoji"]+" "+CATALOGO[x]["nombre"])
            p=CATALOGO[plan_wa]; r=precios[plan_wa]; pts=build_puntos(plan_wa)
            pts_txt="\n".join("   "+pt for pt in pts)
            pdf_link_solo = ("\n📎 *Descarga las condiciones del plan:*\n   "+PDFS_PLANES[p["nombre"]]) if p["nombre"] in PDFS_PLANES else ""
            msg="\n".join([
                "Hola "+nc+" 👋","",
                "Te comparto tu cotización personalizada de *Bupa Seguros* 🏥",
                "📅 Fecha: "+hoy,"",
                "━━━━━━━━━━━━━━━━━━━━━",
                "👤 *Cliente:* "+(nombre or nc)+" · "+str(edad_c)+" años",
                "📋 *Previsión:* "+prevision,
                "🔹 *Plan:* "+p["nombre"]+cup_str(plan_wa),"",
                "👥 *Asegurados:*"+aseg_str(plan_wa),"",
                "💰 *Prima mensual:*",
                "   → "+precio_wa(plan_wa),
                "   → Anual aprox.: "+clp(r["total"]*12,val_uf),"",
                "━━━━━━━━━━━━━━━━━━━━━",
                "✅ *Coberturas:*",
                pts_txt,"",
                "📌 *Topes:*",
                "   • Base: "+p["tope_base"],
                "   • Catastrófico: "+p["tope_cat"],
                "   • Deducible amb.: "+p["ded_amb"],
                "   • Deducible hosp.: "+p["ded_hosp"],"",
                "🏥 *Red:* "+p["red"],
                "📋 *DPS:* "+("No requerida — cubre preexistencias" if not p["dps"] else "Requerida"),
                "⏳ *Carencias:* "+p["carencias"],
                pdf_link_solo,"",
                "━━━━━━━━━━━━━━━━━━━━━",
                "🤝 ¿Te interesa avanzar?",
                "📱 "+ASESOR_NOMBRE,
                "📞 "+ASESOR_TELEFONO,"",
                "_Cotización tarifario Bupa Seguros mayo 2026. UF "+uf_fmt+". El riesgo es cubierto por Bupa Compañía de Seguros de Vida S.A._",
            ])
        else:
            # ── Definición de familias de planes similares ─────────────
            FAMILIAS = {
                "BCT": {
                    "claves": ["BCT60","BCT70","BCT80"],
                    "titulo": "Bupa Cuidado Total",
                    "descripcion_comun": (
                        "✅ Libre elección de médico y clínica\n"
                        "🧠 Salud mental (psicología y psiquiatría)\n"
                        "🍼 Maternidad incluida\n"
                        "💊 Medicamentos: 50% genérico / 30% marca con receta (tope $25.000/mes)\n"
                        "🦷 62% dcto IntegraMédica\n"
                        "➖ Deducible: UF 1/año (GRATIS en Red Bupa)\n"
                        "🏥 Red: Libre elección + cobertura extra Red Bupa\n"
                        "📋 DPS requerida · ⛔ Sin extensión catastrófica\n"
                        "⏳ Carencias: Bariátrica, Septoplastía, Disforia de Género: 1 año"
                    ),
                },
                "BP": {
                    "claves": ["70/25","70/70","80/70"],
                    "titulo": "Bupa + Protección",
                    "descripcion_comun": (
                        "⚡ Catastrófico: 100% hasta UF 9.500\n"
                        "🍼 Maternidad incluida\n"
                        "💀 Muerte accidental: UF 500\n"
                        "💊 Medicamentos: 50% genérico / 20% marca (tope $15.000/mes)\n"
                        "🦷 62% dcto IntegraMédica\n"
                        "➖ Deducible amb.: UF 0,5/año · Hosp.: UF 5/año\n"
                        "🏥 Red: Clínica Bupa Santiago + IntegraMédica\n"
                        "📋 DPS requerida · Solo FONASA\n"
                        "⏳ Carencias: Bariátrica, ocular láser, rinolaringológica: 1 año"
                    ),
                },
                "MULTI": {
                    "claves": ["MULTI","MULTIPRO"],
                    "titulo": "Bupa MultiSalud",
                    "descripcion_comun": (
                        "⚡ Catastrófico: 2 capas hasta UF 7.500\n"
                        "🍼 Maternidad incluida\n"
                        "🧠 Salud mental (psicología y psiquiatría)\n"
                        "💊 Medicamentos: 50% genérico / 20% marca (tope $15.000/mes)\n"
                        "🦷 62% dcto IntegraMédica\n"
                        "🏥 Red ampliada: Bupa · Dávila · Interclinica · Santa María · otros\n"
                        "📋 DPS requerida · Solo FONASA\n"
                        "⏳ Carencias: Bariátrica, ocular láser, rinolaringológica: 1 año"
                    ),
                },
            }

            def detectar_familia(seleccionados):
                """Retorna (familia_key, claves_en_familia, claves_fuera) o None si no hay familia."""
                for fk, fdata in FAMILIAS.items():
                    en_familia = [pk for pk in seleccionados if pk in fdata["claves"]]
                    fuera = [pk for pk in seleccionados if pk not in fdata["claves"]]
                    if len(en_familia) >= 2:
                        return fk, en_familia, fuera
                return None, [], list(seleccionados)

            familia_key, planes_familia, planes_solos = detectar_familia(planes_seleccionados)

            bloques = ""

            # ── Bloque agrupado para planes de la misma familia ─────────
            if familia_key:
                fdata = FAMILIAS[familia_key]
                bloques += "\n🏥 *FAMILIA: "+fdata["titulo"]+"*\n\n"
                bloques += fdata["descripcion_comun"] + "\n\n"
                bloques += "📊 *Diferencia entre variantes: cobertura (%) y tope base*\n"
                bloques += "━━━━━━━━━━━━━━━━━━━━━\n"
                for pk in planes_familia:
                    p = CATALOGO[pk]; r = precios[pk]
                    rec_s = " ⭐ RECOMENDADO" if pk == rec else ""
                    cup_b = ("\n   🎁 Cupón: "+r["cupon"]+" ("+str(r["pct"])+"% dcto)") if r.get("pct",0)>0 else ""
                    # Diferencias clave según familia
                    if familia_key == "BCT":
                        dif = "Hosp y amb: *"+p["hosp"]+"* · Tope: *"+p["tope_base"]+"*"
                    elif familia_key == "BP":
                        dif = "Hosp: *"+p["hosp"]+"* · Amb: *"+p["amb"]+"* · Tope: *"+p["tope_base"]+"*"
                    elif familia_key == "MULTI":
                        dif = "Hosp: *"+p["hosp"]+"* · Amb: *"+p["amb"]+"* · Tope: *"+p["tope_base"]+"*"
                    else:
                        dif = "Hosp: *"+p["hosp"]+"* · Amb: *"+p["amb"]+"*"
                    pdf_lnk = ("\n   📎 "+PDFS_PLANES[p["nombre"]]) if p["nombre"] in PDFS_PLANES else ""
                    bloques += (
                        "\n🔹 *"+p["emoji"]+" "+p["nombre"]+"*"+rec_s+"\n"
                        "   "+dif+"\n"
                        "   💰 "+precio_wa(pk)+cup_b+"\n"
                        "   Anual aprox.: "+clp(r["total"]*12,val_uf)+"\n"
                        "   "+aseg_str(pk).strip()+pdf_lnk+"\n"
                    )
                bloques += "\n━━━━━━━━━━━━━━━━━━━━━\n"

            # ── Bloques individuales para planes fuera de la familia ────
            idx_offset = len(planes_familia) if familia_key else 0
            for i, pk in enumerate(planes_solos, 1):
                p = CATALOGO[pk]; r = precios[pk]; es_conv = pk in CONVENIOS
                rec_s = "\n⭐ *RECOMENDADO*" if pk == rec else ""
                conv_s = "\n🤝 _Convenio: sin DPS · cubre preexistencias_" if es_conv else ""
                pts = build_puntos(pk)
                cup_b = ("\n🎁 Cupón: "+r["cupon"]+" ("+str(r["pct"])+"% dcto)") if r.get("pct",0)>0 else ""
                tr_b = (" · "+r.get("tramo","")) if es_conv else ""
                pdf_lnk_s = ("\n   📎 "+PDFS_PLANES[p["nombre"]]) if p["nombre"] in PDFS_PLANES else ""
                num = idx_offset + i
                bloques += (
                    "\n🔹 *OPCIÓN "+str(num)+" — "+p["nombre"]+"*"+tr_b+rec_s+conv_s+"\n\n"
                    "💰 "+precio_wa(pk)+cup_b+"\n"
                    +"\n".join("   ✅ "+pt for pt in pts[:7])+"\n"
                    "   📌 Tope: "+p["tope_base"]+" · Ded.: "+p["ded_amb"]+"\n"
                    "   📋 DPS: "+("No requerida" if not p["dps"] else "Requerida")+"\n"
                    "   ⏳ Carencias: "+p["carencias"]+pdf_lnk_s+"\n\n"
                    "━━━━━━━━━━━━━━━━━━━━━"
                )

            rec_t = ("\n💡 *Recomendación:* El plan *"+CATALOGO[rec]["nombre"]+"* ofrece el mejor equilibrio.\n") if rec in planes_seleccionados else ""
            msg = "\n".join([
                "Hola "+nc+" 👋","",
                "Te comparto tus opciones de *Bupa Seguros* 🏥",
                "📅 Fecha: "+hoy,"",
                "━━━━━━━━━━━━━━━━━━━━━",
                "👤 *Cliente:* "+(nombre or nc)+" · "+str(edad_c)+" años",
                "📋 *Previsión:* "+prevision,
                "━━━━━━━━━━━━━━━━━━━━━",
                bloques, rec_t,
                "🤝 Conversemos y te ayudo a elegir la mejor opción.",
                "📱 "+ASESOR_NOMBRE,
                "📞 "+ASESOR_TELEFONO,"",
                "_Cotización tarifario Bupa Seguros mayo 2026. UF "+uf_fmt+". El riesgo es cubierto por Bupa Compañía de Seguros de Vida S.A._",
            ])

        st.code(msg, language=None)

        if telefono_cliente:
            wa_link="https://web.whatsapp.com/send?phone=56"+telefono_cliente+"&text="+quote(msg,safe="")
            st.link_button("📲 Abrir WhatsApp Web", wa_link)
        else:
            st.warning("⚠️ Ingresa el número del cliente para abrir WhatsApp.")

        st.success("✅ Mensaje listo con "+str(len(planes_seleccionados))+" plan(es) seleccionado(s).")
        with st.expander("📎 Verificar PDFs"):
            cols_pdf = st.columns(min(len(planes_seleccionados), 3))
            for i, plan_key in enumerate(planes_seleccionados):
                np2 = CATALOGO[plan_key]["nombre"]
                if np2 in PDFS_PLANES:
                    with cols_pdf[i % 3]:
                        st.link_button("📄 "+np2, PDFS_PLANES[np2], use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# PYME
# ══════════════════════════════════════════════════════════════════
if f_pyme:
    st.markdown("---"); st.markdown("## 🏢 Plan PYME Bupa")
    st.info("Sin DPS colectivo · Cubre preexistencias · Mínimo 2 trabajadores")
    st.markdown("- ✅ Sin DPS individual — cubre a todos\n- ✅ Cubre preexistencias desde el primer día\n- ✅ Precio especial por volumen\n- ✅ Deducible $0 en red Bupa/IntegraMédica\n\n**Para cotizar:** RUT empresa · N° trabajadores · Rango de edades · Previsión predominante\n\n💡 Contacta a tu ejecutivo Bupa o ingresa a BupaSales.")

# ══════════════════════════════════════════════════════════════════
# FOOTER CORPORATIVO CON LOGO
# ══════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="margin-top:32px;background:linear-gradient(90deg,#003A70,#005EB8);'
    'border-radius:14px;padding:14px 22px;display:flex;align-items:center;'
    'justify-content:space-between;flex-wrap:wrap;gap:8px;">'
    '<div style="display:flex;align-items:center;gap:12px;">'
    '<div style="background:white;border-radius:8px;padding:4px 10px;">' + LOGO_HTML_SM + '</div>'
    '<div>'
    '<div style="color:white;font-size:12px;font-weight:700;">Cotizador PRO · Bupa Seguros Chile</div>'
    '<div style="color:#7eb8e8;font-size:11px;">Desarrollado para asesoría comercial · Uso interno exclusivo</div>'
    '</div></div>'
    '<div style="color:#7eb8e8;font-size:11px;text-align:right;line-height:1.6;">'
    'El riesgo es cubierto por Bupa Compañía de Seguros de Vida S.A.<br>'
    'Tarifario mayo 2026 · UF ' + uf_fmt +
    '</div></div>',
    unsafe_allow_html=True
)
