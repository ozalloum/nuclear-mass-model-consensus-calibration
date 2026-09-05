#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from consensus_core import MODELS, wilson

COLORS={'development':'#0072B2','confirmation':'#D55E00','FRDM2012':'#0072B2','HFB27':'#E69F00','DZ31':'#009E73','WS4':'#CC79A7'}
MARKERS={'development':'o','confirmation':'s','FRDM2012':'o','HFB27':'s','DZ31':'^','WS4':'D'}
LINESTYLES={'development':'-','confirmation':'--','FRDM2012':'-','HFB27':'--','DZ31':'-.','WS4':':'}


def bootstrap_ci(values, fn=np.mean, nboot=10000, seed=42, alpha=.05):
    x=np.asarray(values,float);x=x[np.isfinite(x)]
    if len(x)<2:return (np.nan,np.nan)
    rng=np.random.default_rng(seed);vals=np.empty(nboot,float)
    for b in range(nboot):
        ii=rng.integers(0,len(x),len(x)); vals[b]=fn(x[ii])
    return tuple(np.quantile(vals,[alpha/2,1-alpha/2]))


def safe_spearman(x,y):
    x=np.asarray(x,float);y=np.asarray(y,float);ok=np.isfinite(x)&np.isfinite(y);x=x[ok];y=y[ok]
    if len(x)<3:return (len(x),np.nan,np.nan)
    r=spearmanr(x,y);return (len(x),float(r.statistic),float(r.pvalue))


def bin_by_edges(x,edges,labels):
    # Development defines the internal cut points. Values outside the development
    # range in the later confirmation belong to the outermost bins rather than
    # being dropped.
    e=np.asarray(edges,float).copy();e[0]=-np.inf;e[-1]=np.inf
    return pd.cut(x,bins=e,labels=labels,include_lowest=True,right=True)


def quintile_table(df,cfg,vintage):
    edges=cfg['D_quintile_edges_MeV'];labels=[f'Q{i}' for i in range(1,6)]
    sub=df.dropna(subset=['D_MeV','E_MeV']).copy();sub['D_bin']=bin_by_edges(sub.D_MeV,edges,labels)
    rows=[]
    for lab in labels:
        x=sub.loc[sub.D_bin==lab,'E_MeV'].to_numpy(float)
        lo,hi=bootstrap_ci(x)
        rows.append({'vintage':vintage,'D_bin':lab,'n':len(x),'D_left':edges[labels.index(lab)],'D_right':edges[labels.index(lab)+1],
                     'mean_E_MeV':float(np.mean(x)) if len(x) else np.nan,'median_E_MeV':float(np.median(x)) if len(x) else np.nan,
                     'mean_E_ci95_lo':lo,'mean_E_ci95_hi':hi})
    return pd.DataFrame(rows)


def condition_table(df,cfg,vintage):
    sub=df.dropna(subset=['D_MeV','E_MeV']).copy()
    A=cfg['fc_A'];sub['FC_A']=(sub.D_MeV<=A['D_max_MeV'])&(sub.E_MeV>=A['E_min_MeV'])
    rows=[]
    def add(var,level,g):
        n=len(g);k=int(g.FC_A.sum());ci=wilson(k,n)
        rows.append({'vintage':vintage,'variable':var,'level':str(level),'n':n,'mean_E_MeV':g.E_MeV.mean(),
                     'median_E_MeV':g.E_MeV.median(),'median_D_MeV':g.D_MeV.median(),
                     'fc_A_n':k,'fc_A_prevalence':k/n if n else np.nan,'fc_A_wilson95_lo':ci[0],'fc_A_wilson95_hi':ci[1]})
    dlabels=['near','middle','far'];sub['d2_tercile']=bin_by_edges(sub.d2_nearest_prior_primary,cfg['extrapolation_d2_tercile_edges'],dlabels)
    ilabels=['low I','mid I','high I'];sub['I_tercile']=bin_by_edges(sub.isospin_asymmetry,cfg['isospin_tercile_edges'],ilabels)
    for lab,g in sub.groupby('d2_tercile',observed=False):
        if len(g):add('extrapolation_distance',lab,g)
    for lab,g in sub.groupby('near_magic',observed=False):add('near_magic',int(lab),g)
    for lab,g in sub.groupby('I_tercile',observed=False):
        if len(g):add('isospin_asymmetry',lab,g)
    return pd.DataFrame(rows)


