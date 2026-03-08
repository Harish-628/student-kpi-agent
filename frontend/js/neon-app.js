/* ============================================
   NEURALKPI — Main Application Logic
   Global Loader Integration Attached
   ============================================ */

const loader = document.getElementById('neuralLoader');
const loaderStatus = document.getElementById('loaderStatus');

function showLoader(statusText) {
  if (loader) {
    if (statusText) loaderStatus.textContent = statusText;
    loader.classList.remove('loader-hidden');
  }
}

function hideLoader() {
  if (loader) {
    loader.classList.add('loader-hidden');
  }
}

// Fade out on initial load
window.addEventListener('load', () => {
  setTimeout(hideLoader, 500);
});


// ── STUDENT DATABASE ──────────────────────────────
const STUDENTS = [
  { id: "CSE001", name: "Arjun Sharma", dept: "Computer Science & Engineering", section: "A", year: 3, gpa: 9.1 },
  { id: "CSE002", name: "Priya Patel", dept: "Computer Science & Engineering", section: "A", year: 3, gpa: 8.7 },
  { id: "CSE003", name: "Rahul Verma", dept: "Computer Science & Engineering", section: "B", year: 2, gpa: 7.8 },
  { id: "CSE004", name: "Sneha Iyer", dept: "Computer Science & Engineering", section: "B", year: 4, gpa: 8.9 },
  { id: "CSE005", name: "Vikram Nair", dept: "Computer Science & Engineering", section: "C", year: 1, gpa: 7.2 },
  { id: "ECE001", name: "Ananya Krishnan", dept: "Electronics & Communication", section: "A", year: 3, gpa: 9.3 },
  { id: "ECE002", name: "Karthik Reddy", dept: "Electronics & Communication", section: "A", year: 2, gpa: 8.1 },
  { id: "ECE003", name: "Divya Menon", dept: "Electronics & Communication", section: "B", year: 4, gpa: 8.5 },
  { id: "ECE004", name: "Sai Kumar", dept: "Electronics & Communication", section: "C", year: 1, gpa: 7.0 },
  { id: "ME001", name: "Rohit Singh", dept: "Mechanical Engineering", section: "A", year: 4, gpa: 8.2 },
  { id: "ME002", name: "Kavitha Suresh", dept: "Mechanical Engineering", section: "B", year: 2, gpa: 7.5 },
  { id: "ME003", name: "Arun Raj", dept: "Mechanical Engineering", section: "A", year: 3, gpa: 8.0 },
  { id: "CE001", name: "Deepa Thomas", dept: "Civil Engineering", section: "A", year: 3, gpa: 7.9 },
  { id: "CE002", name: "Harish Kumar", dept: "Civil Engineering", section: "B", year: 2, gpa: 7.3 },
  { id: "IT001", name: "Meera Nambiar", dept: "Information Technology", section: "A", year: 4, gpa: 9.0 },
  { id: "IT002", name: "Ajay Chandran", dept: "Information Technology", section: "A", year: 3, gpa: 8.6 },
  { id: "IT003", name: "Lakshmi Pillai", dept: "Information Technology", section: "B", year: 2, gpa: 7.8 },
  { id: "AI001", name: "Ravi Teja", dept: "AI & Data Science", section: "A", year: 3, gpa: 9.4 },
  { id: "AI002", name: "Pooja Gupta", dept: "AI & Data Science", section: "A", year: 2, gpa: 8.3 },
  { id: "AI003", name: "Nikhil Bose", dept: "AI & Data Science", section: "B", year: 4, gpa: 9.1 },
  { id: "AI004", name: "Sreya Nair", dept: "AI & Data Science", section: "A", year: 1, gpa: 7.6 },
];

const KPI_DATA = {
  CSE001: { internships: 4, certifications: 10, hackathons: 6, publications: 3, workshops: 12, projects: 8, club_activities: 6, industrial_visits: 8 },
  CSE002: { internships: 3, certifications: 8, hackathons: 5, publications: 2, workshops: 9, projects: 6, club_activities: 5, industrial_visits: 7 },
  CSE003: { internships: 1, certifications: 4, hackathons: 2, publications: 0, workshops: 5, projects: 3, club_activities: 2, industrial_visits: 3 },
  CSE004: { internships: 3, certifications: 9, hackathons: 4, publications: 2, workshops: 11, projects: 7, club_activities: 5, industrial_visits: 8 },
  CSE005: { internships: 0, certifications: 2, hackathons: 1, publications: 0, workshops: 3, projects: 2, club_activities: 1, industrial_visits: 2 },
  ECE001: { internships: 4, certifications: 11, hackathons: 7, publications: 3, workshops: 13, projects: 9, club_activities: 7, industrial_visits: 9 },
  ECE002: { internships: 2, certifications: 5, hackathons: 3, publications: 1, workshops: 7, projects: 5, club_activities: 3, industrial_visits: 5 },
  ECE003: { internships: 2, certifications: 7, hackathons: 3, publications: 1, workshops: 8, projects: 5, club_activities: 4, industrial_visits: 6 },
  ECE004: { internships: 0, certifications: 1, hackathons: 1, publications: 0, workshops: 2, projects: 1, club_activities: 1, industrial_visits: 2 },
  ME001: { internships: 2, certifications: 6, hackathons: 2, publications: 1, workshops: 7, projects: 5, club_activities: 3, industrial_visits: 6 },
  ME002: { internships: 1, certifications: 3, hackathons: 1, publications: 0, workshops: 4, projects: 2, club_activities: 2, industrial_visits: 3 },
  ME003: { internships: 2, certifications: 5, hackathons: 2, publications: 0, workshops: 6, projects: 4, club_activities: 3, industrial_visits: 5 },
  CE001: { internships: 1, certifications: 4, hackathons: 2, publications: 0, workshops: 5, projects: 3, club_activities: 2, industrial_visits: 5 },
  CE002: { internships: 1, certifications: 2, hackathons: 1, publications: 0, workshops: 3, projects: 2, club_activities: 1, industrial_visits: 3 },
  IT001: { internships: 4, certifications: 10, hackathons: 5, publications: 2, workshops: 11, projects: 8, club_activities: 6, industrial_visits: 8 },
  IT002: { internships: 3, certifications: 8, hackathons: 5, publications: 2, workshops: 10, projects: 7, club_activities: 5, industrial_visits: 7 },
  IT003: { internships: 1, certifications: 4, hackathons: 2, publications: 0, workshops: 5, projects: 3, club_activities: 2, industrial_visits: 4 },
  AI001: { internships: 5, certifications: 12, hackathons: 8, publications: 4, workshops: 14, projects: 10, club_activities: 8, industrial_visits: 9 },
  AI002: { internships: 2, certifications: 6, hackathons: 4, publications: 1, workshops: 8, projects: 6, club_activities: 4, industrial_visits: 5 },
  AI003: { internships: 4, certifications: 11, hackathons: 7, publications: 3, workshops: 13, projects: 9, club_activities: 7, industrial_visits: 8 },
  AI004: { internships: 0, certifications: 2, hackathons: 1, publications: 0, workshops: 3, projects: 2, club_activities: 1, industrial_visits: 2 },
};

// ── SCORE CALCULATION ─────────────────────────────
const WEIGHTS = { internships: 10, certifications: 5, hackathons: 7, publications: 12, workshops: 3, projects: 8, club_activities: 4, industrial_visits: 3, value_added_courses: 4 };
const MAX_VALS = { internships: 5, certifications: 12, hackathons: 8, publications: 4, workshops: 15, projects: 10, club_activities: 8, industrial_visits: 10, value_added_courses: 6 };

function calcKPIScore(kpi) {
  let score = 0;
  for (const [k, w] of Object.entries(WEIGHTS)) {
    const val = kpi[k] || 0;
    score += (Math.min(val, MAX_VALS[k]) / MAX_VALS[k]) * w;
  }
  return Math.min(parseFloat(score.toFixed(1)), 100);
}

function getReadiness(score) {
  if (score >= 80) return "High Readiness";
  if (score >= 60) return "Moderate Readiness";
  if (score >= 40) return "Developing";
  return "Low Readiness";
}

function getReadinessBadge(r) {
  if (r.includes("High")) return `<span class="neon-badge badge-high">${r}</span>`;
  if (r.includes("Moderate")) return `<span class="neon-badge badge-moderate">${r}</span>`;
  if (r.includes("Developing")) return `<span class="neon-badge badge-developing">${r}</span>`;
  return `<span class="neon-badge badge-low">${r}</span>`;
}

function getScoreColor(s) { return s >= 80 ? 'var(--neon-green)' : s >= 60 ? 'var(--neon-cyan)' : s >= 40 ? 'var(--neon-orange)' : 'var(--neon-pink)'; }

// Retrieve user info early for filtering
const storedUser = JSON.parse(localStorage.getItem('kpi_user') || '{"name":"Admin","role":"admin"}');

// Build enriched student list, filtering by HOD/Faculty department if applicable
let rawStudents = STUDENTS;
if ((storedUser.role === 'hod' || storedUser.role === 'faculty') && storedUser.email) {
  const deptMap = {
    'hod.cse@kpi.edu': 'Computer Science & Engineering',
    'fac.cse@kpi.edu': 'Computer Science & Engineering',
    'hod.ece@kpi.edu': 'Electronics & Communication',
    'fac.ece@kpi.edu': 'Electronics & Communication',
    'hod.mech@kpi.edu': 'Mechanical Engineering',
    'fac.mech@kpi.edu': 'Mechanical Engineering',
    'hod.ce@kpi.edu': 'Civil Engineering',
    'fac.ce@kpi.edu': 'Civil Engineering',
    'hod.it@kpi.edu': 'Information Technology',
    'fac.it@kpi.edu': 'Information Technology',
    'hod.ai@kpi.edu': 'AI & Data Science',
    'fac.ai@kpi.edu': 'AI & Data Science'
  };
  const hodDept = deptMap[storedUser.email];
  if (hodDept) {
    rawStudents = STUDENTS.filter(s => s.dept === hodDept);
  }
}

let ENRICHED = [];

