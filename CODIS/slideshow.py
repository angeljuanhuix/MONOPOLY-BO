"""
Generate an HTML page to display a slideshow of SVGs with navigation buttons.

Usage: python3 slideshow.py page.html *.svg
"""

import sys
import glob

def generate_slideshow(svgs: list[str]) -> str:
    if not svgs:
        return "<html><body><p>No SVGs to display</p></body></html>"

    escaped_paths = [path.replace("\\", "/").replace("'", "\\'") for path in svgs]
    paths_js = "[" + ", ".join(f"'{path}'" for path in escaped_paths) + "]"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Monopoly Viewer</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }}
        .container {{
            text-align: center;
            background-color: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        #svg-display {{
            max-width: 90vw;
            max-height: 85vh;
        }}
        .controls {{
            margin-top: 0px;
        }}
        button {{
            font-size: 32px;
            cursor: pointer;
            border: none;
            border-radius: 4px;
            background-color: #4CAF50;
            color: white;
        }}
        button:hover {{
            background-color: #45a049;
        }}
        button:disabled {{
            background-color: #cccccc;
            cursor: not-allowed;
        }}
        .info {{
            margin-top: 10px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <img id="svg-display" src="{escaped_paths[0]}" alt="SVG Image">
        <div class="controls">
            <button id="btn-first" onclick="goToFirst()">⏮️</button>
            <button id="btn-prev" onclick="goToPrev()">⬅️</button>
            <button id="btn-next" onclick="goToNext()">➡️</button>
            <button id="btn-last" onclick="goToLast()">⏭️</button>
        </div>
        <div class="info">
            <span id="current-info">1 / {len(svgs)}</span>
        </div>
    </div>
    
    <script>
        const svgPaths = {paths_js};
        let currentIndex = 0;
        
        function updateDisplay() {{
            const img = document.getElementById('svg-display');
            img.src = svgPaths[currentIndex];
            
            document.getElementById('current-info').textContent = 
                (currentIndex + 1) + ' / ' + svgPaths.length;
            
            document.getElementById('btn-first').disabled = currentIndex === 0;
            document.getElementById('btn-prev').disabled = currentIndex === 0;
            document.getElementById('btn-next').disabled = currentIndex === svgPaths.length - 1;
            document.getElementById('btn-last').disabled = currentIndex === svgPaths.length - 1;
        }}
        
        function goToFirst() {{ currentIndex = 0; updateDisplay(); }}
        function goToPrev() {{ if (currentIndex > 0) {{ currentIndex--; updateDisplay(); }} }}
        function goToNext() {{ if (currentIndex < svgPaths.length - 1) {{ currentIndex++; updateDisplay(); }} }}
        function goToLast() {{ currentIndex = svgPaths.length - 1; updateDisplay(); }}
        
        updateDisplay();
    </script>
</body>
</html>"""
    return html


def main() -> None:
    # Ara el programa només necessita saber el nom de l'arxiu HTML
    page = sys.argv[1]
    
    # Oblidem la terminal. Python busca directament a la carpeta "images"
    rutes = glob.glob("images/*.svg")
    svgs = [f.replace('\\', '/') for f in rutes]
    
    if not svgs:
        print("ERROR: No s'ha trobat cap imatge a la carpeta 'images/'.")
        print("Assegura't que la carpeta 'images' està al mateix lloc que slideshow.py")
        return
            
    svgs.sort()

    html = generate_slideshow(svgs)
    with open(page, "w", encoding = "UTF-8") as f:
        f.write(html)
        
    print(f"ÈXIT! S'ha creat '{page}' amb {len(svgs)} imatges.")

if __name__ == "__main__":
    main()