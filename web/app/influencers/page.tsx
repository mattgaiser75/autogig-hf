'use client';

import { useEffect, useState } from 'react';

type Inf = {
  id: string;
  name: string;
  niche: string;
  tone: string;
  platforms: string[];
  avatar_url: string;
  bio: string;
  content_pillars: string[];
  posting_schedule: Record<string,string>;
  hooks_library: string[];
};

export default function Influencers() {
  const [items, setItems] = useState<Inf[]>([]);
  const [name, setName] = useState('Elon Dusk');
  const [niche, setNiche] = useState('AI + Automation');
  const [tone, setTone] = useState('bold, witty');
  const [platforms, setPlatforms] = useState('YouTube, TikTok, X');

  const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const load = () => fetch(api + "/influencers").then(r => r.json()).then(setItems);

  useEffect(()=>{ load(); },[]);

  const create = async () => {
    const model = localStorage.getItem("llm_model") || undefined;
    const res = await fetch(api + "/influencers", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({
        name, niche, tone,
        platforms: platforms.split(',').map(x=>x.trim()),
        model
      })
    });
    if (res.ok) { setName(''); setNiche(''); setTone(''); setPlatforms(''); load(); }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Influencer Personas</h2>

      <div className="card space-y-3">
        <div className="grid md:grid-cols-2 gap-3">
          <input className="border rounded px-3 py-2" placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
          <input className="border rounded px-3 py-2" placeholder="Niche" value={niche} onChange={e=>setNiche(e.target.value)} />
          <input className="border rounded px-3 py-2 md:col-span-2" placeholder="Tone" value={tone} onChange={e=>setTone(e.target.value)} />
          <input className="border rounded px-3 py-2 md:col-span-2" placeholder="Platforms (comma-separated)" value={platforms} onChange={e=>setPlatforms(e.target.value)} />
        </div>
        <button className="btn btn-primary" onClick={create}>Create persona (uses selected LLM if configured)</button>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {items.map(it => (
          <div key={it.id} className="card space-y-2">
            <div className="flex items-center gap-3">
              <img src={it.avatar_url} alt={it.name} className="w-10 h-10 rounded-full border" />
              <div>
                <div className="font-semibold">{it.name}</div>
                <div className="text-xs text-gray-600">{it.niche} • {it.tone}</div>
              </div>
            </div>
            <p className="text-sm">{it.bio}</p>
            <div>
              <div className="text-xs font-medium mb-1">Pillars</div>
              <div className="flex flex-wrap gap-2">
                {it.content_pillars.map((p, i)=>(<span key={i} className="badge">{p}</span>))}
              </div>
            </div>
            <div>
              <div className="text-xs font-medium mb-1">Schedule</div>
              <div className="text-xs text-gray-700">{Object.entries(it.posting_schedule).map(([k,v])=>`${k}: ${v}`).join(' • ')}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
