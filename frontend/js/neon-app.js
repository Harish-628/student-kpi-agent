/* ============================================
   NEURALKPI — Main Application Logic
   All student data embedded for standalone use
   ============================================ */

// ── STUDENT DATABASE ──────────────────────────────
const STUDENTS = [
  {id:"CSE001",name:"Arjun Sharma",    dept:"Computer Science & Engineering",section:"A",year:3,gpa:9.1},
  {id:"CSE002",name:"Priya Patel",     dept:"Computer Science & Engineering",section:"A",year:3,gpa:8.7},
  {id:"CSE003",name:"Rahul Verma",     dept:"Computer Science & Engineering",section:"B",year:2,gpa:7.8},
  {id:"CSE004",name:"Sneha Iyer",      dept:"Computer Science & Engineering",section:"B",year:4,gpa:8.9},
  {id:"CSE005",name:"Vikram Nair",     dept:"Computer Science & Engineering",section:"C",year:1,gpa:7.2},
  {id:"ECE001",name:"Ananya Krishnan", dept:"Electronics & Communication",   section:"A",year:3,gpa:9.3},
  {id:"ECE002",name:"Karthik Reddy",   dept:"Electronics & Communication",   section:"A",year:2,gpa:8.1},
  {id:"ECE003",name:"Divya Menon",     dept:"Electronics & Communication",   section:"B",year:4,gpa:8.5},
  {id:"ECE004",name:"Sai Kumar",       dept:"Electronics & Communication",   section:"C",year:1,gpa:7.0},
  {id:"ME001", name:"Rohit Singh",     dept:"Mechanical Engineering",        section:"A",year:4,gpa:8.2},
  {id:"ME002", name:"Kavitha Suresh",  dept:"Mechanical Engineering",        section:"B",year:2,gpa:7.5},
  {id:"ME003", name:"Arun Raj",        dept:"Mechanical Engineering",        section:"A",year:3,gpa:8.0},
  {id:"CE001", name:"Deepa Thomas",    dept:"Civil Engineering",             section:"A",year:3,gpa:7.9},
  {id:"CE002", name:"Harish Kumar",    dept:"Civil Engineering",             section:"B",year:2,gpa:7.3},
  {id:"IT001", name:"Meera Nambiar",   dept:"Information Technology",        section:"A",year:4,gpa:9.0},
  {id:"IT002", name:"Ajay Chandran",   dept:"Information Technology",        section:"A",year:3,gpa:8.6},
  {id:"IT003", name:"Lakshmi Pillai",  dept:"Information Technology",        section:"B",year:2,gpa:7.8},
  {id:"AI001", name:"Ravi Teja",       dept:"AI & Data Science",             section:"A",year:3,gpa:9.4},
  {id:"AI002", name:"Pooja Gupta",     dept:"AI & Data Science",             section:"A",year:2,gpa:8.3},
  {id:"AI003", name:"Nikhil Bose",     dept:"AI & Data Science",             section:"B",year:4,gpa:9.1},
  {id:"AI004", name:"Sreya Nair",      dept:"AI & Data Science",             section:"A",year:1,gpa:7.6},
];

const KPI_DATA = {
  CSE001:{internships:4,certifications:10,hackathons:6,publications:3,workshops:12,projects:8,club_activities:6,industrial_visits:8},
  CSE002:{internships:3,certifications:8,hackathons:5,publications:2,workshops:9,projects:6,club_activities:5,industrial_visits:7},
  CSE003:{internships:1,certifications:4,hackathons:2,publications:0,workshops:5,projects:3,club_activities:2,industrial_visits:3},
  CSE004:{internships:3,certifications:9,hackathons:4,publications:2,workshops:11,projects:7,club_activities:5,industrial_visits:8},
  CSE005:{internships:0,certifications:2,hackathons:1,publications:0,workshops:3,projects:2,club_activities:1,industrial_visits:2},
  ECE001:{internships:4,certifications:11,hackathons:7,publications:3,workshops:13,projects:9,club_activities:7,industrial_visits:9},
  ECE002:{internships:2,certifications:5,hackathons:3,publications:1,workshops:7,projects:5,club_activities:3,industrial_visits:5},
  ECE003:{internships:2,certifications:7,hackathons:3,publications:1,workshops:8,projects:5,club_activities:4,industrial_visits:6},
  ECE004:{internships:0,certifications:1,hackathons:1,publications:0,workshops:2,projects:1,club_activities:1,industrial_visits:2},
  ME001: {internships:2,certifications:6,hackathons:2,publications:1,workshops:7,projects:5,club_activities:3,industrial_visits:6},
  ME002: {internships:1,certifications:3,hackathons:1,publications:0,workshops:4,projects:2,club_activities:2,industrial_visits:3},
  ME003: {internships:2,certifications:5,hackathons:2,publications:0,workshops:6,projects:4,club_activities:3,industrial_visits:5},
  CE001: {internships:1,certifications:4,hackathons:2,publications:0,workshops:5,projects:3,club_activities:2,industrial_visits:5},
  CE002: {internships:1,certifications:2,hackathons:1,publications:0,workshops:3,projects:2,club_activities:1,industrial_visits:3},
  IT001: {internships:4,certifications:10,hackathons:5,publications:2,workshops:11,projects:8,club_activities:6,industrial_visits:8},
  IT002: {internships:3,certifications:8,hackathons:5,publications:2,workshops:10,projects:7,club_activities:5,industrial_visits:7},
  IT003: {internships:1,certifications:4,hackathons:2,publications:0,workshops:5,projects:3,club_activities:2,industrial_visits:4},
  AI001: {internships:5,certifications:12,hackathons:8,publications:4,workshops:14,projects:10,club_activities:8,industrial_visits:9},
  AI002: {internships:2,certifications:6,hackathons:4,publications:1,workshops:8,projects:6,club_activities:4,industrial_visits:5},
  AI003: {internships:4,certifications:11,hackathons:7,publications:3,workshops:13,projects:9,club_activities:7,industrial_visits:8},
  AI004: {internships:0,certifications:2,hackathons:1,publications:0,workshops:3,projects:2,club_activities:1,industrial_visits:2},
};

