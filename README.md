# ~kitor Magic Lantern scripts
A few automation scripts I wrote to automate some things in my ML development efforts.
Used only on Debian running over WSL1 on Windows 10, however should be mostly generic.

Maybe they will be helpful for others. If not, at least I will have an easy way to backup and keep my env in sync between devices.

## Contents
### `rgb2png`, `yuv2png`
Scripts that convert raw memory dumps into PNG files.

I think I based processing on some existing script, but I can't recall the source now.

### `ml_deploy`, `ml_deploy_qemu`
Scripts that will deploy ML build ( currently non-zip only ) to card / qemu virtual card

Camera model is required as 1st argument.

### `ml_card_deploy`
Script that will deploy artifacts on card. Called with `sudo` by `ml_deploy`, can be called directly.

Camera model is required as 1st argument.

### `remake`
Shell alias that runs `make clean` and then `make`, passing all arguments.

### `gcp`
Shell alias to `git cherry-pick --no-commit`.

I just use it a lot while creating a clean implementation from "dirty" implementation branches.

### `ml_uart`
Shell alias to `sudo minicom -D /dev/ttyS${port} -b 115200`

Meant to be used with WSL (thus `ttyS<number>`).

Port number is optional as 1st argument, defaults to `3`.

### `ml_env`
File to be sourced in `.bashrc` \ `.zshrc` to expose all the functionality in shell.

### `canon_bootdisk.py`
A tool to make card  / card image bootable on Canon EOS cameras, written by [@lorenzo33324](https://github.com/lclevy)
See [canon_bootdisk.md](canon_bootdisk.md) for more details.

## Requirements
For `ml_deploy_qemu`:
* `virt-make-fs`

## Directory structure
```
$ML_DIR
 |-- bin
 |   `-- *                 ( files from this repository )
 |
 |-- artifacts             ( work dir for preparing card deployment )
 |-- artifacts_qemu        ( work dir for preparing qemu deployment )
 |
 |-- qemu-eos              ( main qemu dir )
 |-- qemu-eos-some_suffix  ( additional qemu dirs )
 |
 |-- src
 |   `-- ml                ( Magic Lantern source directory )
```
## Configuration
see `.config` that I shamelessly left in repo.

## Usage scenarios
__enable all features in shell__

`source /path/to/checkout/.activate`

_( or just put it in `.zshrc` / `.bashrc`)_



__for build-and-deploy from `platform/*` directories__

`remake && ml_deploy R`


__for build-and-deploy from `minimal/*` directories__

`remake MODEL=750D && ml_deploy_qemu 750D`


__start UART session on virtual COM5 (WSL)__

`ml_uart 5`
