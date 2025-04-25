This is a basic SSTI(Server Side Template Injection)  challenge.
I just copy pasted my saved payload: `{{ {{ request.application.\__globals\_\_.\__builtins\_\_.\__import__('os').popen('cat /flag.txt').read() }}`

Basically SSTI is where you get to inject code into the server side from the client. What my code is doing is requesting global applications to import os, and with this library open flag.txt and read it.

SummitCTF{sStI_1s_r3ally_popul4r_4_some_r3s0n}
