"""Builds the English client pages, case pages, working-notes index and the "Built for you" pieces.

Run from anywhere:  python3 tools/build_pages.py
Edit the CASES / NOTES data below and run again; it also refreshes the client cards
and the working-notes list on the home page.
"""
import json, os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
DOMAIN = 'https://almaintel.ai'
ARROW = '<span class="arrow" aria-hidden="true">↗</span>'


# ------------------------------------------------------------------ shared chrome
def read(path):
    return open(os.path.join(ROOT, path)).read()


HOME = read('en/index.html')
HEADER_TPL = re.search(r'<header class="site-header">.*?</header>', HOME, re.S).group(0)
FOOTER = re.search(r'<footer class="site-footer">.*?</footer>', HOME, re.S).group(0)
CLOSING = re.search(r'<section class="closing">.*?</section>', HOME, re.S).group(0)


def header(path):
    h = HEADER_TPL.replace(' aria-current="page"', '')
    for href in ('/en/solutions/', '/en/clients/', '/en/how-we-work/', '/en/working-notes/', '/en/team/'):
        if path.startswith(href):
            h = h.replace(f'<a href="{href}">', f'<a href="{href}" aria-current="page">', 1)
    return h


def page(path, title, desc, main, extra=''):
    url = DOMAIN + path
    html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">'
            f'<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">'
            f'<meta property="og:url" content="{url}"><meta property="og:image" content="{DOMAIN}/assets/social-en.png"><meta property="og:site_name" content="Alma Intel">'
            '<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#26224d">'
            '<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="preload" href="/assets/inter.ttf" as="font" type="font/ttf" crossorigin>'
            '<link rel="stylesheet" href="/assets/site.css"><link rel="stylesheet" href="/assets/redesign.css"><link rel="stylesheet" href="/assets/v2.css?v=11">'
            f'<script src="/assets/site.js" defer></script><script src="/assets/v2.js?v=3" defer></script>{extra}</head>\n'
            '<body><a class="skip" href="#contenido">Skip to content</a>' + header(path)
            + f'<main id="contenido">{main}</main>' + FOOTER + '</body></html>\n')
    out = os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(html)


def logo(name, size=16):
    return f'<img src="/assets/logos/{name}.svg" alt="" width="{size}" height="{size}">' if name else '<span class="dot"></span>'


