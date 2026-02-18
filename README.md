# artifacts

Weekly operating system artifact releases generated from fresh cloud images and published as BLAKE3 hash datasets for threat detection, integrity monitoring, and bloom filter generation.

This repository contains curated artifact datasets collected from clean, automatically built operating system images using the **Amazon EC2 Image Builder** pipeline:

- Amazon Linux 2023
- Ubuntu Server 24.04
- Windows Server 2025

Each image is scanned using ```getmeta``` to extract system file metadata. The resulting artifacts are normalized, hashed with BLAKE3, and published as Apache Parquet datasets for downstream analysis and bloom filter generation.
