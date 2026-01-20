<!-- <template>
  <div class="schedule-container">
    <div class="card">
      <div class="card-header">
        <div class="header-info">
          <h3>Monthly Duty Roster</h3>
          <p>Full overview of staff assignments for the month.</p>
        </div>
        
        <div class="month-nav">
          <button @click="changeMonth(-1)" class="btn-icon">←</button>
          <div class="current-month">
            {{ currentMonthName }} {{ currentYear }}
          </div>
          <button @click="changeMonth(1)" class="btn-icon">→</button>
          <button @click="setToday" class="btn-today">Today</button>
        </div>
      </div>

      <div class="calendar-days-header">
        <div v-for="day in weekDays" :key="day" class="weekday-label">{{ day }}</div>
      </div>

      <div class="calendar-grid">
        <div 
          v-for="{ date, isCurrentMonth, dateString } in calendarDays" 
          :key="dateString" 
          :class="[
            'day-cell', 
            { 'not-current': !isCurrentMonth },
            { 'is-today': isToday(dateString) }
          ]"
        >
          <div class="day-number">{{ date.getDate() }}</div>

          <div class="day-content">
            <div v-if="scheduleMap[dateString]" class="staff-list">
              <div 
                v-for="s in scheduleMap[dateString].slice(0, 3)" 
                :key="s.id" 
                class="staff-dot"
                :title="s.staff_name + ' (' + s.position + ')'"
              >
                <span class="dot"></span>
                <span class="name-truncate">{{ s.staff_name }}</span>
              </div>
              <div v-if="scheduleMap[dateString].length > 3" class="more-count">
                +{{ scheduleMap[dateString].length - 3 }} more
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

   <div class="schedule-container">
    <div class="card">
      <div class="calendar-grid">
        <div 
          v-for="{ date, isCurrentMonth, dateString } in calendarDays" 
          :key="dateString" 
          @click="openDayDetail(dateString)"
          :class="['day-cell', { 'not-current': !isCurrentMonth }, { 'is-today': isToday(dateString) }]"
          style="cursor: pointer;"
        >
          <div class="day-number">{{ date.getDate() }}</div>
          </div>
      </div>
    </div>

    <div v-if="selectedDate" class="modal-overlay" @click.self="selectedDate = null">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Duty for {{ formatDateHeader(selectedDate) }}</h3>
          <button @click="selectedDate = null" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <div v-if="currentDayStaff.length > 0" class="modal-staff-list">
            <div v-for="staff in currentDayStaff" :key="staff.id" class="modal-staff-item">
              <div class="staff-info">
                <strong>{{ staff.staff_name }}</strong>
                <span>{{ staff.position }}</span>
              </div>
              <div class="staff-actions">
                <button @click="deleteEntry(staff.id)" class="btn-delete">Remove</button>
              </div>
            </div>
          </div>
          <p v-else class="empty-msg">No staff assigned for this day.</p>
        </div>
        
        <div class="modal-footer">
          <button @click="selectedDate = null" class="btn-secondary">Close</button>
        </div>
      </div>
    </div>
  </div>
</template> -->

