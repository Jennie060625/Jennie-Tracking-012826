import os
import re
import io
import json
import time
import random
import yaml
import math
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

import streamlit as st

# Optional plotting
try:
    import pandas as pd
except Exception:
    pd = None

try:
    import altair as alt
except Exception:
    alt = None


# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Antigravity Agentic AI — WOW Workspace",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# I18N (English / Traditional Chinese)
# =========================
I18N = {
    "en": {
        "app_title": "Antigravity Agentic Workspace — WOW UI",
        "subtitle": "Theme + Language + Painter Styles + Agent Chains + AI Note Keeper",
        "sidebar_config": "Configuration",
        "appearance": "Appearance",
        "theme_mode": "Theme Mode",
        "light": "Light",
        "dark": "Dark",
        "language": "Language",
        "style_engine": "Style Engine (20 Painter Styles)",
        "choose_style": "Choose Style",
        "jackpot": "Jackpot",
        "api_keys": "API Keys",
        "openai_key": "OpenAI API Key",
        "gemini_key": "Gemini API Key",
        "anthropic_key": "Anthropic API Key",
        "grok_key": "Grok (xAI) API Key",
        "loaded_from_env": "Loaded from environment (hidden)",
        "enter_if_missing": "Enter if not set in ENV",
        "tabs_workspace": "Workspace",
        "tabs_agents": "Agents",
        "tabs_notes": "AI Note Keeper",
        "tabs_history": "History",
        "tabs_settings": "Settings",
        "dashboard": "Interactive Dashboard",
        "status": "WOW Status",
        "documents": "Document Input",
        "upload": "Upload Text / MD / PDF / CSV",
        "load_sample": "Load sample dataset",
        "doc_preview": "Preview",
        "scan_keywords": "Scan for Keywords",
        "keyword_color": "Keyword highlight color",
        "keyword_list": "Keywords (comma-separated)",
        "context": "Context",
        "select_context_doc": "Select Context Document",
        "or_manual_context": "Or paste manual context",
        "agents_exec": "Agent Execution",
        "chain_agents": "Chain Agents",
        "start_chain": "Start Chain (step-by-step)",
        "run_all": "Run Chain (auto)",
        "reset_chain": "Reset Chain Session",
        "agent_config": "Agent Config",
        "model": "Model",
        "max_tokens": "Max tokens",
        "temperature": "Temperature",
        "prompt": "Prompt",
        "system_prompt": "System prompt",
        "input_to_agent": "Input to this agent",
        "run_agent": "Run this agent",
        "output": "Output",
        "output_view": "Output view",
        "markdown": "Markdown",
        "text": "Text",
        "edit_output_for_next": "Edit output to use as input for next agent",
        "use_as_next": "Use edited output as next input",
        "next_agent": "Next agent",
        "complete": "Complete",
        "history": "Execution History",
        "agents_yaml_editor": "Edit agents.yaml",
        "save_config": "Save Config",
        "saved": "Saved",
        "invalid_yaml": "Invalid YAML",
        "note_input": "Paste note (text/markdown)",
        "organize": "Organize into markdown",
        "note_view": "Note view",
        "ai_magics": "AI Magics",
        "magic_format": "AI Formatting (Organize)",
        "magic_summary": "AI Summary",
        "magic_actions": "AI Action Items",
        "magic_flashcards": "AI Flashcards",
        "magic_translate": "AI Translate (EN ↔ ZH-TW)",
        "magic_keywords": "AI Keywords Highlight",
        "ask_on_note": "Ask AI on this note (keeps prompt on the note)",
        "ask": "Ask",
        "provider_status": "Provider status",
        "keys_status": "Keys status",
        "token_estimate": "Token estimate",
        "runs_today": "Runs (session)",
        "last_run": "Last run",
        "clear_history": "Clear history",
    },
    "zh-TW": {
        "app_title": "反重力 Agentic 工作台 — WOW 介面",
        "subtitle": "主題 + 語言 + 畫家風格 + Agent 鏈 + AI 筆記整理",
        "sidebar_config": "設定",
        "appearance": "外觀",
        "theme_mode": "主題模式",
        "light": "淺色",
        "dark": "深色",
        "language": "語言",
        "style_engine": "風格引擎（20 種畫家風格）",
        "choose_style": "選擇風格",
        "jackpot": "彩球",
        "api_keys": "API 金鑰",
        "openai_key": "OpenAI API 金鑰",
        "gemini_key": "Gemini API 金鑰",
        "anthropic_key": "Anthropic API 金鑰",
        "grok_key": "Grok（xAI）API 金鑰",
        "loaded_from_env": "已由環境變數載入（不顯示）",
        "enter_if_missing": "若 ENV 未設定請輸入",
        "tabs_workspace": "工作區",
        "tabs_agents": "Agents",
        "tabs_notes": "AI 筆記管家",
        "tabs_history": "歷史紀錄",
        "tabs_settings": "設定",
        "dashboard": "互動式儀表板",
        "status": "WOW 狀態",
        "documents": "文件輸入",
        "upload": "上傳 Text / MD / PDF / CSV",
        "load_sample": "載入範例資料集",
        "doc_preview": "預覽",
        "scan_keywords": "掃描關鍵字",
        "keyword_color": "關鍵字高亮顏色",
        "keyword_list": "關鍵字（逗號分隔）",
        "context": "上下文",
        "select_context_doc": "選擇上下文文件",
        "or_manual_context": "或貼上手動上下文",
        "agents_exec": "Agent 執行",
        "chain_agents": "串接 Agents",
        "start_chain": "開始串接（逐步）",
        "run_all": "執行串接（自動）",
        "reset_chain": "重置串接工作階段",
        "agent_config": "Agent 設定",
        "model": "模型",
        "max_tokens": "Max tokens",
        "temperature": "溫度",
        "prompt": "提示詞",
        "system_prompt": "系統提示詞",
        "input_to_agent": "本 Agent 的輸入",
        "run_agent": "執行此 Agent",
        "output": "輸出",
        "output_view": "輸出檢視",
        "markdown": "Markdown",
        "text": "文字",
        "edit_output_for_next": "編輯輸出（作為下一個 Agent 的輸入）",
        "use_as_next": "使用編輯後輸出作為下一步輸入",
        "next_agent": "下一個 Agent",
        "complete": "完成",
        "history": "執行歷史",
        "agents_yaml_editor": "編輯 agents.yaml",
        "save_config": "儲存設定",
        "saved": "已儲存",
        "invalid_yaml": "YAML 格式錯誤",
        "note_input": "貼上筆記（文字/Markdown）",
        "organize": "整理成 Markdown",
        "note_view": "筆記檢視",
        "ai_magics": "AI 魔法",
        "magic_format": "AI 排版整理（組織化）",
        "magic_summary": "AI 摘要",
        "magic_actions": "AI 行動事項",
        "magic_flashcards": "AI 記憶卡",
        "magic_translate": "AI 翻譯（英 ↔ 繁中）",
        "magic_keywords": "AI 關鍵字高亮",
        "ask_on_note": "針對此筆記提問（保留 Prompt 在筆記上）",
        "ask": "提問",
        "provider_status": "供應商狀態",
        "keys_status": "金鑰狀態",
        "token_estimate": "Token 估算",
        "runs_today": "執行次數（本 session）",
        "last_run": "最後執行",
        "clear_history": "清除歷史",
    },
}

