from spack.spec import Spec


def options_windows(spec: Spec, toolset_version: str):
    """
    The only bootstrapping command line option that is accepted by
    'bootstrap.bat' is the compiler information: either the vc version
    (e.g. MSVC 14.3.x would be vc143) or gcc or clang.
    """
    opts = list()

    if spec.satisfies("%msvc"):
        opts.append(f"vc{toolset_version}")
    elif spec.satisfies("%gcc"):
        opts.append("gcc")
    elif spec.satisfies("%clang"):
        opts.append("clang")

    return opts


def options(spec: Spec, toolset: str, libs: list[str]):
    opts = list()

    # Arm compiler bootstraps with 'gcc' (but builds as 'clang')
    if spec.satisfies("%arm") or spec.satisfies("%fj"):
        opts.append("--with-toolset=gcc")
    else:
        opts.append(f"--with-toolset={toolset}")

    if libs:
        opts.append("--with-libraries=" + ",".join(sorted(libs)))
    else:
        opts.append("--with-libraries=headers")

    if spec.satisfies("+python"):
        opts.append("--with-python=" + spec["python"].command.path)

    if spec.satisfies("+icu"):
        opts.append("--with-icu")
    else:
        opts.append("--without-icu")

    return opts
