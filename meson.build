project(
    'msgspec',
    'c',
    default_options: [
        'warning_level=3',
    ],
    license: 'BSD-3-Clause',
    license_files: ['LICENSE.txt'],
    meson_version: '>=1.1.0',
    version: run_command(
        'python3',
        [
            '-c',
            'from setuptools_scm import get_version;print(get_version(normalize=False, fallback_version="%OZIBUILDVERSION%"))',
        ],
        check: true,
    ).stdout().strip(),
)
fs = import('fs')
pymod = import('python')
python_dependencies = get_option('python-dependencies')
python = pymod.find_installation()
project_name = meson.project_name()
root_files = [
    'README',
    'CHANGELOG.md',
    'LICENSE.txt',
    'requirements.in',
    'pyproject.toml',
    '.gitignore',
]
pyproject_config = configuration_data()
pyproject_config.set(
    'PYTHON_VERSION_DIST',
    'py'+''.join(python.language_version().split('.'))
)
pyproject_config.set('SCM_VERSION', meson.project_version())
pyproject_config.set('VCS_TAG', '@VCS_TAG@')
pyproject_config.set('PROJECT_NAME', project_name)
pyproject_config.set('README_TEXT', fs.read('README'))
pyproject_config.set('REQUIREMENTS_IN', 
    run_command(
        python, ['-c', '''import os;import pathlib
requirements = (
    r.partition('\u0023')[0]
    for r in filter(
        lambda r: not (r.startswith('\u0023') or r == '\n'),
        pathlib.Path('./requirements.in').read_text('utf-8').splitlines(),
    )
)
for req in requirements:
    if len(req) > 0:
        print(f'Requires-Dist: {req}')
'''], check: true
    ).stdout().strip()
)
pyproject_config.set('LICENSE', meson.project_license()[0])
configure_file(
    input: 'pyproject.toml',
    output: 'pyproject.toml',
    configuration: pyproject_config
)
vcs_tag(input: 'pyproject.toml', output: 'pyproject.orig.toml')
if get_option('use-mimalloc') not in ''
    cmake = import('cmake')
    opt_var = cmake.subproject_options()
    opt_var.set_install(false)
    mimalloc = cmake.subproject('mimalloc', options: opt_var)
endif
foreach source : root_files
    if source not in ['pyproject.toml', 'requirements.in', '.gitignore', 'README', 'CHANGELOG.md']
        fs.copyfile(source)
    elif source == 'README'
        fs.copyfile(source, 'README.md')
    endif
endforeach
root_children = ['msgspec', 'tests']
foreach child: root_children
    subdir(child)
endforeach
if false
    executable('root_files', root_files)
    executable('source_files', source_files)
    executable('ext_files', ext_files)
    executable('test_files', test_files)
    executable('root_children', root_children)
    executable('source_children', source_children)
    executable('test_children', test_children)
endif
if not meson.is_subproject()
    dev = subproject('ozi')
    foreach var : get_option('variables')
        name = var.replace('-', '_')
        set_variable(name, dev.get_variable(name))
    endforeach
    deps = run_command(python, '-c', dev.get_variable('install_dependencies'), check: true).stdout().strip().split('$$')
    if deps[0] != ''
        if find_program('uv', disabler: true).found()
            meson.add_postconf_script('uv', 'venv', 'venv')
        else
            meson.add_postconf_script(dev.get_variable('pip'), 'install', 'virtualenv')
            meson.add_postconf_script('virtualenv', 'venv')
        endif
        meson.add_postconf_script(dev.get_variable('pip'), 'install', deps)
    endif
endif
