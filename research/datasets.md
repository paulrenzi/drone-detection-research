---
title: Training data and sound libraries
parent: Research Notes
nav_order: 5
---

# Training data and sound libraries
{: .no_toc }

1. TOC
{:toc}

## Public datasets found

| Dataset | Contents | Licence / access | Use |
|---|---|---|---|
| **DroneAudioset** | 23.5 h annotated recordings, wide SNR range (down to −57 dB) | MIT; Hugging Face `ahlab-drone-project/DroneAudioSet` | Drone-mounted mics; ego-noise research |
| **RWDA** (rotary-wing drone acoustic) | Drone sounds + natural environmental noise, open field | IEEE DataPort | Robust detection in noise |
| **Multiclass acoustic drone dataset** (2025) | 3,200 recordings from 32 UAV types, ~16,000 s | arXiv 2509.04715 | Multi-class identification |
| **Drone Sound Audio Detection** | Binary drone / unknown | Kaggle | Baseline classifier |
| **Sara Al-Emadi drone audio dataset** | Early drone audio corpus | Public | Baseline |
| **Western Sydney 24-mic localization** | Multi-mic recordings with GPS flight logs | Research release | Testing bearings and triangulation offline |

## The real gap

{: .warning }
> The original framing mentions an open-source drone sound library from **Ukraine and Norway**. We have **not** yet found it. Candidates to check: Squarehead (Norway) publications, Ukrainian volunteer projects (Zvook, Sky Fortress), NATO/DIANA challenges. **Add the link here once found.**

- Public datasets are mostly small hobby/commercial quadcopters.
- **Shahed/Geran, Lancet and fibre-optic FPV recordings** are what a military customer cares about, and they are scarce publicly. This is likely the true data bottleneck; partnering with a Ukrainian or Baltic program for recordings matters more than any model architecture.
- **Negative data** (mopeds, chainsaws, generators, tractors, aircraft, wind, rain) from the actual deployment region is just as important, to keep false alarms down.

## Sources

- [DroneAudioset — arXiv 2510.15383](https://arxiv.org/pdf/2510.15383)
- [RWDA — IEEE DataPort](https://ieee-dataport.org/documents/rotary-wing-drone-acoustic-dataset-rwda-dataset)
- [Multiclass acoustic dataset — arXiv 2509.04715](https://arxiv.org/pdf/2509.04715)
- [Kaggle — Drone Sound Audio Detection](https://www.kaggle.com/datasets/amineipad/drone-sound-audio-detection)
- [Sara Al-Emadi — Drone Audio Dataset](https://saraalemadi.com/2019/01/12/drone-audio-dataset/)
