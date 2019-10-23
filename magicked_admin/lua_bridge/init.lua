function log(mesg)
    print(" [Lua] " .. mesg)
end

-- Called by python to add binds to namespaces
function bind_py_func(namespace, func_name, py_func)
    log(
        "Creating Python bind - "
            .. namespace .. "."
            .. func_name .. " -> "
            .. py_func.__name__
    )
    _G[namespace][func_name] = py_func
    return bind_py_func
end

-- Called by python to create Lua namespaces
function new_namespace(namespace)
    log("Creating namespace - " .. namespace)
    _G[namespace] = {}
end
