# firmadyne
./sabinary.py -dbt firmadyne > commandb.sh && chmod +x commandb.sh
./sasrcode.py -dbt firmadyne > commands.sh && chmod +x commands.sh
grep ar71xx commands.sh > commands/ar71xx.sh
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

