# ============================================================
# MÓDULO CRUZ BLANCA — para integrar en cotizador_bupa_pro.py
# ============================================================

# ── DATOS ──────────────────────────────────────────────────

FACTOR_RIESGO = {
    "contratante": [
        (0,  19,  0.6),
        (20, 24,  0.9),
        (25, 34,  1.0),
        (35, 44,  1.3),
        (45, 54,  1.4),
        (55, 64,  2.0),
        (65, 999, 2.4),
    ],
    "carga": [
        (0,  19,  0.6),
        (20, 24,  0.7),
        (25, 34,  0.7),
        (35, 44,  0.9),
        (45, 54,  1.0),
        (55, 64,  1.4),
        (65, 999, 2.2),
    ],
}

GES_UF = 0.971  # por cotizado

# Tarifario RM — (codigo, familia, precio_base_uf, tipo, cob_hosp, cob_amb)
# tipo: "cerrado" = sin libre eleccion, "libre_eleccion"
# cob_hosp / cob_amb: dict {clinica: porcentaje}

PLANES_CB_RM = [
    # ── CAMPUS BUPA MAX NACIONAL (cerrado) ──────────────────
    {
        "codigo": "CMBX001526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.12, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 60, "Clínica Bupa Reñaca": 60,
            "Clínica Bupa Antofagasta": 60, "Clínica Dávila Recoleta": 50,
            "Clínica Andes Salud El Loa": 50, "Hospital Clínico Viña del Mar": 50,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 60, "Clínica Bupa Reñaca": 60,
            "Clínica Bupa Antofagasta": 60, "Integramédica": 60,
        },
    },
    {
        "codigo": "CMBX002526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.14, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 60, "Clínica Bupa Reñaca": 60,
            "Clínica Bupa Antofagasta": 60, "Clínica Dávila Recoleta": 50,
            "Clínica Andes Salud El Loa": 50, "Hospital Clínico Viña del Mar": 50,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 70, "Clínica Bupa Reñaca": 70,
            "Clínica Bupa Antofagasta": 70, "Integramédica": 70,
        },
    },
    {
        "codigo": "CMBX003526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.16, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 60, "Clínica Bupa Reñaca": 60,
            "Clínica Bupa Antofagasta": 60, "Clínica Dávila Recoleta": 50,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 80, "Clínica Bupa Reñaca": 80,
            "Clínica Bupa Antofagasta": 80, "Integramédica": 80,
        },
    },
    {
        "codigo": "CMBX004526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.18, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 70, "Clínica Bupa Reñaca": 70,
            "Clínica Bupa Antofagasta": 70, "Clínica Dávila Recoleta": 60,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 60, "Clínica Bupa Reñaca": 60,
            "Clínica Bupa Antofagasta": 60, "Integramédica": 60,
        },
    },
    {
        "codigo": "CMBX005526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.19, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 70, "Clínica Bupa Reñaca": 70,
            "Clínica Bupa Antofagasta": 70, "Clínica Dávila Recoleta": 60,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 70, "Clínica Bupa Reñaca": 70,
            "Clínica Bupa Antofagasta": 70, "Integramédica": 70,
        },
    },
    {
        "codigo": "CMBX006526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.21, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 70, "Clínica Bupa Reñaca": 70,
            "Clínica Bupa Antofagasta": 70, "Clínica Dávila Recoleta": 60,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 80, "Clínica Bupa Reñaca": 80,
            "Clínica Bupa Antofagasta": 80, "Integramédica": 80,
        },
    },
    {
        "codigo": "CMBX007526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.23, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 80, "Clínica Bupa Reñaca": 80,
            "Clínica Bupa Antofagasta": 80, "Clínica Dávila Recoleta": 70,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 60, "Clínica Bupa Reñaca": 60,
            "Clínica Bupa Antofagasta": 60, "Integramédica": 60,
        },
    },
    {
        "codigo": "CMBX008526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.25, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 80, "Clínica Bupa Reñaca": 80,
            "Clínica Bupa Antofagasta": 80, "Clínica Dávila Recoleta": 70,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 70, "Clínica Bupa Reñaca": 70,
            "Clínica Bupa Antofagasta": 70, "Integramédica": 70,
        },
    },
    {
        "codigo": "CMBX009526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.26, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 80, "Clínica Bupa Reñaca": 80,
            "Clínica Bupa Antofagasta": 80, "Clínica Dávila Recoleta": 70,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 80, "Clínica Bupa Reñaca": 80,
            "Clínica Bupa Antofagasta": 80, "Integramédica": 80,
        },
    },
    {
        "codigo": "CMBX010526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.28, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 90, "Clínica Bupa Reñaca": 90,
            "Clínica Bupa Antofagasta": 90, "Clínica Dávila Recoleta": 80,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 60, "Clínica Bupa Reñaca": 60,
            "Clínica Bupa Antofagasta": 60, "Integramédica": 60,
        },
    },
    {
        "codigo": "CMBX011526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.30, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 90, "Clínica Bupa Reñaca": 90,
            "Clínica Bupa Antofagasta": 90, "Clínica Dávila Recoleta": 80,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 70, "Clínica Bupa Reñaca": 70,
            "Clínica Bupa Antofagasta": 70, "Integramédica": 70,
        },
    },
    {
        "codigo": "CMBX012526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.32, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 90, "Clínica Bupa Reñaca": 90,
            "Clínica Bupa Antofagasta": 90, "Clínica Dávila Recoleta": 80,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 80, "Clínica Bupa Reñaca": 80,
            "Clínica Bupa Antofagasta": 80, "Integramédica": 80,
        },
    },
    {
        "codigo": "CMBX013526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.34, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 100, "Clínica Bupa Reñaca": 100,
            "Clínica Bupa Antofagasta": 100, "Clínica Dávila Recoleta": 90,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 60, "Clínica Bupa Reñaca": 60,
            "Clínica Bupa Antofagasta": 60, "Integramédica": 60,
        },
    },
    {
        "codigo": "CMBX014526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.35, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 100, "Clínica Bupa Reñaca": 100,
            "Clínica Bupa Antofagasta": 100, "Clínica Dávila Recoleta": 90,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 70, "Clínica Bupa Reñaca": 70,
            "Clínica Bupa Antofagasta": 70, "Integramédica": 70,
        },
    },
    {
        "codigo": "CMBX015526", "familia": "Campus Bupa Max Nacional",
        "precio_base": 1.37, "tipo": "cerrado",
        "cob_hosp": {
            "Clínica Bupa Santiago": 100, "Clínica Bupa Reñaca": 100,
            "Clínica Bupa Antofagasta": 100, "Clínica Dávila Recoleta": 90,
        },
        "cob_amb": {
            "Clínica Bupa Santiago": 80, "Clínica Bupa Reñaca": 80,
            "Clínica Bupa Antofagasta": 80, "Integramédica": 80,
        },
    },

    # ── CAMPUS BUPA (libre elección) ─────────────────────────
    {"codigo":"CMBS010526","familia":"Campus Bupa","precio_base":1.27,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":60,"Clínica Dávila Recoleta":50,"Hosp. Del Profesor":50,"Hosp. Clínico U. de Chile":50},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS020526","familia":"Campus Bupa","precio_base":1.31,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":60,"Clínica Dávila Recoleta":50,"Hosp. Del Profesor":50},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS040526","familia":"Campus Bupa","precio_base":1.33,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":70,"Clínica Dávila Recoleta":60,"Hosp. Del Profesor":60},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS030526","familia":"Campus Bupa","precio_base":1.34,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":60,"Clínica Dávila Recoleta":50,"Hosp. Del Profesor":50},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS050526","familia":"Campus Bupa","precio_base":1.36,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":70,"Clínica Dávila Recoleta":60,"Hosp. Del Profesor":60},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS060526","familia":"Campus Bupa","precio_base":1.40,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":70,"Clínica Dávila Recoleta":60,"Hosp. Del Profesor":60},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS070526","familia":"Campus Bupa","precio_base":1.43,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":80,"Clínica Dávila Recoleta":70,"Hosp. Del Profesor":70},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS080526","familia":"Campus Bupa","precio_base":1.47,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":80,"Clínica Dávila Recoleta":70,"Hosp. Del Profesor":70},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS090526","familia":"Campus Bupa","precio_base":1.51,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":80,"Clínica Dávila Recoleta":70,"Hosp. Del Profesor":70},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS100526","familia":"Campus Bupa","precio_base":1.58,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":90,"Clínica Dávila Recoleta":80,"Hosp. Del Profesor":80,"Clínica Indisa":80,"Clínica Red Salud Vitacura":80,"Clínica Santa María":70,"Hosp. Clínico UC":70,"Clínica Meds":70},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS110526","familia":"Campus Bupa","precio_base":1.62,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Red Salud Vitacura":80,"Clínica Santa María":70,"Hosp. Clínico UC":70,"Clínica Meds":70},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS130526","familia":"Campus Bupa","precio_base":1.64,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS120526","familia":"Campus Bupa","precio_base":1.70,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Red Salud Vitacura":80,"Clínica Santa María":70,"Hosp. Clínico UC":70,"Clínica Meds":70},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS140526","familia":"Campus Bupa","precio_base":1.72,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS150526","familia":"Campus Bupa","precio_base":1.76,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS160526","familia":"Campus Bupa","precio_base":1.85,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS170526","familia":"Campus Bupa","precio_base":1.96,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS190526","familia":"Campus Bupa","precio_base":2.03,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS180526","familia":"Campus Bupa","precio_base":2.07,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS200526","familia":"Campus Bupa","precio_base":2.16,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS220526","familia":"Campus Bupa","precio_base":2.23,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS210526","familia":"Campus Bupa","precio_base":2.28,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS240526","familia":"Campus Bupa","precio_base":2.48,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS250526","familia":"Campus Bupa","precio_base":2.68,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":60,"Clínica UC San Carlos":60,"Clínica Las Condes":60},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS260526","familia":"Campus Bupa","precio_base":2.76,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":60,"Clínica UC San Carlos":60,"Clínica Las Condes":60},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS280526","familia":"Campus Bupa","precio_base":2.81,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":70,"Clínica UC San Carlos":70,"Clínica Las Condes":70},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS290526","familia":"Campus Bupa","precio_base":2.89,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":70,"Clínica UC San Carlos":70,"Clínica Las Condes":70},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS270526","familia":"Campus Bupa","precio_base":2.97,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":60,"Clínica UC San Carlos":60,"Clínica Las Condes":60},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS310526","familia":"Campus Bupa","precio_base":2.98,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":80,"Clínica UC San Carlos":80,"Clínica Las Condes":80},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS320526","familia":"Campus Bupa","precio_base":3.07,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":80,"Clínica UC San Carlos":80,"Clínica Las Condes":80},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS300526","familia":"Campus Bupa","precio_base":3.10,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":70,"Clínica UC San Carlos":70,"Clínica Las Condes":70},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS340526","familia":"Campus Bupa","precio_base":3.20,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":60,"Clínica UC San Carlos":60,"Clínica Las Condes":60},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS330526","familia":"Campus Bupa","precio_base":3.28,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":80,"Clínica UC San Carlos":80,"Clínica Las Condes":80},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS350526","familia":"Campus Bupa","precio_base":3.29,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":80,"Clínica UC San Carlos":80,"Clínica Las Condes":80},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS370526","familia":"Campus Bupa","precio_base":3.35,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":70,"Clínica UC San Carlos":70,"Clínica Las Condes":70,"Clínica Alemana":70},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS380526","familia":"Campus Bupa","precio_base":3.45,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":70,"Clínica UC San Carlos":70,"Clínica Las Condes":70,"Clínica Alemana":70},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS360526","familia":"Campus Bupa","precio_base":3.52,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":60,"Clínica UC San Carlos":60,"Clínica Las Condes":60,"Clínica Alemana":60},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS400526","familia":"Campus Bupa","precio_base":3.64,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":80,"Clínica UC San Carlos":80,"Clínica Las Condes":80,"Clínica Alemana":80},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS390526","familia":"Campus Bupa","precio_base":3.81,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":70,"Clínica UC San Carlos":70,"Clínica Las Condes":70,"Clínica Alemana":70},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},
    {"codigo":"CMBS410526","familia":"Campus Bupa","precio_base":4.01,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":100,"Clínica UC San Carlos":100,"Clínica Las Condes":100,"Clínica Alemana":100},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS430526","familia":"Campus Bupa","precio_base":4.18,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":100,"Clínica UC San Carlos":100,"Clínica Las Condes":100,"Clínica Alemana":100},
     "cob_amb":{"Clínica Bupa Santiago":70,"Integramédica":70}},
    {"codigo":"CMBS440526","familia":"Campus Bupa","precio_base":4.31,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":100,"Clínica UC San Carlos":100,"Clínica Las Condes":100,"Clínica Alemana":100},
     "cob_amb":{"Clínica Bupa Santiago":80,"Integramédica":80}},
    {"codigo":"CMBS450526","familia":"Campus Bupa","precio_base":4.42,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":100,"Clínica UC San Carlos":100,"Clínica Las Condes":100,"Clínica Alemana":100},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90}},

    # ── PROTECCIÓN 1 (libre elección) ────────────────────────
    {"codigo":"PROT101526","familia":"Protección 1","precio_base":1.63,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":60,"Clínica Dávila Recoleta":50,"Hosp. Clínico U. de Chile":50,"Hosp. Del Profesor":50},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":60,"Clínica Cordillera":60,"Hosp. Del Profesor":50,"Clínica Dávila Recoleta":50}},
    {"codigo":"PROT102526","familia":"Protección 1","precio_base":1.69,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":60,"Clínica Dávila Recoleta":50,"Hosp. Del Profesor":50},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":70,"Clínica Cordillera":70,"Clínica Dávila Recoleta":60}},
    {"codigo":"PROT103526","familia":"Protección 1","precio_base":1.73,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":60,"Clínica Dávila Recoleta":50,"Hosp. Del Profesor":50},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":80,"Clínica Cordillera":80,"Clínica Dávila Recoleta":70}},
    {"codigo":"PROT104526","familia":"Protección 1","precio_base":1.75,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":70,"Clínica Dávila Recoleta":60,"Hosp. Del Profesor":60},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":60,"Clínica Cordillera":60,"Clínica Dávila Recoleta":50}},
    {"codigo":"PROT105526","familia":"Protección 1","precio_base":1.80,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":70,"Clínica Dávila Recoleta":60,"Hosp. Del Profesor":60},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":70,"Clínica Cordillera":70,"Clínica Dávila Recoleta":60}},
    {"codigo":"PROT106526","familia":"Protección 1","precio_base":1.81,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":70,"Clínica Dávila Recoleta":60,"Hosp. Del Profesor":60},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":80,"Clínica Cordillera":80,"Clínica Dávila Recoleta":70}},
    {"codigo":"PROT107526","familia":"Protección 1","precio_base":1.83,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":80,"Clínica Dávila Recoleta":70,"Hosp. Del Profesor":70},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":60,"Clínica Cordillera":60,"Clínica Dávila Recoleta":50}},
    {"codigo":"PROT108526","familia":"Protección 1","precio_base":1.89,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":80,"Clínica Dávila Recoleta":70,"Hosp. Del Profesor":70},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":70,"Clínica Cordillera":70,"Clínica Dávila Recoleta":60}},
    {"codigo":"PROT109526","familia":"Protección 1","precio_base":1.90,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":80,"Clínica Dávila Recoleta":70,"Hosp. Del Profesor":70},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":80,"Clínica Cordillera":80,"Clínica Dávila Recoleta":70}},
    {"codigo":"PROT110526","familia":"Protección 1","precio_base":1.93,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":90,"Clínica Dávila Recoleta":80,"Hosp. Del Profesor":80},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":60,"Clínica Cordillera":60,"Clínica Dávila Recoleta":50}},
    {"codigo":"PROT111526","familia":"Protección 1","precio_base":1.94,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":90,"Clínica Dávila Recoleta":80,"Hosp. Del Profesor":80},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":70,"Clínica Cordillera":70,"Clínica Dávila Recoleta":60}},
    {"codigo":"PROT112526","familia":"Protección 1","precio_base":2.04,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":90,"Clínica Dávila Recoleta":80,"Hosp. Del Profesor":80},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":80,"Clínica Cordillera":80,"Clínica Dávila Recoleta":70}},
    {"codigo":"PROT113526","familia":"Protección 1","precio_base":2.07,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Hosp. Del Profesor":90},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":60,"Clínica Cordillera":60,"Clínica Dávila Recoleta":50}},
    {"codigo":"PROT114526","familia":"Protección 1","precio_base":2.08,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Hosp. Del Profesor":90},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":70,"Clínica Cordillera":70,"Clínica Dávila Recoleta":60}},
    {"codigo":"PROT115526","familia":"Protección 1","precio_base":2.09,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Hosp. Del Profesor":90},
     "cob_amb":{"Integramédica":90,"Clínica Bupa Santiago":80,"Clínica Cordillera":80,"Clínica Dávila Recoleta":70}},

    # ── PROTECCIÓN 2 (libre elección, red ampliada) ──────────
    {"codigo":"PROT201526","familia":"Protección 2","precio_base":2.34,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":70,"Clínica Indisa":70,"Clínica Red Salud Vitacura":60,"Clínica Santa María":60,"Hosp. Clínico UC":60,"Clínica Meds":60},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":60,"Clínica Las Condes":60}},
    {"codigo":"PROT202526","familia":"Protección 2","precio_base":2.43,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":70,"Clínica Indisa":70,"Clínica Red Salud Vitacura":60,"Clínica Santa María":60,"Hosp. Clínico UC":60,"Clínica Meds":60},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":70,"Clínica Las Condes":70}},
    {"codigo":"PROT203526","familia":"Protección 2","precio_base":2.51,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":70,"Clínica Indisa":70,"Clínica Red Salud Vitacura":60,"Clínica Santa María":60,"Hosp. Clínico UC":60,"Clínica Meds":60},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Las Condes":80}},
    {"codigo":"PROT204526","familia":"Protección 2","precio_base":2.60,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Red Salud Vitacura":70,"Clínica Santa María":70,"Hosp. Clínico UC":70,"Clínica Meds":70},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":60,"Clínica Las Condes":60}},
    {"codigo":"PROT205526","familia":"Protección 2","precio_base":2.69,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Red Salud Vitacura":70,"Clínica Santa María":70,"Hosp. Clínico UC":70,"Clínica Meds":70},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":70,"Clínica Las Condes":70}},
    {"codigo":"PROT206526","familia":"Protección 2","precio_base":2.78,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Red Salud Vitacura":70,"Clínica Santa María":70,"Hosp. Clínico UC":70,"Clínica Meds":70},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Las Condes":80}},
    {"codigo":"PROT207526","familia":"Protección 2","precio_base":2.90,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":80,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80,"Clínica UC San Carlos":70,"Clínica Las Condes":70},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":60,"Clínica Las Condes":60}},
    {"codigo":"PROT208526","familia":"Protección 2","precio_base":2.99,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":80,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80,"Clínica UC San Carlos":70,"Clínica Las Condes":70},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":70,"Clínica Las Condes":70}},
    {"codigo":"PROT209526","familia":"Protección 2","precio_base":3.08,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":80,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80,"Clínica UC San Carlos":70,"Clínica Las Condes":70},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Las Condes":80}},
    {"codigo":"PROT210526","familia":"Protección 2","precio_base":3.16,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":100,"Clínica Red Salud Vitacura":100,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica UC San Carlos":80,"Clínica Las Condes":80},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":60,"Clínica Las Condes":60}},
    {"codigo":"PROT211526","familia":"Protección 2","precio_base":3.25,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":100,"Clínica Red Salud Vitacura":100,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica UC San Carlos":80,"Clínica Las Condes":80},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":70,"Clínica Las Condes":70}},
    {"codigo":"PROT212526","familia":"Protección 2","precio_base":3.34,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":100,"Clínica Red Salud Vitacura":100,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica UC San Carlos":80,"Clínica Las Condes":80},
     "cob_amb":{"Clínica Bupa Santiago":90,"Integramédica":90,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Las Condes":80}},

    # ── SOLUCIÓN 1 (libre elección) ──────────────────────────
    {"codigo":"SOLN101526","familia":"Solución 1","precio_base":3.07,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":80,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80,"Clínica U. de los Andes":60,"Clínica Las Condes":60},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":60,"Clínica Las Condes":60}},
    {"codigo":"SOLN102526","familia":"Solución 1","precio_base":3.26,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":80,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80,"Clínica U. de los Andes":60,"Clínica Las Condes":60},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":70,"Clínica Las Condes":70}},
    {"codigo":"SOLN104526","familia":"Solución 1","precio_base":3.37,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":70,"Clínica Santa María":70,"Hosp. Clínico UC":70,"Clínica Meds":70,"Clínica U. de los Andes":60,"Clínica Las Condes":60},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":60,"Clínica Las Condes":60}},
    {"codigo":"SOLN103526","familia":"Solución 1","precio_base":3.38,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":80,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80,"Clínica U. de los Andes":60,"Clínica Las Condes":60},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Las Condes":80}},
    {"codigo":"SOLN105526","familia":"Solución 1","precio_base":3.49,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":70,"Clínica Las Condes":70},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":70,"Clínica Las Condes":70}},
    {"codigo":"SOLN106526","familia":"Solución 1","precio_base":3.58,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":70,"Clínica Las Condes":70},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Las Condes":80}},
    {"codigo":"SOLN107526","familia":"Solución 1","precio_base":3.69,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":80,"Clínica Las Condes":80},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":60,"Clínica Las Condes":60}},
    {"codigo":"SOLN108526","familia":"Solución 1","precio_base":3.81,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":80,"Clínica Las Condes":80},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":70,"Clínica Las Condes":70}},
    {"codigo":"SOLN110526","familia":"Solución 1","precio_base":3.95,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":60,"Clínica Las Condes":60}},
    {"codigo":"SOLN109526","familia":"Solución 1","precio_base":4.00,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":80,"Clínica Las Condes":80},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Las Condes":80}},
    {"codigo":"SOLN111526","familia":"Solución 1","precio_base":4.08,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":70,"Clínica Las Condes":70}},
    {"codigo":"SOLN112526","familia":"Solución 1","precio_base":4.19,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":80,"Clínica Indisa":80,"Clínica Las Condes":80}},

    # ── SOLUCIÓN 2 (libre elección, red más amplia c/ Alemana) ─
    {"codigo":"SOLN201526","familia":"Solución 2","precio_base":3.97,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Red Salud Vitacura":70,"Clínica Santa María":70,"Hosp. Clínico UC":70,"Clínica Meds":70,"Clínica U. de los Andes":70,"Clínica Las Condes":70,"Clínica Alemana":50},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":70,"Clínica Las Condes":70,"Clínica Alemana":50}},
    {"codigo":"SOLN204526","familia":"Solución 2","precio_base":4.05,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Red Salud Vitacura":80,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80,"Clínica U. de los Andes":80,"Clínica Las Condes":80,"Clínica Alemana":60},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Las Condes":80,"Clínica Alemana":60}},
    {"codigo":"SOLN202526","familia":"Solución 2","precio_base":4.13,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Red Salud Vitacura":70,"Clínica Santa María":70,"Hosp. Clínico UC":70,"Clínica Meds":70,"Clínica U. de los Andes":70,"Clínica Las Condes":70,"Clínica Alemana":50},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Las Condes":80,"Clínica Alemana":60}},
    {"codigo":"SOLN205526","familia":"Solución 2","precio_base":4.21,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Red Salud Vitacura":80,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80,"Clínica U. de los Andes":80,"Clínica Las Condes":80,"Clínica Alemana":60},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Las Condes":80,"Clínica Alemana":60}},
    {"codigo":"SOLN207526","familia":"Solución 2","precio_base":4.33,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90,"Clínica Alemana":70},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":70,"Clínica Las Condes":70,"Clínica Alemana":50}},
    {"codigo":"SOLN203526","familia":"Solución 2","precio_base":4.45,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Red Salud Vitacura":70,"Clínica Santa María":70,"Hosp. Clínico UC":70,"Clínica Meds":70,"Clínica U. de los Andes":70,"Clínica Las Condes":70,"Clínica Alemana":50},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Las Condes":80,"Clínica Alemana":70}},
    {"codigo":"SOLN206526","familia":"Solución 2","precio_base":4.58,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Red Salud Vitacura":80,"Clínica Santa María":80,"Hosp. Clínico UC":80,"Clínica Meds":80,"Clínica U. de los Andes":80,"Clínica Las Condes":80,"Clínica Alemana":70},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Las Condes":80,"Clínica Alemana":60}},
    {"codigo":"SOLN208526","familia":"Solución 2","precio_base":4.82,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90,"Clínica Alemana":70},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Las Condes":80,"Clínica Alemana":70}},
    {"codigo":"SOLN209526","familia":"Solución 2","precio_base":5.00,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90,"Clínica Alemana":70},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":80,"Clínica Las Condes":80,"Clínica Alemana":70}},
    {"codigo":"SOLN210526","familia":"Solución 2","precio_base":5.22,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90,"Clínica Alemana":80},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Las Condes":90,"Clínica Alemana":80}},
    {"codigo":"SOLN213526","familia":"Solución 2","precio_base":5.31,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":100,"Clínica Red Salud Vitacura":100,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90,"Clínica Alemana":90},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Las Condes":90,"Clínica Alemana":90}},
    {"codigo":"SOLN211526","familia":"Solución 2","precio_base":5.41,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90,"Clínica Alemana":80},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Las Condes":90,"Clínica Alemana":80}},
    {"codigo":"SOLN214526","familia":"Solución 2","precio_base":5.50,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":100,"Clínica Red Salud Vitacura":100,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90,"Clínica Alemana":90},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Las Condes":90,"Clínica Alemana":90}},
    {"codigo":"SOLN212526","familia":"Solución 2","precio_base":5.61,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90,"Clínica Alemana":80},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Las Condes":90,"Clínica Alemana":80}},
    {"codigo":"SOLN215526","familia":"Solución 2","precio_base":5.70,"tipo":"libre_eleccion",
     "cob_hosp":{"Clínica Bupa Santiago":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Red Salud Vitacura":90,"Clínica Santa María":90,"Hosp. Clínico UC":90,"Clínica Meds":90,"Clínica U. de los Andes":90,"Clínica Las Condes":90,"Clínica Alemana":90},
     "cob_amb":{"Clínica Bupa Santiago":100,"Integramédica":100,"Clínica Dávila Recoleta":90,"Clínica Indisa":90,"Clínica Las Condes":90,"Clínica Alemana":90}},
]

