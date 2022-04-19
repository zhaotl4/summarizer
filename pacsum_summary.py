import os
import sys 
sys.path.append("..") 
from PacSum.code.pacsum_bert import bert_summary,tfidf_summary
def bert_summ():
    
    os.system('cd .. && cd PacSum && sh scripts.sh')
    summ = bert_summary()
    return summ

def tfidf_summ():
    os.system('cd .. && cd PacSum && sh run_tdidf.sh')
    summ = tfidf_summary()
    return summ
    