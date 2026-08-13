# Nature's Rhythm Yoga — repo working agreement

Static landing page for Nature's Rhythm Yoga (200hr teacher training),
hosted on Cloudflare Workers as static assets. Everything served lives in
`public/`; `wrangler.jsonc` points at it; there is no build step. Cloudflare
Workers Builds redeploys automatically on every push to `main`.

## Before committing — always

    git config user.name "Fid" && git config user.email "fid_kk@proton.me"

## Branches and releases

- Develop on the session's assigned working branch and push there first.
- Standing policy from the repo owner: completed, verified work is released
  by fast-forwarding `main` onto the working branch and pushing `main`.
  Every push to `main` is a release.
- Work in small, complete batches: implement, verify, then commit and
  push — never leave pushed work unverified or half-finished.

## Versioning

- Ascending vMAJOR.MINOR sequence (v1.0, v1.1, v1.2 …). Every push to
  `main` increments the minor by one, regardless of size. A major bump is
  reserved for a ground-up overhaul of the project.
- To find the next number: check existing tags and releases on GitHub and
  the ledger below; take the highest, plus one minor.
- With every push to `main`, provide release-tag text in the chat reply,
  in exactly this shape — the repo owner creates the GitHub release
  manually from it, so never push tags:

      Tag: v<next>  —  Title: <five to nine words, plain and evocative>
      Description: <one to three sentences of editorial prose describing
      what changed from the user's point of view — outcomes, not
      implementation. No bullet lists, no jargon, no file names.>

- Append the release's line to the ledger below as part of the same push.

## Commit style

- Descriptive imperative first line (what the change does, not
  "update X"), then a short prose body — dash bullets are fine there —
  explaining what changed and why it matters.
- One commit per coherent piece of work; multiple commits may share a
  push, but each push gets exactly one version entry.
- Never include model names, AI attribution trailers, session links, or
  other tooling identifiers in commit messages, titles, or code.

## Release ledger

- v1.0 — Nature's Rhythm Yoga arrives on the web
- v1.1 — The project learns how it ships
- v1.2 — The logo lettering shines white and clear
- v1.3 — A moonlit card for shared links
