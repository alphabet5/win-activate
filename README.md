# win-activate
 Windows offline activation tool.


## Setup

```bash
sudo apt-get install chromium-browser python3.9 libnss3-dev && \
curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py && \
sudo python3.9 ./get-pip.py && \
python3.9 -m pip install --upgrade https://github.com/alphabet5/win-activate/releases/download/0.0.1/win_activate-0.0.1-py2.py3-none-any.whl
```

## Building from source

```bash
git clone https://github.com/alphabet5/win-activate.git
cd win-activate
python3.9 setup.py bdist_wheel --universal
python3.9 -m pip install dist/*
```

## Usage

```bash
win-activate --host 1.2.3.4 --pk xxxxx-xxxxx-xxxxx
```

## Changelog
### 0.0.1
- Initial release