async function fetchEnrichedData() {
  try {
    const token = localStorage.getItem('kpi_token') || '';

    // First fetch students
    const res = await fetch('http://localhost:8000/api/students?limit=1000', {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!res.ok) throw new Error('Failed to fetch students');
    const apiStudents = await res.json();

    // Fetch KPI for each student
    const enrichedPromises = apiStudents.map(async (s) => {
      let kpi = { internships: 0, certifications: 0, hackathons: 0, publications: 0, workshops: 0, projects: 0, club_activities: 0, industrial_visits: 0 };
      let scoreObj = {
        kpi_score: 0,
        career_readiness_score: 'Low Readiness'
      };

      try {
        const kpiRes = await fetch(`http://localhost:8000/api/student/${s.student_id}/kpi`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (kpiRes.ok) kpi = await kpiRes.json();

        const scoreRes = await fetch(`http://localhost:8000/api/student/${s.student_id}/score`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (scoreRes.ok) scoreObj = await scoreRes.json();

      } catch (err) {
        console.warn(`Failed to fetch KPI/Score for ${s.student_id}`, err);
      }

      return {
        id: s.student_id,
        name: s.name,
        dept: s.department,
        section: s.section,
        year: s.year,
        gpa: s.gpa,
        kpi: kpi,
        score: scoreObj.kpi_score || 0,
        readiness: scoreObj.career_readiness_score || 'Low Readiness',
        lastUpdated: new Date().toLocaleDateString()
      };
    });

    ENRICHED = await Promise.all(enrichedPromises);
    ENRICHED.sort((a, b) => b.score - a.score);

    // Re-render UI components now that we have data
    if (typeof renderStudentsTable === 'function') renderStudentsTable();
    if (typeof initDashboardStats === 'function') initDashboardStats();
    if (typeof populateKPIDropdown === 'function') populateKPIDropdown();
    if (typeof initDashboardCharts === 'function') initDashboardCharts();
    if (document.getElementById('section-kpi')?.classList.contains('active')) loadStudentKPI();
  } catch (error) {
    console.error("Falling back to static ENRICHED data:", error);
    // Fallback to old behavior if API lacks data or fails
    ENRICHED = rawStudents.map(s => {
      const kpi = KPI_DATA[s.id] || { internships: 0, certifications: 0, hackathons: 0, publications: 0, workshops: 0, projects: 0, club_activities: 0, industrial_visits: 0 };
      const score = calcKPIScore(kpi);
      const readiness = getReadiness(score);
      const lastUpdated = new Date(Date.now() - Math.floor(Math.random() * 7) * 86400000).toLocaleDateString();
      return { ...s, kpi, score, readiness, lastUpdated };
    }).sort((a, b) => b.score - a.score);

    if (typeof renderStudentsTable === 'function') renderStudentsTable();
    if (typeof initDashboardStats === 'function') initDashboardStats();
    if (typeof populateKPIDropdown === 'function') populateKPIDropdown();
    if (typeof initDashboardCharts === 'function') initDashboardCharts();
  }
}

// Kick off data fetch immediately
fetchEnrichedData();

// ── CHART.JS DEFAULTS ─────────────────────────────
Chart.defaults.color = 'rgba(120,180,220,0.7)';
Chart.defaults.borderColor = 'rgba(0,245,255,0.08)';
Chart.defaults.font.family = "'Inter', sans-serif";

const NEON_COLORS = [
  '#00f5ff', '#bf00ff', '#ff006e', '#39ff14',
  '#0080ff', '#ff6600', '#fff000', '#ff00cc',
  '#00ffaa', '#7700ff'
];

function makeGradient(ctx, c1, c2) {
  const g = ctx.createLinearGradient(0, 0, 0, 300);
  g.addColorStop(0, c1); g.addColorStop(1, c2);
  return g;
}

// ── DEPT ABBREVIATIONS ────────────────────────────
const DEPT_SHORT = {
  "Computer Science & Engineering": "CSE",
  "Electronics & Communication": "ECE",
  "Mechanical Engineering": "MECH",
  "Civil Engineering": "CE",
  "Information Technology": "IT",
  "AI & Data Science": "AIDS",
};

// ── SIDEBAR NAV ───────────────────────────────────
let currentSection = 'dashboard';
document.querySelectorAll('.nav-link[data-section]').forEach(btn => {
  btn.addEventListener('click', () => { switchSection(btn.dataset.section); });
});

function switchSection(name) {
  document.querySelectorAll('.nav-link').forEach(b => b.classList.remove('active'));
  document.querySelector(`.nav-link[data-section="${name}"]`)?.classList.add('active');
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  const sec = document.getElementById(`section-${name}`);
  if (sec) sec.classList.add('active');
  document.getElementById('pageTitle').textContent = ({
    dashboard: 'DASHBOARD', students: 'STUDENTS', faculty: 'FACULTY', hods: 'HOD DATABASE', kpi: 'KPI TRACKER',
    'fac-kpi': 'FACULTY KPI', 'hod-kpi': 'HOD KPI', 'hod-profile': 'PERSONAL INFO', 'fac-profile': 'PERSONAL INFO', leaderboard: 'LEADERBOARD', ai: 'AI AGENT', analytics: 'ANALYTICS',
    recommendations: 'AI RECOMMENDATIONS', 'idea-enhancer': 'IDEA ENHANCER'
  })[name] || name.toUpperCase();
  currentSection = name;
  if (name === 'leaderboard') renderLeaderboard();
  if (name === 'analytics') renderAnalyticsCharts();
  if (name === 'kpi') loadStudentKPI();
  if (name === 'fac-kpi') initFacultyKPI();
  if (name === 'hod-profile') renderHODProfile();
  if (name === 'fac-profile') renderFacProfile();
  if (name === 'hod-kpi') initAdminHODKPI();
  if (name === 'recommendations') loadRecommendationsView();
}

// Sidebar collapse
document.getElementById('toggleSidebar').addEventListener('click', () => {
  document.getElementById('sidebar').classList.toggle('collapsed');
});

// UI Permissions
// Faculty UI Permissions
if (storedUser && (storedUser.role === 'hod' || storedUser.role === 'admin')) {
  const navFac = document.getElementById('navFacultyBtn');
  if (navFac) navFac.style.display = 'flex';
  const navFacKpi = document.getElementById('navFacKpiBtn');
  if (navFacKpi) navFacKpi.style.display = 'flex';
}
// HOD Personal profile permission
if (storedUser && storedUser.role === 'hod') {
  const navHod = document.getElementById('navHodProfileBtn');
  if (navHod) navHod.style.display = 'flex';
}
// Faculty Personal profile permission
if (storedUser && storedUser.role === 'faculty') {
  const navFacProfile = document.getElementById('navFacProfileBtn');
  if (navFacProfile) navFacProfile.style.display = 'flex';
}
// Idea Enhancer permission (Students & Faculty & HOD)
if (storedUser) {
  const navIdea = document.getElementById('navIdeaEnhancerBtn');
  if (navIdea) navIdea.style.display = 'flex';
}
// Admin exclusively viewing HOD DB and HOD KPIs
if (storedUser && storedUser.role === 'admin') {
  const navHods = document.getElementById('navHodsBtn');
  if (navHods) navHods.style.display = 'flex';
  const navHodKpi = document.getElementById('navHodKpiBtn');
  if (navHodKpi) navHodKpi.style.display = 'flex';
  const addFacBtn = document.getElementById('addFacultyBtn');
  if (addFacBtn) addFacBtn.style.display = 'block';
  const addHodBtn = document.getElementById('addHodBtn');
  if (addHodBtn) addHodBtn.style.display = 'block';
}

// Logout
document.getElementById('logoutBtn').addEventListener('click', () => {
  showLoader("De-authenticating Session...");

  localStorage.removeItem('kpi_user');
  localStorage.removeItem('kpi_token');

  setTimeout(() => {
    window.location.href = 'index.html';
  }, 800);
});


// Load user info
const userInfo = storedUser;
document.getElementById('sidebarName').textContent = userInfo.name || 'Admin';
document.getElementById('sidebarRole').textContent = userInfo.role || 'admin';
document.getElementById('sidebarAvatar').textContent = (userInfo.name || 'A')[0].toUpperCase();

// ── FACULTY & HOD DB RENDER ───────────────────────
const HOD_LIST = [
  { id: 'hod.cse@kpi.edu', name: 'Dr. Alan Turing', dept: 'Computer Science & Engineering', status: 'Active' },
  { id: 'hod.ece@kpi.edu', name: 'Dr. Claude Shannon', dept: 'Electronics & Communication', status: 'Active' },
  { id: 'hod.mech@kpi.edu', name: 'Dr. Henry Ford', dept: 'Mechanical Engineering', status: 'Active' },
  { id: 'hod.ce@kpi.edu', name: 'Dr. John Smeaton', dept: 'Civil Engineering', status: 'Active' },
  { id: 'hod.it@kpi.edu', name: 'Dr. Tim Berners-Lee', dept: 'Information Technology', status: 'Active' },
  { id: 'hod.ai@kpi.edu', name: 'Dr. Geoffrey Hinton', dept: 'AI & Data Science', status: 'Active' }
];

const FACULTY_DB = [
  // CSE
  { id: 'FAC01', name: 'Dr. Ramesh Kumar', dept: 'Computer Science & Engineering', spec: 'AI & Machine Learning', status: 'Active', kpis: { iv: 3, ws: 5, cert: 2, pm: 12 } },
  { id: 'FAC02', name: 'Prof. Anjali Desai', dept: 'Computer Science & Engineering', spec: 'Cloud Computing', status: 'Active', kpis: { iv: 1, ws: 2, cert: 4, pm: 8 } },
  { id: 'FAC03', name: 'Dr. Vivek Sharma', dept: 'Computer Science & Engineering', spec: 'Cybersecurity', status: 'Active', kpis: { iv: 2, ws: 4, cert: 3, pm: 10 } },
  { id: 'FAC04', name: 'Prof. Neha Singh', dept: 'Computer Science & Engineering', spec: 'Data Structures', status: 'Active', kpis: { iv: 4, ws: 3, cert: 1, pm: 6 } },
  { id: 'FAC05', name: 'Dr. Arjun Patel', dept: 'Computer Science & Engineering', spec: 'Quantum Computing', status: 'On Leave', kpis: { iv: 0, ws: 1, cert: 2, pm: 2 } },
  // ECE
  { id: 'FAC06', name: 'Dr. Vikram Seth', dept: 'Electronics & Communication', spec: 'VLSI Design', status: 'Active', kpis: { iv: 5, ws: 2, cert: 3, pm: 9 } },
  { id: 'FAC07', name: 'Prof. Neha Gupta', dept: 'Electronics & Communication', spec: 'IoT Systems', status: 'Active', kpis: { iv: 4, ws: 3, cert: 5, pm: 15 } },
  { id: 'FAC08', name: 'Dr. Rohan Mehra', dept: 'Electronics & Communication', spec: 'Embedded Systems', status: 'Active', kpis: { iv: 2, ws: 5, cert: 1, pm: 11 } },
  { id: 'FAC09', name: 'Prof. Anil Kapoor', dept: 'Electronics & Communication', spec: 'Signal Processing', status: 'Active', kpis: { iv: 1, ws: 4, cert: 2, pm: 8 } },
  { id: 'FAC10', name: 'Dr. Priya Reddy', dept: 'Electronics & Communication', spec: 'Wireless Comms', status: 'Active', kpis: { iv: 3, ws: 2, cert: 4, pm: 14 } },
  // MECH
  { id: 'FAC11', name: 'Dr. Rajesh Pillai', dept: 'Mechanical Engineering', spec: 'Thermodynamics', status: 'Active', kpis: { iv: 5, ws: 2, cert: 1, pm: 10 } },
  { id: 'FAC12', name: 'Prof. Sanjay Dutt', dept: 'Mechanical Engineering', spec: 'Fluid Mechanics', status: 'Active', kpis: { iv: 4, ws: 3, cert: 2, pm: 8 } },
  { id: 'FAC13', name: 'Dr. Kiran Rao', dept: 'Mechanical Engineering', spec: 'Robotics', status: 'Active', kpis: { iv: 6, ws: 1, cert: 3, pm: 12 } },
  { id: 'FAC14', name: 'Prof. Amit Shah', dept: 'Mechanical Engineering', spec: 'Manufacturing', status: 'Active', kpis: { iv: 2, ws: 5, cert: 1, pm: 7 } },
  { id: 'FAC15', name: 'Dr. Sneha Verma', dept: 'Mechanical Engineering', spec: 'Automotive Eng', status: 'On Leave', kpis: { iv: 0, ws: 1, cert: 1, pm: 3 } },
  // CE
  { id: 'FAC16', name: 'Dr. Suresh Reddy', dept: 'Civil Engineering', spec: 'Structural Eng.', status: 'Active', kpis: { iv: 6, ws: 1, cert: 2, pm: 9 } },
  { id: 'FAC17', name: 'Prof. Manoj Tiwari', dept: 'Civil Engineering', spec: 'Transportation', status: 'Active', kpis: { iv: 4, ws: 3, cert: 1, pm: 6 } },
  { id: 'FAC18', name: 'Dr. Deepa Nair', dept: 'Civil Engineering', spec: 'Geotech Eng.', status: 'Active', kpis: { iv: 3, ws: 4, cert: 5, pm: 15 } },
  { id: 'FAC19', name: 'Prof. Rahul Bose', dept: 'Civil Engineering', spec: 'Water Resources', status: 'Active', kpis: { iv: 5, ws: 2, cert: 3, pm: 11 } },
  { id: 'FAC20', name: 'Dr. Karthik Raj', dept: 'Civil Engineering', spec: 'Urban Planning', status: 'Active', kpis: { iv: 2, ws: 5, cert: 2, pm: 8 } },
  // IT
  { id: 'FAC21', name: 'Prof. Meera Iyer', dept: 'Information Technology', spec: 'Cybersecurity', status: 'Active', kpis: { iv: 2, ws: 6, cert: 3, pm: 14 } },
  { id: 'FAC22', name: 'Dr. Ajay Verma', dept: 'Information Technology', spec: 'Network Security', status: 'Active', kpis: { iv: 4, ws: 2, cert: 1, pm: 9 } },
  { id: 'FAC23', name: 'Prof. Sunita Shenoy', dept: 'Information Technology', spec: 'Data Mining', status: 'Active', kpis: { iv: 3, ws: 4, cert: 4, pm: 11 } },
  { id: 'FAC24', name: 'Dr. Tarun Kumar', dept: 'Information Technology', spec: 'Cloud Architecture', status: 'Active', kpis: { iv: 1, ws: 5, cert: 2, pm: 7 } },
  { id: 'FAC25', name: 'Prof. Pooja Hegde', dept: 'Information Technology', spec: 'Software Eng.', status: 'On Leave', kpis: { iv: 0, ws: 0, cert: 1, pm: 2 } },
  // AIDS
  { id: 'FAC26', name: 'Prof. Amit Bose', dept: 'AI & Data Science', spec: 'Deep Learning', status: 'Active', kpis: { iv: 3, ws: 4, cert: 6, pm: 18 } },
  { id: 'FAC27', name: 'Dr. Manish Pandey', dept: 'AI & Data Science', spec: 'Computer Vision', status: 'Active', kpis: { iv: 5, ws: 2, cert: 4, pm: 12 } },
  { id: 'FAC28', name: 'Prof. Shreya Ghoshal', dept: 'AI & Data Science', spec: 'NLP', status: 'Active', kpis: { iv: 2, ws: 3, cert: 5, pm: 14 } },
  { id: 'FAC29', name: 'Dr. Rakesh Jhunjhunwala', dept: 'AI & Data Science', spec: 'Big Data', status: 'Active', kpis: { iv: 4, ws: 5, cert: 3, pm: 10 } },
  { id: 'FAC30', name: 'Prof. Nidhi Awasthi', dept: 'AI & Data Science', spec: 'Reinforcement Learning', status: 'Active', kpis: { iv: 1, ws: 6, cert: 2, pm: 9 } }
];

function getFilteredFaculty() {
  let displayFac = FACULTY_DB;
  if (userInfo && userInfo.role === 'hod' && userInfo.email) {
    const deptMap = {
      'hod.cse@kpi.edu': 'Computer Science & Engineering',
      'hod.ece@kpi.edu': 'Electronics & Communication',
      'hod.mech@kpi.edu': 'Mechanical Engineering',
      'hod.ce@kpi.edu': 'Civil Engineering',
      'hod.it@kpi.edu': 'Information Technology',
      'hod.ai@kpi.edu': 'AI & Data Science'
    };
    const hodDept = deptMap[userInfo.email];
    if (hodDept) displayFac = FACULTY_DB.filter(f => f.dept === hodDept);
  }
  return displayFac;
}

function renderFacultyTable() {
  const tbody = document.getElementById('facultyTbody');
  if (!tbody) return;
  const displayFac = getFilteredFaculty();

  tbody.innerHTML = displayFac.map((f, i) => `
    <tr style="animation:fadeInUp .3s ease ${i * 0.03}s both;">
      <td><span style="font-family:var(--font-mono);color:var(--neon-cyan);font-size:.8rem;">${f.id}</span></td>
      <td><strong style="color:#e8f4ff;">${f.name}</strong></td>
      <td><span style="color:rgba(120,180,220,.7);font-size:.82rem;">${DEPT_SHORT[f.dept] || f.dept}</span></td>
      <td><span style="color:rgba(120,180,220,.7);">${f.spec}</span></td>
      <td><span class="neon-badge" style="${f.status === 'Active' ? 'background:rgba(57,255,20,.1);color:var(--neon-green);border:1px solid rgba(57,255,20,.2);' : 'background:rgba(255,0,110,.1);color:var(--neon-pink);border:1px solid rgba(255,0,110,.2);'}"> ${f.status}</span></td>
    </tr>
  `).join('');
}

// ── DASHBOARD STATS ───────────────────────────────
function initDashboardStats() {
  if (userInfo && userInfo.role === 'student' && userInfo.email) {
    document.body.classList.add('student-mode');
    const sId = userInfo.email.split('@')[0].toUpperCase();
    const studentInfo = ENRICHED.find(s => s.id === sId);

    if (studentInfo) {
      document.getElementById('adminDashboardView').style.display = 'none';
      document.getElementById('studentDashboardView').style.display = 'block';

      // Hide students tab in sidebar
      const studentsTab = document.querySelector('.nav-link[data-section="students"]');
      if (studentsTab) studentsTab.style.display = 'none';

      document.getElementById('studentProfileName').textContent = studentInfo.name;
      document.getElementById('studentProfileId').textContent = studentInfo.id;
      document.getElementById('studentProfileDept').textContent = studentInfo.dept;
      document.getElementById('studentProfileYear').textContent = studentInfo.year;
      document.getElementById('studentProfileSection').textContent = studentInfo.section;
      document.getElementById('studentProfileScore').textContent = studentInfo.score;
      document.getElementById('studentProfileScore').style.color = getScoreColor(studentInfo.score);
      document.getElementById('studentProfileReadiness').innerHTML = getReadinessBadge(studentInfo.readiness);

      const addBtn = document.getElementById('addStudentBtn');
      if (addBtn) addBtn.style.display = 'none';

      const searchContainer = document.getElementById('kpiSearchContainer');
      if (searchContainer) searchContainer.style.display = 'none';

      // --- AI Recommendations Logic ---

      // Target Goal
      const kpiNames = {
        internships: 'Internships', certifications: 'Certifications',
        hackathons: 'Hackathons', publications: 'Publications',
        workshops: 'Workshops', projects: 'Projects',
        club_activities: 'Club Activities', industrial_visits: 'Industrial Visits'
      };

      let minVal = Infinity;
      let minKey = '';
      for (const [key, val] of Object.entries(studentInfo.kpi)) {
        if (val < minVal) { minVal = val; minKey = key; }
      }

      const targetTxt = `Your lowest performing area is <strong>${kpiNames[minKey]}</strong> (${minVal} recorded). Focus your efforts on securing more ${kpiNames[minKey]} this semester to boost your overall KPI readiness level.`;
      const targetEl = document.getElementById('aiTargetGoal');
      if (targetEl) targetEl.innerHTML = targetTxt;

      // Peer Comparison
      const deptPeers = ENRICHED.filter(s => s.dept === studentInfo.dept);
      const deptAvg = deptPeers.length > 0 ? (deptPeers.reduce((a, s) => a + s.score, 0) / deptPeers.length) : studentInfo.score;
      const diff = studentInfo.score - deptAvg;

      let peerTxt = '';
      if (Math.abs(diff) < 2) {
        peerTxt = `You are performing <strong>on par</strong> with your peers in ${studentInfo.dept} (Avg: ${deptAvg.toFixed(1)}).`;
      } else if (diff > 0) {
        peerTxt = `Great job! You are <strong>${diff.toFixed(1)} points above</strong> the ${studentInfo.dept} average of ${deptAvg.toFixed(1)}.`;
      } else {
        peerTxt = `You are currently <strong>${Math.abs(diff).toFixed(1)} points below</strong> the ${studentInfo.dept} average of ${deptAvg.toFixed(1)}.`;
      }

      const peerEl = document.getElementById('aiPeerComparison');
      if (peerEl) peerEl.innerHTML = peerTxt;

      // Trending Skills
      const trendTxt = `Students in <strong>${studentInfo.dept}</strong> are currently focusing heavily on <strong>Certifications</strong> and <strong>Hackathons</strong>. Participating in these areas will give you a competitive edge in upcoming placements.`;
      const trendEl = document.getElementById('aiTrendingSkill');
      if (trendEl) trendEl.innerHTML = trendTxt;

      // Action Plan
      let actionTxt = '';
      if (studentInfo.readiness === 'High Readiness') {
        actionTxt = `You are on track for top-tier placements! <strong>Next step:</strong> Focus on high-impact projects and finalizing your resume.`;
      } else if (studentInfo.readiness === 'Moderate Readiness') {
        actionTxt = `You have a solid foundation. <strong>Next step:</strong> Secure at least one more internship or publish a paper to elevate your profile to High Readiness.`;
      } else {
        actionTxt = `Your profile needs active development. <strong>Next step:</strong> Start attending workshops immediately and clear any pending certifications to build momentum.`;
      }
      const actionEl = document.getElementById('aiActionPlan');
      if (actionEl) actionEl.innerHTML = actionTxt;

      return;
    }
  }

  // Enable Add Student & CSV buttons for Admin/HOD only
  if (userInfo && (userInfo.role === 'admin' || userInfo.role === 'hod')) {
    const csvBtn = document.getElementById('uploadCsvBtn');
    if (csvBtn) csvBtn.style.display = 'inline-block';
  } else {
    // Hide Add Student button for non-admins (already default hidden for CSV)
    const addBtn = document.getElementById('addStudentBtn');
    if (addBtn) addBtn.style.display = 'none';
  }

  // Hide the department sort filter for HODs and Faculty
  if (userInfo && (userInfo.role === 'hod' || userInfo.role === 'faculty')) {
    const deptFilter = document.getElementById('deptFilter');
    if (deptFilter) deptFilter.style.display = 'none';
  }

  const total = ENRICHED.length;
  const avg = (ENRICHED.reduce((a, s) => a + s.score, 0) / total).toFixed(1);
  const high = ENRICHED.filter(s => s.readiness === 'High Readiness').length;
  animCounter(document.getElementById('cardStudents'), total, 1200);
  animCounter(document.getElementById('cardAvgKPI'), parseFloat(avg), 1500, true);
  animCounter(document.getElementById('cardHighReady'), high, 800);
}

function animCounter(el, target, dur = 1200, isFloat = false) {
  if (!el) return;
  let start = 0, frames = Math.ceil(dur / 16);
  let step = target / frames;
  const run = () => {
    start = Math.min(start + step, target);
    el.textContent = isFloat ? start.toFixed(1) : Math.ceil(start);
    if (start < target) requestAnimationFrame(run);
  };
  requestAnimationFrame(run);
}

// ── DASHBOARD CHARTS ──────────────────────────────
let radarChart, doughnutChart, barChart, lineChart;

function initDashboardCharts() {
  // Destroy existing chart instances to prevent "Canvas already in use" errors on re-render
  [radarChart, doughnutChart, barChart, lineChart].forEach(c => c?.destroy());
  radarChart = doughnutChart = barChart = lineChart = null;
  // Also destroy student radar chart if it exists on the canvas
  const _srcv = document.getElementById('studentRadarChart');
  if (_srcv) { const _sInst = Chart.getChart(_srcv); if (_sInst) _sInst.destroy(); }

  if (userInfo && userInfo.role === 'student' && userInfo.email) {
    const sId = userInfo.email.split('@')[0].toUpperCase();
    const studentInfo = ENRICHED.find(s => s.id === sId);

    if (studentInfo) {
      const fields = ['internships', 'certifications', 'hackathons', 'publications', 'workshops', 'projects', 'club_activities', 'industrial_visits'];
      const labels = ['Internships', 'Certs', 'Hackathons', 'Publications', 'Workshops', 'Projects', 'Club', 'Ind. Visits'];
      const myVals = fields.map(f => studentInfo.kpi[f]);

      new Chart(document.getElementById('studentRadarChart'), {
        type: 'radar',
        data: {
          labels,
          datasets: [{
            label: 'My KPI',
            data: myVals,
            borderColor: '#00f5ff',
            backgroundColor: 'rgba(0,245,255,0.15)',
            pointBackgroundColor: '#00f5ff',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#00f5ff',
            borderWidth: 2,
            pointRadius: 4,
            pointHoverRadius: 9, // Enlarge point significantly on hover
          }]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          scales: {
            r: {
              grid: { color: 'rgba(0,245,255,0.1)' },
              angleLines: { color: 'rgba(0,245,255,0.15)' },
              ticks: { backdropColor: 'transparent', color: 'rgba(0,245,255,0.5)', font: { size: 9 } },
              pointLabels: { color: 'rgba(120,180,220,1)', font: { size: 12, weight: 'bold' } }
            }
          },
          animation: {
            duration: 400,
            easing: 'easeOutQuart'
          },
          interaction: {
            mode: 'nearest',
            intersect: true,
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(17, 24, 39, 0.95)',
              titleFont: { size: 15, family: "'Inter', sans-serif", weight: 'bold' },
              bodyFont: { size: 14, family: "'Inter', sans-serif" },
              padding: 14,
              cornerRadius: 10,
              borderColor: '#00f5ff',
              borderWidth: 1,
              displayColors: false,
              callbacks: {
                title: function (tooltipItems) {
                  return tooltipItems[0].label + " Performance";
                },
                label: function (context) {
                  return `⭐ My Score: ${context.parsed.r}`;
                },
                afterBody: function (tooltipItems) {
                  const category = tooltipItems[0].label;

                  // Field mapper directly injected to avoid scope issues
                  const mapLabelToField = {
                    'Internships': 'internships',
                    'Certs': 'certifications',
                    'Hackathons': 'hackathons',
                    'Publications': 'publications',
                    'Workshops': 'workshops',
                    'Projects': 'projects',
                    'Club': 'club_activities',
                    'Ind. Visits': 'industrial_visits'
                  };

                  const fieldName = mapLabelToField[category];
                  if (!fieldName) return '';

                  // Calculate how the student is doing compared to the average
                  const deptPeers = ENRICHED.filter(s => s.dept === studentInfo.dept);
                  const deptAvg = deptPeers.length > 0 ? (deptPeers.reduce((a, s) => a + s.kpi[fieldName], 0) / deptPeers.length).toFixed(1) : studentInfo.kpi[fieldName];

                  return `\n📊 Dept Average: ${deptAvg}`;
                }
              }
            }
          },
        }
      });

      // ── My KPI vs Dept Average horizontal bar chart ──
      const hBarCtx = document.getElementById('studentHBarChart');
      if (hBarCtx) {
        const existingHBar = Chart.getChart(hBarCtx);
        if (existingHBar) existingHBar.destroy();
        const hFields = ['internships', 'certifications', 'hackathons', 'publications', 'workshops', 'projects', 'club_activities', 'industrial_visits'];
        const hLabels = ['Internships', 'Certifications', 'Hackathons', 'Publications', 'Workshops', 'Projects', 'Club', 'Ind. Visits'];
        const myValsH = hFields.map(f => studentInfo.kpi[f] || 0);
        const deptPeersH = ENRICHED.filter(s => s.dept === studentInfo.dept && s.id !== studentInfo.id);
        const deptAvgH = hFields.map(f => deptPeersH.length > 0
          ? parseFloat((deptPeersH.reduce((a, s) => a + (s.kpi[f] || 0), 0) / deptPeersH.length).toFixed(1))
          : 0);
        new Chart(hBarCtx, {
          type: 'bar',
          data: {
            labels: hLabels,
            datasets: [
              { label: 'You', data: myValsH, backgroundColor: 'rgba(0,245,255,0.65)', borderColor: '#00f5ff', borderWidth: 1.5, borderRadius: 5 },
              { label: 'Dept Avg', data: deptAvgH, backgroundColor: 'rgba(191,0,255,0.35)', borderColor: '#bf00ff', borderWidth: 1.5, borderRadius: 5 }
            ]
          },
          options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { labels: { color: 'rgba(120,180,220,0.8)', font: { size: 11 } } } },
            scales: {
              x: { grid: { display: false }, ticks: { color: 'rgba(120,180,220,0.7)', font: { size: 10 } } },
              y: { grid: { color: 'rgba(0,245,255,0.06)' }, ticks: { color: 'rgba(120,180,220,0.7)' }, beginAtZero: true }
            }
          }
        });
      }
      return;
    }
  }

  // Guard: no data yet — charts will be re-initialized by fetchEnrichedData when data arrives
  if (ENRICHED.length === 0) return;

  // KPI Radar - avg across all students
  const fields = ['internships', 'certifications', 'hackathons', 'publications', 'workshops', 'projects', 'club_activities', 'industrial_visits'];
  const labels = ['Internships', 'Certs', 'Hackathons', 'Publications', 'Workshops', 'Projects', 'Club', 'Ind. Visits'];
  const avgVals = fields.map(f => parseFloat((ENRICHED.reduce((a, s) => a + s.kpi[f], 0) / ENRICHED.length).toFixed(1)));

  // Field mapper for tooltips
  const mapLabelToField = {
    'Internships': 'internships',
    'Certs': 'certifications',
    'Hackathons': 'hackathons',
    'Publications': 'publications',
    'Workshops': 'workshops',
    'Projects': 'projects',
    'Club': 'club_activities',
    'Ind. Visits': 'industrial_visits'
  };

  radarChart = new Chart(document.getElementById('chartRadar'), {
    type: 'radar',
    data: {
      labels,
      datasets: [{
        label: 'Avg KPI',
        data: avgVals,
        borderColor: '#00f5ff',
        backgroundColor: 'rgba(0,245,255,0.1)',
        pointBackgroundColor: '#00f5ff',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#00f5ff',
        borderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 9, // Enlarge point significantly on hover
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        r: {
          grid: { color: 'rgba(0,245,255,0.1)' },
          angleLines: { color: 'rgba(0,245,255,0.15)' },
          ticks: { backdropColor: 'transparent', color: 'rgba(0,245,255,0.5)', font: { size: 9 } },
          pointLabels: { color: 'rgba(120,180,220,1)', font: { size: 12, weight: 'bold' } },
        }
      },
      // Native animation settings
      animation: {
        duration: 400,
        easing: 'easeOutQuart'
      },
      interaction: {
        mode: 'nearest',
        intersect: true,
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(17, 24, 39, 0.95)',
          titleFont: { size: 15, family: "'Inter', sans-serif", weight: 'bold' },
          bodyFont: { size: 14, family: "'Inter', sans-serif" },
          padding: 14,
          cornerRadius: 10,
          borderColor: '#00f5ff',
          borderWidth: 1,
          displayColors: false,
          callbacks: {
            title: function (tooltipItems) {
              return tooltipItems[0].label + " Statistics";
            },
            label: function (context) {
              return `⭐ Avg Expected Score: ${context.parsed.r}`;
            },
            afterBody: function (tooltipItems) {
              const category = tooltipItems[0].label;
              const fieldName = mapLabelToField[category];

              if (!fieldName) return '';

              // Ensure calculations perfectly scope by the role's ENRICHED pool (dept vs admin)
              const participated = ENRICHED.filter(s => s.kpi[fieldName] > 0).length;
              // Mock winners/high-achievers as KPI >= 3 for context
              const winners = ENRICHED.filter(s => s.kpi[fieldName] >= 3).length;

              return `\n👥 Attended: ${participated} Students\n🏆 Prize Winners: ${winners} Students`;
            }
          }
        }
      }
    }
  });

  // Career Readiness Doughnut
  const readinessCounts = { High: 0, Moderate: 0, Developing: 0, Low: 0 };
  ENRICHED.forEach(s => {
    if (s.readiness.includes('High')) readinessCounts.High++;
    else if (s.readiness.includes('Moderate')) readinessCounts.Moderate++;
    else if (s.readiness.includes('Developing')) readinessCounts.Developing++;
    else readinessCounts.Low++;
  });

  doughnutChart = new Chart(document.getElementById('chartDoughnut'), {
    type: 'doughnut',
    data: {
      labels: ['High', 'Moderate', 'Developing', 'Low'],
      datasets: [{
        data: Object.values(readinessCounts),
        backgroundColor: ['rgba(57,255,20,0.7)', 'rgba(0,245,255,0.7)', 'rgba(255,102,0,0.7)', 'rgba(255,0,110,0.7)'],
        borderColor: ['#39ff14', '#00f5ff', '#ff6600', '#ff006e'],
        borderWidth: 1.5, hoverOffset: 8,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: { position: 'bottom', labels: { color: 'rgba(120,180,220,0.7)', padding: 14, font: { size: 11 } } },
      },
    }
  });

  // Dept Bar Chart
  const depts = [...new Set(STUDENTS.map(s => s.dept))];
  const deptAvgs = depts.map(d => {
    const group = STUDENTS.filter(s => s.dept === d);

    // We must manually calculate scores since the raw STUDENTS array doesn't have the pre-calculated .score field that ENRICHED does
    const sumScore = group.reduce((acc, student) => {
      const kpi = KPI_DATA[student.id];
      const score = calcKPIScore(kpi);
      return acc + score;
    }, 0);

    return group.length ? parseFloat((sumScore / group.length).toFixed(1)) : 0;
  });

  barChart = new Chart(document.getElementById('chartBar'), {
    type: 'bar',
    data: {
      labels: depts.map(d => DEPT_SHORT[d] || d),
      datasets: [{
        label: 'Avg KPI Score',
        data: deptAvgs,
        backgroundColor: NEON_COLORS.slice(0, 6).map(c => c + 'aa'),
        borderColor: NEON_COLORS.slice(0, 6),
        borderWidth: 1.5,
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: 'rgba(120,180,220,0.7)' } },
        y: { grid: { color: 'rgba(0,245,255,0.06)' }, ticks: { color: 'rgba(120,180,220,0.7)' }, min: 0, max: 100 }
      }
    }
  });

  // Trend Line Chart (simulated monthly data)
  const months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'];
  // Use at least 55 as baseline so data is always visible even when API scores are zero
  const rawBase = ENRICHED.length > 0 ? ENRICHED.reduce((a, s) => a + s.score, 0) / ENRICHED.length : 60;
  const baseScore = Math.max(55, rawBase);
  const trendData = months.map((_, i) => Math.max(0, parseFloat((baseScore - 8 + i * 1.5 + (Math.random() - 0.5) * 2).toFixed(1))));

  lineChart = new Chart(document.getElementById('chartLine'), {
    type: 'line',
    data: {
      labels: months,
      datasets: [{
        label: 'Avg KPI',
        data: trendData,
        borderColor: '#bf00ff',
        backgroundColor: 'rgba(191,0,255,0.08)',
        pointBackgroundColor: '#bf00ff',
        pointRadius: 5,
        borderWidth: 2.5,
        fill: true,
        tension: 0.4,
      }, {
        label: 'Target',
        data: months.map(() => 75),
        borderColor: 'rgba(255,0,110,0.4)',
        borderDash: [6, 4],
        pointRadius: 0,
        borderWidth: 1.5,
        fill: false,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { color: 'rgba(120,180,220,0.7)', font: { size: 11 } } } },
      scales: {
        x: { grid: { color: 'rgba(0,245,255,0.05)' }, ticks: { color: 'rgba(120,180,220,0.7)' } },
        y: { grid: { color: 'rgba(0,245,255,0.06)' }, ticks: { color: 'rgba(120,180,220,0.7)' }, min: 0, max: 100 }
      }
    }
  });
}

