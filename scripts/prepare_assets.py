"""Create vector poster figures with Python's standard library and XeLaTeX.

All numeric values are transcribed from the user's v2 paper. No data are inferred.
The chart sources use the same Fira font as the poster.
"""
from pathlib import Path
import json
import subprocess
import os

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'race'
OUT.mkdir(parents=True, exist_ok=True)
os.environ['TEXMFVAR'] = str(ROOT / 'tmp' / 'tex-cache')

# The checked-in manifest is the source of truth for the reported results.
data = json.loads((OUT / 'reported_data.json').read_text(encoding='utf-8'))

PREAMBLE = r'''\documentclass[border=5pt]{standalone}
\usepackage{fontspec,graphicx,tikz}
\setmainfont{FiraSans-Regular.otf}[BoldFont=FiraSans-Bold.otf]
\definecolor{ink}{HTML}{0E3B38}
\definecolor{pgreen}{HTML}{446F4E}
\definecolor{firered}{HTML}{D12632}
\definecolor{gray}{HTML}{CFE3E1}
\definecolor{grid}{HTML}{E1EEED}
\begin{document}\color{ink}
\begin{tikzpicture}[x=1cm,y=.65cm,every node/.style={font=\fontsize{18}{22}\selectfont}]
'''

def node(x,y,text,anchor='center',color='ink',size=18,bold=False):
    font = r'\fontsize{' + str(size) + '}{' + str(size+4) + r'}\selectfont' + (r'\bfseries' if bold else '')
    return rf'\node[anchor={anchor},text={color},font={font}] at ({x:.3f},{y:.3f}) {{{text}}};'+'\n'

def rect(x1,y1,x2,y2,color):
    return rf'\path[fill={color}] ({x1:.3f},{y1:.3f}) rectangle ({x2:.3f},{y2:.3f});'+'\n'

def legend(x,y,color,text):
    return rect(x,y-.14,x+.6,y+.14,color)+node(x+.8,y,text,'west',size=17)

def horizontal_grid(ymin,ymax,xmax,ticks):
    s=''
    for tick in ticks:
        x=tick/xmax*20+6
        s+=rf'\draw[grid] ({x:.3f},{ymin}) -- ({x:.3f},{ymax});'+'\n'
        s+=node(x,ymin-.35,str(tick),'north',size=16)
    return s

def compile_asset(name, drawing, preamble=PREAMBLE):
    source=OUT/f'{name}.tex'
    source.write_text(preamble+drawing+r'\end{tikzpicture}\end{document}',encoding='utf-8')
    result=subprocess.run(['xelatex','--disable-installer','--interaction=nonstopmode',
                          '--halt-on-error',f'--output-directory={OUT}',str(source)],
                         cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,
                         encoding='utf-8',errors='replace')
    if result.returncode:
        print(result.stdout[-5000:]);raise RuntimeError(f'Failed to compile {name}')
    print(f'Compiled {name}.pdf',flush=True)

d=data['qwen_code_rsf_mlp']
s=horizontal_grid(0,9.5,100,[0,25,50,75,100])
s+=legend(6,10.3,'gray','Original model')+legend(14,10.3,'firered','RACE + RSF suppression')
for i,(name,a,b) in enumerate(zip(d['benchmarks'],d['baseline'],d['race'])):
    y=8.8-i*1.5
    s+=node(5.65,y,name,'east','firered' if i<2 else 'ink',bold=i<2)
    s+=rect(6,y+.06,6+.2*a,y+.55,'gray')+rect(6,y-.55,6+.2*b,y-.06,'firered')
    s+=node(6+.2*a+.1,y+.30,f'{a:.2f}','west',size=14)
    s+=node(6+.2*b+.1,y-.30,f'{b:.2f}','west','firered',14,True)
s+=node(16,-1.95,r'Benchmark accuracy (\%)',size=19)
compile_asset('code_accuracy',s)

d=data['isi_mlp'];s=''
for v in [0,1,2,3]:
    y=v*2.1
    s+=rf'\draw[grid] (1,{y}) -- (27,{y});'+'\n'+node(.75,y,str(v),'east',size=16)
