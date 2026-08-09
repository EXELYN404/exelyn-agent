import streamlit as st
import re

# ---------------------------------------------------------
# INTERPRETER ENGINE (SUNDASCRIPT ENGINE)
# ---------------------------------------------------------
class SundaInterpreter:
    def __init__(self):
        self.variables = {}
        self.output = []

    def run(self, code):
        self.variables = {}
        self.output = []
        lines = code.split("\n")

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("//"):  # Abaikan baris kosong atawa komentar
                continue

            try:
                self.evaluate_line(line)
            except Exception as e:
                self.output.append(f"[SALAH dina Baris {line_num}]: {str(e)}")
                break

        return "\n".join(self.output)

    def evaluate_line(self, line):
        # 1. Perintah UCAP (Mencetak Teks)
        if line.startswith("UCAP "):
            text = line[5:].strip()
            if text.startswith('"') and text.endswith('"'):
                self.output.append(text[1:-1])
            elif text in self.variables:
                self.output.append(str(self.variables[text]))
            else:
                self.output.append(str(self.eval_expr(text)))

        # 2. Perintah TETAPKEUN (Deklarasi Variabel)
        elif line.startswith("TETAPKEUN "):
            parts = line[10:].split("=", 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                expr = parts[1].strip()
                self.variables[var_name] = self.eval_expr(expr)
            else:
                raise ValueError("Format TETAPKEUN salah. Anggo: TETAPKEUN variabel = nilai")

        # 3. Perintah HITUNG (Hasil Matematika / Variabel)
        elif line.startswith("HITUNG "):
            expr = line[7:].strip()
            result = self.eval_expr(expr)
            self.output.append(f">> {result}")

        # 4. Perintah BALIKAN (Looping / Pengulangan)
        elif line.startswith("BALIKAN "):
            match = re.match(r"BALIKAN\s+(\d+)\s+(.+)", line)
            if match:
                count = int(match.group(1))
                sub_cmd = match.group(2)
                for _ in range(count):
                    self.evaluate_line(sub_cmd)
            else:
                raise ValueError("Format BALIKAN salah. Anggo: BALIKAN <jumlah> <perintah>")
        else:
            raise ValueError(f"Perintah teu dipikawanoh: '{line}'")

    def eval_expr(self, expr):
        for var, val in self.variables.items():
            expr = re.sub(rf"\b{var}\b", str(val), expr)
        
        if not re.match(r"^[0-9\+\-\*\/\(\)\.\s]+$", expr):
            raise ValueError(f"Ekspresi matematika teu valid: {expr}")
        
        return eval(expr)

# ---------------------------------------------------------
# TAMPILAN & CSS ANIMATED CYBERPUNK UI (SUNDA VERSION)
# ---------------------------------------------------------
st.set_page_config(
    page_title="SUNDA SCRIPT IDE",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #080000;
        color: #ff3333;
        font-family: 'Courier New', Courier, monospace;
    }

    @keyframes redGlow {
        0% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000; }
        50% { text-shadow: 0 0 25px #ff0000, 0 0 35px #ff0000; }
        100% { text-shadow: 0 0 5px #ff0000, 0 0 10px #ff0000; }
    }

    .animated-title {
        color: #ff0000 !important;
        font-family: 'Courier New', Courier, monospace;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        letter-spacing: 3px;
        animation: redGlow 2.5s infinite ease-in-out;
        margin-bottom: 5px;
    }

    .status-bar {
        text-align: center;
        color: #880000;
        font-size: 0.85rem;
        border-bottom: 1px solid #440000;
        padding-bottom: 12px;
        margin-bottom: 25px;
    }

    .stTextArea textarea {
        background-color: #120000 !important;
        color: #00ff66 !important;
        border: 1px solid #550000 !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-size: 1rem !important;
    }

    .console-output {
        background-color: #050000;
        border: 1px solid #ff0000;
        border-radius: 5px;
        padding: 15px;
        color: #ffaa00;
        font-family: 'Courier New', Courier, monospace;
        min-height: 180px;
        white-space: pre-wrap;
        box-shadow: inset 0 0 10px rgba(255, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="animated-title">⚡ SUNDA SCRIPT IDE ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="status-bar">BASA PEMROGRAMAN SUNDA INTERPRETER v1.0</div>', unsafe_allow_html=True)

# Contoh Kode Bawaan Bahasa Sunda
default_code = """// Conto Kode Basa SundaScript
UCAP "--- SISTEM SUNDA SCRIPT DIPAANAKAN ---"

TETAPKEUN a = 20
TETAPKEUN b = 30
HITUNG a + b

BALIKAN 3 UCAP "NGAJALANKEUN PROTOKOL CYBER..."

UCAP "PROGRAM PARANTOS RENGSE"
"""

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📜 Editor Kode")
    user_code = st.text_area("Tulis Kode SundaScript di dieu:", value=default_code, height=300)
    run_btn = st.button("⚡ JALANKEUN KODE", use_container_width=True)

with col2:
    st.subheader("🖥️ Hasil Konsol")
    if run_btn:
        interpreter = SundaInterpreter()
        result = interpreter.run(user_code)
        st.markdown(f'<div class="console-output">{result}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="console-output">Pencet "JALANKEUN KODE" pikeun ngamimitian...</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
### 📘 Pituduh Sintaks SundaScript:
*   `UCAP "teks"` : Nampilkeun teks dina layar.
*   `TETAPKEUN variabel = angka/ekspresi` : Nyimpen nilai kana variabel.
*   `HITUNG ekspresi` : Ngitung sarta nampilkeun hasil matematika.
*   `BALIKAN <jumlah> <perintah>` : Ngabalikan perintah lobana $N$ kali.
*   `// catatan` : Komentar nu diabaikeun ku mesin.
""")
