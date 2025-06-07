import json
<<<<<<< HEAD
import os
from aqt import gui_hooks, mw
from aqt.utils import showInfo
from aqt.qt import QTimer, QUrl, Qt, QAction

from .config_ui import ConfigDialog  
from .config_manager import ConfigManager  
=======
from aqt import gui_hooks, mw
from aqt.utils import showInfo
from aqt.qt import QTimer, QUrl
>>>>>>> ec1e16eb8eff6cd6167c7dd21465990a5f258ab0

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
<<<<<<< HEAD
    "d": "difficulty",    
=======
    "d": "difficulty",
>>>>>>> ec1e16eb8eff6cd6167c7dd21465990a5f258ab0
    "r": "retrievability",
    "s": "stability"
}

<<<<<<< HEAD
def get_fsrs_property(card, key):
    """Fetch FSRS properties from card metadata."""
    data_json = mw.col.db.scalar("SELECT data FROM cards WHERE id = ?", card.id)
    
    if not data_json:
        return None  
=======

def get_fsrs_property(card, key):
    import json

    data_json = mw.col.db.scalar("SELECT data FROM cards WHERE id = ?", card.id)
    
    if not data_json:
        return None  # No FSRS data available
>>>>>>> ec1e16eb8eff6cd6167c7dd21465990a5f258ab0

    try:
        fsrs_data = json.loads(data_json)
    except json.JSONDecodeError:
<<<<<<< HEAD
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
=======
        return None  # Invalid JSON format

    # Step 3: Check if the requested FSRS key exists
    key_map = {"difficulty": "d", "retrievability": "dr", "stability": "s"}
    fsrs_key = key_map.get(key, key)  # Map standard key names

    if fsrs_key in fsrs_data:
        return fsrs_data[fsrs_key]

    if key == "difficulty" and "dr" in fsrs_data:
        return fsrs_data["dr"]

    return None  # Key not found


def load_config():
    config = mw.addonManager.getConfig(__name__)
    if not config:
        config = { "play_success_sound": True, "triggers": [], "default_origins": [{"x": 0.1, "y": 1.0}, {"x": 0.9, "y": 1.0}] }
        mw.addonManager.writeConfig(__name__, config)
    return config


def evaluate_numeric_condition(prop_value, condition_str):
>>>>>>> ec1e16eb8eff6cd6167c7dd21465990a5f258ab0
    operators = ["<=", ">=", "<", ">", "==", "!="]
    for op in operators:
        if condition_str.startswith(op):
            try:
                threshold = float(condition_str[len(op):].strip())
<<<<<<< HEAD
                return eval(f"{prop_value} {op} {threshold}")
=======
                value = float(prop_value)
                return eval(f"{value} {op} {threshold}")
>>>>>>> ec1e16eb8eff6cd6167c7dd21465990a5f258ab0
            except ValueError:
                return False
    return False

<<<<<<< HEAD
def evaluate_conditions(conditions, card, ease, revlog):
    """Evaluate multiple FSRS-based conditions."""
=======
    try:
        threshold = float(condition_str[2:].strip())
        value = float(prop_value)
        return eval(f"{value} {condition_str[:2]} {threshold}")
    except (ValueError, TypeError, IndexError):
        return False

def evaluate_conditions(conditions, card, ease, revlog):
>>>>>>> ec1e16eb8eff6cd6167c7dd21465990a5f258ab0
    for key, cond in conditions.items():
        effective_key = ALIAS_MAP.get(key[5:] if key.startswith("prop:") else key, key)
        card_val = get_fsrs_property(card, effective_key)
        if card_val is None or (isinstance(cond, str) and not evaluate_numeric_condition(card_val, cond)):
            return False
    return True

def choose_pattern(card, ease, revlog, config):
<<<<<<< HEAD
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
=======
    for trigger in config.get("triggers", []):
        if evaluate_conditions(trigger.get("conditions", {}), card, ease, revlog):
            return trigger.get("pattern")
    return None


