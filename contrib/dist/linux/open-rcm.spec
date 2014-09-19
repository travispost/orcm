#
# Copyright (c) 2004-2005 The Trustees of Indiana University and Indiana
#                         University Research and Technology
#                         Corporation.  All rights reserved.
# Copyright (c) 2004-2005 The University of Tennessee and The University
#                         of Tennessee Research Foundation.  All rights
#                         reserved.
# Copyright (c) 2004-2005 High Performance Computing Center Stuttgart,
#                         University of Stuttgart.  All rights reserved.
# Copyright (c) 2004-2005 The Regents of the University of California.
#                         All rights reserved.
# Copyright (c) 2006      Cisco Systems, Inc.  All rights reserved.
# $COPYRIGHT$
#
# Additional copyrights may follow
#
# $HEADER$
#

# don't stop with an error if we don't pack all files at once
%define _unpackaged_files_terminate_build  0

# macros to select which part of the specfile should be active
%{!?build_build: %define build_build 0}
%{!?build_install: %define build_install 0}
%{!?build_default: %define build_default 1}

#
# global Open MPI stuff
#
Prefix: /opt/open-rcm
%define ompi_name rcm
%define ompi_name_prefix open-
%define ompi_version 0.5rc1git0336663
%{!?ompi_package_version:%define ompi_package_version default}
%define ompi_extra_version %{nil}
%define ompi_release 1
%define ompi_prefix  /opt/open-rcm/%{ompi_version}
%define ompi_build_root %{_tmppath}/%{ompi_name}-%{ompi_version}-%{ompi_release}-root
%define ompi_source %{ompi_name_prefix}%{ompi_name}-%{ompi_version}.tar.gz
%define ompi_url http://www.open-mpi.org
%define ompi_specfile %{_topdir}/SPECS/open-rcm-%{ompi_version}.spec
%{!?configure_options: %define configure_options  %{nil}}
%define configure_options "--with-platform=contrib/platform/intel/hillsboro/orcm-linux"
%define ompi_configure_params  %{nil}
%define ompi_compile_root %{ompi_name_prefix}%{ompi_name}-%{ompi_version}


#
# fix configure 
#
%define _prefix %{ompi_prefix}
%define _sysconfdir %{_prefix}/etc
%define _libdir %{_prefix}/lib64
%define _includedir %{_prefix}/include
%define _mandir %{_prefix}/share/man
%define _pkgdatadir %{_prefix}/share/openmpi


#
# compiler settings
#
%define ompi_compiler default
%define ompi_cc  " "
%define ompi_cxx " "
%define ompi_f77 " "
%define ompi_fc  " "


######################################################################
#
# Build section
#
######################################################################
%if %{build_build}
Summary: Configure and build the Open MPI tree
Name: %{ompi_name_prefix}%{ompi_name}
Version: %{ompi_version}
Release: %{ompi_release}
License: BSD
Group: Others
URL: %{ompi_url}
Source0: %{ompi_source}
BuildRoot: %{ompi_build_root}

%description
This part build and install the Open MPI source tree.

%prep
%setup -q

%build
OMPI_CONFIGURE_FLAGS="%{ompi_configure_params}"
OMPI_CONFIGURE_OPTIONS="%{configure_options}"
if [ "%{ompi_compiler}" != "default" ]; then
OMPI_CONFIGURE_FLAGS="$OMPI_CONFIGURE_FLAGS CC=%{ompi_cc} CXX=%{ompi_cxx} F77=%{ompi_f77} FC=%{ompi_fc}"
fi

%configure $OMPI_CONFIGURE_FLAGS $OMPI_CONFIGURE_OPTIONS
make -j4

%install

%clean

