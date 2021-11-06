#!/usr/bin/env python3
'''
 @lorenzo33324

 a python tool to check, or patch FAT16/FAT32/Exfat disk images for Canon hacking
 v1.0 (30dec2020)

 tested with Python 3.7.3 on Windows 10

 references: 
 - https://magiclantern.fandom.com/wiki/Bootdisk (EOS_DEVELOP and BOOTDISK strings for autoexec.bin)
 - https://www.magiclantern.fm/forum/index.php?topic=24827.msg230344#msg230344 (STRING string for Canon Basic)
 - https://chdk.fandom.com/wiki/Canon_Basic
'''

import sys
from struct import Struct, pack
from collections import namedtuple
import argparse

class Mbr:
  PARTITION_LIST_OFFSET = 0x1be
  SYNC_OFFSET = 0x1fe
  SYNC_VALUE = 0xaa55
  NUM_PARTITION = 4
  SECTOR_SIZE = 512
  
  #https://www.ntfs.com/fat-part-types.htm
  #4, for FAT16 and partition < 32mb
  #6, for FAT16 and partitions >= 32mb
  #14, FAT LBA
  partitions_type = { 4:'FAT16 <32mb', 6:'FAT16', 14:'FAT16 LBA', 7:'ExFat/NTFS/ReFS', 11:'FAT32', 12:'FAT32 LBA' }

  S_PARTITION = Struct('<B3sB3sLL')
  NT_PARTITION = namedtuple('mbr_partition', 'bootflag chs_first type chs_last lba_start lba_size')
  
  def __init__(self, data):
    self.data = data
    if Struct('<H').unpack_from( self.data, Mbr.SYNC_OFFSET)[0] != Mbr.SYNC_VALUE:
      print('error not sync word in MBR')    
    
  def parse(self):
    part_list = []
    for p in range(Mbr.NUM_PARTITION):
      nt_part = Mbr.NT_PARTITION( *Mbr.S_PARTITION.unpack_from( self.data, Mbr.PARTITION_LIST_OFFSET +p*16) )
      if nt_part.type != 0:
        part_list.append( nt_part )    
    return part_list

#to recognize FAT16, FAT32 and ExFat
#to modify Volume label, Boot program and SCRIPT at 0x1f0

