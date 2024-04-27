# distutils: libraries = flint
# distutils: depends = flint/thread_pool.h

################################################################################
# This file is auto-generated by the script
#   SAGE_ROOT/src/sage_setup/autogen/flint_autogen.py.
# Do not modify by hand! Fix and rerun the script instead.
################################################################################

from libc.stdio cimport FILE
from sage.libs.gmp.types cimport *
from sage.libs.mpfr.types cimport *
from sage.libs.flint.types cimport *

cdef extern from "flint_wrap.h":
    void thread_pool_init(thread_pool_t T, slong size) noexcept
    slong thread_pool_get_size(thread_pool_t T) noexcept
    int thread_pool_set_size(thread_pool_t T, slong new_size) noexcept
    slong thread_pool_request(thread_pool_t T, thread_pool_handle * out, slong requested) noexcept
    void thread_pool_wake(thread_pool_t T, thread_pool_handle i, int max_workers, void (*f)(void*), void * a) noexcept
    void thread_pool_wait(thread_pool_t T, thread_pool_handle i) noexcept
    void thread_pool_give_back(thread_pool_t T, thread_pool_handle i) noexcept
    void thread_pool_clear(thread_pool_t T) noexcept
