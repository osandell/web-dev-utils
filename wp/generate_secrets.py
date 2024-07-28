import random
import string
import subprocess
import sys

# Password is generated according to the WordPress requirements:
# https://wordpress.org/documentation/article/password-best-practices/
def generate_password(length=24):
    characters = string.ascii_letters + string.digits + "!\"#$%&'()*+,-./:;<=>?@[]^_{}|~"
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice("!\"#$%&'()*+,-./:;<=>?@[]^_{}|~")
    ]
    password += random.choices(characters, k=length - 4)
    random.shuffle(password)
    return ''.join(password)

def fetch_wp_auth_keys(prefix):
    result = subprocess.run(["curl", "-s", "https://api.wordpress.org/secret-key/1.1/salt/"], capture_output=True, text=True)
    salts = result.stdout.split("\n")
    formatted_salts = []
    for salt in salts:
        if salt.strip():
            try:
                parts = salt.replace("define('", "").split("',")
                key = parts[0].strip()
                value = parts[1].split("');")[0].strip().strip('\'')
                formatted_salts.append(f"{prefix}_{key.lower()}: {value}")
            except Exception as e:
                print(f"Error processing line: {salt}. Error: {str(e)}")
    return formatted_salts

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <stack name>")
        print("Example: python script.py mysite_com")
        sys.exit(1)

    prefix = sys.argv[1]
    # Generate the password
    password = generate_password()
    outputs = [f"{prefix}_db_password: {password}"]
    # Fetch and add WordPress auth keys and salts to the outputs list
    outputs.extend(fetch_wp_auth_keys(prefix))
    # Sort and print outputs
    for line in sorted(outputs):
        print(line)
