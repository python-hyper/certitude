# -*- coding: utf-8 -*-
from cffi import FFI
ffi = FFI()

ffi.set_source(
    "certitude._certitude", None
)

ffi.cdef("""
    uint32_t validate_cert_chain(uint8_t **encoded_certs,
                                 size_t *cert_sizes,
                                 size_t cert_count,
                                 const char *hostname);
""")

if __name__ == '__main__':
    ffi.compile()