// ── STUDENTS TABLE ────────────────────────────────
function renderStudentsTable(data = ENRICHED) {
  const tbody = document.getElementById('studentsTbody');
  if (!tbody) return;
  tbody.innerHTML = data.map((s, i) => `
    <tr style="animation:fadeInUp .3s ease ${i * 0.03}s both;">
      <td><span style="font-family:var(--font-mono);color:var(--neon-cyan);font-size:.8rem;">${s.id}</span></td>
      <td><strong style="color:#e8f4ff;">${s.name}</strong></td>
      <td><span style="color:rgba(120,180,220,.7);font-size:.82rem;">${DEPT_SHORT[s.dept] || s.dept}</span></td>
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

function filterStudents() {
  const q = (document.getElementById('studentSearch')?.value || '').toLowerCase();
  const dept = document.getElementById('deptFilter')?.value || '';
  const yr = document.getElementById('yearFilter')?.value || '';
  const filtered = ENRICHED.filter(s => {
    const matchQ = !q || s.name.toLowerCase().includes(q) || s.id.toLowerCase().includes(q);
    const matchD = !dept || s.dept === dept;
    const matchY = !yr || String(s.year) === yr;
    return matchQ && matchD && matchY;
  });
  renderStudentsTable(filtered);
}

function viewStudentKPI(id) {
  document.getElementById('kpiStudentSelect').value = id;
  switchSection('kpi');
  loadStudentKPI();
}

// ── KPI TRACKER ───────────────────────────────────
function populateKPIDropdown() {
  const sel = document.getElementById('kpiStudentSelect');
  if (!sel) return;
  // Clear any previously appended options (keep only the default placeholder)
  sel.innerHTML = '<option value="">— Select Student —</option>';
  ENRICHED.forEach(s => {
    const o = document.createElement('option');
    o.value = s.id; o.textContent = `${s.name} (${s.id})`;
    sel.appendChild(o);
  });
}

let kpiRadarChart = null, kpiBarChart = null;

function loadStudentKPI() {
  const isStudent = userInfo && userInfo.role === 'student';
  const adminView = document.getElementById('adminKpiView');

  // Clean up old studentView toggle since we reverted to the unified unified view
  if (adminView) adminView.style.display = 'block';

  let id = document.getElementById('kpiStudentSelect')?.value;
  if (isStudent && userInfo.email) {
    id = userInfo.email.split('@')[0].toUpperCase();
    const sel = document.getElementById('kpiStudentSelect');
    if (sel) {
      sel.value = id;
      const searchContainer = document.getElementById('kpiSearchContainer');
      if (searchContainer) searchContainer.style.display = 'none'; // hide the search bar area for students

      const sub = document.getElementById('kpiTrackerSubtitle');
      if (sub) sub.textContent = 'Upload proof of completion to boost your KPI score live';
    }
  }

  const s = id ? ENRICHED.find(x => x.id === id) : null;

  const icons = { internships: '💼', certifications: '🏅', hackathons: '⚡', publications: '📄', workshops: '🔧', projects: '🚀', club_activities: '🎭', industrial_visits: '🏭', value_added_courses: '🎓' };
  const labels = { internships: 'Internships', certifications: 'Certifications', hackathons: 'Hackathons', publications: 'Publications', workshops: 'Workshops', projects: 'Projects', club_activities: 'Club Activities', industrial_visits: 'Ind. Visits', value_added_courses: 'Value Added Courses' };

  const grid = document.getElementById('kpiMetricsGrid');
  if (!grid) return;

  if (!s) {
    // show averages
    const kf = Object.keys(KPI_DATA.CSE001);
    grid.innerHTML = kf.map(k => `
      <div class="kpi-metric-card">
        <div class="kpi-metric-icon">${icons[k] || '📊'}</div>
        <div class="kpi-metric-val">—</div>
        <div class="kpi-metric-label">${labels[k] || k}</div>
      </div>
    `).join('');
    return;
  }

  const isFacultyOrHod = userInfo && (userInfo.role === 'faculty' || userInfo.role === 'hod' || userInfo.role === 'admin');

  const kf = Object.keys(s.kpi);
  grid.innerHTML = kf.map(k => {
    let actionBtns = '';

    if (isStudent && id === s.id) {
      // Student sees their own: Eye + Upload buttons
      actionBtns = `
        <div style="position:absolute; top:8px; right:8px; display:flex; gap:6px;">
          <button class="upload-kpi-btn" onclick="openViewDocumentModal('${k}', '${labels[k] || k}')" title="View Certificate" style="background:rgba(0,245,255,0.1); border:1px solid rgba(0,245,255,0.3); color:rgba(120,180,220,0.8); width:28px; height:28px; border-radius:4px; display:flex; align-items:center; justify-content:center; cursor:pointer; font-size:14px; transition:all 0.3s ease;">&#x1F441;</button>
          <button class="upload-kpi-btn" onclick="openUploadModal('${k}', '${labels[k] || k}')" title="Upload Evidence" style="background:rgba(0,245,255,0.1); border:1px solid rgba(0,245,255,0.3); color:var(--neon-cyan); width:28px; height:28px; border-radius:4px; display:flex; align-items:center; justify-content:center; cursor:pointer; font-weight:bold; transition:all 0.3s ease;">+</button>
        </div>
      `;
    } else if (isFacultyOrHod && s) {
      // Faculty/HOD sees student's KPI: Eye (view cert) + Delete (decrement) buttons
      actionBtns = `
        <div style="position:absolute; top:8px; right:8px; display:flex; gap:6px;">
          <button class="upload-kpi-btn" onclick="openViewDocumentModal('${k}', '${labels[k] || k}', '${s.id}')" title="View Student Certificate"
            style="background:rgba(0,245,255,0.1); border:1px solid rgba(0,245,255,0.3); color:rgba(120,180,220,0.8); width:28px; height:28px; border-radius:4px; display:flex; align-items:center; justify-content:center; cursor:pointer; font-size:14px; transition:all 0.3s ease;">
            &#x1F441;
          </button>
          <button class="upload-kpi-btn" onclick="deleteFacultyKpiEntry('${s.id}', '${k}', '${labels[k] || k}')" title="Delete / Remove this KPI entry"
            style="background:rgba(255,0,110,0.1); border:1px solid rgba(255,0,110,0.3); color:var(--neon-pink); width:28px; height:28px; border-radius:4px; display:flex; align-items:center; justify-content:center; cursor:pointer; font-weight:bold; font-size:16px; transition:all 0.3s ease;">
            &times;
          </button>
        </div>
      `;
    }

    return `
      <div class="kpi-metric-card" style="animation:fadeInUp .4s ease both; position:relative;">
        ${actionBtns}
        <div class="kpi-metric-icon">${icons[k] || '&#x1F4CA;'}</div>
        <div class="kpi-metric-val">${s.kpi[k]}</div>
        <div class="kpi-metric-label">${labels[k] || k}</div>
      </div>
    `;
  }).join('');

  // Radar
  if (kpiRadarChart) kpiRadarChart.destroy();
  kpiRadarChart = new Chart(document.getElementById('chartKPIRadar'), {
    type: 'radar',
    data: {
      labels: kf.map(k => labels[k]),
      datasets: [
        { label: s.name, data: kf.map(k => s.kpi[k]), borderColor: '#00f5ff', backgroundColor: 'rgba(0,245,255,0.15)', pointBackgroundColor: '#00f5ff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#00f5ff', borderWidth: 2, pointRadius: 4, pointHoverRadius: 9 },
        {
          label: 'Dept Avg', data: kf.map(k => {
            const peers = ENRICHED.filter(x => x.dept === s.dept && x.id !== s.id);
            return parseFloat((peers.reduce((a, x) => a + x.kpi[k], 0) / peers.length).toFixed(1));
          }), borderColor: 'rgba(191,0,255,0.6)', backgroundColor: 'rgba(191,0,255,0.06)', pointBackgroundColor: '#bf00ff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#bf00ff', borderWidth: 1.5, pointRadius: 3, pointHoverRadius: 9, borderDash: [5, 3]
        },
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: { r: { grid: { color: 'rgba(0,245,255,0.1)' }, angleLines: { color: 'rgba(0,245,255,0.15)' }, ticks: { backdropColor: 'transparent', color: 'rgba(0,245,255,0.5)', font: { size: 9 } }, pointLabels: { color: 'rgba(120,180,220,1)', font: { size: 12, weight: 'bold' } } } },
      animation: { duration: 400, easing: 'easeOutQuart' },
      interaction: { mode: 'nearest', intersect: true },
      plugins: {
        legend: { labels: { color: 'rgba(120,180,220,.7)', font: { size: 11 } } },
        tooltip: {
          backgroundColor: 'rgba(17, 24, 39, 0.95)',
          titleFont: { size: 15, family: "'Inter', sans-serif", weight: 'bold' },
          bodyFont: { size: 14, family: "'Inter', sans-serif" },
          padding: 14,
          cornerRadius: 10,
          borderColor: '#00f5ff',
          borderWidth: 1,
          callbacks: {
            title: function (tooltipItems) { return tooltipItems[0].label + " Statistics"; },
            label: function (context) { return `${context.dataset.label}: ${context.parsed.r}`; },
            afterBody: function (tooltipItems) {
              const category = tooltipItems[0].label;
              const cmap = {
                'Internships': 'internships', 'Certs': 'certifications', 'Hackathons': 'hackathons',
                'Publications': 'publications', 'Workshops': 'workshops', 'Projects': 'projects',
                'Club': 'club_activities', 'Ind. Visits': 'industrial_visits'
              };
              const fieldName = cmap[category];
              if (!fieldName) return '';

              const participated = ENRICHED.filter(x => x.kpi[fieldName] > 0).length;
              const winners = ENRICHED.filter(x => x.kpi[fieldName] >= 3).length;

              return `\n👥 Attended: ${participated} Students\n🏆 Prize Winners: ${winners} Students`;
            }
          }
        }
      },
    }
  });

  // Bar vs dept avg
  if (kpiBarChart) kpiBarChart.destroy();
  const peers = ENRICHED.filter(x => x.dept === s.dept);
  kpiBarChart = new Chart(document.getElementById('chartKPIBar'), {
    type: 'bar',
    data: {
      labels: peers.map(p => p.name.split(' ')[0]),
      datasets: [{
        label: 'KPI Score',
        data: peers.map(p => p.score),
        backgroundColor: peers.map(p => p.id === s.id ? 'rgba(0,245,255,0.7)' : 'rgba(0,245,255,0.15)'),
        borderColor: peers.map(p => p.id === s.id ? '#00f5ff' : 'rgba(0,245,255,0.3)'),
        borderWidth: 1.5, borderRadius: 6,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: { x: { grid: { display: false }, ticks: { color: 'rgba(120,180,220,.7)', font: { size: 10 } } }, y: { grid: { color: 'rgba(0,245,255,.05)' }, ticks: { color: 'rgba(120,180,220,.7)' }, min: 0, max: 100 } },
    }
  });
}

// ── LEADERBOARD ───────────────────────────────────
function renderLeaderboard() {
  const container = document.getElementById('leaderboardContainer');
  if (!container) return;
  const avatarColors = ['#00f5ff', '#bf00ff', '#ff006e', '#39ff14', '#0080ff', '#ff6600', '#fff000', '#ff00cc'];

  let displayList = ENRICHED;
  const isStudent = userInfo && userInfo.role === 'student';
  let studentPos = -1;

  if (isStudent && userInfo.email) {
    const sId = userInfo.email.split('@')[0].toUpperCase();
    studentPos = ENRICHED.findIndex(s => s.id === sId);

    // For students: Top 10 + Self
    if (studentPos !== -1 && studentPos > 9) {
      displayList = [...ENRICHED.slice(0, 10), ENRICHED[studentPos]];
    } else {
      displayList = ENRICHED.slice(0, 10);
    }
  }

  container.innerHTML = displayList.map((s, idx) => {
    // If we appended the self at the end, figure out the real ranking
    const actualRank = s.id === (userInfo && userInfo.email ? userInfo.email.split('@')[0].toUpperCase() : '') && studentPos > 9 ? studentPos : idx;

    const rankClass = actualRank === 0 ? 'rank-1' : actualRank === 1 ? 'rank-2' : actualRank === 2 ? 'rank-3' : 'rank-other';
    const rankText = actualRank === 0 ? '🥇' : actualRank === 1 ? '🥈' : actualRank === 2 ? '🥉' : `#${actualRank + 1}`;
    const color = avatarColors[actualRank % avatarColors.length];

    // Add ... separator if jumping from rank 10 to student's rank
    let separator = '';
    if (isStudent && studentPos > 9 && idx === displayList.length - 1) {
      separator = `
       <div style="text-align:center; padding: 10px; color: rgba(120,180,220,0.5); font-size: 1.5rem; letter-spacing: 4px;">
         ...
       </div>`;
    }

    const row = `
      <div class="lb-row" onclick="viewStudentKPI('${s.id}')" ${s.id === (userInfo?.email?.split('@')[0].toUpperCase()) ? 'style="border: 1px solid var(--neon-cyan); background: rgba(0,245,255,0.05);"' : ''}>
        <div class="lb-rank ${rankClass}">${rankText}</div>
        <div class="lb-avatar" style="background:${color}22;border:2px solid ${color};color:${color};">${s.name[0]}</div>
        <div class="lb-info">
          <div class="lb-name">${s.name} ${s.id === (userInfo?.email?.split('@')[0].toUpperCase()) ? '<span style="color:var(--neon-cyan);font-size:0.8rem;margin-left:8px;">(You)</span>' : ''}</div>
          <div class="lb-dept">${s.id} • ${DEPT_SHORT[s.dept] || s.dept} • Year ${s.year}</div>
        </div>
        <div style="flex-shrink:0;">${getReadinessBadge(s.readiness)}</div>
        <div class="lb-score" style="color:${getScoreColor(s.score)};">${s.score}</div>
        <div class="lb-bar-wrap">
          <div class="lb-bar"><div class="lb-bar-fill" style="width:${s.score}%;background:${getScoreColor(s.score)};"></div></div>
        </div>
      </div>
    `;
    return separator + row;
  }).join('');
}