# ------------------------------------------------------------------ client cases
# inputs/outputs: (text, logo file or None, tool or channel name or '')
CASES = [
    dict(
        key='construction', sector='Construction', eyebrow='Construction · General contractor',
        card='A luxury home and office builder in Miami',
        title='An AI assistant and project system for a luxury builder in Miami.',
        summary='A general contractor building luxury homes and office fit-outs needed one place for budgets, quotes, crew hours and client payments. We built a project system and an AI assistant the team talks to by voice or chat.',
        facts=[('Industry', 'Construction, general contractor'), ('Location', 'Miami, Florida'), ('Engagement', 'Monthly partnership'), ('Started', 'May 2026')],
        tools=[('whatsapp', 'WhatsApp'), ('gmail', 'Gmail'), ('quickbooks', 'QuickBooks'), ('excel', 'Excel'), ('claude', 'Claude')],
        inputs=[('Voice notes and photos from the site', 'whatsapp', 'WhatsApp'), ('Supplier quotes and invoices', 'gmail', 'Email'), ('Budgets in spreadsheets', 'excel', 'Excel')],
        kind='Custom app + AI assistant',
        parts=['Project and bid system', 'AI quote reader', 'Operations assistant', 'Subcontractor finder'],
        outputs=[('Budget vs actual for every job', None, 'Project app'), ('An open-book link for each client', None, 'Client portal'), ('Card spending checked against the books', 'quickbooks', 'QuickBooks')],
        situation=['Budgets lived in spreadsheets, quotes arrived as PDFs and photos, and crew hours came in as texts at the end of the day. Clients paying on an open-book basis kept asking where their money was going, and the answer took hours to put together.',
                   'Finding reliable subcontractors meant days of phone calls, and the owner did not want another tool his team would refuse to open.'],
        components=[('Project and bid system', 'Budget templates, quote comparison by trade, contracts, change orders and payments for every job, in one web app.'),
                    ('AI quote reader', 'Reads a quote from a text, a photo or a PDF and maps it line by line to the budget, so nobody retypes it.'),
                    ('Operations assistant', 'The team logs hours, costs and notes by voice or chat. Nothing is saved until a person confirms it.'),
                    ('Subcontractor finder', 'Uses live county permit data to show which licensed subcontractors are working nearby, and drafts the first message.')],
        day=['A foreman sends a voice note with the crew’s hours and the job number.',
             'The assistant matches people, job and cost code, and asks for a quick yes.',
             'The job budget updates. If a line runs over, the project manager gets an alert.',
             'The client opens their link and sees the same numbers the builder sees.'],
        numbers=[('52', 'actions the assistant can take on a job'), ('4', 'people on the team using it'), ('0', 'records saved without a person’s OK')],
        next='Two-way payments with QuickBooks and permit search in more counties.'),
    dict(
        key='consumer-goods', sector='Consumer goods', eyebrow='Consumer goods · Retail and Amazon',
        card='A brand selling to grocers and on Amazon',
        title='Amazon and wholesale accounting, connected to QuickBooks.',
        summary='A consumer-goods brand sells by the case to grocery chains and by the unit on Amazon. We connected Amazon to QuickBooks so every order, fee and refund is recorded, and the books can be explained down to the order.',
        facts=[('Industry', 'Consumer goods'), ('Channels', 'Grocery retail and Amazon'), ('Engagement', 'Fixed-scope project, then hourly'), ('Live since', 'February 2026')],
        tools=[('amazon', 'Amazon'), ('quickbooks', 'QuickBooks'), ('n8n', 'n8n'), ('postgresql', 'PostgreSQL'), ('telegram', 'Telegram')],
        inputs=[('Orders, fees and refunds', 'amazon', 'Amazon'), ('Purchases bought in cases', 'quickbooks', 'QuickBooks'), ('Orders from grocery chains', None, 'Retail')],
        kind='Integration + database',
        parts=['Order pipeline', 'Case-to-unit conversion', 'Refund and fee reconciliation', 'Daily exception check'],
        outputs=[('Every order recorded', 'quickbooks', 'QuickBooks'), ('A daily summary of anything that does not match', 'telegram', 'Telegram and email'), ('Retailer invoices by EDI (in progress)', None, 'EDI')],
        situation=['Amazon sales, fees and refunds were keyed into QuickBooks by hand. Stock was bought in cases and sold in units, so inventory never quite matched, and the books rarely agreed with what Amazon actually paid out.',
                   'At month-end the accountant spent days trying to explain the difference.'],
        components=[('Order pipeline', 'Each Amazon order becomes a sales receipt in QuickBooks, with its fees broken out.'),
                    ('Case-to-unit conversion', 'Purchases arrive in cases and are converted, so stock is always counted in units.'),
                    ('Refund and fee reconciliation', 'Reads Amazon’s event feed and matches every refund and fee to its order.'),
                    ('Daily exception check', 'Flags unmatched sales, refunds without an order and unmapped products. The target is zero.')],
        day=['Overnight, new orders, fees and refunds are pulled from Amazon.',
             'They are recorded in QuickBooks and matched to the payout.',
             'In the morning the team gets a short summary of anything that does not match.',
             'The accountant starts the month from books that already tie to Amazon.'],
        numbers=[('577', 'historical orders replayed to test the books'), ('5', 'automated workflows running every day'), ('Feb 2026', 'in production since')],
        next='A line-by-line inventory reconciliation surfaced damaged stock and logistics problems. Now: EDI with a national grocery chain and an app that reads purchase orders from PDF and email.'),
    dict(
        key='public-agency', sector='Public sector', eyebrow='Public sector · Trade and investment',
        card='An agency with offices across the US',
        title='One CRM for a trade and investment agency with offices across the US.',
        summary='Each office kept its own lists. We turned the project tool the agency already paid for into a shared CRM, cleaned and merged the data, and trained the team in three languages.',
        facts=[('Sector', 'Public sector, trade and investment'), ('Offices', 'A network across the US'), ('Engagement', 'Monthly partnership'), ('Languages', 'English, Spanish, Catalan')],
        tools=[('monday', 'Monday.com'), ('postgresql', 'PostgreSQL'), ('n8n', 'n8n'), ('excel', 'Excel')],
        inputs=[('Contact lists from each office', 'excel', 'Spreadsheets'), ('Trade-fair and database imports', None, 'Imports'), ('Event sign-ups', None, 'Landing pages')],
        kind='CRM build + data pipeline',
        parts=['Shared master records', 'Import and clean-up service', 'Automatic project boards', 'Training and manual'],
        outputs=[('One shared CRM', 'monday', 'Monday.com'), ('Project boards created automatically', 'monday', 'Monday.com'), ('A scorecard for leadership', None, 'Reporting')],
        situation=['Contacts and companies were scattered across offices, spreadsheets and inboxes. The same company existed three times with three spellings, and each office worked its own way.',
                   'Leadership had a three-year plan and no single picture of how far along it was.'],
        components=[('Shared master records', 'One record per person and per company, used by every office.'),
                    ('Import and clean-up service', 'Matches, de-duplicates and enriches incoming lists before they touch the CRM.'),
                    ('Automatic project boards', 'When a company joins a project, its board is created and linked without anyone copying it.'),
                    ('Training and manual', 'A 20-page how-to and sessions in English, Spanish and Catalan.')],
        day=['A list of 1,500 trade-fair visitors arrives.',
             'The import service matches each person and company to existing records.',
             'New contacts land in the right project; duplicates are merged instead of added.',
             'Leadership reads progress on the plan from the same data the offices use.'],
        numbers=[('14,684', 'contacts in one CRM'), ('12,020', 'companies, each with one record'), ('243', 'duplicate records merged')],
        next='Rolling the model out to more offices and an AI assistant that answers questions from the CRM.'),
    dict(
        key='hospitality', sector='Hospitality', eyebrow='Hospitality · Multi-site',
        card='A co-living operator with sites in Europe',
        title='Reporting and operations for a co-living operator with sites in Europe.',
        summary='A co-living and retreat operator needed numbers it could trust and an operation that did not depend on a few people’s memory. We connected its booking system to reporting, reconciled bookings with the CRM and documented how each house runs.',
        facts=[('Industry', 'Hospitality, multi-site'), ('Engagement', 'Monthly partnership'), ('Started', 'March 2026')],
        tools=[('n8n', 'n8n'), ('postgresql', 'Supabase'), ('clickup', 'ClickUp'), ('telegram', 'Telegram'), ('whatsapp', 'WhatsApp')],
        inputs=[('Bookings and payments', None, 'Booking system'), ('Leads and deals', None, 'CRM'), ('Know-how in old documents', 'confluence', 'Confluence')],
        kind='Reporting + integrations + documentation',
        parts=['Revenue reporting', 'Booking and CRM reconciliation', 'Hourly reviewer', 'Knowledge base'],
        outputs=[('Dashboards for management', None, 'Reporting'), ('Alerts when something is off', 'telegram', 'Telegram'), ('Onboarding staff can follow', 'clickup', 'ClickUp')],
        situation=['Revenue looked different depending on who you asked: the booking system said one thing and the CRM another. Know-how lived in outdated documents and in a few people’s heads, and staff rotated often.',
                   'A drop in revenue one month turned out to be rates loaded wrongly, and nobody had noticed for weeks.'],
        components=[('Revenue reporting', 'Occupancy, revenue and promotions by date of stay, traceable down to the booking.'),
                    ('Booking and CRM reconciliation', 'Bookings and CRM deals are compared every morning. Differences become a review list instead of silent corrections.'),
                    ('Hourly reviewer', '270 checks run every hour and alert the team on Telegram when something looks wrong.'),
                    ('Knowledge base', 'Processes moved from old documents into ClickUp, so new staff can onboard themselves.')],
        day=['Every hour, new bookings and payments sync from the booking system.',
             'Early in the morning, bookings are reconciled with the CRM.',
             'The reviewer runs its checks and flags anything unusual on Telegram.',
             'Management opens a dashboard whose numbers match the bookings.'],
        numbers=[('547', 'bookings reconciled since July 2025'), ('270', 'checks every hour'), ('22', 'units across the sites')],
        next='Lead intake into the new CRM and AI assistants for guest questions.'),
    dict(
        key='manufacturing', sector='Manufacturing', eyebrow='Manufacturing · Commercial equipment',
        card='A European manufacturer growing in the US',
        title='Earlier project leads and monthly support for a manufacturer’s US team.',
        summary='A European maker of commercial washroom equipment sells in the US through architects and designers. We support its US team every month and are testing a lead engine that reads public records to find projects before they are specified.',
        facts=[('Industry', 'Manufacturing, commercial equipment'), ('Market', 'United States'), ('Engagement', 'Monthly partnership'), ('Started', 'September 2026')],
        tools=[],
        inputs=[('Searches in a construction database', None, 'Sales team'), ('Public meeting agendas', None, 'Public records'), ('Customer data in several tools', None, 'Operations')],
        kind='Lead engine (pilot) + monthly support',
        parts=['Lead engine', 'Monthly operations support', 'Information-security review'],
        outputs=[('Scored project signals for sales', None, 'Lead engine'), ('Security review and policies', None, 'Report'), ('Hours each month for what slows the team', None, 'Partnership')],
        situation=['The sales team spent days inside a construction-data platform, chasing projects where a competitor’s product had already been specified and arguing to be swapped in late.',
                   'The US team also needed help with day-to-day systems, and with knowing where customer data lived.'],
        components=[('Lead engine', 'Reads public agendas in South Florida, finds construction projects before the permit stage and scores them for the product line.'),
                    ('Monthly operations support', 'A set number of hours each month for whatever slows the team down.'),
                    ('Information-security review', 'Where customer data lives, who can reach it, and the policies to protect it.')],
        day=['A city publishes its meeting agenda.',
             'The engine extracts each project and the firm designing it.',
             'Every project is scored for fit with the product line.',
             'Sales gets a short list with who to call.'],
        numbers=[('5', 'jurisdictions covered in the pilot'), ('335', 'projects analysed'), ('240', 'signals found before the permit stage')],
        next='Testing which signals sales turns into meetings before widening coverage.'),
]


