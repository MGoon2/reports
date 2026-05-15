#!/usr/bin/env python3
from __future__ import annotations
import csv, html, json, os, re, subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path('/mnt/c/Dev')
BASE=Path('/mnt/c/reports/code-research/api-endpoint')
DETAIL=BASE/'finup_endpoint_usage_detail.csv'
OUT_CSV=BASE/'finup_endpoint_second_level_usage.csv'
OUT_MD=BASE/'finup_endpoint_second_level_usage_report.md'
OUT_HTML=BASE/'finup_endpoint_second_level_usage_report.html'
OUT_JSON=BASE/'finup_endpoint_second_level_usage_summary.json'
PATTERNS=BASE/'finup_endpoint_second_level_methods.patterns'
TARGETS=['Finup.Chat.NET.Blazor.Core','FinUp.Finance','FinUp.General','FinUp.Stock']
RG=os.environ.get('RG','rg')
EXT_GLOBS=['*.cs','*.cshtml','*.razor','*.aspx','*.ascx','*.asmx','*.ashx','*.js','*.ts','*.config','*.json','*.xml']
SKIP_GLOBS=['!**/bin/**','!**/obj/**','!**/packages/**','!**/node_modules/**','!**/.git/**','!**/.vs/**','!**/dist/**','!**/build/**','!**/.omx/**']
API_RE=re.compile(r'(^|\.)Api($|\.)', re.I)
UNIT_RE=re.compile(r'UnitTest', re.I)
FINUP_RE=re.compile(r'^finup[\w.\-]*$', re.I)
CONTROL={'if','for','foreach','while','switch','catch','using','lock','return','new','throw'}
CS_CLASS_RE=re.compile(r'\b(?:public|private|protected|internal|sealed|abstract|static|partial\s+)*\s*(?:class|struct|interface|record)\s+(\w+)', re.I)
CS_METHOD_RE=re.compile(r'''^\s*(?:\[[^\]]+\]\s*)*(?:(?:public|private|protected|internal|static|async|override|virtual|sealed|partial|extern|new)\s+)*\s*(?:[\w<>,\[\]\.?]+\s+)+(\w+)\s*\([^;]*\)\s*(?:\{|$|where\b)''', re.X)
CS_CTOR_RE=re.compile(r'^\s*(?:(?:public|private|protected|internal)\s+)?(\w+)\s*\([^;]*\)\s*(?:\{|$)')

@dataclass
class TargetMethod:
    target_project:str
    target_class:str
    method:str
    file:str
    line:str
    endpoints:set[str]=field(default_factory=set)
    endpoint_defs:set[str]=field(default_factory=set)
    source_rows:int=0


def read_text(path:Path)->str:
    for enc in ('utf-8-sig','utf-8','cp949','euc-kr','latin-1'):
        try: return path.read_text(encoding=enc,errors='strict')
        except UnicodeDecodeError: continue
        except OSError: return ''
    return path.read_text(encoding='utf-8',errors='ignore')

def rel(p:Path)->str:
    try: return str(p.relative_to(ROOT)).replace('\\','/')
    except Exception: return str(p).replace('\\','/')

def discover_projects():
    projects={}; dir_to_project={}
    for top in ROOT.iterdir():
        if not top.is_dir() or not FINUP_RE.match(top.name): continue
        for cs in top.glob('*.csproj'):
            name=cs.stem
            projects[name]={'name':name,'dir':top,'csproj':cs,'is_api':bool(API_RE.search(name)),'is_unit':bool(UNIT_RE.search(name))}
            dir_to_project[str(top.resolve())]=name
            break
    return projects, dir_to_project

def project_for(path:Path, dir_to_project):
    rp=str(path.resolve()); best=('', '')
    for ds,name in dir_to_project.items():
        if rp==ds or rp.startswith(ds+'/'):
            if len(ds)>len(best[0]): best=(ds,name)
    return best[1]

def project_refs(projects):
    refs=defaultdict(set)
    for name,rec in projects.items():
        txt=read_text(rec['csproj']).lower()
        for target in TARGETS:
            if target.lower() in txt:
                refs[name].add(target)
    return refs

def parse_method_line(s):
    m=re.match(r'(.+?) \((.+):(\d+)\)$', s or '')
    if not m: return (s or '', '', '')
    return m.group(1), m.group(2), m.group(3)