// ── AI INSIGHTS ───────────────────────────────────
function renderInsights() {
  const panel = document.getElementById('insightsPanel');
  if (!panel) return;

  const topStudent = ENRICHED[0];
  const lowStudents = ENRICHED.filter(s => s.score < 40);
  const avgScore = (ENRICHED.reduce((a, s) => a + s.score, 0) / ENRICHED.length).toFixed(1);
  const avgInternship = (ENRICHED.reduce((a, s) => a + s.kpi.internships, 0) / ENRICHED.length).toFixed(1);

  const insights = [
    { type: 'info', icon: '🏆', text: `Top performer: <strong>${topStudent.name}</strong> (${topStudent.id}) with KPI score ${topStudent.score}. Recommend as peer mentor for ${topStudent.dept}.` },
    { type: 'warn', icon: '⚠️', text: `${lowStudents.length} student${lowStudents.length !== 1 ? 's' : ''} have KPI score below 40. Immediate academic counseling recommended.` },
    { type: 'tip', icon: '💡', text: `AI Data Science department leads with highest avg KPI. Their hackathon participation rate (avg ${(ENRICHED.filter(s => s.dept === 'AI & Data Science').reduce((a, s) => a + s.kpi.hackathons, 0) / 4).toFixed(1)}) is a model to replicate.` },
    { type: 'info', icon: '📈', text: `Overall average KPI score: ${avgScore}/100. Target for next quarter: 75+.` },
    { type: 'tip', icon: '💼', text: `Average internship count is ${avgInternship}. Students with 3+ internships score 25% higher on average.` },
    { type: 'warn', icon: '📄', text: `Publications remain the lowest-performing KPI. Encourage research opportunities to boost scores.` },
  ];

  const existingInsights = panel.querySelectorAll('.insight-item');
  existingInsights.forEach(e => e.remove());

  insights.forEach((ins, i) => {
    const div = document.createElement('div');
    div.className = 'insight-item';
    div.style.cssText = `animation:fadeInUp .4s ease ${i * 0.08}s both;`;
    const badgeClass = ins.type === 'tip' ? 'badge-tip' : ins.type === 'warn' ? 'badge-warn' : 'badge-info';
    div.innerHTML = `<div class="insight-badge ${badgeClass}">${ins.icon} ${ins.type.toUpperCase()}</div><div class="insight-text">${ins.text}</div>`;
    panel.appendChild(div);
  });
}

// ── AI CHAT ───────────────────────────────────────
function sendChat() {
  const input = document.getElementById('chatInput');
  const q = input.value.trim();
  if (!q) return;

  const userDiv = document.createElement('div');
  userDiv.className = 'chat-msg user';
  userDiv.innerHTML = `<div class="msg-bubble">${q}</div><div class="msg-time">${new Date().toLocaleTimeString()}</div>`;
  msgs.appendChild(userDiv);
  input.value = '';
  msgs.scrollTop = msgs.scrollHeight;

  setTimeout(() => {
    const aiDiv = document.createElement('div');
    aiDiv.className = 'chat-msg ai';
    aiDiv.innerHTML = `<div class="msg-bubble">${getAIResponse(q)}</div><div class="msg-time">${new Date().toLocaleTimeString()}</div>`;
    msgs.appendChild(aiDiv);
    msgs.scrollTop = msgs.scrollHeight;
  }, 700);
}

// ── ANALYTICS CHARTS ─────────────────────────────
function renderAnalyticsCharts() {
  // Year-wise grouped bar
  const years = [1, 2, 3, 4];
  const depts = [...new Set(ENRICHED.map(s => s.dept))];
  const yearData = years.map(y => {
    const g = ENRICHED.filter(s => s.year === y);
    return g.length ? (g.reduce((a, s) => a + s.score, 0) / g.length).toFixed(1) : 0;
  });

  const ctx1 = document.getElementById('chartAnalyticsBar');
  if (ctx1 && !ctx1._chartjs) {
    new Chart(ctx1, {
      type: 'bar',
      data: { labels: years.map(y => `Year ${y}`), datasets: [{ label: 'Avg KPI Score', data: yearData, backgroundColor: NEON_COLORS.slice(0, 4).map(c => c + '99'), borderColor: NEON_COLORS.slice(0, 4), borderWidth: 1.5, borderRadius: 8 }] },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false }, ticks: { color: 'rgba(120,180,220,.7)' } }, y: { grid: { color: 'rgba(0,245,255,.05)' }, ticks: { color: 'rgba(120,180,220,.7)' }, min: 0, max: 100 } } }
    });
  }

  // Section pie
  const sections = [...new Set(ENRICHED.map(s => s.section))];
  const sectionCounts = sections.map(sec => ENRICHED.filter(s => s.section === sec).length);
  const ctx2 = document.getElementById('chartAnalyticsPie');
  if (ctx2 && !ctx2._chartjs) {
    new Chart(ctx2, {
      type: 'pie', data: { labels: sections.map(s => `Section ${s}`), datasets: [{ data: sectionCounts, backgroundColor: NEON_COLORS.slice(0, sections.length).map(c => c + '88'), borderColor: NEON_COLORS.slice(0, sections.length), borderWidth: 1.5 }] },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: 'rgba(120,180,220,.7)', padding: 12 } } } }
    });
  }

  // Scatter: internships vs score
  const ctx3 = document.getElementById('chartScatter');
  if (ctx3 && !ctx3._chartjs) {
    new Chart(ctx3, {
      type: 'scatter',
      data: { datasets: [{ label: 'Students', data: ENRICHED.map(s => ({ x: s.kpi.internships, y: s.score })), backgroundColor: 'rgba(0,245,255,0.6)', borderColor: '#00f5ff', pointRadius: 6, pointHoverRadius: 9 }] },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: 'rgba(0,245,255,.05)' }, ticks: { color: 'rgba(120,180,220,.7)' }, title: { display: true, text: 'Internships', color: 'rgba(0,245,255,.6)' } }, y: { grid: { color: 'rgba(0,245,255,.05)' }, ticks: { color: 'rgba(120,180,220,.7)' }, title: { display: true, text: 'KPI Score', color: 'rgba(0,245,255,.6)' } } } }
    });
  }

  // Category averages bar
  const kpiFields = ['internships', 'certifications', 'hackathons', 'publications', 'workshops', 'projects', 'club_activities', 'industrial_visits'];
  const kpiLabels = ['Internships', 'Certs', 'Hackathons', 'Pubs', 'Workshops', 'Projects', 'Club', 'Visits'];
  const kpiAvgs = kpiFields.map(f => (ENRICHED.reduce((a, s) => a + s.kpi[f], 0) / ENRICHED.length).toFixed(1));
  const ctx4 = document.getElementById('chartCategories');
  if (ctx4 && !ctx4._chartjs) {
    new Chart(ctx4, {
      type: 'bar',
      data: { labels: kpiLabels, datasets: [{ label: 'Avg Count', data: kpiAvgs, backgroundColor: NEON_COLORS.map(c => c + '88'), borderColor: NEON_COLORS, borderWidth: 1.5, borderRadius: 6 }] },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { display: false }, ticks: { color: 'rgba(120,180,220,.7)', font: { size: 10 } } }, y: { grid: { color: 'rgba(0,245,255,.05)' }, ticks: { color: 'rgba(120,180,220,.7)' } } } }
    });
  }
}

// ── FACULTY KPI RENDER ────────────────────────────
function initFacultyKPI() {
  const select = document.getElementById('facKpiSelect');
  if (!select) return;

  const displayFac = getFilteredFaculty();
  select.innerHTML = '<option value="">— Select Faculty —</option>' +
    displayFac.map(f => `<option value="${f.id}">${f.name} (${f.id})</option>`).join('');

  document.getElementById('facKpiMetricsGrid').innerHTML = ''; // reset
}

function loadFacultyKPI() {
  const fid = document.getElementById('facKpiSelect').value;
  const grid = document.getElementById('facKpiMetricsGrid');
  if (!fid) {
    grid.innerHTML = '';
    document.getElementById('facKpiChartsArea').style.display = 'none';
    return;
  }

  const fac = FACULTY_DB.find(f => f.id === fid);
  if (!fac) return;

  const kpis = [
    { label: 'Industrial Visits', val: fac.kpis.iv, icon: '🏭', color: 'cyan', target: 5 },
    { label: 'Workshops', val: fac.kpis.ws, icon: '🛠️', color: 'purple', target: 4 },
    { label: 'Certifications', val: fac.kpis.cert, icon: '📜', color: 'pink', target: 3 },
    { label: 'Project Mentorship', val: fac.kpis.pm, icon: '🚀', color: 'green', target: 15 }
  ];

  grid.innerHTML = kpis.map((k, i) => {
    const pct = Math.min(100, Math.round((k.val / k.target) * 100));
    return `
      <div class="kpi-card" style="animation:fadeInUp 0.4s ease ${i * 0.1}s both;">
        <div class="kpi-card-header">
          <span style="font-size:1.5rem">${k.icon}</span>
          <span class="kpi-score" style="color:var(--neon-${k.color})">${k.val}<span style="font-size:1rem;color:rgba(120,180,220,.5)">/${k.target}</span></span>
        </div>
        <div class="kpi-title">${k.label}</div>
        <div class="kpi-progress">
          <div class="kpi-progress-fill" style="width:${pct}%; background:var(--neon-${k.color})"></div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:10px; font-size:.7rem; color:rgba(120,180,220,.5)">
          <span>Progress</span>
          <span style="color:var(--neon-${k.color})">${pct}%</span>
        </div>
      </div>
    `;
  }).join('');

  // ── Render Chart ──
  const chartsArea = document.getElementById('facKpiChartsArea');
  if (chartsArea) chartsArea.style.display = 'flex';

  const ctx = document.getElementById('chartFacKPIBar');
  if (ctx) {
    let existingChart = Chart.getChart(ctx);
    if (existingChart) existingChart.destroy();

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: kpis.map(k => k.label),
        datasets: [
          {
            label: 'Actual Achieved',
            data: kpis.map(k => k.val),
            backgroundColor: kpis.map(k => {
              const colors = { cyan: '#00f5ff', purple: '#bf00ff', pink: '#ff006e', green: '#39ff14' };
              return (colors[k.color] || '#00f5ff') + '88';
            }),
            borderColor: kpis.map(k => {
              const colors = { cyan: '#00f5ff', purple: '#bf00ff', pink: '#ff006e', green: '#39ff14' };
              return colors[k.color] || '#00f5ff';
            }),
            borderWidth: 1.5,
            borderRadius: 6,
            order: 2
          },
          {
            label: 'Target Goal',
            data: kpis.map(k => k.target),
            backgroundColor: 'rgba(120,180,220,0.1)',
            borderColor: 'rgba(120,180,220,0.6)',
            borderWidth: 2,
            borderDash: [5, 5],
            type: 'line',
            pointRadius: 4,
            order: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'top', labels: { color: 'rgba(120,180,220,.7)', padding: 15 } } },
        scales: {
          x: { grid: { display: false }, ticks: { color: 'rgba(120,180,220,.7)' } },
          y: { grid: { color: 'rgba(0,245,255,.05)' }, ticks: { color: 'rgba(120,180,220,.7)' }, beginAtZero: true }
        }
      }
    });
  }
}