# =========================
# Styles (20 painter styles + cyberpunk + bauhaus etc.)
# =========================
PAINTER_STYLES = [
    "van_gogh", "picasso", "monet", "da_vinci", "dali",
    "mondrian", "warhol", "rembrandt", "klimt", "hokusai",
    "munch", "okeeffe", "basquiat", "matisse", "pollock",
    "kahlo", "hopper", "magritte", "cyberpunk", "bauhaus",
]

STYLE_PALETTES = {
    "van_gogh": dict(accent="#F2C14E", accent2="#3A86FF", glow="#FFD166"),
    "picasso": dict(accent="#EF476F", accent2="#118AB2", glow="#FFD166"),
    "monet": dict(accent="#7BDFF2", accent2="#B2F7EF", glow="#EFF7F6"),
    "da_vinci": dict(accent="#B08968", accent2="#7F5539", glow="#E6CCB2"),
    "dali": dict(accent="#FFD60A", accent2="#7400B8", glow="#FFEE99"),
    "mondrian": dict(accent="#E63946", accent2="#1D3557", glow="#F1FAEE"),
    "warhol": dict(accent="#FF4D6D", accent2="#00BBF9", glow="#FEE440"),
    "rembrandt": dict(accent="#8D6E63", accent2="#3E2723", glow="#D7CCC8"),
    "klimt": dict(accent="#D4AF37", accent2="#7B2CBF", glow="#F7E7A9"),
    "hokusai": dict(accent="#1D4ED8", accent2="#60A5FA", glow="#DBEAFE"),
    "munch": dict(accent="#FF5D8F", accent2="#2D2A32", glow="#FFD6E8"),
    "okeeffe": dict(accent="#2A9D8F", accent2="#E76F51", glow="#F4A261"),
    "basquiat": dict(accent="#FCA311", accent2="#14213D", glow="#E5E5E5"),
    "matisse": dict(accent="#FF7A00", accent2="#00A6FB", glow="#FDE74C"),
    "pollock": dict(accent="#06D6A0", accent2="#073B4C", glow="#FFD166"),
    "kahlo": dict(accent="#2EC4B6", accent2="#E71D36", glow="#FF9F1C"),
    "hopper": dict(accent="#457B9D", accent2="#F4A261", glow="#E9C46A"),
    "magritte": dict(accent="#4361EE", accent2="#F72585", glow="#B5179E"),
    "cyberpunk": dict(accent="#00F5D4", accent2="#F15BB5", glow="#FEE440"),
    "bauhaus": dict(accent="#E63946", accent2="#FCA311", glow="#1D3557"),
}


def _css(theme_mode: str, painter_style: str) -> str:
    pal = STYLE_PALETTES.get(painter_style, STYLE_PALETTES["van_gogh"])
    if theme_mode == "dark":
        bg = "#0b0f19"
        panel = "rgba(255,255,255,0.06)"
        panel2 = "rgba(255,255,255,0.10)"
        text = "rgba(255,255,255,0.92)"
        muted = "rgba(255,255,255,0.70)"
        border = "rgba(255,255,255,0.12)"
    else:
        bg = "#f7f8fc"
        panel = "rgba(0,0,0,0.04)"
        panel2 = "rgba(0,0,0,0.06)"
        text = "rgba(0,0,0,0.88)"
        muted = "rgba(0,0,0,0.65)"
        border = "rgba(0,0,0,0.10)"

    accent = pal["accent"]
    accent2 = pal["accent2"]
    glow = pal["glow"]

    return f"""
    <style>
      :root {{
        --wow-bg: {bg};
        --wow-panel: {panel};
        --wow-panel2: {panel2};
        --wow-text: {text};
        --wow-muted: {muted};
        --wow-border: {border};
        --wow-accent: {accent};
        --wow-accent2: {accent2};
        --wow-glow: {glow};
        --wow-radius: 18px;
      }}

      /* App background */
      [data-testid="stAppViewContainer"] {{
        background: radial-gradient(1200px 700px at 10% 10%, color-mix(in srgb, var(--wow-accent) 25%, transparent), transparent 60%),
                    radial-gradient(900px 600px at 90% 0%, color-mix(in srgb, var(--wow-accent2) 18%, transparent), transparent 55%),
                    var(--wow-bg) !important;
        color: var(--wow-text);
      }}

      /* Reduce top padding a bit */
      .block-container {{
        padding-top: 1.1rem;
      }}

      /* Sidebar */
      [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, color-mix(in srgb, var(--wow-panel) 80%, transparent), transparent) !important;
        border-right: 1px solid var(--wow-border);
      }}

      /* Cards */
      .wow-card {{
        background: linear-gradient(180deg, var(--wow-panel), transparent);
        border: 1px solid var(--wow-border);
        border-radius: var(--wow-radius);
        padding: 1rem 1rem;
        box-shadow: 0 18px 60px rgba(0,0,0,0.15);
      }}

      .wow-hero {{
        border-radius: calc(var(--wow-radius) + 6px);
        padding: 1.15rem 1.2rem;
        border: 1px solid var(--wow-border);
        background: linear-gradient(110deg,
          color-mix(in srgb, var(--wow-accent) 20%, transparent),
          color-mix(in srgb, var(--wow-accent2) 16%, transparent));
      }}

      .wow-title {{
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
      }}
      .wow-subtitle {{
        margin: 0.35rem 0 0 0;
        color: var(--wow-muted);
      }}

      .wow-chip {{
        display: inline-flex;
        gap: 0.45rem;
        align-items: center;
        padding: 0.35rem 0.6rem;
        border-radius: 999px;
        border: 1px solid var(--wow-border);
        background: color-mix(in srgb, var(--wow-panel2) 85%, transparent);
        font-size: 0.85rem;
        color: var(--wow-text);
        margin-right: 0.35rem;
        margin-top: 0.35rem;
      }}
      .wow-dot {{
        width: 9px; height: 9px; border-radius: 50%;
        background: var(--wow-accent);
        box-shadow: 0 0 0 4px color-mix(in srgb, var(--wow-accent) 25%, transparent);
      }}
      .wow-dot2 {{
        background: var(--wow-accent2);
        box-shadow: 0 0 0 4px color-mix(in srgb, var(--wow-accent2) 25%, transparent);
      }}

      /* Make buttons look more premium */
      .stButton > button {{
        border-radius: 14px !important;
        border: 1px solid var(--wow-border) !important;
        background: linear-gradient(135deg,
          color-mix(in srgb, var(--wow-accent) 22%, transparent),
          color-mix(in srgb, var(--wow-accent2) 18%, transparent)) !important;
        color: var(--wow-text) !important;
        font-weight: 650 !important;
      }}
      .stButton > button:hover {{
        border-color: color-mix(in srgb, var(--wow-accent) 55%, var(--wow-border)) !important;
      }}

      /* Text areas / inputs */
      .stTextArea textarea, .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 14px !important;
        border: 1px solid var(--wow-border) !important;
        background: color-mix(in srgb, var(--wow-panel2) 70%, transparent) !important;
        color: var(--wow-text) !important;
      }}

      /* Expanders */
      details {{
        border-radius: var(--wow-radius) !important;
        border: 1px solid var(--wow-border) !important;
        background: color-mix(in srgb, var(--wow-panel) 85%, transparent) !important;
        padding: 0.35rem 0.6rem;
      }}

      /* Metric widgets */
      [data-testid="stMetric"] {{
        background: color-mix(in srgb, var(--wow-panel) 70%, transparent);
        border-radius: var(--wow-radius);
        border: 1px solid var(--wow-border);
        padding: 0.9rem;
      }}

      /* Keyword highlight spans */
      .kw {{
        padding: 0.08rem 0.25rem;
        border-radius: 0.5rem;
        border: 1px solid color-mix(in srgb, var(--wow-border) 60%, transparent);
        margin: 0 0.08rem;
        display: inline-block;
      }}
    </style>
    """