def load_target_methods():
    rows=list(csv.DictReader(DETAIL.open(encoding='utf-8-sig')))
    methods={}
    for r in rows:
        if r.get('사용 프로젝트 명') not in TARGETS or r.get('매칭 유형')=='unused': continue
        method,file,line=parse_method_line(r.get('메소드(라인)',''))
        if not method or method.startswith('설정/') or method.startswith('View/') or method.startswith('메소드 식별'): continue
        key=(r['사용 프로젝트 명'], r.get('클래스',''), method, file, line)
        tm=methods.setdefault(key, TargetMethod(r['사용 프로젝트 명'], r.get('클래스',''), method, file, line))
        tm.endpoints.add(r.get('엔드포인트 URL',''))
        tm.endpoint_defs.add(f"{r.get('HTTP','')} {r.get('엔드포인트 클래스','')}.{r.get('엔드포인트 메소드','')}")
        tm.source_rows+=1
    return list(methods.values())

def rg_search(paths, method_names):
    # Regex keeps method call/declaration candidates small.
    pattern=r'\b('+'|'.join(re.escape(m) for m in sorted(method_names, key=len, reverse=True))+r')\s*\('
    PATTERNS.write_text(pattern,encoding='utf-8')
    cmd=[RG,'--no-heading','--line-number','--pcre2','-e',pattern]
    for g in EXT_GLOBS: cmd += ['-g',g]
    for g in SKIP_GLOBS: cmd += ['-g',g]
    cmd += [str(p) for p in paths]
    proc=subprocess.run(cmd,cwd=str(ROOT),text=True,capture_output=True)
    if proc.returncode not in (0,1): raise RuntimeError(proc.stderr[:4000])
    out=[]
    for line in proc.stdout.splitlines():
        try:
            f,ln,content=line.split(':',2); out.append((Path(f),int(ln),content))
        except ValueError: pass
    return out

_line_cache={}
def get_lines(path):
    if path not in _line_cache: _line_cache[path]=read_text(path).splitlines()
    return _line_cache[path]

def find_scope(lines,idx,path):
    klass=''; method=''; start=max(0,idx-220); ext=path.suffix.lower()
    for j in range(idx,start-1,-1):
        line=lines[j]
        if ext=='.cs' and not method:
            m=CS_METHOD_RE.match(line)
            if m and m.group(1) not in CONTROL: method=m.group(1)
            else:
                cm=CS_CTOR_RE.match(line)
                if cm and cm.group(1) not in CONTROL: method=cm.group(1)
        if ext=='.cs' and not klass:
            c=CS_CLASS_RE.search(line)
            if c: klass=c.group(1)
        if klass and method: break
    if not klass: klass='View/Markup' if ext in {'.aspx','.ascx','.cshtml','.razor'} else path.stem
    if not method: method='View/Markup 영역' if ext in {'.aspx','.ascx','.cshtml','.razor'} else '메소드 식별 필요'
    return klass,method

def is_definition_line(line, method):
    stripped=line.strip()
    if stripped.startswith('//'): return True
    if re.search(r'\b(class|interface|delegate)\b', stripped): return True
    if re.match(r'^(public|private|protected|internal|static|async|override|virtual|sealed|partial|new|extern|\s)+', stripped) and re.search(r'\b'+re.escape(method)+r'\s*\(', stripped):
        return True
    return False

def confidence_for(line, caller_project, tm, refs):
    low=line.lower()
    full_class=(tm.target_class or '').lower()
    method_call=bool(re.search(r'\b'+re.escape(tm.method)+r'\s*\(', line))
    full_class_present=bool(full_class and re.search(r'(?<![\w.])'+re.escape(full_class)+r'(?!\w)', low))
    # If the source line explicitly qualifies a ChatApi-like class with a different namespace
    # (e.g. FUApi.ChatApi vs SPApi.ChatApi), do not connect it to the wrong target.
    qualified_chatapi=re.search(r'\b\w+\.chatapi\b', low)
    if qualified_chatapi and full_class.endswith('.chatapi') and not full_class_present:
        return None, '명시된 ChatApi 네임스페이스가 대상 클래스와 다름'
    if full_class_present and method_call:
        return 'High','동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재'
    if tm.target_project in refs.get(caller_project,set()):
        return 'Medium','caller 프로젝트가 target 프로젝트를 참조하고 메소드명이 호출됨'
    if full_class_present or tm.target_project.lower() in low:
        return 'Low','대상 클래스/프로젝트 문자열과 메소드명 호출 후보가 함께 존재'
    return None,'프로젝트 참조/대상 클래스 근거 없는 동명이 메소드 후보 제외'

