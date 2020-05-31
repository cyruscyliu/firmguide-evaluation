# firmadyne
./sabinary.py -dbt firmadyne > commandb.sh && chmod +x commandb.sh
grep "/ar71xx/generic" commandb.sh > commandb/ar71xx_generic.sh
grep "/ramips/rt305x" commandb.sh > commandb/ramips_rt305x.sh
grep "/ramips/mt7620" commandb.sh > commandb/ramips_mt7620.sh
grep "/ramips/mt7621" commandb.sh > commandb/ramips_mt7621.sh
grep "/ath79/generic" commandb.sh > commandb/ath79_generic.sh
grep "/kirkwood/generic" commandb.sh > commandb/kirkwood_generic.sh
grep "/bcm53xx/generic" commandb.sh > commandb/bcm53xx_generic.sh
grep "/ramips/rt3883" commandb.sh > commandb/ramips_rt3883.sh
grep "/ramips/generic" commandb.sh > commandb/ramips_generic.sh
grep "/ipq40xx/generic" commandb.sh > commandb/ipq40xx_generic.sh
grep "/ramips/rt288x" commandb.sh > commandb/ramips_rt288x.sh
grep "/oxnas/generic" commandb.sh > commandb/oxnas_generic.sh
grep "/imx6/generic" commandb.sh > commandb/imx6_generic.sh
