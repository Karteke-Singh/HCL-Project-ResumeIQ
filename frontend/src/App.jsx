import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Activity, ArrowDownToLine, ArrowRight, BriefcaseBusiness, CheckCircle2, ChevronDown, ChevronRight, CircleHelp, ClipboardCheck, Cpu, FileSearch, FileText, LayoutDashboard, LoaderCircle, PlusCircle, Search, ShieldCheck, Sparkles, UploadCloud, X, Zap } from 'lucide-react';
import { api } from './api';

const nav = [
  { id: 'dashboard', label: 'Dashboard', Icon: LayoutDashboard },
  { id: 'jobs', label: 'Jobs', Icon: BriefcaseBusiness },
  { id: 'create', label: 'Create Job', Icon: PlusCircle },
  { id: 'workspace', label: 'Analysis Workspace', Icon: FileSearch }
];
const resultOf = x => x?.result ?? x;
const scoreOf = x => Number(x?.scores?.total_score ?? 0);
const scoreText = x => Number(x || 0).toFixed(1);

export default function App() {
  const [page, setPage] = useState('dashboard');
  const [jobs, setJobs] = useState([]);
  const [jobId, setJobId] = useState('');
  const [job, setJob] = useState(null);
  const [online, setOnline] = useState(false);
  const [apiStatus, setApiStatus] = useState('Checking FastAPI connection…');
  const [files, setFiles] = useState([]);
  const [results, setResults] = useState([]);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState('');
  const [error, setError] = useState('');
  const [expanded, setExpanded] = useState({});
  const [search, setSearch] = useState('');
  const inputRef = useRef(null);

  async function refresh() {
    try {
      const h = await api.health();
      const healthy = Boolean(h?.success && resultOf(h)?.status === 'healthy');
      setOnline(healthy); setApiStatus(healthy ? 'Connected to local FastAPI backend' : 'FastAPI responded; verify database health');
      const response = await api.jobs();
      const list = Array.isArray(resultOf(response)) ? resultOf(response) : [];
      setJobs(list); setJobId(current => current || list[0]?.id || ''); setError('');
    } catch (e) { setOnline(false); setApiStatus('Backend disconnected — start FastAPI on port 8000'); setError(e.message); }
  }
  useEffect(() => { refresh(); }, []);
  useEffect(() => { if (!jobId) { setJob(null); return; } api.job(jobId).then(r => setJob(resultOf(r))).catch(() => setJob(null)); }, [jobId]);

  function addFiles(incoming) {
    const all = Array.from(incoming || []);
    const valid = all.filter(f => /\.(pdf|docx|txt)$/i.test(f.name));
    const invalid = all.filter(f => !/\.(pdf|docx|txt)$/i.test(f.name));
    setError(invalid.length ? `Unsupported file(s): ${invalid.map(f => f.name).join(', ')}. Use PDF, DOCX, or TXT.` : '');
    setFiles(current => { const next = [...current]; valid.forEach(f => { if (!next.some(x => x.name === f.name && x.size === f.size)) next.push(f); }); return next; });
  }
  async function screen() {
    if (!jobId) return setError('Select a job position first.');
    if (!files.length) return setError('Select at least one resume file.');
    setBusy(true); setError(''); setResults([]); const done = [];
    for (let i = 0; i < files.length; i++) {
      const file = files[i]; setProgress(`Screening ${i + 1} of ${files.length}: ${file.name}`);
      try { const response = await api.screen(jobId, file); const r = resultOf(response); done.push({ ...r, filename: file.name, warnings: response?.warnings || r?.warnings || [] }); }
      catch (e) { done.push({ candidate_id: file.name, display_name: file.name, filename: file.name, error: e.message, warnings: [] }); }
      setResults([...done]);
    }
    setBusy(false); setProgress(''); setPage('workspace');
  }
  const goodResults = results.filter(r => !r.error);
  const average = goodResults.length ? goodResults.reduce((n, r) => n + scoreOf(r), 0) / goodResults.length : 0;
  const passed = goodResults.filter(r => r.scores?.passed_hard_requirements).length;
  const visible = useMemo(() => results.filter(r => `${r.candidate_id} ${r.display_name} ${r.filename}`.toLowerCase().includes(search.toLowerCase())), [results, search]);
  function exportCsv() {
    const cols = ['Candidate ID','Name','Resume','Score / 100','Hard Requirements Passed','Experience Passed','Matched Skills','Missing Skills','Explanation','Error'];
    const cell = v => `"${String(v ?? '').replaceAll('"','""')}"`;
    const lines = [cols.map(cell).join(',')];
    results.forEach(r => lines.push([r.candidate_id,r.display_name,r.filename,r.scores?.total_score,r.scores?.passed_hard_requirements,r.experience_passed,(r.matched_skills||[]).join('; '),(r.missing_skills||[]).join('; '),r.explanation,r.error].map(cell).join(',')));
    const url = URL.createObjectURL(new Blob([lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' }));
    const a = document.createElement('a'); a.href = url; a.download = 'resumeiq-screening-results.csv'; a.click(); URL.revokeObjectURL(url);
  }
  function clearSession() { setResults([]); setFiles([]); setExpanded({}); setError(''); }

  return <div className="shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-logo"><Layers /></div><div className="brand-copy"><b>ResumeScreen<span>AI</span></b><small>Recruiter Decision Support</small></div><span className="project-tag">P_101</span></div>
      <div className="nav-label">NAVIGATION</div><nav>{nav.map(({ id, label, Icon }) => <button key={id} className={`nav-item ${page === id ? 'active' : ''}`} onClick={() => { setPage(id); setError(''); }}><Icon size={17}/><span>{label}</span>{page === id && <ChevronRight className="nav-chevron" size={15}/>}</button>)}</nav>
      <div className="sidebar-bottom"><div className="decision-note"><ShieldCheck size={17}/><div><b>Decision Support Only</b><p>Scores and explanations are advisory. Human reviewers make all hiring decisions.</p></div></div><div className="sidebar-foot"><i/> Local prototype <span>v1.0</span></div></div>
    </aside>
    <main className="main">
      <header className="topbar"><div className="mobile-brand"><Layers size={22}/><b>ResumeScreenAI</b></div><div className="top-badges"><span className="badge badge-green"><ShieldCheck size={15}/> Non-Authoritative AI Audit</span><span className="badge badge-purple"><Sparkles size={15}/> Deterministic-First Hybrid Engine</span></div></header>
      <div className="content">
        <div className="page-heading"><div><div className="eyebrow">P_101 · RESUME SCREENING SYSTEM</div><h1>{page === 'dashboard' ? 'Recruiter Screening Dashboard' : page === 'jobs' ? 'Job Requirements' : page === 'create' ? 'Create Job Profile' : 'Analysis Workspace'}</h1><p>{page === 'dashboard' ? 'Deterministic matching, semantic similarity, and grounded explanations.' : page === 'jobs' ? 'Review roles loaded from your FastAPI backend.' : page === 'create' ? 'Draft requirements for a future screening role.' : 'Review score breakdowns, requirement coverage, and explanations.'}</p></div><div className="heading-buttons"><button className="btn btn-white" onClick={() => setPage('create')}><PlusCircle size={16}/> Configure Job</button><button className="btn btn-navy" onClick={() => { setPage('dashboard'); setTimeout(() => document.getElementById('upload-panel')?.scrollIntoView({behavior:'smooth'}), 50); }}><FileSearch size={16}/> Start Screening</button></div></div>
        <div className={`connection ${online ? 'is-online' : 'is-offline'}`}><i/><div className="connection-text"><b>Backend Service Status: {online ? 'Online / Connected' : 'Offline / Disconnected'}</b><small>{apiStatus}. {online ? 'API: 127.0.0.1:8000' : 'Ensure FastAPI is running at http://127.0.0.1:8000.'}</small></div><div className="connection-right"><span><ShieldCheck size={15}/> Deterministic Grounding</span><span><Cpu size={15}/> Hybrid Matching</span><button className="refresh" title="Refresh backend status" onClick={refresh}><Activity size={16}/></button></div></div>
        {error && <div className="error-banner"><CircleHelp size={17}/><span>{error}</span><button onClick={() => setError('')}><X size={16}/></button></div>}
        {page === 'dashboard' && <>
          <section className="metrics"><Metric Icon={BriefcaseBusiness} label="JOBS CONFIGURED" value={jobs.length} note="Loaded from backend" tone="violet"/><Metric Icon={FileSearch} label="SCREENS COMPLETED" value={goodResults.length} note="This session" tone="green"/><Metric Icon={ClipboardCheck} label="DECISION SUPPORT" value="Audited" note="No automated hiring cuts" tone="slate"/></section>
          <section className="dashboard-grid"><div className="panel"><PanelHead title="Recent Screening Analyses" subtitle="Evaluations conducted in this session" action={<button className="link-button" onClick={clearSession}>Clear History</button>}/>{results.length ? <div className="recent-list">{results.slice().reverse().slice(0,5).map((r,i)=><button className="recent-row" key={`${r.filename}-${i}`} onClick={()=>{setPage('workspace');setExpanded({[r.candidate_id]:true});}}><div className="file-icon"><FileText size={18}/></div><div className="recent-name"><b>{r.filename}</b><small>{job?.title || 'Selected job'} · {r.error ? 'Screening error' : 'This session'}</small></div><div className="recent-score">{r.error ? 'Error' : `${scoreText(scoreOf(r))}%`}<small>Fit score</small></div><ChevronRight size={16}/></button>)}</div> : <Empty Icon={FileText} title="No screening analyses yet" text="Upload one or more resumes below to create your first comparison report."/>}</div>
            <div className="panel workflow"><PanelHead title="Screening Workflow" subtitle="Step-by-step decision support"/><Step n="1" title="Define Job Requirements" text="Choose a job description. Mandatory skills and experience are loaded from the backend." active/><Step n="2" title="Upload Candidate Resume" text="Upload PDF, DOCX, or TXT files for text extraction and matching."/><Step n="3" title="Inspect Evidence & Explanations" text="Review score breakdowns, requirement coverage, and evidence snippets."/><button className="btn btn-soft wide" onClick={()=>document.getElementById('upload-panel')?.scrollIntoView({behavior:'smooth'})}>Start by selecting a job <ArrowRight size={15}/></button></div></section>
          <section className="panel upload-panel" id="upload-panel"><PanelHead title="Start a Screening Session" subtitle="Select the role and upload resumes to compare against its requirements."/><div className="upload-grid"><div><label className="field-label" htmlFor="job-select">Select job position</label><div className="select-box"><BriefcaseBusiness size={16}/><select id="job-select" value={jobId} onChange={e=>setJobId(e.target.value)}><option value="">Choose a job…</option>{jobs.map(j=><option key={j.id} value={j.id}>{j.title} ({j.id})</option>)}</select><ChevronDown size={15}/></div>{job && <div className="job-preview"><b>{job.title}</b><p>{job.description || job.jd_text || 'Job description unavailable.'}</p><div className="chips">{(job.requirements?.must_have_skills||[]).map(s=><span key={s}>{s}</span>)}</div><button className="link-button" onClick={()=>setPage('jobs')}>View full requirements <ArrowRight size={14}/></button></div>}</div>
            <div><label className="field-label">Upload candidate resumes</label><div className={`dropzone ${files.length?'has-files':''}`} onDragOver={e=>e.preventDefault()} onDrop={e=>{e.preventDefault();addFiles(e.dataTransfer.files);}}><div className="upload-icon"><UploadCloud size={25}/></div><div className="drop-copy"><b>Drag and drop resume files</b><small>PDF, DOCX, or TXT · up to 10 MB per file</small></div><button className="btn btn-white browse" onClick={()=>inputRef.current?.click()}>Browse files</button><input ref={inputRef} type="file" accept=".pdf,.docx,.txt" multiple hidden onChange={e=>{addFiles(e.target.files);e.target.value='';}}/></div>{files.length>0 && <div className="file-list">{files.map((f,i)=><div className="picked-file" key={`${f.name}-${f.size}`}><FileText size={16}/><span>{f.name}<small>{(f.size/1024).toFixed(1)} KB</small></span><button aria-label={`Remove ${f.name}`} onClick={()=>setFiles(current=>current.filter((_,n)=>n!==i))}><X size={15}/></button></div>)}</div>}<div className="upload-footer"><span>{files.length} resume{files.length===1?'':'s'} selected</span><button className="btn btn-navy" disabled={busy||!files.length||!jobId} onClick={screen}>{busy?<LoaderCircle className="spin" size={16}/>:<Zap size={16}/>} {busy?'Screening…':'Start Resume Screening'}</button></div>{progress && <div className="progress"><LoaderCircle className="spin" size={15}/>{progress}</div>}</div></div></section>
        </>}
        {page === 'jobs' && <JobsPage jobs={jobs} selected={jobId} select={id=>{setJobId(id);setPage('dashboard');}} create={()=>setPage('create')}/>}
        {page === 'create' && <CreatePage back={()=>setPage('dashboard')}/>}
        {page === 'workspace' && <section className="workspace"><div className="metrics"><Metric Icon={FileSearch} label="RESUMES SCREENED" value={goodResults.length} note={`${results.length-goodResults.length} failed`} tone="violet"/><Metric Icon={CheckCircle2} label="HARD REQUIREMENTS PASSED" value={passed} note="Verify extracted evidence" tone="green"/><Metric Icon={Activity} label="AVERAGE SCORE" value={`${scoreText(average)}/100`} note="Successful screens only" tone="slate"/></div><div className="panel"><PanelHead title="Candidate Comparison" subtitle="Results for the selected job · scores are advisory" action={<div className="table-actions"><div className="search-box"><Search size={15}/><input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search candidates"/></div><button className="btn btn-white export" onClick={exportCsv} disabled={!results.length}><ArrowDownToLine size={15}/> Export CSV</button></div>}/>{!results.length?<Empty Icon={FileSearch} title="No results to compare" text="Return to the dashboard and upload resumes to start screening." action={<button className="btn btn-navy" onClick={()=>setPage('dashboard')}>Go to upload</button>}/>:<div className="table-wrap"><table><thead><tr><th>Candidate</th><th>Score / 100</th><th>Hard requirements</th><th>Experience</th><th>Matched skills</th><th>Missing skills</th><th>Audit</th></tr></thead><tbody>{visible.map((r,i)=><tr key={`${r.candidate_id}-${i}`}><td><b>{r.candidate_id}</b><small>{r.filename||r.display_name}</small></td><td><Score score={scoreOf(r)} error={r.error}/></td><td>{r.error?'—':<Status yes={!!r.scores?.passed_hard_requirements}/>}</td><td>{r.error?'—':<Status yes={!!r.experience_passed}/>}</td><td><SkillList list={r.matched_skills||[]}/></td><td><SkillList list={r.missing_skills||[]} missing/></td><td><button className="audit-button" onClick={()=>setExpanded(v=>({...v,[r.candidate_id]:!v[r.candidate_id]}))}>{expanded[r.candidate_id]?'Hide':'View audit'} <ChevronDown size={13}/></button></td></tr>)}</tbody></table></div>}</div>{goodResults.length>0 && <div className="panel chart-panel"><PanelHead title="Score Comparison" subtitle="Scores returned by the screening API"/><div className="chart">{goodResults.map((r,i)=><div className="bar-col" key={`${r.candidate_id}-${i}`}><b>{scoreText(scoreOf(r))}</b><div className="bar-track"><div className="bar-fill" style={{height:`${Math.max(2,Math.min(100,scoreOf(r)))}%`}}/></div><small>{r.candidate_id}</small></div>)}</div></div>}{visible.filter(r=>expanded[r.candidate_id]).map((r,i)=><Audit key={`${r.candidate_id}-${i}`} r={r} job={job?.title}/ >)}<div className="human-note"><ShieldCheck size={18}/><div><b>Human review required</b><p>Use the results to organize evidence and identify follow-up questions. Do not use scores as the sole basis for hiring decisions.</p></div></div></section>}
        <footer className="footer"><span>ResumeScreenAI · P_101</span><span>Deterministic-first · Human-in-the-loop</span></footer>
      </div>
    </main>
  </div>;
}

function Layers(){return <svg width="23" height="23" viewBox="0 0 24 24" fill="none"><path d="m12 3 9 4.5-9 4.5-9-4.5L12 3Zm-9 9 9 4.5 9-4.5M3 16.5 12 21l9-4.5" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round"/></svg>}
function Metric({Icon,label,value,note,tone}){return <div className="metric"><div className={`metric-icon ${tone}`}><Icon size={21}/></div><div><span>{label}</span><b>{value}</b><small>{note}</small></div></div>}
function PanelHead({title,subtitle,action}){return <div className="panel-head"><div><h2>{title}</h2>{subtitle&&<p>{subtitle}</p>}</div>{action&&<div className="panel-action">{action}</div>}</div>}
function Empty({Icon,title,text,action}){return <div className="empty"><div><Icon size={23}/></div><b>{title}</b><p>{text}</p>{action}</div>}
function Step({n,title,text,active}){return <div className="step"><div className={active?'step-no active':'step-no'}>{n}</div><div><b>{title}</b><p>{text}</p></div></div>}
function Score({score,error}){if(error)return <span className="score error">Error</span>;return <span className={`score ${score>=70?'good':score>=45?'mid':'low'}`}>{scoreText(score)}</span>}
function Status({yes}){return <span className={`status ${yes?'yes':'no'}`}><i/>{yes?'Pass':'Review'}</span>}
function SkillList({list,missing}){return list.length?<div className="skill-list">{list.slice(0,5).map(s=><span className={missing?'skill missing':'skill'} key={s}>{s}</span>)}{list.length>5&&<small>+{list.length-5}</small>}</div>:<span className="muted">—</span>}
function Audit({r,job}){const [raw,setRaw]=useState(false);return <div className="panel audit-panel"><PanelHead title={`Evidence Audit · ${r.candidate_id}`} subtitle={`${r.filename||r.display_name} · ${job||r.job_title||'Selected job'}`} action={<Score score={scoreOf(r)} error={r.error}/>}/>{r.error?<div className="notice error-notice">{r.error}</div>:<><div className="audit-metrics"><div><small>LLM fit signal</small><b>{r.scores?.llm_fit_score==null?'Not returned':`${Math.round(r.scores.llm_fit_score*100)}%`}</b></div><div><small>Semantic similarity</small><b>{r.scores?.semantic_score==null?'Not returned':`${Math.round(r.scores.semantic_score*100)}%`}</b></div><div><small>Experience check</small><b>{r.experience_passed?'Requirement met':'Needs review'}</b></div></div><h3>Explanation</h3><p className="explanation">{r.explanation||'No explanation returned.'}</p>{r.llm_reason&&<p className="fit-reason"><Sparkles size={14}/>{r.llm_reason}</p>}<h3>Evidence snippets returned by backend</h3>{r.evidence_snippets?.length?<ul className="evidence-list">{r.evidence_snippets.map((e,i)=><li key={i}><CheckCircle2 size={16}/>{e}</li>)}</ul>:<div className="notice">No evidence snippets returned. Manually verify the original resume before relying on the explanation.</div>}{r.warnings?.length>0&&<div className="notice">{r.warnings.map((w,i)=><div key={i}>• {w}</div>)}</div>}<button className="link-button raw-toggle" onClick={()=>setRaw(v=>!v)}>{raw?'Hide raw response':'Inspect returned fields'} <ChevronDown size={14}/></button>{raw&&<pre className="raw-json">{JSON.stringify(r,null,2)}</pre>}</>}</div>}
function JobsPage({jobs,selected,select,create}){return <div className="panel jobs-panel"><PanelHead title="Available Job Profiles" subtitle="Loaded directly from the FastAPI backend" action={<button className="btn btn-navy" onClick={create}><PlusCircle size={15}/> Create Job</button>}/>{!jobs.length?<Empty Icon={BriefcaseBusiness} title="No jobs available" text="Check that the backend is running and contains job records."/>:<div className="job-cards">{jobs.map(j=><div className={`job-card ${selected===j.id?'selected':''}`} key={j.id}><div className="job-icon"><BriefcaseBusiness size={20}/></div><div><h3>{j.title}</h3><small>{j.id}</small><div className="chips">{(j.requirements?.must_have_skills||[]).map(s=><span key={s}>{s}</span>)}</div><button className="link-button" onClick={()=>select(j.id)}>Use this job <ArrowRight size={14}/></button></div></div>)}</div>}</div>}
function CreatePage({back}){const [title,setTitle]=useState('');const [description,setDescription]=useState('');const [skills,setSkills]=useState('');const [notice,setNotice]=useState('');return <div className="panel create-panel"><PanelHead title="Create a Job Profile" subtitle="Draft requirements for a future screening session."/><div className="notice"><CircleHelp size={16}/>The existing backend routes support reading jobs, but do not yet include a create-job endpoint. This form is a draft and will not be saved to the database.</div><div className="form-stack"><label>Job title<input value={title} onChange={e=>setTitle(e.target.value)} placeholder="e.g. Junior Python Backend Developer"/></label><label>Job description<textarea rows="5" value={description} onChange={e=>setDescription(e.target.value)} placeholder="Responsibilities and qualifications…"/></label><label>Must-have skills <small>Separate skills with commas</small><input value={skills} onChange={e=>setSkills(e.target.value)} placeholder="Python, FastAPI, SQL, Git"/></label><button className="btn btn-navy" onClick={()=>setNotice(title.trim()&&description.trim()?'Draft validated locally. Add POST /api/v1/jobs to save this job to the database.':'Enter a job title and description before validating.')}>Validate draft</button>{notice&&<div className="notice">{notice}</div>}<button className="btn btn-white" onClick={back}>Back to dashboard</button></div></div>}
