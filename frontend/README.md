# Student KPI Management System - Frontend

A professional, modern, and feature-rich frontend for managing student KPI (Key Performance Indicators) with role-based authentication and comprehensive dashboards.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Role-Based Functionality](#role-based-functionality)
- [Getting Started](#getting-started)
- [Demo Credentials](#demo-credentials)
- [File Structure](#file-structure)
- [Customization](#customization)

## ✨ Features

### General Features
- ✅ Modern, professional UI design with gradient backgrounds
- ✅ Fully responsive design (desktop, tablet, mobile)
- ✅ Role-based authentication system
- ✅ Dark/Light mode support
- ✅ Real-time data visualization with Chart.js
- ✅ Toast notifications for user feedback
- ✅ Modal dialogs for forms and confirmations
- ✅ Smooth animations and transitions
- ✅ Mobile-friendly sidebar navigation

### Authentication Features
- 👤 Secure login page with email/password validation
- 🔐 Password visibility toggle
- 💾 Remember me functionality (localStorage/sessionStorage)
- 🔑 4 different user roles with unique dashboards
- 📋 Demo credentials display modal

### Dashboard Features
- 📊 KPI metric cards with real-time data
- 📈 Interactive charts and graphs
- 👥 Student management system
- 📝 KPI tracking and data entry
- 📊 Analytics and reporting
- 👤 User management (Admin only)
- ⚙️ Profile and preference settings
- 🔔 Notification system
- 📱 Activity feed

## 👥 Role-Based Functionality

### 1. **Student** 🎓
- **Dashboard**: View personal KPI score, career readiness percentage
- **KPI Tracking**: View own KPI metrics
- **Analytics**: Personal performance trends
- **Settings**: Profile and password management

**KPI Sections**: Internships, Certifications, Hackathons, Publications, Workshops, Projects, Club Activities, Industrial Visits

### 2. **Faculty/Teacher** 👨‍🏫
- **Dashboard**: Total students, average KPI, top performers
- **Student Management**: View and manage assigned students
- **KPI Tracking**: Monitor student KPI data
- **Analytics**: Department and student performance analytics
- **Settings**: Profile management

### 3. **Department Coordinator** 📋
- **Dashboard**: Department statistics, growth metrics
- **Student Management**: Manage all department students
- **KPI Tracking**: Department-wide KPI tracking
- **Analytics**: Comprehensive department analytics
- **Settings**: Department preferences

### 4. **Administrator** ⚙️
- **Dashboard**: System-wide metrics and health
- **Student Management**: Manage all students
- **KPI Tracking**: System-wide KPI management
- **User Management**: Manage all users and roles
- **Analytics**: System-wide analytics and reports
- **Settings**: System configuration

## 🚀 Getting Started

### 1. Open the Frontend
```bash
# Navigate to the frontend folder
cd frontend

# Open index.html in your browser
# Using Python (simple HTTP server)
python -m http.server 8080

# Using Node.js
npx http-server

# Or directly open in browser
# File -> Open -> frontend/index.html
```

### 2. Login with Demo Credentials
Click on "📋 Demo Credentials" button to see available test accounts.

### 3. Start Using the Dashboard
After login, you'll be redirected to the role-specific dashboard.

## 📋 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Student | student@example.com | password123 |
| Faculty | faculty@example.com | password123 |
| Coordinator | coordinator@example.com | password123 |
| Admin | admin@example.com | admin123 |

## 📁 File Structure

```
frontend/
├── index.html                 # Login page
├── dashboard.html             # Main dashboard (all roles)
├── css/
│   ├── styles.css             # Global styles & utilities
│   ├── auth.css               # Authentication page styles
│   └── dashboard.css          # Dashboard & layout styles
├── js/
│   ├── auth.js                # Authentication logic
│   ├── dashboard.js           # Dashboard functionality
│   └── charts.js              # Chart.js configurations
├── README.md                  # This file
└── assets/
    └── (images/icons - optional)
```

## 🎨 Design Features

### Color Scheme
- **Primary**: #6366f1 (Indigo)
- **Secondary**: #8b5cf6 (Purple)
- **Success**: #10b981 (Green)
- **Warning**: #f59e0b (Amber)
- **Danger**: #ef4444 (Red)
- **Info**: #3b82f6 (Blue)

### Typography
- Font Family: System fonts (-apple-system, Segoe UI, Roboto)
- Responsive text sizes
- Professional hierarchy

### Components
- Cards with hover effects
- Buttons with gradient backgrounds
- Forms with focus states
- Tables with striping
- Modals with animations
- Navigation with active states

## 💻 Browser Compatibility

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers

## 🔧 Customization

### Change Color Scheme
Edit CSS variables in `css/styles.css`:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    /* ... modify colors ... */
}
```

### Add New Navigation Items
Edit `setupNavigation()` in `js/dashboard.js`:
```javascript
const menuItems = {
    newItem: { icon: '🆕', label: 'New Item', section: 'new-item' },
    // ...
};
```

### Modify KPI Categories
Edit the form in `dashboard.html` under the KPI section:
```html
<div class="form-group">
    <label for="newKPIItem">New KPI Item</label>
    <input type="number" id="newKPIItem" min="0" value="0">
</div>
```

## 📊 Integration with Backend

The frontend is designed to work with your FastAPI backend:

```javascript
// Example API call (modify fetch URLs)
fetch('http://localhost:8000/api/student/add', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(studentData)
})
```

### Backend Integration Steps
1. Start your FastAPI server: `python backend/main.py`
2. Enable CORS in your FastAPI app:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📈 Data Visualization

The dashboard includes multiple chart types:
- **Doughnut Charts**: KPI distribution
- **Line Charts**: Performance trends
- **Bar Charts**: Department/Year comparison
- **Radar Charts**: Category performance
- Custom tooltips and legends

## 🔐 Security Notes

**Development Mode Warning**: This frontend uses localStorage/sessionStorage for demo purposes. For production:
1. Implement proper JWT authentication
2. Secure password handling
3. HTTPS enforcement
4. CSRF token implementation
5. Input validation and sanitization
6. Rate limiting on API calls

## 🐛 Troubleshooting

### Login Not Working
- Clear browser cache/cookies
- Check demo credentials above
- Ensure JavaScript is enabled
- Check browser console for errors

### Charts Not Displaying
- Ensure Chart.js is loaded
- Check browser console for errors
- Verify canvas elements exist

### Sidebar Not Toggling
- Check sidebar active class in CSS
- Verify JavaScript event listeners are attached
- Check mobile viewport

## 📱 Mobile Optimization

The frontend is fully responsive:
- Sidebar becomes collapsible on tablets
- Grid layouts adapt to screen size
- Touch-friendly button sizes
- Optimized form inputs for mobile
- Hamburger menu for navigation

## 📚 Additional Features

### Toast Notifications
```javascript
dashboard.showToast('Success message', 'success');
dashboard.showToast('Error message', 'error');
```

### Modal Management
```javascript
dashboard.openModal('modalId');
dashboard.closeModal('modalId');
```

### Chart Initialization
Charts auto-initialize on dashboard load using Chart.js library.

## 🎓 Learning Resources

- [Chart.js Documentation](https://www.chartjs.org/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [CSS Variables Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)

## 📝 License

This project is part of the Student KPI Management System. Follow the project's license terms.

## 🤝 Contributing

For improvements or bug fixes:
1. Test thoroughly in all roles
2. Ensure responsive design
3. Maintain code style and naming conventions
4. Add comments for complex logic

## 📞 Support

For issues or questions, refer to the main project README.

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: Production Ready ✅
