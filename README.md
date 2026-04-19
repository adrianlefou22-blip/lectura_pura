# Lectura Pura — APK

## Pasos para generar el APK desde el teléfono

### 1. Crear cuenta en GitHub (si no tenés)
- github.com → Sign up → gratis

### 2. Crear repositorio nuevo
- github.com → "+" arriba a la derecha → "New repository"
- Nombre: `lectura-pura`
- Visibility: **Public** (necesario para Actions gratuito)
- NO tildar ningún checkbox
- Create repository

### 3. Subir los archivos
GitHub desde el teléfono permite subir archivos así:
- Abrís el repositorio vacío
- Tocás "uploading an existing file"
- Subís TODOS los archivos y carpetas de este ZIP
- En el commit message escribís: `primer commit`
- Tocás "Commit changes"

**Importante**: la carpeta `.github/workflows/build.yml` debe subirse
con esa estructura de carpetas exacta.

### 4. Ver cómo compila
- En el repositorio tocás la pestaña **Actions**
- Vas a ver "Build Lectura Pura APK" corriendo
- Tarda 5-10 minutos
- Cuando termina aparece ✅ verde

### 5. Descargar el APK
- Tocás en el workflow que terminó
- Abajo en "Artifacts" aparece **LecturaPura-APK**
- Lo descargás → es un ZIP que contiene el APK

### 6. Instalar en el teléfono
- Abrís el ZIP descargado → `app-debug.apk`
- Android pregunta si querés instalar de fuentes desconocidas
- Aceptás → Instalar

### 7. Configuración final (OBLIGATORIO)
- Ajustes → Aplicaciones → Lectura Pura → Batería → **Sin restricciones**
- Ajustes → Batería → Optimización → Lectura Pura → **No optimizar**

---

## Por qué este APK funciona con pantalla bloqueada

Este APK tiene en su AndroidManifest.xml:
- `WAKE_LOCK` — mantiene la CPU activa
- `FOREGROUND_SERVICE` — proceso en primer plano real
- `FOREGROUND_SERVICE_MEDIA_PLAYBACK` — prioridad de audio del sistema
- `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` — inmune a optimización de batería

Estos permisos son imposibles de tener en una PWA o browser.
