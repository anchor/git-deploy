#!/usr/bin/env python

#
# deployableversion.py
#
# Provides functions to manipulate version number strings to aid in
# convenient codebase deployments.
#
# Usage:
#   echo $yourVersionNumber | deploymentversionbumper.py bump_rc
#

"""This is a derivation of the Python distutils StrictVersion class. The parser
is mostly the same, and 'rc' replaces 'a' and 'b' as pre-release prefixes.
Methods are provided to generate new version numbers for testing and release,
'bump_for_testing' and 'bump_for_release' respectively.
"""

class DeployableVersion(object):
    """A version number consists of two or three dot-separated numeric
    components, with an optional "pre-release" tag on the end. The pre-release
    tag consists of 'rc' followed by a number. If the numeric components of two
    version numbers are equal, then one with a pre-release tag will always be
    deemed earlier (lesser) than one without.

    The following are valid version numbers (shown in the order that
    would be obtained by sorting according to the supplied cmp function):

        0.4       0.4.0  (these two are equivalent)
        0.4.1
        0.5rc1
        0.5rc3
        0.5
        0.9.6
        1.0
        1.0.4rc3
        1.0.4

    The following are examples of invalid version numbers:

        1
        2.7.2.2
        1.3.rc4
        1.3pl1
        1.3a4
    """

    import re
    version_re = re.compile(r'^(\d+) \. (\d+) (\. (\d+))? (rc(\d+))?$',
                            re.VERBOSE) # should include re.ASCII if available


    def __init__ (self, vstring=None):
        if vstring:
            self.parse(vstring)

    def __repr__ (self):
        return "%s ('%s')" % (self.__class__.__name__, str(self))

    def parse(self, vstring):
        match = self.version_re.match(vstring)
        if not match:
            raise ValueError("invalid version number '%s'" % vstring)

        (major, minor, patch, prerelease, prerelease_num) = \
            match.group(1, 2, 4, 5, 6)

        if patch:
            self.version = tuple(map(int, [major, minor, patch]))
        else:
            self.version = tuple(map(int, [major, minor])) + (0,)

        if prerelease:
            self.prerelease = ('rc', int(prerelease_num))
        else:
            self.prerelease = None


    def __str__ (self):

        if self.version[2] == 0:
            vstring = '.'.join(map(str, self.version[0:2]))
        else:
            vstring = '.'.join(map(str, self.version))

        if self.prerelease:
            vstring = vstring + self.prerelease[0] + str(self.prerelease[1])

        return vstring


    def __cmp__ (self, other):
        if isinstance(other, str):
            other = DeployableVersion(other)

        if self.version != other.version:
            # numeric versions don't match
            # prerelease stuff doesn't matter
            if self.version < other.version:
                return -1
            else:
                return 1

        # have to compare prerelease
        # case 1: neither has prerelease; they're equal
        # case 2: self has prerelease, other doesn't; other is greater
        # case 3: self doesn't have prerelease, other does: self is greater
        # case 4: both have prerelease: must compare them!

        if (not self.prerelease and not other.prerelease):
            return 0
        elif (self.prerelease and not other.prerelease):
            return -1
        elif (not self.prerelease and other.prerelease):
            return 1
        elif (self.prerelease and other.prerelease):
            if self.prerelease == other.prerelease:
                return 0
            elif self.prerelease < other.prerelease:
                return -1
            else:
                return 1
        else:
            assert False, "never get here"

# end class DeployableVersion


def bump_rc(version):
    # Possibilities:
    # case 1: newest tag is an rc, bump the prerelease number
    # case 2: newest tag is a release, no prerelease

    current = DeployableVersion(version)

    if current.prerelease:
        current.prerelease = current.prerelease[:1] + (current.prerelease[1]+1,)
    else:
        # 3-digit version number
        if current.version[2]:
            current.version = current.version[:2] + (current.version[2]+1,)
        # 2-digit version number
        else:
            current.version = current.version[:1] + (current.version[1]+1, 0)
        current.prerelease = ('rc',1)

    return str(current)


def bump_release(version):
    # Possibilities:
    # case 1: newest tag is an rc, leave the version and nuke the prerelease
    # case 2: newest tag is a release, bump the version

    current = DeployableVersion(version)

    if current.prerelease:
        current.prerelease = None
    else:
        # 3-digit version number
        if current.version[2]:
            current.version = current.version[:2] + (current.version[2]+1,)
        # 2-digit version number
        else:
            current.version = current.version[:1] + (current.version[1]+1, 0)

    return str(current)



def plist(LIST):
    for x in LIST:
        print x

def main(argv=None):
    import sys
    import fileinput

    if argv is None:
        argv = sys.argv[1:]

    try:
        VERSIONS = [ DeployableVersion(vstring) for vstring in fileinput.input('-') ]
    except ValueError as e:
        print "Version string '{0}' is not in the recognised format".format(e)
        return 2

    newest = str(max(VERSIONS))

    if 'bump_rc' in argv:
        print bump_rc(newest)

    elif 'bump_release' in argv:
        print bump_release(newest)

    else:
        print "The newest version tag is {0}".format(newest)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())



# vim: et ts=4