# Lista de todas las clínicas para el filtro
CLINICAS_CB = sorted(set(
    c for p in PLANES_CB_RM for c in list(p["cob_hosp"].keys()) + list(p["cob_amb"].keys())
))

# Tope imponible legal (Ley Corta Isapres) en UF
TOPE_IMPONIBLE_UF = 6.3


def get_factor_riesgo(edad: int, rol: str) -> float:
    tabla = FACTOR_RIESGO[rol]
    for min_e, max_e, fr in tabla:
        if min_e <= edad <= max_e:
            return fr
    return 2.4


def calcular_precio_plan(plan: dict, edad_titular: int, edades_cargas: list) -> dict:
    """Calcula el precio total de un plan para titular + cargas."""
    pb = plan["precio_base"]
    n_cotizados = 1 + len(edades_cargas)

    fr_titular = get_factor_riesgo(edad_titular, "contratante")
    precio_titular = fr_titular * pb

    desglose = [{"rol": "Cotizante", "edad": edad_titular, "fr": fr_titular,
                 "precio_uf": precio_titular}]

    precio_cargas = 0.0
    for i, edad in enumerate(edades_cargas):
        fr = get_factor_riesgo(edad, "carga")
        p = fr * pb
        precio_cargas += p
        desglose.append({"rol": f"Carga {i+1}", "edad": edad, "fr": fr,
                          "precio_uf": p})

    ges_total = n_cotizados * GES_UF
    total_uf = precio_titular + precio_cargas + ges_total

    return {
        "total_uf": total_uf,
        "precio_titular_uf": precio_titular,
        "precio_cargas_uf": precio_cargas,
        "ges_uf": ges_total,
        "n_cotizados": n_cotizados,
        "desglose": desglose,
    }


