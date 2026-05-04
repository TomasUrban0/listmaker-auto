# listmaker-auto

Automatización del pipeline de scraping + descarga de PDFs + sincronización con Google Drive, ejecutándose como cron en GitHub Actions.

Origen: port del notebook `listmaker.ipynb` a scripts ejecutables en CI.

## Arquitectura

```
GitHub Actions (cron diario)
        │
        ▼
  ┌─────────────┐
  │  download   │  baja estado previo (history, cookies, Artists/) desde Drive
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │   scrape    │  ListMaker — recorre perfiles, detecta cambios → deltas.jsonl
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │   write     │  Writer — descarga PDFs de capítulos nuevos
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │   upload    │  sube todo de vuelta a Drive
  └─────────────┘
```

## Estructura

```
src/             módulos del pipeline
scripts/         entry points (uno por etapa)
lists/           estado runtime (gitignored, vive en Drive)
.github/workflows/listmaker.yml   cron de GitHub Actions
```

## Secretos requeridos en GitHub

| Secret                        | Qué es                                                       |
|-------------------------------|--------------------------------------------------------------|
| `GDRIVE_OAUTH_CLIENT_ID`      | OAuth Client ID (Desktop app) creado en GCP                  |
| `GDRIVE_OAUTH_CLIENT_SECRET`  | OAuth Client Secret correspondiente                          |
| `GDRIVE_OAUTH_REFRESH_TOKEN`  | Refresh token obtenido con `scripts/auth_oauth.py` (1 vez)   |
| `ARTISTS_FOLDER_ID`           | ID de la carpeta `Artists` en Drive                          |
| `QQ_COOKIES_B64`              | `qq_verified_session.cookies` codificado en base64           |
| `ARTISTS_TXT_B64`             | (opcional) `artists.txt` en base64 si no quieres versionarlo |
| `GDRIVE_SA_JSON`              | (opcional, fallback) JSON de Service Account                 |

**Por qué OAuth user y no Service Account**: las SAs no tienen cuota de
almacenamiento propia, así que pueden actualizar archivos existentes pero
no crear nuevos en Drive personal. Eso rompe el upload de PDFs nuevos y de
`deltas.jsonl`. OAuth user delegation usa la cuota del usuario y funciona.

## Tareas pendientes

- [ ] Portar clases del notebook a módulos en `src/`
- [ ] Cambiar auth de Drive a Service Account (PyDrive2 lo soporta)
- [ ] Entry points en `scripts/` (`download.py`, `scrape.py`, `write.py`, `upload.py`)
- [ ] Workflow YAML con cron + secretos
- [ ] Notificación de fallo (email nativo de GH Actions o webhook)
