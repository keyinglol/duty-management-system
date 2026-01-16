
<template>
  <div id="app" class="dashboard-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo-icon">M</div>
        <h2>ManagerPro</h2>
      </div>
      
      <nav class="nav-menu">
        <router-link to="/" class="nav-item" exact-active-class="active">
          Dashboard
        </router-link>
        <router-link to="/staff" class="nav-item">
          Staff Management
        </router-link>
        <router-link to="/schedule" class="nav-item">
          Schedule Management
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <p>© 2026 Admin Dashboard</p>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <h1>Welcome Back, Admin</h1>
        <div class="user-profile">
          <div class="avatar">A</div>
        </div>
      </header>

      <section class="content-view">
        <router-view />
      </section>
    </main>
  </div>
</template>

<script>

export default {
  name: "App",
};
</script>


<style>
/* CSS Reset & Variables */
:root {
  --primary-color: #2563eb;
  --sidebar-bg: #1e293b;
  --bg-light: #f8fafc;
  --text-main: #334155;
  --text-muted: #64748b;
  --white: #ffffff;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background-color: var(--bg-light);
  color: var(--text-main);
}

/* Layout Structure */
.dashboard-container {
  display: flex;
  min-height: 100vh;
}

/* Sidebar Styling */
.sidebar {
  width: 260px;
  background-color: var(--sidebar-bg);
  color: var(--white);
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 10px rgba(0,0,0,0.1);
}

.sidebar-header {
  padding: 2rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  background: var(--primary-color);
  padding: 8px 12px;
  border-radius: 8px;
  font-weight: bold;
}

.sidebar-header h2 {
  font-size: 1.25rem;
  margin: 0;
}

/* Navigation Links */
.nav-menu {
  flex-grow: 1;
  padding: 0 1rem;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 1rem;
  margin-bottom: 8px;
  color: #94a3b8;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: var(--white);
}

.nav-item.router-link-active {
  background: var(--primary-color);
  color: var(--white);
}

.nav-item .icon {
  margin-right: 12px;
}

.sidebar-footer {
  padding: 1.5rem;
  font-size: 0.8rem;
  color: #64748b;
  border-top: 1px solid rgba(255,255,255,0.1);
}

/* Main Content Area */
.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.top-bar {
  background: var(--white);
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.top-bar h1 {
  font-size: 1.1rem;
  font-weight: 600;
}

.avatar {
  width: 35px;
  height: 35px;
  background: #e2e8f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.content-view {
  padding: 2rem;
  overflow-y: auto;
}
</style>