def signed_residuals(df):
    sub=df.dropna(subset=['D_MeV']).copy()
    out={}
    for m in MODELS: out[m]=sub[f'ME_{m}']-sub.mass_excess_MeV
    return pd.DataFrame(out).corr(method='pearson')


def loo_table(df,vintage):
    sub=df.dropna(subset=['D_MeV']).copy();rows=[]
    for omit in MODELS:
        keep=[m for m in MODELS if m!=omit]
        pred=sub[[f'ME_{m}' for m in keep]].mean(axis=1)
        err=(pred-sub.mass_excess_MeV).abs()
        rows.append({'vintage':vintage,'omitted_model':omit,'n':len(err),'MAE_MeV':err.mean(),'median_AE_MeV':err.median()})
    return pd.DataFrame(rows)


def s2n_summary(df,vintage):
    sub=df.dropna(subset=['D_S2n_MeV','E_S2n_MeV']).copy();n,r,p=safe_spearman(sub.D_S2n_MeV,sub.E_S2n_MeV)
    rows=[{'vintage':vintage,'quantity':'consensus','n':n,'MAE_MeV':sub.E_S2n_MeV.mean() if n else np.nan,
           'spearman_D_vs_E':r,'spearman_p':p}]
    for m in MODELS:
        ss=df.dropna(subset=[f'S2n_{m}_MeV','S2n_exp_MeV']).copy()
        rows.append({'vintage':vintage,'quantity':m,'n':len(ss),'MAE_MeV':(ss[f'S2n_{m}_MeV']-ss.S2n_exp_MeV).abs().mean(),
                     'spearman_D_vs_E':np.nan,'spearman_p':np.nan})
    return pd.DataFrame(rows)


def performance_table(dev,con,cfg):
    rows=[]
    for vintage,df in [('development',dev),('confirmation',con)]:
        sub=df.dropna(subset=['D_MeV','E_MeV']).copy();n,r,p=safe_spearman(sub.D_MeV,sub.E_MeV)
        A=cfg['fc_A'];B=cfg['fc_B']
        fa=(sub.D_MeV<=A['D_max_MeV'])&(sub.E_MeV>=A['E_min_MeV']);fb=(sub.D_MeV<=B['D_max_MeV'])&(sub.E_MeV>=B['E_min_MeV'])
        row={'vintage':vintage,'n_complete':n,'consensus_mean_MAE_MeV':sub.E_MeV.mean(),'consensus_median_MAE_MeV':sub.E_median_MeV.mean(),
             'spearman_D_vs_E':r,'spearman_p':p,'fc_A_n':int(fa.sum()),'fc_A_prevalence':fa.mean(),'fc_B_n':int(fb.sum()),'fc_B_prevalence':fb.mean()}
        for m in MODELS:row[f'{m}_MAE_MeV']=sub[f'err_{m}_MeV'].mean()
        rows.append(row)
    return pd.DataFrame(rows)


def plot_scatter(dev,con,cfg,out):
    fig,ax=plt.subplots(figsize=(5.7,4.4))
    for vintage,df in [('development',dev),('confirmation',con)]:
        sub=df.dropna(subset=['D_MeV','E_MeV'])
        ax.scatter(sub.D_MeV,sub.E_MeV,s=34,marker=MARKERS[vintage],facecolors='none',edgecolors=COLORS[vintage],linewidths=1.15,label=vintage.capitalize())
    A=cfg['fc_A'];ax.axvline(A['D_max_MeV'],color='0.35',ls='--',lw=1,label='FC-A spread threshold')
    ax.axhline(A['E_min_MeV'],color='0.35',ls=':',lw=1,label='FC-A error threshold')
    ax.set_xlabel('Inter-model spread $D$ (MeV)');ax.set_ylabel('Future consensus error $E$ (MeV)')
    ax.set_title('Does model agreement calibrate future error?')
    ax.legend(frameon=False,fontsize=8);ax.grid(alpha=.15,lw=.5);fig.tight_layout();fig.savefig(out,bbox_inches='tight');plt.close(fig)


