import json
import os
from aqt import gui_hooks, mw
from aqt.utils import showInfo
from aqt.qt import QTimer, QUrl, Qt, QAction

from .config_ui import ConfigDialog  
from .config_manager import ConfigManager  

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
except ImportError:
    from PyQt6.QtWebEngineWidgets import QWebEngineView

try:
    from PyQt5.QtMultimedia import QSoundEffect
    SOUND_EFFECT_AVAILABLE = True
except ImportError:
    try:
        from PyQt6.QtMultimedia import QSoundEffect
        SOUND_EFFECT_AVAILABLE = True
    except ImportError:
        SOUND_EFFECT_AVAILABLE = False

ALIAS_MAP = {
    "d": "difficulty",    
    "r": "retrievability",
    "s": "stability"
}

def get_fsrs_property(card, key):
    """Fetch FSRS properties from card metadata."""
    data_json = mw.col.db.scalar("SELECT data FROM cards WHERE id = ?", card.id)
    
    if not data_json:
        return None  

    try:
        fsrs_data = json.loads(data_json)
    except json.JSONDecodeError:
        return None  

    key_map = {"difficulty": "d", "retrievability": "r", "stability": "s"}
    fsrs_key = key_map.get(key, key)  

    return fsrs_data.get(fsrs_key)

def load_confetti_effects():
    """Load confetti effect settings from JSON."""
    effects_path = os.path.join(mw.addonManager.addonsFolder(), "confetti", "config.json")
    try:
        with open(effects_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  

def evaluate_numeric_condition(prop_value, condition_str):
    """Evaluate numeric conditions (e.g., '< 0.40', '>= 3')."""
    operators = ["<=", ">=", "<", ">", "==", "!="]
    for op in operators:
        if condition_str.startswith(op):
            try:
                threshold = float(condition_str[len(op):].strip())
                return eval(f"{prop_value} {op} {threshold}")
            except ValueError:
                return False
    return False

def evaluate_conditions(conditions, card, ease, revlog):
    """Evaluate multiple FSRS-based conditions."""
    for key, cond in conditions.items():
        effective_key = ALIAS_MAP.get(key[5:] if key.startswith("prop:") else key, key)
        card_val = get_fsrs_property(card, effective_key)
        if card_val is None or (isinstance(cond, str) and not evaluate_numeric_condition(card_val, cond)):
            return False
    return True

def choose_pattern(card, ease, revlog, config):
    """Choose the appropriate confetti pattern based on FSRS conditions."""
    effects = load_confetti_effects()
    pattern = effects.get("default", {})

    if get_fsrs_property(card, "difficulty") > 9:
        pattern = effects.get("high_difficulty", pattern)
    elif get_fsrs_property(card, "retrievability") < 0.3:
        pattern = effects.get("low_retrievability", pattern)

    return pattern

def inject_confetti(reviewer, card, ease):
    """Trigger confetti animation based on FSRS difficulty and retrievability."""
    if ease not in (3, 4) or get_fsrs_property(card, "difficulty") < 7.0:
        return

    config = ConfigManager("confetti").config  
    global_opacity = config.get("global_opacity", 0.8)  

    revlog = getattr(card, "revs", [])
    
    pattern = None
    for trigger in config.get("triggers", []):
        conditions = trigger.get("conditions", {})
        if all(get_fsrs_property(card, key) == value for key, value in conditions.items()):
            pattern = trigger.get("pattern")
            break

    if not pattern:
        return  

    origins_json = json.dumps(config.get("default_origins", [{"x": 0.1, "y": 1.0}, {"x": 0.9, "y": 1.0}]))

    opacity = pattern.get("opacity", global_opacity)  

    js_code = f"""
    (function() {{
        function fireConfetti(origin) {{
            confetti({{
                particleCount: {pattern.get("particleCount", 100)},
                spread: {pattern.get("spread", 70)},
                origin: origin,
                startVelocity: {pattern.get("speed", 45)},
                ticks: {pattern.get("duration", 200)},
                decay: {pattern.get("decay", 0.9)},
                opacity: {opacity}  
            }});
        }}

        var origins = {origins_json};
        if (typeof confetti === 'undefined') {{
            let script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1';
            script.onload = function() {{
                origins.forEach(fireConfetti);
            }};
            document.head.appendChild(script);
        }} else {{
            origins.forEach(fireConfetti);
        }}
    }})();
    """

    QTimer.singleShot(200, lambda: reviewer.web.page().runJavaScript(js_code))


config_dialog_instance = None  

def open_config():
    """Open the configuration UI."""
    global config_dialog_instance
    try:
        if config_dialog_instance is None or not config_dialog_instance.isVisible():
            config_dialog_instance = ConfigDialog(mw)  
            config_dialog_instance.setWindowFlags(Qt.Window)  
            config_dialog_instance.setWindowModality(Qt.ApplicationModal)  
            config_dialog_instance.show()
            config_dialog_instance.raise_()
            config_dialog_instance.activateWindow()
    except Exception as e:
        showInfo(f"Error opening config: {str(e)}")


mw.addonManager.setConfigAction(__name__, open_config)

def init_confetti_addon():
    """Initialize the confetti add-on by hooking into Anki's review system."""
    gui_hooks.reviewer_did_answer_card.append(inject_confetti)

init_confetti_addon()


