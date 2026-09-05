from __future__ import annotations
import hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

MODELS=('FRDM2012','HFB27','DZ31','WS4')
DN_MEV=8.0713181

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def load_standard_model(path:Path, model:str)->pd.DataFrame:
    df=pd.read_csv(path)
    req={'N','Z','mass_excess_MeV'}
    if not req.issubset(df.columns): raise ValueError(f'{model}: missing {sorted(req-set(df.columns))}')
    df=df[['N','Z','mass_excess_MeV']].copy()
    df['N']=pd.to_numeric(df.N,errors='raise').astype(int);df['Z']=pd.to_numeric(df.Z,errors='raise').astype(int)
    df['mass_excess_MeV']=pd.to_numeric(df.mass_excess_MeV,errors='coerce')
    df=df.dropna().drop_duplicates(['N','Z'],keep=False)
    if (df.N<0).any() or (df.Z<0).any():raise ValueError(model+': negative N/Z')
    df['model']=model
    return df

def merge_models(targets:pd.DataFrame, model_dir:Path)->pd.DataFrame:
    out=targets.copy()
    for model in MODELS:
        p=model_dir/f'{model}.csv'
        if not p.exists(): raise FileNotFoundError(p)
        m=load_standard_model(p,model).rename(columns={'mass_excess_MeV':f'ME_{model}'})[['N','Z',f'ME_{model}']]
        out=out.merge(m,on=['N','Z'],how='left',validate='one_to_one')
    cols=[f'ME_{m}' for m in MODELS]
    out['n_models']=out[cols].notna().sum(axis=1)
    return out

def compute_s2n_for_models(model_dir:Path)->dict[str,dict[tuple[int,int],float]]:
    out={}
    for model in MODELS:
        df=load_standard_model(model_dir/f'{model}.csv',model)
        mp={(int(r.N),int(r.Z)):float(r.mass_excess_MeV) for r in df.itertuples()}
        s={}
        for (N,Z),me in mp.items():
            nb=mp.get((N-2,Z)); s[(N,Z)]=np.nan if nb is None else nb+2*DN_MEV-me
        out[model]=s
    return out

def score_targets(targets:pd.DataFrame, model_dir:Path)->pd.DataFrame:
    df=merge_models(targets,model_dir)
    cols=[f'ME_{m}' for m in MODELS]
    complete=df.n_models.eq(4)
    df['ME_consensus_mean']=df[cols].mean(axis=1)
    df['ME_consensus_median']=df[cols].median(axis=1)
    df['D_MeV']=df[cols].std(axis=1,ddof=1)
    df['E_MeV']=(df.ME_consensus_mean-df.mass_excess_MeV).abs()
    df['E_median_MeV']=(df.ME_consensus_median-df.mass_excess_MeV).abs()
    for m in MODELS:df[f'err_{m}_MeV']=(df[f'ME_{m}']-df.mass_excess_MeV).abs()
    s2maps=compute_s2n_for_models(model_dir)
    for m in MODELS: df[f'S2n_{m}_MeV']=[s2maps[m].get((int(n),int(z)),np.nan) for n,z in zip(df.N,df.Z)]
    s2cols=[f'S2n_{m}_MeV' for m in MODELS]
    df['S2n_n_models']=df[s2cols].notna().sum(axis=1)
    df['S2n_consensus_mean']=df[s2cols].mean(axis=1)
    df['D_S2n_MeV']=df[s2cols].std(axis=1,ddof=1)
    df['E_S2n_MeV']=(df.S2n_consensus_mean-pd.to_numeric(df.S2n_exp_MeV,errors='coerce')).abs()
    df.loc[~complete,['ME_consensus_mean','ME_consensus_median','D_MeV','E_MeV','E_median_MeV']]=np.nan
    df.loc[df.S2n_n_models.ne(4),['S2n_consensus_mean','D_S2n_MeV','E_S2n_MeV']]=np.nan
    return df

def boot_ci_stat(x,y,stat_fn,nboot=10000,seed=42):
    x=np.asarray(x,float);y=np.asarray(y,float);ok=np.isfinite(x)&np.isfinite(y);x=x[ok];y=y[ok]
    if len(x)<3:return [None,None]
    rng=np.random.default_rng(seed);vals=[]
    for _ in range(nboot):
        ii=rng.integers(0,len(x),len(x));
        try:vals.append(float(stat_fn(x[ii],y[ii])))
        except Exception:pass
    if not vals:return [None,None]
    return [float(np.quantile(vals,.025)),float(np.quantile(vals,.975))]

