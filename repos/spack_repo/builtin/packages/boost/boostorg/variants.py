import spack.package as sp


class variant_set:
    def __init__(self):
        self.libraries = dict()

    def add(
        self,
        name,
        default=None,
        buildable=None,
        is_named=False,
        conflicts=[],
        requires=[],
        **kwargs,
    ):
        """
        Create a spack.Variant with extra logic to handle the cases a library
        should be compiled (i.e., passed to b2 via --with-libraries)

        Args:
         name (str): name of the variant

         default (str,bool,None):  The default value for the variant

                                    By default, each variant is enabled. A value of
                                    'None' is converted to 'True'. This is done so
                                    that each variants.add can omit a default
                                    value. The inversion is done because
                                    spack.Variant assumes a default value of
                                    'False'.

         buildable (str): The version string indicating which versions
                          for which the library should be compiled or `None`

         conflicts (list): The variant's conflicts

                           Each conflict is a dict with keys 'when' and 'msg'
                           that are identical to the values for the spack
                           'conflicts' directive.

                           NOTE: single- and multi-valued variants should use
                                 'requires' instead of 'conflicts'.

         requires (list): The variant's requires

                           Each requirement is a dict with keys 'spec', 'when', and
                           'msg' that are identical to the values for the spack
                           'requires' directive.

         kwargs (dict): The rest of the arguments forwarded on to the
                        spack.Variant constructor

                        This should include 'when' which indicates the version
                        range for which the variant is valid. This is distinct
                        from 'buildable' as the latter only indicates when the
                        library should be compiled.

                        For example, signal2 library was introduced in 1.39.0, but
                        wasn't buildable until 1.88.0. In this case, when="@1.39.0:" and
                        buildable="@1.88.0:".
        """

        if default is None:
            default = True

        if "sticky" not in kwargs:
            kwargs["sticky"] = True

        sp.variant(name, default=default, **kwargs)

        for c in conflicts:
            when = f"+{name}" if not is_named else ""
            if "when" in c:
                when = f"{c['when']} {when}"

            sp.conflicts(c["spec"], when=f"{when}", msg=c["msg"])

        for r in requires:
            when = f"+{name}" if not is_named else ""
            if "when" in r:
                when = f"{r['when']} {when}"

            sp.requires(r["spec"], when=f"{when}", msg=r["msg"])

        if buildable is not None:
            self.libraries[name] = buildable

    def libraries_to_build(self, spec):
        """
        The set of libraries that need to be passed to b2 via --with-libraries to be compiled
        """
        libs = list()

        for name, version in self.libraries.items():
            if spec.satisfies("+{0:s} {1:s}".format(name, version)):
                libs.append(name)

        return sorted(libs)


# fmt: off

def load():

    variants = variant_set()

    # ----------------------------------------------------------------------
    #  Boost-level configurations
    #
    #    These variants affect every library.
    # ----------------------------------------------------------------------
    variants.add(
        "clanglibcpp",
        default=False,
        when="@1.73.0:",
        conflicts=[
            # Boost 1.85.0 stacktrace added a hard compilation error that has to
            # explicitly be suppressed on some platforms:
            # https://github.com/boostorg/stacktrace/issues/163
            {"spec": "@1.85: +stacktrace", "msg": "Stacktrace cannot be used with libc++"},
            # gcc doesn't support libc++
            {"spec": "%gcc", "msg": "gcc doesn't support libc++"},
        ],
        description="Compile with clang's libc++ instead of libstdc++",
    )
    variants.add(
        "cxxstd",
        default="14",
        values=(
            # Boost supports pre-releases like 2a, but spack.CompilerAdaptor doesn't
            "98",
            "03",
            "11",
            "14",
            sp.conditional("17", when="@1.63.0:"),
            sp.conditional("20", when="@1.77.0:"),
            sp.conditional("23", when="@1.79.0:"),
            sp.conditional("26", when="@1.79.0:"),
        ),
        multi=False,
        is_named=True,
        conflicts=[
            # Boost.core requires cxxstd >= 03 since 1.76.0
            {"spec": "cxxstd=98", "when":"@1.76.0:1.83.0", "msg": "This version of Boost requires cxxstd >= 03"},
            # C++98/03 support was removed in 1.84.0
            {"spec": "cxxstd=98", "when":"@1.84.0:", "msg": "This version of Boost requires cxxstd >= 11"},
            {"spec": "cxxstd=03", "when":"@1.84.0:", "msg": "This version of Boost requires cxxstd >= 11"},
        ],
        description="C++ standard",
    )
    variants.add(
        "taggedlayout",
        default=False,
        when="@1.40.0:",
        conflicts=[
            {"spec": "+versionedlayout", "msg": "Layouts cannot be both tagged and versioned"}
        ],
        description="Augment library names with build options",
    )
    variants.add(
        "versionedlayout",
        default=False,
        conflicts=[
            {"spec": "+taggedlayout", "msg": "Layouts cannot be both tagged and versioned"}
        ],
        description="Augment library layout with versioned subdirs",
    )
    # https://boostorg.github.io/build/manual/develop/index.html#bbv2.builtin.features.visibility
    variants.add(
        "visibility",
        values=("global", "protected", "hidden"),
        default="hidden",
        multi=False,
        when="@1.69.0:",
        description="Default symbol visibility in compiled libraries",
    )

    # ----------------------------------------------------------------------
    #  Library-level configurations
    #
    #  These variants are specific to a particular library.
    #
    #  mpi and python are not enabled by default because they pull in many
    #  dependencies and/or because there is a great deal of customization
    #  possible (and it would be difficult to choose sensible defaults).
    # ----------------------------------------------------------------------

    return variants