// ── SCORE CALCULATION ─────────────────────────────
const WEIGHTS = {internships:10,certifications:5,hackathons:7,publications:12,workshops:3,projects:8,club_activities:4,industrial_visits:3};
const MAX_VALS = {internships:5,certifications:12,hackathons:8,publications:4,workshops:15,projects:10,club_activities:8,industrial_visits:10};

function calcKPIScore(kpi){
  let score = 0;
  for(const [k,w] of Object.entries(WEIGHTS)){
    score += (Math.min(kpi[k], MAX_VALS[k]) / MAX_VALS[k]) * w;
  }
  return Math.min(parseFloat(score.toFixed(1)), 100);
}

function getReadiness(score){
  if(score>=80) return "High Readiness";
  if(score>=60) return "Moderate Readiness";
  if(score>=40) return "Developing";
  return "Low Readiness";
}

function getReadinessBadge(r){
  if(r.includes("High"))     return `<span class="neon-badge badge-high">${r}</span>`;
  if(r.includes("Moderate")) return `<span class="neon-badge badge-moderate">${r}</span>`;
  if(r.includes("Developing"))return `<span class="neon-badge badge-developing">${r}</span>`;
  return `<span class="neon-badge badge-low">${r}</span>`;
}

function getScoreColor(s){ return s>=80?'var(--neon-green)':s>=60?'var(--neon-cyan)':s>=40?'var(--neon-orange)':'var(--neon-pink)'; }

// Build enriched student list
const ENRICHED = STUDENTS.map(s=>{
  const kpi = KPI_DATA[s.id];
  const score = calcKPIScore(kpi);
  const readiness = getReadiness(score);
  const lastUpdated = new Date(Date.now() - Math.floor(Math.random()*7)*86400000).toLocaleDateString();
  return { ...s, kpi, score, readiness, lastUpdated };
}).sort((a,b)=>b.score-a.score);

// ── CHART.JS DEFAULTS ─────────────────────────────
Chart.defaults.color = 'rgba(120,180,220,0.7)';
Chart.defaults.borderColor = 'rgba(0,245,255,0.08)';
Chart.defaults.font.family = "'Inter', sans-serif";

const NEON_COLORS = [
  '#00f5ff','#bf00ff','#ff006e','#39ff14',
  '#0080ff','#ff6600','#fff000','#ff00cc',
  '#00ffaa','#7700ff'
];

function makeGradient(ctx, c1, c2){
  const g = ctx.createLinearGradient(0,0,0,300);
  g.addColorStop(0, c1); g.addColorStop(1, c2);
  return g;
}

// ── DEPT ABBREVIATIONS ────────────────────────────
const DEPT_SHORT = {
  "Computer Science & Engineering":"CSE",
  "Electronics & Communication":"ECE",
  "Mechanical Engineering":"MECH",
  "Civil Engineering":"CE",
  "Information Technology":"IT",
  "AI & Data Science":"AIDS",
};

// ── SIDEBAR NAV ───────────────────────────────────
let currentSection = 'dashboard';
document.querySelectorAll('.nav-link[data-section]').forEach(btn=>{
  btn.addEventListener('click',()=>{ switchSection(btn.dataset.section); });
});