def spearman_summary(df):
    sub=df[['D_MeV','E_MeV']].dropna()
    if len(sub)<3:return {'n':len(sub),'rho':None,'p':None,'ci95':[None,None]}
    rho,p=spearmanr(sub.D_MeV,sub.E_MeV)
    ci=boot_ci_stat(sub.D_MeV.values,sub.E_MeV.values,lambda a,b:spearmanr(a,b).statistic)
    return {'n':len(sub),'rho':float(rho),'p':float(p),'ci95':ci}

def wilson(k,n,z=1.959963984540054):
    if n==0:return [None,None]
    p=k/n;den=1+z*z/n;c=(p+z*z/(2*n))/den;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [max(0,c-h),min(1,c+h)]

def strictly_increasing_edges(values):
    """Return bin edges with deterministic one-ULP tie separation."""
    edges=np.asarray(values,float).copy()
    for i in range(1,len(edges)):
        if edges[i]<=edges[i-1]:
            edges[i]=np.nextafter(edges[i-1],np.inf)
    return edges

def development_freeze(scored:pd.DataFrame)->dict:
    sub=scored.dropna(subset=['D_MeV','E_MeV']).copy()
    q25D=float(sub.D_MeV.quantile(.25));q75E=float(sub.E_MeV.quantile(.75))
    edges=strictly_increasing_edges(np.quantile(sub.D_MeV,[0,.2,.4,.6,.8,1.0]))
    d2edges=strictly_increasing_edges(np.quantile(sub.d2_nearest_prior_primary,[0,1/3,2/3,1]))
    iedges=strictly_increasing_edges(np.quantile(sub.isospin_asymmetry,[0,1/3,2/3,1]))
    return {'models':list(MODELS),'consensus':'arithmetic_mean','spread':'sample_sd_ddof1',
            'fc_A':{'D_max_MeV':0.25,'E_min_MeV':1.0},
            'fc_B':{'D_max_MeV':q25D,'E_min_MeV':q75E},
            'D_quintile_edges_MeV':edges.tolist(),'extrapolation_d2_tercile_edges':d2edges.tolist(),
            'isospin_tercile_edges':iedges.tolist(),'bootstrap_n':10000,'seed':42}

def apply_flags(df,cfg):
    out=df.copy();A=cfg['fc_A'];B=cfg['fc_B']
    out['false_consensus_A']=((out.D_MeV<=A['D_max_MeV'])&(out.E_MeV>=A['E_min_MeV'])).astype('Int64')
    out['false_consensus_B']=((out.D_MeV<=B['D_max_MeV'])&(out.E_MeV>=B['E_min_MeV'])).astype('Int64')
    return out

def summarize(df,cfg):
    sub=df.dropna(subset=['D_MeV','E_MeV']).copy();out={'n_complete':len(sub),'spearman':spearman_summary(sub)}
    A=cfg['fc_A'];B=cfg['fc_B']
    for name,r in [('A',A),('B',B)]:
        f=(sub.D_MeV<=r['D_max_MeV'])&(sub.E_MeV>=r['E_min_MeV']);k=int(f.sum());n=len(sub)
        out[f'fc_{name}']={'n':k,'denom':n,'prevalence':k/n if n else None,'wilson95':wilson(k,n)}
    low=sub[sub.D_MeV<=A['D_max_MeV']];k=int((low.E_MeV>=A['E_min_MeV']).sum())
    out['low_spread_failure_rate']={'n_low_spread':len(low),'n_fail':k,'rate':k/len(low) if len(low) else None,'wilson95':wilson(k,len(low))}
    # model sanity
    out['model_MAE_MeV']={m:float(sub[f'err_{m}_MeV'].mean()) for m in MODELS}
    out['consensus_MAE_MeV']=float(sub.E_MeV.mean()) if len(sub) else None
    out['consensus_median_MAE_MeV']=float(sub.E_median_MeV.mean()) if len(sub) else None
    return out
