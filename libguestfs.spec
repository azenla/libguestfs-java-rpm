# Enable to build w/o network.
%global buildnonet 1

Summary:     Access and modify virtual machine disk images
Name:        libguestfs
Version:     1.0.48
Release:     2%{?dist}
License:     LGPLv2+
Group:       Development/Libraries
URL:         http://libguestfs.org/
Source0:     http://libguestfs.org/download/%{name}-%{version}.tar.gz
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root

# Basic build requirements:
BuildRequires: /usr/bin/pod2man
BuildRequires: /usr/bin/pod2text
BuildRequires: febootstrap >= 2.3
BuildRequires: augeas-devel >= 0.5.0
BuildRequires: readline-devel
BuildRequires: squashfs-tools
BuildRequires: qemu-kvm >= 0.10-7
BuildRequires: createrepo
BuildRequires: glibc-static

# This is only needed for RHEL 5 because readline-devel doesn't
# properly depend on it, but doesn't do any harm on other platforms:
BuildRequires: ncurses-devel

# Build requirements for the appliance (see 'make.sh.in' in the source):
BuildRequires: kernel, bash, coreutils, lvm2, ntfs-3g, util-linux-ng
BuildRequires: MAKEDEV, net-tools, augeas-libs, file
BuildRequires: module-init-tools, procps, strace, iputils
BuildRequires: dosfstools, zerofree
%ifarch %{ix86} x86_64
BuildRequires: grub, ntfsprogs
%endif

# Must match the above set of BuildRequires exactly!
Requires:      kernel, bash, coreutils, lvm2, ntfs-3g, util-linux-ng
Requires:      MAKEDEV, net-tools, augeas-libs, file
Requires:      module-init-tools, procps, strace, iputils
Requires:      dosfstools, zerofree
%ifarch %{ix86} x86_64
Requires:      grub, ntfsprogs
%endif

# These are only required if you want to build the bindings for
# different languages:
BuildRequires: ocaml
BuildRequires: ocaml-findlib-devel
BuildRequires: perl-devel
BuildRequires: perl-Test-Simple
BuildRequires: perl-Test-Pod
BuildRequires: perl-Test-Pod-Coverage
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: python-devel
BuildRequires: ruby-devel
BuildRequires: rubygem-rake
BuildRequires: java >= 1.5.0
BuildRequires: jpackage-utils
BuildRequires: java-devel

# For virt-inspector:
BuildRequires: perl-Sys-Virt

# Runtime requires:
Requires:      qemu-kvm >= 0.10-7

# For virt-inspector --windows-registry option.
Requires:      chntpw >= 0.99.6-8


%description
Libguestfs is a library for accessing and modifying guest disk images.
Amongst the things this is good for: making batch configuration
changes to guests, getting disk used/free statistics (see also:
virt-df), migrating between virtualization systems (see also:
virt-p2v), performing partial backups, performing partial guest
clones, cloning guests and changing registry/UUID/hostname info, and
much else besides.

Libguestfs uses Linux kernel and qemu code, and can access any type of
guest filesystem that Linux and qemu can, including but not limited
to: ext2/3/4, btrfs, FAT and NTFS, LVM, many different disk partition
schemes, qcow, qcow2, vmdk.

Libguestfs provides ways to enumerate guest storage (eg. partitions,
LVs, what filesystem is in each LV, etc.).  It can also run commands
in the context of the guest.  Also you can access filesystems over FTP.

Libguestfs is a library that can be linked with C and C++ management
programs.

See also the 'guestfish' package for shell scripting and command line
access.

For Perl bindings, see 'perl-libguestfs'.

For OCaml bindings, see 'ocaml-libguestfs-devel'.

For Python bindings, see 'python-libguestfs'.

For Ruby bindings, see 'ruby-libguestfs'.

For Java bindings, see 'libguestfs-java-devel'.


%package devel
Summary:     Development tools and libraries for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}
Requires:    pkgconfig


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


%package -n guestfish
Summary:     Shell for accessing and modifying virtual machine disk images
Group:       Development/Tools
License:     GPLv2+
Requires:    %{name} = %{version}-%{release}
Requires:    /usr/bin/pod2text


%description -n guestfish
Guestfish is the Filesystem Interactive SHell, for accessing and
modifying virtual machine disk images from the command line and shell
scripts.


%package -n virt-inspector
Summary:     Display OS version, kernel, drivers, etc in a virtual machine
Group:       Development/Tools
License:     GPLv2+
Requires:    %{name} = %{version}-%{release}
Requires:    guestfish
Requires:    perl-Sys-Virt


%description -n virt-inspector
Virt-inspector examines a virtual machine and tries to determine the
version of the OS, the kernel version, what drivers are installed,
whether the virtual machine is fully virtualized (FV) or
para-virtualized (PV), what applications are installed and more.


