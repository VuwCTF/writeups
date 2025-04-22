We are given a series of vi-style commands and a flag that has been mixed up using them. I created a file using the python command `open("test", "wb").write(bytes(60 + range(48))` (48 is the length of the modified file). Then I opened `test` in vim and inputted the commands provided. However the commands clearly didn't work as intended so I manually did some things. Then we have a file that was modified in the same way as the original flag, that we can reverse. Using these we can reconstruct the flag (I needed to patch it a bit since I must have misinputted something at some point)

DawgCTF{pAwsibiLiti3s_ar3_m30wV3l0us}
[The challenge file](/test.modified)
