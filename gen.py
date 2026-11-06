#!/usr/bin/env python3
"""Генератор статичного сайту «Лад». Запуск: python3 gen.py [BASE_URL]"""
import json, os, sys, html, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import EXTRA, ARTICLES

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'https://example.com').rstrip('/')
LANG = sys.argv[2] if len(sys.argv) > 2 else 'uk'
RU = LANG == 'ru'
PFX = '/ru' if RU else ''
SITE = BASE + PFX
RP = '../' if RU else ''   # глибше на рівень — шлях до спільних файлів (css, шрифти)
CUR = '/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build', 'ru' if RU else '')
TG = 'https://t.me/yadhtl'
BRAND = 'Лад'
TODAY = datetime.date.today().isoformat()

M = [
 dict(key='monopay', slug='integratsiya-monopay-1c-bas', group='Оплати', card='MonoPay', price='7 000 грн', amount=7000,
  h1='Інтеграція MonoPay з 1С і BAS',
  desc='Рахунок monobank із замовлення в один клік, автоматичний статус оплати, повернення коштів з 1С. Модуль-розширення, встановлення під ключ.',
  short='Рахунки на оплату з замовлення, статуси, повернення та Покупка частинами — прямо в обліку.',
  lead='Менеджер створює рахунок на оплату прямо із замовлення, клієнт платить карткою, а оплата сама падає в облік і прив’язується до замовлення.',
  pains=['Посилання на оплату робиться вручну в кабінеті банку','Оплати звіряються з замовленнями руками, по сумі й прізвищу','Повернення коштів клієнту — окрема морока і в банку, і в обліку'],
  features=['Рахунок monobank із замовлення в один клік','Посилання на оплату клієнту в месенджер','Статус оплати оновлюється сам, без звірок','Оплата автоматично проводиться і прив’язується до замовлення','Повернення коштів з обліку, повне або часткове','Підтримка «Покупки частинами» monobank']),
 dict(key='novapay', slug='novapay-1c', group='Оплати', card='NovaPay', price='8 000 грн', amount=8000,
  h1='NovaPay: накладений платіж Нової Пошти в 1С',
  desc='Автоматичне завантаження виписок і реєстрів NovaPay в 1С і BAS, рознесення накладеного платежу по замовленнях за ТТН.',
  short='Виписки й реєстри накладеного платежу Нової Пошти автоматично рознесені по замовленнях.',
  lead='Виписки й реєстри NovaPay завантажуються в облік і розносяться по замовленнях за номером ТТН. Без Excel і ручного рознесення.',
  pains=['Реєстри накладеного платежу розносяться вручну','Важко зрозуміти, яке замовлення оплачене, а яке ні','Комісії NovaPay губляться у звітах'],
  features=['Завантаження виписок і реєстрів NovaPay','Рознесення оплат по замовленнях за ТТН','Комісія NovaPay враховується окремо','Видно неоплачені й незнайдені посилки','Робота з кількома ФОП']),
 dict(key='privat', slug='pryvat24-zalyshky-fop-1c', group='Оплати', card='Приват24: залишки', price='3 500 грн', amount=3500,
  h1='Залишки Приват24 по кожному ФОП в 1С',
  desc='Баланси рахунків Приват24 по всіх ФОП прямо в 1С і BAS, з порівнянням із залишком в обліку.',
  short='Залишки на рахунках кожного ФОП поруч із даними обліку, без входу в банк.',
  lead='Баланси рахунків у Приват24 по всіх ваших ФОП видно прямо в обліку — поруч із тим, що показує 1С.',
  pains=['Щоб глянути залишки, треба заходити в банк під кожен ФОП','Розбіжності між банком і обліком знаходяться запізно','Немає однієї картини грошей по всіх ФОП'],
  features=['Залишки рахунків Приват24 по кожному ФОП','Порівняння з залишком у 1С','Одна таблиця на всі ФОП','Оновлення без входу в банк']),
 dict(key='novaposhta', slug='nova-poshta-1c', group='Доставка', card='Нова Пошта', price='5 000 грн', amount=5000,
  h1='Нова Пошта в 1С: відділення, претензії, нагадування',
  desc='Актуальні відділення й поштомати Нової Пошти в 1С і BAS, претензії в один клік, нагадування клієнтам про посилку на зберіганні.',
  short='Відділення й поштомати в обліку, претензії в один клік, нагадування клієнтам про зберігання.',
  lead='Довідник відділень і поштоматів завжди актуальний, претензія по втраченій посилці — в один клік, а клієнт отримує нагадування, що посилка чекає на відділенні.',
  pains=['Застарілі відділення в замовленнях','Претензії по втрачених посилках пишуться вручну','Посилки повертаються, бо клієнт забув забрати'],
  features=['Актуальні відділення й поштомати НП в обліку','Претензія по посилці в один клік','Нагадування клієнту про посилку на зберіганні','Робота з кількома ФОП-відправниками']),
 dict(key='hub', slug='obmin-saytu-z-1c', group='Сайт ↔ облік', card='Хаб обміну', price='від 15 000 грн', amount=15000,
  h1='Обмін сайту з 1С: замовлення, статуси, клієнти',
  desc='Двосторонній обмін інтернет-магазину з 1С і BAS: замовлення, статуси, клієнти, власне API для ботів і CRM.',
  short='Замовлення, статуси, клієнти й API між сайтом та обліком в обидва боки.',
  lead='Замовлення з сайту одразу в обліку, статуси з обліку — на сайті й у клієнта. Плюс API, щоб підключати бота, CRM чи інші сервіси.',
  pains=['Замовлення з сайту переносяться в облік руками','Клієнт не бачить актуального статусу','Кожна нова інтеграція — окремий костиль'],
  features=['Замовлення з сайту в облік автоматично','Статуси з обліку назад на сайт','Клієнти й історія замовлень синхронізовані','Власне API для ботів, CRM та сервісів','Журнал обміну: видно, що і коли пройшло']),
 dict(key='stock', slug='zalyshky-z-1c-na-sayt', group='Сайт ↔ облік', card='Залишки на сайт', price='6 000 грн', amount=6000,
  h1='Залишки з 1С на сайт автоматично',
  desc='Автоматичне вивантаження залишків з 1С і BAS на сайт інтернет-магазину без ручних файлів.',
  short='Наявність товару з обліку на сайті, автоматично й без вивантажень руками.',
  lead='Наявність товару на сайті береться з обліку. Немає товару — сайт це знає, з’явився — одразу доступний до замовлення.',
  pains=['Залишки на сайт вивантажуються руками','Клієнти замовляють те, чого вже немає','Сайт показує «немає», хоча товар на складі'],
  features=['Залишки з обліку на сайт за розкладом','Тільки потрібні склади й товари','Без ручних вивантажень і файлів','Працює з Bitrix, адаптується під інші платформи']),
 dict(key='supplier', slug='obmin-z-postachalnykom-api-1c', group='Постачальники', card='Обмін з постачальником', price='від 9 000 грн', amount=9000,
  h1='Обмін з постачальником по API з 1С',
  desc='Автоматична відправка замовлень постачальнику з 1С і BAS, його залишки й статуси назад в облік.',
  short='Замовлення постачальнику та його залишки через API, без дзвінків і таблиць.',
  lead='Замовлення постачальнику йде з обліку автоматично, а його залишки й відповіді повертаються назад. Без дзвінків, листів і таблиць.',
  pains=['Замовлення постачальнику складаються й відправляються вручну','Невідомо, чи є товар у постачальника','Прихідні накладні не сходяться з замовленням'],
  features=['Відправка замовлень постачальнику з обліку','Залишки постачальника в обліку','Статуси й відповіді постачальника назад','Журнал обміну з помилками','Адаптую під API вашого постачальника']),
 dict(key='generator', slug='heneratsiya-kharakterystyk-1c', group='Товари', card='Генератор характеристик', price='6 000 грн', amount=6000,
  h1='Генератор характеристик номенклатури в 1С',
  desc='Пакетне створення характеристик номенклатури в 1С і BAS з параметрів, пошук і злиття дублікатів.',
  short='Створює характеристики товару пакетом і прибирає дублікати.',
  lead='Створює характеристики товару пакетом із вибраних параметрів і знаходить дублікати, щоб у довіднику був порядок.',
  pains=['Характеристики заводяться по одній, годинами','Дублікати характеристик ламають залишки й звіти','Значення параметрів пишуться по-різному'],
  features=['Пакетне створення характеристик з параметрів','Без дублікатів: перевірка перед створенням','Пошук і злиття вже наявних дублів','Нормалізація значень параметрів']),
 dict(key='notify', slug='spovishchennya-viber-telegram-1c', group='Клієнти', card='Сповіщення Viber / Telegram', price='5 000 грн', amount=5000,
  h1='Сповіщення клієнтам у Viber і Telegram з 1С',
  desc='Автоматичні повідомлення клієнтам з 1С і BAS у Viber і Telegram: підтвердження замовлення, оплата, ТТН, нагадування.',
  short='Клієнт отримує статус, посилання на оплату й ТТН у месенджер автоматично.',
  lead='Клієнт отримує підтвердження замовлення, посилання на оплату, ТТН і нагадування в месенджер — автоматично, як тільки менеджер провів замовлення.',
  pains=['Менеджери пишуть клієнтам вручну','Клієнт не знає, де його замовлення, і дзвонить','Повідомлення забувають відправити'],
  features=['Повідомлення з обліку у Viber і Telegram','Підтвердження, оплата, ТТН — за статусами','Нагадування про повторне замовлення','Шаблони текстів під ваш бренд']),
 dict(key='fop', slug='rozpodil-zamovlen-fop-1c', group='Контроль', card='Контроль ФОП', price='9 000 грн', amount=9000,
  h1='Розподіл замовлень по ФОП і контроль лімітів у 1С',
  desc='Автоматичний вибір ФОП у замовленнях 1С і BAS, контроль лімітів і грошей по ФОП, звірки з постачальниками, доступи.',
  short='Розподіл замовлень по ФОП, ліміти, звірки з постачальниками, доступи для працівників.',
  lead='Облік сам підставляє правильний ФОП у замовлення, стежить за лімітами й допомагає звіряти розрахунки з постачальниками.',
  pains=['ФОП у замовленнях обирається вручну і з помилками','Ліміти ФОП легко перевищити непомітно','Звірки з постачальниками — цілий день роботи'],
  features=['Закріплення ФОП за постачальником','Заборона ФОП з автоматичною заміною','Контроль грошей і лімітів по кожному ФОП','Звірки з постачальниками','Доступи до функцій для кожного працівника']),
 dict(key='desk', slug='robochyy-stil-menedzhera-1c', group='Менеджери', card='Робочий стіл', price='18 000 грн', amount=18000,
  h1='Робочий стіл менеджера в 1С',
  desc='Один екран менеджера в 1С і BAS: пропущені дзвінки, дозамовлення, замовлення, посилки та статистика.',
  short='Один екран менеджера: дзвінки, дозамовлення, замовлення й посилки.',
  lead='Один зручний екран замість десятка форм: кому передзвонити, кому пора дозамовити, які замовлення горять і де посилки.',
  pains=['Менеджер стрибає між формами і губить клієнтів','Пропущені дзвінки й обіцянки передзвонити забуваються','Ніхто не нагадує клієнтам, що пора дозамовити'],
  features=['Картки клієнтів: пропущені, обіцяні, пора дозамовити','Список замовлень з фільтрами й швидким пошуком','Статуси посилок НП прямо в рядку','Статистика роботи менеджерів для власника','Працює на будь-якому екрані']),
 dict(key='ai', slug='ai-pomichnytsya-1c', group='AI', card='AI-помічниця', price='30 000 грн', amount=30000,
  h1='AI-помічниця для 1С',
  desc='AI-помічниця в 1С і BAS: питання до бази простою мовою, прихідні накладні з фото, підсумки дзвінків, розумний пошук.',
  short='Питання до бази простою мовою, накладні з фото, підсумки дзвінків, розумний пошук.',
  lead='Помічниця всередині обліку: відповідає на питання по базі простою мовою, заводить накладні з фото, підсумовує дзвінки клієнтів.',
  pains=['Щоб отримати цифру, треба просити програміста про звіт','Накладні постачальників набиваються вручну','Про що говорили з клієнтом по телефону — ніхто не пам’ятає'],
  features=['Питання до бази звичайною мовою','Прихідні накладні з фото документа','Підсумки дзвінків у замовленні','Розумний пошук по замовленнях і клієнтах','Працює через Telegram-групу команди']),
]

