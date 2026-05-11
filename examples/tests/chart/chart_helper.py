def run(chart_type, data, options, plugin_code):
    namespace = {
        "chart_type": chart_type,
        "data": data,
        "options": options,
    }
    exec(plugin_code, namespace, namespace)
    if "result" not in namespace:
        raise ValueError("Plugin code must assign to `result`.")
    return namespace["result"]
