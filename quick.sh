# firmadyne
./sabinary.py -dbt firmadyne > commandb.sh && chmod +x commandb.sh
grep "/ar71xx/" commandb.sh > commandb/ath79.sh
grep "/ramips/" commandb.sh > commandb/ralink.sh
grep "/ar7/" commandb.sh > commandb/ar7.sh
grep "/brcm47xx/" commandb.sh > commandb/bcm47xx.sh
grep "/adm5120/" commandb.sh > commandb/adm5120.sh
# kernel < 2.6 different from 2.6 above
# grep "/bcm947xx/" commandb.sh > commandb/bcm947xx.sh
grep "/atheros/" commandb.sh > commandb/ar231x.sh
grep "/oxnas/" commandb.sh > commandb/mach-oxnas.sh
grep "/orion/" commandb.sh > commandb/mach-orion5x.sh

./sasrcode.py -dbt firmadyne > commands.sh && chmod +x commands.sh
grep ath79 commands.sh > commands/ath79.sh
grep ralink commands.sh > commands/ralink.sh
grep "ar7 " commands.sh > commands/ar7.sh
grep bcm47xx commands.sh > commands/bcm47xx.sh
grep adm5120 commands.sh > commands/adm5120.sh
# kernel < 2.6 different from 2.6 above
# grep bcm947xx commands.sh > commands/bcm947xx.sh
grep ar231x commands.sh > commands/ar231x.sh
grep mach-oxnas commands.sh > commands/mach-oxnas.sh
grep mach-orion5x commands.sh > commands/mach-orion5x.sh

# text
# ./sabinary.py -dbt text > allb.sh && chmod +x allb.sh
# ./sasrcode.py -dbt text > alls.sh && chmod +x alls.sh

