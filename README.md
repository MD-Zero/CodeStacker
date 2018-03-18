
<h1 style="text-align:center">CodeStacker (CS)</h1>
<p style="text-align:center">A Python build system for C++ projects.</p>

## Features ##
- Simple and straightforward YAML configuration file ("blueprint")
- Recompile only what needs to be
- No garbage produced, only object files and binaries

## Prerequisites ##
CS requires to have Python3 to be installed. Any subsequent
dependencies will be installed by pip3.

## Installing ##
From this repository:
```sh
$ git clone https://github.com/MD-Zero/CodeStacker.git
$ cd CodeStacker
$ pip3 install --user --upgrade .
```

## Usages ##
Once installed with pip, CS is available through the command line:
```sh
$ codestacker build
--- OR ---
$ codestacker -f path/to/blueprint.yaml -c release build
--- OR ---
$ codestacker -v clean
```

## Blueprint grammar ##
The **blueprint file** is a file defining **one or several strategies** for CS
to **carry out a build**. Written using the YAML markup language, it follows a
certain structure which needs to be respected for CS to understand what needs to
be *done* and *how*.

To begin with, let's start with an example of a basic `blueprint.yaml` file:

```yaml
---
default:
  root: project
  binary: $project/bin
  build: $project/build
  include: $project/include
  sources: $project/src
  output: Test
  flags: [-pedantic-errors]
  libraries: [glfw]
...
```

### Structure ###
A blueprint can specify any number of YAML _document_, identified by the
enclosing `---` and `...` markers.<br/>CS **doesn't really mind**, as it will
read all those documents at once and load them in memory.<br/>**Be careful**
when defining several documents with the same structure: **only the last one**
in the file will be used!

CS expects documents to contain one **"master key"** (here `default`),
referencing many **"children keys"**:
* The master key defines your **configuration's name**: by default, CS will look
for a default one (**`default`**) if unspecified; otherwise, you can tell CS to
use yours with the `-c` flag in the command line.
* The children keys define many parameter that CS will use to build your
project.