function switchSection(name){
  document.querySelectorAll('.nav-link').forEach(b=>b.classList.remove('active'));
  document.querySelector(`.nav-link[data-section="${name}"]`)?.classList.add('active');
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  const sec = document.getElementById(`section-${name}`);
  if(sec) sec.classList.add('active');
  document.getElementById('pageTitle').textContent = ({
    dashboard:'DASHBOARD',students:'STUDENTS',kpi:'KPI TRACKER',
    leaderboard:'LEADERBOARD',ai:'AI AGENT',analytics:'ANALYTICS'
  })[name] || name.toUpperCase();
  currentSection = name;
  if(name==='leaderboard') renderLeaderboard();
  if(name==='analytics')   renderAnalyticsCharts();
  if(name==='ai')          renderInsights();
}

// Sidebar collapse
document.getElementById('toggleSidebar').addEventListener('click',()=>{
  document.getElementById('sidebar').classList.toggle('collapsed');
});

// Logout
document.getElementById('logoutBtn').addEventListener('click',()=>{
  localStorage.removeItem('kpi_user');
  window.location.href='neon-login.html';
});

// Load user info
const userInfo = JSON.parse(localStorage.getItem('kpi_user') || '{"name":"Admin","role":"admin"}');
document.getElementById('sidebarName').textContent = userInfo.name || 'Admin';
document.getElementById('sidebarRole').textContent = userInfo.role || 'admin';
document.getElementById('sidebarAvatar').textContent = (userInfo.name||'A')[0].toUpperCase();

// ── DASHBOARD STATS ───────────────────────────────
function initDashboardStats(){
  const total = ENRICHED.length;
  const avg = (ENRICHED.reduce((a,s)=>a+s.score,0)/total).toFixed(1);
  const high = ENRICHED.filter(s=>s.readiness==='High Readiness').length;
  animCounter(document.getElementById('cardStudents'),total,1200);
  animCounter(document.getElementById('cardAvgKPI'),parseFloat(avg),1500,true);
  animCounter(document.getElementById('cardHighReady'),high,800);
}

function animCounter(el,target,dur=1200,isFloat=false){
  if(!el) return;
  let start=0, frames=Math.ceil(dur/16);
  let step=target/frames;
  const run=()=>{
    start=Math.min(start+step,target);
    el.textContent = isFloat ? start.toFixed(1) : Math.ceil(start);
    if(start<target) requestAnimationFrame(run);
  };
  requestAnimationFrame(run);
}

// ── DASHBOARD CHARTS ──────────────────────────────
let radarChart, doughnutChart, barChart, lineChart;

