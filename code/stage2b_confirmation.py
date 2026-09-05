#!/usr/bin/env python3
import argparse,json,datetime
from pathlib import Path
import pandas as pd
from consensus_core import score_targets, apply_flags, summarize, sha256

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args();root=a.root
 dev=root/'stage2a_development/FROZEN_CONFIGURATION_PRE_CONFIRMATION.json';hashp=root/'stage2a_development/FROZEN_CONFIGURATION_PRE_CONFIRMATION.sha256'
 if not dev.exists() or not hashp.exists():raise RuntimeError('Development freeze is required before confirmation.')
 stored=hashp.read_text().split()[0]
 if sha256(dev)!=stored:raise RuntimeError('Development freeze hash mismatch.')
 out=root/'stage2b_confirmation';out.mkdir(parents=True,exist_ok=True);lock=out/'CONFIRMATION_COMPLETED.json'
 if lock.exists():raise RuntimeError('CONFIRMATION ALREADY SCORED. Refusing second scoring in the same run directory.')
 cfg=json.loads(dev.read_text())
 # Ensure exact model bytes have not changed since development.
 for m,h in cfg['standardized_model_sha256'].items():
  p=root/'data/standardized_models'/f'{m}.csv'
  if sha256(p)!=h:raise RuntimeError(f'Model table changed after development freeze: {m}')
 targets=pd.read_csv(root/'data/processed/TARGETS_CONFIRMATION_AME2016_TO_2020_LOCKED.csv')
 scored=apply_flags(score_targets(targets,root/'data/standardized_models'),cfg)
 complete=int(scored.D_MeV.notna().sum())
 if complete<25:raise RuntimeError(f'Only {complete} four-model complete confirmation targets; gate requires >=25.')
 scored.to_csv(out/'CONFIRMATION_SCORED_LOCKED.csv',index=False)
 summary=summarize(scored,cfg)
 (out/'CONFIRMATION_RESULTS_LOCKED.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
 payload={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'configuration_sha256':stored,
          'confirmation_target_sha256':sha256(root/'data/processed/TARGETS_CONFIRMATION_AME2016_TO_2020_LOCKED.csv'),
          'scored_sha256':sha256(out/'CONFIRMATION_SCORED_LOCKED.csv'),'n_complete':complete}
 lock.write_text(json.dumps(payload,indent=2),encoding='utf-8')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