# =========================
# Session State Init
# =========================
def ss_init():
    if "lang" not in st.session_state:
        st.session_state.lang = "en"
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "dark"
    if "painter_style" not in st.session_state:
        st.session_state.painter_style = "van_gogh"

    if "agents_config" not in st.session_state:
        st.session_state.agents_config = None

    if "processed_docs" not in st.session_state:
        st.session_state.processed_docs = {}  # name -> text
    if "execution_log" not in st.session_state:
        st.session_state.execution_log = []  # list of dicts

    if "chain_state" not in st.session_state:
        st.session_state.chain_state = {
            "active": False,
            "agents": [],
            "idx": 0,
            "current_input": "",
            "last_output": "",
            "overrides": {},  # agent_name -> override dict
        }

    if "runs" not in st.session_state:
        st.session_state.runs = 0
    if "last_run_ts" not in st.session_state:
        st.session_state.last_run_ts = None

    # Keys entered by user (only if not in env). Never persist outside session.
    if "ui_keys" not in st.session_state:
        st.session_state.ui_keys = {
            "OPENAI_API_KEY": "",
            "GEMINI_API_KEY": "",
            "ANTHROPIC_API_KEY": "",
            "GROK_API_KEY": "",
        }

    if "note_text" not in st.session_state:
        st.session_state.note_text = ""
    if "note_markdown" not in st.session_state:
        st.session_state.note_markdown = ""
    if "note_last_ai" not in st.session_state:
        st.session_state.note_last_ai = ""


ss_init()
t = I18N[st.session_state.lang]

# Apply CSS theme
st.markdown(_css(st.session_state.theme_mode, st.session_state.painter_style), unsafe_allow_html=True)


# =========================
# Utilities
# =========================
def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def estimate_tokens(text: str) -> int:
    # Very rough estimate (English ~4 chars/token, Chinese less predictable; still OK for UI)
    if not text:
        return 0
    return max(1, int(len(text) / 4))


def get_api_key(env_var: str) -> Tuple[Optional[str], bool]:
    """
    Returns (key, from_env_bool).
    If not found in env, uses session_state.ui_keys[env_var].
    """
    if os.environ.get(env_var):
        return os.environ.get(env_var), True
    v = st.session_state.ui_keys.get(env_var, "")
    return (v if v else None), False


def safe_read_uploaded(file) -> Tuple[str, str]:
    """
    Returns (doc_name, text_content). Handles: txt/md/csv/pdf.
    """
    name = file.name
    mime = file.type or ""

    # PDF
    if mime == "application/pdf" or name.lower().endswith(".pdf"):
        return name, extract_pdf_text(file.read(), pages_spec="1")

    # CSV -> convert to markdown table preview (first N rows)
    if (mime in ["text/csv", "application/vnd.ms-excel"]) or name.lower().endswith(".csv"):
        b = file.read()
        try:
            s = b.decode("utf-8")
        except Exception:
            s = b.decode("utf-8", errors="ignore")

        if pd is None:
            return name, s

        try:
            df = pd.read_csv(io.StringIO(s))
            head = df.head(50)
            return name, head.to_markdown(index=False)
        except Exception:
            return name, s

    # plain text / markdown
    b = file.read()
    try:
        return name, b.decode("utf-8")
    except Exception:
        return name, b.decode("utf-8", errors="ignore")


def extract_pdf_text(pdf_bytes: bytes, pages_spec: str = "1") -> str:
    """
    Extract PDF text by pages_spec like: "1" or "1-3,5".
    Requires pypdf (preferred) or PyPDF2.
    """
    pages_spec = (pages_spec or "").strip() or "1"
    page_numbers = set()

    def add_range(a, b):
        for i in range(a, b + 1):
            page_numbers.add(i)

    for part in pages_spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            try:
                add_range(int(a), int(b))
            except Exception:
                pass
        else:
            try:
                page_numbers.add(int(part))
            except Exception:
                pass

    # fallback if parsing fails
    if not page_numbers:
        page_numbers = {1}

    try:
        from pypdf import PdfReader  # type: ignore
        reader = PdfReader(io.BytesIO(pdf_bytes))
        texts = []
        for p in sorted(page_numbers):
            idx = p - 1
            if 0 <= idx < len(reader.pages):
                texts.append(reader.pages[idx].extract_text() or "")
        return "\n\n".join(texts).strip() or "(No extractable text found in PDF.)"
    except Exception:
        try:
            from PyPDF2 import PdfReader  # type: ignore
            reader = PdfReader(io.BytesIO(pdf_bytes))
            texts = []
            for p in sorted(page_numbers):
                idx = p - 1
                if 0 <= idx < len(reader.pages):
                    texts.append(reader.pages[idx].extract_text() or "")
            return "\n\n".join(texts).strip() or "(No extractable text found in PDF.)"
        except Exception as e:
            return f"(PDF extraction failed: {e})"


def highlight_keywords_html(text: str, keywords: List[str], color: str = "#FF6B6B") -> str:
    """
    Wrap keywords with <span class="kw" style="background:...">keyword</span>.
    Returns HTML (safe to render with unsafe_allow_html=True).
    """
    if not text or not keywords:
        return f"<div>{escape_html(text)}</div>"

    # Escape text first, then re-inject highlights by working on escaped text is tricky.
    # Instead: do a safer approach: split/replace on original but escape pieces.
    # We'll do regex substitution and escape non-matching segments using a callback.
    kws = [k.strip() for k in keywords if k and k.strip()]
    if not kws:
        return f"<div>{escape_html(text)}</div>"

    pattern = re.compile("(" + "|".join(re.escape(k) for k in sorted(set(kws), key=len, reverse=True)) + ")", re.IGNORECASE)

    def repl(m):
        kw = escape_html(m.group(0))
        return f'<span class="kw" style="background:{color}; color:#111; font-weight:700;">{kw}</span>'

    # Escape everything then unescape within matches is hard; do: segment-based
    out = []
    last = 0
    for m in pattern.finditer(text):
        out.append(escape_html(text[last:m.start()]))
        out.append(repl(m))
        last = m.end()
    out.append(escape_html(text[last:]))
    return "<div style='line-height:1.65;'>" + "".join(out).replace("\n", "<br/>") + "</div>"


