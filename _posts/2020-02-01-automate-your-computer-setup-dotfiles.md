---
layout: post
title: Automate your computer setup with dotfiles
date: 2020-02-01
excerpt:
    In this post we are going to look at how to automatically setup your
    computer with your favorite software and configurations. This can be very
    useful when you have a new computer, or when it gets stolen (unfortunaltey
    it happened to me recently).
cover: terminal.png
categories: ["Computer Setup"]
---

## Motivation

Often, when changing laptop or after formatting it, I had to
go through the tedious operation of reinstalling every software I had as well
as all the configuration files. This is when I ask myself "how did I manage
to configure this?", or "what was this amazing extension that worked
so well?". I got fed up of this process and I decided to write down every
program I installed on my machine and backup all the configuration files in
a Github repository: [github.com/ericdaat/dotfiles](https://github.com/ericdaat/dotfiles).

The idea was to never lose a single handy configuration file and to be able to setup a new
computer in a very short time. Of course there are tools like Apple
Time Machine that backs up your computer and lets you reinstall everything
when you acquire a new one, but I wanted something lighter, dedicated to
programming tools.

In this post, you will find (almost) every software and tools I am using,
as well as a script to install them on your computer. Note that I am using
apple computers, so it probably won't work as such for windows and linux.

## Tools I am using

Let's go ahead and review all the tools I use.

### Homebrew Package manager

Linux has [APT](https://en.wikipedia.org/wiki/APT_(software)) (advanced
package tool) that lets you install software using the command line. While
it can be a bit surprising when you're not used to this, it's much more
productive than using graphical interfaces. Anyway, when you're on macOS,
there is no native package manager like that, but you can download one
like [Homebrew](https://brew.sh/) to install all your software.

To install `homebrew`, run the following command in a terminal:

``` bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then, you can install a software very easily with the `brew install` command.
In my case, here is a list of all the software I am installing with homebrew:

``` bash
brew install python3;
brew install r;
brew install vim;
brew install htop;
brew install fzf;
brew install ctags;
brew install node;
brew install zsh;
brew install wget;
brew install tmux;
brew install watch;
brew install nmap;
brew install zmq;
brew install gcc;
brew install eralchemy;
brew install pandoc;

brew install nginx;
brew install redis;
brew install postgresql;
```

In addition to homebrew, there is
[homebrew cask](https://github.com/Homebrew/homebrew-cask), to install
GUI macOS applications like Google Chrome. Again, here is my list:

``` bash
# Browsers
brew cask install google-chrome;
brew cask install firefox;

# Code
brew cask install postman;
brew cask install visual-studio-code;
brew cask install sublime-text;
brew cask install sublime-merge;
brew cask install iterm2;
brew cask install hyper;
brew cask install docker;
brew cask install mactex;
brew cask install homebrew/cask-versions/adoptopenjdk8;
brew cask install rstudio;
brew cask install metabase;

# Apps
brew cask install slack;
brew cask install spotify;
brew cask install vlc;
brew cask install skype;
brew cask install zoomus;
brew cask install whatsapp;
brew cask install zotero;

# Drivers
brew cask install chromedriver
```

### Terminal

Now moving on to configuring your terminal to improve productivity.

#### Zsh

The [Z shell](https://en.wikipedia.org/wiki/Z_shell) is an extended
[Bourne shell](https://en.wikipedia.org/wiki/Bourne_shell) with many
improvements. I prefer it to other shell like
[Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)). Apparently Apple
prefers is too since [macOS Catalina adopted zsh as the default shell, replacing
Bash](https://www.theverge.com/2019/6/4/18651872/apple-macos-catalina-zsh-bash-shell-replacement-features).

If you don't have zsh installed already, run `brew install zsh` to do so.
Then, make sure to customize it with [Oh My Zsh](https://ohmyz.sh/):

``` bash
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

You can edit the terminal theme, and add
[plugins](https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins) like
[git](https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins#git),
[auto completion](https://github.com/zsh-users/zsh-autosuggestions),
[syntax highlighting](https://github.com/zsh-users/zsh-syntax-highlighting),
etc ...

#### Hyper

The native macOS terminal is good but very basic. For instance, you can't
split the windows into multiple terminals. I like [Hyper](https://hyper.is/),
it's a beautiful and modern terminal built on web technologies. You can install
it with `brew cask hyper`. Once installed, you can configure Hyper with the
`.hyper.js` configuration file located in your home directory.
Mine is available
[here](https://github.com/ericdaat/dotfiles/blob/master/hyper/.hyper.js).
Also, make sure to check out this [list of awesome hyper extensions](https://github.com/bnb/awesome-hyper).

### Text editors and IDE

Now onto text editors and IDE (Integrated Development Environment). Like
most developers I like having a clean and productive coding environment. I
changed my mind many times on which text editors and IDE I should use but now
I have a fairly stable list.

#### Jupyter Lab

As a Data Scientist, I love working with Jupyter notebooks to quickly create
presentations or come up with Machine Learning model prototypes.
[Jupyter Lab](https://jupyterlab.readthedocs.io/en/stable/) is for me the best
way to work with Jupyter notebooks. You can customize its appearance and
add useful extensions like [table of contents (toc)](https://github.com/jupyterlab/jupyterlab-toc).

I usually install Jupyter Lab with pip: `pip install jupyterlab`. Then, here
are some of the tweaks I like to make:

- **Python kernels from virtual environments**: I like having multiple
  python virtual environments on my machine, depending on which project
  I am working on. You can install these environments as jupyter kernel
  by doing the following:

  ``` bash
  virtualenv $HOME/venv -p python3;
  source $HOME/venv/bin/activate;
  pip install ipykernel;
  python -m ipykernel install --user --name venv --display-name "Python (venv)"
  ```

- **R kernel**: I recently started using R, but I am not used to R Studio yet,
  so I prefer to stick to Jupyter Lab by using the jupyter R kernel.
  You can install with the following commands in R:

  ``` R
  install.packages(c("repr", "IRdisplay", "IRkernel"), type = "source", repos="https://cran.rstudio.com")
  IRkernel::installspec()
  ```

- **Jupyter Lab extensions**: as mentioned previously, Jupyter Lab allows you
  to install extensions. The ones I love are
  [table of contents](https://github.com/jupyterlab/jupyterlab-toc) and
  [templates](https://github.com/timkpaine/jupyterlab_templates).

  They are pretty easy to install:

  ``` bash
  # toc
  jupyter labextension install @jupyterlab/toc

  # templates
  pip install jupyterlab_templates;
  jupyter labextension install jupyterlab_templates;
  jupyter serverextension enable --py jupyterlab_templates;
  cp notebook_templates /usr/local/share/jupyter/notebook_templates;
  ```

#### Vim

[Vim](https://www.vim.org/) is a very powerful and highly customisable text
editor accessible directly from your terminal. However, it's not really
straighforward, and people struggle to use it at first.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">I&#39;ve been using Vim for about 2 years now, mostly because I can&#39;t figure out how to exit it.</p>&mdash; I Am Devloper (@iamdevloper) <a href="https://twitter.com/iamdevloper/status/435555976687923200?ref_src=twsrc%5Etfw">February 17, 2014</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

But with some dedication, and a good vim configuration, you'll be able to
appreciate it and get very productive! My `.vimrc` configuration file
is available [here](https://github.com/ericdaat/dotfiles/blob/master/vim/vimrc).

Vim plugins can be installed with [Pathogen](https://github.com/tpope/vim-pathogen).

Here are the plugins I am using so far:

- Layout
  - [vim-airline](https://github.com/vim-airline/vim-airline)
  - [dracula](https://github.com/dracula/vim)
- Code
  - [NerdCommenter](https://github.com/scrooloose/nerdcommenter)
  - [Jedi](https://github.com/davidhalter/jedi-vim)
  - [vim-fugitive](https://github.com/tpope/vim-fugitive)
  - [ale](https://github.com/w0rp/ale)

I install all my plugins with [this shell script](https://github.com/ericdaat/dotfiles/blob/master/vim/vim.sh).

#### Visual Studio Code

I mosty code in Python, and I was initially using
[Pycharm IDE](https://www.jetbrains.com/pycharm/). Then, a friend introduced
me to Microsoft Visual Studio Code, and I loved it. It's highly customisable
and can be used for any programming language. I love how tools like
unit testing, docker containers and git versioning are integrated with the
editor, it's very convenient to have everything at the same place.

You can install it with brew: `brew cask install visual-studio-code`.

The list of plugins I use is avaiable [here](https://github.com/ericdaat/dotfiles/blob/master/vscode/extensions.txt).
You can get the list of commands to install them by running the following
command:

``` bash
cat extensions.txt | xargs -L 1 echo code --install-extension
```

#### Sublime Text

Sublime Text is the very first text editor I used when I started to learn
Python. I still use it from time to time, when I am not on vim or VS Code.

Install it with brew: `brew cask install sublime-text`.

Again, I love how customisable it is. Make sure to install
[Package control](https://packagecontrol.io/) that will let you install
sublime text extensions. You can either install it by copy and paste a command
line into Sublime text, or by running the following command:

``` bash
export SUBLIME_PATH="$HOME/Library/Application Support/Sublime Text 3"
wget -O "$SUBLIME_PATH/Installed Packages" "https://packagecontrol.io/Package%20Control.sublime-package";
```

Then, you can install the packages you want within Sublime Text, or by
directly using the Sublime Text configuration files so that the program
installs them automatically for you. For that, you will need two files:

- [Package Control.sublime-settings](https://github.com/ericdaat/dotfiles/blob/master/sublime_text/Package%20Control.sublime-settings)
- [Preferences.sublime-settings](https://github.com/ericdaat/dotfiles/blob/master/sublime_text/Preferences.sublime-settings)

Copy these two files where Sublime Text wants them:

``` bash
export SUBLIME_PATH="$HOME/Library/Application Support/Sublime Text 3"
cp "Package Control.sublime-settings" "$SUBLIME_PATH/Packages/User/"
cp "Preferences.sublime-settings" "$SUBLIME_PATH/Packages/User/"
```

## Conclusion

I hope this post was useful, and conviced you to store all the software,
configuration files and plugins somewhere safe. Make sure to checkout my
Github repo [github.com/ericdaat/dotfiles](https://github.com/ericdaat/dotfiles)
to have the full code.