function initDashboardCharts(){
  // KPI Radar - avg across all students
  const fields=['internships','certifications','hackathons','publications','workshops','projects','club_activities','industrial_visits'];
  const labels=['Internships','Certs','Hackathons','Publications','Workshops','Projects','Club','Ind. Visits'];
  const avgVals=fields.map(f=>parseFloat((ENRICHED.reduce((a,s)=>a+s.kpi[f],0)/ENRICHED.length).toFixed(1)));

  radarChart = new Chart(document.getElementById('chartRadar'),{
    type:'radar',
    data:{
      labels,
      datasets:[{
        label:'Avg KPI',
        data:avgVals,
        borderColor:'#00f5ff',
        backgroundColor:'rgba(0,245,255,0.1)',
        pointBackgroundColor:'#00f5ff',
        pointBorderColor:'#00f5ff',
        borderWidth:2,
        pointRadius:4,
      }]
    },
    options:{
      responsive:true, maintainAspectRatio:false,
      scales:{r:{
        grid:{color:'rgba(0,245,255,0.1)'},
        angleLines:{color:'rgba(0,245,255,0.15)'},
        ticks:{backdropColor:'transparent',color:'rgba(0,245,255,0.5)',font:{size:9}},
        pointLabels:{color:'rgba(120,180,220,0.7)',font:{size:10}},
      }},
      plugins:{legend:{display:false}},
    }
  });

  // Career Readiness Doughnut
  const readinessCounts={High:0,Moderate:0,Developing:0,Low:0};
  ENRICHED.forEach(s=>{
    if(s.readiness.includes('High')) readinessCounts.High++;
    else if(s.readiness.includes('Moderate')) readinessCounts.Moderate++;
    else if(s.readiness.includes('Developing')) readinessCounts.Developing++;
    else readinessCounts.Low++;
  });

  doughnutChart = new Chart(document.getElementById('chartDoughnut'),{
    type:'doughnut',
    data:{
      labels:['High','Moderate','Developing','Low'],
      datasets:[{
        data:Object.values(readinessCounts),
        backgroundColor:['rgba(57,255,20,0.7)','rgba(0,245,255,0.7)','rgba(255,102,0,0.7)','rgba(255,0,110,0.7)'],
        borderColor:['#39ff14','#00f5ff','#ff6600','#ff006e'],
        borderWidth:1.5,hoverOffset:8,
      }]
    },
    options:{
      responsive:true,maintainAspectRatio:false,
      cutout:'68%',
      plugins:{
        legend:{position:'bottom',labels:{color:'rgba(120,180,220,0.7)',padding:14,font:{size:11}}},
      },
    }
  });

  // Dept Bar Chart
  const depts=[...new Set(STUDENTS.map(s=>s.dept))];
  const deptAvgs=depts.map(d=>{
    const group=ENRICHED.filter(s=>s.dept===d);
    return parseFloat((group.reduce((a,s)=>a+s.score,0)/group.length).toFixed(1));
  });

  barChart = new Chart(document.getElementById('chartBar'),{
    type:'bar',
    data:{
      labels:depts.map(d=>DEPT_SHORT[d]||d),
      datasets:[{
        label:'Avg KPI Score',
        data:deptAvgs,
        backgroundColor:NEON_COLORS.slice(0,6).map(c=>c+'aa'),
        borderColor:NEON_COLORS.slice(0,6),
        borderWidth:1.5,
        borderRadius:6,
      }]
    },
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{
        x:{grid:{display:false},ticks:{color:'rgba(120,180,220,0.7)'}},
        y:{grid:{color:'rgba(0,245,255,0.06)'},ticks:{color:'rgba(120,180,220,0.7)'},min:0,max:100}
      }
    }
  });

  // Trend Line Chart (simulated monthly data)
  const months=['Aug','Sep','Oct','Nov','Dec','Jan','Feb'];
  const baseScore = ENRICHED.reduce((a,s)=>a+s.score,0)/ENRICHED.length;
  const trendData = months.map((_,i)=>parseFloat((baseScore - 8 + i*1.5 + (Math.random()-0.5)*2).toFixed(1)));

  lineChart=new Chart(document.getElementById('chartLine'),{
    type:'line',
    data:{
      labels:months,
      datasets:[{
        label:'Avg KPI',
        data:trendData,
        borderColor:'#bf00ff',
        backgroundColor:'rgba(191,0,255,0.08)',
        pointBackgroundColor:'#bf00ff',
        pointRadius:5,
        borderWidth:2.5,
        fill:true,
        tension:0.4,
      },{
        label:'Target',
        data:months.map(()=>75),
        borderColor:'rgba(255,0,110,0.4)',
        borderDash:[6,4],
        pointRadius:0,
        borderWidth:1.5,
        fill:false,
      }]
    },
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'rgba(120,180,220,0.7)',font:{size:11}}}},
      scales:{
        x:{grid:{color:'rgba(0,245,255,0.05)'},ticks:{color:'rgba(120,180,220,0.7)'}},
        y:{grid:{color:'rgba(0,245,255,0.06)'},ticks:{color:'rgba(120,180,220,0.7)'},min:40,max:100}
      }
    }
  });
}

// ── STUDENTS TABLE ────────────────────────────────
function renderStudentsTable(data=ENRICHED){
  const tbody=document.getElementById('studentsTbody');
  if(!tbody) return;
  tbody.innerHTML=data.map((s,i)=>`
    <tr style="animation:fadeInUp .3s ease ${i*0.03}s both;">
      <td><span style="font-family:var(--font-mono);color:var(--neon-cyan);font-size:.8rem;">${s.id}</span></td>
      <td><strong style="color:#e8f4ff;">${s.name}</strong></td>
      <td><span style="color:rgba(120,180,220,.7);font-size:.82rem;">${DEPT_SHORT[s.dept]||s.dept}</span></td>
      <td><span class="neon-badge" style="background:rgba(0,245,255,.1);color:var(--neon-cyan);border:1px solid rgba(0,245,255,.2);">${s.section}</span></td>
      <td><span style="color:rgba(120,180,220,.7);">Year ${s.year}</span></td>
      <td>
        <div style="display:flex;align-items:center;gap:8px;">
          <span style="font-family:var(--font-display);font-weight:700;color:${getScoreColor(s.score)};">${s.score}</span>
          <div class="neon-progress" style="width:60px;">
            <div class="neon-progress-fill" style="width:${s.score}%;background:${getScoreColor(s.score)};"></div>
          </div>
        </div>
      </td>
      <td>${getReadinessBadge(s.readiness)}</td>
      <td>
        <div style="display:flex;gap:6px;">
          <button class="btn btn-sm btn-neon-cyan" onclick="viewStudentKPI('${s.id}')">📊 KPI</button>
        </div>
      </td>
    </tr>
  `).join('');
}

function filterStudents(){
  const q=(document.getElementById('studentSearch')?.value||'').toLowerCase();
  const dept=document.getElementById('deptFilter')?.value||'';
  const yr=document.getElementById('yearFilter')?.value||'';
  const filtered=ENRICHED.filter(s=>{
    const matchQ = !q || s.name.toLowerCase().includes(q) || s.id.toLowerCase().includes(q);
    const matchD = !dept || s.dept===dept;
    const matchY = !yr || String(s.year)===yr;
    return matchQ&&matchD&&matchY;
  });
  renderStudentsTable(filtered);
}

