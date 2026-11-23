"""Статті 23.11.2026 (Claude Batch, Opus: чернетка → редактор / факт-чек). Дані — claude_arts.json.
Підключаються в кінці content.py / content_ru.py через add_claude_arts(ARTICLES, lang)."""
import json, os

_F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'claude_arts.json')


def add_claude_arts(articles, lang):
    if not os.path.exists(_F):
        return
    have = {a['slug'] for a in articles}
    key = 'uk' if lang == 'uk' else 'ru'
    for it in json.load(open(_F, encoding='utf-8')):
        if it['slug'] in have:
            continue
        a = it[key]
        articles.append(dict(slug=it['slug'], module=it['module'], date=it['date'], title=a['title'], desc=a['desc'],
                             lead=a['lead'], body=[(h, list(ps)) for h, ps in a['body']], faq=[(q, ans) for q, ans in a.get('faq', [])]))


_R = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'claude_refresh.json')


def refresh_arts(articles, lang):
    """23.11: старі короткі статті, розширені Claude (slug і модуль ті самі)."""
    if not os.path.exists(_R):
        return
    key = 'uk' if lang == 'uk' else 'ru'
    upd = {it['slug']: it[key] for it in json.load(open(_R, encoding='utf-8'))}
    for a in articles:
        n = upd.get(a['slug'])
        if n:
            a.update(title=n['title'], desc=n['desc'], lead=n['lead'], body=[(h, list(ps)) for h, ps in n['body']],
                     faq=[(q, ans) for q, ans in n.get('faq', [])])


_MG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'claude_modules.json')


def module_guide(key, lang):
    """23.11: додатковий блок-гайд і FAQ для сторінки модуля (Claude). Нема — None."""
    if not os.path.exists(_MG):
        return None
    return json.load(open(_MG, encoding='utf-8')).get(key, {}).get('uk' if lang == 'uk' else 'ru')
