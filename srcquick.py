./sasrcode.py > commands.sh && chmod +x commands.sh
grep ath79 commands.sh > commands/ath79.sh
grep ramips commands.sh > commands/ralink.sh
# grep "ar7 " commands.sh > commands/ar7.sh
# grep bcm47xx commands.sh > commands/bcm47xx.sh
# grep adm5120 commands.sh > commands/adm5120.sh
# grep bcm63xx commands.sh > commands/bcm63xx.sh
# kernel < 2.6 different from 2.6 above
# grep bcm947xx commands.sh > commands/bcm947xx.sh
# grep ar231x commands.sh > commands/ar231x.sh
# grep mach-oxnas commands.sh > commands/mach-oxnas.sh
# grep mach-orion5x commands.sh > commands/mach-orion5x.sh
# grep lantiq commands.sh > commands/lantiq.sh
# grep bcm53xx commands.sh > commands/mach-bcm.sh
# grep at91 commands.sh > commands/mach-at91.sh
# grep ipq806x commands.sh > commands/mach-qcom.sh
# grep mvebu commands.sh > commands/mach-mvebu.sh