function viewStudentKPI(id){
  document.getElementById('kpiStudentSelect').value=id;
  switchSection('kpi');
  loadStudentKPI();
}

// ── KPI TRACKER ───────────────────────────────────
function populateKPIDropdown(){
  const sel=document.getElementById('kpiStudentSelect');
  if(!sel) return;
  ENRICHED.forEach(s=>{
    const o=document.createElement('option');
    o.value=s.id; o.textContent=`${s.name} (${s.id})`;
    sel.appendChild(o);
  });
}

let kpiRadarChart=null, kpiBarChart=null;

function loadStudentKPI(){
  const id=document.getElementById('kpiStudentSelect')?.value;
  const s=id?ENRICHED.find(x=>x.id===id):null;

  const icons={internships:'💼',certifications:'🏅',hackathons:'⚡',publications:'📄',workshops:'🔧',projects:'🚀',club_activities:'🎭',industrial_visits:'🏭'};
  const labels={internships:'Internships',certifications:'Certifications',hackathons:'Hackathons',publications:'Publications',workshops:'Workshops',projects:'Projects',club_activities:'Club Activities',industrial_visits:'Ind. Visits'};

  const grid=document.getElementById('kpiMetricsGrid');
  if(!grid) return;

  if(!s){
    // show averages
    const kf=Object.keys(KPI_DATA.CSE001);
    grid.innerHTML=kf.map(k=>`
      <div class="kpi-metric-card">
        <div class="kpi-metric-icon">${icons[k]||'📊'}</div>
        <div class="kpi-metric-val">—</div>
        <div class="kpi-metric-label">${labels[k]||k}</div>
      </div>
    `).join('');
    return;
  }

  const kf=Object.keys(s.kpi);
  grid.innerHTML=kf.map(k=>`
    <div class="kpi-metric-card" style="animation:fadeInUp .4s ease both;">
      <div class="kpi-metric-icon">${icons[k]||'📊'}</div>
      <div class="kpi-metric-val">${s.kpi[k]}</div>
      <div class="kpi-metric-label">${labels[k]||k}</div>
    </div>
  `).join('');

  // Radar
  if(kpiRadarChart) kpiRadarChart.destroy();
  kpiRadarChart=new Chart(document.getElementById('chartKPIRadar'),{
    type:'radar',
    data:{
      labels:kf.map(k=>labels[k]),
      datasets:[
        {label:s.name,data:kf.map(k=>s.kpi[k]),borderColor:'#00f5ff',backgroundColor:'rgba(0,245,255,0.15)',pointBackgroundColor:'#00f5ff',borderWidth:2,pointRadius:4},
        {label:'Dept Avg',data:kf.map(k=>{
          const peers=ENRICHED.filter(x=>x.dept===s.dept&&x.id!==s.id);
          return parseFloat((peers.reduce((a,x)=>a+x.kpi[k],0)/peers.length).toFixed(1));
        }),borderColor:'rgba(191,0,255,0.6)',backgroundColor:'rgba(191,0,255,0.06)',pointBackgroundColor:'#bf00ff',borderWidth:1.5,pointRadius:3,borderDash:[5,3]},
      ]
    },
    options:{responsive:true,maintainAspectRatio:false,
      scales:{r:{grid:{color:'rgba(0,245,255,0.1)'},angleLines:{color:'rgba(0,245,255,0.15)'},ticks:{backdropColor:'transparent',color:'rgba(0,245,255,0.5)',font:{size:9}},pointLabels:{color:'rgba(120,180,220,.7)',font:{size:10}}}},
      plugins:{legend:{labels:{color:'rgba(120,180,220,.7)',font:{size:11}}}},
    }
  });

  // Bar vs dept avg
  if(kpiBarChart) kpiBarChart.destroy();
  const peers=ENRICHED.filter(x=>x.dept===s.dept);
  kpiBarChart=new Chart(document.getElementById('chartKPIBar'),{
    type:'bar',
    data:{
      labels:peers.map(p=>p.name.split(' ')[0]),
      datasets:[{
        label:'KPI Score',
        data:peers.map(p=>p.score),
        backgroundColor:peers.map(p=>p.id===s.id?'rgba(0,245,255,0.7)':'rgba(0,245,255,0.15)'),
        borderColor:peers.map(p=>p.id===s.id?'#00f5ff':'rgba(0,245,255,0.3)'),
        borderWidth:1.5,borderRadius:6,
      }]
    },
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{x:{grid:{display:false},ticks:{color:'rgba(120,180,220,.7)',font:{size:10}}},y:{grid:{color:'rgba(0,245,255,.05)'},ticks:{color:'rgba(120,180,220,.7)'},min:0,max:100}},
    }
  });
}

