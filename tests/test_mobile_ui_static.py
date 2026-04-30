import re
from pathlib import Path

HTML = Path('NightGuardRoom/Resources/index.html').read_text(encoding='utf-8')


def test_viewport_and_safe_area_are_enabled():
    assert 'viewport-fit=cover' in HTML
    for token in ['safe-area-inset-top', 'safe-area-inset-bottom', 'safe-area-inset-left', 'safe-area-inset-right']:
        assert token in HTML
    assert '--hud-top' in HTML
    assert '--controls-bottom' in HTML


def test_bottom_controls_are_fixed_three_by_three_grid():
    assert '#bottomBar' in HTML
    assert 'command-grid' in HTML
    assert 'grid-template-columns:repeat(3,1fr)' in HTML
    assert 'grid-template-rows:repeat(3,minmax' in HTML
    for label in ['升级床位', '加固房门', '维修房门', '建造防御', '升级设施', '暂停', '提示', '重开', '目标']:
        assert label in HTML
    assert 'buildDefense' in HTML


def test_top_status_bar_has_four_blocks_and_original_labels():
    assert '#topBar{ top:var(--hud-top); left:4%; right:4%;' in HTML
    assert 'grid-template-columns:repeat(4,1fr)' in HTML
    for label in ['时间', '铜钱', '木料', '门']:
        assert label in HTML


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
    for symbol in ['upgradeBed()', 'upgradeDoor()', 'repair()', 'build(type)', 'buildDefense()', 'upgradeTower()', 'spawnPack()', 'drawMap()', 'drawMonster(m)']:
        assert symbol in HTML


def test_room_corridor_visual_markers_present():
    for token in ['#172039', '#1B2745', '#1E1C2D', '#2A263D', '#A66A2D', '#C2873C', '#64F090', '#FF4D5D']:
        assert token in HTML
    assert 'doorShake' in HTML
    assert 'bedGlow' in HTML


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
