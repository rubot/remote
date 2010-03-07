#!/usr/bin/python -i
#
# This code was found on the following blog in c++ and converted to python
#
# http://jinxidoru.blogspot.com/2009/06/itunes-remote-pairing-code.html
#
#

"""
Saturday, June 20, 2009
iTunes Remote pairing code

If you have an iPhone or iPod Touch, you are probably familiar with the iTunes Remote app. It allows
you to control iTunes from a really well designed application. I have recently been working on 
reverse engineering the communication so that I can use the same remote to control other media 
applications like Boxee and XBMC. There are a number of other projects doing similar things (stereo).

The communication has not been difficult to decode. It is a variation of the previously 
reverse-engineered DAAP communication used by iTunes sharing. It's referred to as DACP. If you are 
looking for information about this protocol, Jeffrey Sharkey has done an excellent job of 
documenting his efforts in creating a Google Android implementation of the iTunes Remote (Android 
DACP Remote Control).

Before you can use the iPhone as a remote, there is a pairing process which occurs between the 
server and the remote. There is a good discussion of the pairing process by mycroes (Pairing the 
Itunes Remote app with your own server). The one part that is missing is how iTunes generates the 
pairing code which it sends back to the iPhone. I have finally, with a fair bit of effort, been 
able to decode the value.

The pairing code is generated by a hash algorithm I was able to lift and modify from the xine source 
code. The algorithm takes two arguments. The first is the Pair parameter in the _touch-remote._tcp 
zeroconf record (refer to mycroes's article). The Pair parameter is a 16 character hexadecimal 
string. The second is the four digit passcode provided by the remote which must be sent back by 
iTunes (or the custom server).

These two parameters can be passed to the function provided below. The result is a 32 character 
hexadecimal string which is returned back to the remote application in the form of a GET request.

Since this code was modified from GPL source code (xine), it is also protected by the GPL. Feel 
free to use this code for whatever you want. All I ask is that you give me proper attribution. 
Also, I would love to hear what you have done with it, so please let me know if you use it for a 
cool project.

With no further ado, here's the source.



-- 4 digit passcode
-- Pair sent by the remote with the zeroconf advert

"""

import struct

# Expected
# input 0000000000000001 1234
# output 690E6FF61E0D7C747654A42AED17047D

