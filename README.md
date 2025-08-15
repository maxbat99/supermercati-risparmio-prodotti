# Supermercati — Sito clienti (Netlify)
- Frontend statico: cartella `site/`
- API: FastAPI su URL configurabile (in locale prova porte 8000..8010, in produzione inserisci l’URL nel box in home).
- Deploy: Netlify (publish = `site`), collegato al repo GitHub o via Netlify CLI.

## Deploy con Netlify CLI
1) Install: `npm i -g netlify-cli`
2) Login: `netlify login`
3) Deploy preview: `netlify deploy --dir=site`
4) Deploy prod: `netlify deploy --prod --dir=site`
