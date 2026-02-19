/* ============================================
   Dashboard JavaScript
   ============================================ */

class Dashboard {
    constructor() {
        this.user = this.getSessionUser();
        if (!this.user) {
            window.location.href = 'index.html';
            return;
        }

        this.roleConfig = this.getRoleConfig();
        this.init();
    }

    getSessionUser() {
        let user = JSON.parse(localStorage.getItem('user') || sessionStorage.getItem('user'));
        return user || null;
    }

    getRoleConfig() {
        const configs = {
            'student': {
                name: 'Student Dashboard',
                menuItems: ['dashboard', 'kpi', 'analytics', 'settings'],
                kpiCards: ['kpiScore', 'careerReadiness', 'topAchievement'],
                icon: '🎓'
            },
            'faculty': {
                name: 'Faculty Dashboard',
                menuItems: ['dashboard', 'students', 'kpi', 'analytics', 'settings'],
                kpiCards: ['totalStudents', 'averageKPI', 'topPerfomers'],
                icon: '👨‍🏫'
            },
            'coordinator': {
                name: 'Coordinator Dashboard',
                menuItems: ['dashboard', 'students', 'kpi', 'analytics', 'settings'],
                kpiCards: ['departmentStudents', 'departmentKPI', 'departmentAverage'],
                icon: '📋'
            },
            'admin': {
                name: 'Admin Dashboard',
                menuItems: ['dashboard', 'students', 'kpi', 'users', 'analytics', 'settings'],
                kpiCards: ['totalUsers', 'totalStudents', 'systemHealth'],
                icon: '⚙️'
            }
        };

        return configs[this.user.role] || configs['student'];
    }

    init() {
        this.setupUser();
        this.setupNavigation();
        this.setupEventListeners();
        this.loadDashboardData();
        this.setupRoleBasedUI();
    }

    setupUser() {
        const userInitials = this.user.email.charAt(0).toUpperCase();
        document.getElementById('userAvatar').textContent = userInitials;
        document.getElementById('userName').textContent = this.user.email.split('@')[0];
        document.getElementById('userRole').textContent = this.user.role.charAt(0).toUpperCase() + this.user.role.slice(1);
    }

    setupNavigation() {
        const menuItems = {
            dashboard: { icon: '🏠', label: 'Dashboard', section: 'dashboard' },
            students: { icon: '👥', label: 'Students', section: 'students' },
            kpi: { icon: '📊', label: 'KPI Tracking', section: 'kpi' },
            users: { icon: '👤', label: 'Users', section: 'users' },
            analytics: { icon: '📈', label: 'Analytics', section: 'analytics' },
            settings: { icon: '⚙️', label: 'Settings', section: 'settings' }
        };

        const managementNav = document.getElementById('managementNav');
        const visibleItems = this.roleConfig.menuItems.filter(item => item !== 'dashboard' && item !== 'analytics' && item !== 'settings');

        managementNav.innerHTML = visibleItems.map(item => {
            const config = menuItems[item];
            return `<li><a href="#${item}" class="nav-link" data-section="${config.section}">
                <span class="nav-icon">${config.icon}</span>
                <span>${config.label}</span>
            </a></li>`;
        }).join('');
    }

