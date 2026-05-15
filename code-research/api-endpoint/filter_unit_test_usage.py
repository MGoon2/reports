#!/usr/bin/env python3
from __future__ import annotations
import csv, json, html
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/mnt/c/reports/code-research/api-endpoint')
SRC_ENDPOINTS = BASE / 'finup_api_endpoints.csv'
DETAIL = BASE / 'finup_endpoint_usage_detail.csv'
UNUSED = BASE / 'finup_endpoint_unused.csv'
SUMMARY = BASE / 'finup_endpoint_usage_summary.json'
MD = BASE / 'finup_endpoint_usage_report.md'
HTML = BASE / 'finup_endpoint_usage_report.html'

def is_unittest(value: str) -> bool:
    return 'unittest' in (value or '').lower()

def esc(x):
    return html.escape(str(x if x is not None else ''))

def read_endpoint_inventory():
    endpoints=[]
    with SRC_ENDPOINTS.open(encoding='utf-8-sig', newline='') as f:
        for i,r in enumerate(csv.DictReader(f),1):
            endpoints.append({
                'endpoint_id': str(i),
                '프로젝트 명': (r.get('project') or '').strip(),
                '엔드포인트 URL': (r.get('url') or '').strip(),
                'HTTP': (r.get('http') or '').strip(),
                '엔드포인트 클래스': (r.get('class') or '').strip(),
                '엔드포인트 메소드': (r.get('method') or '').strip(),
                '엔드포인트 정의 위치': f"{(r.get('file') or '').strip()}:{(r.get('line') or '').strip()}" if r.get('file') else '',
            })
    return endpoints

def unused_row(ep):
    return {
        **ep,
        '사용 프로젝트 명': '미사용(정적 매칭 없음)',
        '클래스': '',
        '메소드(라인)': '',
        '사용 파일': '',
        '사용 라인': '',
        '매칭 유형': 'unused',
        '신뢰도': 'N/A',
        '소스 라인': '',
        '메소드 분석': '비-Api FinUp 프로젝트 소스에서 CSV endpoint 문자열/파라미터 literal 기준 사용처를 찾지 못함. UnitTest 프로젝트는 분석 대상에서 제외됨.',
    }

def status_cell(r):
    mt=r.get('매칭 유형','')
    conf=r.get('신뢰도','')
    if mt=='unused': return "<span class='status unused'>미사용</span>"
    if conf=='High': return "<span class='status used'>사용</span><span class='confidence high'>High</span>"
    return "<span class='status review'>검토</span><span class='confidence medium'>Medium</span>"

def verb_class(http):
    h=(http or 'ANY').lower()
    return 'v-' + {'get':'get','post':'post','put':'put','patch':'patch','delete':'delete','any':'any'}.get(h,'any')

def endpoint_def(r):
    http=r.get('HTTP') or 'ANY'
    return f"<span class='verb {verb_class(http)}'>{esc(http)}</span> <span class='method'>{esc(r.get('엔드포인트 클래스'))}.{esc(r.get('엔드포인트 메소드'))}</span>"

def usage_loc(r):
    if r.get('매칭 유형')=='unused': return "<span class='muted'>정적 매칭 없음</span>"
    return f"<strong>{esc(r.get('사용 프로젝트 명'))}</strong><small>{esc(r.get('클래스'))}<br>{esc(r.get('메소드(라인)'))}</small>"

def short_analysis(r):
    txt=r.get('메소드 분석','')
    src=r.get('소스 라인','')
    parts=[esc(txt)]
    if src: parts.append(f"<code class='source'>{esc(src[:220])}{'…' if len(src)>220 else ''}</code>")
    return '<br>'.join(parts)

def md_escape(s):
    return str(s).replace('|','\\|').replace('\n',' ')

