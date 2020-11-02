import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set()
import re
import argparse
print('start')
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('outdir',help='Directory containing output of Retinaface')
    parser.add_argument('annodir',help='Directory containing manual annotations')
    parser.add_argument('data',help='Dataset')
    args = parser.parse_args()
    outdir = args.outdir
    annodir = args.annodir
    data = args.data
    
    true_pos = 0
    false_pos = 0
    false_neg = 0
    true_neg = 0
    image = pd.DataFrame(columns=['image','precision','recall'])
    for filename in os.listdir(outdir):
        boolean = False
        annotated_file = open(os.path.join(annodir,filename),'r').read()
        output_file = open(os.path.join(outdir,filename),'r').read()
        a = output_file.strip().split('\n')
        b = annotated_file.strip().split('\n')
        if len(a) == 1:
            false_neg += 1
        else:
            for y in a[1:]:
                y = np.array(y.strip().split()).astype(int)
                boolean = False
                for x in b[1:]:
                    x = np.array(x.strip().split()).astype(int)
                    flag1 = y[0] in range(x[0]-10,x[0]+10,1)
                    flag2 = y[1] in range(x[1]-10,x[1]+10,1)
                    flag3 = y[2] in range(x[2]-10,x[2]+10,1)
                    flag4 = y[3] in range(x[3]-10,x[3]+10,1)
                    if flag1 and flag2 and flag3 and flag4:
                        boolean = True
                        true_pos += 1
                        break
                if not boolean:
                    false_pos += 1
        print(filename)
        image = image.append(pd.DataFrame({
            'image': re.sub('.txt','',filename),
            'precision': true_pos/(true_pos+false_pos),
            'recall': true_pos/(true_pos+false_neg)
        },index=[0]))
    image = image.reset_index(drop=True)
    image = image.sort_values(by=['precision','recall'],ascending=False)
    fig,axs = plt.subplots(figsize=(10,10))
    sns.lineplot(image['recall'],image['precision'],ax=axs,sort=True,size=10,legend=False,color='red',linewidth=3.5,markers=True)
    axs.set_title('Precision vs Recall curve per Image')
    axs.set_xlabel('Recall')
    axs.set_ylabel('Precision')
    fig.savefig('{}.png'.format(data))
    print('Average Precision: {}\nAverage Recall: {}'.format(np.mean(image['precision']),np.mean(image['recall'])))
    print('fin')