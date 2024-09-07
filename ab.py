import streamlit_authenticator as stauth
hashed_password = stauth.Hasher(['admin123']).generate()
print(hashed_password)
'''ADMIN:
      name: Akshay P
      password: $2b$12$Hx3vBbJ//AvPr2pC9p5iVuFA8j7sdY6dJ.G6BOwKn9KLjtuu1drYu'''