if RU:
    from content_ru import M_RU, EXTRA_RU, ARTICLES_RU, PHRASES
    M, EXTRA, ARTICLES = M_RU, EXTRA_RU, ARTICLES_RU
    PH = sorted(PHRASES.items(), key=lambda kv: -len(kv[0]))

e = html.escape
LOGO_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#C6F26B" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h5l3-7 3 14 3-7h2"/></svg>'
CHECK = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1E5E4E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
WARN = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#B4532A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 16.5v.5"/></svg>'

def head(title, desc, path, ld, root):
    global CUR
    CUR = path
    url = SITE + path
    root = RP + root if not root.startswith('http') else root
    return f'''<!doctype html>
<html lang="{'ru' if RU else 'uk'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="uk" href="{BASE}{path}">
<link rel="alternate" hreflang="ru" href="{BASE}/ru{path}">
<link rel="alternate" hreflang="x-default" href="{BASE}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{'ru_UA' if RU else 'uk_UA'}">
<meta name="theme-color" content="#16181D">
<meta name="google-site-verification" content="qIzzCrMqHk6QFRNcGPq2N3UUjU6E1_YZE65H0vHtTgA">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="preload" href="{root}fonts/manrope-cyrillic-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{root}fonts/unbounded-cyrillic-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
'''

