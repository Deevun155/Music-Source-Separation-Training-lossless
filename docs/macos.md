# macOS (Mac) Installation Guide

This guide provides macOS-specific installation instructions for the Music Source Separation Training code.

## Platform Support

✅ **This code works on macOS (Mac)!**

The core training and inference functionality is fully cross-platform and works on:
- macOS (Apple Silicon M1/M2/M3 and Intel)
- Windows
- Linux

## Quick Start

### Basic Installation (Core Features)

Install the core dependencies needed for training and inference:

```bash
pip install -r requirements.txt
```

This includes everything you need for:
- Training models
- Running inference/separation
- Using all model types
- Using lossless mode

### Optional Features Installation

If you want to use the GUI or real-time streaming, install optional dependencies:

```bash
pip install -r requirements-optional.txt
```

**Note:** These packages may have installation issues on macOS. See troubleshooting below.

## Troubleshooting macOS Installation Issues

### PyAudio Installation Issues

PyAudio is only needed for real-time streaming (`scripts/stream.py`). If you don't need this feature, you can skip it.

If you want to install PyAudio on macOS:

1. First install PortAudio via Homebrew:
   ```bash
   brew install portaudio
   ```

2. Then install PyAudio:
   ```bash
   pip install pyaudio
   ```

### wxPython Installation Issues

wxPython is only needed for the GUI (`gui/gui-wx.py`). If you prefer using the command line, you can skip it.

If you want to install wxPython on macOS:

```bash
pip install -U wxPython
```

If this fails, try installing from a wheel file:
```bash
pip install -U wxPython --find-links https://extras.wxpython.org/wxPython4/extras/
```

### keyboard Package Issues

The `keyboard` package is only needed for real-time streaming. On macOS, it may require sudo permissions or may not work as expected. If you don't need streaming, you can skip it.

## Using the Code on Mac

### Command Line Interface (Recommended)

The command-line interface works perfectly on macOS:

**Inference:**
```bash
python inference.py \
    --model_type bs_roformer \
    --config_path configs/bs_roformer.yaml \
    --start_check_point results/bs_roformer.ckpt \
    --input_folder input/ \
    --store_dir separation_results/ \
    --lossless
```

**Training:**
```bash
python train.py \
    --model_type mel_band_roformer \
    --config_path configs/config_mel_band_roformer_vocals.yaml \
    --results_path results/ \
    --data_path datasets/my_dataset \
    --num_workers 4
```

### Opening Output Folders

The code automatically opens the output folder after processing:
- On macOS: Uses `open` command
- On Windows: Uses `os.startfile()`
- On Linux: Uses `xdg-open`

## Apple Silicon (M1/M2/M3) Specific Notes

### GPU Acceleration

PyTorch supports Apple Silicon GPU acceleration via MPS (Metal Performance Shaders):

```python
# The code will automatically use MPS if available
device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
```

### Memory Management

Apple Silicon Macs with unified memory work great for this code. The memory is shared between CPU and GPU, so you can train larger models than you might expect.

## Verifying Your Installation

Run the Mac compatibility tests to verify everything is set up correctly:

```bash
python tests/test_mac_compatibility.py
```

This will check:
- Platform detection
- Requirements file structure
- Dependency handling
- Cross-platform compatibility

## Getting Help

If you encounter issues specific to macOS:

1. Check that you have Python 3.8 or later: `python3 --version`
2. Make sure pip is up to date: `pip install --upgrade pip`
3. Try using a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. For Apple Silicon (M1/M2/M3), ensure you're using an arm64 version of Python, not x86_64 via Rosetta

## Summary

**What works on Mac:**
✅ Training models
✅ Running inference/separation
✅ Lossless mode
✅ All model architectures
✅ Command-line interface
✅ Ensemble mode

**What's optional on Mac:**
⚠️ GUI (wxPython) - may have installation issues
⚠️ Real-time streaming (PyAudio/keyboard) - may have installation issues

**Bottom line:** The core functionality works perfectly on macOS. Optional features (GUI and streaming) may require extra setup steps but are not needed for most use cases.
