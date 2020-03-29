# firmadyne
./sabinary.py -dbt firmadyne > commandb.sh && chmod +x commandb.sh
grep "/ar71xx/generic" commandb.sh > commandb/ar71xx_generic.sh
./sample.py commandb/ar71xx_generic.sh
grep "/ramips/rt3883" commandb.sh > commandb/ramips_rt3883.sh
./sample.py commandb/ramips_rt3883.sh
grep "/bcm53xx/generic" commandb.sh > commandb/bcm53xx_generic.sh
./sample.py commandb/bcm53xx_generic.sh
grep "/kirkwood/generic" commandb.sh > commandb/kirkwood_generic.sh
./sample.py commandb/kirkwood_generic.sh
# grep "/ar7/" commandb.sh > commandb/ar7.sh
# grep "/brcm47xx/" commandb.sh > commandb/bcm47xx.sh
# grep "/adm5120/" commandb.sh > commandb/adm5120.sh
# kernel < 2.6 different from 2.6 above
# grep "/bcm947xx/" commandb.sh > commandb/bcm947xx.sh
# grep "/atheros/" commandb.sh > commandb/ar231x.sh
grep "/oxnas/generic" commandb.sh > commandb/oxnas_generic.sh
./sample.py commandb/oxnas_generic.sh
# grep "/orion/" commandb.sh > commandb/mach-orion5x.sh

./sasrcode.py -dbt firmadyne > commands.sh && chmod +x commands.sh
# grep ath79 commands.sh > commands/ath79.sh
grep ralink commands.sh > commands/ralink.sh
# grep "ar7 " commands.sh > commands/ar7.sh
# grep bcm47xx commands.sh > commands/bcm47xx.sh
# grep adm5120 commands.sh > commands/adm5120.sh
# grep bcm63xx commands.sh > commands/bcm63xx.sh
# kernel < 2.6 different from 2.6 above
# grep bcm947xx commands.sh > commands/bcm947xx.sh
# grep ar231x commands.sh > commands/ar231x.sh
grep mach-oxnas commands.sh > commands/mach-oxnas.sh
# grep mach-orion5x commands.sh > commands/mach-orion5x.sh
# grep lantiq commands.sh > commands/lantiq.sh
# grep bcm53xx commands.sh > commands/mach-bcm.sh
# grep at91 commands.sh > commands/mach-at91.sh
# grep ipq806x commands.sh > commands/mach-qcom.sh
# grep mvebu commands.sh > commands/mach-mvebu.sh

# text
# ./sabinary.py -dbt text > allb.sh && chmod +x allb.sh
# ./sasrcode.py -dbt text > alls.sh && chmod +x alls.sh