def plot_quintiles(qtab,out):
    fig,ax=plt.subplots(figsize=(5.7,4.4));x=np.arange(1,6)
    for vintage,off in [('development',-0.06),('confirmation',0.06)]:
        g=qtab[qtab.vintage==vintage].sort_values('D_bin');y=g.mean_E_MeV.to_numpy(float)
        lo=g.mean_E_ci95_lo.to_numpy(float);hi=g.mean_E_ci95_hi.to_numpy(float);err=np.vstack([y-lo,hi-y])
        ax.errorbar(x+off,y,yerr=err,marker=MARKERS[vintage],ls=LINESTYLES[vintage],color=COLORS[vintage],capsize=3,lw=1.5,label=vintage.capitalize())
    ax.set_xticks(x,[f'Q{i}' for i in x]);ax.set_xlabel('Development-defined inter-model-spread quintile');ax.set_ylabel('Mean future absolute error (MeV)')
    ax.set_title('Consensus calibration transferred across AME vintages');ax.legend(frameon=False);ax.grid(alpha=.15,lw=.5);fig.tight_layout();fig.savefig(out,bbox_inches='tight');plt.close(fig)


def plot_chart(con,cfg,out):
    sub=con.dropna(subset=['D_MeV','E_MeV']).copy();A=cfg['fc_A'];B=cfg['fc_B']
    fc_a=(sub.D_MeV<=A['D_max_MeV'])&(sub.E_MeV>=A['E_min_MeV'])
    fc_b_all=(sub.D_MeV<=B['D_max_MeV'])&(sub.E_MeV>=B['E_min_MeV'])
    fc_b=fc_b_all&~fc_a
    low=(sub.D_MeV<=A['D_max_MeV'])&~(fc_a|fc_b)
    other=~(fc_a|fc_b|low)
    fig,ax=plt.subplots(figsize=(6.2,4.5))
    ax.scatter(sub.loc[other,'N'],sub.loc[other,'Z'],s=28,marker='.',color='0.65',label='Other confirmation nuclei')
    ax.scatter(sub.loc[low,'N'],sub.loc[low,'Z'],s=40,marker='o',facecolors='none',edgecolors='#009E73',linewidths=1.1,label='Low spread, $E<1$ MeV')
    ax.scatter(sub.loc[fc_b,'N'],sub.loc[fc_b,'Z'],s=58,marker='X',color='#E69F00',label='False consensus (FC-B only)')
    ax.scatter(sub.loc[fc_a,'N'],sub.loc[fc_a,'Z'],s=72,marker='*',color='#D55E00',label='False consensus (FC-A)')
    for r in sub.loc[fc_b].itertuples():
        ax.annotate(f'{int(r.A)}{r.element}',(r.N,r.Z),xytext=(4,4),textcoords='offset points',fontsize=7)
    ax.set_xlabel('Neutron number $N$');ax.set_ylabel('Proton number $Z$');ax.set_title('Low-spread confirmation nuclei')
    ax.legend(frameon=False,fontsize=8);ax.grid(alpha=.15,lw=.5);fig.tight_layout();fig.savefig(out,bbox_inches='tight');plt.close(fig)


