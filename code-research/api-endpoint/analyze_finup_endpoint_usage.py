#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/mnt/c/Dev')
CSV_PATH = Path('/mnt/c/reports/code-research/api-endpoint/finup_api_endpoints.csv')
OUT_DIR = Path('/mnt/c/reports/code-research/api-endpoint')
DETAIL_CSV = OUT_DIR / 'finup_endpoint_usage_detail.csv'
UNUSED_CSV = OUT_DIR / 'finup_endpoint_unused.csv'
MD_REPORT = OUT_DIR / 'finup_endpoint_usage_report.md'
HTML_REPORT = OUT_DIR / 'finup_endpoint_usage_report.html'
SUMMARY_JSON = OUT_DIR / 'finup_endpoint_usage_summary.json'
PATTERN_FILE = OUT_DIR / 'finup_endpoint_usage_patterns.txt'
RG = os.environ.get('RG', 'rg')
SOURCE_GLOBS = ['*.cs','*.cshtml','*.vbhtml','*.aspx','*.ascx','*.asmx','*.ashx','*.js','*.jsx','*.ts','*.tsx','*.config','*.json','*.xml','*.html','*.htm']
SKIP_GLOBS = ['!**/bin/**','!**/obj/**','!**/packages/**','!**/node_modules/**','!**/.git/**','!**/.vs/**','!**/dist/**','!**/build/**','!**/.omx/**']
API_PROJECT_RE = re.compile(r'(^|\.)Api($|\.)', re.I)
FINUP_RE = re.compile(r'^finup[\w.\-]*$', re.I)
CONTROL_METHODS = {'if','for','foreach','while','switch','catch','using','lock','return','new','throw'}
CS_CLASS_RE = re.compile(r'\b(?:public|private|protected|internal|sealed|abstract|static|partial\s+)*\s*(?:class|struct|interface|record)\s+(\w+)', re.I)
CS_METHOD_RE = re.compile(r'''^\s*(?:\[[^\]]+\]\s*)*(?:(?:public|private|protected|internal|static|async|override|virtual|sealed|partial|extern|new)\s+)*\s*(?:[\w<>,\[\]\.?]+\s+)+(\w+)\s*\([^;]*\)\s*(?:\{|$|where\b)''', re.X)
CS_CTOR_RE = re.compile(r'^\s*(?:(?:public|private|protected|internal)\s+)?(\w+)\s*\([^;]*\)\s*(?:\{|$)')
JS_FUNC_RE = re.compile(r'\b(?:function\s+(\w+)\s*\(|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>|(\w+)\s*:\s*function\s*\()')
RAZOR_FUNC_RE = re.compile(r'@(?:functions|code)|\b(?:ActionResult|Task<[^>]+>|IActionResult|JsonResult)\s+(\w+)\s*\(')

@dataclass(frozen=True)
class Endpoint:
    endpoint_id: int
    project: str
    url: str
    endpoint_class: str
    endpoint_method: str
    http: str
    file: str
    line: str
    source: str
    norm_url: str
    literal_parts: tuple[str, ...]


def normalize_url(u: str) -> str:
    u = (u or '').strip().strip('"\'')
    u = re.sub(r'^https?://[^/]+/', '', u, flags=re.I)
    u = u.lstrip('/')
    u = re.sub(r'/+', '/', u)
    return u.lower()


def literal_parts(url: str) -> tuple[str, ...]:
    parts=[]; last=0
    for m in re.finditer(r'\{[^}]+\}', url):
        part=url[last:m.start()]
        if part and len(part.strip('/'))>=2:
            parts.append(part.lower())
        last=m.end()
    tail=url[last:]
    if tail and len(tail.strip('/'))>=2:
        parts.append(tail.lower())
    return tuple(parts)


def load_endpoints() -> list[Endpoint]:
    out=[]
    with CSV_PATH.open(encoding='utf-8-sig', newline='') as f:
        for i,r in enumerate(csv.DictReader(f),1):
            url=(r.get('url') or '').strip(); norm=normalize_url(url)
            out.append(Endpoint(i,(r.get('project') or '').strip(),url,(r.get('class') or '').strip(),(r.get('method') or '').strip(),(r.get('http') or '').strip(),(r.get('file') or '').strip(),(r.get('line') or '').strip(),(r.get('source') or '').strip(),norm,literal_parts(norm)))
    return out


