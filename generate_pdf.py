#!/usr/bin/env python3
"""
Script to convert PROJECT_DOCUMENTATION.md to PDF
Requires: pip install markdown pdfkit weasyprint
Alternative: Use pandoc if available
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required tools are available"""
    try:
        import markdown
        print("✅ markdown library available")
    except ImportError:
        print("❌ markdown library not found. Install with: pip install markdown")
        return False
    
    # Check for pandoc (preferred method)
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ pandoc available")
            return 'pandoc'
    except FileNotFoundError:
        print("ℹ️  pandoc not found, checking alternatives...")
    
    # Check for weasyprint
    try:
        import weasyprint
        print("✅ weasyprint available")
        return 'weasyprint'
    except ImportError:
        print("ℹ️  weasyprint not found, checking alternatives...")
    
    # Check for pdfkit + wkhtmltopdf
    try:
        import pdfkit
        # Check if wkhtmltopdf is installed
        subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, text=True)
        print("✅ pdfkit + wkhtmltopdf available")
        return 'pdfkit'
    except (ImportError, FileNotFoundError):
        print("ℹ️  pdfkit/wkhtmltopdf not found")
    
    print("\n❌ No PDF generation tools found!")
    print("\nInstallation options:")
    print("1. pandoc (recommended): brew install pandoc")
    print("2. weasyprint: pip install weasyprint")
    print("3. pdfkit: pip install pdfkit && brew install wkhtmltopdf")
    return False

def convert_with_pandoc(input_file, output_file):
    """Convert using pandoc (best quality)"""
    cmd = [
        'pandoc',
        str(input_file),
        '-o', str(output_file),
        '--pdf-engine=xelatex',
        '-V', 'geometry:margin=1in',
        '-V', 'fontsize=10pt',
        '--toc',
        '--toc-depth=3',
        '--highlight-style=github'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ PDF generated successfully: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Pandoc conversion failed: {e}")
        print("Stderr:", e.stderr)
        return False

def convert_with_weasyprint(input_file, output_file):
    """Convert using weasyprint"""
    import markdown
    import weasyprint
    
    # Read markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html = markdown.markdown(
        md_content,
        extensions=['codehilite', 'fenced_code', 'tables', 'toc']
    )
    
    # Add CSS styling
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3, h4 {{
                color: #2c3e50;
                margin-top: 2em;
            }}
            h1 {{
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                border-bottom: 1px solid #bdc3c7;
                padding-bottom: 5px;
            }}
            code {{
                background-color: #f8f9fa;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Monaco', 'Consolas', monospace;
            }}
            pre {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                border-left: 4px solid #3498db;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px 12px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            blockquote {{
                border-left: 4px solid #3498db;
                margin: 0;
                padding-left: 20px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    
    # Generate PDF
    try:
        weasyprint.HTML(string=styled_html).write_pdf(str(output_file))
        print(f"✅ PDF generated successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ WeasyPrint conversion failed: {e}")
        return False

def convert_with_pdfkit(input_file, output_file):
    """Convert using pdfkit"""
    import markdown
    import pdfkit
    
    # Read markdown
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html = markdown.markdown(
        md_content,
        extensions=['codehilite', 'fenced_code', 'tables', 'toc']
    )
    
    # Add CSS styling
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
            h1, h2, h3 {{ color: #333; }}
            code {{ background-color: #f4f4f4; padding: 2px 4px; }}
            pre {{ background-color: #f4f4f4; padding: 10px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    
    # Configure options
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    
    try:
        pdfkit.from_string(styled_html, str(output_file), options=options)
        print(f"✅ PDF generated successfully: {output_file}")
        return True
    except Exception as e:
        print(f"❌ pdfkit conversion failed: {e}")
        return False

def main():
    print("🚀 AI E-Commerce Project Documentation PDF Generator")
    print("=" * 60)
    
    # File paths
    input_file = Path("PROJECT_DOCUMENTATION.md")
    output_file = Path("AI_E-Commerce_Complete_Guide.pdf")
    
    # Check if input file exists
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return 1
    
    # Check dependencies
    method = check_dependencies()
    if not method:
        return 1
    
    print(f"\n📄 Converting {input_file} to {output_file}")
    print(f"🔧 Using method: {method}")
    
    # Convert based on available method
    success = False
    if method == 'pandoc':
        success = convert_with_pandoc(input_file, output_file)
    elif method == 'weasyprint':
        success = convert_with_weasyprint(input_file, output_file)
    elif method == 'pdfkit':
        success = convert_with_pdfkit(input_file, output_file)
    
    if success:
        print(f"\n🎉 Success! PDF generated: {output_file.absolute()}")
        print(f"📊 File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")
        return 0
    else:
        print("\n❌ PDF generation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())