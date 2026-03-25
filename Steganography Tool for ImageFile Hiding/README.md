# Steganography Tool for Image/File Hiding

A modern GUI tool to hide and extract text or files within images using Least Significant Bit (LSB) steganography.

## Features
- **Modern UI**: Built with `customtkinter` for a sleek, dark-themed interface.
- **Drag-and-Drop**: Easily drop images into the tool to encode or decode.
- **LSB Encoding**: Uses the `stepic` library to embed data without visible changes to the image.
- **Format Support**: Supports PNG and BMP (PNG is recommended for lossless storage).

## Prerequisites
- Python 3.7+
- pip

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```

2. **To Encode (Hide Message):**
   - Go to the **Encode** tab.
   - Drag and drop an image or click to browse.
   - Enter your secret message in the text box.
   - Click **Hide Data & Save** and choose where to save the modified image (must be .png to preserve data).

3. **To Decode (Extract Message):**
   - Go to the **Decode** tab.
   - Drag and drop the modified image.
   - Click **Extract Hidden Data**.
   - The hidden message will appear in the output box.

## Architecture
- `app.py`: Main GUI implementation.
- `stego_engine.py`: Core steganography logic using `Pillow` and `stepic`.
- `requirements.txt`: List of dependencies.
