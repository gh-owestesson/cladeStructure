<<A Makefile will soon be here.  For now just storing key commands...>> 

cat alignments/all.stk | python/nameInternals.py groups/A.group groups/B.group groups/C.group groups/PV.group > alignments/HRVtrain.stk

python/autoAnnotate.py -seqs alignments/all.stk -groups groups/A.group groups/B.group groups/C.group groups/PV.group -names A B C PV -gff gff/all.gff >> alignments/HRVtrain.stk

cat alignments/all.stk |grep -v NH >> alignments/HRVtrain.stk 