def discover_projects():
    api={}; non={}; dirs={}
    for top in ROOT.iterdir():
        if not top.is_dir() or not FINUP_RE.match(top.name):
            continue
        for csproj in top.glob('*.csproj'):
            name=csproj.stem; rec={'name':name,'dir':top,'csproj':csproj}
            if API_PROJECT_RE.search(name): api[name]=rec
            else:
                non[name]=rec; dirs[top.resolve()]=name
    return api, non, dirs


def build_patterns(endpoints: list[Endpoint]) -> list[str]:
    pats=set()
    for ep in endpoints:
        u=ep.norm_url
        if not u: continue
        # Avoid generic no-slash method names such as getUserIp that collide with ordinary app methods.
        if '/' in u or ':' in u or u.startswith('api') or len(u)>=14:
            if len(u)>=8:
                pats.add(u)
        # For parameterized routes, add literal pieces only when they are specific enough.
        if '{' in u:
            for part in ep.literal_parts:
                token=part.strip('/')
                if len(token)>=10 and ('/' in part or ':' in part):
                    pats.add(part)
    return sorted(pats)


def run_rg(paths: list[Path], patterns: list[str]) -> list[tuple[Path,int,str]]:
    PATTERN_FILE.write_text('\n'.join(patterns), encoding='utf-8')
    cmd=[RG,'--no-heading','--line-number','--ignore-case','--fixed-strings','-f',str(PATTERN_FILE)]
    for g in SOURCE_GLOBS: cmd += ['-g', g]
    for g in SKIP_GLOBS: cmd += ['-g', g]
    cmd += [str(p) for p in paths]
    proc=subprocess.run(cmd, text=True, capture_output=True, cwd=str(ROOT))
    if proc.returncode not in (0,1):
        raise RuntimeError(proc.stderr[:4000])
    hits=[]
    for line in proc.stdout.splitlines():
        # rg format: /path:line:content. Path is absolute and may contain colon only on Windows drive, not here.
        try:
            file_s, line_s, content = line.split(':', 2)
            hits.append((Path(file_s), int(line_s), content))
        except ValueError:
            continue
    return hits


def run_rg_files(paths: list[Path]) -> list[Path]:
    cmd=[RG,'--files']
    for g in SOURCE_GLOBS: cmd += ['-g', g]
    for g in SKIP_GLOBS: cmd += ['-g', g]
    cmd += [str(p) for p in paths]
    proc=subprocess.run(cmd, text=True, capture_output=True, cwd=str(ROOT))
    if proc.returncode not in (0,1): return []
    return [Path(x) for x in proc.stdout.splitlines() if x.strip()]


def read_text(path: Path) -> str:
    for enc in ('utf-8-sig','utf-8','cp949','euc-kr','latin-1'):
        try: return path.read_text(encoding=enc, errors='strict')
        except UnicodeDecodeError: continue
        except OSError: return ''
    try: return path.read_text(encoding='utf-8', errors='ignore')
    except OSError: return ''

_line_cache: dict[Path, list[str]] = {}
def get_lines(path: Path) -> list[str]:
    if path not in _line_cache:
        _line_cache[path]=read_text(path).splitlines()
    return _line_cache[path]


