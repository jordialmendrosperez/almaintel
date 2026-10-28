"""Last build step: analytics, search engines and AI search.

Adds Google Analytics to every page, structured data (organization, FAQ), and writes
robots.txt, sitemap.xml and llms.txt. Safe to run again: it replaces what it added before.

  python3 tools/finalize.py
"""
import datetime, html as htmllib, json, os, re

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
DOMAIN = 'https://almaintel.ai'
GA_ID = 'G-YEQSJ7XVV3'
TODAY = datetime.date.today().isoformat()
# Pages that are not useful in search results
NO_INDEX = re.compile(r'^/(index\.html|404\.html|en/404\.html|es/404\.html|en/ask/|en/for-you/|es/para-ti/)$')

GA = (f'<!-- ga --><script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
      f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script><!-- /ga -->")

ORG = {
    '@context': 'https://schema.org', '@type': 'Organization', '@id': f'{DOMAIN}/#organization',
    'name': 'Alma Intel', 'url': f'{DOMAIN}/', 'email': 'hello@almaintel.ai',
    'logo': f'{DOMAIN}/logos/Alma%20Intel%20-%20Iso%20-%201.png',
    'description': 'Alma Intel is an applied AI firm for mid-market companies (20 to 500 people). We work inside the business, learn how it runs and build AI systems that read, check and prepare the work teams do by hand, in the tools they already use, with people approving what goes out.',
    'founder': [{'@type': 'Person', 'name': 'Sergio Miró', 'jobTitle': 'Co-founder and CEO'},
                {'@type': 'Person', 'name': 'Jordi Almendros', 'jobTitle': 'Co-founder, Operations and Engineering'}],
    'areaServed': [{'@type': 'Country', 'name': 'United States'}, {'@type': 'Country', 'name': 'Spain'}],
    'knowsAbout': ['AI implementation', 'Process automation', 'AI assistants', 'CRM integration', 'QuickBooks integration',
                   'Amazon to QuickBooks accounting', 'Data integration and reporting', 'Monday.com CRM', 'HubSpot'],
}


def pages():
    for root, _dirs, files in os.walk(SITE):
        for f in files:
            if f.endswith('.html'):
                fp = os.path.join(root, f)
                rel = '/' + os.path.relpath(fp, SITE).replace(os.sep, '/')
                yield fp, (rel[:-len('index.html')] if rel.endswith('/index.html') else rel)


def ld(id_, data):
    return f'<script type="application/ld+json" id="{id_}">{json.dumps(data, ensure_ascii=False)}</script>'


def faq(html, lang):
    items = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', html, flags=re.S)
    clean = lambda s: htmllib.unescape(re.sub(r'<[^>]+>', '', s)).strip()
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': lang,
            'mainEntity': [{'@type': 'Question', 'name': clean(q), 'acceptedAnswer': {'@type': 'Answer', 'text': clean(a)}} for q, a in items]}


urls = []
for fp, path in pages():
    html = open(fp).read()
    if 'http-equiv="refresh"' in html:
        continue
    # Google Analytics
    html = re.sub(r'<!-- ga -->.*?<!-- /ga -->', '', html, flags=re.S)
    html = html.replace('</head>', GA + '</head>', 1)
    # Structured data
    html = re.sub(r'<script type="application/ld\+json" id="ld-(org|faq)">.*?</script>', '', html, flags=re.S)
    lang = 'es' if path.startswith('/es/') else 'en'
    if path in ('/en/', '/es/'):
        html = html.replace('</head>', ld('ld-org', dict(ORG, inLanguage=lang)) + '</head>', 1)
    if path in ('/en/how-we-work/', '/es/como-trabajamos/') and '<details>' in html:
        html = html.replace('</head>', ld('ld-faq', faq(html, lang)) + '</head>', 1)
    open(fp, 'w').write(html)
    if not NO_INDEX.match(path):
        alts = dict(re.findall(r'<link rel="alternate" hreflang="(en|es)" href="([^"]+)"', html))
        urls.append((DOMAIN + path, alts))

# sitemap.xml with language alternates
entries = []
for loc, alts in sorted(urls):
    links = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{h}"/>' for l, h in sorted(alts.items()))
    entries.append(f'<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>{links}</url>')
open(os.path.join(SITE, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + '\n'.join(entries) + '\n</urlset>\n')

# robots.txt: open to search engines and AI search (ChatGPT, Claude, Perplexity, Google)
open(os.path.join(SITE, 'robots.txt'), 'w').write(
    'User-agent: *\nAllow: /\nDisallow: /api/\n\n'
    '# AI search and assistants are welcome\n'
    + ''.join(f'User-agent: {b}\nAllow: /\nDisallow: /api/\n\n' for b in
              ['OAI-SearchBot', 'ChatGPT-User', 'GPTBot', 'ClaudeBot', 'Claude-User', 'Claude-SearchBot', 'PerplexityBot', 'Google-Extended'])
    + f'Sitemap: {DOMAIN}/sitemap.xml\n')

# llms.txt: a plain summary for AI assistants
open(os.path.join(SITE, 'llms.txt'), 'w').write(f"""# Alma Intel

> Alma Intel is an applied AI firm for mid-market companies (20 to 500 people), based in Miami and Barcelona. We work inside the business, learn how it really runs and build AI systems that read, check and prepare the work teams do by hand: in the tools they already use (QuickBooks, HubSpot, Salesforce, Monday.com, Shopify, Amazon, Microsoft 365, Google Workspace, WhatsApp), with people approving what goes out. Engagements start with one process and continue as a monthly partnership. Founders: Sergio Miró (CEO) and Jordi Almendros (Operations and Engineering). Contact: hello@almaintel.ai.

## What we build
- [Solutions]({DOMAIN}/en/solutions/): AI assistants that answer from company data, process automation with human approval, and integrations so CRM, accounting and operations share one version of the numbers.
- [How we work]({DOMAIN}/en/how-we-work/): understand and measure the process, design, build and test with the team, then put it to use and keep improving it monthly.

## Client work (names withheld)
- [Construction, Miami]({DOMAIN}/en/clients/construction/): project and bid system plus an AI assistant for a luxury general contractor; quotes read by AI, crew hours by voice, open-book client portal.
- [Consumer goods, Amazon and retail]({DOMAIN}/en/clients/consumer-goods/): Amazon to QuickBooks accounting pipeline with fee and refund reconciliation; EDI with a grocery chain.
- [Public sector, trade and investment]({DOMAIN}/en/clients/public-agency/): one shared CRM on Monday.com for offices across the US; 14,684 contacts and 12,020 companies.
- [Hospitality, multi-site]({DOMAIN}/en/clients/hospitality/): booking-system reporting, reconciliation with the CRM, hourly checks and staff onboarding.
- [Manufacturing, commercial equipment]({DOMAIN}/en/clients/manufacturing/): monthly operations support and a lead engine that reads public records.

## More
- [Team]({DOMAIN}/en/team/)
- [Working notes]({DOMAIN}/en/working-notes/): short notes on data, automation and AI.
- [Lab]({DOMAIN}/en/lab/): solutions in pilot or in development.
- [Book a 30-minute call]({DOMAIN}/en/contact/)
- Spanish version: [{DOMAIN}/es/]({DOMAIN}/es/)
""")
print(f'finalized: {len(urls)} pages in sitemap')
