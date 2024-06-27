# PixelCrypt

This application is designed to work with BMP files, offering users a variety of functionalities, including creating new
BMP files using different construction algorithms and color schemes, as well as embedding and extracting hidden text
messages. Additionally, the program provides a user-friendly interface with the ability to save recent settings and
files.

## Installation

1. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2. Apply the database migrations:
    ```bash
    python manage.py migrate
    ```
   ```bash
   python manage.py makemigrations
   ```

## Overview

This application provides various functionalities for BMP file manipulation. Users can create new BMP files based on
existing ones, using different construction algorithms and color schemes. It also supports embedding and extracting
hidden text messages within BMP files.

## Key Features

### Visual Interface

- Intuitive visual interface for easy navigation and use of all available functions.

### Selecting and Creating BMP Files

- Select an existing BMP file through a file selection dialog.
- Create new BMP files using one of three construction algorithms and three color schemes.
- Save new BMP files through a save file dialog, choosing the location and name.

### Principles of Image Construction

- **Spiral Drawing:** Calculates pixel colors based on distance from the origin and angle. Three combinations of color
  modulation.
- **Diamond Drawing (Astroid):** Generates a diamond shape centered in the image. Colors determined by position relative
  to the diamond.
- **Rose Drawing:** Uses a mathematical rose curve to determine pixel colors. Three combinations of color channels.

### Message Embedding

- Embed short text messages into BMP files by writing bits into the least significant bits of the BMP file's color map
  bytes.

### Message Extraction

- Extract hidden text messages from BMP files by reconstructing the original text from the embedded bits.

### Authorization

- User authorization with username and password. Saves and restores last settings and files used.

### Activity History

- Saves the last three BMP files worked on, modes of creating new bitmaps, messages embedded, and messages extracted for
  authorized users.

### Automatic Restoration

- Continue working with the last settings or choose from the last three modes/files/messages used after authorization.

### Deauthorization

- Users can deauthorize at any time while retaining current program settings.

### Additional Information

- **User Manual:** Detailed explanations on using all functions of the application.
- **About the Program:** Information about the program, its features, and its purpose.
- **About the Authors:** Information about the developers of the program.
