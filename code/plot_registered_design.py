#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();root=a.root
    bg=pd.read_csv(root/'data/processed/ame2012_mass_standardized.csv')
    dev=pd.read_csv(root/'data/processed/TARGETS_DEVELOPMENT_AME2012_TO_2016.csv')
    con=pd.read_csv(root/'data/processed/TARGETS_CONFIRMATION_AME2016_TO_2020_LOCKED.csv')
    fig,ax=plt.subplots(figsize=(6.6,4.8))
    ax.scatter(bg['N'],bg['Z'],s=9,marker='.',c='0.82',label='AME2012 primary measured set',rasterized=True)
    ax.scatter(dev['N'],dev['Z'],s=34,marker='o',facecolors='none',edgecolors='#0072B2',linewidths=1.2,label='AME2012→2016 development')
    ax.scatter(con['N'],con['Z'],s=36,marker='s',facecolors='none',edgecolors='#D55E00',linewidths=1.2,label='AME2016→2020 locked confirmation')
    ax.set_xlabel('Neutron number $N$');ax.set_ylabel('Proton number $Z$')
    ax.set_title('Chronology-registered evaluation nuclei')
    ax.legend(frameon=False,fontsize=8,loc='upper left')
    ax.grid(alpha=.15,linewidth=.5)
    fig.tight_layout()
    out=root/'figures/Fig1_Registered_Historical_Design.pdf';fig.savefig(out,bbox_inches='tight')
    fig.savefig(root/'figures/Fig1_Registered_Historical_Design.png',dpi=240,bbox_inches='tight')
    plt.close(fig)
    print(out)
if __name__=='__main__':main()
