def render_mermaid_to_image(mermaid_code: str, output_path: str) -> bool:
import os
import subprocess
def render_mermaid_to_image(mermaid_code: str, output_path: str) -> bool:
    """
    Render Mermaid code to an image using local mermaid-cli (requires Node.js and mermaid-cli installed).
    """
    try:
        temp_mmd = output_path + ".mmd"
        with open(temp_mmd, "w", encoding="utf-8") as f:
            f.write(mermaid_code)
        # Render to SVG using mermaid-cli
        result = subprocess.run([
            "mmdc", "-i", temp_mmd, "-o", output_path, "-b", "transparent"
        ], capture_output=True, text=True)
        os.remove(temp_mmd)
        return result.returncode == 0
    except Exception as e:
        print(f"Local Mermaid render failed: {e}")
    return False