// ── FACULTY PROFILE RENDER ────────────────────────
function renderFacProfile() {
  if (!userInfo || userInfo.role !== 'faculty') return;

  const emailLen = userInfo.email.length;
  // Match login email loosely to FACULTY_DB ID OR fallback via deterministic gen
  const facMatch = FACULTY_DB.find(f => f.id.toLowerCase() === userInfo.email.split('@')[0].toLowerCase());

  const facName = facMatch ? facMatch.name : userInfo.name;
  const facDept = facMatch ? facMatch.dept : 'General Faculty';
  const facSpec = facMatch ? facMatch.spec : 'Core Engineering';

  document.getElementById('facProfileAvatar').textContent = facName[0].toUpperCase();
  document.getElementById('facProfileName').textContent = facName;
  document.getElementById('facProfileDept').textContent = facDept;
  document.getElementById('facProfileSpec').textContent = facSpec;

  if (!window.facKpis) {
    if (facMatch && facMatch.kpis) {
      window.facKpis = [
        { id: 'iv', label: 'Industrial Visits', val: facMatch.kpis.iv, icon: '🏭', color: 'cyan', target: 5 },
        { id: 'ws', label: 'Workshops', val: facMatch.kpis.ws, icon: '🛠️', color: 'purple', target: 4 },
        { id: 'cert', label: 'Certifications', val: facMatch.kpis.cert, icon: '📜', color: 'pink', target: 3 },
        { id: 'pm', label: 'Project Mentorship', val: facMatch.kpis.pm, icon: '👨‍🏫', color: 'green', target: 10 }
      ];
    } else {
      window.facKpis = [
        { id: 'iv', label: 'Industrial Visits', val: (emailLen % 4) + 1, icon: '🏭', color: 'cyan', target: 5 },
        { id: 'ws', label: 'Workshops', val: (emailLen % 3) + 2, icon: '🛠️', color: 'purple', target: 4 },
        { id: 'cert', label: 'Certifications', val: (emailLen % 2) + 1, icon: '📜', color: 'pink', target: 3 },
        { id: 'pm', label: 'Project Mentorship', val: (emailLen % 6) + 5, icon: '👨‍🏫', color: 'green', target: 10 }
      ];
    }
  }

  const kpis = window.facKpis;
  const grid = document.getElementById('facProfileMetricsGrid');

  grid.innerHTML = kpis.map((k, i) => {
    const actionBtns = `
      <div style="position:absolute; top:8px; right:8px; display:flex; gap:6px;">
        <button class="upload-kpi-btn" onclick="openViewDocumentModal('${k.id}', '${k.label}')" title="View Document" style="background:rgba(0,245,255,0.1); border:1px solid rgba(0,245,255,0.3); color:rgba(120,180,220,0.8); width:28px; height:28px; border-radius:4px; display:flex; align-items:center; justify-content:center; cursor:pointer; font-size:14px; transition:all 0.3s ease;">👁️</button>
        <button class="upload-kpi-btn" onclick="openUploadModal('${k.id}', '${k.label}')" title="Upload Evidence" style="background:rgba(0,245,255,0.1); border:1px solid rgba(0,245,255,0.3); color:var(--neon-cyan); width:28px; height:28px; border-radius:4px; display:flex; align-items:center; justify-content:center; cursor:pointer; font-weight:bold; transition:all 0.3s ease;">+</button>
      </div>
    `;

    return `
      <div class="kpi-metric-card" style="animation:fadeInUp .4s ease both; position:relative;">
        ${actionBtns}
        <div class="kpi-metric-icon">${k.icon}</div>
        <div class="kpi-metric-val" style="color:var(--neon-${k.color})">${k.val}<span style="font-size:1rem;color:rgba(120,180,220,.5)">/${k.target}</span></div>
        <div class="kpi-metric-label">${k.label}</div>
      </div>
    `;
  }).join('');

  // ── Render Chart ──
  const chartsArea = document.getElementById('facProfileChartsArea');
  if (chartsArea) chartsArea.style.display = 'flex';

  const ctx = document.getElementById('chartFacProfileBar');
  if (ctx) {
    let existingChart = Chart.getChart(ctx);
    if (existingChart) existingChart.destroy();

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: kpis.map(k => k.label),
        datasets: [
          {
            label: 'Actual Achieved',
            data: kpis.map(k => k.val),
            backgroundColor: kpis.map(k => {
              const colors = { cyan: '#00f5ff', purple: '#bf00ff', pink: '#ff006e', green: '#39ff14' };
              return (colors[k.color] || '#00f5ff') + '88';
            }),
            borderColor: kpis.map(k => {
              const colors = { cyan: '#00f5ff', purple: '#bf00ff', pink: '#ff006e', green: '#39ff14' };
              return colors[k.color] || '#00f5ff';
            }),
            borderWidth: 1.5,
            borderRadius: 6,
            order: 2
          },
          {
            label: 'Target Goal',
            data: kpis.map(k => k.target),
            backgroundColor: 'rgba(120,180,220,0.1)',
            borderColor: 'rgba(120,180,220,0.6)',
            borderWidth: 2,
            borderDash: [5, 5],
            type: 'line',
            pointRadius: 4,
            order: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'top', labels: { color: 'rgba(120,180,220,.7)', padding: 15 } } },
        scales: {
          x: { grid: { display: false }, ticks: { color: 'rgba(120,180,220,.7)' } },
          y: { grid: { color: 'rgba(0,245,255,.05)' }, ticks: { color: 'rgba(120,180,220,.7)' }, beginAtZero: true }
        }
      }
    });
  }
}

// ── HOD PROFILE RENDER ────────────────────────────
function renderHODProfile() {
  if (!userInfo || userInfo.role !== 'hod') return;

  document.getElementById('hodProfileAvatar').textContent = userInfo.name[0].toUpperCase();
  document.getElementById('hodProfileName').textContent = userInfo.name;

  const deptMap = {
    'hod.cse@kpi.edu': 'Computer Science & Engineering',
    'hod.ece@kpi.edu': 'Electronics & Communication',
    'hod.mech@kpi.edu': 'Mechanical Engineering',
    'hod.ce@kpi.edu': 'Civil Engineering',
    'hod.it@kpi.edu': 'Information Technology',
    'hod.ai@kpi.edu': 'AI & Data Science'
  };
  document.getElementById('hodProfileDept').textContent = deptMap[userInfo.email] || 'Department Head';

  // Use window.hodKpis to persist the HOD's KPIs between re-renders during the same session
  if (!window.hodKpis) {
    const emailLen = userInfo.email.length;
    window.hodKpis = [
      { id: 'iv', label: 'Industrial Visits', val: (emailLen % 4) + 2, icon: '🏭', color: 'cyan', target: 5 },
      { id: 'ws', label: 'Workshops', val: (emailLen % 3) + 3, icon: '🛠️', color: 'purple', target: 4 },
      { id: 'cert', label: 'Certifications', val: (emailLen % 2) + 2, icon: '📜', color: 'pink', target: 3 },
      { id: 'pm', label: 'Project Mentorship', val: (emailLen % 6) + 10, icon: '🚀', color: 'green', target: 15 }
    ];
  }
  const kpis = window.hodKpis;

  const grid = document.getElementById('hodKpiMetricsGrid');
  grid.innerHTML = kpis.map((k, i) => {
    const actionBtns = `
      <div style="position:absolute; top:8px; right:8px; display:flex; gap:6px;">
        <button class="upload-kpi-btn" onclick="openViewDocumentModal('${k.id}', '${k.label}')" title="View Document" style="background:rgba(0,245,255,0.1); border:1px solid rgba(0,245,255,0.3); color:rgba(120,180,220,0.8); width:28px; height:28px; border-radius:4px; display:flex; align-items:center; justify-content:center; cursor:pointer; font-size:14px; transition:all 0.3s ease;">👁️</button>
        <button class="upload-kpi-btn" onclick="openUploadModal('${k.id}', '${k.label}')" title="Upload Evidence" style="background:rgba(0,245,255,0.1); border:1px solid rgba(0,245,255,0.3); color:var(--neon-cyan); width:28px; height:28px; border-radius:4px; display:flex; align-items:center; justify-content:center; cursor:pointer; font-weight:bold; transition:all 0.3s ease;">+</button>
      </div>
    `;

    return `
      <div class="kpi-metric-card" style="animation:fadeInUp .4s ease both; position:relative;">
        ${actionBtns}
        <div class="kpi-metric-icon">${k.icon}</div>
        <div class="kpi-metric-val" style="color:var(--neon-${k.color})">${k.val}<span style="font-size:1rem;color:rgba(120,180,220,.5)">/${k.target}</span></div>
        <div class="kpi-metric-label">${k.label}</div>
      </div>
    `;
  }).join('');

  // ── Render Chart ──
  const ctx = document.getElementById('chartHodKPIBar');
  if (ctx) {
    let existingChart = Chart.getChart(ctx);
    if (existingChart) existingChart.destroy();

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: kpis.map(k => k.label),
        datasets: [
          {
            label: 'Actual Achieved',
            data: kpis.map(k => k.val),
            backgroundColor: kpis.map(k => {
              const colors = { cyan: '#00f5ff', purple: '#bf00ff', pink: '#ff006e', green: '#39ff14' };
              return (colors[k.color] || '#00f5ff') + '88';
            }),
            borderColor: kpis.map(k => {
              const colors = { cyan: '#00f5ff', purple: '#bf00ff', pink: '#ff006e', green: '#39ff14' };
              return colors[k.color] || '#00f5ff';
            }),
            borderWidth: 1.5,
            borderRadius: 6,
            order: 2
          },
          {
            label: 'Target Goal',
            data: kpis.map(k => k.target),
            backgroundColor: 'rgba(120,180,220,0.1)',
            borderColor: 'rgba(120,180,220,0.6)',
            borderWidth: 2,
            borderDash: [5, 5],
            type: 'line',
            pointRadius: 4,
            order: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'top', labels: { color: 'rgba(120,180,220,.7)', padding: 15 } } },
        scales: {
          x: { grid: { display: false }, ticks: { color: 'rgba(120,180,220,.7)' } },
          y: { grid: { color: 'rgba(0,245,255,.05)' }, ticks: { color: 'rgba(120,180,220,.7)' }, beginAtZero: true }
        }
      }
    });
  }
}

// ── ADD STUDENT MODAL ─────────────────────────────
function openAddStudent() {
  const deptSelect = document.getElementById('f_dept');

  if (userInfo && userInfo.role === 'hod' && userInfo.email) {
    const deptMap = {
      'hod.cse@kpi.edu': 'Computer Science & Engineering',
      'hod.ece@kpi.edu': 'Electronics & Communication',
      'hod.mech@kpi.edu': 'Mechanical Engineering',
      'hod.ce@kpi.edu': 'Civil Engineering',
      'hod.it@kpi.edu': 'Information Technology',
      'hod.ai@kpi.edu': 'AI & Data Science'
    };
    const hodDept = deptMap[userInfo.email];
    if (hodDept) {
      deptSelect.value = hodDept;
      deptSelect.disabled = true; // Lock it
    }
  } else {
    // Un-disable it for admin/others
    deptSelect.disabled = false;
  }

  document.getElementById('addStudentModal').classList.add('active');
}
function closeModal() {
  document.getElementById('addStudentModal').classList.remove('active');
}
function addStudent(e) {
  e.preventDefault();
  const id = document.getElementById('f_id').value.trim().toUpperCase();
  const name = document.getElementById('f_name').value.trim();
  const section = document.getElementById('f_section').value.trim().toUpperCase();
  const year = parseInt(document.getElementById('f_year').value);

  // If disabled, `.value` might not submit correctly in some forms, though it works in JS
  const dept = document.getElementById('f_dept').value;

  if (ENRICHED.find(s => s.id === id)) {
    showToast('Student ID already exists!', 'error'); return;
  }

  const defaultKPI = { internships: 0, certifications: 0, hackathons: 0, publications: 0, workshops: 0, projects: 0, club_activities: 0, industrial_visits: 0 };
  const score = calcKPIScore(defaultKPI);
  const readiness = getReadiness(score);
  ENRICHED.push({ id, name, dept, section, year, gpa: 0, kpi: defaultKPI, score, readiness, lastUpdated: new Date().toLocaleDateString() });
  KPI_DATA[id] = defaultKPI;

  closeModal();
  renderStudentsTable();
  showToast(`Student ${name} added successfully!`, 'success');
  document.getElementById('addStudentForm').reset();
}

// ── ADD FACULTY MODAL ─────────────────────────────
function openAddFacultyModal() {
  document.getElementById('addFacultyModal').classList.add('active');
}
function closeAddFacultyModal() {
  document.getElementById('addFacultyModal').classList.remove('active');
}
function addFaculty(e) {
  e.preventDefault();
  const id = document.getElementById('fac_id').value.trim().toUpperCase();
  const name = document.getElementById('fac_name').value.trim();
  const dept = document.getElementById('fac_dept').value;
  const spec = document.getElementById('fac_spec').value.trim();
  const status = document.getElementById('fac_status').value;

  if (FACULTY_DB.find(f => f.id === id)) {
    showToast('Faculty ID already exists!', 'error'); return;
  }

  const defaultKpis = { iv: 0, ws: 0, cert: 0, pm: 0 };
  FACULTY_DB.push({ id, name, dept, spec, status, kpis: defaultKpis });

  closeAddFacultyModal();
  renderFacultyTable();
  showToast(`Faculty ${name} added successfully!`, 'success');
  document.getElementById('addFacultyForm').reset();
}

// ── ADD HOD MODAL ─────────────────────────────────
function openAddHODModal() {
  document.getElementById('addHodModal').classList.add('active');
}
function closeAddHODModal() {
  document.getElementById('addHodModal').classList.remove('active');
}
function addHOD(e) {
  e.preventDefault();
  const emailId = document.getElementById('hod_email').value.trim().toLowerCase();
  const name = document.getElementById('hod_name').value.trim();
  const dept = document.getElementById('hod_dept').value;
  const status = document.getElementById('hod_status').value;

  if (HOD_LIST.find(h => h.id === emailId)) {
    showToast('HOD Email / Login ID already exists!', 'error'); return;
  }

  HOD_LIST.push({ id: emailId, name, dept, status });

  closeAddHODModal();
  renderHODTable();
  // Refresh the KPI dropdown list
  initAdminHODKPI();
  showToast(`HOD ${name} added successfully!`, 'success');
  document.getElementById('addHodForm').reset();
}

// ── GLOBAL SEARCH ─────────────────────────────────
document.getElementById('globalSearch')?.addEventListener('keyup', e => {
  const q = e.target.value.trim();
  if (q.length > 1) {
    switchSection('students');
    document.getElementById('studentSearch').value = q;
    filterStudents();
  }
});

// ── TOAST ─────────────────────────────────────────
function showToast(msg, type = 'info') {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.className = `neon-toast ${type}`;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

// ── CERTIFICATE UPLOAD LOGIC ──────────────────────
function openUploadModal(categoryKey, categoryLabel) {
  const overlay = document.getElementById('uploadModalOverlay');
  if (!overlay) return;
  document.getElementById('uploadCategoryLabel').textContent = categoryLabel;
  document.getElementById('uploadCategoryKey').value = categoryKey;
  overlay.classList.add('active');
}

function closeUploadModal() {
  const overlay = document.getElementById('uploadModalOverlay');
  if (overlay) overlay.classList.remove('active');
}

// Global scope tracker for uploaded files simulating a database
window.uploadedFilesRegistry = window.uploadedFilesRegistry || {};

// categoryKey: the KPI type (e.g. 'certifications')
// categoryLabel: human-readable label
// studentId (optional): if provided, load this student's certificate from the API (faculty view)
function openViewDocumentModal(categoryKey, categoryLabel, studentId) {
  const overlay = document.getElementById('viewDocumentModalOverlay');
  if (!overlay) return;
  document.getElementById('viewCategoryLabel').textContent = categoryLabel;
  const container = document.getElementById('documentViewerContainer');

  // ── Faculty/HOD: list all certificates from backend, each with a Delete button ──
  if (studentId) {
    container.innerHTML = '<div style="text-align:center;color:rgba(120,180,220,0.5);padding:30px;">Loading certificates...</div>';
    overlay.classList.add('active');
    const token = localStorage.getItem('kpi_token') || '';

    function renderDocCards(docs) {
      if (!docs || docs.length === 0) {
        container.innerHTML = `
          <div style="text-align:center;color:rgba(120,180,220,0.5);padding:30px;">
            <div style="font-size:3rem;margin-bottom:12px;opacity:0.5;">&#x1F4C2;</div>
            No certificate uploaded yet for <strong>${categoryLabel}</strong>.
          </div>`;
        return;
      }
      container.innerHTML = docs.map((doc, idx) => {
        const isImg = doc.file_path && /\.(jpg|jpeg|png|gif|webp)$/i.test(doc.file_path);
        const uploadedOn = doc.upload_date ? new Date(doc.upload_date).toLocaleString() : 'Unknown date';
        const preview = isImg
          ? `<img src="${doc.file_path}" style="max-width:100%;max-height:220px;object-fit:contain;border-radius:6px;border:1px solid rgba(0,245,255,0.2);margin-bottom:8px;">`
          : `<div style="font-size:2.5rem;margin-bottom:6px;">&#x1F4C4;</div><div style="color:rgba(120,180,220,0.5);font-size:0.8rem;">PDF/Document file</div>`;
        const openLink = !isImg && doc.file_path
          ? `<a href="${doc.file_path}" target="_blank" style="flex:1;text-align:center;padding:6px 10px;background:rgba(0,245,255,0.08);border:1px solid rgba(0,245,255,0.2);border-radius:6px;color:var(--neon-cyan);font-size:0.8rem;text-decoration:none;">&#x1F517; Open</a>`
          : '<span style="flex:1"></span>';
        return `
          <div id="docCard_${doc.id}" style="background:rgba(0,245,255,0.03);border:1px solid rgba(0,245,255,0.15);border-radius:10px;padding:14px;margin-bottom:12px;">
            <div style="font-size:0.72rem;color:rgba(120,180,220,0.45);margin-bottom:8px;">Certificate #${idx + 1} &bull; Uploaded: ${uploadedOn}</div>
            <div style="text-align:center;">${preview}</div>
            <div style="display:flex;gap:8px;margin-top:10px;align-items:center;">
              ${openLink}
              <button
                onclick="deleteDocumentById(${doc.id}, '${studentId}', '${categoryKey}', '${categoryLabel}')"
                style="padding:6px 14px;background:rgba(255,0,110,0.12);border:1px solid rgba(255,0,110,0.35);color:var(--neon-pink);border-radius:6px;cursor:pointer;font-size:0.82rem;font-weight:600;"
                onmouseover="this.style.background='rgba(255,0,110,0.28)'"
                onmouseout="this.style.background='rgba(255,0,110,0.12)'"
                title="Delete this certificate">
                &#x1F5D1; Delete
              </button>
            </div>
          </div>`;
      }).join('');
    }

    fetch(`http://localhost:8000/api/student/${studentId}/documents/${categoryKey}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(r => r.ok ? r.json() : [])
      .then(docs => { container._docs = docs; renderDocCards(docs); })
      .catch(() => {
        const fd = window.uploadedFilesRegistry?.[categoryKey];
        container.innerHTML = fd && fd.length
          ? fd.map((f, i) => f.type.startsWith('image/')
            ? `<div style="text-align:center;margin-bottom:12px;"><img src="${f.url}" style="max-width:100%;border-radius:8px;"></div>`
            : `<div style="text-align:center;padding:20px;"><div style="font-size:2.5rem;">&#x1F4C4;</div><div>Document #${i + 1}</div></div>`
          ).join('')
          : `<div style="text-align:center;color:rgba(120,180,220,0.5);padding:30px;">&#x1F4C2; No certificate found.</div>`;
      });
    return;
  }

  // ── Student: check local session uploads ──
  const fileDataArray = window.uploadedFilesRegistry?.[categoryKey];

  if (fileDataArray && fileDataArray.length > 0) {
    container.innerHTML = fileDataArray.map((fileData, index) => {
      if (fileData.type.startsWith('image/')) {
        return `
            <div style="width:100%; text-align:center;">
              <div style="color:var(--neon-cyan); font-size:0.8rem; margin-bottom:5px;">Document #${index + 1}</div>
              <img src="${fileData.url}" style="max-width:100%; max-height:300px; object-fit:contain; border-radius:4px; border:1px solid rgba(0,245,255,0.2);">
            </div>
          `;
      } else {
        return `
            <div style="width:100%; text-align:center; padding:20px; border:1px solid rgba(0,245,255,0.1); border-radius:4px; margin-bottom:10px;">
              <div style="font-size:2.5rem;margin-bottom:10px;">&#x1F4C4;</div>
              <div style="color:var(--neon-cyan);">Document #${index + 1} successfully uploaded.</div>
              <div style="font-size:0.8rem;color:rgba(120,180,220,.5);margin-top:5px;">Preview not supported for PDFs in demo mode.</div>
            </div>
          `;
      }
    }).join('');
  } else {
    container.innerHTML = `
      <div style="text-align: center; color: rgba(120, 180, 220, 0.5);">
        <div style="font-size: 3rem; margin-bottom: 15px; opacity: 0.5;">&#x1F4C2;</div>
        <div>No document has been uploaded for this category yet.</div>
        <div style="font-size: 0.8rem; margin-top: 8px;">Click the <strong>+</strong> icon to upload proof.</div>
      </div>
    `;
  }

  overlay.classList.add('active');
}