<template>
  <div class="schedule-container">
    <div class="card">
      <div class="card-header">
        <div class="header-info">
          <h3>Monthly Duty Roster</h3>
          <p>Full overview of staff assignments for the month.</p>
        </div>
        
        <div class="month-nav">
          <button @click="changeMonth(-1)" class="btn-icon">←</button>
          <div class="current-month">
            {{ currentMonthName }} {{ currentYear }}
          </div>
          <button @click="changeMonth(1)" class="btn-icon">→</button>
          <button @click="setToday" class="btn-today">Today</button>
        </div>
      </div>

      <div class="calendar-days-header">
        <div v-for="day in weekDays" :key="day" class="weekday-label">{{ day }}</div>
      </div>

      <div class="calendar-grid">
        <div 
          v-for="{ date, isCurrentMonth, dateString } in calendarDays" 
          :key="dateString" 
          @click="openDayDetail(dateString)" 
          :class="[
            'day-cell', 
            { 'not-current': !isCurrentMonth },
            { 'is-today': isToday(dateString) }
          ]"
          style="cursor: pointer;"
        >
          <div class="day-number">{{ date.getDate() }}</div>

          <div class="day-content">
            <div v-if="scheduleMap[dateString]" class="staff-list">
              <div 
                v-for="s in scheduleMap[dateString].slice(0, 3)" 
                :key="s.id" 
                class="staff-dot"
                :title="s.staff_name + ' (' + s.position + ')'"
              >
                <span class="dot"></span>
                <span class="name-truncate">{{ s.staff_name }}</span>
              </div>
              <div v-if="scheduleMap[dateString].length > 3" class="more-count">
                +{{ scheduleMap[dateString].length - 3 }} more
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedDate" class="modal-overlay" @click.self="selectedDate = null">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Duty for {{ formatDateHeader(selectedDate) }}</h3>
          <button @click="selectedDate = null" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <div v-if="currentDayStaff.length > 0" class="modal-staff-list">
            <div v-for="staff in currentDayStaff" :key="staff.id" class="modal-staff-item">
              <div class="staff-info">
                <strong>{{ staff.staff_name }}</strong>
                <span>{{ staff.position }}</span>
              </div>
              <div class="staff-actions">
                <button @click.stop="deleteEntry(staff.id)" class="btn-delete">Remove</button>
              </div>
            </div>
          </div>
          <p v-else class="empty-msg">No staff assigned for this day.</p>
        </div>
        
        <div class="modal-footer">
          <button @click="selectedDate = null" class="btn-secondary">Close</button>
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
      schedules: [],
      viewDate: new Date(), // The date used to determine which month to show
      weekDays: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      scheduleMap: {},
      selectedDate: null,
    };
  },
  computed: {
    currentDayStaff() {
      return this.scheduleMap[this.selectedDate] || [];
    },
    currentMonthName() {
      return this.viewDate.toLocaleString('default', { month: 'long' });
    },
    currentYear() {
      return this.viewDate.getFullYear();
    },
    calendarDays() {
      const year = this.viewDate.getFullYear();
      const month = this.viewDate.getMonth();
      const firstDay = new Date(year, month, 1);
      
      // Adjust to start from Monday
      let startOffset = firstDay.getDay() - 1;
      if (startOffset === -1) startOffset = 6; 
      
      const days = [];
      const startDate = new Date(firstDay);
      startDate.setDate(firstDay.getDate() - startOffset);
      
      for (let i = 0; i < 42; i++) {
        const d = new Date(startDate);
        d.setDate(startDate.getDate() + i);
        
        // FIX: Generate the string using Local Time instead of ISOString
        const y = d.getFullYear();
        const m = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const localDateString = `${y}-${m}-${day}`;
        
        days.push({
          date: d,
          isCurrentMonth: d.getMonth() === month,
          dateString: localDateString // This now matches "2026-01-16" in your local zone
          });
        }
        return days;
      },
    },
  async mounted() {
    await this.loadSchedules();
    this.buildScheduleMap();
  },
  methods: {
    openDayDetail(dateString) {
      this.selectedDate = dateString;
    },

    formatDateHeader(dateStr) {
      return new Date(dateStr).toLocaleDateString('default', { 
        weekday: 'long', 
        month: 'long', 
        day: 'numeric' 
      });
    },

    async deleteEntry(scheduleId) {
      if (!confirm("Are you sure you want to remove this staff from duty?")) return;

      try {
        await api.delete(`/schedule/${scheduleId}/`);
        // Refresh data
        await this.loadSchedules();
        this.buildScheduleMap();
        
        // If no more staff on this day, you might want to close the modal
        if (this.currentDayStaff.length === 0) {
          // Optional: this.selectedDate = null;
        }
      } catch (e) {
        alert("Failed to delete entry");
        console.error(e);
      }
    },
    async loadSchedules() {
      try {
        const res = await api.get("/schedule/");
        this.schedules = res.data || [];
      } catch (e) {
        console.error("Failed to fetch schedules:", e);
      }
    },
    buildScheduleMap() {
  const map = {};
  this.schedules.forEach(s => {
    // Ensure we take only the YYYY-MM-DD part if the backend sends a full timestamp
    const dateKey = s.duty_date.split('T')[0]; 
    if (!map[dateKey]) map[dateKey] = [];
    map[dateKey].push({
      id: s.id,
      staff_name: s.staff.name,
      position: s.staff.position
    });
  });
  this.scheduleMap = map;
},
    changeMonth(step) {
      this.viewDate = new Date(this.viewDate.setMonth(this.viewDate.getMonth() + step));
    },
    setToday() {
      this.viewDate = new Date();
    },
    // isToday(dateStr) {
    //   return dateStr === new Date().toISOString().split('T')[0];
    // }
    isToday(dateStr) {
  const localToday = new Date();
  const year = localToday.getFullYear();
  const month = String(localToday.getMonth() + 1).padStart(2, '0');
  const day = String(localToday.getDate()).padStart(2, '0');
  
  const todayStr = `${year}-${month}-${day}`;
  return dateStr === todayStr;
}
  }
};
</script>

<style scoped>
.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f1f5f9;
}

.month-nav {
  display: flex;
  align-items: center;
  gap: 12px;
}

.current-month {
  font-size: 1.1rem;
  font-weight: 700;
  min-width: 180px;
  text-align: center;
  color: #1e293b;
}

.btn-icon {
  background: #fff;
  border: 1px solid #e2e8f0;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover { background: #f8fafc; border-color: #cbd5e1; }

.btn-today {
  padding: 6px 16px;
  background: #eff6ff;
  color: #2563eb;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

/* Calendar Grid */
.calendar-days-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.weekday-label {
  padding: 10px;
  text-align: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-auto-rows: minmax(100px, 1fr);
  background: #e2e8f0;
  gap: 1px;
}

.day-cell {
  background: #fff;
  padding: 8px;
  transition: background 0.2s;
  display: flex;
  flex-direction: column;
}

.day-cell.not-current {
  background: #fcfdfe;
}

.day-cell.not-current .day-number {
  color: #cbd5e1;
}

.day-number {
  font-weight: 600;
  font-size: 0.9rem;
  color: #475569;
  margin-bottom: 4px;
}

.is-today {
  background: #f0f7ff !important;
}

.is-today .day-number {
  color: #2563eb;
  background: #dbeafe;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

/* Staff Entries inside cells */
.staff-list {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.staff-dot {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.7rem;
  color: #334155;
}

.dot {
  width: 6px;
  height: 6px;
  background: #2563eb;
  border-radius: 50%;
}

.name-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.more-count {
  font-size: 0.65rem;
  color: #94a3b8;
  padding-left: 4px;
  font-weight: 600;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 24px;
  border-radius: 12px;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
}

.modal-staff-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.staff-info {
  display: flex;
  flex-direction: column;
}

.staff-info span {
  font-size: 0.8rem;
  color: #64748b;
}

.btn-delete {
  background: #fee2e2;
  color: #ef4444;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-delete:hover {
  background: #fecaca;
}

.btn-secondary {
  width: 100%;
  padding: 10px;
  background: #f1f5f9;
  border: none;
  border-radius: 8px;
  margin-top: 15px;
  cursor: pointer;
}
</style>