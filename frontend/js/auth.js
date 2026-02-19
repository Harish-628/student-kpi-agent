/* ============================================
   Authentication JavaScript
   ============================================ */

class AuthManager {
    constructor() {
        this.loginForm = document.getElementById('loginForm');
        this.togglePassword = document.getElementById('togglePassword');
        this.demoModal = document.getElementById('demoModal');
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        this.togglePassword.addEventListener('click', () => this.togglePasswordVisibility());
    }

    togglePasswordVisibility() {
        const passwordInput = document.getElementById('password');
        const toggleBtn = document.getElementById('togglePassword');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleBtn.textContent = '👁️‍🗨️';
        } else {
            passwordInput.type = 'password';
            toggleBtn.textContent = '👁️';
        }
    }

    handleLogin(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const role = document.getElementById('role').value;
        const remember = document.getElementById('remember').checked;

        // Validate inputs
        if (!email || !password || !role) {
            this.showNotification('Please fill in all fields', 'error');
            return;
        }

        // Simulate API call (in production, this would call your backend)
        this.simulateLogin(email, password, role, remember);
    }

    simulateLogin(email, password, role, remember) {
        // Simulate API call with delay
        const loginBtn = this.loginForm.querySelector('.btn-login');
        loginBtn.disabled = true;
        loginBtn.textContent = '🔄 Signing in...';

        setTimeout(() => {
            // Mock validation - in production, validate against backend
            const validCredentials = {
                'student@example.com': 'password123',
                'faculty@example.com': 'password123',
                'coordinator@example.com': 'password123',
                'admin@example.com': 'admin123'
            };

            if (validCredentials[email] === password) {
                // Store user session
                this.storeSession({
                    email: email,
                    role: role,
                    remember: remember
                });

                this.showNotification('✅ Login successful! Redirecting...', 'success');
                
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1000);
            } else {
                this.showNotification('❌ Invalid email or password', 'error');
                loginBtn.disabled = false;
                loginBtn.textContent = 'Sign In';
            }
        }, 1000);
    }

    storeSession(userData) {
        const storage = userData.remember ? localStorage : sessionStorage;
        storage.setItem('user', JSON.stringify({
            email: userData.email,
            role: userData.role,
            loginTime: new Date().toISOString()
        }));
    }

    showNotification(message, type = 'info') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background-color: ${this.getColorForType(type)};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            animation: slideUp 0.3s ease-out;
            z-index: 10000;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    getColorForType(type) {
        const colors = {
            'success': '#10b981',
            'error': '#ef4444',
            'warning': '#f59e0b',
            'info': '#3b82f6'
        };
        return colors[type] || colors['info'];
    }
}

// Demo credentials modal
class DemoModal {
    constructor() {
        this.modal = document.getElementById('demoModal');
        this.closeBtn = this.modal.querySelector('.close-modal');
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.closeBtn.addEventListener('click', () => this.closeModal());
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.closeModal();
        });
    }

    openModal() {
        this.modal.classList.add('active');
    }

    closeModal() {
        this.modal.classList.remove('active');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const authManager = new AuthManager();
    const demoModal = new DemoModal();

    // Create demo credentials button dynamically
    const authFooter = document.querySelector('.auth-footer');
    const demoBtn = document.createElement('div');
    demoBtn.style.cssText = 'margin-top: 1rem; text-align: center;';
    demoBtn.innerHTML = '<a href="#" style="color: #667eea; font-size: 0.9rem;" id="demoCreds">📋 Demo Credentials</a>';
    authFooter.appendChild(demoBtn);

    document.getElementById('demoCreds').addEventListener('click', (e) => {
        e.preventDefault();
        demoModal.openModal();
    });

    // Auto-fill demo credentials
    document.addEventListener('click', (e) => {
        if (e.target.closest('.credentials-table tr')) {
            const row = e.target.closest('tr');
            if (row.querySelectorAll('td').length > 0) {
                const email = row.querySelectorAll('td')[1].textContent;
                const password = row.querySelectorAll('td')[2].textContent;
                const role = row.querySelectorAll('td')[0].textContent.toLowerCase();

                document.getElementById('email').value = email;
                document.getElementById('password').value = password;
                document.getElementById('role').value = role;
                demoModal.closeModal();
            }
        }
    });
});