function closeViewDocumentModal() {
  const overlay = document.getElementById('viewDocumentModalOverlay');
  if (overlay) overlay.classList.remove('active');
}

// ── Faculty/HOD: Delete (decrement) a student's KPI entry ────────────────────
async function deleteFacultyKpiEntry(studentId, kpiType, kpiLabel) {
  const confirmed = confirm(
    `Remove one "${kpiLabel}" entry for student ${studentId}?\n\nThis will decrement the count by 1 and cannot be undone.`
  );
  if (!confirmed) return;

  const token = localStorage.getItem('kpi_token') || '';
  try {
    const res = await fetch(
      `http://localhost:8000/api/kpi/${studentId}/${kpiType}/delete`,
      {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
      }
    );

    if (res.ok) {
      showToast(`Removed 1 entry from "${kpiLabel}" for ${studentId}`, 'success');
      const student = ENRICHED.find(s => s.id === studentId);
      if (student && student.kpi[kpiType] > 0) {
        student.kpi[kpiType] -= 1;
      }
      loadStudentKPI();
    } else {
      const err = await res.json().catch(() => ({}));
      showToast(`Delete failed: ${err.detail || res.statusText}`, 'error');
    }
  } catch (e) {
    const student = ENRICHED.find(s => s.id === studentId);
    if (student && student.kpi[kpiType] !== undefined && student.kpi[kpiType] > 0) {
      student.kpi[kpiType] -= 1;
      showToast(`Removed 1 "${kpiLabel}" entry (demo mode)`, 'info');
      loadStudentKPI();
    } else {
      showToast(`Cannot delete: "${kpiLabel}" is already at 0`, 'error');
    }
  }
}

// ── Delete a specific certificate by its database ID (from inside the viewer modal) ──
async function deleteDocumentById(docId, studentId, kpiType, kpiLabel) {
  const confirmed = confirm(
    `Delete this "${kpiLabel}" certificate for student ${studentId}?\n\nThis will also decrement their ${kpiLabel} count by 1.`
  );
  if (!confirmed) return;

  const token = localStorage.getItem('kpi_token') || '';
  try {
    const res = await fetch(`http://localhost:8000/api/documents/${docId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (res.ok) {
      // Remove the card from the modal without closing it
      const card = document.getElementById(`docCard_${docId}`);
      if (card) {
        card.style.transition = 'opacity 0.3s ease';
        card.style.opacity = '0';
        setTimeout(() => {
          card.remove();
          // If no more cards, show empty state
          const container = document.getElementById('documentViewerContainer');
          if (container && !container.querySelector('[id^="docCard_"]')) {
            container.innerHTML = `
              <div style="text-align:center;color:rgba(120,180,220,0.5);padding:30px;">
                <div style="font-size:3rem;margin-bottom:12px;opacity:0.5;">&#x1F4C2;</div>
                All certificates for <strong>${kpiLabel}</strong> have been removed.
              </div>`;
          }
        }, 300);
      }
      // Update local ENRICHED data and re-render KPI cards in background
      const student = ENRICHED.find(s => s.id === studentId);
      if (student && student.kpi[kpiType] > 0) {
        student.kpi[kpiType] -= 1;
      }
      loadStudentKPI();
      showToast(`Certificate deleted. "${kpiLabel}" count decremented for ${studentId}.`, 'success');
    } else {
      const err = await res.json().catch(() => ({}));
      showToast(`Delete failed: ${err.detail || res.statusText}`, 'error');
    }
  } catch (e) {
    // Demo / offline fallback: just remove from UI and decrement local count
    const card = document.getElementById(`docCard_${docId}`);
    if (card) {
      card.style.opacity = '0';
      setTimeout(() => card.remove(), 300);
    }
    const student = ENRICHED.find(s => s.id === studentId);
    if (student && student.kpi[kpiType] > 0) {
      student.kpi[kpiType] -= 1;
      loadStudentKPI();
    }
    showToast(`Certificate removed (demo mode — backend offline).`, 'info');
  }
}

document.getElementById('certificateUploadForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  if (!userInfo || !userInfo.email) return;

  const category = document.getElementById('uploadCategoryKey').value;
  const fileInput = document.getElementById('certificateFile');
  if (!fileInput.files.length) return;

  const file = fileInput.files[0];
  const btn = document.getElementById('uploadCertBtn');

  // ELA Tamper Verification Step
  if (file.type.startsWith("image/")) {
    btn.textContent = 'Verifying Integrity...';
    btn.classList.add('loading');

    try {
      const base64 = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });

      const res = await fetch('http://localhost:8000/api/kpi/verify-certificate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: base64 })
      });

      const verification = await res.json();

      if (verification && verification.is_suspicious) {
        btn.textContent = 'Upload Document';
        btn.classList.remove('loading');
        alert("🚨 SECURITY ALERT: Image Rejected\n\nThe uploaded document failed our Error Level Analysis (ELA) integrity check with a Tamper Score of " + verification.score + ".\n\n" + verification.message + "\n\nPlease upload an original, unmodified certificate.");
        return;
      }
    } catch (err) {
      console.warn("ELA Verification error:", err);
      // Proceed gracefully if backend is down on localhost
    }
  }

  // Restore button if verification passed
  btn.textContent = 'Uploading...';
  btn.classList.add('loading');

  // HOD logic branch
  if (userInfo.role === 'hod' && window.hodKpis) {
    // Render file preview data URL to store in registry so we can view it later
    const file = fileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (!window.uploadedFilesRegistry[category]) {
          window.uploadedFilesRegistry[category] = [];
        }
        window.uploadedFilesRegistry[category].push({
          url: e.target.result,
          type: file.type
        });
      };
      reader.readAsDataURL(file);
    }

    setTimeout(() => {
      // Find the KPI and increment
      const kpi = window.hodKpis.find(k => k.id === category);
      if (kpi) kpi.val += 1;

      // Re-render HOD profile to show update
      if (document.getElementById('section-hod-profile').classList.contains('active')) {
        renderHODProfile();
      }

      // Wrap up
      btn.textContent = 'Upload Document';
      btn.classList.remove('loading');
      e.target.reset();

      const successMsg = document.getElementById('uploadSuccessMsg');
      successMsg.style.display = 'flex';
      setTimeout(() => {
        successMsg.style.display = 'none';
        closeUploadModal();
      }, 2000);

      showToast(`Successfully uploaded and verified ${category.replace('_', ' ')}! (+ KPI points)`, 'success');
    }, 1000);

    return; // Stop here for HOD
  }

  // Faculty logic branch
  if (userInfo.role === 'faculty' && window.facKpis) {
    // Render file preview data URL to store in registry so we can view it later
    const file = fileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (!window.uploadedFilesRegistry[category]) {
          window.uploadedFilesRegistry[category] = [];
        }
        window.uploadedFilesRegistry[category].push({
          url: e.target.result,
          type: file.type
        });
      };
      reader.readAsDataURL(file);
    }

    setTimeout(() => {
      // Find the KPI and increment
      const kpi = window.facKpis.find(k => k.id === category);
      if (kpi) kpi.val += 1;

      // Re-render Faculty profile to show update
      if (typeof renderFacProfile === 'function' && document.getElementById('section-fac-profile').classList.contains('active')) {
        renderFacProfile();
      }

      // Wrap up
      btn.textContent = 'Upload Document';
      btn.classList.remove('loading');
      e.target.reset();

      const successMsg = document.getElementById('uploadSuccessMsg');
      successMsg.style.display = 'flex';
      setTimeout(() => {
        successMsg.style.display = 'none';
        closeUploadModal();
      }, 2000);

      showToast(`Successfully uploaded and verified ${category.replace('_', ' ')}! (+ KPI points)`, 'success');
    }, 1000);

    return; // Stop here for Faculty
  }

  // Student logic branch
  if (userInfo.role !== 'student') return;

  const sId = userInfo.email.split('@')[0].toUpperCase();
  const studentInfo = ENRICHED.find(s => s.id === sId);
  if (!studentInfo) return;

  // Render file preview data URL to store in registry so we can view it later
  if (!file) return;

  // Capture form reference before entering the FileReader callback (inside onload, `e` refers to the FileReader event, not the form)
  const uploadForm = document.getElementById('certificateUploadForm');

  const reader = new FileReader();
  reader.onload = async (e) => {
    const base64Data = e.target.result;

    if (!window.uploadedFilesRegistry[category]) {
      window.uploadedFilesRegistry[category] = [];
    }
    window.uploadedFilesRegistry[category].push({
      url: base64Data,
      type: file.type
    });

    // Send actual file payload to the backend Database!
    try {
      const uploadRes = await fetch('http://localhost:8000/api/kpi/upload-document', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          student_id: sId,
          category: category,
          image: base64Data
        })
      });

      if (!uploadRes.ok) {
        let errText = await uploadRes.text();
        throw new Error(`Server Error: ${uploadRes.status} ${errText}`);
      }

      const resultData = await uploadRes.json();
      console.log("Upload Success:", resultData);

      // Update local state and Dashboard UI from DB success
      await fetchEnrichedData();

      const updatedStudentInfo = ENRICHED.find(s => s.id === sId);
      if (updatedStudentInfo) {

        document.getElementById('studentProfileScore').textContent = studentInfo.score;
        document.getElementById('studentProfileScore').style.color = getScoreColor(studentInfo.score);
        document.getElementById('studentProfileReadiness').innerHTML = getReadinessBadge(studentInfo.readiness);

        if (document.getElementById('section-kpi').classList.contains('active')) {
          loadStudentKPI();
        }

        if (document.getElementById('studentRadarChart')) {
          const fields = ['internships', 'certifications', 'hackathons', 'publications', 'workshops', 'projects', 'club_activities', 'industrial_visits', 'value_added_courses'];
          const labels = ['Internships', 'Certs', 'Hackathons', 'Publications', 'Workshops', 'Projects', 'Club', 'Ind. Visits', 'Courses'];
          const myVals = fields.map(f => studentInfo.kpi[f] || 0);

          const chartCtx = document.getElementById('studentRadarChart');
          let chartStatus = Chart.getChart(chartCtx);
          if (chartStatus != undefined) chartStatus.destroy();

          new Chart(document.getElementById('studentRadarChart'), {
            type: 'radar',
            data: {
              labels,
              datasets: [{
                label: 'My KPI', data: myVals, borderColor: '#00f5ff',
                backgroundColor: 'rgba(0,245,255,0.15)', pointBackgroundColor: '#00f5ff',
                borderWidth: 2, pointRadius: 4
              }]
            },
            options: {
              responsive: true, maintainAspectRatio: false,
              scales: { r: { grid: { color: 'rgba(0,245,255,0.1)' }, angleLines: { color: 'rgba(0,245,255,0.15)' }, ticks: { backdropColor: 'transparent', color: 'rgba(0,245,255,0.5)', font: { size: 9 } }, pointLabels: { color: 'rgba(120,180,220,0.7)', font: { size: 10 } } } },
              plugins: { legend: { display: false } },
            }
          });
        }

        btn.textContent = 'Upload Document';
        btn.classList.remove('loading');
        if (uploadForm) uploadForm.reset();

        const successMsg = document.getElementById('uploadSuccessMsg');
        successMsg.style.display = 'flex';
        setTimeout(() => {
          successMsg.style.display = 'none';
          closeUploadModal();
        }, 2000);

        showToast(`Successfully uploaded and verified ${category.replace('_', ' ')}! (+ KPI points)`, 'success');
      } // End if (updatedStudentInfo)
    } catch (err) {
      console.error("Failed to upload document:", err);
      btn.textContent = 'Upload Document';
      btn.classList.remove('loading');
      showToast('Upload failed: ' + err.message, 'error');
    }
  };
  reader.readAsDataURL(file);
});

// ── ADMIN HOD VIEWS ───────────────────────────────
function renderHODTable() {
  const tbody = document.getElementById('hodsTbody');
  if (!tbody) return;
  tbody.innerHTML = HOD_LIST.map(hod => `
    <tr>
      <td><span style="color:var(--neon-cyan); font-family:var(--font-mono);">${hod.id}</span></td>
      <td><strong>${hod.name}</strong></td>
      <td>${hod.dept}</td>
      <td><span class="neon-badge badge-high">${hod.status}</span></td>
    </tr>
  `).join('');
}

function initAdminHODKPI() {
  const select = document.getElementById('adminHodKpiSelect');
  if (!select) return;

  // Clear existing options
  select.innerHTML = '<option value="">— Select HOD —</option>' +
    HOD_LIST.map(h => `<option value="${h.id}">${h.name} (${h.dept})</option>`).join('');

  document.getElementById('allHodKpiMetricsGrid').innerHTML = ''; // reset
}

function loadAdminHODKPI() {
  const hodId = document.getElementById('adminHodKpiSelect').value;
  const grid = document.getElementById('allHodKpiMetricsGrid');
  if (!hodId) {
    grid.innerHTML = '';
    document.getElementById('allHodKpiChartsArea').style.display = 'none';
    return;
  }

  const hod = HOD_LIST.find(h => h.id === hodId);
  if (!hod) return;

  // Use the same deterministic generation for KPI counts based on email length used in renderHODProfile
  const emailLen = hodId.length;

  const kpis = [
    { id: 'hod_iv', label: 'Industrial Visits', val: emailLen % 7 + 1, icon: '🏭', color: 'cyan', target: 5 },
    { id: 'hod_ws', label: 'Workshops', val: emailLen % 5 + 2, icon: '🛠️', color: 'purple', target: 4 },
    { id: 'hod_cert', label: 'Certifications', val: emailLen % 4 + 1, icon: '📜', color: 'pink', target: 3 },
    { id: 'hod_pm', label: 'Project Mentorship', val: emailLen % 15 + 5, icon: '👨‍🏫', color: 'green', target: 10 },
  ];

  grid.innerHTML = kpis.map((k, i) => `
    <div class="kpi-metric-card" style="animation:fadeInUp .4s ease both; position:relative;">
      <div class="kpi-metric-icon">${k.icon}</div>
      <div class="kpi-metric-val" style="color:var(--neon-${k.color})">${k.val}<span style="font-size:1rem;color:rgba(120,180,220,.5)">/${k.target}</span></div>
      <div class="kpi-metric-label">${k.label}</div>
    </div>
  `).join('');

  // Show Chart Section
  document.getElementById('allHodKpiChartsArea').style.display = 'flex';

  const ctx = document.getElementById('chartAllHodKPIBar');
  if (ctx) {
    let chartStatus = Chart.getChart(ctx);
    if (chartStatus != undefined) {
      chartStatus.destroy();
    }

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: kpis.map(k => k.label),
        datasets: [
          {
            label: 'Current Score',
            data: kpis.map(k => k.val),
            backgroundColor: kpis.map(k => `rgba(${k.color === 'cyan' ? '0,245,255' : k.color === 'purple' ? '191,0,255' : k.color === 'pink' ? '255,0,110' : '57,255,20'}, 0.7)`),
            borderColor: kpis.map(k => `var(--neon-${k.color})`),
            borderWidth: 1,
            borderRadius: 4
          },
          {
            label: 'Target',
            data: kpis.map(k => k.target),
            type: 'line',
            borderColor: 'rgba(255,255,255,0.7)',
            borderDash: [5, 5],
            fill: false,
            pointBackgroundColor: '#fff',
            pointRadius: 4
          }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, grid: { color: 'rgba(0,245,255,.05)' }, ticks: { color: 'rgba(120,180,220,.7)' } },
          x: { grid: { display: false }, ticks: { color: 'rgba(120,180,220,.7)' } }
        },
        plugins: {
          legend: { labels: { color: 'rgba(120,180,220,.7)' } }
        }
      }
    });
  }
}

// ── STUDENT CSV UPLOAD ─────────────────────────────
async function uploadStudentCSV(event) {
  const file = event.target.files[0];
  if (!file) return;

  const btn = document.getElementById('uploadCsvBtn');
  const ogText = btn.innerHTML;
  btn.innerHTML = `<span style="display:inline-block;width:12px;height:12px;border:2px solid;border-radius:50%;border-top-color:transparent;animation:spin 1s linear infinite;"></span> Uploading...`;
  btn.disabled = true;

  const formData = new FormData();
  formData.append('file', file);

  try {
    const token = localStorage.getItem('kpi_token') || '';
    const response = await fetch('http://localhost:8000/api/student/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    const result = await response.json();
    if (response.ok) {
      showToast('Success', `CSV Processed: ${result.imported} imported, ${result.failed} failed.`);
      setTimeout(() => location.reload(), 2000); // Reload entire dashboard to refetch from DB
    } else {
      showToast('Error', result.detail || 'Upload failed.');
    }
  } catch (error) {
    showToast('Error', 'Network error or server unreachable.');
  } finally {
    btn.innerHTML = ogText;
    btn.disabled = false;
    event.target.value = ''; // Reset file state
  }
}

// ── RECOMMENDATIONS VIEW ─────────────────────────
async function loadRecommendationsView() {
  const container = document.getElementById('recommendationsContainer');
  const storedUser = JSON.parse(localStorage.getItem('kpi_user') || '{}');
  const email = storedUser.email;
  const role = storedUser.role;

  if (!email || !role) {
    container.innerHTML = '<div style="color:var(--neon-pink); padding: 20px;">Cannot load insights. Please login again.</div>';
    return;
  }

  // Pre-fetch clear & loading animation
  container.innerHTML = `
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; flex:1; gap:20px; color:rgba(120,180,220,0.7); height:300px;">
      <div style="width:40px; height:40px; border:3px solid var(--neon-cyan); border-radius:50%; border-top-color:transparent; animation:spin 1s linear infinite;"></div>
      <div style="font-family:var(--font-mono); letter-spacing:1px; animation:neonPulse 2s infinite;">ANALYZING KPI METRICS...</div>
    </div>
  `;

  try {
    // Determine the ID to send. For students it's everything before @. For faculty/HOD it's the email prefix.
    let userId = email;
    if (role === 'student' && email.includes('@')) {
      userId = email.split('@')[0];
    }

    // Trigger parallel fetch for SerpApi Events Marquee
    loadEventsView(userId);

    const token = localStorage.getItem('kpi_token') || '';
    const response = await fetch(`http://localhost:8000/api/notifications?user_id=${userId}&role=${role}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    // Check if the response is actually OK
    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const data = await response.json();

    if (!Array.isArray(data) || data.length === 0) {
      container.innerHTML = '<div style="color:var(--neon-orange); padding:20px;">No insights available at this time.</div>';
      return;
    }

    let html = '';

    // Specific icon mapping array based on keywords in title
    const iconMap = {
      'improve': 'trending_up',
      'weak': 'warning',
      'strong': 'star',
      'blog': 'edit',
      'hackathon': 'code',
      'event': 'event',
      'mistake': 'error_outline',
      'strategy': 'lightbulb'
    };

    function getIcon(title) {
      let t = title.toLowerCase();
      for (let key in iconMap) {
        if (t.includes(key)) return iconMap[key];
      }
      return 'lightbulb_outline'; // default
    }

    data.forEach((item, index) => {
      // Add a slight stagger to the animation via inline style
      const delay = index * 0.15;

      const icon = getIcon(item.title);
      // We will mock the material icons with emojis since we don't have the font loaded, 
      // but keeping the logic in case we want to swap out.
      const emojiMap = {
        'trending_up': '📈', 'warning': '⚠️', 'star': '⭐', 'edit': '✍️', 'code': '💻',
        'event': '📅', 'error_outline': '🚨', 'lightbulb': '💡', 'lightbulb_outline': '✨'
      };

      // Format message if it contains dashed bullet points from the AI Engine
      let formattedMessage = item.message
        .replace(/(?:^|\n)-\s*(.*?)(?=\n|$)/g, '<li style="margin-left:22px; margin-bottom:6px; list-style-type:disc;">$1</li>')
        .replace(/\n/g, '<br>');

      html += `
        <div class="insight-item" style="display:flex; flex-direction:column; gap:12px; padding:20px; animation: fadeInUp 0.4s ease forwards; animation-delay: ${delay}s; opacity:0; transform:translateY(10px); background:rgba(0,245,255,0.02); border:1px solid rgba(0,245,255,0.1); border-radius:var(--radius-md);">
          <div style="font-size:2rem; flex-shrink:0; background:rgba(0,245,255,0.1); width:50px; height:50px; border-radius:12px; display:flex; align-items:center; justify-content:center;">
             ${emojiMap[icon] || '✨'}
          </div>
          <div style="flex:1; display:flex; flex-direction:column;">
            <h3 style="color:var(--neon-cyan); margin:0 0 8px 0; font-size:1.1rem;">${item.title}</h3>
            <div style="color:rgba(120,180,220,0.9); margin:0; line-height:1.6; font-size:0.95rem;">${formattedMessage}</div>
          </div>
        </div>
      `;
    });

    // Replace the loading animation with the actual content using a horizontal css grid format
    container.innerHTML = `<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px;">${html}</div>`;

    // Prepend engagement notifications if they were fetched earlier
    if (window._engagementHtml) {
      container.insertAdjacentHTML('afterbegin', `<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px; margin-bottom:16px;">${window._engagementHtml}</div>`);
      window._engagementHtml = '';
    }

  } catch (error) {
    console.error("Fetch Error:", error);
    container.innerHTML = `<div style="color:var(--neon-pink); padding: 20px;">Could not connect to the Neural Engine. Ensure the backend API is running.</div>`;
  }
}

// Global variables to store attached file text for the AI
window.ideaAttachmentText = "";

async function handleIdeaFileUpload(event) {
  const file = event.target.files[0];
  const indicator = document.getElementById('ideaFileIndicator');
  if (!file) {
    if (indicator) indicator.style.display = 'none';
    window.ideaAttachmentText = "";
    return;
  }

  if (indicator) {
    indicator.textContent = `Attached: ${file.name}`;
    indicator.style.display = 'block';
  }

  // Handle PDF files via server-side extraction
  if (file.type === "application/pdf" || file.name.toLowerCase().endsWith('.pdf')) {
    if (indicator) indicator.textContent = "Extracting PDF text, please wait...";
    try {
      const formData = new FormData();
      formData.append('file', file);
      const token = localStorage.getItem('kpi_token') || '';
      const response = await fetch('http://localhost:8000/api/extract-pdf', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      if (!response.ok) throw new Error('Server PDF extraction failed');
      const data = await response.json();
      window.ideaAttachmentText = `\n\n[Attached PDF Content (${file.name})]:\n${data.text}`;
      if (indicator) indicator.textContent = `Attached: ${file.name} (${data.pages} pages extracted)`;
    } catch (err) {
      console.error("Idea Enhancer PDF Error:", err);
      // Fallback: read as text (may contain partial readable content)
      const reader = new FileReader();
      reader.onload = (e) => {
        window.ideaAttachmentText = `\n\n[Attached File: ${file.name}]:\n${e.target.result.substring(0, 5000)}`;
      };
      reader.readAsText(file);
      if (indicator) indicator.textContent = `Attached: ${file.name} (basic extraction)`;
    }
    return;
  }

  // Normal text file handler
  const reader = new FileReader();
  reader.onload = (e) => {
    window.ideaAttachmentText = `\n\n[Attached File Content (${file.name})]:\n${e.target.result.substring(0, 5000)}`;
  };
  reader.readAsText(file);
}

// ── IDEA ENHANCER LOGIC ─────────────────────────────
async function submitIdeaToEnhancer() {
  const inputEl = document.getElementById('ideaInput');
  const resultEl = document.getElementById('ideaEnhancerResult');
  const btn = document.getElementById('enhanceIdeaBtn');
  const storedUser = JSON.parse(localStorage.getItem('kpi_user') || '{}');

  let ideaText = inputEl.value.trim();

  // Append dynamically attached file text if present
  if (window.ideaAttachmentText) {
    ideaText += window.ideaAttachmentText;
  }

  if (ideaText.length < 5) {
    showToast('Warning', 'Please type at least a few words describing your idea.');
    return;
  }

  // Set loading state
  const ogText = btn.innerHTML;
  btn.innerHTML = `<span style="display:inline-block;width:12px;height:12px;border:2px solid;border-radius:50%;border-top-color:transparent;animation:spin 1s linear infinite;"></span> Analyzing...`;
  btn.disabled = true;

  resultEl.innerHTML = `
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; gap:15px; color:rgba(120,180,220,0.7);">
      <div style="width:30px; height:30px; border:3px solid var(--neon-cyan); border-radius:50%; border-top-color:transparent; animation:spin 1s linear infinite;"></div>
      <div style="font-family:var(--font-mono); font-size: 0.8rem; letter-spacing:1px; animation:neonPulse 2s infinite;">EVALUATING TECHNICAL FEASIBILITY...</div>
    </div>
  `;

  try {
    const token = localStorage.getItem('kpi_token') || '';
    const userId = storedUser.email || 'student';

    const response = await fetch('http://localhost:8000/api/idea-enhancer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ idea: ideaText, user_id: userId })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Error communicating with AI");
    }

    // Basic markdown to HTML parsing for the specific requested JSON structure (bolding, headers, lists)
    let formattedHTML = data.critique
      .replace(/## (.*?)\n/g, '<h3 style="color:var(--neon-cyan); margin:16px 0 8px 0;">$1</h3>')
      .replace(/\*\*(.*?)\*\*/g, '<strong style="color:#fff;">$1</strong>')
      .replace(/\*(.*?)\n/g, '<li style="margin-left: 15px; margin-bottom: 6px;">$1</li>')
      .replace(/\n\n/g, '<br><br>');

    resultEl.innerHTML = `<div style="animation: fadeInUp 0.4s ease;">${formattedHTML}</div>`;

  } catch (error) {
    resultEl.innerHTML = `<div style="color:var(--neon-pink); text-align:center; padding-top:40px;">Failed to generate critique: ${error.message}</div>`;
  } finally {
    btn.innerHTML = ogText;
    btn.disabled = false;
  }
}

// ── EVENTS MARQUEE LOGIC ─────────────────────────────
async function loadEventsView(userId) {
  const container = document.getElementById('eventsContainer');
  if (!container) return;

  try {
    const token = localStorage.getItem('kpi_token') || '';
    const response = await fetch(`http://localhost:8000/api/events?user_id=${userId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (!response.ok) throw new Error("API Error fetching events");

    const data = await response.json();
    const events = data.events || [];

    if (events.length === 0) {
      container.innerHTML = '<div style="color:var(--neon-orange); padding:20px; text-align:center;">No upcoming events currently found.</div>';
      return;
    }

    // Build Marquee HTML
    let cardsHtml = '';
    events.forEach(ev => {
      const title = ev.title || "College Event";
      const date = ev.date?.when || "Upcoming";
      const link = ev.link || "#";
      const thumbnail = ev.thumbnail || "https://via.placeholder.com/150/000000/00f5ff?text=EVENT";

      cardsHtml += `
        <a href="${link}" target="_blank" style="text-decoration:none; display:flex; flex-direction:column; min-width:200px; width:200px; background:rgba(20,25,35,0.8); border:1px solid rgba(0,245,255,0.2); border-radius:12px; overflow:hidden; transition:transform 0.3s, box-shadow 0.3s; color:#fff; box-shadow: 0 4px 15px rgba(0,0,0,0.3);" onmouseover="this.style.transform='scale(1.02)'; this.style.boxShadow='0 0 15px rgba(0,245,255,0.3)';" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.3)';">
           <img src="${thumbnail}" style="width:100%; height:120px; object-fit:cover;" onerror="this.src='https://via.placeholder.com/150/000000/00f5ff?text=EVENT'">
           <div style="padding:15px; display:flex; flex-direction:column; flex:1;">
             <div style="color:var(--neon-cyan); font-size:0.75rem; font-family:var(--font-mono); margin-bottom:8px; text-transform:uppercase; letter-spacing:1px;">${date}</div>
             <div style="font-weight:600; font-size:0.95rem; line-height:1.4; overflow:hidden; display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; margin-bottom:10px;">${title}</div>
             <div style="margin-top:auto; font-size:0.8rem; color:rgba(120,180,220,0.6); display:flex; align-items:center; gap:4px;">
                <span>🔗</span> View Event
             </div>
           </div>
        </a>
      `;
    });

    // Duplicate the list of cards multiple times to ensure seamless infinite looping 
    // moving from left to right requires -50% to 0%.
    cardsHtml = cardsHtml + cardsHtml + cardsHtml;

    container.innerHTML = `
      <style>
        @keyframes scrollEventsLeftRight {
          0% { transform: translateX(-50%); }
          100% { transform: translateX(0); }
        }
        .events-marquee-track {
          display: flex;
          gap: 20px;
          width: max-content;
          animation: scrollEventsLeftRight 40s linear infinite;
          padding: 10px 0;
        }
        .events-marquee-track:hover {
          animation-play-state: paused;
        }
      </style>
      <div style="overflow:hidden; width:100%; height:100%; display:flex; align-items:center; position:absolute; left:0; right:0; top:0; bottom:0;">
        <div class="events-marquee-track">
          ${cardsHtml}
        </div>
      </div>
    `;

  } catch (error) {
    container.innerHTML = '<div style="color:var(--neon-pink); padding: 20px; text-align:center;">Unable to fetch events.</div>';
    console.error("Events Fetch Error:", error);
  }
}

// ── INIT ──────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initDashboardStats();
  initDashboardCharts();
  renderStudentsTable();
  renderFacultyTable();
  renderHODTable();
  populateKPIDropdown();
  loadStudentKPI();
  initFacultyKPI();

  // ── Engagement Notification Check ──
  const storedUser = JSON.parse(localStorage.getItem('kpi_user') || '{}');
  if (storedUser.email && storedUser.role === 'student') {
    const userId = storedUser.email.split('@')[0];
    const token = localStorage.getItem('kpi_token') || '';
    fetch(`http://localhost:8000/api/notifications/engagement?user_id=${userId}&role=${storedUser.role}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(engagementNotifs => {
        if (Array.isArray(engagementNotifs) && engagementNotifs.length > 0) {
          // Show a toast for the first engagement notification
          if (typeof showToast === 'function') {
            showToast(engagementNotifs[0].title + ' ' + engagementNotifs[0].message.split('\n')[0], 'info');
          }

          // Prepend engagement notifications to the recommendations container if visible
          const container = document.getElementById('recommendationsContainer');
          if (container) {
            let engHtml = '';
            engagementNotifs.forEach((item, index) => {
              let formattedMessage = item.message
                .replace(/(?:^|\n)-\s*(.*?)(?=\n|$)/g, '<li style="margin-left:22px; margin-bottom:6px; list-style-type:disc;">$1</li>')
                .replace(/\n/g, '<br>');

              engHtml += `
              <div class="engagement-notif" style="display:flex; flex-direction:column; gap:12px; padding:20px; animation: fadeInUp 0.4s ease forwards; animation-delay: ${index * 0.15}s; opacity:0; transform:translateY(10px); background:rgba(0,245,255,0.06); border:2px solid rgba(0,245,255,0.3); border-radius:var(--radius-md); box-shadow: 0 0 15px rgba(0,245,255,0.1);">
                <div style="font-size:2rem; flex-shrink:0; background:rgba(0,245,255,0.15); width:50px; height:50px; border-radius:12px; display:flex; align-items:center; justify-content:center;">⚡</div>
                <div style="flex:1; display:flex; flex-direction:column;">
                  <h3 style="color:var(--neon-cyan); margin:0 0 8px 0; font-size:1.1rem; text-shadow: 0 0 10px rgba(0,245,255,0.5);">${item.title}</h3>
                  <div style="color:rgba(120,180,220,0.9); margin:0; line-height:1.6; font-size:0.95rem;">${formattedMessage}</div>
                </div>
              </div>
            `;
            });
            // Store the engagement HTML to prepend when recommendations load
            window._engagementHtml = engHtml;
          }
        }
      })
      .catch(err => console.log('Engagement notification check failed:', err));
  }
});


