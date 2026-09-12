/**
 * FixFlow - Smart Service Management & Customer Support Platform
 * Frontend SPA Application Logic
 */

const API_BASE = '/api';

// State Store
const state = {
  token: localStorage.getItem('fixflow_token') || null,
  user: JSON.parse(localStorage.getItem('fixflow_user')) || null,
  activeRole: localStorage.getItem('fixflow_role') || 'CUSTOMER',
  tickets: [],
  categories: [],
  technicians: [],
  notifications: [],
  unreadNotifsCount: 0,
  stats: null,
  currentFilterStatus: 'ALL',
  currentFilterPriority: 'ALL',
  searchQuery: ''
};

// Initialization on DOM load
document.addEventListener('DOMContentLoaded', async () => {
  setupEventListeners();
  
  // Quick auto-login if no token present
  if (!state.token || !state.user) {
    await quickLogin('vikas', 'vikas123'); // Default to Vikas (Customer)
  }

  await loadInitialData();
  renderApp();
});

// Setup event handlers
function setupEventListeners() {
  // Demo Role Buttons
  document.querySelectorAll('.demo-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const role = e.target.dataset.role;
      if (role === 'CUSTOMER') await quickLogin('vikas', 'vikas123');
      else if (role === 'TECHNICIAN') await quickLogin('tech', 'tech123');
      else if (role === 'ADMIN') await quickLogin('admin', 'admin123');
      
      document.querySelectorAll('.demo-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      
      await loadInitialData();
      renderApp();
      showToast(`Switched view to ${role} Role`);
    });
  });

  // Search Input
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value.toLowerCase();
      renderTickets();
    });
  }

  // Filter Pills
  document.querySelectorAll('.pill-btn[data-status]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.pill-btn[data-status]').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      state.currentFilterStatus = e.target.dataset.status;
      renderTickets();
    });
  });

  // Notification Bell Toggle
  const notifBtn = document.getElementById('notifBellBtn');
  if (notifBtn) {
    notifBtn.addEventListener('click', () => {
      const dropdown = document.getElementById('notifDropdown');
      dropdown.classList.toggle('show');
    });
  }

  // Close Modals on overlay click
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal(overlay.id);
    });
  });
}

