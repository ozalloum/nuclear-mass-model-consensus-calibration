#!/usr/bin/env python3
import argparse,json
from pathlib import Path
import pandas as pd
from consensus_core import score_targets, development_freeze, apply_flags, summarize, sha256

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();root=a.root
 out=root/'stage2a_development';out.mkdir(parents=True,exist_ok=True)
 targets=pd.read_csv(root/'data/processed/TARGETS_DEVELOPMENT_AME2012_TO_2016.csv')
 scored=score_targets(targets,root/'data/standardized_models')
 complete=scored.D_MeV.notna().sum()
 if complete<20: raise RuntimeError(f'Only {complete} four-model complete development targets; gate requires >=20.')
 cfg=development_freeze(scored);scored=apply_flags(scored,cfg)
 scored.to_csv(out/'DEVELOPMENT_SCORED.csv',index=False)
 cfg['development_summary']=summarize(scored,cfg)
 cfg['development_target_sha256']=sha256(root/'data/processed/TARGETS_DEVELOPMENT_AME2012_TO_2016.csv')
 cfg['standardized_model_sha256']={m:sha256(root/'data/standardized_models'/f'{m}.csv') for m in cfg['models']}
 p=out/'FROZEN_CONFIGURATION_PRE_CONFIRMATION.json';p.write_text(json.dumps(cfg,indent=2),encoding='utf-8')
 (out/'FROZEN_CONFIGURATION_PRE_CONFIRMATION.sha256').write_text(sha256(p)+'  FROZEN_CONFIGURATION_PRE_CONFIRMATION.json\n')
 print(json.dumps(cfg['development_summary'],indent=2))
if __name__=='__main__':main()