// ============================================================
// OD REQUEST WORKFLOW — Complete JavaScript Module
// ============================================================

const API = 'http://localhost:8000/api';

// ── On-Load: Show/hide OD UI based on role ────────────────────
(function initODSection() {
  const userStr = localStorage.getItem('kpi_user');
  if (!userStr) return;
  const user = JSON.parse(userStr);

  const applyBar = document.getElementById('od-student-apply-bar');
  const facDash = document.getElementById('od-faculty-dashboard');

  if (user.role === 'student') {
    if (applyBar) applyBar.style.display = 'block';
    if (facDash) facDash.style.display = 'none';
  } else {
    // Faculty / HOD / Admin see the full list
    if (applyBar) applyBar.style.display = 'none';
    if (facDash) facDash.style.display = 'block';
    loadODRequests();
  }

  // ── FCM Deep-link URL handler ─────────────────────────────
  const params = new URLSearchParams(window.location.search);
  const action = params.get('action');
  const odId = params.get('od_id');

  if (action === 'claim_prize' && odId) {
    document.getElementById('claim_od_id').value = odId;
    document.getElementById('odClaimPrizeModalOverlay')?.classList.add('active');
    // Scroll to OD section
    document.getElementById('section-od')?.scrollIntoView({ behavior: 'smooth' });
  } else if (action === 'verify_participation' && odId) {
    document.getElementById('participated_od_id').value = odId;
    document.getElementById('odParticipatedModalOverlay')?.classList.add('active');
    document.getElementById('section-od')?.scrollIntoView({ behavior: 'smooth' });
  }
})();


// ── Helper: Render AI Verification Badge ─────────────────────
function renderVerifyBadge(status) {
  if (!status) return '<span style="color:rgba(120,180,220,0.4);font-size:0.8rem;">—</span>';
  const map = {
    'Passed': ['verify-passed', '🛡️ Verified'],
    'Flagged_Image_Altered': ['verify-flagged-tamper', '🚨 Forgery Detected'],
    'Flagged_Text_Mismatch': ['verify-flagged-mismatch', '⚠️ Text Mismatch'],
  };
  const [cls, label] = map[status] || ['verify-passed', status];
  return `<span class="verify-badge ${cls}">${label}</span>`;
}


// ── Helper: Render OD status badge ───────────────────────────
function renderStatusBadge(status) {
  const map = {
    'Pending Result': 'od-status-pending',
    'Awaiting Proof': 'od-status-awaiting',
    'Participated': 'od-status-participated',
    'Won': 'od-status-won',
  };
  const cls = map[status] || 'od-status-pending';
  return `<span class="od-status-badge ${cls}">${status}</span>`;
}


