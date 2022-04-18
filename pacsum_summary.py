import os
import sys 
sys.path.append("..") 
from PacSum.code.pacsum_bert import bert_summary
def bert_summ():
    
    os.system('cd .. && cd PacSum && sh scripts.sh')
    summ = bert_summary()
    return summ
    