%package -n ocaml-%{name}
Summary:     OCaml bindings for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}


%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.


%package -n ocaml-%{name}-devel
Summary:     OCaml bindings for %{name}
Group:       Development/Libraries
Requires:    ocaml-%{name} = %{version}-%{release}


%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.


%package -n perl-%{name}
Summary:     Perl bindings for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}
Requires:    perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description -n perl-%{name}
perl-%{name} contains Perl bindings for %{name}.


%package -n python-%{name}
Summary:     Python bindings for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description -n python-%{name}
python-%{name} contains Python bindings for %{name}.


%package -n ruby-%{name}
Summary:     Ruby bindings for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}
Requires:    ruby(abi) = 1.8
Provides:    ruby(guestfs) = %{version}

%{!?ruby_sitelib: %define ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%{!?ruby_sitearch: %define ruby_sitearch %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}

%description -n ruby-%{name}
ruby-%{name} contains Ruby bindings for %{name}.


%package java
Summary:     Java bindings for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}
Requires:    java >= 1.5.0
Requires:    jpackage-utils

%description java
%{name}-java contains Java bindings for %{name}.

If you want to develop software in Java which uses %{name}, then
you will also need %{name}-java-devel.


%package java-devel
Summary:     Java development package for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}
Requires:    %{name}-java = %{version}-%{release}

%description java-devel
%{name}-java-devel contains the tools for developing Java software
using %{name}.

See also %{name}-javadoc.


%package javadoc
Summary:     Java documentation for %{name}
Group:       Development/Libraries
Requires:    %{name} = %{version}-%{release}
Requires:    %{name}-java = %{version}-%{release}
Requires:    jpackage-utils

%description javadoc
%{name}-javadoc contains the Java documentation for %{name}.


%prep
%setup -q

mkdir -p daemon/m4

# Rerun the generator to make sure all files are up to date.
src/generator.ml


%build
%if %{buildnonet}
mkdir repo
find /var/cache/yum -type f -name '*.rpm' -print0 | xargs -0 cp -t repo
createrepo repo
%define extra --with-mirror=file://$(pwd)/repo --with-repo=fedora-12 --with-updates=none
%else
%define extra %nil
%endif

./configure \
  --prefix=%{_prefix} --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --with-qemu="qemu-kvm qemu-system-%{_build_arch} qemu" \
  --enable-debug-command \
  --enable-supermin \
  %{extra}

# This ensures that /usr/sbin/chroot is on the path.  Not needed
# except for RHEL 5, it shouldn't do any harm on other platforms.
export PATH=/usr/sbin:$PATH

# 'INSTALLDIRS' ensures that perl libs are installed in the vendor dir
# not the site dir.
make INSTALLDIRS=vendor %{?_smp_mflags}


%check
# Enable debugging - very useful if a test does fail, although
# it produces masses of output in the build.log.
export LIBGUESTFS_DEBUG=1

# Uncomment one of these, depending on whether you want to
# do a very long and thorough test ('make check') or just
# a quick test to see if things generally work.

# Currently tests are disabled on all architectures because of:
#   BZ 494075/504273 (ppc, ppc64) - possibly now fixed
#   BZ 505109 (ppc, ppc64) - openbios boot failure
#   BZ 502058 (i386, x86-64) - only on F-11 we think, seems to work on F-12
#   BZ 502074 (i386) - sha1sum segfault on F-11 only
#   BZ 503236 (i386) - cryptomgr_test at doublefault_fn (F-12 only)

# Workaround for BZ 502058.  This is only needed for F-11, but
# won't harm other builds.
export LIBGUESTFS_APPEND=noapic

%ifarch x86_64
make check
%endif