def chip(text, icon, tool):
    sub = f'<small>{tool}</small>' if tool else ''
    return f'<span class="flow-chip">{logo(icon)}<span class="txt">{text}{sub}</span></span>'


def flow(c, compact=False):
    ins = ''.join(chip(*i) for i in c['inputs'])
    outs = ''.join(chip(*o) for o in c['outputs'])
    parts = ''.join(f'<li>{p}</li>' for p in c['parts'])
    return (f'<div class="case-flow"><div class="flow-col"><b>Before</b>{ins}</div><span class="flow-arrow" aria-hidden="true">→</span>'
            f'<div class="flow-core"><span class="built-by"><img src="/assets/favicon.svg" alt="" width="18" height="18">Built by Alma Intel</span>'
            f'<span class="kind">{c["kind"]}</span><ul>{parts}</ul></div>'
            f'<span class="flow-arrow" aria-hidden="true">→</span><div class="flow-col out"><b>Now</b>{outs}</div></div>')


def tool_strip(tools):
    return '<div class="tool-strip">' + ''.join(f'<span>{logo(n, 15)}{t}</span>' for n, t in tools) + '</div>' if tools else ''


# Clients index
blocks = ''
for c in CASES:
    blocks += (f'<article class="client" id="{c["key"]}"><div class="client-head"><div><p class="eyebrow">{c["eyebrow"]}</p><h2>{c["title"]}</h2></div>'
               f'<span class="engagement-tag"><b>Engagement:</b> {dict(c["facts"]).get("Engagement")}</span></div>{flow(c)}'
               f'<div class="client-text"><div><h3>In short</h3><p>{c["summary"]}</p></div><div><h3>Tools involved</h3>{tool_strip(c["tools"]) or "<p>Their own CRM and public data sources.</p>"}'
               f'<div class="actions"><a class="link-arrow" href="/en/clients/{c["key"]}/">Read the full case{ARROW}</a></div></div></div></article>')