class Fat:
  # https://www.ntfs.com/fat-partition-sector.htm
  boot_program_offset = { b'FAT16':62, b'FAT32':90, b'ExFAT':120 } #0x3e, 0x5a, 0x78
  volume_label_offset = { b'FAT16':43, b'FAT32':71, b'ExFAT':130 } #0x2b, 0x47, 0x82
  system_id_offset = { b'FAT16':54, b'FAT32':82, b'ExFAT':3 } #0x36, 0x52
  
  VOLUME_LABEL_SIZE = 11
  SCRIPT_OFFSET = 0x1f0 #https://chdk.fandom.com/wiki/Canon_Basic/Card_Setup
  
  def __init__(self, data, type):
    self.data = data
    self.type = type
    
  def parse(self) :
    oem_name = self.data[3:3+8]
    if self.type == 6 or self.type == 4 or self.type == 14: #FAT16
      self.fs_name = b'FAT16'
    elif self.type == 11 or self.type == 12: #FAT32, https://www.easeus.com/resource/fat32-disk-structure.htm
      self.fs_name = b'FAT32'
    elif self.type == 7: #ExFAT,
      self.fs_name = b'ExFAT'
      assert oem_name == b'EXFAT   '

    voffset, idOffset, boffset = Fat.volume_label_offset[self.fs_name], Fat.system_id_offset[self.fs_name], Fat.boot_program_offset[self.fs_name]+2
    volume_label = self.data[ voffset: voffset+Fat.VOLUME_LABEL_SIZE ]
    system_id    = self.data[ idOffset: idOffset+8 ]
    bootdisk_id  = self.data[ boffset: boffset+8 ]
    string_str = self.data[ Fat.SCRIPT_OFFSET: Fat.SCRIPT_OFFSET+6 ]
    self.vlabel = voffset
    self.bp = boffset
    
    return oem_name, volume_label, system_id, bootdisk_id, string_str 

  def ExFatSum( data ):
    checksum = 0  
    for c in range( len(data) ):
      if c==106 or c==107 or c==112: #skip 'volume flags' and 'percent in use'
        continue
      checksum = ((checksum<<31)&0xffffffff | (checksum>>1)&0xffffffff) + data[c]
    return checksum
    
  def patch(self, remove=False):
    if remove:
      develop = b' '*Fat.VOLUME_LABEL_SIZE
      boot = b' '*8
      script = b' '*6
    else:
      develop = b'EOS_DEVELOP'
      boot = b'BOOTDISK'
      script = b'SCRIPT'

    if self.fs_name == b'ExFAT': #also patching 'SCRIPT', in case of
      #vlabel > bp
      patched = self.data[:self.bp] + boot + self.data[self.bp+8:self.vlabel] + develop + self.data[self.vlabel+Fat.VOLUME_LABEL_SIZE:Fat.SCRIPT_OFFSET] + script + self.data[Fat.SCRIPT_OFFSET+6: -512] #remove last sector filled with checksum  
      chksum = Fat.ExFatSum( patched )
      print('    new checksum: %x' % chksum)
      cs_sector = pack('<L', chksum )*128
      return patched + cs_sector
    else:
      patched = self.data[:self.vlabel] + develop + self.data[self.vlabel+Fat.VOLUME_LABEL_SIZE:self.bp] + boot + self.data[self.bp+8:Fat.SCRIPT_OFFSET] + script + self.data[Fat.SCRIPT_OFFSET+6: 512] #only first sector  
      return patched


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("filename", help="disk image")
  parser.add_argument("-c", "--check", help="check STRINGS", action="store_true")
  parser.add_argument("-p", "--patch", help="patch STRINGS", action="store_true")
  parser.add_argument("-i", "--inplace", help="patch orginal disk imakeoutput file", action="store_true", default=False )
  parser.add_argument("-o", "--output", help="output file", default='patched.bin' )
  args = parser.parse_args()

              
  with open(args.filename, 'rb') as dump_file:
    mbr_data = dump_file.read(Mbr.SECTOR_SIZE)
    mbr = Mbr( mbr_data )
    partitions = mbr.parse()
    #print( partitions )
    
    print('[+] reading VBR at sector %d (offset 0x%x), for partition #0, type %d, size: %d sectors' % (partitions[0].lba_start, partitions[0].lba_start*Mbr.SECTOR_SIZE, partitions[0].type, partitions[0].lba_size) )
    #print('%x' % (partitions[0].lba_start*512) )
    
    dump_file.seek( partitions[0].lba_start*Mbr.SECTOR_SIZE )
    vbr_data = dump_file.read(Mbr.SECTOR_SIZE*12) #12 sectors for ExFat
    dump_file.close()
    
    if partitions[0].type in Mbr.partitions_type:
      fat = Fat( vbr_data, partitions[0].type )
      results = fat.parse()
      print('[+] recognized filesystem: %s' % fat.fs_name )
      if args.check:
        print('Volume label: %s, Boot program+2: %s, at 0x1f0: %s' % ( results[1], results[3], results[4] ) )
      #print( results )
      if args.patch:
        print('[+] patching VBR in memory...' )
        patched = fat.patch( )
        if args.output: #save patched data in separate file
          with open(args.output, 'wb') as patch:
            print('[+] saving patched data as %s' % args.output )
            patch.write( patched ) #for ExFat, only save main VBR sectors
        if args.inplace:
          with open(args.filename, 'r+b') as write_file:
            write_file.seek( partitions[0].lba_start*Mbr.SECTOR_SIZE )
            print('[+] patching VBR in %s' % args.filename )
            write_file.write( patched ) #for FAT16, FAT32 and first VBR of ExFat
            if fat.fs_name == b'ExFAT':
              write_file.write( patched ) #backup VBR


      
