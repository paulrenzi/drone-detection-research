"""US customary presentation only; CAD, exports and machine reports keep SI units."""
import re

MM_PER_IN = 25.4
G_PER_OZ = 28.349523125
G_PER_LB = 453.59237
N_PER_LBF = 4.4482216152605
NM_PER_OZ_IN = 0.007061551814226043


def inch(mm, precision=None):
    value = float(mm) / MM_PER_IN
    digits = precision if precision is not None else (3 if abs(value) < .1 else 2)
    # Suppress negative zero caused by B-rep floating point tolerances.
    if abs(value) < .5 * 10 ** -digits:
        value = 0.
    return f'{value:.{digits}f}'


def length(mm, precision=None):
    return inch(mm, precision) + ' in'


def mass(g):
    g = float(g)
    return f'{g / G_PER_LB:.2f} lb' if abs(g) > G_PER_LB else f'{g / G_PER_OZ:.2f} oz'


def volume(mm3):
    value = float(mm3) / MM_PER_IN ** 3
    return f'{value:.6g} in³'


def density(g_cm3, source=True):
    return f'{float(g_cm3) * 16.387064 / G_PER_LB:.4f} lb/in³' + (f' ({g_cm3:g} g/cm³)' if source else '')


def pressure(mpa):
    return f'{float(mpa) * 145.03773773020923:.2f} psi'


def typography(text):
    # Repair the prior prose's joined words, without touching sold part names.
    text = re.sub(r'\b(now|than|the|preserves|to|separate|nominal|at|about|from|with|one|four|two|three|full|into|by|below|above|is|original|actual|all|use|per|includes|diameter|only|around|and|before|after|ends|begins|every|specified|retains|has|a|A|an|of|same|mic|hanger|Vyper|density|times|hidden|masses|mass|maximum|Conservative|module|IC|OD|breakout|envelope|strap|thickness|coefficient|bores|bridge|SKU|PCB)(?=[+-]?\d)', r'\1 ', text)
    text = re.sub(r'(?<=[a-wyz])(?=\d)', ' ', text)
    text = re.sub(r'\bx(?=\d)', 'x ', text)
    text = re.sub(r'(?<=[;:])(?=\d)|(?<=[A-Za-z]\.)(?=\d)', ' ', text)
    text = re.sub(r',(?=\S)', ', ', text)
    text = re.sub(r'(?<=\d)\s*(degrees?|deg)\b', r' \1', text)
    text = text.replace('flat-top18650', 'flat-top 18650').replace('Flat-top18650', 'Flat-top 18650')
    text = text.replace('printed18650', 'printed 18650').replace('same18650', 'same 18650')
    for a,b in [('onZ0','on Z0'), ('atZ0','at Z0'), ('withY up','with Y up'), ('andY up','and Y up'), ('positiveY','positive Y'), ('negativeY','negative Y'), ('inX','in X')]:
        text = text.replace(a,b)
    return text


_NUM = r'[+-]?\d+(?:\.\d+)?'
_SEQ = rf'{_NUM}(?:\s*(?:x|×|/|\.\.|–|\+/-|±|,|-)\s*{_NUM})*'


