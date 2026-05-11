def run(editor_code, plugin_code):
    namespace = {"editor_code": editor_code}
    exec(plugin_code, namespace, namespace)
    if "result" not in namespace:
        raise ValueError("Plugin code must assign to `result`.")
    return namespace["result"]
