from cffi import FFI
ffi = FFI()

extra_compile_args = ["-g"]
ffi.set_source("_get_clashes_extra", open("get_clashes_extra.cpp").read(), source_extension='.cpp',
               #extra_compile_args=["-fopenmp"], extra_link_args=["-fopenmp"]
               )
ffi.cdef("""
typedef int Pair[2];
int get_clashes_extra(
  double *structures, Pair *pairs,
  int npairs, int *nat, int maxnat, float threshold,
  int *result
);
"""
)

if __name__ == "__main__":
    ffi.compile()
