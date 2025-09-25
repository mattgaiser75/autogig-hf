'use client';

import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [insights, setInsights] = useState<any>(null);

  useEffect(() => {
    const url = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000") + "/analytics/insights";
    fetch(url).then(r => r.json()).then(setInsights).catch(()=>{});
  }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Dashboard</h2>
      <section className="grid md:grid-cols-4 gap-4">
        <div className="card">
          <div className="text-sm text-gray-500">Win Rate</div>
          <div className="text-2xl font-bold">{insights?.win_rate ?? '--'}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-500">Avg Response Time (h)</div>
          <div className="text-2xl font-bold">{insights?.avg_response_time_hours ?? '--'}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-500">Active Opportunities</div>
          <div className="text-2xl font-bold">{insights?.active_opportunities ?? '--'}</div>
        </div>
        <div className="card">
          <div className="text-sm text-gray-500">Automation</div>
          <div className="text-2xl font-bold capitalize">{insights?.automation_health ?? '--'}</div>
        </div>
      </section>

      <section className="card">
        <h3 className="font-semibold mb-2">Run Scout</h3>
        <button
          className="btn btn-primary"
          onClick={async () => {
            const url = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000") + "/automation/run_scout";
            await fetch(url, { method: "POST" });
            alert("Scout job queued.");
          }}
        >
          Run now
        </button>
      </section>
    </div>
  );
}
