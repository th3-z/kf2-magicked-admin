log = {}
bridge = {}

iter = python.iter
enumerate = python.enumerate

log.info = function (mesg)
    print(" [*] [Lua] " .. mesg)
end

log.warning = function (mesg)
    print(" [!] [Lua] " .. mesg)
end

-- Called by python to add binds to namespaces
bridge.new_bind = function (namespace, func_name, py_func)
    log.info(
        "Creating Python bind - "
            .. namespace .. "."
            .. func_name .. " -> "
            .. py_func.__name__
    )
    _G[namespace][func_name] = py_func
    return bind_py_func
end

-- Called by python to create Lua namespaces
bridge.new_namespace = function (namespace)
    log.info("Creating namespace - " .. namespace)
    _G[namespace] = {}
end


