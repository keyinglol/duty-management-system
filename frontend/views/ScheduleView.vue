<template>
  <div class="schedule-page">
    <div class="calendar-container" :class="{ 'blur-bg': showDrawer }">
      <div class="header-actions">
        <div>
          <h1>Duty Schedule</h1>
          <p>View and manage monthly staff rotations.</p>
        </div>
        <button @click="showDrawer = true" class="btn-primary">
          Assign Duty
        </button>
      </div>

      <ScheduleList ref="scheduleList" />
    </div>

    <div v-if="showDrawer" class="drawer-overlay" @click="showDrawer = false"></div>

    <transition name="slide">
      <div v-if="showDrawer" class="drawer">
        <div class="drawer-header">
          <h3>Schedule Management</h3>
          <button @click="showDrawer = false" class="btn-close">&times;</button>
        </div>
        
        <div class="drawer-body">
          <ScheduleForm @refresh-schedule="handleRefresh" />
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import ScheduleForm from "../components/ScheduleForm.vue";
import ScheduleList from "../components/ScheduleList.vue";

export default {
  components: { ScheduleForm, ScheduleList },
  data() {
    return {
      showDrawer: false
    };
  },
  methods: {
  async handleRefresh() {
    this.showDrawer = false; 
    await this.$refs.scheduleList.loadSchedules();
    this.$refs.scheduleList.buildScheduleMap();
  }
}
};
</script>

<style scoped>
.schedule-page {
  position: relative;
  overflow: hidden;
  min-height: calc(100vh - 100px);
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.blur-bg {
  filter: blur(2px);
  pointer-events: none;
  transition: all 0.3s;
}

/* Drawer Overlay (Darkens background) */
.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(2px);
  z-index: 100;
}

/* The Drawer Container */
.drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: 450px;
  height: 100%;
  background: white;
  box-shadow: -10px 0 30px rgba(0, 0, 0, 0.1);
  z-index: 101;
  display: flex;
  flex-direction: column;
}

.drawer-header {
  padding: 20px 30px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #64748b;
  cursor: pointer;
}

.drawer-body {
  padding: 30px;
  overflow-y: auto;
}

/* Slide Animation */
.slide-enter-active, .slide-leave-active {
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-enter, .slide-leave-to {
  transform: translateX(100%);
}

.btn-primary {
  background: #2563eb;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>