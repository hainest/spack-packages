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

    with sp.when("%xl"):
        # IBM XL C
        sp.patch(
            "patches/xl_1_62_0_le.patch",
            when="@1.62.0",
            sha256="fd64b4f1e9c136549c7b704bd0014283e1515de8b68e54f0dd0cde758866eb69",
        )

    with sp.when("%xl_r"):
        # IBM XL C++
        sp.patch(
            "patches/xl_1_62_0_le.patch",
            when="@1.62.0",
            sha256="fd64b4f1e9c136549c7b704bd0014283e1515de8b68e54f0dd0cde758866eb69",
        )

    with sp.when("%nvhpc"):
        # Override the PGI toolset when using the NVIDIA compilers
        sp.patch(
            "patches/nvhpc-1.74.patch",
            when="@1.74.0:1.75",
            sha256="d56f31f2a3956630e5372b987d39cb79b5d2c71760fa150b8eb4a3f1a07e2658",
        )

        sp.patch(
            "patches/nvhpc-1.76.patch",
            when="@1.76.0:1.76",
            sha256="cba819a80b2e9449e11b43f4ab3c6d6097aa37d42925d4d64d0a9ba8e047d9e8",
        )

        # Workaround compiler bug
        sp.patch(
            "patches/nvhpc-find_address.patch",
            when="@1.75.0:1.76",
            sha256="938811004ff77783a82d59c8ebf2582a40db88de89fb0a078351e52e9e0aa704",
        )
