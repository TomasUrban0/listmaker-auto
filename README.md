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

| Secret              | Qué es                                                       |
|---------------------|--------------------------------------------------------------|
| `GDRIVE_SA_JSON`    | JSON de la Service Account con acceso a la carpeta `Artists` |
| `ARTISTS_FOLDER_ID` | ID de la carpeta `Artists` en Drive (la SA no la ve bajo `root`) |
| `QQ_COOKIES_B64`    | `qq_verified_session.cookies` codificado en base64           |
| `ARTISTS_TXT_B64`   | (opcional) `artists.txt` en base64 si no quieres versionarlo |

## Tareas pendientes

- [ ] Portar clases del notebook a módulos en `src/`
- [ ] Cambiar auth de Drive a Service Account (PyDrive2 lo soporta)
- [ ] Entry points en `scripts/` (`download.py`, `scrape.py`, `write.py`, `upload.py`)
- [ ] Workflow YAML con cron + secretos
- [ ] Notificación de fallo (email nativo de GH Actions o webhook)