def itunes_pairingcode( passcode, pair ):
    # initialize the param array
    """
    char param[64]
    ::memset( param, 0, 64 )
    param[56] = '\xc0'
    param[24] = '\x80'

    // set the pair value
    ::strncpy( param, pair.c_str(), 16 )
    
    // copy the pair code
    ::strncpy( param+16, passcode.c_str(), 4 )
    param[22] = param[19]
    param[20] = param[18]
    param[18] = param[17]
    param[19] = param[17] = 0
    """
    param  = pair[0:16]
    #            16          17         18          19        20           21       22           23       
    param += passcode[0] + '\x00' + passcode[1] + '\x00' + passcode[2] + '\x00' + passcode[3] + '\x00'
    param += '\x80' + '\x00'*31 + '\xc0' + '\x00'*7
    
    a = 0x67452301
    b = 0xefcdab89
    c = 0x98badcfe
    d = 0x10325476
    
    a = ((b & c) | (~b & d)) + struct.unpack("I",param[0:4])[0] + a - 0x28955B88
    a = ((a << 0x07) | (a >> 0x19)) + b
    d = ((a & b) | (~a & c)) + struct.unpack("I",param[4:8])[0] + d - 0x173848AA
    d = ((d << 0x0c) | (d >> 0x14)) + a
    c = ((d & a) | (~d & b)) + struct.unpack("I",param[8:12])[0] + c + 0x242070DB
    c = ((c << 0x11) | (c >> 0x0f)) + d
    b = ((c & d) | (~c & a)) + struct.unpack("I",param[12:16])[0] + b - 0x3E423112
    b = ((b << 0x16) | (b >> 0x0a)) + c
    a = ((b & c) | (~b & d)) + struct.unpack("I",param[16:20])[0] + a - 0x0A83F051
    a = ((a << 0x07) | (a >> 0x19)) + b
    d = ((a & b) | (~a & c)) + struct.unpack("I",param[20:24])[0] + d + 0x4787C62A
    d = ((d << 0x0c) | (d >> 0x14)) + a
    c = ((d & a) | (~d & b)) + struct.unpack("I",param[24:28])[0] + c - 0x57CFB9ED
    c = ((c << 0x11) | (c >> 0x0f)) + d
    b = ((c & d) | (~c & a)) + struct.unpack("I",param[28:32])[0] + b - 0x02B96AFF
    b = ((b << 0x16) | (b >> 0x0a)) + c
    a = ((b & c) | (~b & d)) + struct.unpack("I",param[32:36])[0] + a + 0x698098D8
    a = ((a << 0x07) | (a >> 0x19)) + b
    d = ((a & b) | (~a & c)) + struct.unpack("I",param[36:40])[0] + d - 0x74BB0851
    d = ((d << 0x0c) | (d >> 0x14)) + a
    c = ((d & a) | (~d & b)) + struct.unpack("I",param[40:44])[0] + c - 0x0000A44F
    c = ((c << 0x11) | (c >> 0x0f)) + d
    b = ((c & d) | (~c & a)) + struct.unpack("I",param[44:48])[0] + b - 0x76A32842
    b = ((b << 0x16) | (b >> 0x0a)) + c
    a = ((b & c) | (~b & d)) + struct.unpack("I",param[48:52])[0] + a + 0x6B901122
    a = ((a << 0x07) | (a >> 0x19)) + b
    d = ((a & b) | (~a & c)) + struct.unpack("I",param[52:56])[0] + d - 0x02678E6D
    d = ((d << 0x0c) | (d >> 0x14)) + a
    c = ((d & a) | (~d & b)) + struct.unpack("I",param[56:60])[0] + c - 0x5986BC72
    c = ((c << 0x11) | (c >> 0x0f)) + d
    b = ((c & d) | (~c & a)) + struct.unpack("I",param[60:64])[0] + b + 0x49B40821
    b = ((b << 0x16) | (b >> 0x0a)) + c
    
    a = ((b & d) | (~d & c)) + struct.unpack("I",param[4:8])[0] + a - 0x09E1DA9E
    a = ((a << 0x05) | (a >> 0x1b)) + b
    d = ((a & c) | (~c & b)) + struct.unpack("I",param[24:28])[0] + d - 0x3FBF4CC0
    d = ((d << 0x09) | (d >> 0x17)) + a
    c = ((d & b) | (~b & a)) + struct.unpack("I",param[44:48])[0] + c + 0x265E5A51
    c = ((c << 0x0e) | (c >> 0x12)) + d
    b = ((c & a) | (~a & d)) + struct.unpack("I",param[0:4])[0] + b - 0x16493856
    b = ((b << 0x14) | (b >> 0x0c)) + c
    a = ((b & d) | (~d & c)) + struct.unpack("I",param[20:24])[0] + a - 0x29D0EFA3
    a = ((a << 0x05) | (a >> 0x1b)) + b
    d = ((a & c) | (~c & b)) + struct.unpack("I",param[40:44])[0] + d + 0x02441453
    d = ((d << 0x09) | (d >> 0x17)) + a
    c = ((d & b) | (~b & a)) + struct.unpack("I",param[60:64])[0] + c - 0x275E197F
    c = ((c << 0x0e) | (c >> 0x12)) + d
    b = ((c & a) | (~a & d)) + struct.unpack("I",param[16:20])[0] + b - 0x182C0438
    b = ((b << 0x14) | (b >> 0x0c)) + c
    a = ((b & d) | (~d & c)) + struct.unpack("I",param[0x24:0x28])[0] + a + 0x21E1CDE6
    a = ((a << 0x05) | (a >> 0x1b)) + b
    d = ((a & c) | (~c & b)) + struct.unpack("I",param[0x38:60])[0] + d - 0x3CC8F82A
    d = ((d << 0x09) | (d >> 0x17)) + a
    c = ((d & b) | (~b & a)) + struct.unpack("I",param[0x0c:16])[0] + c - 0x0B2AF279
    c = ((c << 0x0e) | (c >> 0x12)) + d
    b = ((c & a) | (~a & d)) + struct.unpack("I",param[0x20:0x24])[0] + b + 0x455A14ED
    b = ((b << 0x14) | (b >> 0x0c)) + c
    a = ((b & d) | (~d & c)) + struct.unpack("I",param[0x34:0x38])[0] + a - 0x561C16FB
    a = ((a << 0x05) | (a >> 0x1b)) + b
    d = ((a & c) | (~c & b)) + struct.unpack("I",param[0x08:12])[0] + d - 0x03105C08
    d = ((d << 0x09) | (d >> 0x17)) + a
    c = ((d & b) | (~b & a)) + struct.unpack("I",param[0x1c:32])[0] + c + 0x676F02D9
    c = ((c << 0x0e) | (c >> 0x12)) + d
    b = ((c & a) | (~a & d)) + struct.unpack("I",param[0x30:0x34])[0] + b - 0x72D5B376
    b = ((b << 0x14) | (b >> 0x0c)) + c
    
    a = (b ^ c ^ d) + struct.unpack("I",param[0x14:0x18])[0] + a - 0x0005C6BE
    a = ((a << 0x04) | (a >> 0x1c)) + b
    d = (a ^ b ^ c) + struct.unpack("I",param[0x20:0x24])[0] + d - 0x788E097F
    d = ((d << 0x0b) | (d >> 0x15)) + a
    c = (d ^ a ^ b) + struct.unpack("I",param[0x2c:48])[0] + c + 0x6D9D6122
    c = ((c << 0x10) | (c >> 0x10)) + d
    b = (c ^ d ^ a) + struct.unpack("I",param[0x38:60])[0] + b - 0x021AC7F4
    b = ((b << 0x17) | (b >> 0x09)) + c
    a = (b ^ c ^ d) + struct.unpack("I",param[0x04:8])[0] + a - 0x5B4115BC
    a = ((a << 0x04) | (a >> 0x1c)) + b
    d = (a ^ b ^ c) + struct.unpack("I",param[0x10:0x14])[0] + d + 0x4BDECFA9
    d = ((d << 0x0b) | (d >> 0x15)) + a
    c = (d ^ a ^ b) + struct.unpack("I",param[0x1c:32])[0] + c - 0x0944B4A0
    c = ((c << 0x10) | (c >> 0x10)) + d
    b = (c ^ d ^ a) + struct.unpack("I",param[0x28:44])[0] + b - 0x41404390
    b = ((b << 0x17) | (b >> 0x09)) + c
    a = (b ^ c ^ d) + struct.unpack("I",param[0x34:0x38])[0] + a + 0x289B7EC6
    a = ((a << 0x04) | (a >> 0x1c)) + b
    d = (a ^ b ^ c) + struct.unpack("I",param[0x00:4])[0] + d - 0x155ED806
    d = ((d << 0x0b) | (d >> 0x15)) + a
    c = (d ^ a ^ b) + struct.unpack("I",param[0x0c:16])[0] + c - 0x2B10CF7B
    c = ((c << 0x10) | (c >> 0x10)) + d
    b = (c ^ d ^ a) + struct.unpack("I",param[0x18:28])[0] + b + 0x04881D05
    b = ((b << 0x17) | (b >> 0x09)) + c
    a = (b ^ c ^ d) + struct.unpack("I",param[0x24:0x28])[0] + a - 0x262B2FC7
    a = ((a << 0x04) | (a >> 0x1c)) + b
    d = (a ^ b ^ c) + struct.unpack("I",param[0x30:0x34])[0] + d - 0x1924661B
    d = ((d << 0x0b) | (d >> 0x15)) + a
    c = (d ^ a ^ b) + struct.unpack("I",param[0x3c:64])[0] + c + 0x1fa27cf8
    c = ((c << 0x10) | (c >> 0x10)) + d
    b = (c ^ d ^ a) + struct.unpack("I",param[0x08:12])[0] + b - 0x3B53A99B
    b = ((b << 0x17) | (b >> 0x09)) + c
    
    a = ((~d | b) ^ c) + struct.unpack("I",param[0x00:4])[0] + a - 0x0BD6DDBC
    a = ((a << 0x06) | (a >> 0x1a)) + b
    d = ((~c | a) ^ b) + struct.unpack("I",param[0x1c:32])[0] + d + 0x432AFF97
    d = ((d << 0x0a) | (d >> 0x16)) + a
    c = ((~b | d) ^ a) + struct.unpack("I",param[0x38:60])[0] + c - 0x546BDC59
    c = ((c << 0x0f) | (c >> 0x11)) + d
    b = ((~a | c) ^ d) + struct.unpack("I",param[0x14:0x18])[0] + b - 0x036C5FC7
    b = ((b << 0x15) | (b >> 0x0b)) + c
    a = ((~d | b) ^ c) + struct.unpack("I",param[0x30:0x34])[0] + a + 0x655B59C3
    a = ((a << 0x06) | (a >> 0x1a)) + b
    d = ((~c | a) ^ b) + struct.unpack("I",param[0x0C:16])[0] + d - 0x70F3336E
    d = ((d << 0x0a) | (d >> 0x16)) + a
    c = ((~b | d) ^ a) + struct.unpack("I",param[0x28:44])[0] + c - 0x00100B83
    c = ((c << 0x0f) | (c >> 0x11)) + d
    b = ((~a | c) ^ d) + struct.unpack("I",param[0x04:8])[0] + b - 0x7A7BA22F
    b = ((b << 0x15) | (b >> 0x0b)) + c
    a = ((~d | b) ^ c) + struct.unpack("I",param[0x20:0x24])[0] + a + 0x6FA87E4F
    a = ((a << 0x06) | (a >> 0x1a)) + b
    d = ((~c | a) ^ b) + struct.unpack("I",param[0x3c:64])[0] + d - 0x01D31920
    d = ((d << 0x0a) | (d >> 0x16)) + a
    c = ((~b | d) ^ a) + struct.unpack("I",param[0x18:28])[0] + c - 0x5CFEBCEC
    c = ((c << 0x0f) | (c >> 0x11)) + d
    b = ((~a | c) ^ d) + struct.unpack("I",param[0x34:0x38])[0] + b + 0x4E0811A1
    b = ((b << 0x15) | (b >> 0x0b)) + c
    a = ((~d | b) ^ c) + struct.unpack("I",param[0x10:0x14])[0] + a - 0x08AC817E
    a = ((a << 0x06) | (a >> 0x1a)) + b
    d = ((~c | a) ^ b) + struct.unpack("I",param[0x2c:48])[0] + d - 0x42C50DCB
    d = ((d << 0x0a) | (d >> 0x16)) + a
    c = ((~b | d) ^ a) + struct.unpack("I",param[0x08:12])[0] + c + 0x2AD7D2BB
    c = ((c << 0x0f) | (c >> 0x11)) + d
    b = ((~a | c) ^ d) + struct.unpack("I",param[0x24:0x28])[0] + b - 0x14792C6F
    b = ((b << 0x15) | (b >> 0x0b)) + c

    a += 0x67452301
    b += 0xefcdab89
    c += 0x98badcfe
    d += 0x10325476
    
    # switch to little endian
    a = ((a&0xff000000)>>24) + ((a&0xff0000)>>8) + ((a&0xff00)<<8) + ((a&0xff)<<24)
    b = ((b&0xff000000)>>24) + ((b&0xff0000)>>8) + ((b&0xff00)<<8) + ((b&0xff)<<24)
    c = ((c&0xff000000)>>24) + ((c&0xff0000)>>8) + ((c&0xff00)<<8) + ((c&0xff)<<24)
    d = ((d&0xff000000)>>24) + ((d&0xff0000)>>8) + ((d&0xff00)<<8) + ((d&0xff)<<24)
    
    # write the pairing id and return it
    return struct.pack("IIII", a, b, c, d )