def inject_confetti(reviewer, card, ease):
    if ease not in (3, 4) or get_fsrs_property(card, "difficulty") < 7.0:
        return

    config = load_config()
    try:
        webview = reviewer.web
    except AttributeError:
        return

    revlog = getattr(card, "revs", [])
    pattern = choose_pattern(card, ease, revlog, config)
    if not pattern:
        return

    origins_json = json.dumps(config.get("default_origins", [{"x": 0.1, "y": 1.0}, {"x": 0.9, "y": 1.0}]))

    js_code = f"""
    (function() {{
        console.log("Injecting confetti script...");
        function fireConfetti(origin) {{
            confetti({{
                particleCount: {pattern.get("particleCount", 100)},
                spread: {pattern.get("spread", 70)},
                origin: origin,
                startVelocity: {pattern.get("speed", 45)},
                ticks: {pattern.get("duration", 200)},
                decay: {pattern.get("fade", 0.9)}
            }});
        }}

        var origins = {origins_json};
        if (typeof confetti === 'undefined') {{
            let script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1';
            script.onload = function() {{
                console.log("Confetti script loaded successfully.");
                origins.forEach(fireConfetti);
            }};
            script.onerror = function() {{
                console.log("Confetti script failed to load.");
            }};
            document.head.appendChild(script);
        }} else {{
            console.log("Confetti script already available.");
            origins.forEach(fireConfetti);
        }}
    }})();
    """

    QTimer.singleShot(200, lambda: webview.page().runJavaScript(js_code))

    if ease not in (3, 4):
        return

    config = load_config()

    try:
        webview = reviewer.web
    except AttributeError:
        return

    revlog = getattr(card, "revs", [])
    pattern = choose_pattern(card, ease, revlog, config)
    if not pattern:
        return

    origins_json = json.dumps(config.get("default_origins", [{"x": 0.1, "y": 1.0}, {"x": 0.9, "y": 1.0}]))
>>>>>>> ec1e16eb8eff6cd6167c7dd21465990a5f258ab0

    js_code = f"""
    (function() {{
        function fireConfetti(origin) {{
            confetti({{
                particleCount: {pattern.get("particleCount", 100)},
                spread: {pattern.get("spread", 70)},
                origin: origin,
                startVelocity: {pattern.get("speed", 45)},
                ticks: {pattern.get("duration", 200)},
<<<<<<< HEAD
                decay: {pattern.get("decay", 0.9)},
                opacity: {opacity}  
=======
                decay: {pattern.get("fade", 0.9)}
>>>>>>> ec1e16eb8eff6cd6167c7dd21465990a5f258ab0
            }});
        }}

        var origins = {origins_json};
<<<<<<< HEAD
=======

        function loadConfetti(callback) {{
            if (typeof confetti === 'undefined') {{
                let script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1';
                script.onload = function() {{
                    setTimeout(() => origins.forEach(fireConfetti), 300);
                }};
                document.head.appendChild(script);
            }} else {{
                origins.forEach(fireConfetti);
            }}
        }}

        loadConfetti();
    }})();
    """

    QTimer.singleShot(200, lambda: webview.page().runJavaScript(js_code))

    if ease not in (3, 4):
        return
    config = load_config()
    try:
        webview = reviewer.web
    except AttributeError:
        return
    revlog = getattr(card, "revs", [])
    pattern = choose_pattern(card, ease, revlog, config)
    if not pattern:
        return
    origins_json = json.dumps(config.get("default_origins", [{"x": 0.1, "y": 1.0}, {"x": 0.9, "y": 1.0}]))
    js_code = f"""
    (function() {{
        function fireConfetti(origin) {{
            confetti({{
                particleCount: {pattern.get("particleCount", 100)},
                spread: {pattern.get("spread", 70)},
                origin: origin,
                startVelocity: {pattern.get("speed", 45)},
                ticks: {pattern.get("duration", 200)},
                decay: {pattern.get("fade", 0.9)}
            }});
        }}
        var origins = {origins_json};
>>>>>>> ec1e16eb8eff6cd6167c7dd21465990a5f258ab0
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
<<<<<<< HEAD

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


=======
    QTimer.singleShot(100, lambda: webview.page().runJavaScript(js_code))

def init_confetti_addon():
    gui_hooks.reviewer_did_answer_card.append(inject_confetti)

init_confetti_addon()
>>>>>>> ec1e16eb8eff6cd6167c7dd21465990a5f258ab0
