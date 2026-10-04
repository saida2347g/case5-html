"""Генерация автономной HTML-страницы об ООО «Веб-Центр». Python 3.9+."""
import argparse
import base64
import html
import json
from pathlib import Path

TITLE = 'Наименование организации на базе, которой Вы проходите практическую подготовку'
SERVICES = [
    ('01', 'Разработка сайтов', 'Корпоративные сайты, интернет-магазины и B2B-порталы.'),
    ('02', 'Поисковое продвижение', 'Оптимизация сайтов и повышение видимости в поисковых системах.'),
    ('03', 'Интернет-реклама', 'Настройка контекстной рекламы и продвижение в социальных сетях.'),
    ('04', 'Поддержка проектов', 'Техническое сопровождение, обновление и доработка сайтов.'),
    ('05', 'Автоматизация', 'Внедрение Битрикс24 и настройка взаимодействия с клиентами.'),
    ('06', 'Аналитика', 'Аудит сайтов и оценка результатов продвижения.'),
]
FONTS = ['Arial', 'Verdana', 'Georgia', 'Times New Roman', 'Trebuchet MS', 'Courier New']

CSS = '''
* {box-sizing:border-box} :root {--ink:#173133;--muted:#536767;--paper:#f5f4ef;--accent:#cae66b}
body {margin:0;background:var(--paper);color:var(--ink);font-family:var(--page-font);line-height:1.65}
a {color:inherit;text-underline-offset:4px} button,select {font:inherit}
.wrap {width:min(1120px,calc(100% - 40px));margin:auto}
header {padding:25px 0;border-bottom:1px solid #cdd3c8}
.nav {display:flex;justify-content:space-between;gap:20px;align-items:center;flex-wrap:wrap}
.brand {font-weight:700;font-size:24px;letter-spacing:-1px}.brand span {color:#64793a}
.tag,.eyebrow {font-size:12px;text-transform:uppercase;letter-spacing:2px}
.hero {padding:65px 0 45px;display:grid;grid-template-columns:1.5fr 1fr;gap:50px;align-items:end}
h1 {font-size:clamp(22px,3vw,34px);line-height:1.3;max-width:780px;font-weight:400;margin:20px 0}
.company {font-size:clamp(42px,7vw,78px);line-height:1.07;letter-spacing:-2px;font-weight:700;margin:20px 0}
.lead {font-size:18px;max-width:660px;color:var(--muted)}
.summary {background:var(--ink);color:white;padding:30px;border-radius:20px}.summary p {margin:0 0 20px}
.pill {display:inline-block;background:var(--accent);color:var(--ink);padding:6px 14px;border-radius:30px;font-size:13px}
.toolbar {border:1px solid #b9c5b3;border-radius:14px;padding:20px 24px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:20px 0 48px;background:#fff}
select {max-width:100%;padding:10px 14px;border:1px solid #738675;border-radius:8px;background:white;color:var(--ink)}
.status {font-size:13px;color:var(--muted);margin:0;width:100%}
section {margin-bottom:56px} h2 {font-size:30px;line-height:1.25;margin:0 0 24px}
.grid {display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card {padding:25px;background:#fff;border:1px solid #e1e4dc;border-radius:16px}
.num {font-size:13px;color:#64793a} h3 {font-size:20px;line-height:1.3;margin:15px 0 10px}.card p {margin:0;color:var(--muted)}
.details {display:grid;grid-template-columns:1fr 1fr;gap:32px}.panel {background:#e8eddf;padding:30px;border-radius:18px}
dl {margin:0}dt {font-size:13px;color:var(--muted);margin-top:18px}dt:first-child {margin-top:0}dd {margin:3px 0;overflow-wrap:anywhere}
.samples {display:grid;grid-template-columns:repeat(2,1fr);gap:16px}.sample {padding:22px;border-top:2px solid #839972;background:white;border-radius:0 0 12px 12px}
.sample p {font-size:21px;margin:10px 0}.sample small {color:var(--muted)}
footer {border-top:1px solid #cdd3c8;padding:25px 0 35px;color:var(--muted);font-size:13px}
:focus-visible {outline:3px solid #657e25;outline-offset:4px}
@media(max-width:760px){.hero,.details{grid-template-columns:1fr;gap:22px}.hero{padding-top:35px}.grid,.samples{grid-template-columns:1fr}.company{letter-spacing:-1px}.wrap{width:calc(100% - 28px)}}
@media print {.toolbar{display:none}body{background:white}.hero{padding-top:20px}.card,.panel,.summary{break-inside:avoid}a{color:inherit}}
'''