    setupEventListeners() {
        // Navigation links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.switchSection(link.dataset.section);
                this.updateActiveNav(link);
            });
        });

        // Logout
        document.getElementById('logoutBtn').addEventListener('click', () => this.logout());

        // Sidebar toggle
        document.getElementById('toggleSidebar').addEventListener('click', () => {
            const sidebar = document.querySelector('.sidebar');
            document.body.classList.toggle('sidebar-open');
            sidebar.classList.toggle('active');
        });

        // Modal close buttons
        document.querySelectorAll('.close-modal').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal');
                if (modal) modal.classList.remove('active');
            });
        });

        // Add Student Button
        document.getElementById('addStudentBtn')?.addEventListener('click', () => {
            this.openModal('addStudentModal');
        });

        // Add Student Form
        document.getElementById('addStudentForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleAddStudent();
        });

        // Add KPI Button
        document.getElementById('addKPIBtn')?.addEventListener('click', () => {
            document.getElementById('kpiFormContainer').style.display = 
                document.getElementById('kpiFormContainer').style.display === 'none' ? 'block' : 'none';
        });

        // Cancel KPI Button
        document.getElementById('cancelKPIBtn')?.addEventListener('click', () => {
            document.getElementById('kpiFormContainer').style.display = 'none';
        });

        // KPI Form Submit
        document.getElementById('kpiForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleAddKPI();
        });

        // Profile Settings Form
        document.getElementById('profileForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.showToast('Profile settings saved successfully', 'success');
        });

        // Password Form
        document.getElementById('passwordForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const newPassword = document.getElementById('newPassword').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            
            if (newPassword !== confirmPassword) {
                this.showToast('Passwords do not match', 'error');
                return;
            }
            
            this.showToast('Password changed successfully', 'success');
            document.getElementById('passwordForm').reset();
        });
    }

    setupRoleBasedUI() {
        // Hide sections not available for this role
        const allSections = ['dashboard', 'students', 'kpi', 'users', 'analytics', 'settings'];
        allSections.forEach(section => {
            const sectionEl = document.getElementById(`${section}-section`);
            if (sectionEl && !this.roleConfig.menuItems.includes(section)) {
                sectionEl.style.display = 'none';
            }
        });

        // Set dashboard subtitle
        const subtitles = {
            'student': 'Track and monitor your academic KPIs and career readiness',
            'faculty': 'Monitor your students\' performance and KPI metrics',
            'coordinator': 'Manage department-wide KPI tracking and analytics',
            'admin': 'System overview and administration'
        };
        document.getElementById('dashboardSubtitle').textContent = subtitles[this.user.role];
    }

    loadDashboardData() {
        this.populateKPICards();
        this.populateRecentActivity();
        this.loadStudentData();
        this.loadKPIData();
        this.initializeCharts();
    }

    populateKPICards() {
        const container = document.getElementById('kpiCardsContainer');
        
        const cardData = {
            'student': [
                { icon: '📊', title: 'Your KPI Score', value: '87', change: '+5 this month', type: 'success' },
                { icon: '🚀', title: 'Career Readiness', value: '72%', change: '+3%', type: 'warning' },
                { icon: '🏆', title: 'Top Achievement', value: 'Hackathon', change: 'Winner', type: 'info' }
            ],
            'faculty': [
                { icon: '👥', title: 'Total Students', value: '125', change: '+12 this semester', type: 'info' },
                { icon: '📊', title: 'Average KPI', value: '78', change: '+5 this month', type: 'success' },
                { icon: '🌟', title: 'Top Performers', value: '15', change: '+3 this month', type: 'success' }
            ],
            'coordinator': [
                { icon: '👥', title: 'Department Students', value: '450', change: '+25 this year', type: 'info' },
                { icon: '📊', title: 'Department KPI Avg', value: '81', change: '+4 this month', type: 'success' },
                { icon: '📈', title: 'Growth Rate', value: '8.5%', change: '+2.3%', type: 'success' }
            ],
            'admin': [
                { icon: '👤', title: 'Total Users', value: '1,250', change: '+180 this month', type: 'info' },
                { icon: '👥', title: 'Total Students', value: '3,500', change: '+450 this semester', type: 'success' },
                { icon: '✅', title: 'System Health', value: '99.8%', change: 'All systems operational', type: 'success' }
            ]
        };

        const data = cardData[this.user.role] || [];
        
        container.innerHTML = data.map(card => `
            <div class="kpi-card ${card.type}">
                <div class="card-icon">${card.icon}</div>
                <div class="card-title">${card.title}</div>
                <div class="card-value">${card.value}</div>
                <div class="card-change">${card.change}</div>
            </div>
        `).join('');
    }

    populateRecentActivity() {
        const activities = [
            { icon: '✅', title: 'KPI Data Updated', time: '2 hours ago' },
            { icon: '📝', title: 'New Student Added', time: '5 hours ago' },
            { icon: '📊', title: 'Report Generated', time: '1 day ago' },
            { icon: '🎓', title: 'Achievement Unlocked', time: '2 days ago' }
        ];

        const activityList = document.getElementById('activityList');
        activityList.innerHTML = activities.map(activity => `
            <div class="activity-item">
                <div class="activity-icon">${activity.icon}</div>
                <div class="activity-content">
                    <div class="activity-title">${activity.title}</div>
                    <div class="activity-time">${activity.time}</div>
                </div>
            </div>
        `).join('');
    }

    loadStudentData() {
        const studentData = [
            { id: 'STU001', name: 'John Doe', dept: 'CSE', year: 3, kpi: 85, status: 'Active' },
            { id: 'STU002', name: 'Jane Smith', dept: 'ECE', year: 2, kpi: 92, status: 'Active' },
            { id: 'STU003', name: 'Mike Johnson', dept: 'CSE', year: 4, kpi: 78, status: 'Active' },
            { id: 'STU004', name: 'Sarah Williams', dept: 'ME', year: 3, kpi: 88, status: 'Active' }
        ];

        const tbody = document.getElementById('studentTableBody');
        if (tbody) {
            tbody.innerHTML = studentData.map(student => `
                <tr>
                    <td>${student.id}</td>
                    <td>${student.name}</td>
                    <td>${student.dept}</td>
                    <td>${student.year}</td>
                    <td><strong>${student.kpi}</strong></td>
                    <td><span class="badge badge-success">${student.status}</span></td>
                    <td>
                        <button class="btn btn-primary" style="padding: 5px 10px; font-size: 0.85rem;">Edit</button>
                    </td>
                </tr>
            `).join('');
        }

        // Populate department filter
        const deptFilter = document.getElementById('filterDepartment');
        if (deptFilter) {
            const departments = [...new Set(studentData.map(s => s.dept))];
            const existingOptions = deptFilter.querySelectorAll('option');
            const lastOption = existingOptions[existingOptions.length - 1];
            
            departments.forEach(dept => {
                if (![...deptFilter.querySelectorAll('option')].some(opt => opt.value === dept)) {
                    const option = document.createElement('option');
                    option.value = dept;
                    option.textContent = dept;
                    deptFilter.insertBefore(option, lastOption);
                }
            });
        }

        // Populate student dropdown for KPI form
        const studentSelect = document.getElementById('studentSelect');
        if (studentSelect) {
            studentSelect.innerHTML = '<option value="">-- Choose Student --</option>' +
                studentData.map(s => `<option value="${s.id}">${s.name} (${s.id})</option>`).join('');
        }
    }

    loadKPIData() {
        const kpiRecords = document.getElementById('kpiRecords');
        if (!kpiRecords) return;

        const mockKPIData = [
            { studentId: 'STU001', studentName: 'John Doe', internships: 2, certifications: 3, hackathons: 1, publications: 0, workshops: 4, projects: 5, clubActivities: 2, industrialVisits: 1 },
            { studentId: 'STU002', studentName: 'Jane Smith', internships: 3, certifications: 5, hackathons: 2, publications: 1, workshops: 6, projects: 8, clubActivities: 3, industrialVisits: 2 }
        ];

        kpiRecords.innerHTML = mockKPIData.map(record => `
            <div class="kpi-record-card">
                <div class="kpi-record-header">
                    <div>
                        <div style="font-weight: 600;">${record.studentName}</div>
                        <div style="font-size: 0.85rem; color: #6b7280;">${record.studentId}</div>
                    </div>
                    <button class="btn btn-secondary" style="padding: 5px 10px; font-size: 0.85rem;">Edit</button>
                </div>
                <div class="kpi-record-stats">
                    <div class="kpi-stat">
                        <div class="kpi-stat-label">Internships</div>
                        <div class="kpi-stat-value">${record.internships}</div>
                    </div>
                    <div class="kpi-stat">
                        <div class="kpi-stat-label">Certifications</div>
                        <div class="kpi-stat-value">${record.certifications}</div>
                    </div>
                    <div class="kpi-stat">
                        <div class="kpi-stat-label">Hackathons</div>
                        <div class="kpi-stat-value">${record.hackathons}</div>
                    </div>
                    <div class="kpi-stat">
                        <div class="kpi-stat-label">Publications</div>
                        <div class="kpi-stat-value">${record.publications}</div>
                    </div>
                    <div class="kpi-stat">
                        <div class="kpi-stat-label">Workshops</div>
                        <div class="kpi-stat-value">${record.workshops}</div>
                    </div>
                    <div class="kpi-stat">
                        <div class="kpi-stat-label">Projects</div>
                        <div class="kpi-stat-value">${record.projects}</div>
                    </div>
                    <div class="kpi-stat">
                        <div class="kpi-stat-label">Club Activities</div>
                        <div class="kpi-stat-value">${record.clubActivities}</div>
                    </div>
                    <div class="kpi-stat">
                        <div class="kpi-stat-label">Industrial Visits</div>
                        <div class="kpi-stat-value">${record.industrialVisits}</div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    initializeCharts() {
        // Initialize Chart.js charts if available
        if (typeof Chart === 'undefined') return;

        // KPI Chart
        const kpiCtx = document.getElementById('kpiChart');
        if (kpiCtx) {
            new Chart(kpiCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Internships', 'Certifications', 'Hackathons', 'Publications', 'Workshops'],
                    datasets: [{
                        data: [15, 25, 10, 8, 20],
                        backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }

        // Trends Chart
        const trendsCtx = document.getElementById('trendsChart');
        if (trendsCtx) {
            new Chart(trendsCtx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'KPI Score',
                        data: [65, 70, 75, 78, 85, 87],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: true
                        }
                    }
                }
            });
        }

        // Department Chart (for analytics)
        const deptCtx = document.getElementById('departmentChart');
        if (deptCtx) {
            new Chart(deptCtx, {
                type: 'bar',
                data: {
                    labels: ['CSE', 'ECE', 'ME', 'CIVIL', 'IT'],
                    datasets: [{
                        label: 'Average KPI Score',
                        data: [82, 78, 75, 80, 85],
                        backgroundColor: '#667eea'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    indexAxis: 'y'
                }
            });
        }
    }

    switchSection(sectionName) {
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        
        const section = document.getElementById(`${sectionName}-section`);
        if (section) {
            section.classList.add('active');
            document.getElementById('pageTitle').textContent = 
                sectionName.charAt(0).toUpperCase() + sectionName.slice(1).replace('-', ' ');
        }
    }

    updateActiveNav(activeLink) {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        activeLink.classList.add('active');
    }

    handleAddStudent() {
        const formData = {
            studentId: document.getElementById('newStudentId').value,
            name: document.getElementById('newStudentName').value,
            department: document.getElementById('newStudentDept').value,
            section: document.getElementById('newStudentSection').value,
            year: document.getElementById('newStudentYear').value
        };

        this.showToast(`Student ${formData.name} added successfully!`, 'success');
        document.getElementById('addStudentForm').reset();
        this.closeModal('addStudentModal');
    }

    handleAddKPI() {
        const studentId = document.getElementById('studentSelect').value;
        if (!studentId) {
            this.showToast('Please select a student', 'error');
            return;
        }

        const kpiData = {
            studentId,
            internships: parseInt(document.getElementById('internships').value),
            certifications: parseInt(document.getElementById('certifications').value),
            hackathons: parseInt(document.getElementById('hackathons').value),
            publications: parseInt(document.getElementById('publications').value),
            workshops: parseInt(document.getElementById('workshops').value),
            projects: parseInt(document.getElementById('projects').value),
            clubActivities: parseInt(document.getElementById('clubActivities').value),
            industrialVisits: parseInt(document.getElementById('industrialVisits').value)
        };

        this.showToast('KPI data saved successfully!', 'success');
        document.getElementById('kpiForm').reset();
        document.getElementById('kpiFormContainer').style.display = 'none';
    }

    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.add('active');
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.remove('active');
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast show ${type}`;
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    logout() {
        localStorage.removeItem('user');
        sessionStorage.removeItem('user');
        this.showToast('Logged out successfully', 'success');
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1000);
    }
}

// Initialize Dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Dashboard();
});
