from zxcvbn import zxcvbn
import math
import string


def calculate_entropy(password):
    charset = 0

    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)


def evaluate_password(password):
    result = zxcvbn(password)
    return {
        "password": password,
        "score": result["score"],
        "crack_time": result["crack_times_display"]["offline_fast_hashing_1e10_per_second"],
        "entropy": calculate_entropy(password),
        "warning": result["feedback"].get("warning") or "",
        "suggestions": result["feedback"].get("suggestions") or [],
    }


def analyze_password(password):
    details = evaluate_password(password)

    print("\n====== PASSWORD ANALYSIS ======")
    print(f"Password: {details['password']}")
    print(f"Score (0-4): {details['score']}")
    print(f"Crack Time: {details['crack_time']}")
    print(f"Entropy: {details['entropy']} bits")

    if details["warning"]:
        print(f"Warning: {details['warning']}")

    if details["suggestions"]:
        print("Suggestions:")
        for suggestion in details["suggestions"]:
            print(f"- {suggestion}")

    return details
