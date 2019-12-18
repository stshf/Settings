## Setting

My Setting

## Caps lock -> Control
```bash
gsettings set org.gnome.desktop.input-sources xkb-options "['ctrl:nocaps']"
```

## Git
```bash
sudo apt-get install git
```

## Vim
```bash
sudo apt-get install vim
```

## 1. bash -> zsh
* install zsh
```bash
sudo apt-get install #!/usr/bin/env zsh
chsh -s $(which zsh)
sudo reboot
```
* zprezto
```bash
git clone --recursive https://github.com/sorin-ionescu/prezto.git "${ZDOTDIR:-$HOME}/.zprezto"
setopt EXTENDED_GLOB
for rcfile in "${ZDOTDIR:-$HOME}"/.zprezto/runcoms/^README.md(.N); do
  ln -s "$rcfile" "${ZDOTDIR:-$HOME}/.${rcfile:t}"
done
```
* .file
```bash
git clone https://github.com/stshf/Settings.git
mv Settings/zsh/.zpreztorc ./
mv Settings/zsh/.zshrc ./
source .zpreztorc
source .zshrc
```

2. Neovim

set python environment using pyenv

* Install packages for compiling python
```bash
sudo apt install build-essential libbz2-dev libdb-dev \
  libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
  libncursesw5-dev libsqlite3-dev libssl-dev \
  zlib1g-dev uuid-dev tk-dev
```

* pyenv install
```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshenv
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshenv
echo 'eval "$(pyenv init -)"' >> ~/.zshenv
```

* Start another shell
```bash
sudo ~/.pyenv/plugins/python-build/install.sh
```

* build python for Neovim
```bash
pyenv install 3.7.2
pyenv rehash
pyenv global 3.7.2
python --version
pip --version
```

* Install Neovim

```bash
pip install neovim
pip freeze | grep neovim
sudo add-apt-repository ppa:neovim-ppa/stable
sudo apt-get update
sudo apt-get install neovim
```
* set my config file
```bash
mv ~/Settings/nvim ~/.config/
```

* dein
```bash
sudo apt-get install curl
mkdir -p ~/.cache/dein
cd ~/.cache/dein
curl https://raw.githubusercontent.com/Shougo/dein.vim/master/bin/installer.sh > installer.sh
sh ./installer.sh ~/.cache/dein
```