// ── LEADERBOARD ───────────────────────────────────
function renderLeaderboard(){
  const container=document.getElementById('leaderboardContainer');
  if(!container) return;
  const avatarColors=['#00f5ff','#bf00ff','#ff006e','#39ff14','#0080ff','#ff6600','#fff000','#ff00cc'];
  container.innerHTML=ENRICHED.map((s,i)=>{
    const rankClass=i===0?'rank-1':i===1?'rank-2':i===2?'rank-3':'rank-other';
    const rankText=i===0?'🥇':i===1?'🥈':i===2?'🥉':`#${i+1}`;
    const color=avatarColors[i%avatarColors.length];
    return `
      <div class="lb-row" onclick="viewStudentKPI('${s.id}')">
        <div class="lb-rank ${rankClass}">${rankText}</div>
        <div class="lb-avatar" style="background:${color}22;border:2px solid ${color};color:${color};">${s.name[0]}</div>
        <div class="lb-info">
          <div class="lb-name">${s.name}</div>
          <div class="lb-dept">${s.id} • ${DEPT_SHORT[s.dept]||s.dept} • Year ${s.year}</div>
        </div>
        <div style="flex-shrink:0;">${getReadinessBadge(s.readiness)}</div>
        <div class="lb-score" style="color:${getScoreColor(s.score)};">${s.score}</div>
        <div class="lb-bar-wrap">
          <div class="lb-bar"><div class="lb-bar-fill" style="width:${s.score}%;background:${getScoreColor(s.score)};"></div></div>
        </div>
      </div>
    `;
  }).join('');
}

// ── AI INSIGHTS ───────────────────────────────────
function renderInsights(){
  const panel=document.getElementById('insightsPanel');
  if(!panel) return;

  const topStudent=ENRICHED[0];
  const lowStudents=ENRICHED.filter(s=>s.score<40);
  const avgScore=(ENRICHED.reduce((a,s)=>a+s.score,0)/ENRICHED.length).toFixed(1);
  const avgInternship=(ENRICHED.reduce((a,s)=>a+s.kpi.internships,0)/ENRICHED.length).toFixed(1);

  const insights=[
    {type:'info',icon:'🏆',text:`Top performer: <strong>${topStudent.name}</strong> (${topStudent.id}) with KPI score ${topStudent.score}. Recommend as peer mentor for ${topStudent.dept}.`},
    {type:'warn',icon:'⚠️',text:`${lowStudents.length} student${lowStudents.length!==1?'s':''} have KPI score below 40. Immediate academic counseling recommended.`},
    {type:'tip',icon:'💡',text:`AI Data Science department leads with highest avg KPI. Their hackathon participation rate (avg ${(ENRICHED.filter(s=>s.dept==='AI & Data Science').reduce((a,s)=>a+s.kpi.hackathons,0)/4).toFixed(1)}) is a model to replicate.`},
    {type:'info',icon:'📈',text:`Overall average KPI score: ${avgScore}/100. Target for next quarter: 75+.`},
    {type:'tip',icon:'💼',text:`Average internship count is ${avgInternship}. Students with 3+ internships score 25% higher on average.`},
    {type:'warn',icon:'📄',text:`Publications remain the lowest-performing KPI. Encourage research opportunities to boost scores.`},
  ];

  const existingInsights = panel.querySelectorAll('.insight-item');
  existingInsights.forEach(e=>e.remove());

  insights.forEach((ins,i)=>{
    const div=document.createElement('div');
    div.className='insight-item';
    div.style.cssText=`animation:fadeInUp .4s ease ${i*0.08}s both;`;
    const badgeClass=ins.type==='tip'?'badge-tip':ins.type==='warn'?'badge-warn':'badge-info';
    div.innerHTML=`<div class="insight-badge ${badgeClass}">${ins.icon} ${ins.type.toUpperCase()}</div><div class="insight-text">${ins.text}</div>`;
    panel.appendChild(div);
  });
}

