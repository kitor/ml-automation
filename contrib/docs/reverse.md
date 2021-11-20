# Reverse engineering Canon firmware



## Introduction

This document tries to capitalize knowledge of Magic Lantern development into documentation, as code only might be difficult for new contributors.

It could start as a general index for existing material on Wikis, forum, code and Discord (how to points to it?).

## Existing information and material

### Open source code

Legacy dev tree : https://foss.heptapod.net/magic-lantern/magic-lantern/

Ongoing dev : https://github.com/reticulatedpines/magiclantern_simplified

### Previous work

Forum / Reverse Engineering : https://www.magiclantern.fm/forum/index.php?board=6.0

Forum / General Development : https://www.magiclantern.fm/forum/index.php?board=25.0

Legacy Wiki : https://magiclantern.fandom.com/wiki/Magic_Lantern_Firmware_Wiki

Current Wiki (mostly end user oriented): https://wiki.magiclantern.fm/start

CHDK for devs : https://chdk.fandom.com/wiki/For_Developers (some software and hardware are identical / similar)

## Getting started

See also : https://wiki.magiclantern.fm/faq

### Dumping firmware

#### Canon basic

##### [Canon Basic scripting (DIGIC 8, DIGIC X models)](https://www.magiclantern.fm/forum/index.php?topic=25305.msg230372#msg230372)

#### Universal / portable dumper

https://www.magiclantern.fm/forum/index.php?topic=16534.0

### Analysis firmware

Despite QEmu oriented, it is useful as an overview : https://foss.heptapod.net/magic-lantern/magic-lantern/-/blob/branch/qemu/contrib/qemu/HACKING.rst

#### Ghidra

Download and release : https://github.com/NationalSecurityAgency/ghidra

General tutorial ?

How to load and start analysis ?

Ghidra scripts : https://www.magiclantern.fm/forum/index.php?topic=23810.msg214713#msg214713

## Porting / Contributing

### Find stubs

https://www.magiclantern.fm/forum/index.php?topic=12177.0

(new version with Ghidra ?)

### Debugging

#### QEmu

https://foss.heptapod.net/magic-lantern/magic-lantern/-/tree/branch/qemu/contrib/qemu

#### UART

see devkit-and-uart on discord (how to point to a room ?)

## Ongoing work

Do not ask when it will be ready, contribute instead : code, testing, docs

Most devs discussions are happening on Discord : https://discord.gg/Rnnx5AKG 

### R

### RP

### 200D

#### 5D4

## Hardware information

(not sure it is right to divide software and hardware here)

per Digic hardware differences: https://wiki.magiclantern.fm/digic

### MPU (peripherals)

https://www.magiclantern.fm/forum/index.php?topic=25661.0

### Lime (Network) : 

https://wiki.magiclantern.fm/digic:processors:lime

### EDMAC (External DMA control)

https://www.magiclantern.fm/forum/index.php?topic=26249.0

## Firmware information

### Graphics

##### [Compositors, layers, contexts in RGB and YUV - How Digic 7(6?)+ draw GUI](https://www.magiclantern.fm/forum/index.php?topic=26024.msg235083#msg235083) : 

## Acronym dictionary

See also : https://wiki.magiclantern.fm/glossary

- **ximr** stands for **rmix** : render/mixer : https://discordapp.com/channels/671072748985909258/830413304077877249/909219061722923058





