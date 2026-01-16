<template>
  <div class="form-container">
    <div class="card">
      <div class="card-header">
        <h3>Add New Staff Member</h3>
        <p>Fill in the details below to register a new employee.</p>
      </div>

      <form @submit.prevent="addStaff" class="staff-form">
        <div class="form-group">
          <label>Full Name</label>
          <input 
            v-model="name" 
            placeholder="e.g. John Doe" 
            required 
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Age</label>
            <input 
              v-model="age" 
              type="number" 
              placeholder="0" 
              required 
            />
          </div>

          <!-- <div class="form-group">
            <label>Position</label>
            <input 
              v-model="position" 
              placeholder="e.g. Manager" 
              required 
            />
          </div> -->

          <div class="form-group">
            <label>Position</label>
            <select v-model="position" required class="form-select">
              <option value="" disabled selected>Select a position</option>
              <option value="Manager">Manager</option>
              <option value="Senior">Senior</option>
              <option value="Junior">Junior</option>
            </select>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn-secondary" @click="resetForm">Clear</button>
          <button type="submit" class="btn-primary">Add Staff Member</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from "../api/axios";

export default {
  data() {
    return { name: "", age: "", position: "" };
  },
  methods: {
    async addStaff() {
      try {
        await api.post("/staff/", {
          name: this.name,
          age: this.age,
          position: this.position,
        });
        this.resetForm();
        this.$emit("staff-added");
        // Optional: Add a notification toast here
      } catch (error) {
        console.error("Error adding staff:", error);
      }
    },
    resetForm() {
      this.name = "";
      this.age = "";
      this.position = "";
    }
  },
};
</script>

<style scoped>
/* Professional Card Styling */
.card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid #e2e8f0;
}

.card-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.card-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
}

.card-header p {
  margin: 5px 0 0;
  color: #64748b;
  font-size: 0.9rem;
}

/* Form Layout */
.staff-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 1.5rem;
}

label {
  font-weight: 600;
  font-size: 0.85rem;
  color: #334155;
  margin-bottom: 0.5rem;
}


/* Shared Styling for Inputs and Selects */
input, 
select {
  padding: 10px 14px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  color: #334155;
  background-color: #ffffff;
  width: 100%; /* Ensures they fill the container equally */
  box-sizing: border-box; /* Prevents padding from adding to width */
}

/* Specific Select Styling to match Input height exactly */
select {
  height: 42px; /* Matches the typical height of your padded inputs */
  cursor: pointer;
  appearance: none; /* Removes the default ugly arrow */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2364748b'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  padding-right: 40px; /* Space for the custom arrow */
}

input:focus,
select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Buttons */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

button {
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background-color: #2563eb;
  color: white;
}

.btn-primary:hover {
  background-color: #1d4ed8;
}

.btn-secondary {
  background-color: #f1f5f9;
  color: #475569;
}

.btn-secondary:hover {
  background-color: #e2e8f0;
}
</style>