// ── AI CHAT ───────────────────────────────────────
const AI_RESPONSES=[
  q=>{
    if(/top|best|highest/i.test(q)){
      const t=ENRICHED[0];
      return `🏆 Top performer is <strong>${t.name}</strong> (${t.id}) with KPI score <strong>${t.score}</strong> — ${t.readiness}. Department: ${DEPT_SHORT[t.dept]}.`;
    }
  },
  q=>{
    if(/average|avg/i.test(q)){
      const avg=(ENRICHED.reduce((a,s)=>a+s.score,0)/ENRICHED.length).toFixed(1);
      return `📊 Average KPI score across all ${ENRICHED.length} students is <strong>${avg}/100</strong>.`;
    }
  },
  q=>{
    if(/low|struggling|below/i.test(q)){
      const lows=ENRICHED.filter(s=>s.score<40);
      return lows.length
        ?`⚠️ ${lows.length} students have low KPI (<40): ${lows.map(s=>s.name).join(', ')}. Recommend immediate mentoring.`
        :'✅ No students are critically below threshold!';
    }
  },
  q=>{
    if(/cse|computer science/i.test(q)){
      const dept=ENRICHED.filter(s=>s.dept==='Computer Science & Engineering');
      const avg=(dept.reduce((a,s)=>a+s.score,0)/dept.length).toFixed(1);
      return `💻 CSE has ${dept.length} students with avg KPI ${avg}. Top: ${dept[0].name} (${dept[0].score}).`;
    }
  },
  q=>{
    if(/ai|data science/i.test(q)){
      const dept=ENRICHED.filter(s=>s.dept==='AI & Data Science');
      const avg=(dept.reduce((a,s)=>a+s.score,0)/dept.length).toFixed(1);
      return `🤖 AI & Data Science has ${dept.length} students with avg KPI ${avg} — highest performing department!`;
    }
  },
  q=>{
    if(/department|dept/i.test(q)){
      const depts=[...new Set(ENRICHED.map(s=>s.dept))];
      const summary=depts.map(d=>{
        const g=ENRICHED.filter(s=>s.dept===d);
        return `${DEPT_SHORT[d]}: ${(g.reduce((a,s)=>a+s.score,0)/g.length).toFixed(1)}`;
      }).join(' | ');
      return `🏢 Department averages: ${summary}`;
    }
  },
  q=>{
    if(/internship/i.test(q)){
      const sorted=[...ENRICHED].sort((a,b)=>b.kpi.internships-a.kpi.internships);
      return `💼 Most internships: ${sorted[0].name} (${sorted[0].kpi.internships}). Students with 3+ internships score significantly higher.`;
    }
  },
  q=>{
    if(/hackathon/i.test(q)){
      const sorted=[...ENRICHED].sort((a,b)=>b.kpi.hackathons-a.kpi.hackathons);
      return `⚡ Hackathon leader: ${sorted[0].name} with ${sorted[0].kpi.hackathons} hackathons! Hackathons correlate strongly with higher KPI scores.`;
    }
  },
  q=>{
    if(/recommendation|suggest|improve/i.test(q)){
      return `💡 AI Recommendations:\n1. Boost hackathon participation (high KPI impact)\n2. Encourage research publications\n3. Peer mentoring from top 5 students\n4. Industry connect for more internships`;
    }
  },
];

function getAIResponse(q){
  for(const fn of AI_RESPONSES){
    const r=fn(q);
    if(r) return r;
  }
  return `🤖 I analyzed the data for your query. The system has ${ENRICHED.length} students across 6 departments. Try asking about top performers, department stats, or improvement recommendations!`;
}

function sendChat(){
  const input=document.getElementById('chatInput');
  const msgs=document.getElementById('chatMessages');
  const q=input.value.trim();
  if(!q) return;

  const userDiv=document.createElement('div');
  userDiv.className='chat-msg user';
  userDiv.innerHTML=`<div class="msg-bubble">${q}</div><div class="msg-time">${new Date().toLocaleTimeString()}</div>`;
  msgs.appendChild(userDiv);
  input.value='';
  msgs.scrollTop=msgs.scrollHeight;

  setTimeout(()=>{
    const aiDiv=document.createElement('div');
    aiDiv.className='chat-msg ai';
    aiDiv.innerHTML=`<div class="msg-bubble">${getAIResponse(q)}</div><div class="msg-time">${new Date().toLocaleTimeString()}</div>`;
    msgs.appendChild(aiDiv);
    msgs.scrollTop=msgs.scrollHeight;
  },700);
}

