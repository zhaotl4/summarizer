import os
import sys 
sys.path.append("..") 
from PreSumm.src.abs_final_summary import abs_final_summ
def presum_abs_summ():
    
    os.system('cd .. && cd PreSumm && sh scripts.sh')
    summ = abs_final_summ()
    return summ
    