def find_scope(lines: list[str], idx0: int, path: Path):
    klass=''; method=''; ext=path.suffix.lower(); start=max(0,idx0-240)
    for j in range(idx0, start-1, -1):
        line=lines[j]
        if not method:
            if ext=='.cs':
                m=CS_METHOD_RE.match(line)
                if m and m.group(1) not in CONTROL_METHODS: method=m.group(1)
                else:
                    cm=CS_CTOR_RE.match(line)
                    if cm and cm.group(1) not in CONTROL_METHODS: method=cm.group(1)
            elif ext in {'.js','.jsx','.ts','.tsx'}:
                m=JS_FUNC_RE.search(line)
                if m: method=next(g for g in m.groups() if g)
            elif ext in {'.cshtml','.vbhtml','.aspx','.ascx'}:
                m=RAZOR_FUNC_RE.search(line)
                if m and m.groups(): method=next((g for g in m.groups() if g), '') or 'Razor/View'
        if not klass and ext=='.cs':
            c=CS_CLASS_RE.search(line)
            if c: klass=c.group(1)
        if klass and method: break
    if not klass:
        if ext in {'.js','.jsx','.ts','.tsx'}: klass='JavaScript/TypeScript'
        elif ext in {'.config','.json','.xml'}: klass='Config'
        elif ext in {'.cshtml','.vbhtml','.aspx','.ascx','.html','.htm'}: klass='View/Markup'
        else: klass=path.stem
    if not method:
        if ext in {'.config','.json','.xml'}: method='설정/상수 영역'
        elif ext in {'.cshtml','.vbhtml','.aspx','.ascx','.html','.htm'}: method='View/Markup 영역'
        else: method='메소드 식별 필요'
    return klass, method


def line_context(lines, idx0):
    return re.sub(r'\s+',' ', ' '.join(x.strip() for x in lines[max(0,idx0-2):min(len(lines),idx0+3)]))[:500]


def match_endpoint(ep: Endpoint, norm_line: str, raw_line: str):
    u=ep.norm_url
    if not u: return False,'',''
    if '/' not in u and ':' not in u and not any(x in raw_line.lower() for x in ['http','/','url','endpoint','route']):
        return False,'',''
    if u in norm_line:
        return True, ('template-exact' if '{' in u else 'exact'), 'High'
    if '{' in u and ep.literal_parts:
        # Require all literal segments for parameter routes when possible. This catches interpolated/concatenated paths without exploding on broad prefixes.
        pos=-1; ok=True
        for part in ep.literal_parts:
            k=norm_line.find(part, pos+1)
            if k<0:
                ok=False; break
            pos=k
        if ok:
            return True,'param-literals','Medium'
        if len(ep.literal_parts)==1 and len(ep.literal_parts[0].strip('/'))>=10 and ep.literal_parts[0] in norm_line:
            return True,'param-prefix','Medium'
    return False,'',''


def classify_usage(path: Path, line: str, ctx: str, match_type: str, confidence: str):
    blob=(line+' '+ctx).lower(); signals=[]
    if any(x in blob for x in ['httpclient','restclient','webclient','httprequest','httpwebrequest','postasjsonasync','getasync','postasync','deleteasync','patchasync']): signals.append('서버-side HTTP 호출 후보')
    if any(x in blob for x in ['$.ajax','ajax(','fetch(','axios','.getjson','xmlhttprequest']): signals.append('클라이언트 AJAX/fetch 호출 후보')
    if any(x in blob for x in ['appsettings','web.config','app.config','urlconfig','baseurl','apiurl','endpoint']): signals.append('설정/상수 URL 후보')
    if any(x in blob for x in ['signalr','hubconnection','wss://','websocket']): signals.append('SignalR/실시간 연결 후보')
    if any(x in blob for x in ['test','unittest','xunit','mstest','nunit']): signals.append('테스트 코드 후보')
    if not signals: signals.append('문자열/경로 참조 후보')
    mt={'exact':'CSV URL과 동일한 정적 문자열','template-exact':'CSV 파라미터 템플릿과 동일한 정적 문자열','param-prefix':'CSV 파라미터 URL의 고정 prefix 매칭','param-literals':'CSV 파라미터 URL의 고정 구간 순차 매칭'}.get(match_type,match_type)
    return f"{'; '.join(signals)}. 매칭={mt}, 신뢰도={confidence}."


def rel(path: Path):
    try: return str(path.relative_to(ROOT)).replace('\\','/')
    except Exception: return str(path).replace('\\','/')


