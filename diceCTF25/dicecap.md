We are provided a packet capture file. Looking through the individual packets shows sections of a text message:
```
so you're in right sent at 1743126492that zip file thing? i've just zipped it up for you so it should be hot to go! sent at 1743126493

oh yeah of course sent at 1743126493
```
and what appears to be a remote shell:
```
$
./locale

en_US
$
```
 before a FTP transmission is initiated:
 
```
220 (vsFTPd 3.0.5)
USER hacker
331 Please specify the password.
PASS hacker
230 Login successful.
[...]
RETR main
150 Opening BINARY mode data connection for main (16296 bytes).
226 Transfer complete.
MDTM main
213 20250327234415
[...]
RETR coolzip.zip
150 Opening BINARY mode data connection for coolzip.zip (1170 bytes).
226 Transfer complete.
MDTM coolzip.zip
213 20250328014837
```

The files `main` and `coolzip.zip` are transmitted later (in TCP stream 12 and 16 respectively)
We can see from the hex representations that `main` is a Linux executable (ELF) and that `coolzip.zip` is unsurprisingly a ZIP archive. The latter also contains a file called `flag.txt`:
![hex representation of coolzip.zip](https://raw.githubusercontent.com/VuwCTF/writeups/refs/heads/main/diceCTF25/dicecap1.png)
Downloading and attempting to extract it reveals it is password protected. Opening the ELF in Ghidra shows a function `generate_password`. On completion, it prints `The password is: ` then the result of three `strcat` operations. This means the password is split into three components.

The first gets the current time using `time(nullptr)`, returning the Unix time in seconds. It then divides the result, casted to an int, by 60, then multiplies by 60. Because this is integer division, it has the effect of rounding down to the nearest minute. The messages earlier in the communication end with what appear to be Unix timestamps, so we can copy them and round them down:
`(1743126493 / 60) * 60 = 1743126480`

The second component is the locale of the system, which is also conveniently transmitted earlier as `en_US`.

The final component is the result of `getlogin()`. A quick manpage search reveals that this gives the username of the currently logged in user. This is transmitted at the beginning of the FTP session as `hacker`. 
This gives a final password of `1743126480en_UShacker`. Inputting this as the password to the zip file allows us to decrypt it and read the contents of `flag.txt`:
**`dice{5k1d_y0ur_w@y_t0_v1ct0ry_t0d4y!!!}`**
