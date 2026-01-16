<template>
  <div class="list-container">
    
    <div class="card">
      <div class="card-header">
        <div class="header-text">
          <h3>Staff Directory</h3>
          <p>Manage your current employees and their roles.</p>
        </div>
        <div class="header-actions">
          <span class="count-badge">{{ staffList.length }} Staff Members</span>
        </div>
      </div>

      <div class="filter-bar">
  <input 
    v-model="searchQuery" 
    type="text" 
    placeholder="Search by name..." 
    class="filter-input"
  />
  <select v-model="selectedPosition" class="filter-select">
    <option value="">All Positions</option>
    <option v-for="pos in positions" :key="pos" :value="pos">{{ pos }}</option>
  </select>
</div>

      <div class="table-responsive">
        <table class="staff-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Age</th>
              <th>Position</th>
              <th class="text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <!-- <tr v-for="staff in staffList" :key="staff.id"> -->
            <tr v-for="staff in filteredStaff" :key="staff.id">
              <td class="font-bold">{{ staff.name }}</td>
              <td>{{ staff.age }}</td>
              <td>
                <span class="role-badge">{{ staff.position }}</span>
              </td>
              <td class="text-right">
                <button @click="deleteStaff(staff.id)" class="btn-delete" title="Remove Staff">
                  <span class="icon">🗑️</span> Delete
                </button>
              </td>
            </tr>
            <tr v-if="staffList.length === 0">
              <td colspan="4" class="empty-state">
                No staff members found. Add one to get started.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../api/axios";

export default {
  data() {
    return { 
      staffList: [],
      searchQuery: "",      
      selectedPosition: "", 
    };
  },
  computed: {
    // This extracts all unique positions from your staff list for the dropdown
    positions() {
      const allPos = this.staffList.map(s => s.position);
      return [...new Set(allPos)];
    },
    // This is the list the table actually displays
    filteredStaff() {
      return this.staffList.filter(staff => {
        const matchesName = staff.name.toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesPos = this.selectedPosition === "" || staff.position === this.selectedPosition;
        return matchesName && matchesPos;
      });
    }
  },
  methods: {
    async fetchStaff() {
      try {
        const res = await api.get("/staff/");
        this.staffList = res.data;
      } catch (error) {
        console.error("Error fetching staff:", error);
      }
    },
    async deleteStaff(id) {
      if (confirm("Are you sure you want to remove this staff member?")) {
        try {
          await api.delete(`/staff/${id}/`);
          this.fetchStaff();
        } catch (error) {
          console.error("Error deleting staff:", error);
        }
      }
    },
  },
  mounted() {
    this.fetchStaff();
  },
};
</script>

<style scoped>
.card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  overflow: hidden; /* Ensures table corners match card */
}

.card-header {
  padding: 1.5rem 2rem;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
}

.card-header p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 0.85rem;
}

.count-badge {
  background: #eff6ff;
  color: #2563eb;
  padding: 4px 12px;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid #dbeafe;
}

/* Table Styling */
.table-responsive {
  width: 100%;
  overflow-x: auto;
}

.staff-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.staff-table th {
  background: #f8fafc;
  padding: 12px 20px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  border-bottom: 1px solid #e2e8f0;
}

.staff-table td {
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
  color: #334155;
  font-size: 0.95rem;
}

.staff-table tr:hover {
  background-color: #f8fafc;
}

.font-bold {
  font-weight: 600;
  color: #1e293b;
}

/* Role Badge */
.role-badge {
  background: #f1f5f9;
  color: #475569;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
}

/* Delete Button */
.btn-delete {
  background: transparent;
  color: #ef4444;
  border: 1px solid #fecaca;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-delete:hover {
  background: #fef2f2;
  border-color: #ef4444;
}

.text-right {
  text-align: right;
}

.empty-state {
  text-align: center;
  padding: 3rem !important;
  color: #94a3b8;
  font-style: italic;
}
.filter-bar {
  padding: 1rem 2rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  gap: 1rem;
}

.filter-input {
  flex-grow: 1;
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: white;
  min-width: 150px;
}

.filter-input:focus, .filter-select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}
</style>