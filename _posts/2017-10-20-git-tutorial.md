---
layout: post
title: An introduction to Git
date: 2017-10-20
excerpt:
    A short introduction and tutorial to Git, the versionning tool created by Linus Torvalds.
cover: tree.jpg
---

## Some History

Git was created by Linus Torvalds in 2005 for development of the Linux kernel,
with other kernel developers contributing to its initial development.
Its current maintainer since 2005 is Junio Hamano.

The name "git" was given by Linus Torvalds when he wrote the very first version. He described the tool as "the stupid content tracker" and the name as (depending on your way):

 1. random three-letter combination that is pronounceable, and not actually used by any common UNIX command. The fact that it is a mispronunciation of "get" may or may not be relevant.
 2. stupid. contemptible and despicable. simple. Take your pick from the dictionary of slang.
 3. "global information tracker": you're in a good mood, and it actually works for you. Angels sing, and a light suddenly fills the room.
 4. "g*dd*mn idiotic truckload of sh*t": when it breaks

*Source: [Wikipedia](https://en.wikipedia.org/wiki/Git)*

## First Steps

### Install git

``` bash
sudo apt-get install git
```

### Configure git

``` bash
git config --global user.name "John Doe"
git config --global user.email "john@example.com"
```

### Init an empty repository

``` bash
mkdir lab-git && cd lab-git
git init
```

### ... Or clone an exisiting one

``` bash
git clone git://github.com/schacon/grit.git
```

### Create a file

``` bash
touch hi.py
```

So far we have:

 1. A local git repository
 2. A `hi.py` file that is not being tracked

What we need to do:

 1. Tell git to track the file
 2. Create a remote repository to store our code
 3. Push our code to the remote repository

### Tracking a file

``` bash
git status # our file is untracked
git add hi.py
git status # our file is tracked!
```

### Setting a remote repository

Usually done through websites like [github](https://github.com), [bitbucket](https://bitbucket.org/), [gitlab](https://about.gitlab.com/).

Once a remote repository is created, we are provided its url. Then, tell the local repository what its remote url is.

``` bash
git remote add origin https://github.com/user/repo.git # origin is our remote name
git remote -V # verify the remote
```

### Commit and push to the remote repository

Even though we tracked our file, we didn't commit anything. When commiting, we provide a message explaining what we changes within the tracked files.

``` bash
git commit -m "started tracking hi.py"
```

Now, we commited our change. Although, everything is still local, nothing is published on the remote repository yet. To do so, we must `push` our last commit.

``` bash
git push origin master # push to the branch master on the origin remote repository
```

To get the latest changes on remote, use `pull` command.

``` bash
git pull origin master
```

### Additional useful commands

Display last commits

``` bash
git log
```

Display what has been changed since the last commit

``` bash
git diff
```

Cancels all local changes and rolls back to how the file was at latest commit

``` bash
git checkout hi.py
```

### A visual recap

![git_basic_usage](/assets/img/articles/git/git-stages.png)

*Source: [marklodato.github.io](https://marklodato.github.io/visual-git-guide/index-en.html)*

## Collaborating with other people

### Common configuration

*n* co-workers, one repository, one production server.

Co-workers work on the same project and can edit the same files simultaneously. Updates are pushed on the distant repository, and pulled from the production server.

![git_servers](/assets/img/articles/git/git-servers.png)

NEVER EVER commit, push or edit anything on the production server.

### Branches

Branches allow people to work on separate tasks without messing with the master branch code. It is useful to experiment, or add functionalities. Branches can start from the master branch, or from another branch.

![git_branches](/assets/img/articles/git/git-branches.png)

*Source : [backlogtool.com](https://backlogtool.com/git-tutorial/en/stepup/stepup1_5.html)*

Check branches within local repository

``` bash
git branch
```

Create a branch named `awesome-feature` from the active branch

``` bash
git checkout -b awesome-feature
```

Edit some code, add and commit files. Then push them to the remote server, but not on master.

``` bash
git push origin awesome-feature # create branch on the remote repo
```

Delete local branch

``` bash
git branch -d awesome-feature
```

### Merging and pull requests

When we are finished working on our feature-branch, we must check for conflicts before pushing to master. To do so, pull the master branch into your branch, and fix your conflicts locally.

When all the conflicts are resolved, push again, *still on your branch*, to the remote repository. Then, make a pull request, that will eventually get merged on the master branch by the repository administrator.

## More useful tools

### Stash your local changes

When your `git pull` fails because you are editing a file that has been changed by someone else, temporarily stash your changes, pull the recent modifications, then apply your changes again.

``` bash
git pull origin awesome-feature # fails

git stash conflict-file.py # stash changes
git pull origin awesome-feature # works but your changes are temporarily gone
git stash apply # re-apply your changes
git commit -m "made the world a better place"
git push origin awesome-feature # now the world really is a better place
```

### Ignore unnecessary files

Please never add anything other than code/configuration files in a git repository. This is not Google Drive.

Create a `.gitignore` file at the root of your repository, with the following content:

``` yml
*.pyc
*.csv
```

This tells git to never track `.pyc` or `.csv` files, because who needs to ?

You can also ignore entire directories. You should avoid using `git add *` if you're not sure you're ignoring unnecessary files.

### Remove files on the repository

What if you no longer want to track something ?

``` bash
git rm go_away.py # will also delete the file from your disk
```

``` bash
git rm --cached go_away.py # will only delete on the remote repository
```

### Versioning configuration files or critical files

Sometimes you want to track files that contain passwords, or configuration
variables.
Those files are likely to change independently from the code, so
you don't want to commit every single change in those.
They might also
contain sensitive information that you don't want to store within the
repository.

What you should is tracking a `.dist` version of the file that has all the
required fields, but without any value.

``` yml
DB_HOST=
DB_USER=
DB_PASSWORD=
```

If you are refering to a conf file named `variables.env`, name you dist file
`variables.env.dist`. Track the `.dist` file, but ignore `variables.env`.

### README.md

Every repository should have a decent README.md file, explaining what it is
about, and how to configure and install the dependencies to start the
application.
This file is written using the *Markdown* syntax. You can read about it and
have look at this [cheat
sheet](https://guides.github.com/pdfs/markdown-cheatsheet-online.pdf) to get
started.

Go ahead and do this tutorial if you have 15 minutes to spare: [try.github.io](https://try.github.io/levels/1/challenges/1)