def seleccionar_recomendados(planes_calc: list, sueldo_uf: float, clinica_pref: str) -> list:
    """
    Selecciona automáticamente 2 planes recomendados:
    1. El mejor que cubre la clínica preferida con mayor porcentaje hospitalario
    2. El más económico cercano al 7% del sueldo que también cubre la clínica
    Devuelve lista de índices en planes_calc.
    """
    cotizacion_7 = sueldo_uf * 0.07

    # Ordenar por cobertura hospitalaria de la clínica preferida (desc), luego por precio (asc)
    con_clinica = [
        (i, p) for i, p in enumerate(planes_calc)
        if clinica_pref in p["plan"]["cob_hosp"] or clinica_pref in p["plan"]["cob_amb"]
    ]

    if not con_clinica:
        # Si no hay planes con esa clínica, usar todos
        con_clinica = list(enumerate(planes_calc))

    # Plan 1: mayor cobertura hospitalaria en clínica preferida
    def score_cobertura(item):
        _, p = item
        h = p["plan"]["cob_hosp"].get(clinica_pref, 0)
        a = p["plan"]["cob_amb"].get(clinica_pref, 0)
        return (h + a, -p["calculo"]["total_uf"])

    con_clinica_sorted = sorted(con_clinica, key=score_cobertura, reverse=True)
    idx_mejor = con_clinica_sorted[0][0] if con_clinica_sorted else 0

    # Plan 2: el más cercano al 7% (precio <= cotización 7% si existe, si no el más barato)
    candidatos_7 = [(i, p) for i, p in con_clinica if p["calculo"]["total_uf"] <= cotizacion_7]
    if candidatos_7:
        idx_economico = max(candidatos_7, key=lambda x: x[1]["calculo"]["total_uf"])[0]
    else:
        # Ninguno cabe en el 7%, tomar el más barato
        idx_economico = min(con_clinica, key=lambda x: x[1]["calculo"]["total_uf"])[0]

    if idx_economico == idx_mejor:
        # Si son el mismo, tomar el segundo más barato
        restantes = [(i, p) for i, p in con_clinica if i != idx_mejor]
        if restantes:
            idx_economico = min(restantes, key=lambda x: x[1]["calculo"]["total_uf"])[0]

    return list(dict.fromkeys([idx_mejor, idx_economico]))  # sin duplicados, orden preservado




