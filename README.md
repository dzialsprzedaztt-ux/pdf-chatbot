# 🤖 PDF Chatbot – Asystent dokumentów

Chatbot działający w przeglądarce, który odpowiada na pytania na podstawie Twoich PDF-ów.
**Hosting: GitHub Pages · Backend: bezpośrednio Claude API · Baza: pliki lokalne (JSON)**

---

## 📁 Struktura projektu

```
pdf-chatbot/
├── index.html          ← Strona WWW z widgetem czatu
├── knowledge.json      ← Baza wiedzy (generowana ze skryptu)
├── process_pdfs.py     ← Skrypt do przetwarzania PDF-ów
├── docs/               ← Tu wrzucasz swoje PDF-y
│   └── (twoje pliki.pdf)
└── README.md
```

---

## 🚀 Instrukcja krok po kroku

### Krok 1 – Sklonuj repozytorium

```bash
git clone https://github.com/TWOJ-LOGIN/pdf-chatbot.git
cd pdf-chatbot
```

### Krok 2 – Wrzuć swoje PDF-y

Skopiuj pliki PDF do folderu `docs/`:

```bash
cp /ścieżka/do/twojego/plik.pdf docs/
```

### Krok 3 – Przetwórz PDF-y

Zainstaluj zależności i uruchom skrypt:

```bash
pip install pymupdf
python process_pdfs.py
```

Skrypt stworzy plik `knowledge.json` z treścią Twoich dokumentów.

### Krok 4 – Wgraj na GitHub

```bash
git add .
git commit -m "Dodaję dokumenty do bazy wiedzy"
git push
```

### Krok 5 – Włącz GitHub Pages

1. Wejdź na GitHub → repozytorium → **Settings**
2. Sekcja **Pages** → Source: **Deploy from a branch**
3. Branch: `main`, folder: `/ (root)` → **Save**
4. Po chwili strona będzie dostępna pod adresem:
   `https://TWOJ-LOGIN.github.io/pdf-chatbot/`

### Krok 6 – Użyj chatbota

1. Wejdź na stronę GitHub Pages
2. Wpisz swój klucz **Anthropic API** (uzyskasz go na [console.anthropic.com](https://console.anthropic.com))
3. Zadawaj pytania!

---

## 🔑 Jak zdobyć klucz API?

1. Zarejestruj się na [console.anthropic.com](https://console.anthropic.com)
2. Wejdź w **API Keys** → **Create Key**
3. Skopiuj klucz (zaczyna się od `sk-ant-...`)
4. Wklej go w pole na stronie chatbota

> ⚠️ **Bezpieczeństwo:** Klucz jest przechowywany tylko w pamięci przeglądarki (sessionStorage) i nie jest nigdzie wysyłany poza API Anthropic. Nie commituj klucza do repozytorium!

---

## ⚙️ Konfiguracja skryptu

W pliku `process_pdfs.py` możesz zmienić:

```python
CHUNK_SIZE    = 500   # Rozmiar fragmentu (znaków) — więcej = więcej kontekstu
CHUNK_OVERLAP = 80    # Nakładanie fragmentów — zapobiega ucięciu zdań
```

---

## 🔄 Aktualizacja dokumentów

Gdy chcesz dodać nowe PDF-y:

```bash
cp nowy_plik.pdf docs/
python process_pdfs.py
git add knowledge.json
git commit -m "Aktualizacja bazy wiedzy"
git push
```

---

## 🛠️ Wymagania

- Python 3.8+
- `pymupdf` (`pip install pymupdf`)
- Konto GitHub
- Klucz Anthropic API

---

## 📝 Licencja

MIT – używaj swobodnie w projektach prywatnych i komercyjnych.