page('/en/clients/', 'Client work | Alma Intel',
     'How Alma Intel works with a builder, a consumer-goods brand, a public agency, a hospitality group and a manufacturer.',
     f'''<section class="page-head wrap"><p class="eyebrow">Clients</p><h1>Inside our<br>engagements.</h1>
<p class="lead">Five companies, five industries. We keep their names private because they are our clients, not our marketing. Each case shows what came in, what we built and what the team works with now.</p></section>
<section class="wrap">{blocks}
<div class="lab-nudge"><p>Working on a problem none of these cover? Some of what we build starts in our lab before it reaches a client.</p><a class="link-arrow" href="/en/lab/">See what’s in the lab{ARROW}</a></div></section>
{CLOSING}''')

# Case pages
for i, c in enumerate(CASES):
    nxt = CASES[(i + 1) % len(CASES)]
    facts = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in c['facts'])
    if c['tools']:
        facts += f'<div><dt>Tools</dt><dd>{tool_strip(c["tools"])}</dd></div>'
    comps = ''.join(f'<article class="component"><span class="n">0{n + 1}</span><h3>{t}</h3><p>{d}</p></article>' for n, (t, d) in enumerate(c['components']))
    day = ''.join(f'<li>{s}</li>' for s in c['day'])
    nums = ''.join(f'<div><b>{n}</b><span>{t}</span></div>' for n, t in c['numbers'])
    situation = ''.join(f'<p>{p}</p>' for p in c['situation'])
    main = f'''<section class="page-head wrap"><div class="case-hero"><div><p class="eyebrow"><a href="/en/clients/">Clients</a> · {c["eyebrow"]}</p>
<h1>{c["title"]}</h1><p class="lead">{c["summary"]}</p></div><dl class="facts">{facts}</dl></div></section>
<section class="wrap">{flow(c)}
<div class="case-section"><div><p class="eyebrow">The situation</p><h2>Where they started.</h2></div><div>{situation}</div></div>
<div class="case-section"><div><p class="eyebrow">What we built</p><h2>The pieces.</h2></div><div class="components">{comps}</div></div>
<div class="case-section"><div><p class="eyebrow">A normal day</p><h2>How it works now.</h2></div><ol class="day">{day}</ol></div>
<div class="case-section"><div><p class="eyebrow">In numbers</p><h2>What it handles.</h2></div><div><div class="numbers">{nums}</div><p class="numbers-note">Figures from the live systems, October 2026. Client name withheld.</p></div></div>
<div class="case-section"><div><p class="eyebrow">What’s next</p><h2>Where it goes from here.</h2></div><div><p>{c["next"]}</p></div></div>
<div class="case-cta"><h2>Does your team have a process like this one?</h2><div class="actions"><a class="button light" href="/en/contact/?proceso=caso-{c["key"]}">Book a 30-minute call{ARROW}</a></div></div>
<nav class="case-next" aria-label="More cases"><a href="/en/clients/"><small>Back</small>All client work</a><a href="/en/clients/{nxt["key"]}/"><small>Next case</small>{nxt["card"]} →</a></nav></section>'''
    page(f'/en/clients/{c["key"]}/', f'{c["sector"]} case | Alma Intel', c['summary'], main)

