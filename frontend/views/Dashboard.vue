<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="title-area">
        <h1>System Overview</h1>
        <p class="text-muted">{{ todayDate }}</p>
      </div>
      <!-- <div class="header-actions">
        <button class="btn-outline" @click="exportReport">Export Monthly Report</button>
        
      </div> -->
      <div class="header-actions">
        <button class="btn-primary" @click="exportReport">
            Export Monthly Report
        </button>
    </div>
</header>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-info">
          <span class="label">Total Workforce</span>
          <span class="value">{{ stats.total_staff }}</span>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-info">
          <span class="label">Today's Assignments</span>
          <span class="value">{{ stats.today_shifts_count }}</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-info">
          <span class="label">Unfilled Shift Gaps</span>
          <span class="value" :class="{ 'text-danger': stats.unfilled_gaps > 0 }">
            {{ stats.unfilled_gaps }}
          </span>
        </div>
      </div>
    </div>

    <div class="dashboard-grid">
      <div class="left-column">
        <div class="card mb-4">
          <div class="card-header border-bottom">
            <h3>Personnel Utilization</h3>
            <span class="subtitle">Ranking by shift frequency</span>
          </div>
          <div class="workload-list">
            <div v-for="(item, index) in stats.ranked_staff" :key="item.id" class="workload-row">
              <span class="rank-index">{{ index + 1 }}</span>
              <div class="staff-meta">
                <span class="staff-name">{{ item.name }}</span>
                <span class="staff-position">{{ item.position }}</span>
              </div>
              <div class="bar-container">
                <div class="progress-track">
                  <div class="progress-fill" :style="{ width: (item.count / maxShifts) * 100 + '%' }"></div>
                </div>
                <span class="count-value">{{ item.count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="right-column">
        <div class="card mb-4">
          <div class="card-header border-bottom">
            <h3>Today's Roster</h3>
          </div>
          <div class="today-list">
            <div v-for="s in todayShifts" :key="s.id" class="roster-item">
              <div class="roster-info">
                <strong>{{ s.staff.name }}</strong>
                <span>{{ s.staff.position }}</span>
              </div>
            </div>
            <div v-if="todayShifts.length === 0" class="empty-state">No scheduled activity</div>
          </div>
        </div>

        <div class="card">
          <div class="card-header border-bottom">
            <h3>Quick Actions</h3>
          </div>
          <div class="action-list">
            <button @click="$router.push('/staff')" class="nav-btn">Manage Personnel</button>
            <button @click="$router.push('/schedule')" class="nav-btn">Access Roster</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api/axios";

export default {
  data() {
    return {
      // Initialize stats with empty values to avoid template errors before loading
      stats: {
        total_staff: 0,
        today_shifts_count: 0,
        unfilled_gaps: 0,
        ranked_staff: []
      },
      todayShifts: [],
      todayDate: new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric' })
    };
  },
  computed: {
    // We still calculate maxShifts locally to ensure the bar graph is relative
    maxShifts() {
      if (!this.stats.ranked_staff || this.stats.ranked_staff.length === 0) return 1;
      return Math.max(...this.stats.ranked_staff.map(s => s.count), 1);
    }
  },
  async mounted() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      const today = new Date().toLocaleDateString('en-CA'); // YYYY-MM-DD
      try {
        // Fetch from the new statistics API and the existing schedule API
        const [statsRes, scheduleRes] = await Promise.all([
          api.get("/statistics/summary"),
          api.get("/schedule/")
        ]);
        
        this.stats = statsRes.data;
        
        // Still filter today's shifts locally to show the names in the right column
        // (Or create an endpoint like /schedule/today if todayShifts is very large)
        this.todayShifts = scheduleRes.data.filter(s => s.duty_date === today);
        
      } catch (e) {
        console.error("Error loading dashboard data:", e);
      }
    },
    exportReport() {
      // Points to your FastAPI export endpoint
      window.open("http://localhost:8000/schedule/export", "_blank");
    }
  }
};
</script>

<style scoped>
/* (All your existing CSS stays the same) */
.dashboard { color: #334155; }
.text-muted { color: #64748b; font-size: 0.9rem; }
.text-danger { color: #ef4444 !important; }
.dashboard-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem; }
.btn-primary {
  background: #0f172a; /* Deep slate professional color */
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.btn-primary:hover {
  background: #1e293b;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-primary span {
  font-size: 1.1rem;
}
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 2rem; }
.stat-card { background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #e2e8f0; }
.label { display: block; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8; margin-bottom: 0.5rem; }
.value { font-size: 1.75rem; font-weight: 600; color: #0f172a; }
.dashboard-grid { display: grid; grid-template-columns: 1.6fr 1fr; gap: 1.5rem; }
.card { background: white; border-radius: 8px; border: 1px solid #e2e8f0; overflow: hidden; }
.card-header { padding: 1.25rem 1.5rem; }
.border-bottom { border-bottom: 1px solid #f1f5f9; }
.card-header h3 { font-size: 1rem; margin: 0; font-weight: 600; }
.mb-4 { margin-bottom: 1.5rem; }
.workload-list { padding: 0.5rem 1.5rem; }
.workload-row { display: flex; align-items: center; padding: 1rem 0; border-bottom: 1px solid #f8fafc; gap: 1.25rem; }
.rank-index { color: #cbd5e1; font-weight: 700; width: 20px; }
.staff-meta { width: 150px; }
.staff-name { display: block; font-size: 0.9rem; font-weight: 500; }
.staff-position { font-size: 0.75rem; color: #94a3b8; }
.bar-container { flex-grow: 1; display: flex; align-items: center; gap: 1rem; }
.progress-track { flex-grow: 1; height: 6px; background: #f1f5f9; border-radius: 3px; }
.progress-fill { height: 100%; background: #475569; border-radius: 3px; transition: width 0.5s ease; }
.count-value { font-size: 0.85rem; font-weight: 600; min-width: 30px; text-align: right; }
.today-list { padding: 0.5rem 1.5rem; }
.roster-item { display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid #f8fafc; }
.roster-info strong { display: block; font-size: 0.85rem; }
.roster-info span { font-size: 0.75rem; color: #94a3b8; }
.badge-status { font-size: 0.65rem; font-weight: 700; background: #f0fdf4; color: #166534; padding: 2px 8px; border-radius: 4px; }
.action-list { padding: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem; }
.nav-btn { text-align: left; padding: 10px 12px; border: 1px solid #e2e8f0; background: white; border-radius: 6px; cursor: pointer; font-size: 0.9rem; font-weight: 500; }
.nav-btn:hover { border-color: #94a3b8; background: #f8fafc; }
.empty-state { padding: 1rem; text-align: center; color: #94a3b8; font-size: 0.9rem; }
</style>