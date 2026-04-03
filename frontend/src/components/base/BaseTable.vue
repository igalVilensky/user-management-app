<script setup>
import BaseSkeleton from './BaseSkeleton.vue';

const props = defineProps({
  columns: {
    type: Array,
    required: true
  },
  data: {
    type: Array,
    required: true
  },
  loading: Boolean,
  emptyText: {
    type: String,
    default: 'No users found in the system.'
  },
  ariaLabel: {
    type: String,
    default: 'Data table'
  },
  sortBy: {
    type: String,
    default: null
  },
  sortOrder: {
    type: String,
    default: 'asc'
  }
});

const emit = defineEmits(['sort']);

function handleSort(col) {
  if (col.sortable) {
    emit('sort', col.key);
  }
}
</script>

<template>
  <div class="base-table-container">
    <table class="base-table" :aria-label="ariaLabel">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" :style="{ width: col.width }" scope="col"
            :class="{ 'sortable': col.sortable }" @click="handleSort(col)"
            :aria-sort="props.sortBy === col.key ? (props.sortOrder === 'asc' ? 'ascending' : 'descending') : 'none'">
            <div class="th-content">
              {{ col.label }}
              <span v-if="col.sortable" class="sort-indicator">
                <template v-if="props.sortBy === col.key">
                  {{ props.sortOrder === 'asc' ? '↑' : '↓' }}
                </template>
                <template v-else>↕</template>
              </span>
            </div>
          </th>
        </tr>
      </thead>

      <tbody>
        <!-- Loading -->
        <template v-if="loading">
          <tr v-for="i in 5" :key="`skeleton-${i}`" aria-hidden="true">
            <td v-for="col in columns" :key="col.key">
              <BaseSkeleton width="85%" height="1.25rem" />
            </td>
          </tr>
        </template>

        <!-- Data -->
        <template v-else-if="data.length > 0">
          <tr v-for="(row, idx) in data" :key="row.id || idx">
            <td v-for="col in columns" :key="col.key" :data-label="col.label">
              <span class="cell-content">
                <slot :name="`cell(${col.key})`" :row="row" :value="row[col.key]">
                  {{ row[col.key] }}
                </slot>
              </span>
            </td>
          </tr>
        </template>

        <!-- Empty -->
        <tr v-else>
          <td :colspan="columns.length" class="empty-cell">
            <div class="empty-state">
              <p>{{ emptyText }}</p>
              <slot name="empty-cta" />
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.base-table-container {
  width: 100%;
  overflow-x: auto;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: white;
}

.base-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

/* Header */
th {
  padding: 1rem 0.75rem;
  background: var(--hover-bg);
  border-bottom: 2px solid var(--border-color);
  text-align: left;
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
  white-space: nowrap;
}

th.sortable {
  cursor: pointer;
  user-select: none;
}

th.sortable:hover {
  background: var(--border-color);
}

.th-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-indicator {
  color: var(--text-secondary);
  font-size: 0.8em;
}

/* Cells (desktop) */
td {
  padding: 1rem 0.75rem;
  border-bottom: 1px solid var(--border-color);
  font-size: 0.875rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

tr:last-child td {
  border-bottom: none;
}

/* Shared content wrapper */
.cell-content {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Empty */
.empty-cell {
  padding: 3rem 1rem;
  text-align: center;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: var(--text-secondary);
}

/* =========================
   Mobile Card Layout
========================= */
@media (max-width: 640px) {
  .base-table {
    min-width: unset;
  }

  .base-table thead {
    display: none;
  }

  .base-table tr {
    display: block;
    margin-bottom: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 1rem;
    background: white;
  }

  .base-table td {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px dashed var(--border-color);
    overflow: hidden;
  }

  .base-table td:last-child {
    border-bottom: none;
  }

  /* label */
  .base-table td::before {
    content: attr(data-label);
    font-weight: 600;
    color: var(--text-secondary);
    margin-right: 1rem;
    flex: 0 0 auto;
  }

  /* value */
  .cell-content {
    min-width: 0;
    max-width: 60%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    text-align: right;
  }

  .actions-cell {
    justify-content: flex-end;
  }
}
</style>