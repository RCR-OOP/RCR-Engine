from rich.console import Console

console = Console()

def main():
    from .engine import Engine

    e = Engine()
    e.start()

    # * Code

    e.join()

if __name__ == "__main__":
    try:
        main()
    except:
        console.print_exception(word_wrap=True, show_locals=True)