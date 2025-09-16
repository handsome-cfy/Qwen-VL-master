# 8890 HTTP
export http_proxy=http://127.0.0.1:8890
export https_proxy=$http_proxy

# 8891 SOCKS5（如果只想全局走 SOCKS，可把上面两句换成下面）
export ALL_PROXY=socks5h://127.0.0.1:8891