def us_text(text, quote_metric=False):
    """Convert legacy metric prose; quote originals only in the source register.

    Protect URLs, code, density references and the two prescribed slicer settings.
    Explicit model-unit declarations are added separately by the document writer.
    """
    saved = []
    seen = set()
    def keep(value):
        saved.append(value)
        return f'\ue000{len(saved)-1}\ue001'
    text = re.sub(r'```[\s\S]*?```|https?://[^\s)<>]+|`[^`\n]+`', lambda m: keep(m[0]), text)
    text = re.sub(r'[\d.]+ lb/in³ \([\d.]+ g/cm³\)', lambda m: keep(m[0]), text)
    text = re.sub(r'\b(mm|cm)([23])\b',lambda m:m[1]+{'2':'²','3':'³'}[m[2]],text)
    text = typography(text)
    text = re.sub(r'0\.4\s*mm\s+nozzle(?:\s*\(0\.016 in\))?', lambda m: keep('0.4 mm nozzle (0.016 in)'), text)
    text = re.sub(r'0\.20?\s*mm\s+layers(?:\s*\(0\.008 in\))?', lambda m: keep('0.20 mm layers (0.008 in)'), text)
    text = re.sub(r'('+_NUM+r')\s*g/cm[³3]', lambda m: keep(density(float(m[1]))), text)
    def sourced(us, original):
        original=re.sub(r'(?<=\d)\s*[x×]\s*(?=\d)',' x ',original.strip())
        original=re.sub(r'\s*\+/-\s*',' ± ',original)
        quote=quote_metric and original not in seen
        seen.add(original)
        return us + (f' ({original})' if quote else '')
    text = re.sub(r'('+_NUM+r')\s*kg\.cm\b', lambda m: sourced(f'{float(m[1]) * 9.80665 * .01 / NM_PER_OZ_IN:.2f} oz·in',m[0]), text)
    text = re.sub(r'('+_NUM+r')\s*N\b', lambda m: sourced(f'{float(m[1]) / N_PER_LBF:.2f} lbf',m[0]), text)
    text = re.sub(r'('+_NUM+r')\s*(?:°?C)\b', lambda m: f'{float(m[1])*1.8+32:.0f} °F', text)
    text = re.sub(r'('+_NUM+r')\s*mm[³3]\b', lambda m: volume(m[1]), text)
    def dims(m):
        seq=m[1]
        # Preserve three decimals for source envelopes, fits, films and thin walls.
        precise = quote_metric or bool(re.search(r'clearance|toleran|press land|bore|running gap|residual', text[max(0,m.start()-35):m.end()+40], re.I))
        converted=re.sub(_NUM, lambda n: inch(float(n[0]),3 if precise else None),seq)
        converted=re.sub(r'\s*[x×]\s*',' x ',converted)
        converted=re.sub(r'\s*(?:\+/-|±)\s*',' ± ',converted)
        converted=re.sub(r'\s*(?:\.\.|–|-)\s*(?=\d)','–',converted)
        return sourced(converted+' in',m[0])
    text = re.sub('('+_SEQ+r')\s*mm\b', dims, text)
    text = re.sub('('+_NUM+r')\s*g\b',lambda m:sourced(mass(m[1]),m[0]),text)
    text = re.sub('('+_NUM+r')\s*m\b',lambda m:sourced(length(float(m[1])*1000),m[0]),text)
    # Values inserted as references must not themselves be converted.
    text=re.sub(r'\ue000(\d+)\ue001',lambda m:saved[int(m[1])],text)
    return text.replace('an 0.', 'a 0.')


def write_checks_markdown(data, path):
    """Human check report from unchanged JSON; every dimensional field has units."""
    def value(key, v):
        if isinstance(v,(list,tuple)):
            return '['+', '.join(value(key,item) for item in v)+']'
        if isinstance(v,dict):
            return '{'+', '.join(k+': '+value(k,item) for k,item in v.items())+'}'
        if isinstance(v,bool):return str(v).lower()
        if v is None:return 'none'
        if isinstance(v,str):return us_text(v)
        if key.endswith('_mm3'):return volume(v)
        if key.endswith('_mm2'):return f'{v/MM_PER_IN**2:.6g} in²'
        if key.endswith('_mm'):return length(v,3)
        if key.endswith('_Nm'):return f'{v/NM_PER_OZ_IN:.2f} oz·in'
        if key.endswith('_N'):return f'{v/N_PER_LBF:.2f} lbf'
        if key.endswith('_MPa'):return pressure(v)
        if key.endswith('_g'):return mass(v)
        if key.endswith('_deg'):return f'{v:g} degrees'
        return f'{v:.9g}' if isinstance(v,float) else str(v)
    def label(key):
        return re.sub(r'_(?:mm3|mm2|mm|Nm|MPa|N|g|deg)$','',key).replace('_',' ')
    def name(key):
        key=re.sub(r'(stake_(?:cell_holder_)?range_)('+_NUM+r')$',lambda m:m[1]+length(m[2],3),key)
        key=re.sub(r'(BOOT_RESET_pin_access_)('+_NUM+r')$',lambda m:m[1]+length(m[2],3),key)
        key=re.sub(r'(stake_(?:clamp|cell)_tie_)('+_NUM+r')(_clearance)$',lambda m:m[1]+length(m[2])+m[3],key)
        return key.replace('_',' ')
    lines=['# Generated geometry checks — US customary display','',
           f"**{len(data['checks'])-len(data['failed'])}/{len(data['checks'])} checks pass.**",'',
           'Display values are converted from the current `checks.json` model values. Lengths use three decimal inches here to preserve clearance information; small areas and volumes retain significant digits. Values near zero can round to zero. Check names containing stock positions are also converted for display. The acceleration factor 3g means three times gravity.', '',
           data['clearance_distances'], '',
           'Discrete sampling: 0.5 degree contact; 2 degree rotor-neck; 0.197 in extraction; 5 degree prescribed pitch.', '',
           *['- '+us_text(item) for item in data['limitations']], '']
    for row in data['checks']:
        details='; '.join(label(k)+': '+value(k,v) for k,v in row.items() if k not in ('check','pass_'))
        lines.append(f"- {'PASS' if row['pass_'] else 'FAIL'}: {name(row['check'])} — {details}")
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