def main():
    endpoints=load_endpoints(); api_projects, non_api_projects, project_dirs=discover_projects(); paths=[rec['dir'] for rec in non_api_projects.values()]
    patterns=build_patterns(endpoints); rg_hits=run_rg(paths, patterns); files=run_rg_files(paths)
    file_to_project={}
    for d,name in project_dirs.items(): file_to_project[str(d)]=name
    def project_for(path: Path):
        rp=path.resolve()
        best=('', '')
        for ds,name in file_to_project.items():
            if str(rp).startswith(ds+'/') or str(rp)==ds:
                if len(ds)>len(best[0]): best=(ds,name)
        return best[1]
    hits=[]; seen=set()
    for path,line_no,content in rg_hits:
        proj=project_for(path)
        if not proj: continue
        norm_line=normalize_url(content.lower())
        lines=get_lines(path); klass,method=find_scope(lines, max(0,line_no-1), path); ctx=line_context(lines, max(0,line_no-1))
        for ep in endpoints:
            ok,mt,conf=match_endpoint(ep,norm_line,content)
            if not ok: continue
            key=(ep.endpoint_id,proj,rel(path),line_no,mt)
            if key in seen: continue
            seen.add(key)
            hits.append({'endpoint_id':ep.endpoint_id,'프로젝트 명':ep.project,'엔드포인트 URL':ep.url,'HTTP':ep.http,'엔드포인트 클래스':ep.endpoint_class,'엔드포인트 메소드':ep.endpoint_method,'엔드포인트 정의 위치':f"{ep.file}:{ep.line}" if ep.file else '','사용 프로젝트 명':proj,'클래스':klass,'메소드(라인)':f"{method} ({rel(path)}:{line_no})",'사용 파일':rel(path),'사용 라인':line_no,'매칭 유형':mt,'신뢰도':conf,'소스 라인':content.strip(),'메소드 분석':classify_usage(path,content,ctx,mt,conf)})
    used_endpoint_ids={h['endpoint_id'] for h in hits}; unused=[ep for ep in endpoints if ep.endpoint_id not in used_endpoint_ids]
    fields=['프로젝트 명','엔드포인트 URL','엔드포인트 클래스','엔드포인트 메소드','사용 프로젝트 명','클래스','메소드(라인)','메소드 분석','HTTP','엔드포인트 정의 위치','사용 파일','사용 라인','매칭 유형','신뢰도','소스 라인','endpoint_id']
    detail_rows=sorted(hits,key=lambda x:(x['프로젝트 명'].lower(),x['엔드포인트 URL'].lower(),x['사용 프로젝트 명'].lower(),x['사용 파일'],x['사용 라인']))
    for ep in unused:
        detail_rows.append({'endpoint_id':ep.endpoint_id,'프로젝트 명':ep.project,'엔드포인트 URL':ep.url,'HTTP':ep.http,'엔드포인트 클래스':ep.endpoint_class,'엔드포인트 메소드':ep.endpoint_method,'엔드포인트 정의 위치':f"{ep.file}:{ep.line}" if ep.file else '','사용 프로젝트 명':'미사용(정적 매칭 없음)','클래스':'','메소드(라인)':'','사용 파일':'','사용 라인':'','매칭 유형':'unused','신뢰도':'N/A','소스 라인':'','메소드 분석':'비-Api FinUp 프로젝트 소스에서 CSV endpoint 문자열/파라미터 literal 기준 사용처를 찾지 못함.'})
    with DETAIL_CSV.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(detail_rows)
    with UNUSED_CSV.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['프로젝트 명','엔드포인트 URL','HTTP','엔드포인트 클래스','엔드포인트 메소드','엔드포인트 정의 위치','endpoint_id']); w.writeheader();
        for ep in unused: w.writerow({'프로젝트 명':ep.project,'엔드포인트 URL':ep.url,'HTTP':ep.http,'엔드포인트 클래스':ep.endpoint_class,'엔드포인트 메소드':ep.endpoint_method,'엔드포인트 정의 위치':f"{ep.file}:{ep.line}" if ep.file else '', 'endpoint_id': ep.endpoint_id})
    by_api=Counter(h['프로젝트 명'] for h in hits); by_use=Counter(h['사용 프로젝트 명'] for h in hits); by_conf=Counter(h['신뢰도'] for h in hits); by_match=Counter(h['매칭 유형'] for h in hits); ep_by_api=Counter(ep.project for ep in endpoints); used_by_api=defaultdict(set)
    for h in hits: used_by_api[h['프로젝트 명']].add(h['endpoint_id'])
    api_summary=[]
    for api_name in sorted(ep_by_api):
        total=ep_by_api[api_name]; used=len(used_by_api[api_name]); api_summary.append({'api_project':api_name,'endpoint_count':total,'used_endpoint_count':used,'usage_hit_count':by_api.get(api_name,0),'unused_endpoint_count':total-used})
    summary={'generated_at':datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds'),'root':str(ROOT),'csv':str(CSV_PATH),'endpoint_rows':len(endpoints),'unique_endpoint_urls':len({ep.norm_url for ep in endpoints}),'api_projects_from_csv':sorted({ep.project for ep in endpoints}),'discovered_api_projects_excluded':sorted(api_projects),'analyzed_non_api_projects':sorted(non_api_projects),'analyzed_non_api_project_count':len(non_api_projects),'candidate_patterns':len(patterns),'scanned_files':len(files),'candidate_hit_lines':len(rg_hits),'usage_hits':len(hits),'used_endpoint_rows':len(used_endpoint_ids),'unused_endpoint_rows':len(unused),'by_confidence':dict(by_conf),'by_match_type':dict(by_match),'top_using_projects':by_use.most_common(20),'api_summary':api_summary,'outputs':{'detail_csv':str(DETAIL_CSV),'unused_csv':str(UNUSED_CSV),'markdown':str(MD_REPORT),'html':str(HTML_REPORT),'patterns':str(PATTERN_FILE)}}
    SUMMARY_JSON.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    def md_escape(s): return str(s).replace('|','\\|').replace('\n',' ')
    top_hits=sorted(hits,key=lambda x:(x['신뢰도']!='High',x['프로젝트 명'],x['엔드포인트 URL'],x['사용 프로젝트 명']))[:220]
    md=['# FinUp 비-Api 프로젝트 API Endpoint 사용 분석','',f"- 생성시각: `{summary['generated_at']}`",f"- 기준 CSV: `{CSV_PATH}`",f"- 분석 루트: `{ROOT}`",'- 제외 기준: 프로젝트명에 `.Api` 세그먼트가 있는 `FinUp.*Api*` 프로젝트는 사용처 분석 대상에서 제외','- 매칭 기준: CSV `url` 정적 문자열 exact match + `{param}` route의 고정 literal/prefix match','- Binance 디자인 적용: `/home/kmyoon/.codex/skills/codex-design/binance/DESIGN.md`의 dark canvas, yellow accent, markets-table card 스타일을 HTML에 반영','','## 1. 요약','','|항목|값|','|---|---:|']
    for k,label in [('endpoint_rows','CSV endpoint row'),('unique_endpoint_urls','고유 URL'),('analyzed_non_api_project_count','분석한 비-Api 프로젝트'),('scanned_files','스캔 대상 파일'),('candidate_hit_lines','후보 hit 라인'),('usage_hits','사용처 hit'),('used_endpoint_rows','사용 확인 endpoint row'),('unused_endpoint_rows','정적 미사용 endpoint row')]: md.append(f"|{label}|{summary[k]}|")
    md += ['','## 2. API 프로젝트별 사용 확인 현황','','|API 프로젝트|Endpoint 수|사용 확인 Endpoint|사용처 Hit|정적 미사용 Endpoint|','|---|---:|---:|---:|---:|']
    for r in api_summary: md.append(f"|{md_escape(r['api_project'])}|{r['endpoint_count']}|{r['used_endpoint_count']}|{r['usage_hit_count']}|{r['unused_endpoint_count']}|")
    md += ['','## 3. 사용 프로젝트 상위','','|사용 프로젝트|Hit 수|','|---|---:|']
    for p,c in by_use.most_common(30): md.append(f"|{md_escape(p)}|{c}|")
    md += ['','## 4. Endpoint 사용처 표 (상위 220건, 전체는 CSV/HTML 참조)','','|프로젝트 명|엔드포인트 URL|엔드포인트 클래스|엔드포인트 메소드|사용 프로젝트 명|클래스|메소드(라인)|메소드 분석|','|---|---|---|---|---|---|---|---|']
    for h in top_hits: md.append('|{}|{}|{}|{}|{}|{}|{}|{}|'.format(md_escape(h['프로젝트 명']),md_escape(h['엔드포인트 URL']),md_escape(h['엔드포인트 클래스']),md_escape(h['엔드포인트 메소드']),md_escape(h['사용 프로젝트 명']),md_escape(h['클래스']),md_escape(h['메소드(라인)']),md_escape(h['메소드 분석'])))
    md += ['','## 5. 산출물','',f"- 전체 상세 CSV: `{DETAIL_CSV}`",f"- 정적 미사용 Endpoint CSV: `{UNUSED_CSV}`",f"- Binance 스타일 HTML: `{HTML_REPORT}`",f"- 요약 JSON: `{SUMMARY_JSON}`",f"- 매칭 패턴 파일: `{PATTERN_FILE}`",'','## 6. 한계 및 다음 확인 필요 사항','','- 본 분석은 소스 정적 매칭이다. 런타임에서 base URL + path segment를 DB/환경변수로 조립하는 경우 누락될 수 있다.','- `{param}` route는 고정 literal/prefix 기반 중간 신뢰도 매칭을 포함하므로, 동명이 route family 사이는 수동 검증이 필요하다.','- 짧은 단일 세그먼트 endpoint(`getUserIp` 등)는 일반 메소드명과 충돌할 수 있어 URL/route 문맥이 없는 경우 사용처로 보지 않았다.','- API 호출 성공/실패 처리, 재시도, 중복 처리 위험은 호출 메소드별 추가 흐름 분석이 필요하다.','- 운영 설정의 실제 base URL, proxy/rewrite 설정, IIS 가상 디렉터리 매핑은 배포 환경에서 확인해야 한다.']
    MD_REPORT.write_text('\n'.join(md),encoding='utf-8')
    table_rows=[]
    for h in detail_rows:
        cls='unused' if h.get('매칭 유형')=='unused' else ('high' if h.get('신뢰도')=='High' else 'medium')
        table_rows.append('<tr class="{}">{}</tr>'.format(cls,''.join(f'<td>{html.escape(str(h.get(col,"")))}</td>' for col in fields[:8])))
    api_cards=''.join(f"<div class='stat'><span>{html.escape(r['api_project'])}</span><strong>{r['used_endpoint_count']}/{r['endpoint_count']}</strong><em>{r['usage_hit_count']} hits</em></div>" for r in api_summary)
    top_cards=''.join(f"<div class='pill'><span>{html.escape(p)}</span><b>{c}</b></div>" for p,c in by_use.most_common(16))
    html_doc=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>FinUp Endpoint Usage Analysis</title><style>:root{{--primary:#fcd535;--primary-active:#f0b90b;--canvas:#0b0e11;--card:#1e2329;--elev:#2b3139;--body:#eaecef;--muted:#707a8a;--muted2:#929aa5;--ink:#181a20;--up:#0ecb81;--down:#f6465d;--info:#3b82f6}}*{{box-sizing:border-box}}body{{margin:0;background:var(--canvas);color:var(--body);font-family:BinanceNova,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;font-size:14px;line-height:1.5}}header{{padding:64px 32px 40px;max-width:1440px;margin:auto}}.brand{{color:var(--primary);font-weight:800;letter-spacing:.08em;font-size:13px}}h1{{font-size:48px;line-height:1.1;letter-spacing:-.5px;margin:16px 0 12px;color:#fff}}.lead{{max-width:980px;color:var(--muted2);font-size:16px}}.metrics{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:32px}}.metric{{background:var(--card);border:1px solid var(--elev);border-radius:12px;padding:24px}}.metric span{{display:block;color:var(--muted);font-size:12px}}.metric strong{{display:block;color:var(--primary);font-family:BinancePlex,IBM Plex Sans,monospace;font-size:36px;line-height:1.1;margin-top:8px}}main{{max-width:1440px;margin:auto;padding:0 32px 64px}}section{{margin:32px 0}}h2{{font-size:24px;color:#fff;margin:0 0 16px}}.card{{background:var(--card);border:1px solid var(--elev);border-radius:12px;padding:24px;overflow:hidden}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}}.stat,.pill{{background:#0f1318;border:1px solid var(--elev);border-radius:8px;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:12px}}.stat span,.pill span{{color:var(--muted2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.stat strong,.pill b{{color:var(--primary);font-family:BinancePlex,monospace}}.stat em{{color:var(--muted);font-style:normal;font-size:12px}}.toolbar{{display:flex;gap:12px;margin-bottom:14px;align-items:center;flex-wrap:wrap}}input{{background:#0f1318;border:1px solid var(--elev);border-radius:8px;color:#fff;padding:10px 14px;min-width:320px;outline:none}}input:focus{{box-shadow:0 0 0 2px rgba(59,130,246,.5)}}a.btn{{background:var(--primary);color:var(--ink);text-decoration:none;padding:10px 16px;border-radius:6px;font-weight:700}}.hint{{color:var(--muted);font-size:12px}}.table-wrap{{overflow:auto;max-height:75vh;border:1px solid var(--elev);border-radius:12px}}table{{border-collapse:collapse;width:100%;min-width:1500px}}th,td{{border-bottom:1px solid var(--elev);padding:10px 12px;text-align:left;vertical-align:top}}th{{position:sticky;top:0;background:#181d24;color:var(--muted2);font-size:12px;z-index:1}}td{{color:var(--body);font-size:13px}}tr.high td:first-child{{border-left:3px solid var(--up)}}tr.medium td:first-child{{border-left:3px solid var(--primary)}}tr.unused td{{color:#7c8492}}tr.unused td:first-child{{border-left:3px solid var(--down)}}code{{color:var(--primary)}}footer{{background:#fafafa;color:#181a20;padding:32px;margin-top:48px}}footer .inner{{max-width:1440px;margin:auto}}@media(max-width:900px){{.metrics{{grid-template-columns:1fr 1fr}}h1{{font-size:34px}}input{{min-width:100%;width:100%}}}}</style></head><body><header><div class="brand">BINANCE STYLE · FINUP CODE RESEARCH</div><h1>FinUp 비-Api 프로젝트 API Endpoint 사용 분석</h1><p class="lead">CSV endpoint 목록을 기준으로 <code>FinUp.*Api</code> 프로젝트를 제외한 나머지 <code>FinUp.*</code> 프로젝트에서 정적 사용처를 찾았습니다. Exact/template match는 high, 파라미터 literal/prefix match는 medium으로 분류했습니다.</p><div class="metrics"><div class="metric"><span>CSV endpoints</span><strong>{summary['endpoint_rows']}</strong></div><div class="metric"><span>Non-Api projects</span><strong>{summary['analyzed_non_api_project_count']}</strong></div><div class="metric"><span>Usage hits</span><strong>{summary['usage_hits']}</strong></div><div class="metric"><span>Unused rows</span><strong>{summary['unused_endpoint_rows']}</strong></div></div></header><main><section><h2>API 프로젝트별 사용 확인</h2><div class="card"><div class="grid">{api_cards}</div></div></section><section><h2>사용 프로젝트 Top</h2><div class="card"><div class="grid">{top_cards}</div></div></section><section><h2>전체 Endpoint 사용처 표</h2><div class="card"><div class="toolbar"><input id="q" placeholder="프로젝트, URL, 클래스, 메소드 검색"><a class="btn" href="{DETAIL_CSV.name}">CSV 다운로드</a><span class="hint">행 수: {len(detail_rows)} · 생성: {summary['generated_at']}</span></div><div class="table-wrap"><table id="tbl"><thead><tr>{''.join(f'<th>{html.escape(c)}</th>' for c in fields[:8])}</tr></thead><tbody>{''.join(table_rows)}</tbody></table></div></div></section></main><footer><div class="inner">Design source: <code>/home/kmyoon/.codex/skills/codex-design/binance/DESIGN.md</code>. Static analysis source: <code>{CSV_PATH}</code>, <code>{ROOT}</code>.</div></footer><script>const q=document.getElementById('q'),rows=[...document.querySelectorAll('#tbl tbody tr')];q.addEventListener('input',()=>{{const s=q.value.toLowerCase();rows.forEach(r=>r.style.display=r.textContent.toLowerCase().includes(s)?'':'none')}});</script></body></html>'''
    HTML_REPORT.write_text(html_doc,encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
