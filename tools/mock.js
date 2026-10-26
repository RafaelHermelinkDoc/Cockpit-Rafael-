/* Attrappe der Plattform (window.claude.use) mit In-Memory-Datenbank: onSnapshot, set/update(merge)/delete, where/orderBy/limit/get; assets, sample, downloads, permissions, mcp */
(function(){
  const SEED = window.__SEED || {};
  const q = new URLSearchParams(location.search);
  const data = {};   // collection -> Map(id -> doc)
  const subs = {};   // collection -> [cb]
  Object.keys(SEED).forEach(c => { data[c] = new Map(); SEED[c].forEach(d => { const o = Object.assign({}, d); const id = o.id; delete o.id; data[c].set(id, o); }); });
  const col = c => { if (!data[c]) data[c] = new Map(); return data[c]; };
  const clone = v => JSON.parse(JSON.stringify(v === undefined ? null : v));
  const isObj = v => v && typeof v === 'object' && !Array.isArray(v);
  function merge(a, b){ const o = Object.assign({}, a); Object.keys(b).forEach(k => { if (isObj(b[k]) && isObj(o[k])) o[k] = merge(o[k], b[k]); else o[k] = clone(b[k]); }); return o; }
  const delay = ms => new Promise(r => setTimeout(r, ms));
  window.__mock = { writes: [], failWrites: false, dbDelay: +(q.get('dbDelay') || 0), downloads: [], uploads: [] };
  function notify(c){ (subs[c] || []).forEach(cb => cb(snap(c))); }
  function snap(c, docs){ const arr = docs || Array.from(col(c).entries()).map(([id, d]) => ({ id, d })); return { docs: arr.map(x => ({ id: x.id, exists: true, data: () => clone(x.d) })) }; }
  function query(c, w, ob, lim){
    return {
      where: (f, op, v) => query(c, w.concat([[f, op, v]]), ob, lim),
      orderBy: (f, dir) => query(c, w, [f, dir || 'asc'], lim),
      limit: n => query(c, w, ob, n),
      get: async () => { await delay(5); return snap(c, run()); },
      onSnapshot: (cb, err) => { (subs[c] = subs[c] || []).push(() => cb(snap(c, run()))); setTimeout(() => cb(snap(c, run())), 20 + window.__mock.dbDelay); return () => {}; }
    };
    function run(){
      let arr = Array.from(col(c).entries()).map(([id, d]) => ({ id, d }));
      w.forEach(([f, op, v]) => { arr = arr.filter(x => op === '==' ? x.d[f] === v : op === '<=' ? x.d[f] <= v : op === '>=' ? x.d[f] >= v : op === '<' ? x.d[f] < v : op === '>' ? x.d[f] > v : true); });
      if (ob) arr.sort((a, b) => (a.d[ob[0]] < b.d[ob[0]] ? -1 : a.d[ob[0]] > b.d[ob[0]] ? 1 : 0) * (ob[1] === 'desc' ? -1 : 1));
      if (lim) arr = arr.slice(0, lim);
      return arr;
    }
  }
  async function write(path, op, body){
    await delay(3);
    if (window.__mock.failWrites){ const e = new Error('fail'); e.code = 'unavailable'; throw e; }
    const i = path.indexOf('/'), c = path.slice(0, i), id = path.slice(i + 1);
    const m = col(c);
    if (op === 'set') m.set(id, clone(body));
    else if (op === 'update'){ if (!m.has(id)){ const e = new Error('not found'); e.code = 'not_found'; throw e; } m.set(id, merge(m.get(id), body)); }
    else if (op === 'delete') m.delete(id);
    window.__mock.writes.push({ path, op, body: clone(body) });
    notify(c);
  }
  const db = {
    collection: c => query(c, [], null, 0),
    doc: path => ({
      set: b => write(path, 'set', b), update: b => write(path, 'update', b), delete: () => write(path, 'delete', null),
      get: async () => { const i = path.indexOf('/'); const d = col(path.slice(0, i)).get(path.slice(i + 1)); return { exists: !!d, id: path.slice(i + 1), data: () => clone(d) }; }
    })
  };
  const SAMPLE = {
    'heute gelaufen': () => ({ eintraege: [{ typ: 'takt', rhythmusId: (SEED.rhythmen && SEED.rhythmen[0] ? SEED.rhythmen[0].id : 'x'), date: today(), ziel: 'Sport' }] }),
    'default': () => ({ eintraege: [{ typ: 'bewegung', projectId: 'sprind-scoping', text: 'Testbewegung', date: today(), ziel: 'Scoping Review' }] })
  };
  function today(){ const d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  const caps = {
    db: db,
    assets: { upload: async (blob, o) => { const id = 'a' + Math.random().toString(36).slice(2, 10).padEnd(30, '0'); window.__mock.uploads.push(id); return { id }; }, delete: async id => {} },
    sample: { json: async (prompt, o) => { await delay(40); const m = /Notiz: «([^»]*)»/.exec(prompt); const txt = (m ? m[1] : '').toLowerCase(); const f = Object.keys(SAMPLE).find(k => k !== 'default' && txt.includes(k)); return (SAMPLE[f] || SAMPLE.default)(); } },
    downloads: { save: async x => { window.__mock.downloads.push({ filename: x.filename, size: x.data.length }); } },
    permissions: { state: async () => 'prompt' },
    mcp: { callTool: async () => { const e = new Error('nc'); e.code = 'server_not_connected'; throw e; } }
  };
  window.claude = { use: async name => { await delay(2); if (!caps[name]) throw new Error('no ' + name); return caps[name]; } };
})();
