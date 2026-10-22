# SolarSentinel Frontend

Responsive HTML/CSS/JavaScript dashboard for the InnoTech SolarSentinel project.

## Run locally
1. Extract the ZIP.
2. Open `index.html` in Chrome/Edge, or use VS Code Live Server.
3. Upload a thermal image and click **Analyze image**.
4. The default demo mode shows a simulated UI result so you can demonstrate the frontend before the ML API is ready.

**Important:** Demo mode is not a real AI prediction. It generates a sample status and displays a visual marker on the uploaded image. The actual highlighted thermal region and prediction must come from your model/API.

## Connect Member 3's API
In `script.js`:
```js
const API_URL = "http://127.0.0.1:8000/api/analyze";
const DEMO_MODE = false;
```
If frontend and backend use different ports, the backend must enable CORS for the frontend origin.

### Expected API
The frontend sends `multipart/form-data` with the image under the field name `file`.

Example JSON response:
```json
{
  "status": "Anomaly",
  "confidence": 0.92,
  "severity": "Medium",
  "summary": "A suspicious hotspot region was detected.",
  "recommendation": "Arrange a closer inspection by a qualified technician.",
  "highlighted_image_url": "http://127.0.0.1:8000/results/annotated-image.png"
}
```
For the frontend, `confidence` should be a number from 0 to 100. If your model returns a 0-to-1 probability (e.g. `0.92`), convert it to percentage before sending it, or update `renderResult()` to multiply by 100. `highlighted_image_url` is optional; when present, it should be a URL accessible by the browser. If absent, the frontend displays a demo marker rather than a genuine model-generated heatmap.

## Features
- Responsive overview dashboard and summary cards
- Thermal image upload, preview, drag-and-drop and size/type checks
- Analysis results, confidence, severity and recommendation
- Original/highlighted image comparison
- Inspection history, status filter and CSV export
//readme