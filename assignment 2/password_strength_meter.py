import re
import streamlit as st
import random
import string

def check_password(password):
    score = 0

    if len(password) >= 8:
        score += 1
    else:
        print("❌ Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        print("❌ Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        print("❌ Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        print("❌ Include at least one special character (!@#$%^&*).")
    
    if score == 4:
        print("✅ Strong Password!")
    elif score == 3:
        print("⚠️ Moderate Password - Consider adding more security features.")
    else:
        print("❌ Weak Password - Improve it using the suggestions above.")

password = input("Enter your password: ")

check_password(password)

# Generate Password
def generate_pw(length, specials): 
    chars = string.ascii_letters + string.digits + (string.punctuation if specials else "")
    return ''.join(random.choice(chars) for _ in range(length))

def score_pw(pw, w):
    return (len(pw) * w['len'] +
            sum(c.isupper() for c in pw) * w['upper'] +
            sum(c.isdigit() for c in pw) * w['digit'] +
            sum(c in string.punctuation for c in pw) * w['spec'])

st.title("🔐 Password Generator")
length = st.sidebar.slider("Length", 8, 32, 12)
specials = st.sidebar.checkbox("Use Special Characters", True)
w = {
    'len': st.sidebar.slider("Length Weight", 0.1, 2.0, 1.0),
    'upper': st.sidebar.slider("Uppercase Weight", 0.1, 2.0, 1.0),
    'digit': st.sidebar.slider("Digits Weight", 0.1, 2.0, 1.0),
    'spec': st.sidebar.slider("Special Char Weight", 0.1, 2.0, 1.0),
}

if st.button("Generate Password"):
    pw = generate_pw(length, specials)
    if pw.lower():
        st.error("⚠️ Too common. Try again.")
    else:
        st.success(f"`{pw}`")
        st.info(f"Score: {score_pw(pw, w):.2f}")

user_pw = st.text_input("Check your own password:")
if user_pw:
    if user_pw.lower():
        st.error("❌ Weak! Too common.")
    else:
        score = score_pw(user_pw, w)
        st.success(f"Score: {score:.2f}")
        st.caption("Strong 💪" if score > 40 else "Okay 😐" if score > 20 else "Weak 🚫")