def remove_prefix(text, prefix):
    if text.find(prefix) > 0:
        return text[:text.index(prefix)]
    return text  # or whatever