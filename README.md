# status-display-notify-send

<!-- [![ci](https://github.com/rachmadanHaryono/status-display-notify-send/workflows/ci/badge.svg)](https://github.com/rachmadanHaryono/status-display-notify-send/actions?query=workflow%3Aci) -->
<!-- [![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://rachmadanHaryono.github.io/status-display-notify-send/) -->
<!-- [![pypi version](https://img.shields.io/pypi/v/status-display-notify-send.svg)](https://pypi.org/project/status-display-notify-send/) -->
<!-- [![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/status-display-notify-send/community) -->
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

display song cmus is playing using notify-send.

## Requirements

status-display-notify-send requires Python 3.7 or above.

<details>
<summary>To install Python 3.7, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.7
pyenv install 3.7

# make it available globally
pyenv global system 3.7
```
</details>

## Installation

With `pip`:
```bash
python3 -m pip install status-display-notify-send
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3 -m pip install --user pipx

pipx install --python python3.6 status-display-notify-send
```
