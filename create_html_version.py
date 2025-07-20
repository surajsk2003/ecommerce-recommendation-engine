#!/usr/bin/env python3
"""
Simple script to convert PROJECT_DOCUMENTATION.md to HTML
Then you can print to PDF from your browser
"""

import os
import sys
from pathlib import Path

def convert_markdown_to_html():
    """Convert markdown to HTML with styling"""
    
    input_file = Path("PROJECT_DOCUMENTATION.md")
    output_file = Path("AI_E-Commerce_Complete_Guide.html")
    
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return False
    
    # Read the markdown file
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Create HTML with embedded CSS
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI E-Commerce Recommendation Engine - Complete Guide</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 
                        'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #fff;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-top: 40px;
            font-size: 2.5em;
        }}
        
        h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #bdc3c7;
            padding-bottom: 10px;
            margin-top: 35px;
            font-size: 2em;
        }}
        
        h3 {{
            color: #34495e;
            margin-top: 30px;
            font-size: 1.5em;
        }}
        
        h4 {{
            color: #34495e;
            margin-top: 25px;
            font-size: 1.2em;
        }}
        
        p {{
            margin-bottom: 16px;
            text-align: justify;
        }}
        
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
            font-size: 0.9em;
            color: #e74c3c;
        }}
        
        pre {{
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            color: #2c3e50;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding-left: 20px;
            color: #666;
            font-style: italic;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px 15px;
            text-align: left;
        }}
        
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        
        ul, ol {{
            margin-bottom: 16px;
            padding-left: 30px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        .toc {{
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin: 30px 0;
        }}
        
        .toc h2 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 1px solid #bdc3c7;
        }}
        
        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        
        .toc ul ul {{
            padding-left: 20px;
        }}
        
        .toc a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        .toc a:hover {{
            text-decoration: underline;
        }}
        
        .highlight {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
        }}
        
        .note {{
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
        }}
        
        .warning {{
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
        }}
        
        @media print {{
            body {{
                margin: 0;
                padding: 20px;
                font-size: 12pt;
            }}
            
            h1 {{
                page-break-before: always;
                font-size: 18pt;
            }}
            
            h2 {{
                page-break-before: avoid;
                font-size: 16pt;
            }}
            
            h3 {{
                font-size: 14pt;
            }}
            
            pre, code {{
                page-break-inside: avoid;
            }}
            
            table {{
                page-break-inside: avoid;
            }}
            
            .toc {{
                page-break-after: always;
            }}
        }}
    </style>
</head>
<body>
"""
    
    # Simple markdown-to-HTML conversion
    lines = markdown_content.split('\n')
    html_lines = []
    in_code_block = False
    code_language = ""
    
    for line in lines:
        # Handle code blocks
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                code_language = line[3:].strip()
                html_lines.append(f'<pre><code class="{code_language}">')
                in_code_block = True
            continue
        
        if in_code_block:
            # Escape HTML in code blocks
            escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html_lines.append(escaped_line)
            continue
        
        # Handle headers
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{line[5:]}</h4>')
        
        # Handle lists
        elif line.startswith('- ') or line.startswith('* '):
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.startswith('1. '):
            html_lines.append(f'<li>{line[3:]}</li>')
        
        # Handle tables
        elif '|' in line and line.strip().startswith('|'):
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if all(cell in ['---', ':---', '---:', ':---:'] or cell.startswith('-') for cell in cells):
                # Skip table separator line
                continue
            else:
                # Check if this is likely a header row (next line is separator)
                row_html = '<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>'
                html_lines.append(row_html)
        
        # Handle bold and italic
        elif '**' in line or '*' in line or '`' in line:
            # Simple replacements for common markdown
            formatted_line = line
            formatted_line = formatted_line.replace('**', '<strong>').replace('**', '</strong>')
            formatted_line = formatted_line.replace('`', '<code>').replace('`', '</code>')
            html_lines.append(f'<p>{formatted_line}</p>')
        
        # Regular paragraphs
        elif line.strip():
            html_lines.append(f'<p>{line}</p>')
        
        # Empty lines
        else:
            html_lines.append('<br>')
    
    # Combine HTML
    html_content += '\n'.join(html_lines)
    html_content += """
</body>
</html>
"""
    
    # Write HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML file created: {output_file.absolute()}")
    return True

def main():
    print("🚀 AI E-Commerce Documentation HTML Generator")
    print("=" * 50)
    
    success = convert_markdown_to_html()
    
    if success:
        print("\n🎉 HTML file generated successfully!")
        print("\n📋 To create PDF:")
        print("1. Open the HTML file in your browser")
        print("2. Press Cmd+P (Mac) or Ctrl+P (Windows)")
        print("3. Choose 'Save as PDF'")
        print("4. Select appropriate options:")
        print("   - Layout: Portrait")
        print("   - Margins: Default or Minimum")
        print("   - Background graphics: ✓ (to include styling)")
        print("\n🌟 The HTML file includes:")
        print("- Professional styling")
        print("- Print-optimized CSS")
        print("- Syntax highlighting")
        print("- Responsive design")
        
        # Try to open the file
        html_file = Path("AI_E-Commerce_Complete_Guide.html").absolute()
        print(f"\n📖 Open in browser: file://{html_file}")
        
        return 0
    else:
        print("❌ Failed to generate HTML file")
        return 1

if __name__ == "__main__":
    sys.exit(main())