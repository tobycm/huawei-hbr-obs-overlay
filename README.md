# Huawei Band HBR OBS Overlay

A overlay for displaying heart rate from Huawei Band 8, 9, 10 (?) watches on OBS

## How to use

### Requirements

- BLE capable machine
- [uv](https://docs.astral.sh/uv/) - install uv to install python and dependencies
- [OBS Studio](https://obsproject.com/) - duh

### 1. Install Python (skip if already installed)

```sh
uv python install
```

### 2. Install dependencies

```sh
uv sync
```

### 3. Set HBR mode on watch

Depends on model. On Band 9, go to Settings, scroll down, and select HR Broadcast.

### 4. Run the overlay

```sh
uv run main.py
```

### 5. Add the overlay to OBS

Use a Window Capture (Windows) / Screen Capture (Linux). Select tk window. Add filter to the capture, select Chroma Key and choose `green` color.

### 6. ???

### 7. Profit

## Ending notes

Monitoring code credit: https://gist.github.com/HDR/4a778f21a05dbb9648d26e15acd3eb0c
