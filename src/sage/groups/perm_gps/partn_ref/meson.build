py.install_sources(
  '__init__.py',
  'all.py',
  'automorphism_group_canonical_label.pxd',
  'canonical_augmentation.pxd',
  'data_structures.pxd',
  'double_coset.pxd',
  'refinement_binary.pxd',
  'refinement_graphs.pxd',
  'refinement_lists.pxd',
  'refinement_matrices.pxd',
  'refinement_python.pxd',
  'refinement_sets.pxd',
  subdir: 'sage/groups/perm_gps/partn_ref',
)

extension_data = {
  'automorphism_group_canonical_label' : files(
    'automorphism_group_canonical_label.pyx',
  ),
  'canonical_augmentation' : files('canonical_augmentation.pyx'),
  'data_structures' : files('data_structures.pyx'),
  'double_coset' : files('double_coset.pyx'),
  'refinement_binary' : files('refinement_binary.pyx'),
  'refinement_graphs' : files('refinement_graphs.pyx'),
  'refinement_lists' : files('refinement_lists.pyx'),
  'refinement_matrices' : files('refinement_matrices.pyx'),
  'refinement_python' : files('refinement_python.pyx'),
  'refinement_sets' : files('refinement_sets.pyx'),
}

foreach name, pyx : extension_data
  py.extension_module(
    name,
    sources: pyx,
    subdir: 'sage/groups/perm_gps/partn_ref',
    install: true,
    include_directories: [inc_cpython, inc_data_structures, inc_rings],
    dependencies: [py_dep, cysignals, gmp],
  )
endforeach

