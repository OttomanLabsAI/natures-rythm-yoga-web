# Nature's Rhythm Yoga — website

Landing page for the Nature's Rhythm Yoga 200-hour teacher training at
[Yoga in the Stars](https://maps.google.com/?q=344+Grove+Green+Road,+Leytonstone,+London+E11+4EA),
Leytonstone. A static site built for hosting on Cloudflare.

## Structure

```
public/                  ← everything that gets served
  index.html             ← the landing page
  404.html               ← custom not-found page
  favicon.svg
  robots.txt
  _headers               ← security & caching headers (Cloudflare)
  assets/
    css/styles.css
    js/main.js
wrangler.jsonc           ← Cloudflare Workers (static assets) config
package.json
```

No build step — the files in `public/` are served as-is.

## Local development

```sh
npm install
npm run dev          # serves the site with wrangler at http://localhost:8787
```

(Any static file server pointed at `public/` also works.)

## Deploying to Cloudflare

Two equivalent options — pick one:

### Option A — Workers with static assets (recommended, configured here)

**Via the dashboard (Git integration):** Cloudflare dashboard → **Workers & Pages →
Create → Workers → Import a repository**, select this repo. The included
`wrangler.jsonc` is picked up automatically; no build command is needed
(deploy command: `npx wrangler deploy`). Every push to the production branch
deploys, and other branches get preview URLs.

**Via the CLI:**

```sh
npx wrangler login
npm run deploy
```

### Option B — Cloudflare Pages

Dashboard → **Workers & Pages → Create → Pages → Connect to Git**, select this
repo, leave the build command empty and set the **build output directory** to
`public`. The `_headers` and `404.html` files are honoured by Pages too.

After the first deploy, add the custom domain under the project's
**Settings → Domains & Routes** (Workers) or **Custom domains** (Pages).

## Notes

- **Media is loaded from the existing site.** The logo, studio photo and
  community video are referenced from `naturesrhythmyoga.com` (WordPress
  uploads). To make this site fully self-contained, download those files into
  `public/assets/img/` / `public/assets/video/` and update the URLs in
  `public/index.html`.
- **Forms are front-end only.** The open-day RSVP and free-session forms show a
  confirmation message but don't send data anywhere yet. Wire them to a backend
  (e.g. a Worker handler + email/API, or a form service) before relying on them.
- Fonts (Fraunces, Karla) are served from Google Fonts.
