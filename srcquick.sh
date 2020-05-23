./sasrcode.py > commands.sh && chmod +x commands.sh
grep ar71xx commands.sh > commands/ath79-no-dt.sh
grep ramips commands.sh > commands/ralink.sh
grep ath79 commands.sh > commands/ath79.sh
grep kirkwood commands.sh > commands/mach-mvebu.sh
grep bcm53xx commands.sh > commands/mach-bcm.sh
grep at91 commands.sh > commands/mach-at91.sh
grep oxnas commands.sh > commands/mach-oxnas.sh
grep ipq806x commands.sh > commands/mach-qcom.sh
grep layerscape commands.sh > commands/mach-imx
grep malta commands.sh > commands/malta.sh
grep orion commands.sh > commands/mach-orion5x.sh
grep lantiq commands.sh > commands/lantiq.sh
