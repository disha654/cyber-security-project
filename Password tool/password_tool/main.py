import argparse
import tkinter as tk
from tkinter import messagebox, scrolledtext

from strength_checker import analyze_password, evaluate_password
from wordlist_generator import generate_wordlist, export_wordlist


def launch_gui():
    root = tk.Tk()
    root.title("Password Tool")
    root.geometry("700x650")

    frame = tk.Frame(root, padx=14, pady=14)
    frame.pack(fill="both", expand=True)

    title = tk.Label(frame, text="Password Strength Analyzer & Wordlist Generator", font=("Segoe UI", 12, "bold"))
    title.pack(anchor="w", pady=(0, 10))

    analyze_label = tk.Label(frame, text="Password to analyze")
    analyze_label.pack(anchor="w")
    analyze_entry = tk.Entry(frame, width=50)
    analyze_entry.pack(anchor="w", pady=(0, 8))

    fields_frame = tk.Frame(frame)
    fields_frame.pack(fill="x", pady=(6, 4))

    tk.Label(fields_frame, text="Name").grid(row=0, column=0, sticky="w", padx=(0, 8))
    name_entry = tk.Entry(fields_frame, width=20)
    name_entry.grid(row=0, column=1, sticky="w", padx=(0, 14))

    tk.Label(fields_frame, text="Pet").grid(row=0, column=2, sticky="w", padx=(0, 8))
    pet_entry = tk.Entry(fields_frame, width=20)
    pet_entry.grid(row=0, column=3, sticky="w")

    tk.Label(fields_frame, text="DOB").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(8, 0))
    dob_entry = tk.Entry(fields_frame, width=20)
    dob_entry.grid(row=1, column=1, sticky="w", padx=(0, 14), pady=(8, 0))

    tk.Label(fields_frame, text="Keyword").grid(row=1, column=2, sticky="w", padx=(0, 8), pady=(8, 0))
    keyword_entry = tk.Entry(fields_frame, width=20)
    keyword_entry.grid(row=1, column=3, sticky="w", pady=(8, 0))

    output_label = tk.Label(frame, text="Output")
    output_label.pack(anchor="w", pady=(12, 4))

    output_box = scrolledtext.ScrolledText(frame, width=80, height=18)
    output_box.pack(fill="both", expand=True)

    def write_output(text):
        output_box.insert(tk.END, text + "\n")
        output_box.see(tk.END)

    def on_analyze():
        password = analyze_entry.get().strip()
        if not password:
            messagebox.showwarning("Missing input", "Enter a password to analyze.")
            return

        details = evaluate_password(password)
        write_output("\n====== PASSWORD ANALYSIS ======")
        write_output(f"Password: {details['password']}")
        write_output(f"Score (0-4): {details['score']}")
        write_output(f"Crack Time: {details['crack_time']}")
        write_output(f"Entropy: {details['entropy']} bits")

        if details["warning"]:
            write_output(f"Warning: {details['warning']}")

        if details["suggestions"]:
            write_output("Suggestions:")
            for suggestion in details["suggestions"]:
                write_output(f"- {suggestion}")

    def on_generate():
        wordlist = generate_wordlist(
            name=name_entry.get().strip() or None,
            pet=pet_entry.get().strip() or None,
            dob=dob_entry.get().strip() or None,
            keyword=keyword_entry.get().strip() or None,
        )

        if not wordlist:
            messagebox.showwarning("Missing input", "Enter at least one field to generate a wordlist.")
            return

        export_wordlist(wordlist)
        write_output(f"\n[OK] Wordlist saved to output/wordlist.txt")
        write_output(f"Total words generated: {len(wordlist)}")

    buttons = tk.Frame(frame)
    buttons.pack(anchor="w", pady=(10, 0))

    tk.Button(buttons, text="Analyze Password", command=on_analyze, width=18).pack(side="left", padx=(0, 8))
    tk.Button(buttons, text="Generate Wordlist", command=on_generate, width=18).pack(side="left", padx=(0, 8))
    tk.Button(buttons, text="Clear Output", command=lambda: output_box.delete("1.0", tk.END), width=14).pack(side="left")

    root.mainloop()


def main():
    parser = argparse.ArgumentParser(
        description="Password Strength Analyzer & Custom Wordlist Generator"
    )

    parser.add_argument("--analyze", help="Analyze a password")
    parser.add_argument("--generate", action="store_true", help="Generate wordlist")
    parser.add_argument("--gui", action="store_true", help="Launch Tkinter GUI")

    parser.add_argument("--name", help="First name")
    parser.add_argument("--pet", help="Pet name")
    parser.add_argument("--dob", help="Date of birth")
    parser.add_argument("--keyword", help="Custom keyword")

    args = parser.parse_args()

    if args.gui:
        launch_gui()
        return

    if args.analyze:
        analyze_password(args.analyze)

    if args.generate:
        wordlist = generate_wordlist(
            name=args.name,
            pet=args.pet,
            dob=args.dob,
            keyword=args.keyword
        )
        export_wordlist(wordlist)

    if not args.analyze and not args.generate:
        parser.print_help()


if __name__ == "__main__":
    print("\n[LOCK] Cyber Security Project Tool")
    print("For Educational & Authorized Testing Only\n")
    main()
