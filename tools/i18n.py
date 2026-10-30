"""Spanish version of the English site.

The English pages are the source. Every visible text (and alt/aria-label/placeholder/title)
is looked up in tools/i18n/es.json and the page is written again under /es/.

  python3 tools/i18n.py missing   # list English texts that still need a translation
  python3 tools/i18n.py build     # write site/es/... and assets/pieces-es.json

Run tools/build_pages.py first; this script also adds the EN / ES switch to every page.
"""
import html as htmllib, json, os, re, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')
MAP_FILE = os.path.join(HERE, 'i18n', 'es.json')
ATTRS = ('alt', 'aria-label', 'placeholder', 'title', 'content', 'data-fy-open')
SKIP_TAGS = {'script', 'style'}
SKIP_PAGES = {'/en/ask/',  # redirect to "Built for you", English only
              '/en/working-notes/order-entry-simulator/'}  # English only for now; /es/ redirects to it

# Spanish paths and anchors, so links and sources read in Spanish
SLUGS = {'clients': 'clientes', 'construction': 'construccion', 'consumer-goods': 'gran-consumo', 'public-agency': 'sector-publico',
         'hospitality': 'hosteleria', 'manufacturing': 'industria', 'solutions': 'soluciones', 'how-we-work': 'como-trabajamos',
         'working-notes': 'mesa-de-trabajo', 'reading-is-not-recording': 'leer-no-es-registrar', 'merging-contacts': 'fusionar-contactos',
         'payment-or-revenue': 'cobro-o-ingreso', 'examples': 'ejemplos', 'from-document-to-record': 'del-documento-al-registro',
         'crm-with-context': 'un-crm-que-conserva-la-historia', 'reports-in-context': 'informes-con-contexto', 'team': 'equipo',
         'contact': 'contacto', 'for-you': 'para-ti'}
ANCHORS = {'assistants': 'asistentes', 'automation': 'automatizacion', 'integrations': 'integraciones'}


def es_path(en_path):
    """/en/clients/construction/#x -> /es/clientes/construccion/#x (query strings are kept as they are)."""
    m = re.match(r'/en(/[^?#]*)?(\?[^#]*)?(#.*)?$', en_path)
    path, query, frag = (m.group(1) or '/'), (m.group(2) or ''), (m.group(3) or '')
    path = '/'.join(SLUGS.get(seg, seg) for seg in path.split('/'))
    if frag:
        frag = '#' + ANCHORS.get(frag[1:], SLUGS.get(frag[1:], frag[1:]))
    return '/es' + path + query + frag


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


