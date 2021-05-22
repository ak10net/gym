from tqdm import tqdm, trange
import time

'''
for i in tqdm([1,2,3,4,5]):
    time.sleep(0.3)
 '''
'''
for i in trange(10):
    time.sleep(0.3)
'''

with tqdm(total=100) as pbar:
    for i in range(10):
        time.sleep(0.1)
        pbar.update(10)
        
        
print('done')