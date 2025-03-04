echo "mydeseq2-antisenseReads5 vs mynoiseq-antisenseReads5"
echo "****************************** inf_lt_0h_vs_ctr ******************************"
perl ~/scripts/myscripts/rnaseqCompareTsv.pl genelist_med4phm2 mydeseq2-antisenseReads5/mydeseq2HoAs.updn.inf_lt_0h_vs_ctr.tsv mynoiseq-antisenseReads5/mynoiseqHoAs.updn.inf_lt_0h_vs_ctr.tsv deseq2 noiseq | grep "deseq2.*noiseq"
echo "****************************** inf_lt_1h_vs_ctr ******************************"
perl ~/scripts/myscripts/rnaseqCompareTsv.pl genelist_med4phm2 mydeseq2-antisenseReads5/mydeseq2HoAs.updn.inf_lt_1h_vs_ctr.tsv mynoiseq-antisenseReads5/mynoiseqHoAs.updn.inf_lt_1h_vs_ctr.tsv deseq2 noiseq | grep "deseq2.*noiseq"
echo "****************************** inf_lt_2h_vs_ctr ******************************"
perl ~/scripts/myscripts/rnaseqCompareTsv.pl genelist_med4phm2 mydeseq2-antisenseReads5/mydeseq2HoAs.updn.inf_lt_2h_vs_ctr.tsv mynoiseq-antisenseReads5/mynoiseqHoAs.updn.inf_lt_2h_vs_ctr.tsv deseq2 noiseq | grep "deseq2.*noiseq"
echo "****************************** inf_lt_4h_vs_ctr ******************************"
perl ~/scripts/myscripts/rnaseqCompareTsv.pl genelist_med4phm2 mydeseq2-antisenseReads5/mydeseq2HoAs.updn.inf_lt_4h_vs_ctr.tsv mynoiseq-antisenseReads5/mynoiseqHoAs.updn.inf_lt_4h_vs_ctr.tsv deseq2 noiseq | grep "deseq2.*noiseq"
echo "****************************** inf_lt_8h_vs_ctr ******************************"
perl ~/scripts/myscripts/rnaseqCompareTsv.pl genelist_med4phm2 mydeseq2-antisenseReads5/mydeseq2HoAs.updn.inf_lt_8h_vs_ctr.tsv mynoiseq-antisenseReads5/mynoiseqHoAs.updn.inf_lt_8h_vs_ctr.tsv deseq2 noiseq | grep "deseq2.*noiseq"
echo "****************************** inf_dk_0h_vs_ctr ******************************"
perl ~/scripts/myscripts/rnaseqCompareTsv.pl genelist_med4phm2 mydeseq2-antisenseReads5/mydeseq2HoAs.updn.inf_dk_0h_vs_ctr.tsv mynoiseq-antisenseReads5/mynoiseqHoAs.updn.inf_dk_0h_vs_ctr.tsv deseq2 noiseq | grep "deseq2.*noiseq"
echo "****************************** inf_dk_1h_vs_ctr ******************************"
perl ~/scripts/myscripts/rnaseqCompareTsv.pl genelist_med4phm2 mydeseq2-antisenseReads5/mydeseq2HoAs.updn.inf_dk_1h_vs_ctr.tsv mynoiseq-antisenseReads5/mynoiseqHoAs.updn.inf_dk_1h_vs_ctr.tsv deseq2 noiseq | grep "deseq2.*noiseq"
echo "****************************** inf_dk_2h_vs_ctr ******************************"
perl ~/scripts/myscripts/rnaseqCompareTsv.pl genelist_med4phm2 mydeseq2-antisenseReads5/mydeseq2HoAs.updn.inf_dk_2h_vs_ctr.tsv mynoiseq-antisenseReads5/mynoiseqHoAs.updn.inf_dk_2h_vs_ctr.tsv deseq2 noiseq | grep "deseq2.*noiseq"
echo "****************************** inf_dk_4h_vs_ctr ******************************"
perl ~/scripts/myscripts/rnaseqCompareTsv.pl genelist_med4phm2 mydeseq2-antisenseReads5/mydeseq2HoAs.updn.inf_dk_4h_vs_ctr.tsv mynoiseq-antisenseReads5/mynoiseqHoAs.updn.inf_dk_4h_vs_ctr.tsv deseq2 noiseq | grep "deseq2.*noiseq"
echo "****************************** inf_dk_8h_vs_ctr ******************************"
perl ~/scripts/myscripts/rnaseqCompareTsv.pl genelist_med4phm2 mydeseq2-antisenseReads5/mydeseq2HoAs.updn.inf_dk_8h_vs_ctr.tsv mynoiseq-antisenseReads5/mynoiseqHoAs.updn.inf_dk_8h_vs_ctr.tsv deseq2 noiseq | grep "deseq2.*noiseq"
