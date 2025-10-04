#!/usr/bin/env python3
"""
Documentation generator for PKI open-source website
Converts Markdown files to HTML with navigation and styling
"""

import os
import re
import markdown
from pathlib import Path
from datetime import datetime

# Configuration
PKIAAS_DOCS_PATH = "/home/rdem/git/pkiaas/docs"
OUTPUT_PATH = "/home/rdem/git/pki-opensource/docs"
TEMPLATE_PATH = "/home/rdem/git/pki-opensource"

# HTML Template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - PKI Documentation</title>
    <meta name="description" content="{description}">

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        primary: {{
                            50: '#EEF2FF',
                            100: '#E0E7FF',
                            200: '#C7D2FE',
                            300: '#A5B4FC',
                            400: '#818CF8',
                            500: '#1E3A8A',
                            600: '#1E40AF',
                            700: '#1E3A8A',
                            800: '#1E3A8A',
                            900: '#1E3A8A'
                        }}
                    }}
                }}
            }}
        }}
    </script>

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">

    <!-- Prism.js for syntax highlighting -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">

    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        h1, h2, h3, h4 {{ font-family: 'Poppins', sans-serif; }}
        code, pre {{ font-family: 'Fira Code', monospace; }}

        .prose h1 {{ @apply text-4xl font-bold text-gray-900 mb-6 mt-8; }}
        .prose h2 {{ @apply text-3xl font-bold text-gray-900 mb-4 mt-6; }}
        .prose h3 {{ @apply text-2xl font-bold text-gray-900 mb-3 mt-5; }}
        .prose h4 {{ @apply text-xl font-semibold text-gray-900 mb-2 mt-4; }}
        .prose p {{ @apply text-gray-700 mb-4 leading-relaxed; }}
        .prose ul {{ @apply list-disc list-inside mb-4 text-gray-700; }}
        .prose ol {{ @apply list-decimal list-inside mb-4 text-gray-700; }}
        .prose li {{ @apply mb-2; }}
        .prose a {{ @apply text-primary-700 hover:text-primary-900 underline; }}
        .prose code {{ @apply bg-gray-100 px-2 py-1 rounded text-sm text-gray-800; }}
        .prose pre {{ @apply bg-gray-900 p-4 rounded-lg overflow-x-auto mb-4; }}
        .prose pre code {{ @apply bg-transparent px-0 py-0 text-gray-100; }}
        .prose blockquote {{ @apply border-l-4 border-primary-500 pl-4 italic text-gray-700 mb-4; }}
        .prose table {{ @apply w-full border-collapse mb-4; }}
        .prose th {{ @apply bg-primary-100 text-primary-900 font-semibold p-2 border border-gray-300; }}
        .prose td {{ @apply p-2 border border-gray-300; }}

        /* Sidebar active link */
        .nav-link.active {{ @apply bg-primary-100 text-primary-900 font-semibold; }}
    </style>
</head>
<body class="bg-gray-50">
    <!-- Top Navigation -->
    <nav class="bg-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex items-center space-x-3">
                    <a href="/index.html" class="flex items-center space-x-3">
                        <svg class="h-8 w-8 text-primary-700" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
                        </svg>
                        <span class="text-2xl font-bold text-primary-700">PKI</span>
                    </a>
                </div>
                <div class="hidden md:flex space-x-8">
                    <a href="/index.html" class="text-gray-700 hover:text-primary-700">Home</a>
                    <a href="/docs/README.html" class="text-gray-700 hover:text-primary-700">Documentation</a>
                    <a href="https://github.com/rdemsystems/pki" target="_blank" class="text-gray-700 hover:text-primary-700">GitHub</a>
                    <a href="https://www.rdem-systems.com/contact" class="bg-primary-700 text-white px-4 py-2 rounded-md hover:bg-primary-800">Support</a>
                </div>
            </div>
        </div>
    </nav>

    <div class="flex">
        <!-- Sidebar Navigation -->
        <aside class="w-64 bg-white shadow-lg min-h-screen sticky top-16 overflow-y-auto">
            <div class="p-6">
                <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Documentation</h3>
                <nav class="space-y-1">
                    {navigation}
                </nav>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 p-8 max-w-4xl">
            <div class="prose">
                {content}
            </div>

            <!-- Footer -->
            <footer class="mt-12 pt-8 border-t border-gray-200 text-sm text-gray-600">
                <p>Last updated: {date}</p>
                <p class="mt-2">
                    <a href="https://github.com/rdemsystems/pki" target="_blank" class="text-primary-700 hover:text-primary-900">Edit this page on GitHub</a>
                </p>
            </footer>
        </main>
    </div>

    <!-- Prism.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-php.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