def header(root, back=False):
    nav = (f'<a class="navlink" href="{root}">← Усі модулі</a>' if back else
           '<nav class="nav"><a href="#modules">Модулі</a><a href="#services">Послуги</a><a href="#how">Як працюємо</a><a href="statti/">Статті</a><a href="#contact">Контакти</a></nav>')
    sw = (f'<a class="lang" href="{BASE}{CUR}" hreflang="uk" lang="uk">UA</a>' if RU else f'<a class="lang" href="{BASE}/ru{CUR}" hreflang="ru" lang="ru">RU</a>')
    return f'<header class="wrap top"><a class="logo" href="{root}"><span class="mark">{LOGO_SVG}</span>{BRAND}</a><div class="navwrap">{nav}{sw}</div></header>\n'

def footer():
    return f'<footer class="foot"><div class="wrap">© {datetime.date.today().year} {BRAND} · Автоматизація e-commerce · <a href="{SITE}/statti/">Статті</a> · <a href="{TG}">Telegram @yadhtl</a></div></footer>\n</body>\n</html>\n'

def cta(title, text):
    return f'''<section class="dark" id="contact"><div class="wrap ctaband">
<div><h2 class="h2">{title}</h2><p class="muted">{text}</p></div>
<a class="btn lime" href="{TG}">Написати в Telegram @yadhtl</a>
</div></section>\n'''