# ------------------------------------------------------------------ working notes
THUMBS = {
    'payment-or-revenue': '<div class="th-bars"><div>September<i style="--w:30%"></i><b>$360</b></div><div>October<i style="--w:70%"></i><b>$840</b></div></div>',
    'merging-contacts': '<div class="th-contacts"><div><b>J. Smith</b>Acme Corp<br>j.smith@acme.test</div><span>?</span><div><b>John Smith</b>ACME Inc.<br>john@acme.test</div></div>',
    'reading-is-not-recording': '<div class="th-receipt"><i></i><i></i><i></i><b>$184.20</b></div><span class="th-arrow">→</span><span class="th-ledger">Record?</span>',
}
NOTES = [
    ('payment-or-revenue', 'Demonstration · Finance', 'Is a September payment September revenue?', 'Follow one stay across two months. The money is the same; the question the report answers changes.', '4 min'),
    ('merging-contacts', 'Decision note · Data', 'Would you merge these two contacts?', 'A match helps you find a record. Deciding what to do with it needs more context.', '4 min'),
    ('reading-is-not-recording', 'Working note · Applied AI', 'Reading a receipt is not recording an expense.', 'What should happen between AI reading a value and a change in your books.', '3 min'),
]


def note_cards(heading='h3'):
    return '<div class="note-cards">' + ''.join(
        f'<a class="note-card" href="/en/working-notes/{k}/"><div class="note-thumb" aria-hidden="true">{THUMBS[k]}</div>'
        f'<div class="note-body"><p class="eyebrow">{tag}</p><{heading}>{t}</{heading}><p>{d}</p><span class="note-meta">{mins} read</span>'
        f'<span class="read">Read the note<span aria-hidden="true">→</span></span></div></a>' for k, tag, t, d, mins in NOTES) + '</div>'


page('/en/working-notes/', 'Working notes | Alma Intel', 'Notes on data, automation and AI from the work we do with clients.',
     f'''<section class="page-head wrap"><p class="eyebrow">Working notes</p><h1>What we learn<br>by doing the work.</h1>
<p class="lead">Short notes on data, automation and AI. Each one starts with a question we met in a real project and leaves you with something you can use.</p></section>
<section class="section wrap">{note_cards("h2")}<p class="notes-foot">Examples are reconstructed so they explain the idea without exposing client information.</p></section>
{CLOSING}''')

# ------------------------------------------------------------------ home: refresh client cards and notes
home = read('en/index.html')
cards = ''.join(
    f'<a class="client-card" href="/en/clients/{c["key"]}/"><p class="eyebrow">{c["sector"]}</p><h3>{c["card"]}</h3>'
    f'{flow(c)}<span class="more">Read the case{ARROW}</span></a>' for c in CASES[:3])
home = re.sub(r'<div class="client-cards">.*?</div></div></section>', f'<div class="client-cards">{cards}</div></div></section>', home, count=1, flags=re.S)
home = re.sub(r'<div class="(journal-short-list|note-cards)">.*?</section>', note_cards() + '</section>', home, count=1, flags=re.S)
open(os.path.join(ROOT, 'en/index.html'), 'w').write(home)

# ------------------------------------------------------------------ the old search prototype now points to "Built for you"
os.makedirs(os.path.join(ROOT, 'en', 'ask'), exist_ok=True)
open(os.path.join(ROOT, 'en', 'ask', 'index.html'), 'w').write('<!doctype html><meta charset="utf-8"><title>Alma Intel</title>'
                                                           '<meta http-equiv="refresh" content="0; url=/en/for-you/"><link rel="canonical" href="https://almaintel.ai/en/for-you/">')
MIC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/></svg>'

# ------------------------------------------------------------------ "For you" pages: library of approved pieces
# Each piece is a finished section of this site. The AI may only choose and order them;
# the page shows every piece's source next to it.
def section_from(path, start):
    html = read(path)
    i = html.index(start)
    return html[i:html.index('</section>', i) + len('</section>')]


PIECES = []


def piece(pid, kind, title, summary, tags, html, src_label, src_url, group=None):
    PIECES.append(dict(id=pid, kind=kind, title=title, summary=summary, tags=tags, html=html,
                       source=src_label, url=src_url, group=group))


