#!/usr/bin/env python3
"""
process_pdfs.py – Przetwarza PDF-y z folderu /docs na plik knowledge.json
Wymagania: pip install pymupdf
"""

import json
import os
import sys
import re

# ─── KONFIGURACJA ───────────────────────────────────────────────
PDF_FOLDER   = "docs"          # Folder z plikami PDF
OUTPUT_FILE  = "knowledge.json" # Plik wyjściowy
CHUNK_SIZE   = 500             # Liczba znaków na fragment (możesz zmienić)
CHUNK_OVERLAP = 80             # Nakładanie się fragmentów
# ────────────────────────────────────────────────────────────────


def install_pymupdf():
    """Próbuje zainstalować pymupdf jeśli brakuje."""
    print("📦 Instaluję pymupdf...")
    os.system(f"{sys.executable} -m pip install pymupdf -q")


def extract_text_from_pdf(pdf_path: str) -> str:
    """Wyciąga tekst z PDF używając pymupdf."""
    try:
        import fitz  # pymupdf
    except ImportError:
        install_pymupdf()
        import fitz

    doc = fitz.open(pdf_path)
    texts = []
    for page in doc:
        text = page.get_text("text")
        if text.strip():
            texts.append(text)
    doc.close()
    return "\n".join(texts)


def clean_text(text: str) -> str:
    """Czyści tekst z nadmiarowych białych znaków."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n ', '\n', text)
    return text.strip()


def split_into_chunks(text: str, source: str) -> list[dict]:
    """Dzieli tekst na fragmenty z nakładaniem."""
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + CHUNK_SIZE
        chunk_text = text[start:end].strip()

        if chunk_text:
            # Staraj się kończyć na granicy zdania
            if end < text_len:
                last_dot = max(
                    chunk_text.rfind('. '),
                    chunk_text.rfind('.\n'),
                    chunk_text.rfind('! '),
                    chunk_text.rfind('? ')
                )
                if last_dot > CHUNK_SIZE * 0.5:
                    chunk_text = chunk_text[:last_dot + 1]

            chunks.append({
                "source": source,
                "text": chunk_text,
                "chunk_index": len(chunks)
            })

        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def main():
    print("=" * 55)
    print("  PDF → knowledge.json  ")
    print("=" * 55)

    # Sprawdź folder docs
    if not os.path.isdir(PDF_FOLDER):
        os.makedirs(PDF_FOLDER)
        print(f"\n📁 Utworzono folder '{PDF_FOLDER}/'")
        print(f"   ➜ Wrzuć tam swoje pliki PDF i uruchom skrypt ponownie.\n")
        return

    # Znajdź pliki PDF
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"\n⚠️  Brak plików PDF w folderze '{PDF_FOLDER}/'")
        print(f"   ➜ Wrzuć pliki PDF i uruchom skrypt ponownie.\n")
        return

    print(f"\n📄 Znaleziono {len(pdf_files)} plik(i/ów) PDF:")
    for f in pdf_files:
        print(f"   • {f}")

    # Przetwarzaj PDF-y
    all_chunks = []
    for filename in pdf_files:
        pdf_path = os.path.join(PDF_FOLDER, filename)
        print(f"\n🔄 Przetwarzam: {filename}")
        try:
            raw_text = extract_text_from_pdf(pdf_path)
            text = clean_text(raw_text)

            if not text:
                print(f"   ⚠️  Brak tekstu (PDF może być zeskanowany)")
                continue

            chunks = split_into_chunks(text, source=filename)
            all_chunks.extend(chunks)
            print(f"   ✅ {len(chunks)} fragmentów, {len(text)} znaków")

        except Exception as e:
            print(f"   ❌ Błąd: {e}")

    if not all_chunks:
        print("\n❌ Nie udało się przetworzyć żadnego pliku.")
        return

    # Zapisz do JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    # Podsumowanie
    sources = list({c['source'] for c in all_chunks})
    print("\n" + "=" * 55)
    print(f"✅ Gotowe! Zapisano do: {OUTPUT_FILE}")
    print(f"   Dokumenty : {len(sources)}")
    print(f"   Fragmenty : {len(all_chunks)}")
    print(f"   Rozmiar   : {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")
    print("=" * 55)
    print("\n🚀 Następny krok: wgraj knowledge.json na GitHub razem z index.html\n")


if __name__ == "__main__":
    main()