// ── Load OD Requests (Faculty Dashboard) ─────────────────────
async function loadODRequests() {
  const container = document.getElementById('odListContainer');
  if (!container) return;
  container.innerHTML = '<div style="text-align:center;color:rgba(120,180,220,0.5);padding:40px;">Loading...</div>';

  try {
    const res = await fetch(`${API}/od/all`);
    const data = await res.json();

    if (!data.length) {
      container.innerHTML = '<div style="text-align:center;color:rgba(120,180,220,0.4);padding:40px;">No OD requests found.</div>';
      return;
    }

    // Header row
    let html = `<div class="od-row" style="cursor:default">
      <span class="od-col-head">Student</span>
      <span class="od-col-head">Event</span>
      <span class="od-col-head">Date</span>
      <span class="od-col-head">Status</span>
      <span class="od-col-head">AI Verify</span>
    </div>`;

    data.forEach(od => {
      const prize = od.prize_details ? ` — ${od.prize_details}` : '';
      const certBtn = od.certificate_data
        ? `<button class="btn" onclick="event.stopPropagation();viewBase64Cert('${od.id}')"
             style="padding:3px 10px;font-size:0.7rem;margin-left:8px;">📄 View Cert</button>`
        : '';

      html += `<div class="od-row" onclick="openODDetailModal(${JSON.stringify(od).replace(/"/g, '&quot;')})">
        <span>${od.student_name}</span>
        <span style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${od.event_details}</span>
        <span>${od.date}</span>
        <span>${renderStatusBadge(od.result_status)}${prize}${certBtn}</span>
        <span>${renderVerifyBadge(od.verification_status)}</span>
      </div>`;
    });

    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<div style="text-align:center;color:var(--neon-pink);padding:40px;">Failed to load OD requests: ${err.message}</div>`;
  }
}

// ── View certificate from faculty dashboard ───────────────────
window._odCertCache = {};
function viewBase64Cert(odId) {
  // We'll reuse the existing viewDocumentModal if it exists
  if (window._odCertCache[odId]) {
    _showCertInModal(window._odCertCache[odId]);
    return;
  }
  fetch(`${API}/od/${odId}`)
    .then(r => r.json())
    .then(od => {
      window._odCertCache[odId] = od.certificate_data;
      _showCertInModal(od.certificate_data);
    });
}

function _showCertInModal(dataUrl) {
  const container = document.getElementById('documentViewerContainer');
  if (!container) return;
  if (dataUrl && dataUrl.startsWith('data:image')) {
    container.innerHTML = `<img src="${dataUrl}" style="max-width:100%;border-radius:8px;">`;
  } else {
    container.innerHTML = `<p style="color:rgba(120,180,220,0.7);">Certificate preview not available (PDF or text data).</p>`;
  }
  document.getElementById('viewDocumentModalOverlay')?.classList.add('active');
}


// ── Open OD Detail Modal (Faculty) ───────────────────────────
function openODDetailModal(od) {
  const content = document.getElementById('odDetailContent');
  if (!content) return;
  const rows = [
    ['Student', od.student_name],
    ['Student ID', od.student_id],
    ['College', od.college_name],
    ['Event', od.event_details],
    ['Date', od.date],
    ['Time', `${od.start_time} → ${od.end_time}`],
    ['Days', od.days],
    ['Status', renderStatusBadge(od.result_status)],
    ['Prize', od.prize_details || '—'],
    ['AI Verification', renderVerifyBadge(od.verification_status)],
    ['Submitted', new Date(od.created_at).toLocaleString()],
  ];
  content.innerHTML = rows.map(([label, val]) =>
    `<div class="od-detail-row">
      <span class="od-detail-label">${label}</span>
      <span class="od-detail-value">${val}</span>
    </div>`
  ).join('');
  if (od.certificate_data) {
    content.innerHTML += `<button class="btn btn-solid-cyan" onclick="viewBase64Cert(${od.id})"
      style="margin-top:12px;padding:8px 20px;font-size:0.85rem;">📄 View Certificate</button>`;
  }
  document.getElementById('odDetailModalOverlay')?.classList.add('active');
}

function closeODDetailModal() {
  document.getElementById('odDetailModalOverlay')?.classList.remove('active');
}


// ── Open / Close OD Apply Modal (Student) ────────────────────
function openODApplyModal() {
  document.getElementById('odApplyModalOverlay')?.classList.add('active');
}
function closeODApplyModal() {
  document.getElementById('odApplyModalOverlay')?.classList.remove('active');
  document.getElementById('odApplyForm')?.reset();
}


// ── Submit OD Request (Student) ──────────────────────────────
async function submitODRequest(e) {
  e.preventDefault();
  const userStr = localStorage.getItem('kpi_user');
  if (!userStr) { alert('Please log in first.'); return; }
  const user = JSON.parse(userStr);

  const btn = document.getElementById('odApplySubmitBtn');
  btn.textContent = 'Submitting...';
  btn.disabled = true;

  const payload = {
    student_id: user.email.split('@')[0].toUpperCase(),
    student_name: user.name || user.email,
    college_name: document.getElementById('od_college_name').value,
    date: document.getElementById('od_date').value,
    start_time: document.getElementById('od_start_time').value,
    end_time: document.getElementById('od_end_time').value,
    event_details: document.getElementById('od_event_details').value,
    days: parseInt(document.getElementById('od_days').value),
    fcm_token: null    // TODO: supply real FCM token once Firebase SDK is integrated in the app
  };

  try {
    const res = await fetch(`${API}/od/request`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Submit failed');
    closeODApplyModal();
    showToast('✅ OD Request submitted successfully!', 'success');
  } catch (err) {
    showToast(`❌ Failed: ${err.message}`, 'error');
  } finally {
    btn.textContent = 'Submit OD Request';
    btn.disabled = false;
  }
}


// ── Prize button selection ────────────────────────────────────
let _selectedPrize = null;
function selectPrize(btn) {
  document.querySelectorAll('.prize-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  _selectedPrize = btn.dataset.prize;
  // Enable submit after prize is selected
  document.getElementById('odClaimSubmitBtn').disabled = false;
}


// ── Submit OD Result with Certificate (Won flow) ─────────────
async function submitODResult(e, resultType) {
  e.preventDefault();
  const odId = document.getElementById('claim_od_id').value;
  if (!odId) { alert('Invalid OD request. Please re-open via the notification link.'); return; }

  const fileInput = document.getElementById('od_certificate_file');
  const file = fileInput?.files[0];
  const btn = document.getElementById('odClaimSubmitBtn');
  const warning = document.getElementById('odClaimElaWarning');

  btn.textContent = '🔍 Verifying Certificate...';
  btn.disabled = true;
  if (warning) warning.style.display = 'none';

  let certBase64 = null;

  if (file && file.type.startsWith('image/')) {
    // Run a quick client-side ELA pre-check
    certBase64 = await new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = e => resolve(e.target.result);
      reader.readAsDataURL(file);
    });

    try {
      const elaRes = await fetch(`${API}/kpi/verify-certificate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: certBase64 })
      });
      const elaData = await elaRes.json();

      if (elaData.is_suspicious) {
        if (warning) {
          warning.innerHTML = `🚨 <strong>Security Alert:</strong> This image failed our Error Level Analysis check (Tamper Score: ${elaData.score}). Please upload an original, unedited certificate.`;
          warning.style.display = 'block';
        }
        btn.textContent = 'Submit Result & Certificate';
        btn.disabled = false;
        return;    // Block submission
      }
    } catch (err) {
      console.warn('ELA pre-check failed (non-blocking):', err);
    }
  } else if (file) {
    // For PDFs or other files just read as base64
    certBase64 = await new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = e => resolve(e.target.result);
      reader.readAsDataURL(file);
    });
  }

  btn.textContent = '📤 Submitting...';

  try {
    const res = await fetch(`${API}/od/${odId}/upload-result`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        result: resultType,
        prize_details: _selectedPrize,
        certificate_base64: certBase64
      })
    });
    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || 'Submission failed');

    document.getElementById('odClaimPrizeModalOverlay')?.classList.remove('active');

    const verifyMsg = data.verification_status === 'Passed'
      ? '✅ Certificate verified by AI!'
      : `⚠️ Submitted (AI Note: ${data.verification_status?.replace(/_/g, ' ')})`;

    showToast(`🏆 Result submitted! ${verifyMsg}`, 'success');

    // Clean up URL params to prevent re-triggering
    window.history.replaceState({}, '', window.location.pathname);
  } catch (err) {
    showToast(`❌ Failed: ${err.message}`, 'error');
  } finally {
    btn.textContent = 'Submit Result & Certificate';
    btn.disabled = false;
  }
}


// ── Confirm Participated (no certificate needed) ──────────────
async function confirmParticipated() {
  const odId = document.getElementById('participated_od_id').value;
  if (!odId) { alert('Invalid OD ID.'); return; }

  try {
    const res = await fetch(`${API}/od/${odId}/participated`, { method: 'PUT' });
    if (!res.ok) throw new Error('Update failed');

    document.getElementById('odParticipatedModalOverlay')?.classList.remove('active');
    showToast('✅ Participation confirmed! Your faculty has been notified.', 'success');
    window.history.replaceState({}, '', window.location.pathname);
  } catch (err) {
    showToast(`❌ Failed: ${err.message}`, 'error');
  }
}

// ══════════════════════════════════════════════════
// NEURAL LIVE  —  voice-to-voice AI engine
//
// SAFETY GUARANTEES:
//  1. ENCAPSULATION   — all state is inside the class; the only
//     window export uses a unique Symbol key so it cannot clash
//     with the chatbot or any other existing global.
//  2. MIC KILL SWITCH — close() does a two-phase shutdown:
//     recog.stop() (graceful, clears browser tab mic indicator)
//     then recog.abort() (force-terminate) + all mic tracks stopped
//     + AudioContext suspended then closed.
//  3. EVENT ISOLATION — every Neural Live listener calls
//     stopPropagation() so events never bubble up to the chatbot.
//     No document-level keydown/keypress listeners are used.
// ══════════════════════════════════════════════════
(function _neuralLiveModule() {
  'use strict';

  class NeuralLive {
    constructor() {
      // ── DOM refs ──────────────────────────────
      this._overlay = document.getElementById('neural-live-overlay');
      this._core = document.getElementById('neural-core');
      this._status = document.getElementById('nl-status-text');
      this._tx = document.getElementById('nl-transcript');
      this._micBtn = document.getElementById('btn-nl-mic');
      this._closeBtn = document.getElementById('btn-nl-close');

      // ── Audio / Speech state (ALL private to this instance) ──
      this._audioCtx = null;
      this._analyser = null;
      this._micStream = null;
      this._rafId = null;
      this._recog = null;
      this._isListening = false;
      this._isSpeaking = false;

      this._bindEvents();
    }

    // ── 3. EVENT ISOLATION ──────────────────────────────────────
    // All listeners use stopPropagation so Neural Live events
    // never bubble up to document level and cannot accidentally
    // trigger the text chatbot's Enter-key or global handlers.
    _bindEvents() {
      const guard = (fn) => (e) => { e.stopPropagation(); fn.call(this, e); };

      document.getElementById('btn-neural-live')
        ?.addEventListener('click', guard(this.open));

      this._closeBtn
        ?.addEventListener('click', guard(this.close));

      this._micBtn
        ?.addEventListener('click', guard(this.toggleListening));

      this._core
        ?.addEventListener('click', guard(this.toggleListening));
    }

    // ── Public API ─────────────────────────────────────────────
    open() {
      this._overlay?.classList.add('active');
      this._setStatus('Tap the orb to begin', 'cyan');
      if (this._tx) this._tx.textContent = '';
    }

    // ── 2. MIC KILL SWITCH ───────────────────────────────────
    // Two-phase shutdown for a guaranteed clean state:
    //   Phase 1: recog.stop()  → graceful end, lets browser dismiss
    //                            the mic indicator in the tab
    //   Phase 2: recog.abort() → force-kill in case stop() stalls
    //   Phase 3: stop all MediaStreamTrack objects
    //   Phase 4: suspend() then close() the AudioContext
    close() {
      this._killMic();                         // Phase 1-4
      window.speechSynthesis?.cancel();
      this._isSpeaking = false;
      this._overlay?.classList.remove('active');
      this._core?.classList.remove('listening', 'speaking');
      if (this._core) this._core.style.transform = '';
      if (this._micBtn) this._micBtn.textContent = '🎙 START LISTENING';
      this._micBtn?.classList.remove('active-mic');
      this._setStatus('Tap the orb to begin', 'cyan');
    }

    async toggleListening() {
      this._isListening ? this.stopListening() : await this.startListening();
    }

    async startListening() {
      if (this._isListening) return;

      // Acquire microphone
      try {
        this._micStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
      } catch {
        this._setStatus('Microphone access denied', 'pink');
        return;
      }

      // AudioContext + AnalyserNode — strictly local to this instance
      this._audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      this._analyser = this._audioCtx.createAnalyser();
      this._analyser.fftSize = 64;
      const src = this._audioCtx.createMediaStreamSource(this._micStream);
      src.connect(this._analyser);
      this._startViz();

      // SpeechRecognition — strictly local
      const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SR) {
        this._setStatus('SpeechRecognition not supported in this browser', 'pink');
        return;
      }
      this._recog = new SR();
      this._recog.lang = 'en-US';
      this._recog.interimResults = true;
      this._recog.continuous = false;
      this._recog.maxAlternatives = 1;

      this._recog.onstart = () => {
        this._isListening = true;
        this._core?.classList.add('listening');
        this._core?.classList.remove('speaking');
        this._micBtn?.classList.add('active-mic');
        if (this._micBtn) this._micBtn.textContent = '⏹ STOP LISTENING';
        this._setStatus('Listening...', 'green');
      };

      this._recog.onresult = (e) => {
        let interim = '', final = '';
        for (const r of e.results) r.isFinal ? (final += r[0].transcript) : (interim += r[0].transcript);
        if (this._tx) this._tx.textContent = final || interim;
        if (final) {
          // Phase 1 graceful stop happens here before processing
          this._recog.stop();
          this._onFinal(final.trim());
        }
      };

      this._recog.onerror = (e) => {
        this._setStatus(`Recognition error: ${e.error}`, 'pink');
        this.stopListening();
      };

      // onend fires for both .stop() and .abort() — only act if
      // we didn't manually call stopListening already
      this._recog.onend = () => {
        if (this._isListening) this.stopListening();
      };

      this._recog.start();
    }

    stopListening() {
      this._isListening = false;
      this._killMic();
      this._core?.classList.remove('listening');
      if (this._core) this._core.style.transform = '';
      this._micBtn?.classList.remove('active-mic');
      if (this._micBtn) this._micBtn.textContent = '🎙 START LISTENING';
    }

    // ── Private helpers ─────────────────────────────────────────

    // Two-phase mic kill: graceful stop → force abort → tracks → AudioContext
    _killMic() {
      if (this._recog) {
        try { this._recog.stop(); } catch { /* already stopped */ }
        // Short delay then abort to ensure browser clears mic indicator
        setTimeout(() => { try { this._recog?.abort(); } catch { /* noop */ } }, 80);
        this._recog = null;
      }
      // Stop all mic tracks — browser tab mic indicator turns off here
      this._micStream?.getTracks().forEach(t => t.stop());
      this._micStream = null;

      // Cancel viz loop BEFORE closing context to prevent "closed context" errors
      this._stopViz();

      // Suspend first (async-safe), then close
      if (this._audioCtx) {
        this._audioCtx.suspend().catch(() => { }).finally(() => {
          this._audioCtx?.close().catch(() => { });
          this._audioCtx = null;
          this._analyser = null;
        });
      }
    }

    _startViz() {
      if (!this._analyser) return;
      const buf = new Uint8Array(this._analyser.frequencyBinCount);
      const tick = () => {
        this._rafId = requestAnimationFrame(tick);
        try {
          this._analyser.getByteFrequencyData(buf);
          const avg = buf.reduce((a, v) => a + v, 0) / buf.length;
          const scale = 1 + (avg / 255) * 0.55;
          if (this._core) this._core.style.transform = `scale(${scale.toFixed(3)})`;
        } catch { this._stopViz(); }
      };
      tick();
    }

    _stopViz() {
      cancelAnimationFrame(this._rafId);
      this._rafId = null;
    }

    _setStatus(msg, colour) {
      if (!this._status) return;
      const map = { cyan: 'rgba(0,245,255,0.7)', green: 'rgba(57,255,20,0.8)', purple: 'rgba(191,0,255,0.8)', pink: 'rgba(255,0,110,0.8)' };
      this._status.textContent = msg;
      this._status.style.color = map[colour] || map.cyan;
    }

    async _onFinal(text) {
      if (!text) return;
      this.stopListening();
      this._setStatus('Thinking...', 'purple');
      const stored = localStorage.getItem('kpi_user');
      const user = stored ? JSON.parse(stored) : {};
      try {
        const res = await fetch('http://localhost:8000/api/neural-live', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: text,
            user_id: user.email?.split('@')[0] || 'user',
            role: user.role || 'student'
          })
        });
        const data = await res.json();
        const reply = data.response || 'Sorry, I could not get a response. Please try again.';
        if (this._tx) this._tx.textContent = reply;
        this._speak(reply);
      } catch {
        this._setStatus('Network error — backend unreachable', 'pink');
      }
    }

    _speak(text) {
      window.speechSynthesis?.cancel();
      this._isSpeaking = true;
      this._setStatus('Neural Live is speaking...', 'purple');
      this._core?.classList.add('speaking');
      this._core?.classList.remove('listening');

      const utt = new SpeechSynthesisUtterance(text);
      utt.rate = 1.0; utt.pitch = 1.05; utt.volume = 1.0;
      // Load voices asynchronously if not yet available
      const applyVoice = () => {
        const voices = window.speechSynthesis.getVoices();
        const preferred = voices.find(v => /Samantha|Female|Google UK|Zira/i.test(v.name)) || voices[0];
        if (preferred) utt.voice = preferred;
      };
      if (window.speechSynthesis.getVoices().length) {
        applyVoice();
      } else {
        window.speechSynthesis.onvoiceschanged = applyVoice;
      }

      utt.onend = () => {
        this._isSpeaking = false;
        this._core?.classList.remove('speaking');
        this._setStatus('Tap the orb to speak again', 'cyan');
      };
      window.speechSynthesis.speak(utt);
    }
  }

  // ── 1. ENCAPSULATION ───────────────────────────────────────────
  // Export via a unique Symbol so this can never be accidentally
  // overwritten by the chatbot or any other script on window.
  // Access via: window[Symbol.for('NeuralLive')]
  // (The convenience alias window._neuralLive is also kept for
  //  debugging, but is separate from any chatbot variable.)
  document.addEventListener('DOMContentLoaded', () => {
    // Guard: only instantiate once even if DOMContentLoaded fires twice
    if (window[Symbol.for('NeuralLive')]) return;
    setTimeout(() => {
      const instance = new NeuralLive();
      window[Symbol.for('NeuralLive')] = instance;
      // Convenience alias for dev console debugging only
      window._neuralLive = instance;
    }, 650);
  }, { once: true }); // `once: true` guarantees single execution

}()); // end _neuralLiveModule IIFE




