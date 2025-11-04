# Music Source Separation Universal Training Code

Repository for training models for music source separation. Repository is based on [kuielab code](https://github.com/kuielab/sdx23/tree/mdx_AB/my_submission/src) for [SDX23 challenge](https://github.com/kuielab/sdx23/tree/mdx_AB/my_submission/src). The main idea of this repository is to create training code, which is easy to modify for experiments. Original script created by ZFTurbo of [MVSep.com](https://mvsep.com). This fork has been modified with an inference script that supports the `--lossless` command, using an implementation developed by [axeldelafosse](https://github.com/axeldelafosse/BS-RoFormer) and modified by me.

## Platform Compatibility

This code works on **Windows, macOS (Mac), and Linux**. The core training and inference functionality is cross-platform compatible.

**📖 For macOS users:** See the detailed [macOS Installation Guide](docs/macos.md) for Mac-specific instructions and troubleshooting.

### Installation

**Basic installation (all platforms):**
```bash
pip install -r requirements.txt
```

**Optional features (GUI and real-time streaming):**
```bash
pip install -r requirements-optional.txt
```

**Note for macOS users:** If you encounter issues installing optional dependencies (pyaudio, keyboard, wxpython), you can skip them if you don't need:
- Real-time audio streaming (`scripts/stream.py`) - requires pyaudio and keyboard
- GUI interface (`gui/gui-wx.py`) - requires wxpython

The main training and inference scripts work without these optional dependencies.

## Lossless mode

The `--lossless` flag (default disabled) enables perfect reconstruction of the original mix by intelligently distributing any residual content back into the stems. This ensures that when all stems are summed together, they exactly match the input mix.

By default, music source separation can be slightly lossy -- the sum of the separated stems may not perfectly equal the original mix due to model limitations. The lossless mode addresses this by:

1. Calculating the residual (difference between original mix and sum of stems)
2. Running the model again on this residual to classify its content
3. Using a hybrid approach to distribute the residual:
   - Clear drum/percussion content goes to the drums stem
   - Clear musical/harmonic content goes to the other stem
   - Ambiguous content is distributed proportionally based on the energy ratio

This results in:

- Perfect reconstruction when stems are summed
- Musically appropriate distribution of residual content
- Minimal impact on separation quality of primary elements

## Advanced Lossless mode

The `--lossless_advanced` flag does the same thing as the standard `--lossless` flag but differs in step 3. Clear drum/percussion content still goes into the drums stem, but different parts of the residual (harmonic content and ambiguous content) are given their new stems: `residual_other` and `residual_ambiguous`. The means that the `other` stem is untouched from the original model output. This means the user gets to decide what to do with the residual content.

This results in:

- Perfect reconstruction when stems are summed (including both residual stems)
- An untouched `other` stem
  - Useful if the user needs the content in the original stem
- User's choice for the residual content
  - Useful if (for example) most of the harmonic residual is a guitar or piano, and the ambiguous content is just distortion
- Minimal impact on separation quality of primary elements


### Usage

To use lossless mode, simply add the `--lossless` flag to your command:

```bash
python inference.py \
    --model_type bs_roformer \
    --config_path configs/bs_roformer.yaml \
    --start_check_point results/bs_roformer.ckpt \
    --input_folder input/ \
    --store_dir separation_results/ \
    --lossless
```

Note that this will run the model twice, so it will be 2x slower than the default mode.

## Models

Model can be chosen with `--model_type` arg.

Available models for training:

* MDX23C based on [KUIELab TFC TDF v3 architecture](https://github.com/kuielab/sdx23/). Key: `mdx23c`.
* Demucs4HT [[Paper](https://arxiv.org/abs/2211.08553)]. Key: `htdemucs`.
* VitLarge23 based on [Segmentation Models Pytorch](https://github.com/qubvel/segmentation_models.pytorch). Key: `segm_models`.
* TorchSeg based on [TorchSeg module](https://github.com/qubvel/segmentation_models.pytorch). Key: `torchseg`.
* Band Split RoFormer [[Paper](https://arxiv.org/abs/2309.02612), [Repository](https://github.com/lucidrains/BS-RoFormer)] . Key: `bs_roformer`.
* Mel-Band RoFormer [[Paper](https://arxiv.org/abs/2310.01809), [Repository](https://github.com/lucidrains/BS-RoFormer)]. Key: `mel_band_roformer`.
* Swin Upernet [[Paper](https://arxiv.org/abs/2103.14030)] Key: `swin_upernet`.
* BandIt Plus [[Paper](https://arxiv.org/abs/2309.02539), [Repository](https://github.com/karnwatcharasupat/bandit)] Key: `bandit`.
* SCNet [[Paper](https://arxiv.org/abs/2401.13276), [Official Repository](https://github.com/starrytong/SCNet), [Unofficial Repository](https://github.com/amanteur/SCNet-PyTorch)] Key: `scnet`.
* BandIt v2 [[Paper](https://arxiv.org/abs/2407.07275), [Repository](https://github.com/kwatcharasupat/bandit-v2)] Key: `bandit_v2`.
* Apollo [[Paper](https://arxiv.org/html/2409.08514v1), [Repository](https://github.com/JusperLee/Apollo)] Key: `apollo`.
* TS BSMamba2 [[Paper](https://arxiv.org/pdf/2409.06245), [Repository](https://github.com/baijinglin/TS-BSmamba2)] Key: `bs_mamba2`.
* Conformer [[Paper](https://arxiv.org/abs/2005.08100), [Repository](https://github.com/dillfrescott/mvsep-beta)] Key: `conformer`.
* SCNet Tran Key: `scnet_tran`.
* SCNet Masked Key: `scnet_masked`.

1. **Note 1**: For `segm_models` there are many different encoders is possible. [Look here](https://github.com/qubvel/segmentation_models.pytorch#encoders-).
2. **Note 2**: Thanks to [@lucidrains](https://github.com/lucidrains) for recreating the RoFormer models based on papers.
3. **Note 3**: For `torchseg` gives access to more than 800 encoders from `timm` module. It's similar to `segm_models`.

## How to: Train

To train model you need to:

1) Choose model type with option `--model_type`, including: `mdx23c`, `htdemucs`, `segm_models`, `mel_band_roformer`, `bs_roformer`.
2) Choose location of config for model `--config_path` `<config path>`. You can find examples of configs in [configs folder](configs/). Prefixes `config_musdb18_` are examples for [MUSDB18 dataset](https://sigsep.github.io/datasets/musdb.html).
3) If you have a check-point from the same model or from another similar model you can use it with option: `--start_check_point` `<weights path>`
4) Choose path where to store results of training `--results_path` `<results folder path>`

### Training example

```bash
python train.py \
    --model_type mel_band_roformer \
    --config_path configs/config_mel_band_roformer_vocals.yaml \
    --start_check_point results/model.ckpt \
    --results_path results/ \
    --data_path 'datasets/dataset1' 'datasets/dataset2' \
    --valid_path datasets/musdb18hq/test \
    --num_workers 4 \
    --device_ids 0
```

All training parameters are [here](https://github.com/ZFTurbo/Music-Source-Separation-Training/blob/main/utils/settings.py#L20).

### Training with LoRA

Look here: [LoRA training](docs/LoRA.md)

## How to: Inference

### Inference example

```bash
python inference.py \
    --model_type mdx23c \
    --config_path configs/config_mdx23c_musdb18.yaml \
    --start_check_point results/last_mdx23c.ckpt \
    --input_folder input/wavs/ \
    --store_dir separation_results/
```

All inference parameters are [here](https://github.com/ZFTurbo/Music-Source-Separation-Training/blob/main/utils/settings.py#L130).

## Useful notes

* All batch sizes in config are adjusted to use with single NVIDIA A6000 48GB. If you have less memory please adjust correspodningly in model config `training.batch_size` and `training.gradient_accumulation_steps`.
* It's usually always better to start with old weights even if shapes not fully match. Code supports loading weights for not fully same models (but it must have the same architecture). Training will be much faster.

## Code description

* `configs/config_*.yaml` - configuration files for models
* `models/*` - set of available models for training and inference
* `dataset.py` - dataset which creates new samples for training
* `gui-wx.py` - GUI interface for code
* `inference.py` - process folder with music files and separate them
* `train.py` - main training code
* `train_accelerate.py` - experimental training code to use with `accelerate` module. Speed up for MultiGPU.
* `utils.py` - common functions used by train/valid
* `valid.py` - validation of model with metrics
* `ensemble.py` - useful script to ensemble results of different models to make results better (see [docs](docs/ensemble.md)).   

## Pre-trained models

Look here: [List of Pre-trained models](docs/pretrained_models.md)

If you trained some good models, please, share them. You can post config and model weights [in this issue](https://github.com/ZFTurbo/Music-Source-Separation-Training/issues/1).

## Dataset types

Look here: [Dataset types](docs/dataset_types.md)

## Augmentations

Look here: [Augmentations](docs/augmentations.md)

## Graphical user interface

Look here: [GUI documentation](docs/gui.md) or see tutorial on [Youtube](https://youtu.be/M8JKFeN7HfU)

## Citation

* [arxiv paper](https://arxiv.org/abs/2305.07489)

```text
@misc{solovyev2023benchmarks,
      title={Benchmarks and leaderboards for sound demixing tasks}, 
      author={Roman Solovyev and Alexander Stempkovskiy and Tatiana Habruseva},
      year={2023},
      eprint={2305.07489},
      archivePrefix={arXiv},
      primaryClass={cs.SD}
}
```