# Quick test:
#./fish/guestfish -v <<EOT
#alloc test.img 100M
#run
#sfdisk /dev/sda 0 0 0 ,
#pvcreate /dev/sda1
#vgcreate VG /dev/sda1
#lvcreate LV1 VG 10M
#lvcreate LV2 VG 10M
#mkfs ext2 /dev/VG/LV1
#mount /dev/VG/LV1 /
#ll /
#lvs
#sync
#EOT


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Delete the ordinary appliance, leaving just the supermin appliance.
rm $RPM_BUILD_ROOT%{_libdir}/guestfs/vmlinuz.*
mkdir keep
mv $RPM_BUILD_ROOT%{_libdir}/guestfs/initramfs.*.supermin.img keep
rm $RPM_BUILD_ROOT%{_libdir}/guestfs/initramfs.*.img
mv keep/* $RPM_BUILD_ROOT%{_libdir}/guestfs/
rmdir keep

# Delete static libraries, libtool files.
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs.a
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs.la

# Clean up the examples/ directory which will get installed in %doc.
# Note we can't delete the original examples/Makefile because that
# will be needed by the check section later in the RPM build.
cp -a examples ex
pushd ex
make clean
rm Makefile*
rm -rf .deps .libs
popd

# Same for ocaml/examples.
cp -a ocaml/examples ocaml/ex
pushd ocaml/ex
make clean
rm Makefile*
popd

find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete

rm $RPM_BUILD_ROOT%{python_sitearch}/libguestfsmod.a
rm $RPM_BUILD_ROOT%{python_sitearch}/libguestfsmod.la

if [ "$RPM_BUILD_ROOT%{python_sitearch}" != "$RPM_BUILD_ROOT%{python_sitelib}" ]; then
   mkdir -p $RPM_BUILD_ROOT%{python_sitelib}
   mv $RPM_BUILD_ROOT%{python_sitearch}/guestfs.py* \
     $RPM_BUILD_ROOT%{python_sitelib}/
fi

# Install ruby bindings by hand.
mkdir -p $RPM_BUILD_ROOT%{ruby_sitelib}
mkdir -p $RPM_BUILD_ROOT%{ruby_sitearch}
install -p -m0644 ruby/lib/guestfs.rb $RPM_BUILD_ROOT%{ruby_sitelib}
install -p -m0755 ruby/ext/guestfs/_guestfs.so $RPM_BUILD_ROOT%{ruby_sitearch}

# Remove static-linked Java bindings.
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs_jni.a
rm $RPM_BUILD_ROOT%{_libdir}/libguestfs_jni.la

# Generator shouldn't be executable when we distribute it.
chmod -x src/generator.ml

# Find locale files.
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/guestfs-supermin-helper
%{_libdir}/guestfs/
%{_libdir}/libguestfs.so.*


%files devel
%defattr(-,root,root,-)
%doc ChangeLog HACKING TODO README ex html/guestfs.3.html html/pod.css
%doc src/generator.ml
%{_libdir}/libguestfs.so
%{_mandir}/man3/guestfs.3*
%{_includedir}/guestfs.h
%{_includedir}/guestfs-actions.h
%{_includedir}/guestfs-structs.h
%{_libdir}/pkgconfig/libguestfs.pc


%files -n guestfish
%defattr(-,root,root,-)
%doc html/guestfish.1.html html/pod.css recipes/
%{_bindir}/guestfish
%{_mandir}/man1/guestfish.1*


%files -n virt-inspector
%defattr(-,root,root,-)
%{_bindir}/virt-inspector
%{_mandir}/man1/virt-inspector.1*


%files -n ocaml-%{name}
%defattr(-,root,root,-)
%doc README
%{_libdir}/ocaml/guestfs
%exclude %{_libdir}/ocaml/guestfs/*.a
%exclude %{_libdir}/ocaml/guestfs/*.cmxa
%exclude %{_libdir}/ocaml/guestfs/*.cmx
%exclude %{_libdir}/ocaml/guestfs/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files -n ocaml-%{name}-devel
%defattr(-,root,root,-)
%doc ocaml/ex
%{_libdir}/ocaml/guestfs/*.a
%{_libdir}/ocaml/guestfs/*.cmxa
%{_libdir}/ocaml/guestfs/*.cmx
%{_libdir}/ocaml/guestfs/*.mli


%files -n perl-%{name}
%defattr(-,root,root,-)
%doc perl/examples
%{perl_vendorarch}/*
%{_mandir}/man3/Sys::Guestfs.3pm*


%files -n python-%{name}
%defattr(-,root,root,-)
%doc README
%{python_sitearch}/*
%{python_sitelib}/*.py
%{python_sitelib}/*.pyc
%{python_sitelib}/*.pyo


%files -n ruby-%{name}
%defattr(-,root,root,-)
%doc README
%{ruby_sitelib}/guestfs.rb
%{ruby_sitearch}/_guestfs.so


%files java
%defattr(-,root,root,-)
%doc README
%{_libdir}/libguestfs_jni*.so.*
%{_datadir}/java/*.jar


%files java-devel
%defattr(-,root,root,-)
%doc README
%{_libdir}/libguestfs_jni*.so


%files javadoc
%defattr(-,root,root,-)
%doc README
%{_datadir}/javadoc/%{name}-java-%{version}


%changelog
* Tue Jun 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.48-2
- Accidentally omitted the supermin image from previous version.

* Tue Jun 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.48-1
- New upstream release 1.0.48.
- Should fix all the brokenness from 1.0.47.
- Requires febootstrap >= 2.3.

* Mon Jun 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.47-2
- New upstream release 1.0.47.
- Enable experimental supermin appliance build.
- Fix path to appliance.

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.45-2
- New upstream release 1.0.45.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-2
- Disable ppc/ppc64 tests again because of RHBZ#505109.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-1
- New upstream version 1.0.44.
- Try enabling tests on ppc & ppc64 since it looks like the bug(s?)
  in qemu which might have caused them to fail have been fixed.

* Tue Jun  9 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.43-1
- New upstream version 1.0.43.
- New upstream URL.
- Requires chntpw program.

* Sat Jun  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.42-1
- New upstream version 1.0.42.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.41-1
- New upstream version 1.0.41.
- Fixes a number of regressions in RHBZ#503169.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.40-1
- New upstream version 1.0.40.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.39-1
- New upstream version 1.0.39.
- Fixes:
  . libguestfs /dev is too sparse for kernel installation/upgrade (RHBZ#503169)
  . OCaml bindings build failure (RHBZ#502309)

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-2
- Disable tests on ix86 because of RHBZ#503236.

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-1
- New upstream version 1.0.38.

* Fri May 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.37-1
- New upstream version 1.0.37.
- Fixes:
  . "mkdir-p" should not throw errors on preexisting directories (RHBZ#503133)
  . cramfs and squashfs modules should be available in libguestfs appliances
      (RHBZ#503135)

* Thu May 28 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.36-2
- New upstream version 1.0.36.
- Rerun the generator in prep section.

* Thu May 28 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.35-1
- New upstream version 1.0.35.
- Fixes multiple bugs in bindings parameters (RHBZ#501892).

* Wed May 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.34-1
- New upstream version 1.0.34.

* Wed May 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.33-1
- New upstream version 1.0.33.
- --with-java-home option is no longer required.
- Upstream contains potential fixes for:
    501878 built-in commands like 'alloc' and 'help' don't autocomplete
    501883 javadoc messed up in libguestfs java documentation
    501885 Doesn't detect missing Java, --with-java-home=no should not be needed
    502533 Polish translation of libguestfs
    n/a    Allow more ext filesystem kmods (Charles Duffy)

* Tue May 26 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.32-2
- New upstream version 1.0.32.
- Use %%find_lang macro.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.31-1
- Rebuild for OCaml 3.11.1.
- New upstream version 1.0.31.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.30-1
- New upstream version 1.0.30.  Now includes test-bootbootboot.sh script.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.29-3
- New upstream version 1.0.29 (fixes RHBZ#502007 RHBZ#502018).
- This should allow us to enable tests for i386 and x86-64.
- Added test-bootbootboot.sh script which was missed from 1.0.29 tarball.
- Pass kernel noapic flag to workaround RHBZ#502058.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.28-1
- New upstream version 1.0.28.  Nothing has visibly changed, but
  the source has been gettextized and we want to check that doesn't
  break anything.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.27-3
- Change requirement from qemu -> qemu-kvm (RHBZ#501761).

* Tue May 19 2009 Richard Jones <rjones@redhat.com> - 1.0.27-2
- New upstream version 1.0.27.

* Mon May 18 2009 Richard Jones <rjones@redhat.com> - 1.0.26-6
- Experimentally try to reenable ppc and ppc64 builds.
- Note BZ numbers which are causing tests to fail.

* Mon May 18 2009 Richard Jones <rjones@redhat.com> - 1.0.26-1
- New upstream version 1.0.26.

* Tue May 12 2009 Richard Jones <rjones@redhat.com> - 1.0.25-4
- New upstream version 1.0.25.
- Enable debugging when running the tests.
- Disable tests - don't work correctly in Koji.

* Tue May 12 2009 Richard Jones <rjones@redhat.com> - 1.0.24-1
- New upstream version 1.0.24.
- BRs glibc-static for the new command tests.
- Enable tests.

* Mon May 11 2009 Richard Jones <rjones@redhat.com> - 1.0.23-2
- New upstream version 1.0.23.
- Don't try to use updates during build.

* Fri May  8 2009 Richard Jones <rjones@redhat.com> - 1.0.21-3
- New upstream version 1.0.21.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.0.20-2
- New upstream version 1.0.20.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.0.19-1
- New upstream version 1.0.19.

* Tue Apr 28 2009 Richard Jones <rjones@redhat.com> - 1.0.15-1
- New upstream version 1.0.15.

* Fri Apr 24 2009 Richard Jones <rjones@redhat.com> - 1.0.12-1
- New upstream version 1.0.12.

* Wed Apr 22 2009 Richard Jones <rjones@redhat.com> - 1.0.6-1
- New upstream version 1.0.6.

* Mon Apr 20 2009 Richard Jones <rjones@redhat.com> - 1.0.2-1
- New upstream version 1.0.2.

* Thu Apr 16 2009 Richard Jones <rjones@redhat.com> - 0.9.9-12
- Multiple fixes to get it to scratch build in Koji.

* Sat Apr  4 2009 Richard Jones <rjones@redhat.com> - 0.9.9-1
- Initial build.