def escape_html(s: str) -> str:
    if s is None:
        return ""
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#039;")
    )


def render_template(tpl: str, variables: Dict[str, Any]) -> str:
    """
    Lightweight templating:
      - supports {input}, {context}, {note}, etc.
    """
    tpl = tpl or "{input}"
    try:
        return tpl.format(**variables)
    except Exception:
        # If formatting fails, fall back to raw
        return tpl


# =========================
# Agents YAML
# =========================
AGENTS_YAML_PATH = "agents.yaml"


def load_agents_config() -> Dict[str, Any]:
    if not os.path.exists(AGENTS_YAML_PATH):
        # Minimal fallback to keep app alive
        return {
            "agents": [
                {
                    "name": "Agent-1",
                    "provider": "openai",
                    "model": "gpt-4o-mini",
                    "system_prompt": "You are a helpful assistant.",
                    "prompt": "{input}",
                    "temperature": 0.2,
                    "max_tokens": 12000,
                }
            ]
        }
    with open(AGENTS_YAML_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"agents": []}


def save_agents_config(cfg: Dict[str, Any]) -> None:
    with open(AGENTS_YAML_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False, allow_unicode=True)


if st.session_state.agents_config is None:
    st.session_state.agents_config = load_agents_config()


# =========================
# Model + Provider Routing
# =========================
MODEL_CHOICES = [
    # OpenAI
    "gpt-4o-mini",
    "gpt-4.1-mini",

    # Gemini
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3-flash-preview",

    # Anthropic (common options)
    "claude-3-5-sonnet-latest",
    "claude-3-5-haiku-latest",
    "claude-3-opus-latest",

    # Grok (xAI)
    "grok-4-fast-reasoning",
    "grok-3-mini",
]

# best-effort provider inference
def infer_provider(model: str) -> str:
    m = (model or "").lower()
    if m.startswith("gpt-"):
        return "openai"
    if m.startswith("gemini-"):
        return "gemini"
    if m.startswith("claude-"):
        return "anthropic"
    if m.startswith("grok-"):
        return "grok"
    return "openai"


def call_llm(
    provider: str,
    model: str,
    api_key: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 12000,
    temperature: float = 0.2,
) -> Tuple[str, Dict[str, Any]]:
    """
    Returns (text, meta). Meta includes provider/model and best-effort usage.
    """
    provider = (provider or infer_provider(model)).lower().strip()
    meta = {"provider": provider, "model": model, "max_tokens": max_tokens, "temperature": temperature}

    if provider == "openai":
        try:
            from openai import OpenAI  # type: ignore
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt or ""},
                    {"role": "user", "content": user_prompt or ""},
                ],
                temperature=float(temperature),
                max_tokens=int(max_tokens),
            )
            text = resp.choices[0].message.content or ""
            usage = getattr(resp, "usage", None)
            if usage:
                meta["usage"] = dict(usage)
            return text, meta
        except Exception as e:
            return f"(OpenAI call failed: {e})", meta

    if provider == "gemini":
        try:
            import google.generativeai as genai  # type: ignore
            genai.configure(api_key=api_key)
            # Gemini uses system instruction differently; pass as system_instruction when supported.
            try:
                model_obj = genai.GenerativeModel(model_name=model, system_instruction=system_prompt or "")
            except Exception:
                model_obj = genai.GenerativeModel(model_name=model)

            resp = model_obj.generate_content(
                user_prompt or "",
                generation_config={"temperature": float(temperature), "max_output_tokens": int(max_tokens)},
            )
            text = getattr(resp, "text", None) or ""
            return text, meta
        except Exception as e:
            return f"(Gemini call failed: {e})", meta

    if provider == "anthropic":
        try:
            from anthropic import Anthropic  # type: ignore
            client = Anthropic(api_key=api_key)
            resp = client.messages.create(
                model=model,
                max_tokens=int(max_tokens),
                temperature=float(temperature),
                system=system_prompt or "",
                messages=[{"role": "user", "content": user_prompt or ""}],
            )
            # resp.content is list of blocks
            blocks = getattr(resp, "content", []) or []
            text_parts = []
            for b in blocks:
                # anthropic block has .text
                tx = getattr(b, "text", None)
                if tx:
                    text_parts.append(tx)
            text = "\n".join(text_parts).strip()
            return text, meta
        except Exception as e:
            return f"(Anthropic call failed: {e})", meta

    if provider == "grok":
        # Grok is OpenAI-compatible via https://api.x.ai/v1
        try:
            from openai import OpenAI  # type: ignore
            client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt or ""},
                    {"role": "user", "content": user_prompt or ""},
                ],
                temperature=float(temperature),
                max_tokens=int(max_tokens),
            )
            text = resp.choices[0].message.content or ""
            usage = getattr(resp, "usage", None)
            if usage:
                meta["usage"] = dict(usage)
            return text, meta
        except Exception as e:
            return f"(Grok call failed: {e})", meta

    return f"(Unknown provider '{provider}'.)", meta


