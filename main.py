import sys
import subprocess
from interfaces.cli_app import run_cli

def main():
    if len(sys.argv) < 2:
        print("Використання: python main.py [cli | web]")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "cli":
        run_cli()
    elif mode == "web":
        print("Запуск Streamlit сервера...")
        subprocess.run(["streamlit", "run", "interfaces/web_app.py"])
    else:
        print("Невідомий режим. Використовуйте 'cli' або 'web'.")

if __name__ == "__main__":
    main()