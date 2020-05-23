# firmadyne
./sabinary.py -dbt firmadyne > commandb.sh && chmod +x commandb.sh
# grep "/ar71xx/generic" commandb.sh > commandb/ar71xx_generic.sh
# ./sample.py commandb/ar71xx_generic.sh
grep "/ramips/rt3883" commandb.sh > commandb/ramips_rt3883.sh
# ./sample.py commandb/ramips_rt3883.sh
grep "/bcm53xx/generic" commandb.sh > commandb/bcm53xx_generic.sh
# ./sample.py commandb/bcm53xx_generic.sh
grep "/kirkwood/generic" commandb.sh > commandb/kirkwood_generic.sh
# ./sample.py commandb/kirkwood_generic.sh
grep "/ath79/generic" commandb.sh > commandb/ath79_generic.sh
# ./sample.py commandb/ath79_generic.sh
# grep "/ar7/" commandb.sh > commandb/ar7.sh
# grep "/brcm47xx/" commandb.sh > commandb/bcm47xx.sh
# grep "/adm5120/" commandb.sh > commandb/adm5120.sh
# kernel < 2.6 different from 2.6 above
# grep "/bcm947xx/" commandb.sh > commandb/bcm947xx.sh
# grep "/atheros/" commandb.sh > commandb/ar231x.sh
grep "/oxnas/generic" commandb.sh > commandb/oxnas_generic.sh
# ./sample.py commandb/oxnas_generic.sh
# grep "/orion/" commandb.sh > commandb/mach-orion5x.sh
