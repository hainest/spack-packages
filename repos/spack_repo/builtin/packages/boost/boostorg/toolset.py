from spack.spec import Spec


def config(spec: Spec):
    toolsets = {
        "%gcc": "gcc",
        "%intel": "intel-linux",
        "%oneapi": "intel-linux",
        "%clang": "clang",
        "%arm": "clang",
        "%xl": "xlcpp",
        "%xl_r": "xlcpp",
        "%nvhpc": "pgi",
        "%fj": "clang",
    }

    for cc, toolset in toolsets.items():
        if spec.satisfies(cc):
            return toolset

    # fallback to gcc if no toolset found
    return "gcc"