endpoints=read_endpoint_inventory()
endpoint_by_id={ep['endpoint_id']: ep for ep in endpoints}
old_rows=list(csv.DictReader(DETAIL.open(encoding='utf-8-sig')))
usage_rows=[r for r in old_rows if r.get('매칭 유형')!='unused']
removed=[r for r in usage_rows if is_unittest(r.get('사용 프로젝트 명','')) or is_unittest(r.get('프로젝트 명',''))]
kept=[r for r in usage_rows if r not in removed]
used_ids={r.get('endpoint_id') for r in kept}
new_unused=[unused_row(ep) for ep in endpoints if ep['endpoint_id'] not in used_ids]
fields=['프로젝트 명','엔드포인트 URL','엔드포인트 클래스','엔드포인트 메소드','사용 프로젝트 명','클래스','메소드(라인)','메소드 분석','HTTP','엔드포인트 정의 위치','사용 파일','사용 라인','매칭 유형','신뢰도','소스 라인','endpoint_id']
kept_sorted=sorted(kept,key=lambda x:(x['프로젝트 명'].lower(),x['엔드포인트 URL'].lower(),x['사용 프로젝트 명'].lower(),x.get('사용 파일',''),int(x.get('사용 라인') or 0)))
detail_rows=kept_sorted+new_unused
with DETAIL.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(detail_rows)
with UNUSED.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['프로젝트 명','엔드포인트 URL','HTTP','엔드포인트 클래스','엔드포인트 메소드','엔드포인트 정의 위치','endpoint_id'],extrasaction='ignore')
    w.writeheader(); w.writerows(new_unused)

by_api=Counter(r['프로젝트 명'] for r in kept)
by_use=Counter(r['사용 프로젝트 명'] for r in kept)
by_conf=Counter(r['신뢰도'] for r in kept)
by_match=Counter(r['매칭 유형'] for r in kept)
ep_by_api=Counter(ep['프로젝트 명'] for ep in endpoints)
used_by_api=defaultdict(set)
for r in kept: used_by_api[r['프로젝트 명']].add(r['endpoint_id'])
api_summary=[]
for api_name in sorted(ep_by_api):
    total=ep_by_api[api_name]; used=len(used_by_api[api_name])
    api_summary.append({'api_project':api_name,'endpoint_count':total,'used_endpoint_count':used,'usage_hit_count':by_api.get(api_name,0),'unused_endpoint_count':total-used})
old_summary=json.loads(SUMMARY.read_text(encoding='utf-8'))
analyzed=[p for p in old_summary.get('analyzed_non_api_projects',[]) if not is_unittest(p)]
summary={**old_summary,
    'generated_at': datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds'),
    'unit_test_projects_excluded': True,
    'unit_test_usage_rows_removed': len(removed),
    'analyzed_non_api_projects': analyzed,
    'analyzed_non_api_project_count': len(analyzed),
    'usage_hits': len(kept),
    'used_endpoint_rows': len(used_ids),
    'unused_endpoint_rows': len(new_unused),
    'by_confidence': dict(by_conf),
    'by_match_type': dict(by_match),
    'top_using_projects': by_use.most_common(20),
    'api_summary': api_summary,
}
SUMMARY.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

# Markdown refresh, concise full summary + top 220 rows.
md=['# FinUp 비-Api 프로젝트 API Endpoint 사용 분석','',f"- 생성시각: `{summary['generated_at']}`",f"- 기준 CSV: `{SRC_ENDPOINTS}`",'- 제외 기준: `FinUp.*Api*` 프로젝트와 프로젝트명에 `UnitTest`가 포함된 사용 프로젝트 제외','- 매칭 기준: CSV `url` 정적 문자열 exact match + `{param}` route의 고정 literal/prefix match','','## 1. 요약','','|항목|값|','|---|---:|']
for k,label in [('endpoint_rows','CSV endpoint row'),('unique_endpoint_urls','고유 URL'),('analyzed_non_api_project_count','분석한 비-Api 프로젝트(UnitTest 제외)'),('usage_hits','사용처 hit(UnitTest 제외)'),('unit_test_usage_rows_removed','UnitTest 사용처 제거 행'),('used_endpoint_rows','사용 확인 endpoint row'),('unused_endpoint_rows','정적 미사용 endpoint row')]:
    md.append(f"|{label}|{summary.get(k,0)}|")
