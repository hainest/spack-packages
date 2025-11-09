import spack.package as sp


def load():

    #
    # ----- Compilers ---------
    #
    with sp.when("%fj"):
        # Change the method for version analysis when using Fujitsu compiler.
        sp.patch(
            "patches/fujitsu_version_analysis.patch",
            when="@1.67.0:1.76.0",
            sha256="34233f0a408ce9b1bb49b548086ef7f2caffc1eece52976d47ffb7cab4fee802",
        )

        sp.patch(
            "patches/fujitsu_version_analysis-1.77.patch",
            when="@1.77.0:",
            sha256="f627cd4a5e33680ff1d08f427a526d43b80a35a2204852d82e769ffa916b4e77",
        )
