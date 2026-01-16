<template>
  <div class="schedule-forms-container">
    <div class="grid-layout">
      
      <div class="card">
        <div class="card-header">
          <div class="icon-circle manual">👤</div>
          <div>
            <h3>Manual Assignment</h3>
            <p>Assign a specific staff member to a date.</p>
          </div>
        </div>

        <form @submit.prevent="addSchedule" class="form-body">
          <div class="form-group">
            <label>Staff Member</label>
            <div class="searchable-container">
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Type name or position..." 
                class="search-input"
                @focus="showDropdown = true"
                @blur="hideDropdown" 
              />
              <ul v-if="showDropdown && filteredStaff.length" class="dropdown-list">
                <li 
                  v-for="staff in filteredStaff" 
                  :key="staff.id"
                  @mousedown="selectStaff(staff)"
                >
                  <span class="staff-name">{{ staff.name }}</span>
                  <span class="staff-pos">{{ staff.position }}</span>
                </li>
              </ul>
              <ul v-else-if="showDropdown && searchQuery" class="dropdown-list">
                <li class="no-results">No matches found for "{{ searchQuery }}"</li>
              </ul>
            </div>
          </div>

          <div class="form-group">
            <label>Duty Date</label>
            <input v-model="duty_date" type="date" required />
          </div>

          <div v-if="errorMessage" class="error-box">
            {{ errorMessage }}
          </div>

          <button type="submit" class="btn-primary full-width" :disabled="!staff_id">
            Confirm Assignment
          </button>
        </form>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="icon-circle auto">⚡</div>
          <div>
            <h3>Auto-Generator</h3>
            <p>Automatically fill the roster for a date range.</p>
          </div>
        </div>

        <form @submit.prevent="autoSchedule" class="form-body">
          <div class="form-row">
            <div class="form-group">
              <label>Start Date</label>
              <input v-model="start_date" type="date" required />
            </div>
            <div class="form-group">
              <label>End Date</label>
              <input v-model="end_date" type="date" required />
            </div>
          </div>

          <div class="info-box">
            <p>* The system will distribute duties evenly among all active staff.</p>
          </div>

          <button type="submit" class="btn-auto full-width">
            Generate Schedule
          </button>
        </form>
      </div>

    </div>
  </div>
</template>

<script>
import api from "../api/axios";

export default {
  data() {
    return {
      // Manual Assignment Data
      staff_id: "",
      duty_date: "",
      searchQuery: "",
      showDropdown: false,
      
      // Auto-Generator Data
      start_date: "",
      end_date: "",
      
      // Loaded Data
      staffList: [],
      errorMessage: "",
    };
  },
  computed: {
    // Filters staff based on name OR position
    filteredStaff() {
      const query = this.searchQuery.toLowerCase();
      if (!query) return this.staffList;
      return this.staffList.filter(staff => 
        staff.name.toLowerCase().includes(query) ||
        staff.position.toLowerCase().includes(query)
      );
    }
  },
  async mounted() {
    await this.loadStaff();
  },
  methods: {
    async addSchedule() {
      if (!this.staff_id || !this.duty_date) return;
      
      // Clear previous errors
      this.errorMessage = "";

      try {
        await api.post("/schedule/", {
          staff_id: this.staff_id,
          duty_date: this.duty_date,
        });
        
        // Reset Form on Success
        this.staff_id = "";
        this.searchQuery = "";
        this.duty_date = "";
        this.$emit("refresh-schedule"); 
        
      } catch (err) {
        // Check if the backend sent a 400 error with a detail message
        if (err.response && err.response.data && err.response.data.detail) {
          this.errorMessage = err.response.data.detail;
        } else {
          this.errorMessage = "A server error occurred. Please try again.";
        }
        
        // Optional: Auto-hide error after 5 seconds
        setTimeout(() => { this.errorMessage = ""; }, 5000);
      }
    },
    async loadStaff() {
      try {
        const res = await api.get("/staff/");
        this.staffList = res.data;
      } catch (err) {
        console.error("Failed to load staff:", err);
      }
    },
    selectStaff(staff) {
      this.staff_id = staff.id;
      this.searchQuery = staff.name; // Display name in input
      this.showDropdown = false;
    },
    hideDropdown() {
      // Timeout allows the 'mousedown' event on list items to fire before the list disappears
      setTimeout(() => {
        this.showDropdown = false;
      }, 200);
    },
    async autoSchedule() {
      if (!this.start_date || !this.end_date) return;
      try {
        await api.post("/schedule/auto", {
          start_date: this.start_date,
          end_date: this.end_date,
        });
        
        // Reset Form
        this.start_date = "";
        this.end_date = "";
        
        this.$emit("refresh-schedule");
      } catch (err) {
        console.error("Auto-schedule failed:", err);
      }
    },
  },
};
</script>

<style scoped>
.grid-layout {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.card {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.card-header {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.icon-circle {
  width: 45px;
  height: 45px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.manual { background: #eff6ff; color: #2563eb; }
.auto { background: #fdf2f8; color: #db2777; }

.card-header h3 { margin: 0; font-size: 1.1rem; color: #1e293b; }
.card-header p { margin: 2px 0 0; font-size: 0.85rem; color: #64748b; }

.form-body { padding: 1.5rem; }

.form-group { 
  margin-bottom: 1.25rem; 
  position: relative; /* Needed for absolute dropdown */
}

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem; }

label {
  display: block;
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Searchable Dropdown Styles */
.dropdown-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 50;
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  margin-top: 4px;
  max-height: 200px;
  overflow-y: auto;
  list-style: none;
  padding: 0;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.dropdown-list li {
  padding: 10px 15px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f1f5f9;
}

.dropdown-list li:hover {
  background: #f8fafc;
}

.staff-name { font-weight: 500; color: #1e293b; }
.staff-pos { font-size: 0.75rem; color: #64748b; background: #f1f5f9; padding: 2px 6px; border-radius: 4px; }

.no-results {
  padding: 15px;
  text-align: center;
  color: #94a3b8;
  font-size: 0.85rem;
}

.info-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.info-box p { font-size: 0.75rem; color: #64748b; margin: 0; }

/* Buttons */
button {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-primary { background: #2563eb; color: white; }
.btn-auto { background: #1e293b; color: white; }

button:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
button:disabled { background: #cbd5e1; cursor: not-allowed; }
.error-box {
  background: #fef2f2;
  border: 1px solid #fee2e2;
  color: #dc2626;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 0.85rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  animation: shake 0.4s ease-in-out;
}

/* Optional: Shake animation to draw attention */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
</style>