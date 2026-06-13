"""
detector_server.py — лёгкий веб-UI для проверки видео реальным детектором (Студент 6).

Поднимает локальный сервер: страница с загрузкой видео -> прогон
fakeface_detector_real.analyze_video_safe -> показ вероятностей (ансамбль),
разбивки по моделям и регулируемого порога.

Запуск (из корня проекта, в uv-venv с установленным детектором):
    .venv/Scripts/python src/media/detector_server.py

Это MVP/demo: вывод — risk-сигнал, не вердикт (см. дисклеймер в UI).
"""

from __future__ import annotations

import os
import sys
import tempfile

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from fakeface_detector_real import analyze_video_safe
except ImportError:
    from src.media.fakeface_detector_real import analyze_video_safe

app = FastAPI(title="FakeFace Detector")

PAGE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>FakeFace — проверка видео</title>
<style>
  :root{--bg:#0b0e14;--panel:#141a24;--line:#243040;--txt:#e6edf3;--mut:#8b97a7;
    --accent:#6ea8fe;--ok:#3ddc84;--alert:#ff6b6b;}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font:15px/1.55 system-ui,"Segoe UI",Roboto,sans-serif;color:var(--txt);
    background:radial-gradient(900px 500px at 75% -120px,#1b2a44,transparent),var(--bg);
    min-height:100vh;display:flex;justify-content:center;padding:44px 16px}
  .wrap{width:100%;max-width:580px}
  h1{font-size:25px;font-weight:700;letter-spacing:-.4px;margin-bottom:6px} h1 b{color:var(--accent)}
  .sub{color:var(--mut);margin-bottom:22px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:20px}
  .drop{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;
    width:100%;min-height:148px;padding:24px 18px;text-align:center;border:1.5px dashed #34465c;
    border-radius:13px;background:#0e141d;cursor:pointer;transition:.15s}
  .drop:hover,.drop.drag{border-color:var(--accent);background:#101a29}
  .drop .ico{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;
    background:#16243a;color:var(--accent);font-size:20px}
  .drop .main{font-weight:600} .drop .main b{color:var(--accent)} .drop .hint{color:var(--mut);font-size:13px}
  .fname{color:var(--mut);font-size:13px;margin-top:12px;min-height:18px;word-break:break-all}
  .btn{display:block;width:100%;margin-top:14px;padding:13px;border:0;border-radius:11px;
    background:var(--accent);color:#08111f;font-weight:700;font-size:15px;cursor:pointer;transition:.15s}
  .btn:disabled{opacity:.45;cursor:default} .btn:not(:disabled):hover{filter:brightness(1.08)}
  .spin{display:none;align-items:center;gap:10px;margin-top:14px;color:var(--mut);font-size:14px}
  .spin.on{display:flex}
  .ldr{width:16px;height:16px;border:2px solid #2a3850;border-top-color:var(--accent);border-radius:50%;animation:sp .8s linear infinite}
  @keyframes sp{to{transform:rotate(360deg)}}
  .verdict{display:none;margin-top:18px;padding:14px 16px;border-radius:13px;border:1px solid;font-weight:600}
  .verdict.alert{background:#241114;border-color:#5a262a;color:#ffb4b4}
  .verdict.safe{background:#0f2118;border-color:#1f5038;color:#a6f0c6}
  .prob{margin-top:14px}
  .prob .row{display:flex;justify-content:space-between;font-size:13px;margin-bottom:5px}
  .prob .row b{font-variant-numeric:tabular-nums}
  .track{height:9px;border-radius:6px;background:#0a0f17;border:1px solid var(--line);overflow:hidden;margin-bottom:13px;position:relative}
  .track i{display:block;height:100%;border-radius:6px;transition:width .25s}
  .track .mark{position:absolute;top:-3px;bottom:-3px;width:2px;background:#cdd6e0;opacity:.6}
  .thr{display:flex;align-items:center;gap:10px;margin-top:6px;font-size:13px;color:var(--mut)}
  .thr input{flex:1;accent-color:var(--accent)}
  .thr b{color:var(--txt);font-variant-numeric:tabular-nums}
  .flags{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
  .flag{display:flex;align-items:center;justify-content:space-between;gap:8px;background:#0e141d;
    border:1px solid var(--line);border-radius:11px;padding:11px 13px}
  .flag .k{color:var(--mut);font-size:13px}
  .pill{font-size:12px;font-weight:700;padding:3px 11px;border-radius:999px;white-space:nowrap}
  .pill.t{background:#3a1619;color:#ff9b9b} .pill.f{background:#123325;color:#7ce8ac}
  details{margin-top:12px} summary{color:var(--mut);font-size:13px;cursor:pointer}
  pre{margin-top:8px;font:12.5px/1.55 ui-monospace,Consolas,monospace;color:var(--mut);
    background:#0a0f17;border:1px solid var(--line);border-radius:11px;padding:12px;overflow:auto;white-space:pre-wrap}
  .dis{color:var(--mut);font-size:12px;margin-top:18px;line-height:1.55}
</style>
</head>
<body>
<div class="wrap">
  <h1>FakeFace<b>.</b> проверка видео</h1>
  <p class="sub">Ансамбль из 3 моделей оценивает лицо (дипфейк) и голос (синтез). Порог настраивается.</p>

  <div class="card">
    <label class="drop" id="drop">
      <span class="ico">⬆</span>
      <span class="main"><b>Перетащи видео</b> или нажми, чтобы выбрать</span>
      <span class="hint">mp4 / mov / webm — анализ ~15–35 с (3 модели на GPU)</span>
      <input id="file" type="file" accept="video/*" hidden/>
    </label>
    <div class="fname" id="fname"></div>
    <button class="btn" id="go" disabled>Анализировать</button>
    <div class="spin" id="spin"><span class="ldr"></span> Анализ ансамблем на GPU…</div>

    <div class="verdict" id="verdict"></div>

    <div class="prob" id="prob" style="display:none">
      <div class="row"><span>Дипфейк (лицо), ансамбль‑max</span><b id="pf">—</b></div>
      <div class="track"><i id="pfbar"></i><span class="mark" id="pfmark"></span></div>
      <div class="row"><span>Синтетический голос</span><b id="pv">—</b></div>
      <div class="track"><i id="pvbar"></i><span class="mark" id="pvmark"></span></div>
      <div class="thr">Порог: <input id="thr" type="range" min="0" max="1" step="0.01" value="0.5"/><b id="thrv">0.50</b></div>
    </div>

    <div id="flags" class="flags" style="display:none"></div>
    <details id="detWrap" style="display:none"><summary>Технические детали (по моделям)</summary><pre id="det"></pre></details>
  </div>

  <p class="dis">⚠️ MVP, не вердикт — <b>risk-сигнал</b> для ручной проверки. Готовые модели плохо
  переносятся на чужие дипфейки (низкий recall): возможны пропуски. Двигай <b>порог</b>, чтобы
  поднять чувствительность. Голос-детектор надёжнее видео.</p>
</div>

<script>
const $=id=>document.getElementById(id);
const file=$('file'),drop=$('drop'),go=$('go'),fname=$('fname'),spin=$('spin'),
      verdict=$('verdict'),prob=$('prob'),flags=$('flags'),detWrap=$('detWrap'),det=$('det'),
      thr=$('thr'),thrv=$('thrv');
const LB={has_face:'Лицо в кадре',possible_deepfake:'Возможный дипфейк',
          synthetic_voice_suspected:'Синтетический голос',lip_sync_anomaly:'Рассинхрон губ'};
let chosen=null, last=null;   // last = {a, d, pf, pv, hasFace, hasAudio}

function pick(f){chosen=f; fname.textContent=f?('Выбрано: '+f.name+'  ·  '+(f.size/1048576).toFixed(1)+' МБ'):''; go.disabled=!f;}
file.addEventListener('change',e=>pick(e.target.files[0]||null));
['dragenter','dragover'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add('drag')}));
['dragleave','drop'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.remove('drag')}));
drop.addEventListener('drop',e=>{const f=e.dataTransfer.files[0]; if(f){file.files=e.dataTransfer.files; pick(f);}});

function colour(p){ return p>=.66?'#ff6b6b':p>=.4?'#f5a623':'#3ddc84'; }

function render(){
  if(!last) return;
  const t=parseFloat(thr.value); thrv.textContent=t.toFixed(2);
  const pf=last.pf, pv=last.pv;
  $('pf').textContent=(pf*100).toFixed(0)+'%';
  $('pv').textContent=last.hasAudio?((pv*100).toFixed(0)+'%'):'нет аудио';
  const bf=$('pfbar'),bv=$('pvbar');
  bf.style.width=(pf*100)+'%'; bf.style.background=colour(pf);
  bv.style.width=(last.hasAudio?pv*100:0)+'%'; bv.style.background=colour(pv);
  $('pfmark').style.left=(t*100)+'%'; $('pvmark').style.left=(t*100)+'%';

  const df = pf>=t, sv = last.hasAudio && pv>=t;
  const A={has_face:last.hasFace, possible_deepfake:df, synthetic_voice_suspected:sv, lip_sync_anomaly:false};
  flags.innerHTML='';
  ['has_face','possible_deepfake','synthetic_voice_suspected','lip_sync_anomaly'].forEach(k=>{
    const v=!!A[k], alarm = k!=='has_face' && v;
    flags.insertAdjacentHTML('beforeend',
      `<div class="flag"><span class="k">${LB[k]}</span><span class="pill ${alarm?'t':'f'}">${v?'да':'нет'}</span></div>`);
  });
  const susp = df || sv;
  verdict.className='verdict '+(susp?'alert':'safe');
  verdict.textContent = susp
    ? '⚠️ При пороге '+t.toFixed(2)+' есть risk-сигналы подделки — на ручную проверку.'
    : '✓ При пороге '+t.toFixed(2)+' явных признаков подделки нет (не гарантия подлинности).';
}
thr.addEventListener('input',render);

go.addEventListener('click', async ()=>{
  if(!chosen) return;
  go.disabled=true; spin.classList.add('on');
  verdict.style.display='none'; prob.style.display='none'; flags.style.display='none'; detWrap.style.display='none';
  try{
    const fd=new FormData(); fd.append('video',chosen);
    const r=await fetch('/analyze',{method:'POST',body:fd});
    if(!r.ok) throw new Error('HTTP '+r.status);
    const j=await r.json(); const a=j.media_anomalies||{}, d=j.details||{};
    last={ a, d, pf:(d.avg_fake_probability||0), pv:(d.voice_fake_probability||0),
           hasFace:!!a.has_face, hasAudio:!!d.has_audio };
    thr.value = d.threshold!=null ? d.threshold : 0.5;
    det.textContent=JSON.stringify(d,null,2);
    verdict.style.display='block'; prob.style.display='block'; flags.style.display='grid'; detWrap.style.display='block';
    render();
  }catch(e){
    verdict.className='verdict alert'; verdict.textContent='Ошибка анализа: '+e.message; verdict.style.display='block';
  }finally{ spin.classList.remove('on'); go.disabled=false; }
});
</script>
</body></html>"""


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return PAGE


@app.post("/analyze")
async def analyze(video: UploadFile = File(...)) -> JSONResponse:
    suffix = os.path.splitext(video.filename or "")[1] or ".mp4"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        tmp.write(await video.read())
        tmp.close()
        anomalies, details = analyze_video_safe(tmp.name)
        return JSONResponse({"media_anomalies": anomalies, "details": details})
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
