#!/usr/bin/env python3
"""Собирает privacy.html, terms.html, support.html и index.html.

Восемь языков на одной странице; нужный выбирается по языку браузера или по
якорю вида #ru. Сделано так же, как в ~/Developer/toshas-farm-legal, чтобы
обе страницы поддерживались одинаково.
"""
import html
import json
import os

EMAIL = "vladislava.bogaturova@gmail.com"
DEV = "Vladyslava Ostapchuk"
UPDATED = "2026-10-10"
EULA = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"
APP = "Wow Intermittent fasting"

LANGS = ["en", "ru", "uk", "pl", "es", "ja", "ko", "zh"]
NAMES = {
    "en": "English",
    "ru": "Русский",
    "uk": "Українська",
    "pl": "Polski",
    "es": "Español",
    "ja": "日本語",
    "ko": "한국어",
    "zh": "中文",
}

T = json.load(open(os.path.join(os.path.dirname(__file__), "i18n.json"), encoding="utf-8"))

# Цвета взяты из самого приложения: фон экранов #e4f3fc, акцент #975712.
CSS = """
:root{--accent:#975712;--ink:#465452;--cream:#e4f3fc;--bg:#fff;--fg:#2b2a28}
@media (prefers-color-scheme:dark){:root{--bg:#161d21;--fg:#e9eff2;--cream:#222d33;--ink:#cfe0e6}}
*{box-sizing:border-box}
/* Длинные слова вроде «конфиденциальности» иначе вылезают за край на телефоне. */
body{margin:0;font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--fg);overflow-wrap:break-word}
header{background:var(--accent);color:#fff;padding:20px 16px}
header .in,main{max-width:760px;margin:0 auto}
header h1{margin:0;font-size:26px}
header p{margin:4px 0 0;opacity:.95}
.top{display:flex;gap:14px;flex-wrap:wrap;font-size:15px;margin-top:10px}
.top a{color:#fff}
nav.lang{display:flex;flex-wrap:wrap;gap:6px;margin:16px 0}
nav.lang a{padding:4px 10px;border-radius:14px;background:var(--cream);color:var(--accent);text-decoration:none;font-size:14px;border:1px solid var(--accent)}
nav.lang a.on{background:var(--accent);color:#fff}
main{padding:8px 16px 48px}
h2{color:var(--accent);margin:28px 0 6px;font-size:20px}
section.l h1{color:var(--accent)}
a{color:var(--accent)}
@media (prefers-color-scheme:dark){h2,section.l h1,a,nav.lang a{color:#f0b877}nav.lang a.on{color:#161d21;background:#f0b877}.top a{color:#fff}}
section.l{display:none}
section.l.on{display:block}
footer{max-width:760px;margin:0 auto;padding:0 16px 32px;font-size:14px;opacity:.75}
"""

JS = """
(function(){var L=%s;var q=(location.hash||'').replace('#','');
function pick(){if(L.indexOf(q)>=0)return q;var n=(navigator.languages||[navigator.language||'en']);
for(var i=0;i<n.length;i++){var c=String(n[i]).toLowerCase().slice(0,2);if(L.indexOf(c)>=0)return c;}return 'en';}
function show(c){document.documentElement.lang=c;document.querySelectorAll('section.l').forEach(function(s){s.classList.toggle('on',s.id==='l-'+c)});
document.querySelectorAll('nav.lang a').forEach(function(a){a.classList.toggle('on',a.dataset.l===c)});}
document.querySelectorAll('nav.lang a').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();history.replaceState(null,'','#'+a.dataset.l);show(a.dataset.l)})});
show(pick());})();
""" % json.dumps(LANGS)


def e(s):
    return html.escape(s, quote=False)


def page(kind):
    title_key = {
        "privacy": "privacy_title",
        "terms": "terms_title",
        "support": "support_title",
        "index": "home_title",
    }[kind]
    nav = "".join(f'<a href="#{c}" data-l="{c}">{NAMES[c]}</a>' for c in LANGS)
    contact = lambda d: (  # noqa: E731
        f"<h2>{e(d['contact_h'])}</h2>"
        f"<p>{e(d['contact'])} <a href=\"mailto:{EMAIL}\">{EMAIL}</a></p>"
    )

    secs = []
    for c in LANGS:
        d = T[c]
        body = []
        if kind == "privacy":
            body.append(f"<p><em>{e(d['updated'])}: {UPDATED}</em></p>")
            for k in ["p1", "p2", "p3", "p4", "p5", "p6"]:
                body.append(f"<h2>{e(d[k + '_h'])}</h2><p>{e(d[k])}</p>")
            body.append(contact(d) + f"<p>{e(DEV)}</p>")
        elif kind == "terms":
            body.append(f"<p><em>{e(d['updated'])}: {UPDATED}</em></p>")
            body.append(f"<h2>{e(d['t1_h'])}</h2><p>{e(d['t1'])} <a href=\"{EULA}\">{EULA}</a></p>")
            for k in ["t2", "t3", "t4", "t5"]:
                body.append(f"<h2>{e(d[k + '_h'])}</h2><p>{e(d[k])}</p>")
            body.append(contact(d) + f"<p>{e(DEV)}</p>")
        elif kind == "support":
            body.append(f"<p>{e(d['s_intro'])}</p>")
            body.append(contact(d))
            for k in ["s1", "s2", "s3"]:
                body.append(f"<h2>{e(d[k + '_h'])}</h2><p>{e(d[k])}</p>")
        else:
            body.append(f"<p>{e(d['home_text'])}</p>")
            body.append(
                "<ul>"
                f"<li><a href=\"privacy.html#{c}\">{e(d['privacy_title'])}</a></li>"
                f"<li><a href=\"terms.html#{c}\">{e(d['terms_title'])}</a></li>"
                f"<li><a href=\"support.html#{c}\">{e(d['support_title'])}</a></li>"
                "</ul>"
            )
        secs.append(
            f'<section class="l" id="l-{c}" lang="{c}">'
            f"<h1>{e(d[title_key])}</h1>{''.join(body)}</section>"
        )

    links = (
        '<div class="top"><a href="index.html">Home</a><a href="privacy.html">Privacy</a>'
        '<a href="terms.html">Terms</a><a href="support.html">Support</a></div>'
    )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(APP)}</title><meta name="robots" content="index,follow"><style>{CSS}</style></head><body>
<header><div class="in"><h1>⏱ {e(APP)}</h1><p>{e(DEV)}</p>{links}</div></header>
<main><nav class="lang">{nav}</nav>{''.join(secs)}</main>
<footer>© 2026 {e(DEV)}</footer><script>{JS}</script></body></html>"""


for kind, fn in [
    ("privacy", "privacy.html"),
    ("terms", "terms.html"),
    ("support", "support.html"),
    ("index", "index.html"),
]:
    path = os.path.join(os.path.dirname(__file__), fn)
    open(path, "w", encoding="utf-8").write(page(kind))
print("built", len(LANGS), "languages")