%files 
%defattr(-,root,root,-)
%{_sysconfdir}/*
%{_prefix}/bin/*
%{_libdir}/*
%{_includedir}/*
%doc %{_pkgdatadir}/*
%doc %{_mandir}/man1/*
%doc %{_mandir}/man7/*
%endif 


######################################################################
#
# Install section
#
######################################################################
%if %{build_install}
Summary: Install a already compiled tree 
Name: %{ompi_name_prefix}%{ompi_name}
Version: %{ompi_version}
Release: %{ompi_release}
License: BSD
Group: Others
URL: %{ompi_url}
Source0: %{ompi_source}
BuildRoot: %{ompi_build_root}

%description
This part build and install the Open MPI source tree.

%prep

%build


%install
cd %{ompi_compile_root}
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


#
# create a module file on request
#
if [ 1 == 0 ] ; then 
%{__mkdir_p} $RPM_BUILD_ROOT/nirwana/%{ompi_name}/
cat <<EOF >$RPM_BUILD_ROOT/nirwana/%{ompi_name}/%{ompi_version}
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI RPM).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds Open MPI v0.5rc1gite958cca to various paths"
}

module-whatis   "Sets up Open MPI v0.5rc1gite958cca in your enviornment"

append-path PATH "%{_prefix}/bin/"
append-path LD_LIBRARY_PATH %{_libdir}
append-path MANPATH %{_mandir}
EOF
fi


#
# profile.d files
#
if [ 1 == 0 ] ; then
%{__mkdir_p} $RPM_BUILD_ROOT/etc/profile.d/
cat <<EOF > $RPM_BUILD_ROOT/etc/profile.d/%{ompi_name}-%{ompi_version}.sh
# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI RPM).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

CHANGED=0
if test -z "`echo $PATH | grep %{_prefix}/bin`"; then
    PATH=\${PATH}:%{_prefix}/bin/
    CHANGED=1
fi
if test -z "`echo $LD_LIBRARY_PATH | grep %{_libdir}`"; then
    LD_LIBRARY_PATH=\${LD_LIBRARY_PATH}:%{_libdir}
    CHANGED=1
fi
if test -z "`echo $MANPATH | grep %{_mandir}`"; then
    MANPATH=\${MANPATH}:%{_mandir}
    CHANGED=1
fi
if test "$CHANGED" = "1"; then
    export PATH LD_LIBRARY_PATH MANPATH
fi
EOF

cat <<EOF > $RPM_BUILD_ROOT/etc/profile.d/%{ompi_name}-%{ompi_version}s.csh
# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI RPM).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

if ("`echo $PATH | grep %{_prefix}/bin`") then
    setenv PATH \${PATH}:%{_prefix}/bin/
endif
if ("$?LD_LIBRARY_PATH") then
    if ("`echo $LD_LIBRARY_PATH | grep %{_libdir}`") then
        setenv LD_LIBRARY_PATH \${LD_LIBRARY_PATH}:%{_libdir}
    endif
endif
if ("$?MANPATH") then
    if ("`echo $MANPATH | grep %{_mandir}`") then
        setenv MANPATH \${MANPATH}:%{_mandir}
    endif
endif
EOF
fi


%clean

%files 
%defattr(-,root,root,-)
%{_sysconfdir}/*
%{_prefix}/bin/*
%{_libdir}/*
%{_includedir}/*
%doc %{_pkgdatadir}/*
%doc %{_mandir}/man1/*
%doc %{_mandir}/man7/*

%endif 


######################################################################
#
# default  
#
######################################################################
%if %{build_default}
Summary: Open MPI 
Name: %{ompi_name_prefix}%{ompi_name}
Version: %{ompi_version}%{ompi_extra_version}
Release: %{ompi_release}
License: %{ompi_license}
Group: Development/Library
URL: %{ompi_url}
Source0: %{ompi_source}
BuildRoot: %{ompi_build_root}

%description
Open MPI is a project combining technologies and resources from
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in
order to build the best MPI library available.

This RPM contains all the tools necessary to compile, link, and run
Open MPI jobs. Additional this RPM also contains modules for communicating
via shared memory and TCP networks. Components for other transports (e.g.
Myrinet, Infiniband, ...) are provided in separate RPMs.


%prep

%build

BUILD_PACKAGE=1
for entry in /no_build; do
    for file in  $RPM_BUILD_ROOT/$entry; do
        if [ -e $file ] ; then
            BUILD_PACKAGE=1
        fi
    done
done
if [ $BUILD_PACKAGE == 1 ] ; then 
eval export OMPI_PACKAGE_VERSION=`/bin/echo unknown`
rpmbuild -bc --define '_topdir %_topdir'  --define 'build_build 1' --define 'build_default 0' --define "ompi_package_version $OMPI_PACKAGE_VERSION" %{ompi_specfile}
fi

BUILD_PACKAGE=1
for entry in /no_install; do
    for file in  $RPM_BUILD_ROOT/$entry; do
        if [ -e $file ] ; then
            BUILD_PACKAGE=1
        fi
    done
done
if [ $BUILD_PACKAGE == 1 ] ; then 
eval export OMPI_PACKAGE_VERSION=`/bin/echo unknown`
rpmbuild -bi --define '_topdir %_topdir'  --define 'build_install 1' --define 'build_default 0' --define "ompi_package_version $OMPI_PACKAGE_VERSION" %{ompi_specfile}
fi


%install
cd %{ompi_compile_root}
#rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
#rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/*
%{_prefix}/bin/*
%{_libdir}/*
%{_includedir}/*
%doc %{_pkgdatadir}/*
%doc %{_mandir}/man1/*
%doc %{_mandir}/man7/*
#%{ompi_prefix}

%endif


#############################################################################
#
# Changelog
#
#############################################################################
%changelog
* Tue Jun 27 2006 Sven Stork <stork@hlrs.de>
- switch to specfile generator

* Wed Apr 26 2006 Jeff Squyres <jsquyres@cisco.com>
- Revamp files listings to ensure that rpm -e will remove directories
  if rpm -i created them.
- Simplify options for making modulefiles and profile.d scripts.
- Add oscar define.
- Ensure to remove the previous installation root during prep.
- Cleanup the modulefile specification and installation; also ensure
  that the profile.d scripts get installed if selected.
- Ensure to list sysconfdir in the files list if it's outside of the
  prefix.

* Wed Mar 30 2006 Jeff Squyres <jsquyres@cisco.com>
- Lots of bit rot updates
- Reorganize and rename the subpackages
- Add / formalize a variety of rpmbuild --define options
- Comment out the docs subpackage for the moment (until we have some
  documentation -- coming in v1.1!)

* Wed May 03 2005 Jeff Squyres <jsquyres@open-mpi.org>
- Added some defines for LANL defaults
- Added more defines for granulatirty of installation location for
  modulefile
- Differentiate between installing in /opt and whether we want to
  install environment script files
- Filled in files for man and mca-general subpackages

* Thu Apr 07 2005 Greg Kurtzer <GMKurtzer@lbl.gov>
- Added opt building
- Added profile.d/modulefile logic and creation
- Minor cleanups

* Fri Apr 01 2005 Greg Kurtzer <GMKurtzer@lbl.gov>
- Added comments
- Split package into subpackages
- Cleaned things up a bit
- Sold the code to Microsoft, and now I am retiring. Thanks guys!

* Wed Mar 23 2005 Mezzanine <mezzanine@kainx.org>
- Specfile auto-generated by Mezzanine