</body>
</html>
"""


def generate_navigation(docs_structure, current_path=""):
    """Generate sidebar navigation HTML"""
    nav_html = []

    for category, items in docs_structure.items():
        nav_html.append(f'<div class="mb-4">')
        nav_html.append(f'<h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">{category}</h4>')

        for item in items:
            active_class = "active" if item['path'] == current_path else ""
            nav_html.append(f'<a href="{item["path"]}" class="nav-link block px-3 py-2 rounded-md text-sm text-gray-700 hover:bg-gray-100 {active_class}">{item["title"]}</a>')

        nav_html.append('</div>')

    return '\n'.join(nav_html)


def convert_markdown_to_html(md_file_path, output_html_path, docs_structure):
    """Convert a single markdown file to HTML"""

    # Read markdown content
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract title from first H1
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "PKI Documentation"

    # Extract first paragraph for description
    desc_match = re.search(r'^(?!#)(.+)$', md_content, re.MULTILINE)
    description = desc_match.group(1)[:150] if desc_match else "PKI open-source documentation"

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc', 'tables', 'fenced_code'])
    html_content = md.convert(md_content)

    # Replace .md links with .html links
    html_content = re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', html_content)
    html_content = re.sub(r'href="([^"]+)\.md#', r'href="\1.html#', html_content)

    # Generate navigation
    relative_path = os.path.relpath(output_html_path, OUTPUT_PATH)
    navigation = generate_navigation(docs_structure, relative_path)

    # Fill template
    final_html = HTML_TEMPLATE.format(
        title=title,
        description=description,
        navigation=navigation,
        content=html_content,
        date=datetime.now().strftime("%Y-%m-%d")
    )

    # Write HTML file
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"✅ Generated: {output_html_path}")


def scan_documentation():
    """Scan documentation directory and build structure"""
    docs_structure = {}
    file_mapping = []

    for root, dirs, files in os.walk(PKIAAS_DOCS_PATH):
        for file in files:
            if file.endswith('.md'):
                md_path = os.path.join(root, file)
                relative_path = os.path.relpath(md_path, PKIAAS_DOCS_PATH)

                # Convert path to HTML
                html_relative = relative_path.replace('.md', '.html')
                html_path = os.path.join(OUTPUT_PATH, html_relative)

                # Extract category from directory
                parts = relative_path.split(os.sep)
                category = parts[0] if len(parts) > 1 else "General"

                # Get title from filename
                title = file.replace('.md', '').replace('-', ' ').replace('_', ' ').title()

                if category not in docs_structure:
                    docs_structure[category] = []

                docs_structure[category].append({
                    'title': title,
                    'path': '/docs/' + html_relative
                })

                file_mapping.append((md_path, html_path))

    return docs_structure, file_mapping


def main():
    """Main generation function"""
    print("🔨 PKI Documentation Generator")
    print("=" * 50)

    # Scan documentation
    print("\n📂 Scanning documentation...")
    docs_structure, file_mapping = scan_documentation()

    print(f"Found {len(file_mapping)} markdown files")

    # Generate HTML files
    print("\n🔄 Converting markdown to HTML...")
    for md_path, html_path in file_mapping:
        convert_markdown_to_html(md_path, html_path, docs_structure)

    print(f"\n✅ Generated {len(file_mapping)} HTML pages")
    print(f"📁 Output directory: {OUTPUT_PATH}")
    print("\n🚀 Ready to deploy!")


if __name__ == "__main__":
    main()
