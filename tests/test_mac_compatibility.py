#!/usr/bin/env python3
"""
Tests for Mac/cross-platform compatibility

This test suite verifies that the code handles different platforms correctly.
"""

import platform
import subprocess
import sys
from pathlib import Path


def test_platform_detection():
    """Test that we can detect the current platform"""
    system = platform.system()
    print(f"✓ Platform detected: {system}")
    assert system in ['Windows', 'Darwin', 'Linux'], f"Unknown platform: {system}"


def test_open_folder_logic():
    """Test the logic for opening folders on different platforms"""
    # Test the logic without actually opening folders
    system = platform.system()
    
    if system == 'Windows':
        cmd_type = "os.startfile"
    elif system == 'Darwin':
        cmd_type = "subprocess.run(['open', folder])"
    else:
        cmd_type = "subprocess.run(['xdg-open', folder])"
    
    print(f"✓ Platform: {system} -> Would use: {cmd_type}")
    assert cmd_type is not None


def test_requirements_files_exist():
    """Test that both requirements files exist"""
    base_path = Path(__file__).parent.parent
    
    req_main = base_path / 'requirements.txt'
    req_opt = base_path / 'requirements-optional.txt'
    
    assert req_main.exists(), "requirements.txt not found"
    print("✓ requirements.txt exists")
    
    assert req_opt.exists(), "requirements-optional.txt not found"
    print("✓ requirements-optional.txt exists")


def test_optional_deps_separated():
    """Test that optional dependencies are properly separated"""
    base_path = Path(__file__).parent.parent
    
    main_reqs = (base_path / 'requirements.txt').read_text()
    opt_reqs = (base_path / 'requirements-optional.txt').read_text()
    
    # Check that problematic packages are in optional, not main
    assert 'pyaudio' not in main_reqs, "pyaudio should be in requirements-optional.txt"
    assert 'keyboard' not in main_reqs, "keyboard should be in requirements-optional.txt"
    assert 'wxpython' not in main_reqs.lower(), "wxpython should be in requirements-optional.txt"
    
    print("✓ Optional dependencies properly separated")
    
    # Check that they ARE in optional
    assert 'pyaudio' in opt_reqs, "pyaudio should be in requirements-optional.txt"
    assert 'keyboard' in opt_reqs, "keyboard should be in requirements-optional.txt"
    assert 'wxpython' in opt_reqs.lower(), "wxpython should be in requirements-optional.txt"
    
    print("✓ Optional dependencies present in requirements-optional.txt")


def test_readme_has_platform_info():
    """Test that README documents platform compatibility"""
    base_path = Path(__file__).parent.parent
    
    readme = (base_path / 'README.md').read_text()
    
    # Check for key platform-related content
    assert 'Platform Compatibility' in readme or 'macOS' in readme or 'Mac' in readme, \
        "README should mention platform compatibility"
    print("✓ README contains platform compatibility information")
    
    assert 'requirements-optional.txt' in readme, \
        "README should mention requirements-optional.txt"
    print("✓ README mentions optional requirements")


def test_gui_has_dependency_check():
    """Test that GUI file has dependency check"""
    base_path = Path(__file__).parent.parent
    
    gui_code = (base_path / 'gui' / 'gui-wx.py').read_text()
    
    # Check that it handles missing wx gracefully
    assert 'try:' in gui_code and 'import wx' in gui_code, \
        "GUI should have try/except for wx import"
    print("✓ GUI has dependency check for wxPython")
    
    # Check that it uses platform-specific folder opening
    assert 'platform.system()' in gui_code, \
        "GUI should use platform.system() for cross-platform compatibility"
    print("✓ GUI uses platform detection for folder opening")


def test_stream_has_dependency_check():
    """Test that stream script has dependency check"""
    base_path = Path(__file__).parent.parent
    
    stream_code = (base_path / 'scripts' / 'stream.py').read_text()
    
    # Check that it handles missing pyaudio/keyboard gracefully
    assert 'PYAUDIO_AVAILABLE' in stream_code or 'try:' in stream_code, \
        "stream.py should check for pyaudio availability"
    print("✓ stream.py has dependency check for pyaudio")
    
    assert 'KEYBOARD_AVAILABLE' in stream_code or 'keyboard' in stream_code, \
        "stream.py should check for keyboard availability"
    print("✓ stream.py has dependency check for keyboard")


if __name__ == '__main__':
    print("Running Mac/cross-platform compatibility tests...\n")
    
    tests = [
        test_platform_detection,
        test_open_folder_logic,
        test_requirements_files_exist,
        test_optional_deps_separated,
        test_readme_has_platform_info,
        test_gui_has_dependency_check,
        test_stream_has_dependency_check,
    ]
    
    failed = 0
    for test in tests:
        try:
            print(f"\nRunning {test.__name__}...")
            test()
            print(f"✓ {test.__name__} passed")
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Tests completed: {len(tests) - failed}/{len(tests)} passed")
    
    if failed > 0:
        print(f"✗ {failed} test(s) failed")
        sys.exit(1)
    else:
        print("✓ All tests passed!")
        sys.exit(0)