for i,(name,a,b) in enumerate(zip(d['methods'],d['code'],d['math'])):
    x=2.5+i*3.75
    s+=rect(x-.95,0,x-.08,a*2.1,'pgreen')+rect(x+.08,0,x+.95,b*2.1,'firered')
    s+=node(x-.6,a*2.1+.18,f'{a:.2f}','south',size=14)
    s+=node(x+.6,b*2.1+.18,f'{b:.2f}','south',size=14)
    s+=node(x,-.2,name,'north',size=16,bold=name=='RACE')
s+=legend(4,7.05,'pgreen','Code target')+legend(14,7.05,'firered','Math target')
s+=node(14,-1.95,'Intervention Specificity Index (ISI); higher is better',size=17)
compile_asset('isi',s)

d=data['distribution_mlp'];s=''
for v in [0,50,100,150]:
    y=v*.052
    s+=rf'\draw[grid] (1,{y:.3f}) -- (27,{y:.3f});'+'\n'+node(.7,y,str(v),'east',size=16)
for i,(name,a,b) in enumerate(zip(d['corpora'],d['code_rsf_delta_ppl'],d['math_rsf_delta_ppl'])):
    x=5+i*9
    s+=rect(x-1.95,0,x-.12,a*.052,'pgreen')+rect(x+.12,0,x+1.95,b*.052,'firered')
    s+=node(x-1.55,a*.052+.18,rf'+{a:.2f}\%','south',size=17,bold=True)
    s+=node(x+1.55,b*.052+.18,rf'+{b:.2f}\%','south',size=17,bold=True)
    s+=node(x,-.3,name,'north',size=19)
s+=legend(3,8.8,'pgreen','Code-selected neurons')+legend(15,8.8,'firered','Math-selected neurons')
s+=node(14,-1.95,r'Relative perplexity increase (\%)',size=19)
compile_asset('distribution',s)

d=data['comprehensions'];s=horizontal_grid(0,3.8,60,[0,20,40,60])
s+=legend(6,4.65,'gray','Original model')+legend(15,4.65,'firered','PyComp-1K + RSF')
for i,(name,a,b) in enumerate(zip(d['benchmarks'],d['baseline_records'],d['pycomp_records'])):
    y=3-i*2
    s+=node(5.6,y,name,'east',size=19)
    s+=rect(6,y+.04,6+a/3,y+.66,'gray')+rect(6,y-.66,6+b/3,y-.04,'firered')
    s+=node(6+a/3+.15,y+.35,str(a),'west',size=18)
    s+=node(6+b/3+.15,y-.35,rf'{b}  ({(b/a-1)*100:.1f}\%)','west','firered',19,True)
s+=node(16,-1.95,'Outputs containing a Python comprehension',size=17)
compile_asset('comprehensions',s)

s=horizontal_grid(0,5.6,150,[0,50,100,150])
for i,(name,v) in enumerate(zip(['GxAct','AttnLRP','RDA'],[144.29,144.62,.63])):
    y=4.7-i*1.8
    s+=node(5.6,y,name,'east',size=20,bold=i==2)
    s+=rect(6,y-.4,6+v/7.5,y+.4,'pgreen' if i==2 else 'gray')
    s+=node(6+v/7.5+.15,y,rf'{v:.2f}$\times$','west','pgreen' if i==2 else 'ink',19,True)
s+=node(16,-1.95,'Extra scoring FLOPs / forward-inference FLOPs',size=17)
compile_asset('scoring_cost',s)

paper_path=str(Path(data['source'])).replace('\\','/')
compile_asset('rda_overview',r'\node[inner sep=0pt] {\includegraphics[page=1,trim=304bp 446.89bp 71.276bp 218bp,clip]{'+paper_path+'}};')
# Re-emit the clipped figure so hidden text from the rest of the source page
# does not pollute text extraction from the finished poster.
clean_pdf=ROOT/'tmp'/'pdfs'/'rda_clean.pdf'
subprocess.run(['pdftocairo','-pdf',str(OUT/'rda_overview.pdf'),str(clean_pdf)],check=True)
clean_pdf.replace(OUT/'rda_overview.pdf')
print('All vector assets and source data are ready.')
