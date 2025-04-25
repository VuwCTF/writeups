ida gave us ```C
if ( argc == 2 && argv[1] )
  {
    compareHash = "a0a8b4b0d49e10fe3cea86cfb182e895bf086ae1";
    iLen = strlen(argv[1]);
    SHA1(argv[1], iLen, inputBuff);
    for ( i = 0; i <= 19; ++i )
      snprintf(&setSpecifiedFormat[2 * i], 3uLL, "%02x", (unsigned __int8)inputBuff[i]);
    setSpecifiedFormat[40] = 0;
    flag[0] = 0x160A213C38382006LL;
    flag[1] = 0x3D0A3E313C2E1301LL;
    strcpy(noth, "e\"\n!e\n6e1f");
    v10 = 26LL;
    v9 = 85;
    if ( (unsigned int)checkCompare(setSpecifiedFormat, compareHash) )
    {
      puts("Incorrect key!");
    }
    else
    {
      sub_4011D3((__int64)flag, v10, v9);
      *((_BYTE *)flag + v10) = 0;
      printf("%s}\n", (const char *)flag);
    }
    return 0LL;
  }
  else
  {
    puts("Usage: ./crackme <key>");
    return 1LL;
  }```

We can actually just ignore the hash, and look directly at sub_4011D3 which is the algorithm used to unencrypt the flag.

```C
unsigned __int64 __fastcall sub_4011D3(__int64 flag, unsigned __int64 len, unsigned int xorVal)
{
  unsigned __int64 result; // rax
  unsigned __int64 i; // [rsp+1Ch] [rbp-8h]

  result = xorVal;
  if ( flag )
  {
    for ( i = 0LL; ; ++i )
    {
      result = i;
      if ( i >= len )
        break;
      *(_BYTE *)(flag + i) ^= xorVal;
    }
  }
  return result;
} 

``` 
I have renamed a1 a2 and a3, to easily explain what this is doing. It is simply taking the position in the aray flag, while i < len and xoring it with the value passed in. 

```    
flag[0] = 0x160A213C38382006LL;
flag[1] = 0x3D0A3E313C2E1301LL;
strcpy(noth, "e\"\n!e\n6e1f");
len = 26LL;
xorVal = 85;```

These are the values. Also the string copy, even though it is passing into a different variable, it is part of the flag. So if we take these values and xor then with 85 we can get the flag.
