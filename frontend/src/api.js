const BASE = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1').replace(/\/$/, '');
async function request(path, options = {}) {
  const response = await fetch(`${BASE}${path}`, options);
  const type = response.headers.get('content-type') || '';
  const data = type.includes('application/json') ? await response.json() : await response.text();
  if (!response.ok) throw new Error(typeof data === 'object' ? (data.detail || 'API request failed') : data);
  return data;
}
export const api = {
  health: () => request('/health'),
  jobs: () => request('/jobs'),
  job: id => request(`/jobs/${encodeURIComponent(id)}`),
  screen: (jobId, file) => { const body = new FormData(); body.append('job_id', jobId); body.append('file', file); return request('/screening/single', { method: 'POST', body }); }
};
