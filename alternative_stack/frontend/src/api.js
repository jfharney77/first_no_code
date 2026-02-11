const BASE = '/api';

async function request(url, options = {}) {
    const res = await fetch(`${BASE}${url}`, {
        headers: { 'Content-Type': 'application/json', ...options.headers },
        ...options,
    });
    if (res.status === 204) return null;
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || 'Request failed');
    }
    return res.json();
}

// Team Members
export const getTeamMembers = () => request('/team');
export const getTeamMember = (id) => request(`/team/${id}`);
export const createTeamMember = (data) => request('/team', { method: 'POST', body: JSON.stringify(data) });
export const updateTeamMember = (id, data) => request(`/team/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteTeamMember = (id) => request(`/team/${id}`, { method: 'DELETE' });

// Chores
export const getChore = (id) => request(`/chores/${id}`);
export const createChore = (data) => request('/chores', { method: 'POST', body: JSON.stringify(data) });
export const updateChore = (id, data) => request(`/chores/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteChore = (id) => request(`/chores/${id}`, { method: 'DELETE' });
export const toggleChore = (id) => request(`/chores/${id}/toggle`, { method: 'POST' });

// Calendar
export const getCalendar = (year, month) => request(`/calendar/${year}/${month}`);

// Recurring
export const getRecurringChores = () => request('/recurring');
export const getRecurringChore = (id) => request(`/recurring/${id}`);
export const createRecurringChore = (data) => request('/recurring', { method: 'POST', body: JSON.stringify(data) });
export const updateRecurringChore = (id, data) => request(`/recurring/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteRecurringChore = (id) => request(`/recurring/${id}`, { method: 'DELETE' });
export const generateRecurring = (id) => request(`/recurring/${id}/generate`, { method: 'POST' });
