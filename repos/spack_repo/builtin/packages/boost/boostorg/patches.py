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

    with sp.when("%oneapi"):
        # https://www.intel.com/content/www/us/en/developer/articles/technical/building-boost-with-oneapi.html
        sp.patch(
            "patches/intel-oneapi-linux-jam.patch",
            when="@1.76:",
            sha256="8e3faa26450312e5ea8db8f32afda109b8559ba496e6a5799ddde271c9a6fc44",
        )

        # https://github.com/spack/spack/issues/44003
        sp.patch(
            "oneapi_pthread.patch",
            sha256="7845717c5d916fabc0e62eb6e1f5ad8f13baaf4a4b71b99b19847703386064c4",
            when="@1.76: %oneapi@2022:",
        )

    with sp.when("%cce"):
        # Fix float128 support when building with CUDA and Cray compiler
        sp.patch(
            "patches/config_PR378.patch",
            when="@:1.76",
            level=2,
            sha256="666eec8cfb0f71a87443ab27d179a9771bda32bcb8ff5e16afa3767f7b7f1e70",
        )

    #
    # ----- Platform-specific ---------
    #
    with sp.when("platform=darwin"):
        # Fix for version comparison on newer Clang on darwin
        # See: https://github.com/boostorg/build/issues/440
        # See: https://github.com/macports/macports-ports/pull/6726
        sp.patch(
            "patches/darwin_clang_version.patch",
            level=0,
            when="@1.56.0:1.72.0",
            sha256="95f5420d8ed34f60e3f88b38a4a5e8a032c94dc57b85cc2ab8243dd0d754a626",
        )

        # Allow building context asm sources with GCC on Darwin
        # See https://github.com/spack/spack/pull/24889
        # and https://github.com/boostorg/context/issues/177
        sp.patch(
            "patches/context-macho-gcc.patch",
            when="@1.65:1.76 +context %gcc",
            sha256="6edc1de3dcb931939a875796207057c00708525d86926b588ba55f65c18dc611",
        )

    with sp.when("platform=windows"):
        # https://github.com/boostorg/filesystem/issues/284
        sp.patch(
            "patches/filesystem_PR284.patch",
            when="@1.82.0",
            sha256="738ba8e0d7b5cdcf5fae4998f9450b51577bbde1bb0d220a0721551609714ca4",
        )

    #
    # ----- Python ---------
    #
    with sp.when("^python@3:"):
        # Backport Python3 import problem
        # See https://github.com/boostorg/python/pull/218
        sp.patch(
            "patches/python_PR218.patch",
            when="@1.63.0:1.67",
            sha256="7f95f95be9645eb7f10a7222173c8549501aebbe1db12b955442a7554dc59f3e",
        )
        sp.patch(
            "patches/python_jam-1_77.patch",
            when="@1.77:",
            sha256="b8569d7d4c3ef0501a39857126a2b0a88519bf256c29f3252a6958916ce82255",
        )
        sp.patch(
            "patches/python_jam.patch",
            when="@1.56:1.76",
            sha256="2ab6c72d03dec6a4ae20220a9dfd5c8c572c5294252155b85c6874d97c323199",
        )
        sp.patch(
            "patches/python_jam_pre156.patch",
            when="@:1.55.0",
            sha256="f994ac84634f2f833a7a4d3179c5bf9a06f14349ef67aacba39d08837ffab004",
        )

    #
    # --------------------------------------------------------------------------------------
    #

    # Fix missing declaration of uintptr_t with glibc>=2.17 - https://bugs.gentoo.org/482372
    sp.patch(
        "patches/glibc_gentoo_v1.53.0.patch",
        when="@1.53.0:1.54",
        sha256="b6f6ce68282159d46c716a1e6c819c815914bdb096cddc516fa48134209659f2",
    )

    sp.patch(
        "patches/call_once_variadic.patch",
        when="@1.54.0:1.55 %gcc@5.0:",
        sha256="4f2b06f77ad5e485e9debb769199414b2d6ebc0784aa1a8e28c1144fa971e155",
    )

    # Add option to C/C++ compile commands in clang-linux.jam
    sp.patch(
        "patches/clang-linux_add_option.patch",
        when="@1.56.0:1.63.0",
        sha256="d1cd178ea5348fafbba797113fc5a92cc822f3606dc2fe65c14cc2275334001b",
    )

    sp.patch(
        "patches/clang-linux_add_option2.patch",
        when="@1.47.0:1.55.0",
        sha256="4f0f7c0c0711e330aa077e2a1a989f68cbdcf7a3d20f85db872f3c34fce278e1",
    )

    # Support bzip2 and gzip in other directory
    # See https://github.com/boostorg/build/pull/154
    sp.patch(
        "patches/build_PR154.patch",
        when="@1.56.0:1.63",
        sha256="fb7d84358c36309062fa4aaaa187343eb16871bd95893f0270e0941955c488ab",
    )
