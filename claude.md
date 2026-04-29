You are a Senior Creative Director, UI/UX Lead, Copywriter, and Front-End Engineer.

You are working inside the existing Alma Intel website project.

Your task is to redesign and improve the Alma Intel website homepage so it clearly communicates what Alma Intel does, who it helps, and why decision makers should care.

Before coding:
1. Inspect the existing project structure.
2. Identify the current stack, files, routes, styles, and components.
3. Reuse the existing stack: HTML5, CSS3, and Vanilla JavaScript unless the project clearly uses something else.
4. Do not introduce unnecessary libraries.
5. Do not break existing pages, navigation, forms, or deployment setup.

Do not ask questions first. Use the information below and make reasonable assumptions where needed.

---

## PROJECT CONTEXT

Alma Intel is an automation and AI consulting firm that helps small and mid-sized businesses turn AI into business efficiency.

The company helps businesses improve the way they operate by:
- Connecting existing tools.
- Automating repetitive workflows.
- Integrating CRMs, ERP systems, accounting platforms, spreadsheets, e-commerce platforms, email, and dashboards.
- Building smarter systems around daily operations.
- Creating dashboards and reporting systems.
- Applying AI where it creates real operational value.

Alma Intel does not sell generic AI packages. The company starts with business problems and builds practical systems around them.

**Main tagline:** Turn AI into business efficiency.

---

## TARGET AUDIENCE

The page is for decision makers in small and mid-sized businesses:
- Owners, CEOs, COOs, CFOs
- Managing directors
- Operations, sales, and finance leaders

**Important audience insight:**
Many visitors may not know what automation really means. They may not search for "AI automation consulting." They usually recognize symptoms:
- Too much manual work.
- Too many spreadsheets.
- CRM not updated.
- Reports take too long.
- Accounting and e-commerce do not connect.
- Leads are lost because follow-up is manual.
- Teams copy data between systems.
- Leadership lacks visibility.
- They want to use AI but do not know where it actually makes sense.

The website must make these visitors think: "This is exactly what is happening in my company."

---

## MAIN GOAL OF THE PAGE

The homepage should quickly answer:
1. What does Alma Intel do?
2. Is this relevant to my business?
3. What problems do they solve?
4. What does automation actually look like in practice?
5. Why should I trust them?
6. What should I do next?

**Primary conversion goal:** Book a consultation / audit.
**Secondary goal:** Help visitors understand what Alma Intel automates through clear examples.

---

## VISUAL DIRECTION

Create a premium, dark, modern, executive-level technology website.

The page should feel: Clear, serious, premium, modern, intelligent, trustworthy, practical, editorial, easy to scan.

It should NOT feel: Generic SaaS, AI-generated, overloaded, neon/futuristic cliché, startup template, too playful, too abstract, too corporate and boring.

---

## COLOR PALETTE

```css
--navy: #25224a;
--deep: #16163b;
--accent: #6d73e6;
--light: #e7ecf2;
--white: #ffffff;
```

Use the dark colors as the main base. Use `#6d73e6` for CTAs, highlights, lines, active states, and selected accents. Use `#e7ecf2` and `#ffffff` for readable text and light sections if needed.

Do not use the old turquoise/green accent. Use the new palette above.

---

## TYPOGRAPHY

Use Inter if available. If the current project uses Sora for headings and Inter for body, keep it only if it looks premium and consistent. Otherwise, simplify around Inter.

Typography should feel editorial, clean, and highly readable.

---

## LAYOUT PRINCIPLES

- Prefer left-aligned layouts.
- Avoid centered content everywhere.
- Use strong hierarchy.
- Use generous spacing.
- Keep the page easy to read.
- Avoid too many cards that all look the same.
- Use section contrast intentionally.
- Make desktop feel premium and spacious.
- Make mobile feel intentionally designed, not just squeezed.

---

## MOBILE DESIGN RULES

Mobile is critical. Do not simply shrink the desktop layout.

**Mobile must NOT:**
- Hide important content just to save space.
- Show exactly the same as desktop but smaller.
- Create huge text-heavy sections.

**Mobile must:**
- Use shorter versions of long headlines where needed.
- Use concise section intros.
- Collapse or simplify long lists intelligently.
- Show all important service/use-case categories in a compact way.
- Reduce visual noise.
- Keep CTAs easy to tap.
- Avoid sticky buttons if they feel annoying.
- Keep the first viewport clear and compelling.

Use creative responsive design, not lazy hiding.

---

## COPYWRITING RULES

**Avoid generic phrases:**
- "Unlock the power of AI"
- "Revolutionize your business"
- "AI-powered transformation"
- "Disrupt your industry"
- "Future-proof your business"
- "Innovative solutions" without context

