from cffi import FFI
ffi = FFI()


ffi.set_source("_get_clashes", open("get_clashes.cpp").read(), source_extension='.cpp',
               #extra_compile_args=["-fopenmp"], extra_link_args=["-fopenmp"]
               )
ffi.cdef("""
void get_clashes(
  int n, int nat, float threshold,
  double *structures, bool *matrix
);
"""
)

if __name__ == "__main__":
    ffi.compile()
