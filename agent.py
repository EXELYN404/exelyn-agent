import sys
from openai import OpenAI

# ---------------------------------------------------------
# 1. ISI KONFIGURASI KAMU DI SINI (AGAR TIDAK PERLU PASTE)
# ---------------------------------------------------------
API_KEY = "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"  # Ganti dengan API Key kamu
BASE_URL = "https://router.requesty.ai/v1"  # Sesuaikan URL provider kamu
MODEL_NAME = "deepseek/deepseek-coder"      # Sesuaikan nama model

# ---------------------------------------------------------
# WARNA TERMINAL (ANSI ESCAPE CODES) - RED & BLACK HACKER
# ---------------------------------------------------------
RED = "\033[38;2;255;0;0m"
DARK_RED = "\033[38;2;139;0;0m"
GREEN_CODE = "\033[38;2;0;255;102m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_banner():
    print(f"{RED}{BOLD}")
    print("=" * 50)
    print("      ⚡ EXELYN AGENT - CODING ASSISTANT ⚡      ")
    print("       SYSTEM STATUS: ONLINE | PROTOCOL: CLI     ")
    print("=" * 50)
    print(f"{RESET}")

def main():
    print_banner()

    if API_KEY == "PASTE_API_KEY_KAMU_DI_SINI" or not API_KEY:
        print(f"{DARK_RED}[!] ERROR: Masukkan API Key kamu di dalam file app.py terlebih dahulu!{RESET}")
        sys.exit()

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    system_prompt = """
    You are EXELYN AGENT, an elite hacker-style AI coding assistant.
    Your responses must be precise, highly technical, clean, and optimized.
    Always write clean, secure code and explain complex logic efficiently.
    """

    messages = [{"role": "system", "content": system_prompt}]

    print(f"{RED}[SYSTEM INITIALIZED] Type 'exit' or 'quit' to close.{RESET}\n")

    while True:
        try:
            user_input = input(f"{DARK_RED}EXELYN-USER>{RESET} ")
            if user_input.lower() in ["exit", "quit"]:
                print(f"{RED}[+] Terminating session...{RESET}")
                break
            if not user_input.strip():
                continue

            messages.append({"role": "user", "content": user_input})

            print(f"\n{RED}EXELYN-AGENT>{RESET} ", end="")
            
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                stream=True
            )

            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    full_response += text
                    sys.stdout.write(f"{GREEN_CODE}{text}{RESET}")
                    sys.stdout.flush()

            print("\n")
            messages.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            print(f"\n{RED}[!] Interrupted by user. Exiting...{RESET}")
            break
        except Exception as e:
            print(f"\n{DARK_RED}[ERROR] {str(e)}{RESET}\n")

if __name__ == "__main__":
    main()