// ── ANALYTICS CHARTS ─────────────────────────────
function renderAnalyticsCharts(){
  // Year-wise grouped bar
  const years=[1,2,3,4];
  const depts=[...new Set(ENRICHED.map(s=>s.dept))];
  const yearData=years.map(y=>{
    const g=ENRICHED.filter(s=>s.year===y);
    return g.length?(g.reduce((a,s)=>a+s.score,0)/g.length).toFixed(1):0;
  });

  const ctx1=document.getElementById('chartAnalyticsBar');
  if(ctx1 && !ctx1._chartjs){
    new Chart(ctx1,{
      type:'bar',
      data:{labels:years.map(y=>`Year ${y}`),datasets:[{label:'Avg KPI Score',data:yearData,backgroundColor:NEON_COLORS.slice(0,4).map(c=>c+'99'),borderColor:NEON_COLORS.slice(0,4),borderWidth:1.5,borderRadius:8}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},ticks:{color:'rgba(120,180,220,.7)'}},y:{grid:{color:'rgba(0,245,255,.05)'},ticks:{color:'rgba(120,180,220,.7)'},min:0,max:100}}}
    });
  }

  // Section pie
  const sections=[...new Set(ENRICHED.map(s=>s.section))];
  const sectionCounts=sections.map(sec=>ENRICHED.filter(s=>s.section===sec).length);
  const ctx2=document.getElementById('chartAnalyticsPie');
  if(ctx2 && !ctx2._chartjs){
    new Chart(ctx2,{
      type:'pie',data:{labels:sections.map(s=>`Section ${s}`),datasets:[{data:sectionCounts,backgroundColor:NEON_COLORS.slice(0,sections.length).map(c=>c+'88'),borderColor:NEON_COLORS.slice(0,sections.length),borderWidth:1.5}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{color:'rgba(120,180,220,.7)',padding:12}}}}
    });
  }

  // Scatter: internships vs score
  const ctx3=document.getElementById('chartScatter');
  if(ctx3 && !ctx3._chartjs){
    new Chart(ctx3,{
      type:'scatter',
      data:{datasets:[{label:'Students',data:ENRICHED.map(s=>({x:s.kpi.internships,y:s.score})),backgroundColor:'rgba(0,245,255,0.6)',borderColor:'#00f5ff',pointRadius:6,pointHoverRadius:9}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{color:'rgba(0,245,255,.05)'},ticks:{color:'rgba(120,180,220,.7)'},title:{display:true,text:'Internships',color:'rgba(0,245,255,.6)'}},y:{grid:{color:'rgba(0,245,255,.05)'},ticks:{color:'rgba(120,180,220,.7)'},title:{display:true,text:'KPI Score',color:'rgba(0,245,255,.6)'}}}}
    });
  }

  // Category averages bar
  const kpiFields=['internships','certifications','hackathons','publications','workshops','projects','club_activities','industrial_visits'];
  const kpiLabels=['Internships','Certs','Hackathons','Pubs','Workshops','Projects','Club','Visits'];
  const kpiAvgs=kpiFields.map(f=>(ENRICHED.reduce((a,s)=>a+s.kpi[f],0)/ENRICHED.length).toFixed(1));
  const ctx4=document.getElementById('chartCategories');
  if(ctx4 && !ctx4._chartjs){
    new Chart(ctx4,{
      type:'bar',
      data:{labels:kpiLabels,datasets:[{label:'Avg Count',data:kpiAvgs,backgroundColor:NEON_COLORS.map(c=>c+'88'),borderColor:NEON_COLORS,borderWidth:1.5,borderRadius:6}]},
      options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},ticks:{color:'rgba(120,180,220,.7)',font:{size:10}}},y:{grid:{color:'rgba(0,245,255,.05)'},ticks:{color:'rgba(120,180,220,.7)'}}}}
    });
  }
}

// ── ADD STUDENT MODAL ─────────────────────────────
function openAddStudent(){
  document.getElementById('addStudentModal').classList.add('active');
}
function closeModal(){
  document.getElementById('addStudentModal').classList.remove('active');
}
function addStudent(e){
  e.preventDefault();
  const id=document.getElementById('f_id').value.trim().toUpperCase();
  const name=document.getElementById('f_name').value.trim();
  const dept=document.getElementById('f_dept').value;
  const section=document.getElementById('f_section').value.trim().toUpperCase();
  const year=parseInt(document.getElementById('f_year').value);

  if(ENRICHED.find(s=>s.id===id)){
    showToast('Student ID already exists!','error'); return;
  }

  const defaultKPI={internships:0,certifications:0,hackathons:0,publications:0,workshops:0,projects:0,club_activities:0,industrial_visits:0};
  const score=calcKPIScore(defaultKPI);
  const readiness=getReadiness(score);
  ENRICHED.push({id,name,dept,section,year,gpa:0,kpi:defaultKPI,score,readiness,lastUpdated:new Date().toLocaleDateString()});
  KPI_DATA[id]=defaultKPI;

  closeModal();
  renderStudentsTable();
  showToast(`Student ${name} added successfully!`,'success');
  document.getElementById('addStudentForm').reset();
}

// ── GLOBAL SEARCH ─────────────────────────────────
document.getElementById('globalSearch')?.addEventListener('keyup',e=>{
  const q=e.target.value.trim();
  if(q.length>1){
    switchSection('students');
    document.getElementById('studentSearch').value=q;
    filterStudents();
  }
});

// ── TOAST ─────────────────────────────────────────
function showToast(msg,type='info'){
  const t=document.getElementById('toast');
  t.textContent=msg;
  t.className=`neon-toast ${type}`;
  t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),3000);
}

// ── INIT ──────────────────────────────────────────
document.addEventListener('DOMContentLoaded',()=>{
  initDashboardStats();
  initDashboardCharts();
  renderStudentsTable();
  populateKPIDropdown();
  loadStudentKPI();
});
