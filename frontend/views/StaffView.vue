<template>
  <div class="staff-management">
    <div class="page-header">
      <div class="header-info">
        <h1>Staff Management</h1>
        <p>Overview and administration of your organization's team.</p>
      </div>
    </div>

    <div class="tabs-container">
      <div class="tabs-list">
        <button 
          :class="['tab-btn', { active: activeTab === 'list' }]" 
          @click="activeTab = 'list'"
        >
         Staff Directory
        </button>
        <button 
          :class="['tab-btn', { active: activeTab === 'add' }]" 
          @click="activeTab = 'add'"
        >
         Add New Staff
        </button>
      </div>

      <div class="tab-content">
        <transition name="fade" mode="out-in">
          <div v-if="activeTab === 'list'" key="list">
            <StaffList ref="staffListComponent" />
          </div>

          <div v-else-if="activeTab === 'add'" key="add">
            <StaffForm @staff-added="onStaffAdded" />
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import StaffForm from "../components/StaffForm.vue";
import StaffList from "../components/StaffList.vue";

export default {
  components: { StaffForm, StaffList },
  data() {
    return {
      activeTab: 'list' // Default tab
    };
  },
  methods: {
    onStaffAdded() {
      // Switch to list tab to see the new addition
      this.activeTab = 'list';
      // Wait for the next tick to ensure the list component is rendered before calling its method
      this.$nextTick(() => {
        if (this.$refs.staffListComponent) {
          this.$refs.staffListComponent.fetchStaff();
        }
      });
    },
  },
};
</script>

<style scoped>
.staff-management {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 1.75rem;
  color: #1e293b;
  margin: 0;
}

.page-header p {
  color: #64748b;
  margin-top: 5px;
}

/* Tabs Styling */
.tabs-list {
  display: flex;
  gap: 10px;
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 1.5rem;
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: none;
  font-size: 0.95rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px; /* Alignment with border-bottom */
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-btn:hover {
  color: #2563eb;
}

.tab-btn.active {
  color: #2563eb;
  border-bottom: 2px solid #2563eb;
}

.tab-content {
  margin-top: 1rem;
}

/* Smooth Transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.icon {
  font-size: 1.1rem;
}
</style>