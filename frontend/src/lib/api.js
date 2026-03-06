const BASE = '/api';

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export const api = {
  // Users
  createUser: () => request('/users', { method: 'POST' }),
  getUser: (id) => request(`/users/${id}`),
  updateUser: (id, data) => request(`/users/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),

  // Chat
  chat: (data) => request('/chat', { method: 'POST', body: JSON.stringify(data) }),
  getChatHistory: (userId, contextType = 'general') =>
    request(`/chat/history/${userId}?context_type=${contextType}`),
  clearChat: (userId, contextType = 'general') =>
    request(`/chat/history/${userId}?context_type=${contextType}`, { method: 'DELETE' }),

  // Vacancies
  listVacancies: (userId) => request(`/vacancies/${userId}`),
  createVacancy: (data) => request('/vacancies', { method: 'POST', body: JSON.stringify(data) }),
  createVacancyFromUrl: (data) => request('/vacancies/from-url', { method: 'POST', body: JSON.stringify(data) }),
  createVacancyFromText: (data) => request('/vacancies/from-text', { method: 'POST', body: JSON.stringify(data) }),
  updateVacancy: (id, data) => request(`/vacancies/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteVacancy: (id) => request(`/vacancies/${id}`, { method: 'DELETE' }),

  // CVs
  listTemplates: () => request('/cvs/templates'),
  listCVs: (userId) => request(`/cvs/${userId}`),
  createCV: (data) => request('/cvs', { method: 'POST', body: JSON.stringify(data) }),
  getCV: (id) => request(`/cvs/detail/${id}`),
  updateCV: (id, data) => request(`/cvs/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),
  deleteCV: (id) => request(`/cvs/${id}`, { method: 'DELETE' }),
  exportPDF: (id) => fetch(`${BASE}/cvs/${id}/pdf`, { method: 'POST' }),
  changeTemplate: (id, templateId) =>
    request(`/cvs/${id}/change-template?template_id=${templateId}`, { method: 'POST' }),
};
