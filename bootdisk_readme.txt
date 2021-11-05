>wmic diskdrive list brief
Caption                          DeviceID            Model                            Partitions  Size
ST4000DM004-2CV104               \\.\PHYSICALDRIVE1  ST4000DM004-2CV104               2           4000784417280
Kingston FCR-HS219/1 USB Device  \\.\PHYSICALDRIVE6  Kingston FCR-HS219/1 USB Device  0
ST2000DM001-9YN164               \\.\PHYSICALDRIVE2  ST2000DM001-9YN164               3           2000396321280
ST2000DM001-1CH164               \\.\PHYSICALDRIVE3  ST2000DM001-1CH164               2           2000396321280
Samsung SSD 860 EVO 500GB        \\.\PHYSICALDRIVE0  Samsung SSD 860 EVO 500GB        3           500105249280


D:\canon_hack\bootdisk>python canon_bootdisk.py sd.img
[+] reading VBR at sector 99 (offset 0xc600), for partition #0, type 6, size: 506781 sectors
[+] recognized filesystem: b'FAT16'

D:\canon_hack\bootdisk>python canon_bootdisk.py -c sd.img
[+] reading VBR at sector 99 (offset 0xc600), for partition #0, type 6, size: 506781 sectors
[+] recognized filesystem: b'FAT16'
Volume label: b'EOS_DEVELOP', Boot program+2: b'BOOTDISK', at 0x1f0: b'\x00\x00\x00\x00\x00\x00'

D:\canon_hack\bootdisk>python canon_bootdisk.py -pi sd.img
[+] reading VBR at sector 99 (offset 0xc600), for partition #0, type 6, size: 506781 sectors
[+] recognized filesystem: b'FAT16'
[+] patching VBR in memory...
[+] saving patched data as patched.bin
[+] patching VBR in sd.img

D:\canon_hack\bootdisk>python canon_bootdisk.py -c sd.img
[+] reading VBR at sector 99 (offset 0xc600), for partition #0, type 6, size: 506781 sectors
[+] recognized filesystem: b'FAT16'
Volume label: b'EOS_DEVELOP', Boot program+2: b'BOOTDISK', at 0x1f0: b'SCRIPT'