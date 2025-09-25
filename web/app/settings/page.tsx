'use client';

import { useEffect, useState } from 'react';

type Model = { id: string; label: string };

export default function Settings(){
  const [models, setModels] = useState<Model[]>([]);
  const [provider, setProvider] = useState<string>('');
  const [selected, setSelected] = useState<string>('');
  const [def, setDef] = useState<string>('');
  const api = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(()=>{
    fetch(api + "/llm/models").then(r=>r.json()).then(d=>{
      setProvider(d.provider);
      setModels(d.models || []);
      setDef(d.default);
      const saved = localStorage.getItem("llm_model") || d.default;
      setSelected(saved);
    }).catch(()=>{});
  },[]);

  const save = () => {
    localStorage.setItem("llm_model", selected);
    alert("Saved model: " + selected);
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Settings</h2>
      <div className="card space-y-3">
        <div className="text-sm text-gray-600">LLM Provider: <b>{provider || 'unknown'}</b></div>
        <label className="block text-sm font-medium">Choose model</label>
        <select className="border rounded px-3 py-2" value={selected} onChange={e=>setSelected(e.target.value)}>
          {models.map(m=> <option key={m.id} value={m.id}>{m.label} ({m.id})</option>)}
          {!models.length && def ? <option value={def}>{def}</option> : null}
        </select>
        <div className="flex gap-2">
          <button className="btn btn-primary" onClick={save}>Save</button>
          <button className="btn" onClick={()=>{ setSelected(def); }}>Reset to default</button>
        </div>
        <p className="text-xs text-gray-500">The selected model will be used when creating personas and composing pitches.</p>
      </div>
    </div>
  )
}
