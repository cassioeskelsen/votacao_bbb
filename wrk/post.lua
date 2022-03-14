wrk.method = "POST"
wrk.body   = "voto=x"
wrk.headers["user-agent"] = "wrk"
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"