def write(path, s):
    full = os.path.join(OUT, path.strip('/'), 'index.html') if path != '/' else os.path.join(OUT, 'index.html')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if RU:
        for a, b in PH:
            s = s.replace(a, b)
    open(full, 'w', encoding='utf-8').write(s)

ORG = {"@type": "Organization", "name": BRAND, "url": SITE + '/', "sameAs": [TG]}

# ---------- index ----------
cards = ''.join(f'''<a class="card" href="{m["slug"]}/"><span class="tag">{e(m["group"])}</span><h3>{e(m["card"])}</h3><p>{e(m["short"])}</p><span class="price"><b>{e(m["price"])}</b><small>разово</small></span></a>''' for m in M)
ld_index = {"@context": "https://schema.org", "@graph": [ORG,
    {"@type": "WebSite", "name": BRAND, "url": SITE + '/', "inLanguage": LANG},
    {"@type": "ItemList", "name": "Модулі автоматизації e-commerce для 1С і BAS",
     "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{SITE}/{m["slug"]}/', "name": m["h1"]} for i, m in enumerate(M)]}]}
idx = head('Автоматизація інтернет-магазину: модулі для 1С і BAS — ' + BRAND,
           'Готові модулі для 1С, BAS і CRM: MonoPay, NovaPay, Нова Пошта, обмін із сайтом і постачальниками, AI-помічниця. Разова оплата, встановлення під ключ.',
           '/', ld_index, '')
idx += header('')
idx += f'''<main>
<section class="wrap hero">
<div class="grow"><p class="kicker">Автоматизація e-commerce</p>
<h1>Оплати, доставка, сайт і облік — в одній системі, без ручної роботи</h1>
<p class="lead">Готові модулі для облікових систем (1С, BAS та інших) і CRM: MonoPay, NovaPay, Нова Пошта, обмін із сайтом і постачальниками, AI-помічниця. Перевірено щодня на реальному інтернет-магазині.</p>
<div class="row"><a class="btn dark" href="{TG}">Безкоштовна консультація</a><a class="btn ghost" href="#modules">Дивитись модулі</a></div></div>
<div class="stats"><div class="stat"><b>12</b><span>готових модулів</span></div><div class="stat"><b>1 раз</b><span>купуєте — і назавжди ваше</span></div><div class="stat lime wide"><b>600 грн/год</b><span>консультації і доробки під вас</span></div></div>
</section>
<section class="dark"><div class="wrap three">
<div><h3>Без ручного внесення</h3><p class="muted">Оплати, виписки, ТТН і статуси самі падають в облік.</p></div>
<div><h3>Працює без мене</h3><p class="muted">Встановив, налаштував, навчив — далі система живе сама.</p></div>
<div><h3>З реального бізнесу</h3><p class="muted">Кожен модуль народився з проблеми живого магазину, а не з ТЗ.</p></div>
</div></section>
<section class="wrap sec" id="modules"><h2 class="h2">Модулі</h2>
<p class="lead sm">Ціна разова: модуль ваш назавжди. Входить встановлення, налаштування, навчання та 30 днів виправлень. Ліцензія на одну базу.</p>
<div class="cards">{cards}</div>
<p class="note">Потрібен модуль під іншу облікову систему чи версію — адаптую, оцінка безкоштовна.</p></section>
<section class="wrap sec" id="services"><h2 class="h2">Послуги</h2><div class="grid4">
<div class="box lime"><h3>Консультація та оцінка</h3><p>Розбираємо задачу, кажу, що реально зробити, скільки годин і коштів.</p><b>600 грн/год</b></div>
<div class="box"><h3>Доробки під вас</h3><p>Нові функції, звіти, обробки, зміни в модулях. Спершу оцінка — потім робота.</p><b>600 грн/год</b></div>
<div class="box"><h3>Супровід модулів</h3><p>Банк чи пошта змінили API, оновили платформу — оновлю модуль і все перевірю.</p><b>за годинами</b></div>
<div class="box"><h3>Сайт і CRM</h3><p>Bitrix, Laravel, інтеграції сайту з обліком, CRM, ботами та розсилками.</p><b>від 600 грн/год</b></div>
</div></section>
<section class="white" id="how"><div class="wrap sec"><h2 class="h2">Як працюємо</h2><div class="grid4 steps">
<div><i>01</i><h3>Дзвінок 30 хв</h3><p>Яка у вас система, що болить, що хочете автоматизувати. Безкоштовно.</p></div>
<div><i>02</i><h3>Демо наживо</h3><p>Показую модуль у роботі через демонстрацію екрана, до покупки.</p></div>
<div><i>03</i><h3>Встановлення</h3><p>Сам ставлю віддалено на копію, потім на робочу базу, налаштовую і навчаю.</p></div>
<div><i>04</i><h3>Працює</h3><p>30 днів виправлень включено. Далі — доробки й супровід за годинами, коли треба.</p></div>
</div></div></section>
<section class="wrap sec"><div class="box who"><div><p class="kicker">Хто це робить</p><h2 class="h2">Не агенція. Один розробник — від дзвінка до підтримки</h2></div>
<div><p>Кожен модуль я зробив сам для живого магазину і щодня бачу, як він працює.</p><p>Ви говорите з тим, хто пише код, а не з менеджером агенції. Сам ставлю, сам навчаю, сам підтримую.</p></div></div></section>
<section class="wrap sec case"><div><p class="kicker">Перевірено в роботі</p><h2 class="h2">Не демо-стенд, а щоденна робота</h2><p class="lead sm">Кожен модуль спершу місяцями працює в живому інтернет-магазині: оплати, накладений платіж, обмін із сайтом і постачальниками, AI-помічниця для менеджерів. Лише потім — на продаж.</p></div>
<div class="stats"><div class="stat"><b>12</b><span>модулів у щоденній роботі</span></div><div class="stat"><b>30 днів</b><span>виправлень після встановлення — у ціні</span></div></div></section>
</main>
'''
idx += cta('Розкажіть, що болить', 'Напишіть, яка у вас система і що хочете автоматизувати. Відповім протягом дня з рішенням і оцінкою.')
idx += footer()
write('/', idx)

GEN_FAQ = [('Чи запрацює на моїй конфігурації?', 'Модуль ставиться як розширення, без зміни основної конфігурації. Якщо у вас інша версія чи доопрацьована база — адаптую, оцінка безкоштовна.'),
           ('А якщо сервіс змінить API?', 'Оновлю модуль за годинами, 600 грн/год. Зазвичай це година-дві роботи.'),
           ('Можна доробити під мої процеси?', 'Так. Спершу оцінюю, скільки годин займе, потім роблю. 600 грн/год.')]

# ---------- module pages ----------
for m in M:
    path = f'/{m["slug"]}/'
    x = EXTRA[m["key"]]
    faq = x["faq"] + GEN_FAQ
    art = [a for a in ARTICLES if a["module"] == m["key"]]
    ld = {"@context": "https://schema.org", "@graph": [ORG,
        {"@type": "Service", "name": m["h1"], "description": m["desc"], "provider": {"@type": "Organization", "name": BRAND},
         "areaServed": "UA", "offers": {"@type": "Offer", "price": m["amount"], "priceCurrency": "UAH"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Модулі", "item": SITE + '/'},
            {"@type": "ListItem", "position": 2, "name": m["card"], "item": SITE + path}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    s = head(f'{m["h1"]} — {m["price"]} | {BRAND}', m["desc"], path, ld, '../')
    s += header('../', back=True)
    pains = ''.join(f'<li>{WARN}<span>{e(p)}</span></li>' for p in m["pains"])
    feats = ''.join(f'<li>{CHECK}<span>{e(f)}</span></li>' for f in m["features"])
    others = ''.join(f'<a href="../{o["slug"]}/">{e(o["card"])}</a>' for o in M if o is not m)
    how = ''.join(f'<li>{e(t)}</li>' for t in x["how"])
    need = ''.join(f'<li>{CHECK}<span>{e(t)}</span></li>' for t in x["need"])
    faqhtml = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    arthtml = ''.join(f'<section class="wrap sec"><a class="artlink" href="../statti/{a["slug"]}/"><span class="tag">Стаття</span><b>{e(a["title"])}</b></a></section>' for a in art)
    s += f'''<main>
<section class="wrap hero">
<div class="grow"><p class="kicker">{e(m["group"])}</p><h1>{e(m["h1"])}</h1><p class="lead">{e(m["lead"])}</p></div>
<aside class="pricebox"><span class="muted">Разова оплата, модуль ваш назавжди</span><b>{e(m["price"])}</b><span>Встановлення, налаштування, навчання і 30 днів виправлень уже в ціні.</span><a class="btn lime" href="{TG}">Подивитись демо</a></aside>
</section>
<section class="white"><div class="wrap sec"><h2 class="h2">Що зараз забирає час</h2><ul class="list pains">{pains}</ul></div></section>
<section class="wrap sec"><h2 class="h2">Що робить модуль</h2><ul class="list feats">{feats}</ul></section>
<section class="wrap sec"><h2 class="h2">Як це працює</h2><ol class="flow">{how}</ol></section>
<section class="wrap sec"><h2 class="h2">Що потрібно для підключення</h2><ul class="need">{need}</ul></section>
<section class="wrap sec"><div class="box lime grid3">
<div><i>01</i><h3>Демо наживо</h3><p>Показую модуль у роботі через демонстрацію екрана, до оплати.</p></div>
<div><i>02</i><h3>Встановлення</h3><p>Сам ставлю віддалено: спершу на копію бази, потім на робочу.</p></div>
<div><i>03</i><h3>Навчання</h3><p>Показую вашим людям, як працювати, і 30 днів виправляю, якщо щось не так.</p></div>
</div></section>
<section class="wrap sec"><h2 class="h2">Питання</h2>{faqhtml}</section>{arthtml}
<section class="wrap sec"><h2 class="h2 sm">Інші модулі</h2><div class="others">{others}</div></section>
</main>
'''
    s += cta('Покажу, як це працює, за 15 хвилин', 'Напишіть у Telegram, яка у вас система, — домовимось про демо.')
    s += footer()
    write(path, s)

# ---------- articles ----------
MB = {m["key"]: m for m in M}
for a in ARTICLES:
    path = f'/statti/{a["slug"]}/'
    mod = MB[a["module"]]
    ld = {"@context": "https://schema.org", "@graph": [ORG,
        {"@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": a["date"], "dateModified": a["date"],
         "inLanguage": LANG, "author": {"@type": "Organization", "name": BRAND, "url": SITE + '/'},
         "publisher": {"@type": "Organization", "name": BRAND}, "mainEntityOfPage": SITE + path},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Головна", "item": SITE + '/'},
            {"@type": "ListItem", "position": 2, "name": "Статті", "item": SITE + '/statti/'},
            {"@type": "ListItem", "position": 3, "name": a["title"], "item": SITE + path}]}]}
    s = head(f'{a["title"]} | {BRAND}', a["desc"], path, ld, '../../')
    s += header('../../', back=True)
    body = ''.join(f'<h2>{e(h)}</h2>' + ''.join(f'<p>{e(p)}</p>' for p in ps) for h, ps in a["body"])
    s += f'''<main><article class="wrap sec prose">
<p class="kicker"><a href="../">Статті</a> · {a["date"][8:10]}.{a["date"][5:7]}.{a["date"][:4]}</p>
<h1>{e(a["title"])}</h1><p class="lead">{e(a["lead"])}</p>
{body}
<div class="box lime artcta"><h3>Готовий модуль: {e(mod["h1"])}</h3><p>{e(mod["short"])} {e(mod["price"])} разово, встановлення під ключ.</p><a class="btn dark" href="../../{mod["slug"]}/">Детальніше про модуль</a></div>
</article></main>
'''
    s += cta('Є схожа задача?', 'Напишіть у Telegram, яка у вас система, — підкажу, як це зробити.')
    s += footer()
    write(path, s)

ld = {"@context": "https://schema.org", "@graph": [ORG, {"@type": "CollectionPage", "name": "Статті про автоматизацію інтернет-магазину", "url": SITE + '/statti/', "inLanguage": LANG}]}
s = head(f'Статті: автоматизація інтернет-магазину з 1С і BAS | {BRAND}', 'Практичні інструкції: оплата monobank у 1С, накладений платіж NovaPay, залишки на сайт, Нова Пошта в обліку.', '/statti/', ld, '../')
s += header('../', back=True)
items = ''.join(f'<a class="card" href="{a["slug"]}/"><span class="tag">Інструкція</span><h3>{e(a["title"])}</h3><p>{e(a["desc"])}</p></a>' for a in ARTICLES)
s += f'<main><section class="wrap hero"><div class="grow"><p class="kicker">Статті</p><h1>Автоматизація інтернет-магазину: практичні інструкції</h1><p class="lead">Як прибрати ручну роботу з оплатами, доставкою й обміном із сайтом у 1С та BAS.</p></div></section><section class="wrap sec"><div class="cards">{items}</div></section></main>\n'
s += cta('Хочете так само у себе?', 'Напишіть у Telegram, яка у вас система.')
s += footer()
write('/statti/', s)

if RU:
    print('ok ru ->', SITE)
    sys.exit(0)

# ---------- sitemap, robots, 404, favicon ----------
urls = ['/'] + [f'/{m["slug"]}/' for m in M] + ['/statti/'] + [f'/statti/{a["slug"]}/' for a in ARTICLES]
def alt(u):
    return (f'<xhtml:link rel="alternate" hreflang="uk" href="{BASE}{u}"/><xhtml:link rel="alternate" hreflang="ru" href="{BASE}/ru{u}"/>'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{u}"/>')
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + ''.join(
    f'  <url><loc>{BASE}{p}{u}</loc><lastmod>{TODAY}</lastmod>{alt(u)}</url>\n' for u in urls for p in ('', '/ru')) + '</urlset>\n'
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
open(os.path.join(OUT, 'favicon.svg'), 'w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#16181D"/><path d="M6 16h6l4-9 4 18 4-9h2" fill="none" stroke="#C6F26B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
nf = head('Сторінку не знайдено — ' + BRAND, 'Сторінку не знайдено.', '/404.html', ORG | {"@context": "https://schema.org"}, SITE + '/')
nf = nf.replace('<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"')
nf += header(SITE + '/') + f'<main class="wrap sec"><h1>Сторінку не знайдено</h1><p class="lead"><a href="{BASE}/">На головну</a></p></main>' + footer()
open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(nf)
INDEXNOW = '6f1c2b9e4d7a4e0f9b3c8a51d2e7f640'
open(os.path.join(OUT, INDEXNOW + '.txt'), 'w').write(INDEXNOW)
print('ok', len(urls), 'pages ->', BASE)