def main():
    projects,dir_to_project=discover_projects(); refs=project_refs(projects); methods=load_target_methods(); method_names={m.method for m in methods}
    target_dirs={m.target_project: projects[m.target_project]['dir'] for m in methods if m.target_project in projects}
    search_paths=[rec['dir'] for name,rec in projects.items() if not rec['is_api'] and not rec['is_unit']]
    rg_hits=rg_search(search_paths, method_names)
    by_method=defaultdict(list)
    for tm in methods: by_method[tm.method].append(tm)
    results=[]; seen=set()
    for path,line_no,line in rg_hits:
        caller_project=project_for(path,dir_to_project)
        if not caller_project or caller_project not in projects: continue
        if projects[caller_project]['is_api'] or projects[caller_project]['is_unit']: continue
        line_methods=[m for m in method_names if re.search(r'\b'+re.escape(m)+r'\s*\(', line)]
        if not line_methods: continue
        lines=get_lines(path)
        for meth in line_methods:
            if is_definition_line(line,meth): continue
            for tm in by_method[meth]:
                if caller_project==tm.target_project: continue
                # avoid same physical target file/dir self hits
                if str(path.resolve()).startswith(str(target_dirs.get(tm.target_project,Path('/__none__')).resolve())+'/'): continue
                conf,reason=confidence_for(line,caller_project,tm,refs)
                if conf is None:
                    continue
                if path.suffix.lower() in {'.js','.ts','.jsx','.tsx'} and conf == 'Medium':
                    # A JS function with the same name is not evidence of a C# target method call.
                    continue
                klass,caller_method=find_scope(lines,max(0,line_no-1),path)
                key=(tm.target_project,tm.target_class,tm.method,caller_project,rel(path),line_no)
                if key in seen: continue
                seen.add(key)
                results.append({
                    '대상 사용 프로젝트':tm.target_project,
                    'Endpoint 호출 클래스':tm.target_class,
                    'Endpoint 호출 메소드':tm.method,
                    'Endpoint 호출 메소드 위치':f"{tm.file}:{tm.line}",
                    '호출 Endpoint 목록':' | '.join(sorted(tm.endpoints)),
                    'Endpoint 정의 목록':' | '.join(sorted(tm.endpoint_defs)),
                    '외부 호출 프로젝트':caller_project,
                    '외부 호출 클래스':klass,
                    '외부 호출 메소드(라인)':f"{caller_method} ({rel(path)}:{line_no})",
                    '외부 호출 파일':rel(path),
                    '외부 호출 라인':line_no,
                    '호출 소스 라인':line.strip(),
                    '프로젝트 참조 근거':'ProjectReference/Reference' if tm.target_project in refs.get(caller_project,set()) else '',
                    '신뢰도':conf,
                    '분석':reason,
                })
    # Add uncovered target methods.
    covered={(r['대상 사용 프로젝트'],r['Endpoint 호출 클래스'],r['Endpoint 호출 메소드'],r['Endpoint 호출 메소드 위치']) for r in results}
    for tm in methods:
        key=(tm.target_project,tm.target_class,tm.method,f"{tm.file}:{tm.line}")
        if key not in covered:
            results.append({
                '대상 사용 프로젝트':tm.target_project,'Endpoint 호출 클래스':tm.target_class,'Endpoint 호출 메소드':tm.method,'Endpoint 호출 메소드 위치':f"{tm.file}:{tm.line}",
                '호출 Endpoint 목록':' | '.join(sorted(tm.endpoints)),'Endpoint 정의 목록':' | '.join(sorted(tm.endpoint_defs)),
                '외부 호출 프로젝트':'정적 외부 호출 없음','외부 호출 클래스':'','외부 호출 메소드(라인)':'','외부 호출 파일':'','외부 호출 라인':'','호출 소스 라인':'','프로젝트 참조 근거':'','신뢰도':'N/A','분석':'대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.'
            })
    fields=['대상 사용 프로젝트','Endpoint 호출 클래스','Endpoint 호출 메소드','Endpoint 호출 메소드 위치','호출 Endpoint 목록','Endpoint 정의 목록','외부 호출 프로젝트','외부 호출 클래스','외부 호출 메소드(라인)','외부 호출 파일','외부 호출 라인','호출 소스 라인','프로젝트 참조 근거','신뢰도','분석']
    results=sorted(results,key=lambda r:(r['대상 사용 프로젝트'],r['Endpoint 호출 클래스'],r['Endpoint 호출 메소드'],r['외부 호출 프로젝트'],str(r['외부 호출 파일']),str(r['외부 호출 라인'])))
    with OUT_CSV.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(results)
    summary={
        'generated_at':datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds'),
        'targets':TARGETS,
        'target_endpoint_call_methods':len(methods),
        'external_call_rows':sum(1 for r in results if r['외부 호출 프로젝트']!='정적 외부 호출 없음'),
        'uncovered_target_methods':sum(1 for r in results if r['외부 호출 프로젝트']=='정적 외부 호출 없음'),
        'by_target_project':Counter(r['대상 사용 프로젝트'] for r in results if r['외부 호출 프로젝트']!='정적 외부 호출 없음'),
        'by_external_project':Counter(r['외부 호출 프로젝트'] for r in results if r['외부 호출 프로젝트']!='정적 외부 호출 없음'),
        'by_confidence':Counter(r['신뢰도'] for r in results),
        'project_references':{k:sorted(v) for k,v in refs.items() if v.intersection(TARGETS)},
        'outputs':{'csv':str(OUT_CSV),'markdown':str(OUT_MD),'html':str(OUT_HTML)}
    }
    # json can't serialize Counter
    summary['by_target_project']=dict(summary['by_target_project']); summary['by_external_project']=dict(summary['by_external_project']); summary['by_confidence']=dict(summary['by_confidence'])
    OUT_JSON.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    def md(s): return str(s).replace('|','\\|').replace('\n',' ')
    lines=['# FinUp Endpoint 사용 메소드 2차 호출 연결 분석','',f"- 생성시각: `{summary['generated_at']}`",f"- 기준 1차 CSV: `{DETAIL}`",f"- 대상 프로젝트: `{', '.join(TARGETS)}`",'- 제외: `.Api` 프로젝트, `UnitTest` 프로젝트, 대상 프로젝트 내부 self-call','- 매칭: endpoint 호출 메소드명 정적 호출 검색 + ProjectReference/대상 클래스명 근거로 신뢰도 부여','','## 요약','','|항목|값|','|---|---:|',f"|Endpoint 호출 메소드|{summary['target_endpoint_call_methods']}|",f"|외부 호출 연결 row|{summary['external_call_rows']}|",f"|외부 호출 미발견 메소드|{summary['uncovered_target_methods']}|",'','## 대상 프로젝트별 외부 호출 연결 수','','|대상 프로젝트|연결 수|','|---|---:|']
    for k,v in summary['by_target_project'].items(): lines.append(f"|{md(k)}|{v}|")
    lines += ['','## 외부 호출 프로젝트별 연결 수','','|외부 호출 프로젝트|연결 수|','|---|---:|']
    for k,v in sorted(summary['by_external_project'].items(), key=lambda x:(-x[1],x[0])): lines.append(f"|{md(k)}|{v}|")
    lines += ['','## 상세 연결 표','','|대상 사용 프로젝트|Endpoint 호출 클래스|Endpoint 호출 메소드|Endpoint 호출 메소드 위치|호출 Endpoint 목록|외부 호출 프로젝트|외부 호출 클래스|외부 호출 메소드(라인)|신뢰도|분석|','|---|---|---|---|---|---|---|---|---|---|']
    for r in results[:500]:
        lines.append('|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|'.format(md(r['대상 사용 프로젝트']),md(r['Endpoint 호출 클래스']),md(r['Endpoint 호출 메소드']),md(r['Endpoint 호출 메소드 위치']),md(r['호출 Endpoint 목록']),md(r['외부 호출 프로젝트']),md(r['외부 호출 클래스']),md(r['외부 호출 메소드(라인)']),md(r['신뢰도']),md(r['분석'])))
    OUT_MD.write_text('\n'.join(lines),encoding='utf-8')
    cards=''.join(f"<article class='metric'><span>{html.escape(k)}</span><strong>{v}</strong></article>" for k,v in [('Methods',summary['target_endpoint_call_methods']),('External links',summary['external_call_rows']),('Uncovered',summary['uncovered_target_methods']),('Rows',len(results))])
    target_cards=''.join(f"<article class='api-card'><span>{html.escape(k)}</span><strong>{v}</strong></article>" for k,v in sorted(summary['by_target_project'].items()))
    trs=[]
    for i,r in enumerate(results,1):
        cls='none' if r['외부 호출 프로젝트']=='정적 외부 호출 없음' else ('high' if r['신뢰도']=='High' else 'medium')
        trs.append('<tr class="{}"><td>{}</td>{}</tr>'.format(cls,i,''.join(f'<td>{html.escape(str(r[c]))}</td>' for c in ['대상 사용 프로젝트','Endpoint 호출 클래스','Endpoint 호출 메소드','호출 Endpoint 목록','외부 호출 프로젝트','외부 호출 클래스','외부 호출 메소드(라인)','신뢰도','분석'])))
    html_doc=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>FinUp Endpoint 2차 호출 분석</title><style>:root{{--primary:#fcd535;--primary-active:#f0b90b;--ink:#181a20;--muted:#707a8a;--line:#eaecef;--canvas:#fff;--soft:#fafafa;--dark:#0b0e11;--up:#0ecb81;--down:#f6465d;--info:#3b82f6}}*{{box-sizing:border-box}}body{{margin:0;background:var(--canvas);color:var(--ink);font-family:BinanceNova,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}.topbar{{height:10px;background:repeating-linear-gradient(135deg,var(--primary) 0 18px,var(--primary-active) 18px 36px,var(--dark) 36px 54px)}}.hero{{padding:64px 56px 46px;background:linear-gradient(135deg,#0b0e11 0%,#181a20 58%,#2b3139 100%);color:#fff}}.pill{{display:inline-flex;background:var(--primary);color:var(--ink);border-radius:6px;padding:12px 24px;font-weight:800}}h1{{font-size:52px;line-height:1.1;margin:24px 0 14px}}.meta{{max-width:1120px;color:#eaecef;line-height:1.65}}.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;padding:28px 56px;background:var(--soft);border-bottom:1px solid var(--line)}}.metric,.api-card{{padding:18px 20px;background:#fff;border:1px solid var(--line);border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:14px;box-shadow:0 6px 18px rgba(24,26,32,.04)}}.metric span,.api-card span{{color:var(--muted);font-size:12px;font-weight:800;text-transform:uppercase}}.metric strong,.api-card strong{{font-family:BinancePlex,ui-monospace,monospace;font-size:30px}}main{{padding:34px 56px 64px}}.panel{{margin:0 0 24px;padding:24px;border:1px solid var(--line);border-radius:10px;background:#fff;box-shadow:0 12px 28px rgba(24,26,32,.05)}}h2{{margin:0 0 14px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}.toolbar{{display:flex;gap:10px;align-items:center;margin:0 0 14px}}input{{height:38px;min-width:380px;border:1px solid var(--line);border-radius:6px;padding:0 12px}}a.btn{{display:inline-flex;align-items:center;height:38px;padding:0 16px;border-radius:6px;background:var(--primary);color:var(--ink);font-weight:800;text-decoration:none}}.table-wrap{{border:1px solid var(--line);border-radius:8px;background:#fff;box-shadow:0 12px 28px rgba(24,26,32,.06)}}table{{width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;font-size:12px}}th,td{{padding:11px 10px;border-bottom:1px solid var(--line);vertical-align:top;word-break:break-word}}th{{background:#fafafa;color:var(--muted);text-align:left;font-weight:800}}tr.high td:first-child{{border-left:3px solid var(--up)}}tr.medium td:first-child{{border-left:3px solid var(--primary)}}tr.none td:first-child{{border-left:3px solid var(--down)}}tbody tr:nth-child(even){{background:#fcfcfc}}footer{{padding:30px 56px;background:#fafafa;color:var(--muted);border-top:1px solid var(--line);font-size:12px}}</style></head><body><div class="topbar"></div><section class="hero"><span class="pill">Second-level endpoint caller audit</span><h1>Endpoint 호출 메소드 → 외부 호출 프로젝트 연결 분석</h1><p class="meta">1차 분석에서 endpoint를 직접 호출한 4개 프로젝트의 메소드를 추출하고, 해당 메소드를 외부 비-Api/비-UnitTest 프로젝트에서 호출하는 정적 근거를 연결했습니다.</p></section><section class="summary">{cards}</section><main><section class="panel"><h2>대상 프로젝트별 연결 수</h2><div class="grid">{target_cards}</div></section><section class="panel"><h2>상세 연결 표</h2><div class="toolbar"><input id="q" placeholder="프로젝트, 메소드, endpoint 검색"><a class="btn" href="{OUT_CSV.name}">CSV 다운로드</a></div><div class="table-wrap"><table id="tbl"><thead><tr><th>#</th><th>대상 사용 프로젝트</th><th>Endpoint 호출 클래스</th><th>Endpoint 호출 메소드</th><th>호출 Endpoint 목록</th><th>외부 호출 프로젝트</th><th>외부 호출 클래스</th><th>외부 호출 메소드(라인)</th><th>신뢰도</th><th>분석</th></tr></thead><tbody>{''.join(trs)}</tbody></table></div></section></main><footer>Generated from <code>{DETAIL}</code>. Static analysis; dynamic reflection/DI/runtime routing may require manual verification.</footer><script>const q=document.getElementById('q');const rows=[...document.querySelectorAll('#tbl tbody tr')];q.addEventListener('input',()=>{{const s=q.value.toLowerCase();rows.forEach(r=>r.style.display=r.textContent.toLowerCase().includes(s)?'':'none')}});</script></body></html>'''
    OUT_HTML.write_text(html_doc,encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
