def remove_prefix(text, prefix):
    if text.index(prefix) > 0:
        return text[:text.index(prefix)]
    return text  # or whatever