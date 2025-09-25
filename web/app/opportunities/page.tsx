'use client';

import { useEffect, useState } from 'react';

type Opp = {
  id: string;
  title: string;
  description: string;
  source: string;
  proposals_count: number;
  semantic_match_score: number;
  final_rank_score: number;
};

export default function Opportunities() {
  const [items, setItems] = useState<Opp[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const load = () => fetch(api + "/opportunities").then(r => r.json()).then(setItems);

  useEffect(() => { load(); }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Opportunities</h2>

      <div className="card space-y-3">
        <div className="grid md:grid-cols-2 gap-3">
          <input className="border rounded px-3 py-2" placeholder="Title" value={title} onChange={e=>setTitle(e.target.value)} />
          <input className="border rounded px-3 py-2" placeholder="Description" value={description} onChange={e=>setDescription(e.target.value)} />
        </div>
        <button className="btn btn-primary" onClick={async ()=>{
          await fetch(api + "/opportunities", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({ title, description, source: "manual" })
          });
          setTitle(''); setDescription('');
          load();
        }}>Add</button>
      </div>

      <div className="grid gap-3">
        {items.map(o => (
          <div key={o.id} className="card">
            <div className="flex items-start justify-between">
              <div>
                <div className="font-semibold">{o.title}</div>
                <div className="text-sm text-gray-600">{o.description}</div>
              </div>
              <div className="text-right">
                <div className="badge">score {o.final_rank_score.toFixed(2)}</div>
                <div className="text-xs text-gray-500">proposals {o.proposals_count}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