def run_agent(
    agent_conf: Dict[str, Any],
    input_text: str,
    overrides: Dict[str, Any],
    keys: Dict[str, Optional[str]],
) -> Tuple[str, Dict[str, Any]]:
    """
    agent_conf: from agents.yaml
    overrides: per-run override: model/max_tokens/temperature/prompt/system_prompt/provider
    keys: dict of resolved api keys by provider
    """
    # base fields
    name = agent_conf.get("name", "Unnamed Agent")
    base_model = agent_conf.get("model", "gpt-4o-mini")
    base_provider = agent_conf.get("provider", infer_provider(base_model))
    base_prompt = agent_conf.get("prompt", "{input}")
    base_system = agent_conf.get("system_prompt", "You are a helpful assistant.")
    base_temp = float(agent_conf.get("temperature", 0.2))
    base_max = int(agent_conf.get("max_tokens", 12000))

    # overrides
    provider = overrides.get("provider", base_provider)
    model = overrides.get("model", base_model)
    prompt_tpl = overrides.get("prompt", base_prompt)
    system_prompt = overrides.get("system_prompt", base_system)
    temperature = float(overrides.get("temperature", base_temp))
    max_tokens = int(overrides.get("max_tokens", base_max))

    provider = (provider or infer_provider(model)).lower().strip()

    # choose key
    if provider == "openai":
        api_key = keys.get("openai")
    elif provider == "gemini":
        api_key = keys.get("gemini")
    elif provider == "anthropic":
        api_key = keys.get("anthropic")
    elif provider == "grok":
        api_key = keys.get("grok")
    else:
        api_key = None

    if not api_key:
        return f"(Missing API key for provider '{provider}' while running {name}.)", {
            "agent": name,
            "provider": provider,
            "model": model,
            "error": "missing_api_key",
        }

    user_prompt = render_template(prompt_tpl, {"input": input_text})

    started = time.time()
    text, meta = call_llm(
        provider=provider,
        model=model,
        api_key=api_key,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    elapsed = time.time() - started

    meta.update({"agent": name, "elapsed_s": round(elapsed, 3)})
    return text, meta


# =========================
# WOW Sidebar
# =========================
with st.sidebar:
    st.markdown(f"### ⚙️ {t['sidebar_config']}")

    st.markdown(f"#### ✨ {t['appearance']}")
    colA, colB = st.columns(2)
    with colA:
        st.session_state.theme_mode = st.selectbox(
            t["theme_mode"],
            ["dark", "light"],
            index=0 if st.session_state.theme_mode == "dark" else 1,
            format_func=lambda x: t["dark"] if x == "dark" else t["light"],
        )
    with colB:
        st.session_state.lang = st.selectbox(
            t["language"],
            ["en", "zh-TW"],
            index=0 if st.session_state.lang == "en" else 1,
        )
        t = I18N[st.session_state.lang]  # refresh language strings

    st.markdown(f"#### 🎨 {t['style_engine']}")
    c1, c2 = st.columns([3, 1])
    with c1:
        st.session_state.painter_style = st.selectbox(
            t["choose_style"], PAINTER_STYLES, index=PAINTER_STYLES.index(st.session_state.painter_style)
        )
    with c2:
        if st.button("🎰 " + t["jackpot"], use_container_width=True):
            st.session_state.painter_style = random.choice(PAINTER_STYLES)
            st.rerun()

    # Re-apply CSS after any sidebar changes
    st.markdown(_css(st.session_state.theme_mode, st.session_state.painter_style), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"#### 🔑 {t['api_keys']}")

    def key_input(env_var: str, label: str):
        key, from_env = get_api_key(env_var)
        if from_env:
            st.caption(f"{label}: **{t['loaded_from_env']}**")
        else:
            st.session_state.ui_keys[env_var] = st.text_input(
                label,
                type="password",
                value=st.session_state.ui_keys.get(env_var, ""),
                help=t["enter_if_missing"],
            )

    key_input("OPENAI_API_KEY", t["openai_key"])
    key_input("GEMINI_API_KEY", t["gemini_key"])
    key_input("ANTHROPIC_API_KEY", t["anthropic_key"])
    key_input("GROK_API_KEY", t["grok_key"])

    st.markdown("---")
    with st.expander("🧪 Session Controls", expanded=False):
        if st.button(t["clear_history"], use_container_width=True):
            st.session_state.execution_log = []
            st.session_state.runs = 0
            st.session_state.last_run_ts = None
            st.session_state.chain_state = {"active": False, "agents": [], "idx": 0, "current_input": "", "last_output": "", "overrides": {}}
            st.toast("Cleared.", icon="🧹")


# =========================
# WOW Header + Status Chips
# =========================
resolved_openai, openai_from_env = get_api_key("OPENAI_API_KEY")
resolved_gemini, gemini_from_env = get_api_key("GEMINI_API_KEY")
resolved_anthropic, anthropic_from_env = get_api_key("ANTHROPIC_API_KEY")
resolved_grok, grok_from_env = get_api_key("GROK_API_KEY")

keys_status = {
    "openai": bool(resolved_openai),
    "gemini": bool(resolved_gemini),
    "anthropic": bool(resolved_anthropic),
    "grok": bool(resolved_grok),
}

provider_ok = sum(1 for k, v in keys_status.items() if v)
last_run_disp = st.session_state.last_run_ts or "—"

st.markdown(
    f"""
<div class="wow-hero">
  <div style="display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap;">
    <div>
      <div class="wow-title">{t['app_title']}</div>
      <div class="wow-subtitle">{t['subtitle']}</div>
      <div style="margin-top:0.55rem;">
        <span class="wow-chip"><span class="wow-dot"></span><b>{t['status']}</b></span>
        <span class="wow-chip"><span class="wow-dot2"></span>{st.session_state.theme_mode.upper()} · {st.session_state.painter_style.replace('_',' ').upper()}</span>
        <span class="wow-chip">🌐 {st.session_state.lang}</span>
        <span class="wow-chip">🔌 {t['provider_status']}: {provider_ok}/4</span>
        <span class="wow-chip">🕒 {t['last_run']}: {escape_html(str(last_run_disp))}</span>
      </div>
    </div>
    <div style="min-width:280px; max-width:420px;">
      <div class="wow-card">
        <div style="display:flex; gap:0.6rem; flex-wrap:wrap;">
          <span class="wow-chip">🔑 {t['keys_status']}: OpenAI={'✅' if keys_status['openai'] else '—'}</span>
          <span class="wow-chip">Gemini={'✅' if keys_status['gemini'] else '—'}</span>
          <span class="wow-chip">Anthropic={'✅' if keys_status['anthropic'] else '—'}</span>
          <span class="wow-chip">Grok={'✅' if keys_status['grok'] else '—'}</span>
        </div>
        <div style="margin-top:0.6rem; color:var(--wow-muted); font-size:0.9rem;">
          Tip: If a key exists in ENV, it stays hidden automatically.
        </div>
      </div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# =========================
# Tabs
# =========================
tab_workspace, tab_agents, tab_notes, tab_history, tab_settings = st.tabs(
    [f"🪐 {t['tabs_workspace']}", f"🤖 {t['tabs_agents']}", f"📝 {t['tabs_notes']}", f"🕰️ {t['tabs_history']}", f"⚙️ {t['tabs_settings']}"]
)


# =========================
# Workspace Tab
# =========================
with tab_workspace:
    st.markdown(f"### 📊 {t['dashboard']}")

    # Basic dashboard metrics
    agents_count = len((st.session_state.agents_config or {}).get("agents", []))
    docs_count = len(st.session_state.processed_docs)
    runs = st.session_state.runs

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Active Agents", agents_count)
    with m2:
        st.metric("Docs Loaded", docs_count)
    with m3:
        st.metric(t["runs_today"], runs)
    with m4:
        pulse = int(time.time()) % 1000
        st.metric("System Pulse", pulse)

    # Optional chart: elapsed time history
    if alt is not None and st.session_state.execution_log:
        rows = []
        for i, rec in enumerate(st.session_state.execution_log[-40:]):
            meta = rec.get("meta", {})
            rows.append({
                "run": i + 1,
                "agent": meta.get("agent", rec.get("agent", "agent")),
                "elapsed_s": float(meta.get("elapsed_s", 0.0) or 0.0),
            })
        if rows and pd is not None:
            df = pd.DataFrame(rows)
            c = alt.Chart(df).mark_bar().encode(
                x=alt.X("run:O", title="Recent steps"),
                y=alt.Y("elapsed_s:Q", title="Elapsed (s)"),
                color=alt.Color("agent:N", legend=None),
                tooltip=["agent", "elapsed_s"],
            ).properties(height=180)
            st.altair_chart(c, use_container_width=True)

    st.markdown("---")
    st.markdown(f"### 📂 {t['documents']}")

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        up_col1, up_col2 = st.columns([1, 1])
        with up_col1:
            uploaded_files = st.file_uploader(t["upload"], accept_multiple_files=True)
        with up_col2:
            if st.button("🧾 " + t["load_sample"], use_container_width=True):
                sample_csv = """SupplierID,Deliverdate,CustomerID,LicenseNo,Category,UDID,DeviceNAME,LotNO,SerNo,Model,Number
B00079,20251107,C05278,衛部醫器輸字第033951號,E.3610植入式心律器之脈搏產生器,00802526576331,“波士頓科技”英吉尼心臟節律器,890057,,L111,1
B00079,20251106,C06030,衛部醫器輸字第033951號,E.3610植入式心律器之脈搏產生器,00802526576331,“波士頓科技”英吉尼心臟節律器,872177,,L111,1
B00209,20251028,C03210,衛部醫器輸字第026988號,L.5980經陰道骨盆腔器官脫垂治療用手術網片,07798121803473,“博美敦”凱莉星脫垂修補系統,,00012184,Calistar S,1
"""
                st.session_state.processed_docs["sample_dataset.csv"] = sample_csv
                st.toast("Sample loaded: sample_dataset.csv", icon="📎")

        if uploaded_files:
            for f in uploaded_files:
                name, text = safe_read_uploaded(f)
                if name not in st.session_state.processed_docs:
                    st.session_state.processed_docs[name] = text

        if not st.session_state.processed_docs:
            st.info("Upload a document or load the sample dataset to begin.")
        else:
            # Keyword scan controls
            kw_col1, kw_col2 = st.columns([2, 1])
            with kw_col1:
                keywords_csv = st.text_input(t["keyword_list"], value="SupplierID,CustomerID,LicenseNo,Model,DeviceNAME")
            with kw_col2:
                kw_color = st.color_picker(t["keyword_color"], value="#FF8A5B")

            keywords = [k.strip() for k in keywords_csv.split(",") if k.strip()]

            # Document previews
            for doc_name, doc_text in list(st.session_state.processed_docs.items()):
                with st.expander(f"📄 {doc_name}", expanded=False):
                    st.text_area(t["doc_preview"], doc_text, height=220, key=f"preview_{doc_name}")

                    b1, b2 = st.columns([1, 2])
                    with b1:
                        if st.button(f"🔎 {t['scan_keywords']}", key=f"scan_{doc_name}"):
                            html = highlight_keywords_html(doc_text, keywords=keywords, color=kw_color)
                            st.session_state.processed_docs[f"{doc_name}__highlighted"] = html
                    with b2:
                        st.caption("Keyword scan produces HTML-highlighted view (does not change original text).")

                    if f"{doc_name}__highlighted" in st.session_state.processed_docs:
                        st.markdown(st.session_state.processed_docs[f"{doc_name}__highlighted"], unsafe_allow_html=True)

    with right:
        st.markdown(f"<div class='wow-card'><b>{t['context']}</b><br/>Pick a document as context for agents, or paste custom context in the Agents tab.</div>", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"<div class='wow-card'><b>WOW Tips</b><br/>• Use 🎰 Jackpot to explore painter styles.<br/>• Use step-by-step chain mode to edit each agent’s output before passing to the next.</div>", unsafe_allow_html=True)


# =========================
# Agents Tab
# =========================
with tab_agents:
    st.markdown(f"### 🤖 {t['agents_exec']}")

    # Resolve keys once
    openai_key, _ = get_api_key("OPENAI_API_KEY")
    gemini_key, _ = get_api_key("GEMINI_API_KEY")
    anthropic_key, _ = get_api_key("ANTHROPIC_API_KEY")
    grok_key, _ = get_api_key("GROK_API_KEY")

    resolved_keys = {
        "openai": openai_key,
        "gemini": gemini_key,
        "anthropic": anthropic_key,
        "grok": grok_key,
    }

    agents_cfg = st.session_state.agents_config or {"agents": []}
    all_agents = agents_cfg.get("agents", [])
    agent_names = [a.get("name", f"agent_{i+1}") for i, a in enumerate(all_agents)]

    topL, topR = st.columns([1.1, 0.9], gap="large")

    with topL:
        st.markdown(f"#### 🧠 {t['context']}")

        doc_options = list(st.session_state.processed_docs.keys())
        selected_doc = st.selectbox(t["select_context_doc"], ["None"] + doc_options, index=0)

        manual_context = st.text_area(t["or_manual_context"], height=180, placeholder="Paste context here...")

        context_text = ""
        if selected_doc != "None":
            context_text = st.session_state.processed_docs.get(selected_doc, "")
        if manual_context.strip():
            context_text = manual_context.strip()

        st.caption(f"{t['token_estimate']}: {estimate_tokens(context_text)}")

    with topR:
        st.markdown(f"#### 🔗 {t['chain_agents']}")
        selected_agents = st.multiselect(t["chain_agents"], agent_names, default=[])

        chain_controls_1, chain_controls_2 = st.columns(2)
        with chain_controls_1:
            if st.button("🧭 " + t["start_chain"], use_container_width=True, disabled=not bool(selected_agents)):
                st.session_state.chain_state = {
                    "active": True,
                    "agents": selected_agents,
                    "idx": 0,
                    "current_input": context_text,
                    "last_output": "",
                    "overrides": {},
                }
                st.toast("Chain started (step-by-step).", icon="🧭")
                st.rerun()

        with chain_controls_2:
            if st.button("⚡ " + t["run_all"], use_container_width=True, disabled=not bool(selected_agents)):
                # auto-run chain but still allow pre-run overrides via a quick editor below
                st.session_state.chain_state = {
                    "active": True,
                    "agents": selected_agents,
                    "idx": 0,
                    "current_input": context_text,
                    "last_output": "",
                    "overrides": st.session_state.chain_state.get("overrides", {}) if isinstance(st.session_state.chain_state, dict) else {},
                }
                st.session_state.chain_state["auto"] = True
                st.toast("Chain running (auto).", icon="⚡")
                st.rerun()

        if st.button("🔁 " + t["reset_chain"], use_container_width=True):
            st.session_state.chain_state = {"active": False, "agents": [], "idx": 0, "current_input": "", "last_output": "", "overrides": {}}
            st.toast("Chain reset.", icon="🔁")
            st.rerun()

        st.markdown("<div class='wow-card'>You can override each agent’s <b>model / max_tokens / temperature / prompt</b> before executing.</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Chain UI (step-by-step)
    cs = st.session_state.chain_state
    if cs.get("active") and cs.get("agents"):
        idx = int(cs.get("idx", 0))
        chain = cs["agents"]
        auto = bool(cs.get("auto", False))

        if idx >= len(chain):
            st.success(t["complete"])
            cs["active"] = False
            cs["auto"] = False
        else:
            agent_name = chain[idx]
            agent_conf = next((a for a in all_agents if a.get("name") == agent_name), None) or {}
            base_model = agent_conf.get("model", "gpt-4o-mini")
            base_provider = agent_conf.get("provider", infer_provider(base_model))
            base_prompt = agent_conf.get("prompt", "{input}")
            base_system = agent_conf.get("system_prompt", "You are a helpful assistant.")
            base_temp = float(agent_conf.get("temperature", 0.2))
            base_max = int(agent_conf.get("max_tokens", 12000))

            st.markdown(f"### 🧩 Step {idx+1}/{len(chain)} — **{agent_name}**")

            # Overrides storage
            if agent_name not in cs.get("overrides", {}):
                cs["overrides"][agent_name] = {}

            overrides = cs["overrides"][agent_name]

            # Agent config editor
            with st.expander("🛠️ " + t["agent_config"], expanded=True):
                cA, cB, cC = st.columns([1.2, 1, 1])
                with cA:
                    model = st.selectbox(
                        t["model"],
                        MODEL_CHOICES,
                        index=MODEL_CHOICES.index(overrides.get("model", base_model)) if overrides.get("model", base_model) in MODEL_CHOICES else 0,
                        key=f"model_{agent_name}_{idx}",
                    )
                with cB:
                    max_tokens = st.number_input(
                        t["max_tokens"],
                        min_value=256,
                        max_value=200000,
                        value=int(overrides.get("max_tokens", base_max or 12000)),
                        step=256,
                        key=f"max_{agent_name}_{idx}",
                    )
                with cC:
                    temperature = st.slider(
                        t["temperature"],
                        min_value=0.0,
                        max_value=1.5,
                        value=float(overrides.get("temperature", base_temp)),
                        step=0.05,
                        key=f"temp_{agent_name}_{idx}",
                    )

                provider = infer_provider(model)
                st.caption(f"Provider (auto): **{provider}**")

                system_prompt = st.text_area(
                    t["system_prompt"],
                    value=overrides.get("system_prompt", base_system),
                    height=120,
                    key=f"sys_{agent_name}_{idx}",
                )
                prompt_tpl = st.text_area(
                    t["prompt"],
                    value=overrides.get("prompt", base_prompt),
                    height=140,
                    key=f"prompt_{agent_name}_{idx}",
                )

                # Persist overrides
                overrides.update(
                    {
                        "provider": provider,
                        "model": model,
                        "max_tokens": int(max_tokens),
                        "temperature": float(temperature),
                        "system_prompt": system_prompt,
                        "prompt": prompt_tpl,
                    }
                )
                cs["overrides"][agent_name] = overrides
                st.session_state.chain_state = cs

            # Input editor (can edit before run)
            st.markdown("#### 🧾 " + t["input_to_agent"])
            cs["current_input"] = st.text_area(
                t["input_to_agent"],
                value=cs.get("current_input", ""),
                height=220,
                key=f"input_{agent_name}_{idx}",
            )
            st.caption(f"{t['token_estimate']}: {estimate_tokens(cs['current_input'])}")

            # Run button + status
            run_col1, run_col2 = st.columns([1, 1])
            with run_col1:
                do_run = st.button("▶️ " + t["run_agent"], key=f"run_{agent_name}_{idx}", use_container_width=True)
            with run_col2:
                view = st.radio(
                    t["output_view"],
                    [t["markdown"], t["text"]],
                    horizontal=True,
                    key=f"view_{agent_name}_{idx}",
                )

            if do_run or auto:
                with st.status(f"Running {agent_name}…", expanded=True) as status:
                    st.write(f"Model: **{overrides.get('model')}** | Provider: **{overrides.get('provider')}**")
                    st.write(f"max_tokens={overrides.get('max_tokens')} | temperature={overrides.get('temperature')}")
                    output, meta = run_agent(agent_conf, cs["current_input"], overrides, resolved_keys)

                    cs["last_output"] = output
                    st.session_state.chain_state = cs

                    # log
                    st.session_state.execution_log.append(
                        {
                            "ts": now_str(),
                            "agent": agent_name,
                            "input_tokens_est": estimate_tokens(cs["current_input"]),
                            "output_tokens_est": estimate_tokens(output),
                            "output": output,
                            "meta": meta,
                        }
                    )
                    st.session_state.runs += 1
                    st.session_state.last_run_ts = now_str()

                    if view == t["markdown"]:
                        st.markdown(output)
                    else:
                        st.text_area(t["output"], output, height=260)

                    status.update(label=f"{agent_name} Complete", state="complete")

                # Output editor for next step
                st.markdown("#### ✍️ " + t["edit_output_for_next"])
                edited = st.text_area(
                    t["edit_output_for_next"],
                    value=cs["last_output"],
                    height=240,
                    key=f"edited_{agent_name}_{idx}",
                )

                next_col1, next_col2 = st.columns([1, 1])
                with next_col1:
                    if st.button("➡️ " + t["use_as_next"], key=f"use_next_{agent_name}_{idx}", use_container_width=True):
                        cs["current_input"] = edited
                        cs["idx"] = idx + 1
                        cs["auto"] = False
                        st.session_state.chain_state = cs
                        st.rerun()

                with next_col2:
                    if idx + 1 < len(chain):
                        st.markdown(f"<div class='wow-card'><b>{t['next_agent']}:</b> {escape_html(chain[idx+1])}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='wow-card'><b>{t['next_agent']}:</b> —</div>", unsafe_allow_html=True)

                # Auto mode advance
                if auto:
                    cs["current_input"] = edited
                    cs["idx"] = idx + 1
                    st.session_state.chain_state = cs
                    st.rerun()
    else:
        st.info("Select agents and start a chain to run step-by-step (with editable outputs).")


# =========================
# AI Note Keeper Tab
# =========================
with tab_notes:
    st.markdown(f"### 📝 {t['tabs_notes']}")

    # Controls
    ncol1, ncol2, ncol3 = st.columns([1.2, 1, 1])
    with ncol1:
        note_model = st.selectbox("Model", MODEL_CHOICES, index=0, key="note_model")
    with ncol2:
        note_max = st.number_input(t["max_tokens"], min_value=256, max_value=200000, value=12000, step=256, key="note_max")
    with ncol3:
        note_temp = st.slider(t["temperature"], 0.0, 1.5, 0.2, 0.05, key="note_temp")

    provider = infer_provider(note_model)
    openai_key, _ = get_api_key("OPENAI_API_KEY")
    gemini_key, _ = get_api_key("GEMINI_API_KEY")
    anthropic_key, _ = get_api_key("ANTHROPIC_API_KEY")
    grok_key, _ = get_api_key("GROK_API_KEY")
    key_map = {"openai": openai_key, "gemini": gemini_key, "anthropic": anthropic_key, "grok": grok_key}
    note_key = key_map.get(provider)

    st.markdown("#### " + t["note_input"])
    st.session_state.note_text = st.text_area(
        t["note_input"],
        value=st.session_state.note_text,
        height=240,
        placeholder="Paste meeting notes / raw markdown / logs…",
        key="note_input_area",
    )

    view_mode = st.radio(t["note_view"], [t["markdown"], t["text"]], horizontal=True, key="note_view_mode")

    # 6 AI Magics
    st.markdown(f"#### ✨ {t['ai_magics']}")
    magic1, magic2, magic3, magic4, magic5, magic6 = st.columns(6)

    def note_ai(system_prompt: str, user_prompt: str) -> str:
        if not note_key:
            return f"(Missing API key for provider '{provider}'.)"
        out, _meta = call_llm(
            provider=provider,
            model=note_model,
            api_key=note_key,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=int(note_max),
            temperature=float(note_temp),
        )
        st.session_state.note_last_ai = out
        st.session_state.runs += 1
        st.session_state.last_run_ts = now_str()
        return out

    # Magic: AI Formatting (Organize)
    with magic1:
        if st.button("🧱", help=t["magic_format"], use_container_width=True):
            sys = "You are an expert note editor. Output clean, organized markdown."
            usr = (
                "Transform the following note into organized Markdown.\n"
                "Requirements:\n"
                "- Use clear headings\n"
                "- Add a concise summary at top\n"
                "- Use bullet points\n"
                "- Preserve important details; do not hallucinate\n"
                "- If the note contains tabular data, use Markdown tables\n\n"
                f"NOTE:\n{st.session_state.note_text}"
            )
            st.session_state.note_markdown = note_ai(sys, usr)

    # Magic: Summary
    with magic2:
        if st.button("🧠", help=t["magic_summary"], use_container_width=True):
            sys = "You summarize notes accurately."
            usr = f"Summarize this note in Markdown with sections: Key Points, Risks, Open Questions.\n\n{st.session_state.note_text}"
            st.session_state.note_markdown = note_ai(sys, usr)

    # Magic: Action Items
    with magic3:
        if st.button("✅", help=t["magic_actions"], use_container_width=True):
            sys = "You extract action items from notes."
            usr = (
                "Extract action items from this note.\n"
                "Output Markdown with a table: Action | Owner | Due | Status | Notes.\n"
                "If owner/due/status not present, leave blank.\n\n"
                f"{st.session_state.note_text}"
            )
            st.session_state.note_markdown = note_ai(sys, usr)

    # Magic: Flashcards
    with magic4:
        if st.button("🃏", help=t["magic_flashcards"], use_container_width=True):
            sys = "You turn notes into study flashcards."
            usr = (
                "Create 10-20 flashcards from this note.\n"
                "Output Markdown as:\n"
                "## Flashcards\n"
                "- **Q:** ...\n"
                "  **A:** ...\n\n"
                f"{st.session_state.note_text}"
            )
            st.session_state.note_markdown = note_ai(sys, usr)

    # Magic: Translate
    with magic5:
        if st.button("🌐", help=t["magic_translate"], use_container_width=True):
            sys = "You translate faithfully."
            usr = (
                "Translate the note between English and Traditional Chinese.\n"
                "If the note is mostly Chinese, translate to English; if mostly English, translate to Traditional Chinese.\n"
                "Preserve formatting as Markdown.\n\n"
                f"{st.session_state.note_text}"
            )
            st.session_state.note_markdown = note_ai(sys, usr)

    # Magic: Keywords highlight (non-AI, user-chosen keywords + color)
    with magic6:
        if st.button("🔦", help=t["magic_keywords"], use_container_width=True):
            pass  # UI below

    kw1, kw2 = st.columns([2, 1])
    with kw1:
        note_keywords = st.text_input("Keywords for highlight (comma-separated)", value="SupplierID,CustomerID,LicenseNo,Model", key="note_kw")
    with kw2:
        note_kw_color = st.color_picker("Color", value="#FEE440", key="note_kw_color")

    if st.button("Apply Keyword Highlight to Markdown (HTML preview)"):
        kws = [x.strip() for x in note_keywords.split(",") if x.strip()]
        html = highlight_keywords_html(st.session_state.note_markdown or st.session_state.note_text, kws, note_kw_color)
        st.markdown(html, unsafe_allow_html=True)

    # Show / Edit note markdown
    st.markdown("---")
    if view_mode == t["markdown"]:
        st.session_state.note_markdown = st.text_area(
            "Markdown",
            value=st.session_state.note_markdown or "",
            height=320,
            key="note_md_edit",
        )
        st.markdown(st.session_state.note_markdown or "")
    else:
        st.session_state.note_text = st.text_area(
            "Text",
            value=st.session_state.note_text or "",
            height=320,
            key="note_text_edit",
        )

    # Ask on note (keeps prompt on the note)
    st.markdown("---")
    st.markdown(f"#### 💬 {t['ask_on_note']}")
    user_q = st.text_input("Prompt", value="", key="note_ask_prompt")
    if st.button("💬 " + t["ask"], use_container_width=True):
        if not note_key:
            st.error(f"Missing API key for provider '{provider}'.")
        else:
            sys = "You are a helpful assistant. Use the note as the primary context."
            note_context = st.session_state.note_markdown or st.session_state.note_text
            usr = f"NOTE CONTEXT:\n{note_context}\n\nUSER REQUEST:\n{user_q}\n\nReturn in Markdown."
            ans = note_ai(sys, usr)
            st.markdown(ans)


# =========================
# History Tab
# =========================
with tab_history:
    st.markdown(f"### 🕰️ {t['history']}")
    if not st.session_state.execution_log:
        st.info("No runs yet.")
    else:
        for rec in reversed(st.session_state.execution_log[-200:]):
            meta = rec.get("meta", {}) or {}
            header = f"{rec.get('ts','')} — {rec.get('agent','')} ({meta.get('provider','')}/{meta.get('model','')})"
            with st.expander(header, expanded=False):
                st.caption(f"Elapsed: {meta.get('elapsed_s','?')}s | Input~{rec.get('input_tokens_est',0)} tok | Output~{rec.get('output_tokens_est',0)} tok")
                st.markdown(rec.get("output", ""))


# =========================
# Settings Tab (agents.yaml editor)
# =========================
with tab_settings:
    st.markdown(f"### ⚙️ {t['tabs_settings']}")
    st.markdown(f"<div class='wow-card'><b>{t['agents_yaml_editor']}</b><br/>Edit YAML, save, and your Agents list updates immediately.</div>", unsafe_allow_html=True)
    st.write("")

    with st.expander("🧾 agents.yaml", expanded=True):
        yaml_content = yaml.safe_dump(st.session_state.agents_config, sort_keys=False, allow_unicode=True)
        new_yaml = st.text_area("YAML", yaml_content, height=360)

        c1, c2 = st.columns([1, 3])
        with c1:
            if st.button("💾 " + t["save_config"], use_container_width=True):
                try:
                    parsed = yaml.safe_load(new_yaml) or {"agents": []}
                    # minimal validation
                    if "agents" not in parsed or not isinstance(parsed["agents"], list):
                        raise ValueError("YAML must have top-level key: agents: [ ... ]")
                    st.session_state.agents_config = parsed
                    save_agents_config(parsed)
                    st.success(t["saved"])
                except Exception as e:
                    st.error(f"{t['invalid_yaml']}: {e}")

        with c2:
            st.caption("Tip: Each agent can include: name, provider(optional), model, system_prompt, prompt, temperature, max_tokens.")
