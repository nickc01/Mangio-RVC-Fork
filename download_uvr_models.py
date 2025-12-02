#!/usr/bin/env python3
"""
Download required models from Hugging Face
Usage: python download_uvr_models.py
"""

import os
import sys
import requests
from tqdm import tqdm

# Hugging Face repository
HF_REPO = "lj1995/VoiceConversionWebUI"
HF_BASE_URL = f"https://huggingface.co/{HF_REPO}/resolve/main"

# Essential models (required for RVC to work)
ESSENTIAL_MODELS = [
    "hubert_base.pt",
    "rmvpe.pt",
]

# UVR5 models to download
UVR5_MODELS = [
    "uvr5_weights/HP2-人声vocals+非人声instrumentals.pth",
    "uvr5_weights/HP2_all_vocals.pth",
    "uvr5_weights/HP3_all_vocals.pth",
    "uvr5_weights/HP5-主旋律人声vocals+其他instrumentals.pth",
    "uvr5_weights/HP5_only_main_vocal.pth",
    "uvr5_weights/VR-DeEchoAggressive.pth",
    "uvr5_weights/VR-DeEchoDeReverb.pth",
    "uvr5_weights/VR-DeEchoNormal.pth",
]

# Optional ONNX model (larger file)
ONNX_MODEL = "uvr5_weights/onnx_dereverb_By_FoxJoy"

def download_file(url, destination):
    """Download a file with progress bar"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        os.makedirs(os.path.dirname(destination), exist_ok=True)

        with open(destination, 'wb') as f, tqdm(
            desc=os.path.basename(destination),
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))

        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    print("=" * 60)
    print("Model Downloader for Mangio-RVC-Fork")
    print("=" * 60)
    print()

    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    uvr5_dir = os.path.join(script_dir, "uvr5_weights")

    print(f"Download destination: {script_dir}")
    print()

    # Create uvr5_weights directory if it doesn't exist
    os.makedirs(uvr5_dir, exist_ok=True)

    successful = 0
    failed = 0

    # Download essential models first
    print("=" * 60)
    print("Downloading Essential Models")
    print("=" * 60)
    print(f"Downloading {len(ESSENTIAL_MODELS)} essential models...")
    print()

    for model_path in ESSENTIAL_MODELS:
        model_name = os.path.basename(model_path)
        destination = os.path.join(script_dir, model_path)

        # Check if file already exists
        if os.path.exists(destination):
            file_size = os.path.getsize(destination)
            if file_size > 1000:  # If file is larger than 1KB, assume it's valid
                print(f"✓ {model_name} already exists ({file_size:,} bytes), skipping...")
                successful += 1
                continue

        print(f"Downloading {model_name}...")
        url = f"{HF_BASE_URL}/{model_path}"

        if download_file(url, destination):
            print(f"✓ Downloaded {model_name}")
            successful += 1
        else:
            print(f"✗ Failed to download {model_name}")
            failed += 1
        print()

    # Download UVR5 models
    print()
    print("=" * 60)
    print("Downloading UVR5 Models")
    print("=" * 60)
    print(f"Downloading {len(UVR5_MODELS)} UVR5 models...")
    print()

    for model_path in UVR5_MODELS:
        model_name = os.path.basename(model_path)
        destination = os.path.join(script_dir, model_path)

        # Check if file already exists
        if os.path.exists(destination):
            file_size = os.path.getsize(destination)
            if file_size > 1000:  # If file is larger than 1KB, assume it's valid
                print(f"✓ {model_name} already exists ({file_size:,} bytes), skipping...")
                successful += 1
                continue

        print(f"Downloading {model_name}...")
        url = f"{HF_BASE_URL}/{model_path}"

        if download_file(url, destination):
            print(f"✓ Downloaded {model_name}")
            successful += 1
        else:
            print(f"✗ Failed to download {model_name}")
            failed += 1
        print()

    # Ask about ONNX model
    print()
    print("=" * 60)
    print("Optional: MDX-Net Dereverb (ONNX) Model")
    print("=" * 60)
    print("This model is larger and provides stereo reverb removal.")
    print()

    download_onnx = input("Download ONNX dereverb model? (y/n): ").strip().lower()

    if download_onnx == 'y':
        print()
        print("Downloading ONNX model folder...")

        # ONNX models are in a folder structure, we need to download individual files
        onnx_files = [
            "uvr5_weights/onnx_dereverb_By_FoxJoy/vocals.onnx",
        ]

        for onnx_path in onnx_files:
            onnx_name = os.path.basename(onnx_path)
            destination = os.path.join(script_dir, onnx_path)

            if os.path.exists(destination):
                print(f"✓ {onnx_name} already exists, skipping...")
                continue

            print(f"Downloading {onnx_name}...")
            url = f"{HF_BASE_URL}/{onnx_path}"

            if download_file(url, destination):
                print(f"✓ Downloaded {onnx_name}")
                successful += 1
            else:
                print(f"✗ Failed to download {onnx_name}")
                failed += 1

    # Summary
    print()
    print("=" * 60)
    print("Download Summary")
    print("=" * 60)
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()

    if failed == 0:
        print("✓ All models downloaded successfully!")
        print()
        print("You can now use Mangio-RVC-Fork!")
        print("- Essential models (hubert_base.pt, rmvpe.pt) are ready for voice conversion")
        print("- UVR5 models are ready for vocals/accompaniment separation")
    else:
        print("⚠ Some downloads failed. Please check your internet connection and try again.")
        print()
        print("Note: Essential models (hubert_base.pt, rmvpe.pt) are REQUIRED for RVC to work.")

    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Download interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