// Quick Login Helper for seamless evaluation & switching
async function quickLogin(username, password) {
  try {
    const res = await fetch(`${API_BASE}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok) {
      state.token = data.access;
      state.user = data.user;
      state.activeRole = data.user.role;
      localStorage.setItem('fixflow_token', data.access);
      localStorage.setItem('fixflow_user', JSON.stringify(data.user));
      localStorage.setItem('fixflow_role', data.user.role);
    }
  } catch (err) {
    console.error("Login failed:", err);
  }
}

// Fetch Initial Data from REST APIs
async function loadInitialData() {
  try {
    const headers = getAuthHeaders();

    // Fetch Tickets
    const ticketsRes = await fetch(`${API_BASE}/tickets/`, { headers });
    if (ticketsRes.ok) state.tickets = await ticketsRes.json();

    // Fetch Service Categories
    const catRes = await fetch(`${API_BASE}/services/`);
    if (catRes.ok) state.categories = await catRes.json();

    // Fetch Notifications
    const notifRes = await fetch(`${API_BASE}/notifications/`, { headers });
    if (notifRes.ok) {
      const notifData = await notifRes.json();
      state.notifications = notifData.notifications || [];
      state.unreadNotifsCount = notifData.unread_count || 0;
    }

    // Fetch Technicians (if Admin)
    if (state.activeRole === 'ADMIN') {
      const techRes = await fetch(`${API_BASE}/auth/technicians/`, { headers });
      if (techRes.ok) state.technicians = await techRes.json();

      const statsRes = await fetch(`${API_BASE}/payments/reports/stats/`, { headers });
      if (statsRes.ok) state.stats = await statsRes.json();
    }
  } catch (err) {
    console.error("Error loading data:", err);
  }
}

// Helper Auth Headers
function getAuthHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': state.token ? `Bearer ${state.token}` : ''
  };
}

// Render Main App UI
function renderApp() {
  renderUserBadge();
  renderNotifications();
  renderKPIs();
  renderRoleSpecificHeader();
  renderTickets();
}

// Render Header User Info
function renderUserBadge() {
  const badgeEl = document.getElementById('userBadgeContainer');
  if (badgeEl && state.user) {
    badgeEl.innerHTML = `
      <div class="user-badge">
        <div class="avatar-sm">${state.user.first_name ? state.user.first_name[0] : 'U'}</div>
        <span class="user-name">${state.user.first_name} ${state.user.last_name || ''}</span>
        <span class="user-role-tag">${state.user.role_display}</span>
      </div>
    `;
  }
}

// Render Notifications Dropdown & Badge
function renderNotifications() {
  const badgeEl = document.getElementById('notifBadge');
  const listEl = document.getElementById('notifList');
  
  if (badgeEl) {
    badgeEl.textContent = state.unreadNotifsCount;
    badgeEl.style.display = state.unreadNotifsCount > 0 ? 'flex' : 'none';
  }

  if (listEl) {
    if (state.notifications.length === 0) {
      listEl.innerHTML = `<div class="notif-item" style="color: var(--text-muted);">No new notifications</div>`;
    } else {
      listEl.innerHTML = state.notifications.map(n => `
        <div class="notif-item ${n.is_read ? '' : 'unread'}">
          <div class="notif-title">${escapeHTML(n.title)}</div>
          <div>${escapeHTML(n.message)}</div>
          <div class="notif-time">${new Date(n.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
        </div>
      `).join('');
    }
  }
}

// Render KPI Cards (for Admin / General view)
function renderKPIs() {
  const kpiContainer = document.getElementById('kpiContainer');
  if (!kpiContainer) return;

  if (state.activeRole === 'ADMIN' && state.stats) {
    kpiContainer.style.display = 'grid';
    kpiContainer.innerHTML = `
      <div class="kpi-card">
        <div class="kpi-icon revenue"><i class="fas fa-indian-rupee-sign"></i></div>
        <div class="kpi-info">
          <h3>₹${state.stats.total_revenue.toLocaleString('en-IN')}</h3>
          <p>Total Revenue</p>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon pending"><i class="fas fa-ticket"></i></div>
        <div class="kpi-info">
          <h3>${state.stats.open_tickets}</h3>
          <p>Open Service Requests</p>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon tech"><i class="fas fa-user-check"></i></div>
        <div class="kpi-info">
          <h3>${state.stats.completed_tickets}</h3>
          <p>Completed Tickets</p>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon customers"><i class="fas fa-users"></i></div>
        <div class="kpi-info">
          <h3>${state.stats.total_customers}</h3>
          <p>Registered Customers</p>
        </div>
      </div>
    `;
  } else {
    kpiContainer.style.display = 'none';
  }
}

// Render Role Action Buttons & Title Header
function renderRoleSpecificHeader() {
  const titleEl = document.getElementById('dashboardHeaderTitle');
  const actionBtnEl = document.getElementById('headerActionBtnContainer');

  if (titleEl) {
    if (state.activeRole === 'CUSTOMER') {
      titleEl.innerHTML = `
        <h1>My Service Requests</h1>
        <p>Track repair status, view assigned technicians, and download invoices.</p>
      `;
    } else if (state.activeRole === 'TECHNICIAN') {
      titleEl.innerHTML = `
        <h1>Technician Workboard</h1>
        <p>Manage your assigned service jobs and post completion updates.</p>
      `;
    } else {
      titleEl.innerHTML = `
        <h1>FixFlow Admin Control</h1>
        <p>Overview of system metrics, technician assignments, and service categories.</p>
      `;
    }
  }

  if (actionBtnEl) {
    if (state.activeRole === 'CUSTOMER') {
      actionBtnEl.innerHTML = `
        <button class="action-btn" onclick="openCreateTicketModal()">
          <i class="fas fa-plus"></i> Create Service Request
        </button>
      `;
    } else if (state.activeRole === 'ADMIN') {
      actionBtnEl.innerHTML = `
        <button class="action-btn" onclick="openAddCategoryModal()">
          <i class="fas fa-folder-plus"></i> Manage Categories
        </button>
      `;
    } else {
      actionBtnEl.innerHTML = '';
    }
  }
}

// Filter and Render Tickets Grid
function renderTickets() {
  const gridEl = document.getElementById('ticketsGrid');
  if (!gridEl) return;

  let filtered = state.tickets.filter(ticket => {
    // Search match
    const searchMatch = !state.searchQuery || 
      ticket.ticket_number.toLowerCase().includes(state.searchQuery) ||
      ticket.title.toLowerCase().includes(state.searchQuery) ||
      ticket.category_name.toLowerCase().includes(state.searchQuery) ||
      ticket.description.toLowerCase().includes(state.searchQuery);

    // Status filter
    const statusMatch = state.currentFilterStatus === 'ALL' || ticket.status === state.currentFilterStatus;

    return searchMatch && statusMatch;
  });

  if (filtered.length === 0) {
    gridEl.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 2rem; color: var(--text-muted);">
        <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 1rem; color: var(--text-sub);"></i>
        <h3>No Service Requests Found</h3>
        <p>Try adjusting your search criteria or create a new request.</p>
      </div>
    `;
    return;
  }

  gridEl.innerHTML = filtered.map(ticket => `
    <div class="ticket-card">
      <div>
        <div class="ticket-top">
          <span class="ticket-code">${ticket.ticket_number}</span>
          <span class="badge-tag status-${ticket.status}">${formatStatus(ticket.status)}</span>
        </div>
        
        <h3 class="ticket-title">${escapeHTML(ticket.title)}</h3>
        <div style="font-size: 0.8rem; color: var(--primary); margin-bottom: 0.5rem;">
          <i class="fas fa-${ticket.category_icon || 'tag'}"></i> ${escapeHTML(ticket.category_name)}
          • <span class="priority-${ticket.priority}">Priority: ${ticket.priority}</span>
        </div>
        <p class="ticket-desc">${escapeHTML(ticket.description)}</p>

        <!-- Status Pipeline -->
        ${renderPipeline(ticket.status)}

        ${ticket.technician_notes ? `
          <div style="background: rgba(99, 102, 241, 0.08); padding: 0.65rem; border-radius: var(--radius-sm); font-size: 0.8rem; border-left: 3px solid var(--primary); margin-top: 0.75rem;">
            <strong>Technician Note:</strong> "${escapeHTML(ticket.technician_notes)}"
          </div>
        ` : ''}
      </div>

      <div class="ticket-footer">
        <div class="tech-info">
          <i class="fas fa-user-gear"></i>
          <span>${ticket.technician_details ? ticket.technician_details.first_name + ' ' + (ticket.technician_details.last_name || '') : 'Unassigned'}</span>
        </div>

        <div style="display: flex; gap: 0.4rem;">
          ${renderTicketActions(ticket)}
        </div>
      </div>
    </div>
  `).join('');
}

// Render Pipeline Bar
function renderPipeline(status) {
  const steps = ['PENDING', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED'];
  const currentIndex = steps.indexOf(status);

  return `
    <div class="pipeline-container">
      <div class="pipeline-steps">
        ${steps.map((step, idx) => {
          let stepClass = '';
          if (idx < currentIndex) stepClass = 'completed';
          else if (idx === currentIndex) stepClass = 'active';
          return `<div class="pipeline-step ${stepClass}">${idx < currentIndex ? '<i class="fas fa-check"></i>' : idx + 1}</div>`;
        }).join('')}
      </div>
      <div class="pipeline-labels">
        <span>Pending</span>
        <span>Assigned</span>
        <span>In Progress</span>
        <span>Completed</span>
      </div>
    </div>
  `;
}

// Render Context Action Buttons per Ticket & Role
function renderTicketActions(ticket) {
  let btns = '';

  if (state.activeRole === 'ADMIN') {
    btns += `<button class="btn-sm" onclick="openAssignModal(${ticket.id})"><i class="fas fa-user-plus"></i> Assign</button>`;
  }

  if (state.activeRole === 'TECHNICIAN' && ticket.status !== 'COMPLETED') {
    btns += `<button class="btn-sm" onclick="openStatusUpdateModal(${ticket.id})"><i class="fas fa-pen-to-square"></i> Update</button>`;
  }

  if (ticket.status === 'COMPLETED' && ticket.invoice_details) {
    btns += `<button class="btn-sm" onclick="viewInvoice(${ticket.id})"><i class="fas fa-file-invoice"></i> Invoice</button>`;
  }

  if (state.activeRole === 'CUSTOMER' && ticket.status === 'COMPLETED' && !ticket.rating) {
    btns += `<button class="btn-sm" onclick="openRatingModal(${ticket.id})"><i class="fas fa-star"></i> Rate</button>`;
  }

  return btns;
}

// Modals Handler Functions
function openCreateTicketModal() {
  const selectCat = document.getElementById('ticketCategorySelect');
  if (selectCat) {
    selectCat.innerHTML = state.categories.map(c => `
      <option value="${c.id}">${c.name} (Base ₹${c.base_price})</option>
    `).join('');
  }
  openModal('createTicketModal');
}

async function submitCreateTicket(event) {
  event.preventDefault();
  const title = document.getElementById('ticketTitle').value;
  const categoryId = document.getElementById('ticketCategorySelect').value;
  const priority = document.getElementById('ticketPriority').value;
  const description = document.getElementById('ticketDescription').value;

  try {
    const res = await fetch(`${API_BASE}/tickets/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        title,
        category: categoryId,
        priority,
        description
      })
    });
    if (res.ok) {
      closeModal('createTicketModal');
      await loadInitialData();
      renderApp();
      showToast('Service Request created successfully!');
    }
  } catch (err) {
    showToast('Failed to create service request', true);
  }
}

function openAssignModal(ticketId) {
  document.getElementById('assignTicketId').value = ticketId;
  const selectTech = document.getElementById('technicianSelect');
  if (selectTech) {
    selectTech.innerHTML = state.technicians.map(t => `
      <option value="${t.id}">${t.first_name} ${t.last_name || ''} (${t.specialization || 'General'})</option>
    `).join('');
  }
  openModal('assignModal');
}

async function submitAssignTechnician(event) {
  event.preventDefault();
  const ticketId = document.getElementById('assignTicketId').value;
  const technicianId = document.getElementById('technicianSelect').value;

  try {
    const res = await fetch(`${API_BASE}/tickets/${ticketId}/assign/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ technician_id: technicianId })
    });
    if (res.ok) {
      closeModal('assignModal');
      await loadInitialData();
      renderApp();
      showToast('Technician assigned successfully!');
    }
  } catch (err) {
    showToast('Failed to assign technician', true);
  }
}

function openStatusUpdateModal(ticketId) {
  document.getElementById('updateTicketId').value = ticketId;
  openModal('updateStatusModal');
}

async function submitStatusUpdate(event) {
  event.preventDefault();
  const ticketId = document.getElementById('updateTicketId').value;
  const statusVal = document.getElementById('updateStatusSelect').value;
  const notes = document.getElementById('updateWorkNotes').value;
  const extraCharge = document.getElementById('updateExtraCharge').value || 300;

  try {
    const res = await fetch(`${API_BASE}/tickets/${ticketId}/status/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        status: statusVal,
        technician_notes: notes,
        additional_charge: extraCharge
      })
    });
    if (res.ok) {
      closeModal('updateStatusModal');
      await loadInitialData();
      renderApp();
      showToast('Ticket status updated successfully!');
    }
  } catch (err) {
    showToast('Failed to update ticket status', true);
  }
}

function viewInvoice(ticketId) {
  const ticket = state.tickets.find(t => t.id === ticketId);
  if (!ticket || !ticket.invoice_details) return;

  const inv = ticket.invoice_details;
  const modalBody = document.getElementById('invoiceModalBody');

  modalBody.innerHTML = `
    <div class="invoice-box">
      <div class="invoice-header-row">
        <div>
          <div class="invoice-brand">FIXFLOW</div>
          <div style="font-size: 0.8rem; color: #6b7280; margin-top: 0.2rem;">Service Management & Customer Support</div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 1.1rem; font-weight: 700;">SERVICE INVOICE</div>
          <div style="font-size: 0.85rem; color: #4b5563;">Invoice #: ${inv.invoice_number}</div>
          <div style="font-size: 0.85rem; color: #4b5563;">Date: ${new Date(inv.issued_at).toLocaleDateString()}</div>
        </div>
      </div>

      <div style="margin-bottom: 1.5rem; display: flex; justify-content: space-between; font-size: 0.9rem; color: #374151;">
        <div>
          <strong>Billed To:</strong><br>
          ${ticket.customer_details ? ticket.customer_details.first_name + ' ' + (ticket.customer_details.last_name || '') : 'Customer'}<br>
          ${ticket.customer_details ? ticket.customer_details.address || 'New Delhi' : ''}
        </div>
        <div>
          <strong>Ticket Ref:</strong> ${ticket.ticket_number}<br>
          <strong>Technician:</strong> ${ticket.technician_details ? ticket.technician_details.first_name : 'Assigned Staff'}
        </div>
      </div>

      <table class="invoice-table">
        <thead>
          <tr>
            <th>Description</th>
            <th style="text-align: right;">Amount</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>${ticket.category_name} (Base Repair Charge)</td>
            <td style="text-align: right;">₹${inv.service_charge.toLocaleString('en-IN')}</td>
          </tr>
          <tr>
            <td>Spare Parts / Additional Diagnostics Charge</td>
            <td style="text-align: right;">₹${inv.additional_charge.toLocaleString('en-IN')}</td>
          </tr>
        </tbody>
      </table>

      <div class="invoice-total-row">
        Total Amount: ₹${inv.total_amount.toLocaleString('en-IN')}
      </div>

      <div style="margin-top: 1.5rem; display: flex; align-items: center; justify-content: space-between;">
        <span class="paid-stamp">STATUS: ${inv.payment_status}</span>
        <button class="action-btn" style="padding: 0.5rem 1rem; font-size: 0.85rem;" onclick="window.print()">
          <i class="fas fa-print"></i> Print Invoice
        </button>
      </div>
    </div>
  `;

  openModal('invoiceModal');
}

function openRatingModal(ticketId) {
  document.getElementById('ratingTicketId').value = ticketId;
  openModal('ratingModal');
}

async function submitRating(event) {
  event.preventDefault();
  const ticketId = document.getElementById('ratingTicketId').value;
  const rating = document.getElementById('ratingScoreSelect').value;
  const review = document.getElementById('ratingReviewText').value;

  try {
    const res = await fetch(`${API_BASE}/tickets/${ticketId}/rate/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ rating, review_text: review })
    });
    if (res.ok) {
      closeModal('ratingModal');
      await loadInitialData();
      renderApp();
      showToast('Thank you for rating our service!');
    }
  } catch (err) {
    showToast('Failed to submit rating', true);
  }
}

// Utility Modal Helpers
function openModal(id) {
  document.getElementById(id).classList.add('show');
}
function closeModal(id) {
  document.getElementById(id).classList.remove('show');
}

// Helper Formatters
function formatStatus(status) {
  return status.replace('_', ' ');
}

function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, 
    tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
  );
}

// Toast Alert Manager
function showToast(message, isError = false) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  if (isError) toast.style.borderColor = 'var(--priority-high)';
  toast.innerHTML = `<i class="fas ${isError ? 'fa-circle-exclamation' : 'fa-circle-check'}" style="color: ${isError ? 'var(--priority-high)' : 'var(--status-completed)'}"></i> ${message}`;
  
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}