def generate(font='Arial', font_file=None):
    """Возвращает HTML; опциональный файл шрифта встраивается в data URI."""
    e = html.escape
    # JSON-экранирование подходит для строк CSS; знак < закрывает возможность </style>.
    css_font = json.dumps(font, ensure_ascii=False).replace('<', r'\3C ')
    face = ''
    if font_file:
        p = Path(font_file)
        formats = {'.woff2': ('font/woff2', 'woff2'), '.woff': ('font/woff', 'woff'), '.ttf': ('font/ttf', 'truetype'), '.otf': ('font/otf', 'opentype')}
        if p.suffix.lower() not in formats:
            raise ValueError('Нужен файл .woff2, .woff, .ttf или .otf')
        mime, fmt = formats[p.suffix.lower()]
        encoded = base64.b64encode(p.read_bytes()).decode('ascii')
        face = f'@font-face{{font-family:{css_font};src:url(data:{mime};base64,{encoded}) format("{fmt}");font-display:swap;}}'
    families = [font] + [f for f in FONTS if f != font][:5]
    options = ''.join(f'<option value="{e(f, quote=True)}">{e(f)}{" — основной" if i == 0 else ""}</option>' for i,f in enumerate(families))
    cards = ''.join(f'<article class="card"><span class="num">{n}</span><h3>{e(name)}</h3><p>{e(desc)}</p></article>' for n,name,desc in SERVICES)
    samples = ''.join(f'<article class="sample" style="font-family:{e(json.dumps(f), quote=True)}, serif"><small>{i+1:02d} / {e(f)}</small><p>Цифровые решения для бизнеса</p><small>Разработка · Продвижение · Автоматизация</small></article>' for i,f in enumerate(families))
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(TITLE)} — ООО «Веб-Центр»</title>
<style>{face}\n:root{{--page-font:{css_font},sans-serif}}\n{CSS}</style>
</head>
<body>
<header><div class="wrap nav"><div class="brand">Веб<span>•</span>Центр</div><span class="tag">Практическая подготовка / Кейс 05</span></div></header>
<main class="wrap">
<div class="hero"><div><span class="eyebrow">Знакомство с организацией</span><h1>{e(TITLE)}</h1><p class="company">ООО «Веб-Центр»</p><p class="lead">Разработка сайтов, интернет-маркетинг и автоматизация работы с клиентами.</p></div><aside class="summary"><span class="pill">Информационные технологии</span><h2 style="margin-top:22px">От сайта —<br>к развитию бизнеса</h2><p>Компания помогает организациям создавать цифровые продукты, привлекать клиентов и развивать присутствие в интернете.</p><a href="https://web-c.ru/">Официальный сайт ↗</a></aside></div>
<div class="toolbar"><label for="font-select">Шрифт страницы</label><select id="font-select">{options}</select><p id="font-status" class="status" aria-live="polite">Основной вариант: {e(font)}. Выберите другой шрифт для сравнения.</p></div>
<section aria-labelledby="services"><h2 id="services">Основные направления работы</h2><div class="grid">{cards}</div></section>
<section class="details" aria-label="Сведения об организации"><div class="panel"><h2>О компании</h2><dl><dt>Полное наименование</dt><dd>Общество с ограниченной ответственностью «Веб-Центр»</dd><dt>Организационно-правовая форма</dt><dd>Общество с ограниченной ответственностью</dd><dt>ИНН / ОГРН</dt><dd>3254006851 / 1073254000137</dd><dt>Направление деятельности</dt><dd>Информационные технологии и интернет-маркетинг</dd></dl></div><div class="panel"><h2>География и контакты</h2><dl><dt>Москва</dt><dd>Смоленский бульвар, д. 24, стр. 2</dd><dt>Брянск</dt><dd>ул. Фокина, д. 143</dd><dt>Санкт-Петербург</dt><dd>26-я линия Васильевского острова, д. 15, корп. 2</dd><dt>Связаться с компанией</dt><dd><a href="tel:88007076370">8 (800) 707-63-70</a><br><a href="mailto:mail@web-c.ru">mail@web-c.ru</a></dd></dl></div></section>
<section aria-labelledby="fonts"><h2 id="fonts">Один текст — шесть вариантов</h2><p>Основной шрифт и пять альтернатив для сравнения оформления.</p><div class="samples">{samples}</div></section>
</main>
<footer><div class="wrap">Учебная работа. Информация об организации: <a href="https://web-c.ru/about/">о компании</a> и <a href="https://web-c.ru/contacts/">контакты</a>. Дата подготовки: 04.10.2026.<br>Отображение системных шрифтов зависит от их наличия на устройстве.</div></footer>
<script>
const selector = document.getElementById('font-select');
selector.addEventListener('change', () => {{
  document.documentElement.style.setProperty('--page-font', JSON.stringify(selector.value) + ', sans-serif');
  document.getElementById('font-status').textContent = 'Выбран шрифт: ' + selector.value;
}});
</script>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'index.html')
    parser.add_argument('--font', default='Arial', help='Название основного шрифта')
    parser.add_argument('--font-file', type=Path, help='Локальный файл основного шрифта для встраивания')
    args = parser.parse_args()
    if not args.font.strip():
        parser.error('Название шрифта не должно быть пустым')
    try:
        result = generate(args.font, args.font_file)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding='utf-8')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Ошибка: {exc}\n')
    print(f'Создана страница: {args.output.resolve()}')

if __name__ == '__main__':
    main()
