document.addEventListener('DOMContentLoaded', () => {
    loadJobs();

    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', loadJobs);
    }
});

function loadJobs() {
    const grid = document.getElementById('job-grid');
    if (!grid) return; // Not on dashboard

    fetch('/api/jobs')
        .then(response => response.json())
        .then(jobs => {
            grid.innerHTML = '';

            if (jobs.length === 0) {
                grid.innerHTML = `
                    <div class="col-span-full text-center py-20 bg-white rounded-xl border border-dashed border-slate-300">
                        <svg class="mx-auto h-12 w-12 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                           <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <h3 class="mt-2 text-sm font-medium text-slate-900">No jobs found</h3>
                        <p class="mt-1 text-sm text-slate-500">Check your settings or wait for the scheduler.</p>
                        <div class="mt-6">
                            <a href="/settings" class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-indigo-600 bg-indigo-50 hover:bg-indigo-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                                Configure Settings
                            </a>
                        </div>
                    </div>
                `;
                return;
            }

            jobs.forEach(job => {
                const card = createJobCard(job);
                grid.appendChild(card);
            });
        })
        .catch(err => {
            console.error('Error loading jobs:', err);
            grid.innerHTML = '<p class="col-span-full text-center text-red-500">Failed to load jobs.</p>';
        });
}

function createJobCard(job) {
    const div = document.createElement('div');
    div.className = 'bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300 border border-slate-100 overflow-hidden flex flex-col';

    // Source Badge Color
    const badgeColor = job.source === 'LinkedIn' ? 'bg-blue-100 text-blue-800' : 'bg-orange-100 text-orange-800';

    div.innerHTML = `
        <div class="p-6 flex-grow">
            <div class="flex justify-between items-start">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${badgeColor}">
                    ${job.source}
                </span>
                <span class="text-xs text-slate-400">${job.posted_date ? new Date(job.posted_date).toLocaleDateString() : 'Recently'}</span>
            </div>
            <h3 class="mt-4 text-lg font-bold text-slate-900 leading-tight line-clamp-2" title="${job.title}">
                <a href="${job.url}" target="_blank" class="hover:text-indigo-600 transition-colors">
                    ${job.title}
                </a>
            </h3>
            <div class="mt-2 flex items-center text-sm text-slate-500">
                <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                ${job.company}
            </div>
            <div class="mt-1 flex items-center text-sm text-slate-500">
                <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                ${job.location}
            </div>
        </div>
        <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-between items-center">
            <span class="text-xs font-semibold text-slate-400">Relevance: <span class="text-green-600">${job.relevance_score || 0}</span></span>
            <a href="${job.url}" target="_blank" class="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-500">
                Apply Now
                <svg class="ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
            </a>
        </div>
    `;
    return div;
}