**Use concrete language:**
- "Connect Amazon sales data with QuickBooks."
- "Automate lead follow-up from your CRM."
- "Reduce manual reporting."
- "Give leadership real-time visibility."
- "Sync data between tools your team already uses."
- "Replace spreadsheet-driven processes with controlled workflows."

**Tone:** Confident but not arrogant. Professional but human. Clear but not basic. Practical but premium. Serious but not cold.

---

## PAGE STRUCTURE

### 1. HERO SECTION
Goal: Immediately explain what Alma Intel does.

Suggested headline: "AI & automation that make your business run better."
Alternative: "Turn AI into business efficiency."

Use one strong H1. The tagline can appear as supporting copy.

Hero subheadline: Alma Intel helps SMEs connect tools, automate workflows, and build smarter systems around sales, finance, operations, and reporting.

Include:
- Primary CTA: "Book a consultation"
- Secondary CTA: "See what we automate"
- Small trust/clarity line: "No generic AI packages. We start with the business process."

Visual: Create a premium abstract system-flow visual. It can suggest connected tools, workflows, dashboards, data movement, or operational clarity. Avoid robots, generic AI brains, stock illustrations, or messy gradients.

### 2. PROBLEM SECTION
Goal: Make decision makers recognize their operational pain.

Headline direction: "Most companies do not need more tools. They need their tools to work together."

Pain points:
- Your team enters the same data in multiple systems.
- Your CRM is not updated reliably.
- Reports take too long to prepare.
- Accounting, e-commerce, and ERP systems do not speak to each other.
- Leads are lost because follow-up is manual.
- Spreadsheets control important workflows.
- Teams spend hours reconciling information.
- You want to use AI, but you are not sure where it makes sense.

Design this section in a premium way. It should not feel like a basic bullet list.

### 3. "WHAT AUTOMATION ACTUALLY MEANS" SECTION
Goal: Educate visitors who do not understand automation.

Explain: Automation means connecting the tools your business already uses so data, tasks, alerts, reports, and workflows move automatically instead of depending on manual work.

Use a before/after structure:
- Before: People copy data, chase updates, prepare reports manually, and fix errors.
- After: Systems update each other, alerts are triggered, dashboards stay current, and teams focus on work that matters.

### 4. USE CASES / EXAMPLES SECTION
Goal: Elevate current examples into clear, high-value use cases. This is one of the most important sections.

**Finance**
- Amazon to QuickBooks automation.
- Invoice tracking. Payment reminders. Accounts receivable visibility.
- Reconciliation support. Financial reporting workflows.

**Sales**
- CRM automation. Lead assignment. Follow-up reminders.
- Pipeline updates. Status changes. Sales dashboards.

**Operations**
- ERP and accounting integrations. Data synchronization.
- Workflow alerts. Internal process automation. Project/task visibility.

**Data & AI**
- Sales and operations dashboards.
- AI assistants for internal teams.
- Data cleanup. Search and summarize company information.
- Analyze records and draft responses.

Each use case: clear title + short explanation + concrete outcome.

Avoid identical card grids. Use visual hierarchy, categories, contrast, and editorial layout.

### 5. APPROACH SECTION
Goal: Show Alma Intel has a clear process.

Four steps:
1. **Audit** — We review your tools, workflows, pain points, and manual work.
2. **Design** — We define the right system based on your existing operations and goals.
3. **Build** — We implement the automation, integration, dashboard, AI workflow, or internal tool.
4. **Evolve** — We improve the system as your business grows.

### 6. BENEFITS SECTION
Goal: Translate the service into business outcomes.

- Less manual work. Fewer errors. Cleaner data.
- Faster decisions. Better visibility. More reliable follow-up.
- Stronger finance workflows. Stronger sales operations. More scalable processes.

Do not invent fake metrics. If using numbers, label them clearly as examples or remove them.

### 7. WHY ALMA INTEL SECTION
Goal: Build credibility without fake testimonials.

- We start with the business problem, not the technology.
- We work around your existing systems.
- We build practical solutions, not generic AI packages.
- We focus on visibility, efficiency, and operational control.
- We design systems that teams can actually use.

### 8. FINAL CTA SECTION
Goal: End with a strong conversion moment.

Headline: "Start with one process. Build the system around it."
CTA: "Book a consultation"
Microcopy: "No pitch. We'll identify where automation can create practical business value."

---

## NAVIGATION

Simple nav: Home | What We Automate | Process | Contact
CTA in nav: "Book a consultation"

If existing pages like Consulting or Products exist, preserve them. The homepage should work even if visitors never open those pages.

---

## FORM