for c in CASES:
    url = f'/en/clients/{c["key"]}/'
    tags = ' '.join([c['sector'], c['kind'], ' '.join(c['parts']), ' '.join(t for _, t in c['tools'])])
    piece(f'case-{c["key"]}', 'Client case', c['title'], c['summary'], tags,
          f'<section class="section wrap"><p class="eyebrow fy-eyebrow">{c["eyebrow"]}</p><h2 class="fy-h2">{c["title"]}</h2>'
          f'<p class="lead fy-lead">{c["summary"]}</p>{flow(c)}<div class="actions"><a class="link-arrow" href="{url}">Read the full case{ARROW}</a></div></section>',
          f'Client case · {c["sector"]}', url)
    piece(f'parts-{c["key"]}', 'What we built (components)', f'What we built for the {c["sector"].lower()} client',
          '; '.join(t for t, _ in c['components']), tags,
          f'<section class="section wrap"><div class="case-section fy-flat"><div><p class="eyebrow">What we built · {c["sector"]}</p><h2>The pieces.</h2></div>'
          f'<div class="components">' + ''.join(f'<article class="component"><span class="n">0{n + 1}</span><h3>{t}</h3><p>{d}</p></article>' for n, (t, d) in enumerate(c['components'])) + '</div></div></section>',
          f'Client case · {c["sector"]}', url)
    piece(f'day-{c["key"]}', 'A normal day with the system', f'How the {c["sector"].lower()} client works now', ' '.join(c['day']), tags,
          f'<section class="section wrap"><div class="case-section fy-flat"><div><p class="eyebrow">A normal day · {c["sector"]}</p><h2>How it works now.</h2></div>'
          f'<ol class="day">' + ''.join(f'<li>{s}</li>' for s in c['day']) + '</ol></div></section>',
          f'Client case · {c["sector"]}', url)
    piece(f'nums-{c["key"]}', 'Figures from a live system', f'Numbers from the {c["sector"].lower()} client',
          '; '.join(f'{n} {t}' for n, t in c['numbers']), tags,
          f'<section class="section wrap"><div class="case-section fy-flat"><div><p class="eyebrow">In numbers · {c["sector"]}</p><h2>What it handles.</h2></div>'
          f'<div><div class="numbers">' + ''.join(f'<div><b>{n}</b><span>{t}</span></div>' for n, t in c['numbers']) +
          '</div><p class="numbers-note">Figures from the live system, October 2026. Client name withheld.</p></div></div></section>',
          f'Client case · {c["sector"]}', url)

piece('why', 'Why Alma Intel', 'The AI team model for mid-market companies',
      'Large companies embed AI engineers in their operations; we bring that model to companies with 20 to 500 people. We start inside the operation, build and run the system, and measure what changed.',
      'why model team embedded engineers value difference',
      section_from('en/index.html', '<section class="section wrap"><div class="model-grid">'), 'Home · Why Alma Intel', '/en/')
piece('build', 'What we build', 'AI assistants, process automation, integrations and data',
      'Assistants that answer from your own data; automation of documents and requests with human approval; integrations so CRM, accounting and operations share one version of the numbers.',
      'solutions services assistants automation integrations crm accounting reporting data',
      section_from('en/index.html', '<section class="section wrap ruled"><div class="section-heading-row"><div><p class="eyebrow">What we build'),
      'Home · What we build', '/en/solutions/')
sol_html = read('en/solutions/index.html')
for sid, pid, title, summary, tags in [
    ('assistants', 'sol-assistants', 'AI assistants: your information, accessible to the team',
     'Assistants connected to your documents and processes, with the context and permissions each question needs: internal questions, visible sources, drafted responses.',
     'assistant knowledge documents answers search internal questions chat voice'),
    ('automation', 'sol-automation', 'Process automation: from an input to the next step',
     'Workflows that interpret information, apply rules and prepare actions across your tools, with review where it is needed: documents and requests, approvals, tasks and follow-up.',
     'automation automate workflow invoices documents requests approvals tasks follow-up manual work'),
    ('integrations', 'sol-integrations', 'Integrations and data: your tools, working together',
     'We connect CRM, operations and financial systems so data reaches the right place and keeps its meaning: CRM and internal systems, synchronisation, reporting.',
     'integration connect sync crm accounting erp reporting dashboards data quickbooks hubspot salesforce'),
]:
    piece(pid, 'Solution', title, summary, tags, section_from('en/solutions/index.html', f'<section class="solution-block'
          + (' solution-tinted' if sid == 'automation' else ' ') + f'" id="{sid}">'), 'Solutions', f'/en/solutions/#{sid}')
hww = read('en/how-we-work/index.html')
i = hww.index('<div class="stage-explorer')
process_html = ('<section class="section wrap"><div class="section-heading-row"><div><p class="eyebrow">How we work</p><h2>From a manual process<br>to a system you can use.</h2></div></div>'
                + hww[i:hww.index('</section>', i)] + '</section>')