md += ['','## 2. API 프로젝트별 사용 확인 현황','','|API 프로젝트|Endpoint 수|사용 확인 Endpoint|사용처 Hit|정적 미사용 Endpoint|','|---|---:|---:|---:|---:|']
for r in api_summary: md.append(f"|{md_escape(r['api_project'])}|{r['endpoint_count']}|{r['used_endpoint_count']}|{r['usage_hit_count']}|{r['unused_endpoint_count']}|")
md += ['','## 3. 사용 프로젝트 상위(UnitTest 제외)','','|사용 프로젝트|Hit 수|','|---|---:|']
for p,c in by_use.most_common(30): md.append(f"|{md_escape(p)}|{c}|")
md += ['','## 4. Endpoint 사용처 표 (상위 220건, 전체는 CSV/HTML 참조)','','|프로젝트 명|엔드포인트 URL|엔드포인트 클래스|엔드포인트 메소드|사용 프로젝트 명|클래스|메소드(라인)|메소드 분석|','|---|---|---|---|---|---|---|---|']
for r in kept_sorted[:220]:
    md.append('|{}|{}|{}|{}|{}|{}|{}|{}|'.format(md_escape(r['프로젝트 명']),md_escape(r['엔드포인트 URL']),md_escape(r['엔드포인트 클래스']),md_escape(r['엔드포인트 메소드']),md_escape(r['사용 프로젝트 명']),md_escape(r['클래스']),md_escape(r['메소드(라인)']),md_escape(r['메소드 분석'])))
md += ['','## 5. 산출물','',f"- 전체 상세 CSV: `{DETAIL}`",f"- 정적 미사용 Endpoint CSV: `{UNUSED}`",f"- HTML: `{HTML}`",f"- 요약 JSON: `{SUMMARY}`"]
MD.write_text('\n'.join(md),encoding='utf-8')

metric_cards=''.join(f"<article class='metric'><span>{label}</span><strong>{value}</strong></article>" for label,value in [('CSV endpoints',summary['endpoint_rows']),('Non-Api projects',summary['analyzed_non_api_project_count']),('Usage hits',summary['usage_hits']),('Static-unused rows',summary['unused_endpoint_rows']),('UnitTest removed',summary['unit_test_usage_rows_removed']),('Candidate hit lines',summary.get('candidate_hit_lines','-'))])
api_cards=''.join(f"<article class='api-card'><span>{esc(a['api_project'])}</span><strong>{a['used_endpoint_count']}/{a['endpoint_count']}</strong><em>{a['usage_hit_count']} hits · unused {a['unused_endpoint_count']}</em></article>" for a in api_summary)
top_using=''.join(f"<li data-project=\"{esc(p)}\"><span>{esc(p)}</span><strong>{c}</strong></li>" for p,c in by_use.most_common(16))
trs=[]
for i,r in enumerate(detail_rows,1):
    cls='unused-row' if r.get('매칭 유형')=='unused' else ('used-row' if r.get('신뢰도')=='High' else 'review-row')
    trs.append(f"""
          <tr class='{cls}'>
            <td class='no'>{i}</td>
            <td><span class='project'>{esc(r.get('프로젝트 명'))}</span></td>
            <td><code class='endpoint'>{esc(r.get('엔드포인트 URL'))}</code></td>
            <td>{endpoint_def(r)}</td>
            <td class='status-cell'>{status_cell(r)}</td>
            <td class='usage-loc'>{usage_loc(r)}</td>
            <td class='analysis'>{short_analysis(r)}</td>
          </tr>""")