def plot_mass_s2n(dev,con,out):
    fig,ax=plt.subplots(figsize=(5.7,4.4))
    # one point per vintage/observable: Spearman rho with bootstrap-free point estimate; sample size in annotation
    xs=[1,2];labels=['Mass excess','$S_{2n}$']
    for vintage,df in [('development',dev),('confirmation',con)]:
        vals=[];ns=[]
        for dcol,ecol in [('D_MeV','E_MeV'),('D_S2n_MeV','E_S2n_MeV')]:
            n,r,p=safe_spearman(df[dcol],df[ecol]);vals.append(r);ns.append(n)
        ax.plot(xs,vals,marker=MARKERS[vintage],ls=LINESTYLES[vintage],color=COLORS[vintage],lw=1.5,label=vintage.capitalize())
        for x,y,n in zip(xs,vals,ns):
            if np.isfinite(y):ax.annotate(f'n={n}',(x,y),xytext=(4,5),textcoords='offset points',fontsize=7,color=COLORS[vintage])
    ax.axhline(0,color='0.45',lw=.8);ax.set_xticks(xs,labels);ax.set_xlim(.75,2.25);ax.set_ylabel('Spearman $\\rho(D,E)$')
    ax.set_title('Is disagreement equally informative for bulk and local observables?');ax.legend(frameon=False);ax.grid(alpha=.15,lw=.5);fig.tight_layout();fig.savefig(out,bbox_inches='tight');plt.close(fig)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();root=a.root
    cfg=json.loads((root/'stage2a_development/FROZEN_CONFIGURATION_PRE_CONFIRMATION.json').read_text())
    if not (root/'stage2b_confirmation/CONFIRMATION_COMPLETED.json').exists():raise RuntimeError('Locked confirmation must be completed before Stage 2C.')
    dev=pd.read_csv(root/'stage2a_development/DEVELOPMENT_SCORED.csv');con=pd.read_csv(root/'stage2b_confirmation/CONFIRMATION_SCORED_LOCKED.csv')
    out=root/'stage2c_analysis';out.mkdir(exist_ok=True);tables=root/'tables';figs=root/'figures';tables.mkdir(exist_ok=True);figs.mkdir(exist_ok=True)
    perf=performance_table(dev,con,cfg);perf.to_csv(tables/'Table2_Consensus_Performance.csv',index=False)
    qtab=pd.concat([quintile_table(dev,cfg,'development'),quintile_table(con,cfg,'confirmation')],ignore_index=True);qtab.to_csv(tables/'Table3_Consensus_Calibration_Quintiles.csv',index=False)
    ctab=pd.concat([condition_table(dev,cfg,'development'),condition_table(con,cfg,'confirmation')],ignore_index=True);ctab.to_csv(tables/'Table4_Conditional_False_Consensus.csv',index=False)
    s2=pd.concat([s2n_summary(dev,'development'),s2n_summary(con,'confirmation')],ignore_index=True);s2.to_csv(tables/'Table5_S2n_Consensus.csv',index=False)
    loo=pd.concat([loo_table(dev,'development'),loo_table(con,'confirmation')],ignore_index=True);loo.to_csv(tables/'TableS1_Leave_One_Model_Out.csv',index=False)
    signed_residuals(dev).to_csv(tables/'TableS2_Residual_Correlation_Development.csv')
    signed_residuals(con).to_csv(tables/'TableS3_Residual_Correlation_Confirmation.csv')
    plot_scatter(dev,con,cfg,figs/'Fig2_Consensus_Calibration_Scatter.pdf')
    plot_quintiles(qtab,figs/'Fig3_Consensus_Calibration_Quintiles.pdf')
    plot_chart(con,cfg,figs/'Fig4_False_Consensus_Nuclear_Chart.pdf')
    plot_mass_s2n(dev,con,figs/'Fig5_Mass_vs_S2n_Consensus_Information.pdf')
    summary={'performance_rows':len(perf),'calibration_rows':len(qtab),'condition_rows':len(ctab),'s2n_rows':len(s2),
             'figures':['Fig2_Consensus_Calibration_Scatter.pdf','Fig3_Consensus_Calibration_Quintiles.pdf','Fig4_False_Consensus_Nuclear_Chart.pdf','Fig5_Mass_vs_S2n_Consensus_Information.pdf']}
    (out/'STAGE2C_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