piece('process', 'How we work (four steps)', 'Understand, design, implement, put to use',
      'We follow a real process with your team and measure it; agree inputs, rules and controls before building; build and test the exceptions with you; then roll it out, document it and support it.',
      'process method steps how we work start diagnostic implementation rollout',
      process_html, 'How we work', '/en/how-we-work/')
piece('engage', 'How to work with us', 'One project, or ongoing development',
      'Implement one process with defined objectives and tests, or keep improving it with agreed priorities and ongoing support.',
      'engagement pricing project monthly partnership retainer start cost',
      section_from('en/how-we-work/index.html', '<section class="section wrap"><div class="engagement-overview">'), 'How we work', '/en/how-we-work/')
piece('faq', 'Questions before starting', 'Tools, price and timing, control, support',
      'We start from the tools you already use; price and timing are defined around the process; you decide which actions need a person to confirm; we document and support after delivery.',
      'faq replace tools price timing security control approval support after delivery',
      section_from('en/how-we-work/index.html', '<section class="section method-faq">'), 'How we work · FAQ', '/en/how-we-work/')
piece('team', 'Team', 'The partners lead every engagement',
      'Sergio Miró (two decades between Europe and the US) and Jordi Almendros (builds the systems). You talk to the people doing the work.',
      'team people founders partners who experience trust',
      section_from('en/index.html', '<section class="section ruled wrap"><div class="team-teaser">'), 'Team', '/en/team/')
tools_html = ('<section class="section wrap"><p class="eyebrow">Works with your tools</p><div class="tool-strip fy-tools">'
              + ''.join(f'<span>{logo(n, 18)}{t}</span>' for n, t in [
                  ('quickbooks', 'QuickBooks'), ('xero', 'Xero'), ('salesforce', 'Salesforce'), ('hubspot', 'HubSpot'), ('monday', 'Monday.com'),
                  ('shopify', 'Shopify'), ('amazon', 'Amazon'), ('stripe', 'Stripe'), ('microsoft', 'Microsoft 365'), ('excel', 'Excel'),
                  ('google-workspace', 'Google Workspace'), ('slack', 'Slack'), ('whatsapp', 'WhatsApp'), ('sap', 'SAP'), ('clickup', 'ClickUp'), ('notion', 'Notion')])
              + '</div></section>')
piece('tools', 'Tools we work with', 'The tools we connect', 'QuickBooks, Xero, Salesforce, HubSpot, Monday.com, Shopify, Amazon, Stripe, Microsoft 365, Excel, Google Workspace, Slack, WhatsApp, SAP, ClickUp, Notion.',
      'tools integrations software quickbooks hubspot salesforce shopify amazon', tools_html, 'Home · Tools', '/en/')
for k, tag, t, d, mins in NOTES:
    piece(f'note-{k}', 'Working note', t, d, tag,
          f'<a class="note-card" href="/en/working-notes/{k}/"><div class="note-thumb" aria-hidden="true">{THUMBS[k]}</div>'
          f'<div class="note-body"><p class="eyebrow">{tag}</p><h3>{t}</h3><p>{d}</p><span class="note-meta">{mins} read</span>'
          f'<span class="read">Read the note<span aria-hidden="true">→</span></span></div></a>',
          'Working notes', f'/en/working-notes/{k}/', group='notes')
for k, s, t, d, f in [
    ('lab-signals', 'pilot', 'Signal engine', 'Flags the moment a design firm is tied to a public project, months before it goes out to bid.', 'leads construction public sector tenders architects permits'),
    ('lab-assistant', 'pilot', 'Operations assistant', 'Your team talks to it by voice or WhatsApp. It logs hours, updates job costs and answers from your own data.', 'assistant voice whatsapp hours field'),
    ('lab-control', 'building', 'Control room', 'One place to see every system we run for you: what it did, what it flagged and what is waiting for a person.', 'monitoring dashboard control visibility'),
    ('lab-opportunities', 'building', 'Opportunity graph', 'Tenders and grants from the World Bank, the EU, the US, the UK and Canada, matched against a portfolio of companies.', 'tenders grants international export agency'),
]:
    piece(k, f'Lab solution ({"Pilot" if s == "pilot" else "Building"})', t, d, f,
          f'<article class="lab-item"><span class="status status--{s}">{"Pilot" if s == "pilot" else "Building"}</span><h3 class="fy-lab-h">{t}</h3><p>{d}</p>'
          f'<a class="link-arrow" href="/en/contact/?proceso={k}">Apply this to my company{ARROW}</a></article>',
          'Lab', '/en/lab/', group='lab')

