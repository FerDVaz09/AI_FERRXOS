# 🤖 AI_FERRXOS - Asistente Invisible para Reuniones

> Copiloto IA para tu escritorio. Analiza reuniones en tiempo real, invisible para Zoom/Teams.
>
> 📥 **[Descargar v1.0 (120 MB)](https://github.com/FerDVaz09/AI_FERRXOS/releases/download/v1.0/AI_FERRXOS.exe)**

## 📋 Características

✅ **Ghost Mode**: Ventana invisible en compartir pantalla  
✅ **IA en Tiempo Real**: Análisis con Gemini 1.5 Flash  
✅ **Múltiples Modos**: Entrevista, Negocios, Presentación, Custom  
✅ **Historial Inteligente**: Guarda y busca resúmenes  
✅ **Dark Mode**: Diseño estilo Bloomberg Terminal  

## 🚀 Requisitos

- **Python**: 3.10+
- **Windows**: 10/11 (Ghost Mode requiere Windows)
- **API Key**: Google Gemini (gratis hasta 15 req/min)

## 📦 Instalación

```bash
# 1. Clonar proyecto
git clone https://github.com/FerDVaz09/AI_FERRXOS.git
cd AI_FERRXOS

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # En Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Obtener API Key (gratis)
# Ir a: https://ai.google.dev/
# Crear clave en "Get API Key"

# 5. Ejecutar
python src/main.py
```

## 🎯 Uso Rápido

1. **Abre la app** → Pestaña "⚙️ Configuración"
2. **Pega tu API Key** de Google Gemini
3. **Selecciona modo** (Negocios, Entrevista, etc.)
4. **Guarda configuración** → 💾
5. **Inicia reunión** → ▶️ en pestaña "📡 Live Feed"
6. **Análisis automático** en panel derecho
7. **Finaliza** → ⏹️ Se guarda en "📋 Historial"

## 📁 Estructura

```
AI_FERRXOS/
├── src/
│   ├── main.py                 # Entrada
│   ├── config.json             # Config guardada
│   ├── history.json            # Historial
│   ├── ui/
│   │   ├── main_window.py      # Ventana principal
│   │   ├── styles.py           # Estilos dark
│   │   └── widgets.py          # Widgets
│   └── core/
│       ├── ai_brain.py         # Gemini
│       ├── ghost.py            # Invisibilidad
│       └── audio.py            # Audio
├── web/
│   ├── index.html              # Landing
│   └── style.css               # Estilos
├── requirements.txt
└── README.md
```

## 🔧 Configuración

### `config.json`

```json
{
  "api_key": "tu-clave-aqui",
  "modo": "negocios",
  "custom_prompt": "Actúa como...",
  "ghost_mode_enabled": true
}
```

### `history.json`

Automático. Cada reunión genera:

```json
{
  "id": "uuid-001",
  "fecha": "2026-01-02 10:30:00",
  "titulo": "Reunión Freddy",
  "modo": "NEGOCIOS",
  "resumen_ia": "...",
  "transcript_completo": "..."
}
```

## 🌟 Modos IA

| Modo | Caso de Uso | Ejemplo |
|------|-------------|---------|
| 🎤 **Entrevista** | Entrevistas técnicas | Analizar respuestas de candidatos |
| 💼 **Negocios** | Sales/Negociaciones | Detectar objeciones, oportunidades |
| 🗣️ **Presentación** | Presentaciones | Control de ritmo, claridad |
| 🛠️ **Custom** | Personalizado | Tu propio prompt |

## 🔐 Seguridad

- ✅ API Key guardada **encriptada** localmente
- ✅ Ventana **invisible** en capturas de pantalla
- ✅ **Sin datos** en la nube (solo archivos JSON locales)
- ✅ **Open Source** - Revisa el código

## 📞 Soporte & Contacto

- 📧 Email: **ferdypruebass@gmail.com**
- 💬 Discord: **ferxxos_08**
- 🐛 Reportar bugs: [GitHub Issues](https://github.com/FerDVaz09/AI_FERRXOS/issues)
- 📖 Documentación: [Ver en GitHub](https://github.com/FerDVaz09/AI_FERRXOS)

## 📄 Licencia

Privada - 2026 © AI_FERRXOS - Desarrollado por **ferxxos_08**

---

**Made with ❤️ in Python**  
*Copiloto Invisible. Análisis Visible.*
