"""
detector_server.py — лёгкий веб-UI для проверки видео реальным детектором (Студент 6).

Поднимает локальный сервер: страница с загрузкой видео -> прогон
fakeface_detector_real.analyze_video_safe -> показ media_anomalies + деталей.

Запуск (из корня проекта, в uv-venv с установленным детектором):
    .venv/Scripts/python -m uvicorn src.media.detector_server:app --host 127.0.0.1 --port 8000
или просто:
    .venv/Scripts/python src/media/detector_server.py

Это MVP/demo: вывод — risk-сигнал, не вердикт (см. дисклеймер в UI).
"""

from __future__ import annotations

import os
import sys
import tempfile

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

# импорт детектора (работает и как пакет, и при запуске файла напрямую)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from fakeface_detector_real import analyze_video_safe
except ImportError:  # запуск как модуль пакета
    from src.media.fakeface_detector_real import analyze_video_safe

app = FastAPI(title="FakeFace Detector")

PAGE = """<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>FakeFace — проверка видео</title>
<style>
  :root{
    --bg:#0b0e14; --panel:#141a24; --line:#222c3a; --txt:#e6edf3; --mut:#8b97a7;
    --accent:#6ea8fe; --ok:#2ecc71; --alert:#ff5d5d; --warn:#f5a623;
  }
  *{box-sizing:border-box} html,body{margin:0}
  body{font:15px/1.5 system-ui,Segoe UI,Roboto,sans-serif;background:
    radial-gradient(1200px 600px at 70% -10%,#16203020,transparent),var(--bg);
    color:var(--txt);min-height:100vh;display:flex;align-items:flex-start;justify-content:center;padding:48px 16px}
  .wrap{width:100%;max-width:680px}
  h1{font-size:26px;margin:0 0 4px;letter-spacing:-.5px}
  h1 .dot{color:var(--accent)}
  .sub{color:var(--mut);margin:0 0 24px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:22px;margin-bottom:18px}
  .drop{border:1.5px dashed #2c3a4e;border-radius:14px;padding:34px;text-align:center;cursor:pointer;
    transition:.18s;background:#0e141d}
  .drop:hover,.drop.drag{border-color:var(--accent);background:#101a28}
  .drop b{color:var(--accent)}
  .drop small{display:block;color:var(--mut);margin-top:6px}
  .file{margin-top:14px;color:var(--mut);font-size:13px;word-break:break-all}
  button{margin-top:16px;width:100%;padding:13px;border:0;border-radius:11px;cursor:pointer;
    background:linear-gradient(180deg,#6ea8fe,#4f86e6);color:#06101f;font-weight:700;font-size:15px;transition:.15s}
  button:disabled{opacity:.5;cursor:default}
  button:not(:disabled):hover{filter:brightness(1.08)}
  .verdict{display:none;margin-bottom:18px;border-radius:14px;padding:16px 18px;font-weight:600;border:1px solid}
  .verdict.alert{background:#2a1416;border-color:#5a2326;color:#ffb3b3}
  .verdict.safe{background:#10231a;border-color:#1f4d36;color:#9ff0c4}
  .flags{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .flag{display:flex;align-items:center;justify-content:space-between;background:#0e141d;
    border:1px solid var(--line);border-radius:11px;padding:11px 13px}
  .flag .k{color:var(--mut);font-size:13px}
  .pill{font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px}
  .pill.t{background:#3a1518;color:#ff8e8e}  /* true / alert */
  .pill.f{background:#12281d;color:#74e0a3}  /* false / ok */
  .det{margin-top:14px;font:12.5px/1.6 ui-monospace,Menlo,Consolas,monospace;color:var(--mut);
    background:#0a0f17;border:1px solid var(--line);border-radius:11px;padding:12px;white-space:pre-wrap;display:none}
  .spin{display:none;margin-top:16px;color:var(--mut);text-align:center}
  .spin.on{display:block}
  .dis{color:var(--mut);font-size:12px;margin-top:18px;line-height:1.5}
  .bar{height:3px;border-radius:3px;overflow:hidden;margin-top:10px;background:#16202e}
  .bar i{display:block;height:100%;width:30%;background:var(--accent);animation:run 1.1s infinite}
  @keyframes run{0%{margin-left:-30%}100%{margin-left:100%}}
</style>
</head>
<body>
<div class="wrap">
  <h1>FakeFace<span class="dot">.</span> проверка видео</h1>
  <p class="sub">Загрузи видео — детектор оценит лицо, признаки дипфейка и синтетический голос (на GPU).</p>

  <div class="card">
    <label class="drop" id="drop">
      <b>Перетащи видео</b> или нажми, чтобы выбрать
      <small>mp4 / mov / webm — анализируется ~10–25 c</small>
      <input id="file" type="file" accept="video/*" hidden/>
    </label>
    <div class="file" id="fname"></div>
    <button id="go" disabled>Анализировать</button>
    <div class="spin" id="spin">Анализ на GPU…<div class="bar"><i></i></div></div>
  </div>

  <div class="verdict" id="verdict"></div>
  <div class="card" id="res" style="display:none">
    <div class="flags" id="flags"></div>
    <div class="det" id="det"></div>
  </div>

  <p class="dis">⚠️ MVP, не вердикт. Система выдаёт <b>risk-сигнал</b> и объясняет почему —
  финальное решение за человеком. Точность ограничена готовыми моделями
  (видео-модель не валидирована на реальных video-deepfake; аудио уверенно ловит TTS-синтез).</p>
</div>

<script>
const f=document.getElementById('file'), drop=document.getElementById('drop'),
      go=document.getElementById('go'), fname=document.getElementById('fname'),
      spin=document.getElementById('spin'), res=document.getElementById('res'),
      flags=document.getElementById('flags'), det=document.getElementById('det'),
      verdict=document.getElementById('verdict');
let chosen=null;
function pick(file){chosen=file; fname.textContent=file?('Файл: '+file.name+' ('+(file.size/1048576).toFixed(1)+' МБ)'):''; go.disabled=!file;}
f.onchange=e=>pick(e.target.files[0]);
;['dragenter','dragover'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add('drag')}));
;['dragleave','drop'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.remove('drag')}));
drop.addEventListener('drop',e=>{const file=e.dataTransfer.files[0]; if(file){f.files=e.dataTransfer.files; pick(file);}});
const LABELS={has_face:'Лицо в кадре',possible_deepfake:'Возможный дипфейк',synthetic_voice_suspected:'Синтетический голос',lip_sync_anomaly:'Рассинхрон губ'};
go.onclick=async()=>{
  if(!chosen)return;
  go.disabled=true; spin.classList.add('on'); res.style.display='none'; verdict.style.display='none';
  try{
    const fd=new FormData(); fd.append('video',chosen);
    const r=await fetch('/analyze',{method:'POST',body:fd});
    const j=await r.json();
    const a=j.media_anomalies||{}, d=j.details||{};
    flags.innerHTML='';
    for(const k of ['has_face','possible_deepfake','synthetic_voice_suspected','lip_sync_anomaly']){
      const v=!!a[k];
      // has_face=true это норма (зелёный), остальные true = тревога (красный)
      const alert = k==='has_face' ? false : v;
      flags.insertAdjacentHTML('beforeend',
        `<div class="flag"><span class="k">${LABELS[k]}</span>
         <span class="pill ${alert?'t':'f'}">${v?'да':'нет'}</span></div>`);
    }
    det.style.display='block';
    det.textContent=JSON.stringify(d,null,2);
    res.style.display='block';
    const suspicious = a.possible_deepfake || a.synthetic_voice_suspected || a.lip_sync_anomaly;
    verdict.className='verdict '+(suspicious?'alert':'safe');
    verdict.textContent=suspicious
      ? '⚠️ Обнаружены risk-сигналы подделки — материал стоит передать на ручную проверку.'
      : '✓ Явных признаков подделки не обнаружено (это не гарантия подлинности).';
    verdict.style.display='block';
  }catch(e){
    verdict.className='verdict alert'; verdict.textContent='Ошибка анализа: '+e; verdict.style.display='block';
  }finally{ spin.classList.remove('on'); go.disabled=false; }
};
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