Preserve the existing Formspree form (action: https://formspree.io/f/xbdalzld).
Fields: Name, Company, Email, Phone (optional), What process do you want to improve?
Make the form feel premium and simple.

---

## DESIGN DETAILS

**Use:**
- Subtle borders. Thin dividers. Editorial labels.
- System-flow lines. Small annotations.
- High-quality hover/focus states. Premium button interactions.
- Scroll or reveal effects only if subtle and performant.

**Avoid:**
- Basic translateY hover only.
- Repetitive cards.
- Fake dashboards that look generic.
- Overly bright gradients.
- Too many icons.
- Centering everything.
- Huge walls of text.
- Repeated CTAs with the same label everywhere.

---

## ACCESSIBILITY

- One H1. Correct heading order. High contrast.
- Visible focus states. Semantic buttons and links.
- Proper form labels. Mobile tap targets.
- `prefers-reduced-motion` support.

---

## SEO

Title: `Alma Intel | AI & Automation Consulting for Business Efficiency`
Meta description: `Alma Intel helps small and mid-sized businesses connect tools, automate workflows, build dashboards, and turn AI into practical business efficiency.`

Use semantic sections and meaningful headings.

---

## QUALITY CHECK BEFORE FINISHING

- The hero explains the company in under 10 seconds.
- The page speaks to decision makers.
- Automation is explained clearly.
- Examples are concrete.
- The page is not overloaded.
- Mobile is intentionally designed.
- CTAs are visible and clear.
- The new color palette is used.
- The design does not feel like a generic AI startup.
- No fake claims or unsupported metrics were added.
- Existing pages and form functionality are not broken.

---

## FINAL RESPONSE FORMAT

After implementation, summarize:
1. Files changed.
2. Main design/copy improvements.
3. How to preview locally.
4. Any assumptions made.

---

## HISTORIAL DEL PROYECTO - Alma Intel Website

### Stack Técnico
- HTML5 + CSS3 + Vanilla JavaScript
- Fuentes: Sora (headings) + Inter (body) — simplificar a Inter si no se ve premium
- Form: Formspree (action: https://formspree.io/f/xbdalzld) — campos: name, company, email, phone (optional), challenge
- Hosting: GitHub + Cloudflare Pages
- Repositorio: https://github.com/jordialmendrosperez/almaintel

### Páginas Existentes
1. **index.html** — Landing principal (en rediseño)
2. **consulting.html** — Servicios de consultoría (preservar)
3. **products.html** — Productos (preservar)
4. **how-we-can-help-you.html** — Preservar
5. **privacy.html** / **terms.html** — Preservar

### Paleta de Colores Actualizada (USAR ESTA)
```css
--navy: #25224a;
--deep: #16163b;
--accent: #6d73e6;
--light: #e7ecf2;
--white: #ffffff;
```
La paleta anterior (azul #3753E5 + turquesa #00D4AA) está obsoleta. No usar.

### Lecciones Aprendidas — NO Repetir

1. **Contenido centrado** — Layouts siempre left-aligned.
2. **Hovers solo con translateY** — Usar underlines, slides, efectos con personalidad.
3. **Promesas no verificables** — Sin métricas inventadas ni claims genéricos.
4. **Copy corporativo vacío** — Concreto y específico siempre.
5. **Precios visibles** — No incluir precios en las service cards.
6. **Mobile sobrecargado** — No shrinkear desktop. Diseñar mobile con intención.
7. **Esconder secciones enteras en mobile** — Mostrar todo pero de forma inteligente.
8. **CTAs repetidos** — Variar el label según el contexto.
9. **Sticky button molesto** — Evitar.

### Principios de Mobile (CRÍTICO)

**La regla de oro:** No se trata de quitar cosas sin sentido, sino de usar visibilidad y layout creativamente.

- H1 desktop largo → versión corta en mobile (clases `.desktop-text` / `.mobile-short`)
- Features lists → mostrar solo top 3-4 en mobile
- Cards en grid → 1 columna en mobile
- Case studies → 1 compacto en mobile si hay varios
- Process outputs con box → solo texto en mobile
- CTAs variados: nunca el mismo label en todos lados

### Qué Funciona Bien (mantener o evolucionar)
- Timeline vertical para el proceso (Audit → Design → Build → Evolve)
- Pain points con diseño editorial (no bullet list básica)
- Stats con contexto pequeño debajo
- Microcopy útil: "No pitch.", contexto de stats
- Gradiente oscuro para secciones de contraste
- Service numbers grandes en esquina
- Desktop/mobile text alternativo con clases CSS

### Setup de Deployment
```bash
git add index.html consulting.html products.html
git commit -m "..."
git push origin main
# Cloudflare Pages hace deploy automático desde main
```
