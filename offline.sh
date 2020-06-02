#!/bin/bash
cd ~/esv
 ./salamander close
 ./salamander open -p ~/build/2529f54b83692eebb2a9a9db2ef50ae6/
 ./salamander synthesize -nc
 ./salamander close
 ./salamander open -p ~/build/89494294f998e62c0784f215d25eae64/
 ./salamander synthesize -nc
 ./salamander close
 ./salamander open -p ~/build/1eb17956454ba2925775bced266ee1a9/
 ./salamander synthesize -nc
 ./salamander close
 ./salamander open -p ~/build/653f4efe62bbf5e0a329dac4a57de2b5/
 ./salamander synthesize -nc
 ./salamander close
 ./salamander open -p ~/build/bfae3162fb949c343763ad9ea7ab3fe0/
 ./salamander synthesize -nc
 ./salamander close
 cd $OLDPWD