def label_for(pid):
    """Short name of a piece for the "On this page" index."""
    head = pid.split('-')[0]
    return {'case': 'The case', 'parts': 'What we built', 'day': 'A normal day', 'nums': 'In numbers', 'why': 'Why us',
            'build': 'What we build', 'engage': 'Working together', 'faq': 'Questions', 'team': 'Who you work with',
            'tools': 'Tools', 'note': 'Working note', 'lab': 'From the lab', 'process': 'How we work',
            'sol': {'sol-assistants': 'AI assistants', 'sol-automation': 'Process automation', 'sol-integrations': 'Integrations'}.get(pid)}[head]


with open(os.path.join(ROOT, 'assets', 'pieces.json'), 'w') as f:
    json.dump({p['id']: dict(html=p['html'], source=p['source'], url=p['url'], group=p['group'], label=label_for(p['id'])) for p in PIECES}, f, ensure_ascii=False)
with open(os.path.join(ROOT, '..', 'ask-data', 'pieces.json'), 'w') as f:
    json.dump([dict(id=p['id'], kind=p['kind'], title=p['title'], summary=p['summary'], tags=p['tags']) for p in PIECES], f, ensure_ascii=False, indent=1)
print('pieces:', len(PIECES))

# ------------------------------------------------------------------ "For you" page
FY_EXAMPLES = ['We are a builder and our job costs live in spreadsheets', 'We sell on Amazon and our books never match',
               'Our CRM is a mess across three offices', 'How do you start, and what does it cost?']
fy_ex = ''.join(f'<button type="button">{e}</button>' for e in FY_EXAMPLES)
page('/en/for-you/', 'A page built for you | Alma Intel',
     'Tell us what you are looking for and we build a page for you from our real client work, with the source of every part.',
     f'''<section class="fy-intro wrap" data-fy-intro><p class="eyebrow">Built for you</p>
<h1>Tell us what you need.<br><span class="headline-accent">We’ll build the page.</span></h1>
<p class="lead">Describe your company or the problem in your own words. In a few seconds you get a page put together from our real client work, with the source of every part.</p>
<button type="button" class="fy-trigger" data-fy-open><span>What are you trying to fix?</span><kbd>⌘K</kbd></button>
<div class="fy-chips">{"".join(f'<button type="button" data-fy-open="{e}">{e}</button>' for e in FY_EXAMPLES)}</div>
<p class="ask-note">Built only from approved content on this site. The AI chooses and orders it; it does not invent anything. Pages are kept for 90 days so you can share them.</p></section>
<div data-fy-out hidden></div>
<div class="fy-overlay" data-fy-overlay hidden role="dialog" aria-modal="true" aria-label="Build your page">
<div class="fy-panel">
<div class="fy-ask"><form class="ask-bar fy-bar" data-fy-form><label class="sr-only" for="fy-q">What are you trying to fix?</label>
<input id="fy-q" autocomplete="off" maxlength="300" placeholder="e.g. We run 12 job sites and track costs in Excel">
<button type="button" class="ask-mic" aria-pressed="false" aria-label="Ask by voice" hidden>{MIC}</button>
<button type="submit" class="ask-go" aria-label="Build my page">→</button></form>
<p class="fy-error" data-fy-error role="alert"></p>
<div class="fy-examples">{fy_ex}</div>
<p class="fy-hint"><span>Built from our real work, with sources</span><button type="button" data-fy-close>Esc to close</button></p></div>
<div class="fy-stage" data-fy-stage><canvas aria-hidden="true"></canvas><p class="fy-asked" data-fy-asked></p><p class="fy-status" data-fy-status role="status">Reading what you need…</p></div>
</div></div>''', '<script src="/assets/foryou.js?v=7" defer></script>')

# ------------------------------------------------------------------ home: entry point to "Built for you"
FY_BAND = f'''<section class="fy-band" data-fy-band><div class="wrap fy-band-grid"><div><p class="eyebrow">Built for you</p>
<h2>Not sure where to start?<br><span class="headline-accent">Get a page built around your problem.</span></h2>
<p class="lead">Describe your company in your own words. In a few seconds we put together a page from our real client work, with the source of every part.</p></div>
<div><form class="fy-band-form" action="/en/for-you/" method="get"><label class="sr-only" for="fy-home-q">What are you trying to fix?</label>
<input id="fy-home-q" name="ask" maxlength="300" autocomplete="off" placeholder="What are you trying to fix?"><button type="submit" class="ask-go" aria-label="Build my page">→</button></form>
<div class="fy-band-chips">{"".join(f'<a href="/en/for-you/?ask={e.replace(" ", "+")}">{e}</a>' for e in FY_EXAMPLES[:3])}</div></div></div></section>'''
home = read('en/index.html')
home = re.sub(r'<section class="fy-band" data-fy-band>.*?</section>', '', home, flags=re.S)
tools_end = home.index('</section>', home.index('<section class="tools-band"')) + len('</section>')
home = home[:tools_end] + FY_BAND + home[tools_end:]
open(os.path.join(ROOT, 'en/index.html'), 'w').write(home)
