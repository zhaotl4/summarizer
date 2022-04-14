import os
import sys 
sys.path.append("..") 
from PreSumm.src.abs_final_summary import abs_final_summ
def presum_abs():
    
    print(os.system('pwd'))
    os.system('cd .. && cd PreSumm && sh scripts.sh')
    print(os.system('pwd'))
    summ = abs_final_summ()
    print(summ)
    return summ
    

presum_abs()