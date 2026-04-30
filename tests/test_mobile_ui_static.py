import re
from pathlib import Path

HTML = Path('NightGuardRoom/Resources/index.html').read_text(encoding='utf-8')

def test_viewport_and_safe_area_are_enabled():
    assert 'viewport-fit=cover' in HTML
    for token in ['safe-area-inset-top', 'safe-area-inset-bottom', 'safe-area-inset-left', 'safe-area-inset-right']:
        assert token in HTML
    assert '--hud-top' in HTML
    assert '--controls-bottom' in HTML


def test_bottom_controls_are_contextual_not_nine_button_grid():
    assert '#bottomBar' in HTML
    assert 'grid-template-columns:repeat(3,1fr)' not in HTML
    assert 'command-primary' in HTML
    assert 'command-secondary' in HTML
    assert 'drawer' in HTML
    assert 'moreBuild' in HTML


def test_disabled_actions_show_shortage_reason():
    assert 'function shortage' in HTML
    assert '缺' in HTML
    assert 'aria-disabled' in HTML
    assert 'disabledReason' in HTML


def test_restart_requires_confirmation():
    assert 'confirmRestart' in HTML
    assert '确认重开' in HTML
    assert "game.confirmRestart" in HTML


def test_no_in_game_floating_arrow_or_scroll_button():
    forbidden = ['scrollTop', 'backToTop', 'floatArrow', 'floating-arrow', 'right-arrow']
    for word in forbidden:
        assert word not in HTML


def test_core_gameplay_still_present():
    for symbol in ['upgradeBed()', 'upgradeDoor()', 'repair()', 'build(type)', 'upgradeTower()', 'spawnPack()', 'drawMap()', 'drawMonster(m)']:
        assert symbol in HTML


def test_html_has_single_script_and_canvas():
    assert HTML.count('<canvas id="game"') == 1
    assert HTML.count('<script>') == 1
    assert HTML.count('</script>') == 1
    assert HTML.count('<div id="bottomBar"') == 1

def test_overlay_does_not_block_in_game_bottom_controls():
    assert '#ui{ position:absolute; inset:0;' in HTML
    assert '#bottomBar{ bottom:var(--controls-bottom);' in HTML
    assert 'pointer-events:auto' in re.search(r'#bottomBar\{[^}]+\}', HTML).group(0)
    overlay_css = re.search(r'#overlay\{[^}]+\}', HTML).group(0)
    card_css = re.search(r'\.card\{[^}]+\}', HTML).group(0)
    assert 'pointer-events:none' in overlay_css
    assert 'pointer-events:auto' in card_css


def test_inline_javascript_parses_with_node():
    import subprocess, tempfile
    script = re.search(r'<script>(.*)</script>', HTML, re.S).group(1)
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f:
        f.write(script)
        name = f.name
    try:
        subprocess.run(['node', '--check', name], check=True, capture_output=True, text=True)
    finally:
        Path(name).unlink(missing_ok=True)

