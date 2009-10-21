cat alignments/all.stk | python/nameInternals.py groups/A.group groups/B.group groups/C.group groups/PV.group > tree.newick

python/autoAnnotate.py -seqs alignments/all.stk -groups groups/A.group groups/B.group groups/C.group groups/PV.group -names A B C PV -gff gff/all.gff > annos.stk

cat tree.newick	> alignments/HRVtrain.stk
cat annos.stk >> alignments/HRVtrain.stk
cat alignments/all.stk |grep -v NH >> alignments/HRVtrain.stk 