class Texts(HTMLParser):
    """Collect translatable texts in document order."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
        for k, v in attrs:
            if k in ATTRS and v and norm(v) and not (k == 'content' and tag != 'meta'):
                self.out.append(norm(v))

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and norm(data) and re.search(r'[A-Za-z]', data):
            self.out.append(norm(data))


def texts(html):
    p = Texts()
    p.feed(html)
    return p.out


def en_pages():
    for root, _dirs, files in os.walk(os.path.join(SITE, 'en')):
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(root, f)


def load_map():
    return json.load(open(MAP_FILE)) if os.path.exists(MAP_FILE) else {}


def page_path(fp):
    rel = '/' + os.path.relpath(fp, SITE).replace(os.sep, '/')
    return rel[:-len('index.html')] if rel.endswith('index.html') else rel


# ---------------------------------------------------------------- language switch on every page
def with_switch(html, en_path, es_path, current):
    nav = (f'<nav class="language" aria-label="Language">'
           f'<a lang="en" hreflang="en" href="{en_path}" aria-current="{str(current == "en").lower()}">EN</a><span aria-hidden="true">/</span>'
           f'<a lang="es" hreflang="es" href="{es_path}" aria-current="{str(current == "es").lower()}">ES</a></nav>')
    html = re.sub(r'<nav class="language".*?</nav>', '', html, flags=re.S)
    return html.replace('<button type="button" class="menu-toggle"', nav + '<button type="button" class="menu-toggle"', 1)


def with_alternates(html, en_path, es_path):
    html = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">', '', html)
    alt = (f'<link rel="alternate" hreflang="en" href="https://almaintel.ai{en_path}">'
           f'<link rel="alternate" hreflang="es" href="https://almaintel.ai{es_path}">'
           f'<link rel="alternate" hreflang="x-default" href="https://almaintel.ai{en_path}">')
    return re.sub(r'(<link rel="canonical"[^>]*>)', r'\1' + alt, html, count=1)


# ---------------------------------------------------------------- translate one page
def translate(html, tmap, missing):
    def tr(text):
        key = norm(htmllib.unescape(text))
        if not key or not re.search(r'[A-Za-z]', key):
            return text
        if key in tmap:
            lead = text[:len(text) - len(text.lstrip())]
            trail = text[len(text.rstrip()):]
            return lead + htmllib.escape(tmap[key], quote=False) + trail
        missing.add(key)
        return text

    out, i = [], 0
    for m in re.finditer(r'<(script|style)\b.*?</\1>|<[^>]+>', html, flags=re.S | re.I):
        out.append(tr(html[i:m.start()]))
        tag = m.group(0)
        if not tag.lower().startswith(('<script', '<style')):
            def attr(a):
                name, quote, val = a.group(1), a.group(2), a.group(3)
                key = norm(htmllib.unescape(val))
                if name == 'content' and not tag.startswith('<meta'):
                    return a.group(0)
                if key in tmap:
                    return f'{name}={quote}{htmllib.escape(tmap[key])}{quote}'
                if key and re.search(r'[A-Za-z]{3}', key) and name != 'content':
                    missing.add(key)
                return a.group(0)
            tag = re.sub(r'\b(' + '|'.join(ATTRS) + r')=(["\'])(.*?)\2', attr, tag)
        out.append(tag)
        i = m.end()
    out.append(tr(html[i:]))
    return ''.join(out)


def to_es_links(html):
    html = re.sub(r'(href|action)="(/en/[^"]*)"', lambda m: f'{m.group(1)}="{es_path(m.group(2))}"', html)
    html = re.sub(r'(<link rel="canonical" href="https://almaintel\.ai)(/en/[^"]*)"', lambda m: f'{m.group(1)}{es_path(m.group(2))}"', html)
    html = re.sub(r'\bid="(' + '|'.join(list(ANCHORS) + list(SLUGS)) + r')"', lambda m: f'id="{ANCHORS.get(m.group(1), SLUGS.get(m.group(1)))}"', html)
    return html.replace('<html lang="en">', '<html lang="es">').replace('content="en_US"', 'content="es_ES"')


def build(check_only=False):
    tmap = load_map()
    missing = set()
    for fp in en_pages():
        en_path = page_path(fp)
        if en_path in SKIP_PAGES:
            continue
        es_url = es_path(en_path)
        src = open(fp).read()
        src = with_alternates(with_switch(src, en_path, es_url, 'en'), en_path, es_url)
        if not check_only:
            open(fp, 'w').write(src)
        es = translate(src, tmap, missing)
        es = with_alternates(with_switch(to_es_links(es), en_path, es_url, 'es'), en_path, es_url)
        es = es.replace('/assets/pieces.json', '/assets/pieces-es.json')
        if not check_only:
            out = os.path.join(SITE, es_url.strip('/'), 'index.html') if es_url.endswith('/') else os.path.join(SITE, es_url.strip('/'))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w').write(es)
    # Pieces for the Spanish "Built for you" page
    pieces = json.load(open(os.path.join(SITE, 'assets', 'pieces.json')))
    es_pieces = {}
    for pid, p in pieces.items():
        es_pieces[pid] = dict(p, html=to_es_links(translate(p['html'], tmap, missing)),
                              source=tmap.get(p['source'], p['source']), label=tmap.get(p['label'], p['label']),
                              url=es_path(p['url']))
        for k in ('source', 'label'):
            if p[k] not in tmap:
                missing.add(p[k])
    if not check_only:
        json.dump(es_pieces, open(os.path.join(SITE, 'assets', 'pieces-es.json'), 'w'), ensure_ascii=False)
    return sorted(missing)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'build'
    todo = build(check_only=(cmd == 'missing'))
    if cmd == 'missing':
        json.dump(todo, open(os.path.join(HERE, 'i18n', 'es-missing.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'{len(todo)} texts without translation' + (' (see tools/i18n/es-missing.json)' if cmd == 'missing' else ''))
