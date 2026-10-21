"""Refresh derived mass tables/kit quantities from an already verified cache."""
import sys,json
sys.dont_write_bytecode=True
from build import load_cache,mass_report,OUT
p=load_cache();m=mass_report(p)
from variants import write_kit_manifest
write_kit_manifest()
print('Mass reports refreshed; dart',m['dart_total_g'],'stake',m['stake']['total_g'],'g')
