# Perpetual Design System 5 — Infografías ejecutivas

Repositorio autocontenido con una plantilla de presentación de **Perpetual Technologies** en HTML, enfocada en infografías ejecutivas (estilo BCG/McKinsey). Genera un único archivo `.html` que embebe la tipografía Armin Grotesk (base64) y los logos SVG inline, de modo que puede abrirse en cualquier navegador o conectarse a herramientas de diseño sin dependencias externas.

## Qué es

`perpetual-infographics.html` es un deck de 10 slides (1280 x 720) con plantillas de infografía reutilizables:

1. **Portada** — H1 "Infografías ejecutivas" con composición de marca (círculo azul, hexágono, círculos amarillo/naranja).
2. **Cinco opciones** — 5 formas numeradas 01-05 en fila, cada una con título y descripción.
3. **Proceso de crecimiento** — gráfica de línea ascendente (SVG) con 3 hitos etiquetados.
4. **Mapa de información** — mind-map con nodo central (hexágono) y 4 tarjetas INFODATA conectadas.
5. **Indicadores clave** — 4 hexágonos de métricas con "Millón usuarios".
6. **Estructura creativa** — org chart con nodo CREATIVO y 3 hijos (Equipo, Estrategia, Negocio).
7. **Flujo en seis pasos** — 6 tarjetas numeradas 01-06 en abanico.
8. **Pirámide de audiencia** — 4 niveles apilados con leyenda de porcentajes.
9. **Línea de tiempo** — timeline horizontal con 4 hitos (1996, 2003, 2015, 2021).
10. **Pilares de valor** — 4 iconos circulares (Inversión, Estrategia, Crecimiento, Creatividad).

Todos los slides incluyen el logo Perpetual y usan exclusivamente Armin Grotesk. Sin fotos de personas: solo formas de marca (hexágonos, círculos, paneles tintados).

## Estructura

```
.
├── assets/
│   ├── fonts/        Armin Grotesk (.otf): Normal, Regular, Semi_Bold, Black
│   └── logo/         Logos SVG (color y dark)
├── build_html.py     Generador del HTML (helpers, tokens, slides)
└── perpetual-infographics.html   Salida generada (autocontenida)
```

## Regenerar

```bash
python3 build_html.py
```

Imprime `OK`, el tamaño del archivo y el número de slides. La salida se escribe en `perpetual-infographics.html`.

## Tokens de marca

- Acento: `#1a56db` (azul), `#f97316` (naranja), `#fbb900` (amarillo)
- Paleta de datos adicional: `#059669` (verde), `#7e22ce` (violeta), `#6b7280` (gris)
- Fondos claros en blanco; oscuros en `#0b1220`
- Coordenadas en pulgadas x 96 sobre un lienzo de 13.333 x 7.5 in

## Nota

El HTML es **autocontenido** (fuentes y logos embebidos), pensado para inspeccionarse en navegador y conectarse a herramientas de diseño (Figma, Canva, etc.) sin recursos externos.
