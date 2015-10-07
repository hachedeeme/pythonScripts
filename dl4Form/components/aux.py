
first_to_lowercase = lambda text: text[:1].lower() + text[1:] if text else ''

jump_separator     = lambda text: text + ': !' + ('=' * (77 - len(text)))