# ============================================================
# UI STREAMLIT — pegar dentro de cotizador_bupa_pro.py
# Reemplaza el bloque `if seccion == "Cruz Blanca":` 
# ============================================================

def seccion_cruz_blanca(uf_valor: float, asesor: dict):
    """
    Bloque completo de cotización ISAPRE Cruz Blanca.
    uf_valor: float — valor UF del día (ya calculado en el cotizador principal)
    asesor: dict    — datos del asesor logueado (nombre, telefono, email)
    """
    import streamlit as st
    import pandas as pd

    st.markdown("""
    <div style='background:linear-gradient(90deg,#E30613,#b30000);
                padding:14px 20px;border-radius:10px;margin-bottom:18px'>
        <span style='color:white;font-size:1.3rem;font-weight:700'>
        🏥 Cotizador ISAPRE Cruz Blanca
        </span>
        <span style='color:#ffcccc;font-size:0.85rem;margin-left:10px'>
        Tarifario Mayo 2026 · Región Metropolitana
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── FILTROS ────────────────────────────────────────────────
    is_mobile = st.session_state.get("is_mobile", False)
    col_filters = st.expander("⚙️ Filtros y datos del cotizante", expanded=True) if is_mobile else st.container()

    with col_filters:
        c1, c2, c3 = st.columns([2, 2, 2])
        with c1:
            sueldo_input = st.number_input(
                "💰 Sueldo imponible ($)", min_value=0, step=50000,
                value=1500000, key="cb_sueldo",
                help="Sueldo imponible mensual en pesos chilenos"
            )
            sueldo_uf = sueldo_input / uf_valor
            tope_uf = min(sueldo_uf, TOPE_IMPONIBLE_UF)
            cotiz_7_uf  = tope_uf * 0.07
            cotiz_12_uf = tope_uf * 0.12
            st.caption(f"≈ UF {sueldo_uf:.2f} · 7% = UF {cotiz_7_uf:.3f} · 12% = UF {cotiz_12_uf:.3f}")

        with c2:
            edad_titular = st.number_input(
                "👤 Edad cotizante", min_value=18, max_value=99,
                value=35, key="cb_edad_titular"
            )
            n_cargas = st.number_input(
                "👨‍👩‍👧 N° de cargas", min_value=0, max_value=8,
                value=0, key="cb_n_cargas"
            )

        with c3:
            clinica_pref = st.selectbox(
                "🏥 Clínica preferida (hospitalaria)",
                ["(Sin preferencia)"] + CLINICAS_CB,
                key="cb_clinica_pref"
            )
            tipo_plan = st.selectbox(
                "📋 Tipo de plan",
                ["Todos", "Cerrado (solo red Bupa/Integramédica)", "Con libre elección"],
                key="cb_tipo_plan"
            )

        # Edades cargas
        edades_cargas = []
        if n_cargas > 0:
            st.markdown("**Edades de las cargas:**")
            cols_c = st.columns(min(n_cargas, 4))
            for i in range(n_cargas):
                with cols_c[i % 4]:
                    e = st.number_input(f"Carga {i+1}", min_value=0, max_value=99,
                                        value=10, key=f"cb_carga_{i}")
                    edades_cargas.append(e)

    # ── FILTRADO DE PLANES ──────────────────────────────────────
    tipo_map = {
        "Todos": None,
        "Cerrado (solo red Bupa/Integramédica)": "cerrado",
        "Con libre elección": "libre_eleccion",
    }
    filtro_tipo = tipo_map[tipo_plan]

    planes_filtrados = [
        p for p in PLANES_CB_RM
        if (filtro_tipo is None or p["tipo"] == filtro_tipo)
        and (clinica_pref == "(Sin preferencia)"
             or clinica_pref in p["cob_hosp"]
             or clinica_pref in p["cob_amb"])
    ]

    if not planes_filtrados:
        st.warning("⚠️ No se encontraron planes con los filtros seleccionados. Prueba ampliar los criterios.")
        return

    # ── CALCULAR PRECIOS ────────────────────────────────────────
    planes_calc = []
    for p in planes_filtrados:
        calculo = calcular_precio_plan(p, edad_titular, edades_cargas)
        total_clp = calculo["total_uf"] * uf_valor
        adicional_uf = calculo["total_uf"] - cotiz_7_uf
        pct_sueldo = (calculo["total_uf"] / tope_uf * 100) if tope_uf > 0 else 0

        if pct_sueldo <= 7:
            semaforo = "🟢"
            factib = "Cubierto por 7%"
        elif pct_sueldo <= 12:
            semaforo = "🟡"
            factib = f"Adicional UF {adicional_uf:.3f} (≈ ${adicional_uf*uf_valor:,.0f})"
        else:
            semaforo = "🔴"
            factib = f"Supera 12% — no factible (individual)"

        planes_calc.append({
            "plan": p,
            "calculo": calculo,
            "total_clp": total_clp,
            "adicional_uf": adicional_uf,
            "pct_sueldo": pct_sueldo,
            "semaforo": semaforo,
            "factib": factib,
        })

    # Ordenar por precio
    planes_calc.sort(key=lambda x: x["calculo"]["total_uf"])

    # ── SELECCIÓN AUTOMÁTICA DE RECOMENDADOS ────────────────────
    clinica_para_rec = clinica_pref if clinica_pref != "(Sin preferencia)" else "Clínica Bupa Santiago"
    idxs_rec = seleccionar_recomendados(planes_calc, sueldo_uf, clinica_para_rec)

    # Permitir al asesor cambiar la selección
    st.markdown("---")
    st.markdown("#### 📌 Planes seleccionados para cotización")
    st.caption("El sistema pre-seleccionó el mejor y el más económico. Puedes cambiar la selección.")

    opciones_display = [
        f"{p['semaforo']} {p['plan']['codigo']} — {p['plan']['familia']} — UF {p['calculo']['total_uf']:.3f} ({p['pct_sueldo']:.1f}% sueldo)"
        for p in planes_calc
    ]
    seleccionados_idx = st.multiselect(
        "Selecciona 1 o más planes:",
        options=list(range(len(planes_calc))),
        default=idxs_rec,
        format_func=lambda i: opciones_display[i],
        key="cb_seleccion",
    )

    if not seleccionados_idx:
        st.info("Selecciona al menos un plan para ver la cotización.")
        return

    planes_sel = [planes_calc[i] for i in seleccionados_idx]

    # ── TABS DE RESULTADO ───────────────────────────────────────
    tab_detalle, tab_comp, tab_wa, tab_email = st.tabs(
        ["📋 Detalle", "📊 Comparativa", "💬 WhatsApp", "📧 Email"]
    )

    # ── TAB DETALLE ─────────────────────────────────────────────
    with tab_detalle:
        for pc in planes_sel:
            p    = pc["plan"]
            calc = pc["calculo"]
            col_h, col_b = st.columns([3, 2])
            with col_h:
                tag_tipo = "🔒 Cerrado" if p["tipo"] == "cerrado" else "🔓 Libre Elección"
                st.markdown(f"""
                <div style='background:#fff;border:2px solid #E30613;border-radius:10px;
                            padding:16px;margin-bottom:12px'>
                    <div style='color:#E30613;font-size:1rem;font-weight:700'>
                        {p['familia']} &nbsp;<span style='font-size:0.8rem;color:#666'>{tag_tipo}</span>
                    </div>
                    <div style='font-size:0.85rem;color:#444;margin:2px 0 8px'>{p['codigo']}</div>
                    <div style='font-size:1.5rem;font-weight:700;color:#222'>
                        UF {calc['total_uf']:.3f}
                        <span style='font-size:0.95rem;color:#555;font-weight:400'>
                        &nbsp;≈ ${pc['total_clp']:,.0f}/mes
                        </span>
                    </div>
                    <div style='margin-top:6px'>{pc['semaforo']} {pc['factib']}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                st.markdown("**Desglose por beneficiario:**")
                for d in calc["desglose"]:
                    st.markdown(
                        f"- {d['rol']} ({d['edad']} años): "
                        f"UF {d['precio_uf']:.3f} ≈ ${d['precio_uf']*uf_valor:,.0f}"
                    )
                st.markdown(f"- GES ({calc['n_cotizados']} cotizados): UF {calc['ges_uf']:.3f}")

            c_hosp, c_amb = st.columns(2)
            with c_hosp:
                st.markdown("**🏥 Cobertura Hospitalaria:**")
                for cl, pct in sorted(p["cob_hosp"].items(), key=lambda x: -x[1]):
                    star = " ⭐" if cl == clinica_pref else ""
                    st.markdown(f"- {pct}% {cl}{star}")
            with c_amb:
                st.markdown("**💊 Cobertura Ambulatoria:**")
                for cl, pct in sorted(p["cob_amb"].items(), key=lambda x: -x[1]):
                    star = " ⭐" if cl == clinica_pref else ""
                    st.markdown(f"- {pct}% {cl}{star}")

            pdf_url = f"https://raw.githubusercontent.com/momocatracho2-gif/cotizador-pro-bupa/main/pdfs/CB/{p['codigo']}.pdf"
            st.markdown(f"[📎 Ver PDF del plan]({pdf_url})")
            st.markdown("---")

    # ── TAB COMPARATIVA ─────────────────────────────────────────
    with tab_comp:
        filas = []
        for pc in planes_sel:
            p    = pc["plan"]
            calc = pc["calculo"]
            cob_cli = p["cob_hosp"].get(clinica_pref, p["cob_amb"].get(clinica_pref, "-"))
            filas.append({
                "Código": p["codigo"],
                "Familia": p["familia"],
                "Tipo": "Cerrado" if p["tipo"] == "cerrado" else "Libre Elec.",
                f"Cob. {clinica_pref[:15]}": f"{cob_cli}%" if cob_cli != "-" else "-",
                "UF Total": f"{calc['total_uf']:.3f}",
                "$ Total": f"${pc['total_clp']:,.0f}",
                "% Sueldo": f"{pc['pct_sueldo']:.1f}%",
                "Adicional": f"UF {pc['adicional_uf']:.3f}" if pc['adicional_uf'] > 0 else "Sin adicional",
                "": pc["semaforo"],
            })
        st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)

        st.markdown(f"""
        **Referencia sueldo:** UF {sueldo_uf:.2f} (${sueldo_input:,.0f})  
        **7% = UF {cotiz_7_uf:.3f}** · **12% = UF {cotiz_12_uf:.3f}** · **Tope imponible = UF {TOPE_IMPONIBLE_UF}**
        """)

    # ── HELPER: texto de desglose ───────────────────────────────
    def texto_desglose(pc):
        p    = pc["plan"]
        calc = pc["calculo"]
        lineas = []
        for d in calc["desglose"]:
            lineas.append(
                f"   {d['rol']} {d['edad']} años = UF{d['precio_uf']:.3f} - ${d['precio_uf']*uf_valor:,.0f}"
            )
        return "\n".join(lineas)

    def texto_coberturas(pc):
        p = pc["plan"]
        lineas = ["🏥 Cobertura Hospitalaria:"]
        for cl, pct in sorted(p["cob_hosp"].items(), key=lambda x: -x[1]):
            star = " ⭐" if cl == clinica_pref else ""
            lineas.append(f"   {pct}% {cl}{star}")
        lineas.append("💊 Cobertura Ambulatoria:")
        for cl, pct in sorted(p["cob_amb"].items(), key=lambda x: -x[1]):
            star = " ⭐" if cl == clinica_pref else ""
            lineas.append(f"   {pct}% {cl}{star}")
        return "\n".join(lineas)

    def bloque_plan_wa(pc, idx):
        p    = pc["plan"]
        calc = pc["calculo"]
        pdf_url = f"https://raw.githubusercontent.com/momocatracho2-gif/cotizador-pro-bupa/main/pdfs/CB/{p['codigo']}.pdf"
        tag_tipo = "[Cerrado]" if p["tipo"] == "cerrado" else "[Libre Elección]"
        adicional_txt = (
            f"Sin adicional — cubierto por tu 7%"
            if pc["adicional_uf"] <= 0
            else f"Adicional sobre 7%: UF {pc['adicional_uf']:.3f} ≈ ${pc['adicional_uf']*uf_valor:,.0f}/mes"
        )
        return f"""📌 PLAN DE SALUD {idx}
✅ Isapre Cruz Blanca
✅ {p['familia']} {tag_tipo}
   ({p['codigo']})
✅ Valor por Beneficiario
{texto_desglose(pc)}
✅ Valor Mensual
   UF {calc['total_uf']:.3f}
   $ {pc['total_clp']:,.0f}
{pc['semaforo']} {adicional_txt}
✅ Ver y descargar plan 👇🏻
   {pdf_url}
✅ Detalle de Coberturas
{texto_coberturas(pc)}"""

    # ── TAB WHATSAPP ────────────────────────────────────────────
    with tab_wa:
        bloques = []
        for i, pc in enumerate(planes_sel, 1):
            bloques.append(bloque_plan_wa(pc, i))

        # Resumen financiero
        resumen_fin = f"""
📊 RESUMEN FINANCIERO
💰 Sueldo imponible: ${sueldo_input:,.0f} (UF {sueldo_uf:.2f})
📌 Tope imponible Ley Corta: UF {TOPE_IMPONIBLE_UF}
💡 Tu 7% legal = UF {cotiz_7_uf:.3f} (${cotiz_7_uf*uf_valor:,.0f}/mes)
⚠️  Máximo legal (12%) = UF {cotiz_12_uf:.3f} (${cotiz_12_uf*uf_valor:,.0f}/mes)"""

        firma = f"""
---
🩺 {asesor.get('nombre','Asesor Bupa')}
📱 {asesor.get('telefono','')}
✉️ {asesor.get('email','')}
🏢 AsesorIA Seguros · Bupa Chile"""

        msg_wa = "\n\n".join(bloques) + "\n" + resumen_fin + "\n" + firma

        st.text_area("Mensaje WhatsApp:", value=msg_wa, height=500, key="cb_wa_txt")
        st.caption("Copia el texto y pégalo en WhatsApp.")

        is_mobile_st = st.session_state.get("is_mobile", False)
        tel = asesor.get("telefono", "").replace("+", "").replace(" ", "")
        wa_text = msg_wa.replace("\n", "%0A").replace(" ", "%20")
        wa_url = f"https://wa.me/?text={wa_text}" if is_mobile_st else f"https://web.whatsapp.com/send?text={wa_text}"
        st.link_button("💬 Abrir en WhatsApp", url=wa_url)

    # ── TAB EMAIL ───────────────────────────────────────────────
    with tab_email:
        nom_cliente = st.text_input("Nombre del cliente (para el asunto):", key="cb_email_nom", value="")

        asunto_email = f"Cotización ISAPRE Cruz Blanca — {nom_cliente or 'su consulta'}"

        bloques_email = []
        for i, pc in enumerate(planes_sel, 1):
            p    = pc["plan"]
            calc = pc["calculo"]
            pdf_url = f"https://raw.githubusercontent.com/momocatracho2-gif/cotizador-pro-bupa/main/pdfs/CB/{p['codigo']}.pdf"
            tag_tipo = "Plan Cerrado" if p["tipo"] == "cerrado" else "Plan con Libre Elección"
            adicional_txt = (
                "Cubierto íntegramente por su cotización obligatoria del 7%."
                if pc["adicional_uf"] <= 0
                else f"Adicional sobre el 7%: UF {pc['adicional_uf']:.3f} aprox. ${pc['adicional_uf']*uf_valor:,.0f}/mes."
            )

            desglose_lines = "\n".join(
                f"  • {d['rol']} ({d['edad']} años): UF {d['precio_uf']:.3f} ≈ ${d['precio_uf']*uf_valor:,.0f}"
                for d in calc["desglose"]
            )
            hosp_lines = "\n".join(
                f"  • {pct}% {cl}{'  ⭐' if cl == clinica_pref else ''}"
                for cl, pct in sorted(p["cob_hosp"].items(), key=lambda x: -x[1])
            )
            amb_lines = "\n".join(
                f"  • {pct}% {cl}{'  ⭐' if cl == clinica_pref else ''}"
                for cl, pct in sorted(p["cob_amb"].items(), key=lambda x: -x[1])
            )

            bloques_email.append(f"""OPCIÓN {i}: {p['familia']} — {tag_tipo}
Código: {p['codigo']}

Valor mensual: UF {calc['total_uf']:.3f} ≈ ${pc['total_clp']:,.0f}

Desglose por beneficiario:
{desglose_lines}
  • GES ({calc['n_cotizados']} cotizados): UF {calc['ges_uf']:.3f}

{pc['semaforo']} {adicional_txt}

Coberturas hospitalarias:
{hosp_lines}

Coberturas ambulatorias:
{amb_lines}

Ver plan: {pdf_url}
""")

        cuerpo_email = f"""Estimado/a {nom_cliente or 'cliente'},

Le presento la cotización de ISAPRE Cruz Blanca según los datos proporcionados.

DATOS FINANCIEROS
Sueldo imponible: ${sueldo_input:,.0f} (UF {sueldo_uf:.2f})
Tope imponible Ley Corta: UF {TOPE_IMPONIBLE_UF}
Cotización obligatoria 7%: UF {cotiz_7_uf:.3f} (${cotiz_7_uf*uf_valor:,.0f}/mes)
Máximo legal 12%: UF {cotiz_12_uf:.3f} (${cotiz_12_uf*uf_valor:,.0f}/mes)

{"="*50}

{"=" * 50 + chr(10) + ("=" * 50 + chr(10)).join(bloques_email)}

Cualquier consulta quedo a su disposición.

Saludos cordiales,
{asesor.get('nombre','Asesor Bupa')}
{asesor.get('telefono','')} | {asesor.get('email','')}
AsesorIA Seguros · Bupa Chile
"""
        st.text_area("Cuerpo del email:", value=cuerpo_email, height=500, key="cb_email_txt")
        outlook_url = (
            f"https://outlook.live.com/mail/0/deeplink/compose?"
            f"subject={asunto_email.replace(' ','%20')}"
            f"&body={cuerpo_email.replace(chr(10),'%0A').replace(' ','%20')}"
        )
        st.link_button("📧 Abrir en Outlook Online", url=outlook_url)