html_doc=f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<title>FinUp Endpoint Usage Analysis · Binance</title><meta name="design-reference" content="/mnt/c/reports/code-research/api-endpoint/finup_api_endpoints.html" /><meta name="design-source" content="/home/kmyoon/.codex/skills/codex-design/binance/DESIGN.md" />
<style>
*{{box-sizing:border-box}}:root{{--primary:#fcd535;--primary-active:#f0b90b;--ink:#181a20;--muted:#707a8a;--line:#eaecef;--line-dark:#2b3139;--canvas:#ffffff;--soft:#fafafa;--dark:#0b0e11;--dark-card:#1e2329;--dark-elevated:#2b3139;--up:#0ecb81;--down:#f6465d;--info:#3b82f6}}body{{margin:0;background:var(--canvas);color:var(--ink);font-family:BinanceNova,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}.topbar{{height:10px;background:repeating-linear-gradient(135deg,var(--primary) 0 18px,var(--primary-active) 18px 36px,var(--dark) 36px 54px)}}.hero{{position:relative;overflow:hidden;padding:72px 56px 52px;background:linear-gradient(135deg,#0b0e11 0%,#181a20 58%,#2b3139 100%);color:#fff}}.hero:before{{content:"";position:absolute;inset:auto -90px -160px auto;width:420px;height:420px;border-radius:50%;background:radial-gradient(circle,rgba(252,213,53,.38) 0 32%,transparent 66%);filter:blur(2px)}}.hero:after{{content:"";position:absolute;inset:36px 56px auto auto;width:76px;height:76px;background:var(--primary);transform:rotate(45deg);opacity:.95;box-shadow:110px 70px 0 rgba(252,213,53,.42),-82px 108px 0 rgba(252,213,53,.22)}}.pill{{position:relative;display:inline-flex;align-items:center;gap:8px;background:var(--primary);color:var(--ink);border-radius:6px;padding:12px 24px;font-size:14px;font-weight:700;line-height:1}}h1{{position:relative;margin:28px 0 16px;max-width:1080px;font-size:56px;line-height:1.1;letter-spacing:-1px;font-weight:700}}.meta{{position:relative;max-width:1120px;color:#eaecef;font-size:15px;line-height:1.65}}.meta code{{background:rgba(255,255,255,.08);color:var(--primary);border:1px solid var(--line-dark);border-radius:4px;padding:1px 6px}}.summary{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;padding:28px 56px;background:var(--soft);border-bottom:1px solid var(--line)}}.metric{{min-height:86px;padding:18px 20px;background:var(--canvas);border:1px solid var(--line);border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:14px;box-shadow:0 6px 18px rgba(24,26,32,.04)}}.metric span{{color:var(--muted);font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.05em}}.metric strong{{color:var(--ink);font-family:BinancePlex,ui-monospace,monospace;font-size:30px;line-height:1}}main{{padding:34px 56px 64px}}.panel{{margin:0 0 24px;padding:24px;border:1px solid var(--line);border-radius:10px;background:#fff;box-shadow:0 12px 28px rgba(24,26,32,.05)}}.panel-head{{display:flex;align-items:flex-end;justify-content:space-between;gap:18px;margin-bottom:18px}}h2{{margin:0;color:var(--ink);font-size:24px;letter-spacing:-.2px}}.sub{{margin:6px 0 0;color:var(--muted);font-size:13px}}.actions{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}}.btn{{display:inline-flex;align-items:center;justify-content:center;height:38px;padding:0 16px;border-radius:6px;background:var(--primary);color:var(--ink);text-decoration:none;font-size:13px;font-weight:800}}.search{{height:38px;min-width:340px;border:1px solid var(--line);border-radius:6px;padding:0 12px;font-size:13px;color:var(--ink);background:#fff}}.search:focus{{outline:none;border-color:var(--info);box-shadow:0 0 0 2px rgba(59,130,246,.18)}}.api-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}}.api-card{{padding:14px 16px;border:1px solid var(--line);border-radius:8px;background:var(--soft);display:grid;gap:6px}}.api-card span{{color:var(--muted);font-size:12px;font-weight:700}}.api-card strong{{color:var(--ink);font-family:BinancePlex,ui-monospace,monospace;font-size:24px}}.api-card em{{color:var(--muted);font-style:normal;font-size:12px}}.two-col{{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:24px;align-items:start}}.top-list{{list-style:none;padding:0;margin:0;display:grid;gap:8px}}.top-list li{{display:flex;justify-content:space-between;gap:12px;padding:10px 12px;border:1px solid var(--line);border-radius:6px;background:#fff;cursor:pointer;transition:background .12s ease,border-color .12s ease,transform .12s ease}}.top-list li:hover{{background:#fff9dc;border-color:var(--primary);transform:translateY(-1px)}}.top-list li.active{{background:#fff4c2;border-color:var(--primary-active);box-shadow:0 0 0 2px rgba(252,213,53,.22)}}.top-list span{{color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.top-list strong{{color:var(--primary-active);font-family:BinancePlex,ui-monospace,monospace}}.top-actions{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:12px 0 12px}}.view-all{{height:34px;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--ink);padding:0 12px;font-size:12px;font-weight:800;cursor:pointer}}.view-all:hover{{border-color:var(--primary-active);background:#fff9dc}}.filter-chip{{color:var(--muted);font-size:12px;line-height:1.4}}.table-wrap{{border:1px solid var(--line);border-radius:8px;background:#fff;box-shadow:0 12px 28px rgba(24,26,32,.06)}}table{{width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;font-size:13px}}thead th{{background:#fafafa;color:var(--muted);text-align:left;padding:13px 12px;border-bottom:1px solid var(--line);font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.04em}}tbody td{{padding:13px 12px;border-bottom:1px solid var(--line);vertical-align:top;word-break:break-word}}tbody tr:nth-child(even){{background:#fcfcfc}}tbody tr:hover{{background:#fff9dc}}tbody tr:last-child td{{border-bottom:none}}th.no,td.no{{width:48px;color:var(--muted);text-align:right;font-family:BinancePlex,ui-monospace,monospace}}th.api,td.api{{width:150px}}th.url,td.url{{width:230px}}th.def,td.def{{width:200px}}th.status-h,td.status-cell{{width:110px}}th.usage,td.usage-loc{{width:290px}}.project{{display:inline-flex;max-width:100%;padding:4px 8px;border-radius:999px;background:#f5f5f5;border:1px solid var(--line);font-weight:700;color:var(--ink)}}code.endpoint{{color:#b8860b;font-family:BinancePlex,ui-monospace,monospace;font-size:12px}}code.source{{display:block;margin-top:8px;color:#4f5967;background:#fafafa;border:1px solid var(--line);border-radius:6px;padding:8px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12px;line-height:1.45}}.verb{{display:inline-flex;min-width:54px;justify-content:center;align-items:center;margin-right:6px;border-radius:4px;padding:3px 7px;color:#fff;font-size:11px;font-weight:800;font-family:BinancePlex,ui-monospace,monospace}}.v-get{{background:#0ecb81}}.v-post{{background:#3b82f6}}.v-patch{{background:#f0b90b;color:#181a20}}.v-delete{{background:#f6465d}}.v-put{{background:#2dbdb6}}.v-any{{background:#707a8a}}.method{{font-weight:700;color:var(--ink)}}.status{{display:inline-flex;align-items:center;justify-content:center;min-width:54px;padding:5px 8px;border-radius:999px;font-weight:800;font-size:12px}}.status.used{{background:#e7fbf3;color:#087a50}}.status.review{{background:#fff4c2;color:#7a5b00}}.status.unused{{background:#ffe9ed;color:#b51f35}}.confidence{{display:block;margin-top:6px;color:var(--muted);font-family:BinancePlex,ui-monospace,monospace;font-size:11px}}.usage-loc small{{display:block;margin-top:5px;color:var(--muted);line-height:1.45}}.analysis{{color:#303640;line-height:1.55}}.muted{{color:var(--muted)}}footer{{padding:30px 56px;background:#fafafa;color:var(--muted);border-top:1px solid var(--line);font-size:12px}}footer code{{color:var(--ink)}}@media(max-width:1100px){{.two-col{{grid-template-columns:1fr}}.search{{min-width:100%}}h1{{font-size:40px}}main,.summary,.hero,footer{{padding-left:24px;padding-right:24px}}table{{table-layout:auto}}}}
</style></head><body><div class="topbar"></div><section class="hero"><span class="pill">Binance endpoint usage audit</span><h1>FinUp 비-Api 프로젝트 Endpoint 사용 분석</h1><p class="meta">기준 파일 <code>finup_api_endpoints.html</code>의 문서형 레이아웃을 참고해 재구성했습니다. 프로젝트명에 <code>UnitTest</code>가 포함된 사용 프로젝트는 제외했습니다. 테이블은 페이지 자체 스크롤을 사용하며 내부 고정 높이/내부 스크롤 영역을 두지 않습니다.</p></section><section class="summary" aria-label="분석 요약">{metric_cards}</section><main><section class="panel"><div class="panel-head"><div><h2>API 프로젝트별 사용 확인</h2><p class="sub">값은 사용 확인 endpoint / 전체 endpoint, hits, 정적 미사용 건수입니다. UnitTest 프로젝트는 제외되었습니다.</p></div></div><div class="api-grid">{api_cards}</div></section><section class="two-col"><section class="panel"><div class="panel-head"><div><h2>전체 Endpoint 사용처</h2><p class="sub">전체 {len(detail_rows)}행 · 사용처 {summary['usage_hits']}건 · 정적 미사용 {summary['unused_endpoint_rows']}건 · UnitTest 제거 {summary['unit_test_usage_rows_removed']}건</p></div><div class="actions"><input id="q" class="search" placeholder="프로젝트, URL, 클래스, 메소드 검색" /><a class="btn" href="finup_endpoint_usage_detail.csv">CSV 다운로드</a></div></div><div class="table-wrap"><table id="tbl"><thead><tr><th class="no">#</th><th class="api">API 프로젝트</th><th class="url">Endpoint URL</th><th class="def">Endpoint 정의</th><th class="status-h">사용 여부</th><th class="usage">사용 위치</th><th>분석</th></tr></thead><tbody>{''.join(trs)}</tbody></table></div></section><aside class="panel"><h2>사용 프로젝트 Top</h2><p class="sub">정적 매칭 hit 수 기준입니다. 프로젝트를 클릭하면 왼쪽 테이블이 필터링됩니다.</p><div class="top-actions"><button type="button" id="showAll" class="view-all">전체 보기</button><span id="activeFilter" class="filter-chip">전체 표시 중</span></div><ol class="top-list">{top_using}</ol></aside></section></main><footer>Reference: <code>/mnt/c/reports/code-research/api-endpoint/finup_api_endpoints.html</code> · Source data: <code>finup_endpoint_usage_detail.csv</code> · Generated from <code>finup_endpoint_usage_summary.json</code></footer><script>const q=document.getElementById('q');const rows=[...document.querySelectorAll('#tbl tbody tr')];const topItems=[...document.querySelectorAll('.top-list li[data-project]')];const showAll=document.getElementById('showAll');const activeFilter=document.getElementById('activeFilter');let selectedProject='';function normalize(value){{return(value||'').toLowerCase().trim()}}function applyFilters(){{const search=normalize(q.value);const project=normalize(selectedProject);rows.forEach(row=>{{const text=normalize(row.textContent);const projectMatched=!project||text.includes(project);const searchMatched=!search||text.includes(search);row.style.display=projectMatched&&searchMatched?'':'none'}});topItems.forEach(item=>item.classList.toggle('active',item.dataset.project===selectedProject));activeFilter.textContent=selectedProject?`${{selectedProject}} 필터 적용 중`:'전체 표시 중'}}q.addEventListener('input',applyFilters);topItems.forEach(item=>{{item.addEventListener('click',()=>{{selectedProject=item.dataset.project||'';applyFilters()}})}});showAll.addEventListener('click',()=>{{selectedProject='';q.value='';applyFilters()}});</script></body></html>'''
HTML.write_text(html_doc,encoding='utf-8')
print(json.dumps({'removed_unit_test_usage_rows':len(removed),'usage_hits':len(kept),'used_endpoint_rows':len(used_ids),'unused_endpoint_rows':len(new_unused),'detail_rows':len(detail_rows),'top_using_projects':summary['top_using_projects'][:5]},ensure_ascii=False,indent=2))
